"""Run all methods and generate report artifacts."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gradient_methods import fletcher_reeves, steepest_descent
from src.hooke_jeeves import hooke_jeeves
from src.nelder_mead import nelder_mead
from src.plotting import save_convergence_plot, save_path_plot, save_surface_contour
from src.target import EPS, F_STAR, Q, X0, X_STAR, f, grad

FIGURES = ROOT / "figures"
TABLES = ROOT / "tables"
VALUES = ROOT / "values.json"


def _fmt(value: float) -> str:
    return f"{value:.6g}".replace(".", ",")


def _selected_rows(history: list[dict], x_key: str = "x", f_key: str = "f", limit: int = 9) -> list[dict]:
    if len(history) <= limit:
        return history
    keep = list(range(limit - 1)) + [len(history) - 1]
    return [history[i] for i in keep]


def _write_table(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def _nm_table(history: list[dict]) -> None:
    rows = []
    for item in _selected_rows(history):
        x = item["best_x"]
        rows.append([item["iter"], _fmt(x[0]), _fmt(x[1]), _fmt(item["best_f"]), _fmt(item["spread"])])
    _write_table(TABLES / "tab_4_1_nm.csv", ["k", "x", "y", "f_best", "spread"], rows)


def _point_table(path: Path, history: list[dict], extra: str) -> None:
    rows = []
    for item in _selected_rows(history):
        x = item["x"]
        rows.append([item["iter"], _fmt(x[0]), _fmt(x[1]), _fmt(item["f"]), _fmt(item[extra])])
    _write_table(path, ["k", "x_k", "y_k", "f(x_k)", extra], rows)


def generate() -> None:
    FIGURES.mkdir(exist_ok=True)
    TABLES.mkdir(exist_ok=True)

    nm = nelder_mead(f, X0, tol=EPS)
    hj = hooke_jeeves(f, X0, tol=EPS)
    sd = steepest_descent(f, grad, Q, X0, tol=EPS)
    fr = fletcher_reeves(f, grad, Q, X0, tol=EPS)

    save_surface_contour(FIGURES / "fig_3_4_surface_contour.png")
    nm_points = np.array([item["best_x"] for item in nm.history])
    nm_simplexes = [item["simplex"] for item in nm.history[:: max(1, len(nm.history) // 12)]]
    save_path_plot(FIGURES / "fig_4_1_nm_trajectory.png", nm_points, "Метод Нелдера-Мида", nm_simplexes)
    save_path_plot(FIGURES / "fig_4_2_hj_trajectory.png", np.array([item["x"] for item in hj.history]), "Метод Хука-Дживса")
    save_path_plot(FIGURES / "fig_4_3_sd_trajectory.png", np.array([item["x"] for item in sd.history]), "Метод наискорейшего спуска")
    save_path_plot(FIGURES / "fig_4_4_fr_trajectory.png", np.array([item["x"] for item in fr.history]), "Метод Флетчера-Ривса")
    save_convergence_plot(
        FIGURES / "fig_5_convergence.png",
        {
            "Нелдер-Мид": [item["best_f"] for item in nm.history],
            "Хук-Дживс": [item["f"] for item in hj.history],
            "Наискорейший спуск": [item["f"] for item in sd.history],
            "Флетчер-Ривс": [item["f"] for item in fr.history],
        },
    )

    _nm_table(nm.history)
    _point_table(TABLES / "tab_4_2_hj.csv", hj.history, "delta")
    _point_table(TABLES / "tab_4_3_sd.csv", sd.history, "grad_norm")
    _point_table(TABLES / "tab_4_4_fr.csv", fr.history, "grad_norm")

    compare = pd.DataFrame(
        [
            ["Нелдер-Мид", nm.iterations, nm.x[0], nm.x[1], nm.fun, np.linalg.norm(nm.x - X_STAR)],
            ["Хук-Дживс", hj.iterations, hj.x[0], hj.x[1], hj.fun, np.linalg.norm(hj.x - X_STAR)],
            ["Наискорейший спуск", sd.iterations, sd.x[0], sd.x[1], sd.fun, np.linalg.norm(sd.x - X_STAR)],
            ["Флетчер-Ривс", fr.iterations, fr.x[0], fr.x[1], fr.fun, np.linalg.norm(fr.x - X_STAR)],
        ],
        columns=["Метод", "Итерации", "x", "y", "f", "||x-x*||"],
    )
    compare_out = compare.copy()
    for col in ["x", "y", "f", "||x-x*||"]:
        compare_out[col] = compare_out[col].map(_fmt)
    compare_out.to_csv(TABLES / "tab_5_compare.csv", index=False, encoding="utf-8")

    values = {
        "page_1": "3",
        "page_2": "3",
        "page_3": "4",
        "page_3_1": "4",
        "page_3_2": "4",
        "page_3_3": "5",
        "page_3_4": "5",
        "page_4": "6",
        "page_4_1": "6",
        "page_4_2": "8",
        "page_4_3": "11",
        "page_4_4": "13",
        "page_5": "15",
        "page_6": "16",
        "page_app": "17",
        "x_star": _fmt(X_STAR[0]),
        "y_star": _fmt(X_STAR[1]),
        "f_star": _fmt(F_STAR),
        "nm_x": _fmt(nm.x[0]),
        "nm_y": _fmt(nm.x[1]),
        "nm_f": _fmt(nm.fun),
        "nm_iter": str(nm.iterations),
        "hj_x": _fmt(hj.x[0]),
        "hj_y": _fmt(hj.x[1]),
        "hj_f": _fmt(hj.fun),
        "hj_iter": str(hj.iterations),
        "sd_x": _fmt(sd.x[0]),
        "sd_y": _fmt(sd.x[1]),
        "sd_f": _fmt(sd.fun),
        "sd_iter": str(sd.iterations),
        "fr_x": _fmt(fr.x[0]),
        "fr_y": _fmt(fr.x[1]),
        "fr_f": _fmt(fr.fun),
        "fr_iter": str(fr.iterations),
    }
    VALUES.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated artifacts in {ROOT}")


if __name__ == "__main__":
    generate()
