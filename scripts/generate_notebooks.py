"""Create standalone Colab-friendly Jupyter notebooks without nbformat."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
REPO = "megusto0/mp-1"
BRANCH = "master"

INSTALL = "!pip install -q numpy pandas sympy matplotlib\n"

TARGET_CODE = r"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Path("figures").mkdir(exist_ok=True)
Path("tables").mkdir(exist_ok=True)

Q = np.array([[4.0, -2.0], [-2.0, 6.0]])
B = np.array([-8.0, 6.0])
C = 30.0
X0 = np.array([0.0, 0.0])
EPS = 1e-4
X_STAR = np.linalg.solve(Q, -B)
F_STAR = 21.6

def f(point):
    x = np.asarray(point, dtype=float)
    return float(0.5 * x @ Q @ x + B @ x + C)

def grad(point):
    x = np.asarray(point, dtype=float)
    return Q @ x + B

def original_formula(x, y):
    return 2 * (x - 3) ** 2 + 3 * (y + 2) ** 2 - 2 * x * y + 4 * x - 6 * y

def grid():
    x = np.linspace(-1.0, 4.0, 220)
    y = np.linspace(-3.0, 2.0, 220)
    xx, yy = np.meshgrid(x, y)
    return xx, yy, original_formula(xx, yy)

def plot_path(points, title, simplexes=None, out=None):
    xx, yy, zz = grid()
    fig, ax = plt.subplots(figsize=(7, 5), dpi=130)
    contour = ax.contour(xx, yy, zz, levels=25, cmap="viridis")
    ax.clabel(contour, inline=True, fontsize=7)
    if simplexes is not None:
        for simplex in simplexes:
            closed = np.vstack([simplex, simplex[0]])
            ax.plot(closed[:, 0], closed[:, 1], color="#4b5563", alpha=0.35, linewidth=1)
    points = np.asarray(points)
    ax.plot(points[:, 0], points[:, 1], marker="o", linewidth=1.8, markersize=3.5, label="траектория")
    ax.scatter([points[0, 0]], [points[0, 1]], color="#2563eb", s=45, label="x0")
    ax.scatter([X_STAR[0]], [X_STAR[1]], color="red", marker="*", s=120, label="x*")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    if out:
        fig.savefig(out, bbox_inches="tight")
    plt.show()
"""

NELDER_CODE = r"""
def nelder_mead(func, x0, step=1.0, tol=1e-4, max_iter=300, alpha=1.0, gamma=2.0, beta=0.5, sigma=0.5):
    x0 = np.asarray(x0, dtype=float)
    simplex = [x0]
    for i in range(len(x0)):
        vertex = x0.copy()
        vertex[i] += step
        simplex.append(vertex)
    simplex = np.array(simplex, dtype=float)
    history = []

    for iteration in range(max_iter + 1):
        values = np.array([func(vertex) for vertex in simplex])
        order = np.argsort(values)
        simplex = simplex[order]
        values = values[order]
        spread = float(np.max(values) - np.min(values))
        history.append({
            "iter": iteration,
            "simplex": simplex.copy(),
            "best_x": simplex[0].copy(),
            "best_f": float(values[0]),
            "spread": spread,
        })
        if spread < tol:
            break

        centroid = simplex[:-1].mean(axis=0)
        worst = simplex[-1]
        reflected = centroid + alpha * (centroid - worst)
        f_reflected = func(reflected)

        if f_reflected < values[0]:
            expanded = centroid + gamma * (reflected - centroid)
            simplex[-1] = expanded if func(expanded) < f_reflected else reflected
        elif f_reflected < values[-2]:
            simplex[-1] = reflected
        else:
            if f_reflected < values[-1]:
                contracted = centroid + beta * (reflected - centroid)
            else:
                contracted = centroid - beta * (centroid - worst)
            if func(contracted) < min(f_reflected, values[-1]):
                simplex[-1] = contracted
            else:
                best = simplex[0].copy()
                simplex = best + sigma * (simplex - best)

    best = history[-1]["best_x"]
    return best, float(func(best)), history
"""

HOOKE_CODE = r"""
def bisection_min(func, a, b, tol=1e-4):
    while (b - a) > tol:
        mid = (a + b) / 2.0
        left = a + (b - a) / 4.0
        right = b - (b - a) / 4.0
        f_left, f_mid, f_right = func(left), func(mid), func(right)
        if f_left < f_mid:
            b = mid
        elif f_right < f_mid:
            a = mid
        else:
            a, b = left, right
    t = (a + b) / 2.0
    return t, float(func(t))

def exploratory_search(func, base, delta):
    point = base.copy()
    for i in range(len(point)):
        best_value = func(point)
        trial = point.copy()
        trial[i] += delta
        if func(trial) < best_value:
            point = trial
            continue
        trial = point.copy()
        trial[i] -= delta
        if func(trial) < best_value:
            point = trial
    return point

def hooke_jeeves(func, x0, delta=1.0, tol=1e-4, max_iter=300):
    base = np.asarray(x0, dtype=float)
    history = []
    iteration = 0
    while delta > tol and iteration < max_iter:
        explored = exploratory_search(func, base, delta)
        if func(explored) < func(base):
            direction = explored - base
            phi = lambda t: func(explored + t * direction)
            t_star, _ = bisection_min(phi, 0.0, 2.0, tol)
            candidate = explored + t_star * direction
            base = candidate if func(candidate) < func(base) else explored
        else:
            delta *= 0.5
        history.append({"iter": iteration, "x": base.copy(), "f": float(func(base)), "delta": float(delta)})
        iteration += 1
    return base, float(func(base)), history
"""

GRADIENT_CODE = r"""
def steepest_descent(func, grad_func, q_matrix, x0, tol=1e-4, max_iter=300):
    x = np.asarray(x0, dtype=float)
    history = []
    for iteration in range(max_iter + 1):
        g = grad_func(x)
        norm_g = float(np.linalg.norm(g))
        history.append({"iter": iteration, "x": x.copy(), "f": float(func(x)), "grad_norm": norm_g})
        if norm_g < tol:
            break
        alpha = float((g @ g) / (g @ q_matrix @ g))
        x = x - alpha * g
    return x, float(func(x)), history

def fletcher_reeves(func, grad_func, q_matrix, x0, tol=1e-4, max_iter=300):
    x = np.asarray(x0, dtype=float)
    g = grad_func(x)
    direction = -g
    history = []
    for iteration in range(max_iter + 1):
        norm_g = float(np.linalg.norm(g))
        history.append({"iter": iteration, "x": x.copy(), "f": float(func(x)), "grad_norm": norm_g})
        if norm_g < tol:
            break
        alpha = float(-(g @ direction) / (direction @ q_matrix @ direction))
        x_next = x + alpha * direction
        g_next = grad_func(x_next)
        beta = float((g_next @ g_next) / (g @ g))
        direction = -g_next + beta * direction
        x, g = x_next, g_next
    return x, float(func(x)), history
"""


def colab_url(name: str) -> str:
    return f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/notebooks/{name}"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip().splitlines(True),
    }


def badge(name: str, title: str, lead: str) -> dict:
    return md(
        f"""
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(name)})

# {title}

{lead}
"""
    )


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOK_DATA = {
    "01_analysis.ipynb": [
        badge(
            "01_analysis.ipynb",
            "01. Аналитическое исследование",
            "Раскрываем функцию, находим градиент, Гессиан и точку глобального минимума.",
        ),
        code(INSTALL),
        code(
            r"""
import sympy as sp
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

Path("figures").mkdir(exist_ok=True)
x, y = sp.symbols("x y")
expr = 2 * (x - 3) ** 2 + 3 * (y + 2) ** 2 - 2 * x * y + 4 * x - 6 * y
expanded = sp.expand(expr)
grad_expr = [sp.diff(expr, x), sp.diff(expr, y)]
hessian = sp.hessian(expr, (x, y))
stationary = sp.solve(grad_expr, [x, y])
print("f(x, y) =", expanded)
print("grad f =", grad_expr)
print("H =", hessian)
print("stationary point =", stationary)
"""
        ),
        code(TARGET_CODE),
        code(
            r"""
xx, yy, zz = grid()
fig = plt.figure(figsize=(12, 5), dpi=130)
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(xx, yy, zz, cmap="viridis", linewidth=0, alpha=0.9)
ax1.scatter([X_STAR[0]], [X_STAR[1]], [F_STAR], color="red", s=45)
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("f(x, y)")
ax1.set_title("Поверхность функции")

ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(xx, yy, zz, levels=22, cmap="viridis")
ax2.clabel(contour, inline=True, fontsize=7)
ax2.scatter([X_STAR[0]], [X_STAR[1]], color="red", marker="*", s=110, label="x*")
ax2.set_xlabel("x"); ax2.set_ylabel("y")
ax2.set_title("Линии уровня")
ax2.grid(True, alpha=0.25)
ax2.legend()
fig.tight_layout()
fig.savefig("figures/fig_3_4_surface_contour.png", bbox_inches="tight")
plt.show()
"""
        ),
    ],
    "02_nelder_mead.ipynb": [
        badge(
            "02_nelder_mead.ipynb",
            "02. Метод Нелдера-Мида",
            "Реализуем метод деформируемого симплекса и показываем последовательность симплексов.",
        ),
        code(INSTALL),
        code(TARGET_CODE),
        code(NELDER_CODE),
        code(
            r"""
x_min, f_min, history = nelder_mead(f, X0, tol=EPS)
print("x =", x_min, "f =", f_min, "iterations =", history[-1]["iter"])

rows = []
for item in history[:8] + [history[-1]]:
    x = item["best_x"]
    rows.append([item["iter"], x[0], x[1], item["best_f"], item["spread"]])
df = pd.DataFrame(rows, columns=["k", "x", "y", "f_best", "spread"])
df.to_csv("tables/tab_4_1_nm.csv", index=False)
display(df)

points = np.array([item["best_x"] for item in history])
simplexes = [item["simplex"] for item in history[:: max(1, len(history) // 12)]]
plot_path(points, "Метод Нелдера-Мида", simplexes, "figures/fig_4_1_nm_trajectory.png")
"""
        ),
    ],
    "03_hooke_jeeves.ipynb": [
        badge(
            "03_hooke_jeeves.ipynb",
            "03. Метод Хука-Дживса",
            "Используем исследующий поиск и метод деления отрезка пополам для поиска шага.",
        ),
        code(INSTALL),
        code(TARGET_CODE),
        code(HOOKE_CODE),
        code(
            r"""
x_min, f_min, history = hooke_jeeves(f, X0, tol=EPS)
print("x =", x_min, "f =", f_min, "iterations =", len(history))

rows = []
for item in history[:8] + [history[-1]]:
    x = item["x"]
    rows.append([item["iter"], x[0], x[1], item["f"], item["delta"]])
df = pd.DataFrame(rows, columns=["k", "x_k", "y_k", "f(x_k)", "delta"])
df.to_csv("tables/tab_4_2_hj.csv", index=False)
display(df)

plot_path(np.array([item["x"] for item in history]), "Метод Хука-Дживса", out="figures/fig_4_2_hj_trajectory.png")
"""
        ),
    ],
    "04_steepest_descent.ipynb": [
        badge(
            "04_steepest_descent.ipynb",
            "04. Метод наискорейшего спуска",
            "Оптимальный шаг для квадратичной функции вычисляется по явной формуле.",
        ),
        code(INSTALL),
        code(TARGET_CODE),
        code(GRADIENT_CODE),
        code(
            r"""
x_min, f_min, history = steepest_descent(f, grad, Q, X0, tol=EPS)
print("x =", x_min, "f =", f_min, "iterations =", history[-1]["iter"])

rows = []
for item in history[:8] + [history[-1]]:
    x = item["x"]
    rows.append([item["iter"], x[0], x[1], item["f"], item["grad_norm"]])
df = pd.DataFrame(rows, columns=["k", "x_k", "y_k", "f(x_k)", "grad_norm"])
df.to_csv("tables/tab_4_3_sd.csv", index=False)
display(df)

plot_path(np.array([item["x"] for item in history]), "Метод наискорейшего спуска", out="figures/fig_4_3_sd_trajectory.png")
"""
        ),
    ],
    "05_fletcher_reeves.ipynb": [
        badge(
            "05_fletcher_reeves.ipynb",
            "05. Метод Флетчера-Ривса",
            "Метод сопряженных градиентов для положительно определенной квадратичной функции.",
        ),
        code(INSTALL),
        code(TARGET_CODE),
        code(GRADIENT_CODE),
        code(
            r"""
x_min, f_min, history = fletcher_reeves(f, grad, Q, X0, tol=EPS)
print("x =", x_min, "f =", f_min, "iterations =", history[-1]["iter"])

rows = []
for item in history:
    x = item["x"]
    rows.append([item["iter"], x[0], x[1], item["f"], item["grad_norm"]])
df = pd.DataFrame(rows, columns=["k", "x_k", "y_k", "f(x_k)", "grad_norm"])
df.to_csv("tables/tab_4_4_fr.csv", index=False)
display(df)

plot_path(np.array([item["x"] for item in history]), "Метод Флетчера-Ривса", out="figures/fig_4_4_fr_trajectory.png")
"""
        ),
    ],
    "06_comparison.ipynb": [
        badge(
            "06_comparison.ipynb",
            "06. Сравнение методов",
            "Сводим результаты всех методов в одну таблицу и строим общий график сходимости.",
        ),
        code(INSTALL),
        code(TARGET_CODE),
        code(NELDER_CODE + "\n" + HOOKE_CODE + "\n" + GRADIENT_CODE),
        code(
            r"""
nm_x, nm_f, nm_h = nelder_mead(f, X0, tol=EPS)
hj_x, hj_f, hj_h = hooke_jeeves(f, X0, tol=EPS)
sd_x, sd_f, sd_h = steepest_descent(f, grad, Q, X0, tol=EPS)
fr_x, fr_f, fr_h = fletcher_reeves(f, grad, Q, X0, tol=EPS)

compare = pd.DataFrame([
    ["Нелдер-Мид", nm_h[-1]["iter"], nm_x[0], nm_x[1], nm_f, np.linalg.norm(nm_x - X_STAR)],
    ["Хук-Дживс", len(hj_h), hj_x[0], hj_x[1], hj_f, np.linalg.norm(hj_x - X_STAR)],
    ["Наискорейший спуск", sd_h[-1]["iter"], sd_x[0], sd_x[1], sd_f, np.linalg.norm(sd_x - X_STAR)],
    ["Флетчер-Ривс", fr_h[-1]["iter"], fr_x[0], fr_x[1], fr_f, np.linalg.norm(fr_x - X_STAR)],
], columns=["Метод", "Итерации", "x", "y", "f", "||x-x*||"])
compare.to_csv("tables/tab_5_compare.csv", index=False)
display(compare)

series = {
    "Нелдер-Мид": [item["best_f"] for item in nm_h],
    "Хук-Дживс": [item["f"] for item in hj_h],
    "Наискорейший спуск": [item["f"] for item in sd_h],
    "Флетчер-Ривс": [item["f"] for item in fr_h],
}
fig, ax = plt.subplots(figsize=(7, 5), dpi=130)
for name, values in series.items():
    err = np.maximum(np.array(values) - F_STAR, 1e-12)
    ax.semilogy(range(len(values)), err, marker="o", markersize=3, linewidth=1.5, label=name)
ax.set_xlabel("Номер итерации")
ax.set_ylabel("f(x_k) - f*")
ax.set_title("Сравнение сходимости")
ax.grid(True, which="both", alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig("figures/fig_5_convergence.png", bbox_inches="tight")
plt.show()
"""
        ),
    ],
}


def main() -> None:
    NOTEBOOKS.mkdir(exist_ok=True)
    for name, cells in NOTEBOOK_DATA.items():
        path = NOTEBOOKS / name
        path.write_text(json.dumps(notebook(cells), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
