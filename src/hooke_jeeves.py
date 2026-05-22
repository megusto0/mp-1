"""Hooke-Jeeves method with interval-halving line search."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class HookeJeevesResult:
    x: np.ndarray
    fun: float
    iterations: int
    history: list[dict]


def bisection_min(func, a: float, b: float, tol: float = 1e-4) -> tuple[float, float]:
    """Minimize a unimodal function on [a, b] by interval halving."""
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


def _exploratory_search(func, base: np.ndarray, delta: float) -> np.ndarray:
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


def hooke_jeeves(
    func,
    x0: np.ndarray,
    delta: float = 1.0,
    tol: float = 1e-4,
    max_iter: int = 300,
) -> HookeJeevesResult:
    """Minimize a two-dimensional function by the Hooke-Jeeves method."""
    base = np.asarray(x0, dtype=float)
    history: list[dict] = []
    iteration = 0

    while delta > tol and iteration < max_iter:
        explored = _exploratory_search(func, base, delta)
        if func(explored) < func(base):
            direction = explored - base
            phi = lambda t: func(explored + t * direction)
            t_star, _ = bisection_min(phi, 0.0, 2.0, tol)
            new_base = explored + t_star * direction
            if func(new_base) < func(base):
                base = new_base
            else:
                base = explored
        else:
            delta *= 0.5

        history.append(
            {
                "iter": iteration,
                "x": base.copy(),
                "f": float(func(base)),
                "delta": float(delta),
            }
        )
        iteration += 1

    return HookeJeevesResult(base, float(func(base)), iteration, history)
