"""Variant 16 target function and derivatives."""
from __future__ import annotations

import numpy as np

Q = np.array([[4.0, -2.0], [-2.0, 6.0]])
B = np.array([-8.0, 6.0])
C = 30.0
X0 = np.array([0.0, 0.0])
EPS = 1e-4
X_STAR = np.linalg.solve(Q, -B)
F_STAR = 21.6


def f(point: np.ndarray | list[float] | tuple[float, float]) -> float:
    """Return f(x, y) for variant 16."""
    x = np.asarray(point, dtype=float)
    return float(0.5 * x @ Q @ x + B @ x + C)


def grad(point: np.ndarray | list[float] | tuple[float, float]) -> np.ndarray:
    """Return gradient of f at point."""
    x = np.asarray(point, dtype=float)
    return Q @ x + B


def hessian() -> np.ndarray:
    """Return constant Hessian matrix."""
    return Q.copy()


def original_formula(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Return f(x, y) in the form used in the lab task."""
    return 2 * (x - 3) ** 2 + 3 * (y + 2) ** 2 - 2 * x * y + 4 * x - 6 * y
