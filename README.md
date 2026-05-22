# Лабораторная работа 1. Безусловная многопараметрическая оптимизация

Репозиторий содержит воспроизводимые Python-вычисления для варианта 16:

```text
f(x, y) = 2(x - 3)^2 + 3(y + 2)^2 - 2xy + 4x - 6y
x0 = (0, 0), eps = 1e-4
```

Методичка требует:

- построить график функции;
- найти стационарные точки аналитически и исследовать их;
- решить задачу методами Нелдера-Мида, Хука-Дживса, наискорейшего спуска и Флетчера-Ривса;
- для метода Хука-Дживса использовать метод деления отрезка пополам для одномерного поиска шага;
- показать последовательность симплексов и последовательные приближения `{x_k}`.

## Colab

После публикации репозитория на GitHub ноутбуки открываются по ссылкам:

- [01_analysis.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/01_analysis.ipynb)
- [02_nelder_mead.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/02_nelder_mead.ipynb)
- [03_hooke_jeeves.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/03_hooke_jeeves.ipynb)
- [04_steepest_descent.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/04_steepest_descent.ipynb)
- [05_fletcher_reeves.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/05_fletcher_reeves.ipynb)
- [06_comparison.ipynb](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/06_comparison.ipynb)

## Локальный запуск

```bash
python -m pip install -r requirements.txt
python scripts/generate_artifacts.py
python build_template.py
python build_report.py
```

После запуска создаются:

- `figures/*.png` - графики для отчета;
- `tables/*.csv` - таблицы сходимости;
- `values.json` - численные значения для подстановки;
- `report_template.docx` - шаблон отчета по ГОСТ с плейсхолдерами;
- `report_v16.docx` - заполненный отчет.

## Структура

```text
src/target.py              целевая функция, градиент, Гессиан
src/nelder_mead.py         метод Нелдера-Мида
src/hooke_jeeves.py        метод деления отрезка пополам и Хука-Дживса
src/gradient_methods.py    наискорейший спуск и Флетчер-Ривс
src/plotting.py            общая визуализация
scripts/generate_artifacts.py
scripts/generate_notebooks.py
notebooks/*.ipynb
```
