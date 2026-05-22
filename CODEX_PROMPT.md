# Prompt for Codex: populate `megusto0/mp-1`

You are working on the repository `https://github.com/megusto0/mp-1`.
Create a reproducible Python/Jupyter project for lab work 1:
numerical methods for unconstrained multiparameter optimization, variant 16.

Use the following task from the methodical guide:

- plot the given function in any mathematical package;
- find stationary points analytically and investigate the function at those points;
- solve the unconstrained optimization problem with:
  - Nelder-Mead, reflection coefficient `alpha = 1`, choose expansion, contraction and shrink coefficients yourself;
  - Hooke-Jeeves with the specified one-dimensional method for step search;
  - steepest descent and Fletcher-Reeves, using explicit formulas for the step;
- illustrate the extremum search process:
  - simplex sequence for Nelder-Mead;
  - successive approximations `{x_k}` for the other methods;
- choose the initial point and accuracy yourself.

Use these fixed values:

```text
f(x, y) = 2(x - 3)^2 + 3(y + 2)^2 - 2xy + 4x - 6y
x0 = (0, 0)
eps = 1e-4
Hooke-Jeeves line search: bisection / interval-halving method
GitHub repo: https://github.com/megusto0/mp-1
```

Expected result:

1. Create `src/` modules with clean implementations:
   - `target.py`
   - `nelder_mead.py`
   - `hooke_jeeves.py`
   - `gradient_methods.py`
   - `plotting.py`
2. Create six notebooks in `notebooks/`:
   - `01_analysis.ipynb`
   - `02_nelder_mead.ipynb`
   - `03_hooke_jeeves.ipynb`
   - `04_steepest_descent.ipynb`
   - `05_fletcher_reeves.ipynb`
   - `06_comparison.ipynb`
3. Each notebook must run locally and in Google Colab. Add a Colab bootstrap cell that clones `megusto0/mp-1` only when running inside Colab.
4. Generate report artifacts:
   - `figures/*.png`
   - `tables/*.csv`
   - `values.json`
5. Generate a GOST-style report:
   - `report_template.docx` with placeholders;
   - `report_v16.docx` filled after notebooks/artifact scripts run.
6. Keep the report under 21 pages. Use concise code snippets, tables with selected iterations, and one combined comparison table.
7. The text must be clear for a first-time reader: state the problem, derive the gradient/Hessian, explain stopping criteria, and interpret results.

Run and verify:

```bash
python -m pip install -r requirements.txt
python scripts/generate_notebooks.py
python scripts/generate_artifacts.py
python build_template.py
python build_report.py
python -m py_compile src/*.py scripts/*.py build_report.py build_template.py
```

Acceptance criteria:

- all notebooks exist and contain executable code cells;
- all required figures and tables are produced;
- `report_v16.docx` opens and has no unresolved `[[FIG:...]]`, `[[TBL:...]]`, `[[CODE:...]]`, or `[[VAL:...]]` placeholders except intentionally unresolved manual page numbers if Word pagination is edited later;
- the final answer lists generated files and verification commands.
