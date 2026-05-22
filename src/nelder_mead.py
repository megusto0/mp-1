"""Nelder-Mead simplex method."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class NelderMeadResult:
    x: np.ndarray
    fun: float
    iterations: int
    history: list[dict]


def nelder_mead(
    func,
    x0: np.ndarray,
    step: float = 1.0,
    tol: float = 1e-4,
    max_iter: int = 300,
    alpha: float = 1.0,
    gamma: float = 2.0,
    beta: float = 0.5,
    sigma: float = 0.5,
) -> NelderMeadResult:
    """Minimize a two-dimensional function by the Nelder-Mead method."""
    x0 = np.asarray(x0, dtype=float)
    n = len(x0)
    simplex = [x0]
    for i in range(n):
        vertex = x0.copy()
        vertex[i] += step
        simplex.append(vertex)
    simplex = np.array(simplex, dtype=float)
    history: list[dict] = []

    for iteration in range(max_iter + 1):
        values = np.array([func(vertex) for vertex in simplex])
        order = np.argsort(values)
        simplex = simplex[order]
        values = values[order]
        spread = float(np.max(values) - np.min(values))
        history.append(
            {
                "iter": iteration,
                "simplex": simplex.copy(),
                "best_x": simplex[0].copy(),
                "best_f": float(values[0]),
                "spread": spread,
            }
        )
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
    return NelderMeadResult(best, float(func(best)), history[-1]["iter"], history)
