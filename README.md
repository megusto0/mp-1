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

## Состав работы

Ноутбуки самодостаточны: в Google Colab они запускаются напрямую, без команд клонирования репозитория.

| № | Тема | Ноутбук | Colab |
|---|------|---------|-------|
| 01 | Аналитическое исследование функции | [`01_analysis.ipynb`](notebooks/01_analysis.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/01_analysis.ipynb) |
| 02 | Метод Нелдера-Мида | [`02_nelder_mead.ipynb`](notebooks/02_nelder_mead.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/02_nelder_mead.ipynb) |
| 03 | Метод Хука-Дживса | [`03_hooke_jeeves.ipynb`](notebooks/03_hooke_jeeves.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/03_hooke_jeeves.ipynb) |
| 04 | Метод наискорейшего спуска | [`04_steepest_descent.ipynb`](notebooks/04_steepest_descent.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/04_steepest_descent.ipynb) |
| 05 | Метод Флетчера-Ривса | [`05_fletcher_reeves.ipynb`](notebooks/05_fletcher_reeves.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/05_fletcher_reeves.ipynb) |
| 06 | Сравнение методов | [`06_comparison.ipynb`](notebooks/06_comparison.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/megusto0/mp-1/blob/master/notebooks/06_comparison.ipynb) |

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
notebooks/*.ipynb         самодостаточные ноутбуки с Colab-кнопками
```
