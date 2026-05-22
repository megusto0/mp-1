"""Gradient methods for a positive definite quadratic function."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class GradientResult:
    x: np.ndarray
    fun: float
    iterations: int
    history: list[dict]


def steepest_descent(
    func,
    grad,
    q_matrix: np.ndarray,
    x0: np.ndarray,
    tol: float = 1e-4,
    max_iter: int = 300,
) -> GradientResult:
    """Minimize a quadratic function by steepest descent."""
    x = np.asarray(x0, dtype=float)
    history: list[dict] = []
    for iteration in range(max_iter + 1):
        g = grad(x)
        norm_g = float(np.linalg.norm(g))
        history.append({"iter": iteration, "x": x.copy(), "f": float(func(x)), "grad_norm": norm_g})
        if norm_g < tol:
            break
        alpha = float((g @ g) / (g @ q_matrix @ g))
        x = x - alpha * g
    return GradientResult(x, float(func(x)), history[-1]["iter"], history)


def fletcher_reeves(
    func,
    grad,
    q_matrix: np.ndarray,
    x0: np.ndarray,
    tol: float = 1e-4,
    max_iter: int = 300,
) -> GradientResult:
    """Minimize a quadratic function by Fletcher-Reeves conjugate gradients."""
    x = np.asarray(x0, dtype=float)
    g = grad(x)
    direction = -g
    history: list[dict] = []

    for iteration in range(max_iter + 1):
        norm_g = float(np.linalg.norm(g))
        history.append({"iter": iteration, "x": x.copy(), "f": float(func(x)), "grad_norm": norm_g})
        if norm_g < tol:
            break
        alpha = float(-(g @ direction) / (direction @ q_matrix @ direction))
        x_next = x + alpha * direction
        g_next = grad(x_next)
        beta = float((g_next @ g_next) / (g @ g))
        direction = -g_next + beta * direction
        x, g = x_next, g_next

    return GradientResult(x, float(func(x)), history[-1]["iter"], history)
