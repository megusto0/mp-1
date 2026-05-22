"""Plot helpers for the optimization report."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .target import F_STAR, X_STAR, original_formula


def _grid():
    x = np.linspace(-1.0, 4.0, 220)
    y = np.linspace(-3.0, 2.0, 220)
    xx, yy = np.meshgrid(x, y)
    zz = original_formula(xx, yy)
    return xx, yy, zz


def save_surface_contour(path: str | Path) -> None:
    """Save surface and contour plots for the target function."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    xx, yy, zz = _grid()
    fig = plt.figure(figsize=(12, 5), dpi=180)
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(xx, yy, zz, cmap="viridis", linewidth=0, alpha=0.9)
    ax1.scatter([X_STAR[0]], [X_STAR[1]], [F_STAR], color="red", s=45)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("f(x, y)")
    ax1.set_title("Поверхность функции")

    ax2 = fig.add_subplot(1, 2, 2)
    contour = ax2.contour(xx, yy, zz, levels=22, cmap="viridis")
    ax2.clabel(contour, inline=True, fontsize=7)
    ax2.scatter([X_STAR[0]], [X_STAR[1]], color="red", marker="*", s=110, label="x*")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_title("Линии уровня")
    ax2.grid(True, alpha=0.25)
    ax2.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_path_plot(path: str | Path, points: np.ndarray, title: str, simplexes=None) -> None:
    """Save contour plot with an optimization trajectory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    xx, yy, zz = _grid()
    fig, ax = plt.subplots(figsize=(7, 5), dpi=180)
    contour = ax.contour(xx, yy, zz, levels=25, cmap="viridis")
    ax.clabel(contour, inline=True, fontsize=7)
    if simplexes is not None:
        for simplex in simplexes:
            closed = np.vstack([simplex, simplex[0]])
            ax.plot(closed[:, 0], closed[:, 1], color="#4b5563", alpha=0.35, linewidth=1)
    ax.plot(points[:, 0], points[:, 1], marker="o", linewidth=1.8, markersize=3.5, label="траектория")
    ax.scatter([points[0, 0]], [points[0, 1]], color="#2563eb", s=45, label="x0")
    ax.scatter([X_STAR[0]], [X_STAR[1]], color="red", marker="*", s=120, label="x*")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def save_convergence_plot(path: str | Path, series: dict[str, list[float]]) -> None:
    """Save convergence plot for all methods."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5), dpi=180)
    for name, values in series.items():
        err = np.maximum(np.array(values, dtype=float) - F_STAR, 1e-12)
        ax.semilogy(range(len(values)), err, marker="o", markersize=3, linewidth=1.5, label=name)
    ax.set_xlabel("Номер итерации")
    ax.set_ylabel("f(x_k) - f*")
    ax.set_title("Сравнение сходимости")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
