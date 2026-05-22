"""Create executable Jupyter notebooks without requiring nbformat."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

BOOTSTRAP = r"""
from pathlib import Path
import sys

try:
    import google.colab  # type: ignore
    IN_COLAB = True
except Exception:
    IN_COLAB = False

if IN_COLAB and not Path("mp-1").exists():
    !git clone https://github.com/megusto0/mp-1.git
    %cd mp-1

ROOT = Path.cwd()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
"""


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
        md("# 01. Аналитическое исследование\n\nВариант 16: раскрываем функцию, находим градиент, Гессиан и точку минимума."),
        code(BOOTSTRAP),
        code(
            """
import sympy as sp
from src.target import Q, B, C, X_STAR, F_STAR

x, y = sp.symbols("x y")
expr = 2 * (x - 3) ** 2 + 3 * (y + 2) ** 2 - 2 * x * y + 4 * x - 6 * y
print("f expanded =", sp.expand(expr))
print("grad =", [sp.diff(expr, x), sp.diff(expr, y)])
print("stationary =", sp.solve([sp.diff(expr, x), sp.diff(expr, y)], [x, y]))
print("Hessian =", sp.hessian(expr, (x, y)))
print("x* =", X_STAR, "f* =", F_STAR)
"""
        ),
        code(
            """
from src.plotting import save_surface_contour
save_surface_contour("figures/fig_3_4_surface_contour.png")
"""
        ),
    ],
    "02_nelder_mead.ipynb": [
        md("# 02. Метод Нелдера-Мида\n\nПоказываем последовательность симплексов и таблицу сходимости."),
        code(BOOTSTRAP),
        code(
            """
from scripts.generate_artifacts import generate
generate()
"""
        ),
    ],
    "03_hooke_jeeves.ipynb": [
        md("# 03. Метод Хука-Дживса\n\nИспользуется метод деления отрезка пополам для одномерного поиска шага."),
        code(BOOTSTRAP),
        code(
            """
from src.hooke_jeeves import hooke_jeeves
from src.target import X0, EPS, f
result = hooke_jeeves(f, X0, tol=EPS)
print(result.x, result.fun, result.iterations)
"""
        ),
        code("from scripts.generate_artifacts import generate\ngenerate()"),
    ],
    "04_steepest_descent.ipynb": [
        md("# 04. Метод наискорейшего спуска\n\nОптимальный шаг для квадратичной функции вычисляется явно."),
        code(BOOTSTRAP),
        code(
            """
from src.gradient_methods import steepest_descent
from src.target import X0, EPS, Q, f, grad
result = steepest_descent(f, grad, Q, X0, tol=EPS)
print(result.x, result.fun, result.iterations)
"""
        ),
        code("from scripts.generate_artifacts import generate\ngenerate()"),
    ],
    "05_fletcher_reeves.ipynb": [
        md("# 05. Метод Флетчера-Ривса\n\nМетод сопряженных градиентов для квадратичной функции двух переменных."),
        code(BOOTSTRAP),
        code(
            """
from src.gradient_methods import fletcher_reeves
from src.target import X0, EPS, Q, f, grad
result = fletcher_reeves(f, grad, Q, X0, tol=EPS)
print(result.x, result.fun, result.iterations)
"""
        ),
        code("from scripts.generate_artifacts import generate\ngenerate()"),
    ],
    "06_comparison.ipynb": [
        md("# 06. Сравнение методов\n\nФормируем таблицу сравнения и общий график сходимости."),
        code(BOOTSTRAP),
        code("from scripts.generate_artifacts import generate\ngenerate()"),
        code(
            """
import pandas as pd
pd.read_csv("tables/tab_5_compare.csv")
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
