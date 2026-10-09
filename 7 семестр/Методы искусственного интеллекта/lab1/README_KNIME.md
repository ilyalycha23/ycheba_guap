# ЛР1. Метод линейной регрессии (работа №2 практикума KNIME)

Студент: **И.А. Лаврешин**, группа **4321**  
Курс: Методы искусственного интеллекта

## Что уже сделано

| Файл | Назначение |
|------|------------|
| `data/Salary_Data.csv` | Исходные данные (30 записей: Employee, YearsExperience, Salary) |
| `run_experiment.py` | Воспроизведение эксперимента (разбиение 20% Linear, обучение, метрики, графики) |
| `results.json` | Числовые результаты |
| `figures/` | Рисунки для отчёта |
| `Отчет_ЛР1_Лаврешин_Линейная_регрессия.docx` | Готовый отчёт |
| `ОтчетЛР1ШишкинKNIMEЛинейнаярегрессия.docx` | Пример отчёта (образец оформления) |

Пересчёт результатов:

```powershell
python run_experiment.py
python build_report.py
```

## Как повторить в KNIME (для защиты)

1. Скачайте [KNIME Analytics Platform](https://www.knime.com/downloads) и установите.
2. File → New → New KNIME Workflow, имя например `Lab1_Linear_Regression`.
3. Из Node Repository перетащите узлы и соедините как на схеме:

```
CSV Reader → Color Manager → Partitioning ─┬→ Linear Regression Learner ─┐
                                           └→ Regression Predictor ←──────┘
                                                    ├→ Numeric Scorer
                                                    └→ Scatter Plot
```

4. Настройки:
   - **CSV Reader** → файл `lab1/data/Salary_Data.csv`
   - **Color Manager** → цвет по столбцу `Salary`
   - **Partitioning** → Relative **20%**, sampling **Linear** (порт 1 = train → Learner, порт 2 = test → Predictor)
   - **Linear Regression Learner** → Target: `Salary`, Include: `YearsExperience`
   - **Numeric Scorer** → Reference: `Salary`, Prediction: `Prediction (Salary)`
   - **Scatter Plot** → X: `YearsExperience`, Y: `Salary`
5. Execute all → сделайте скриншоты workflow, таблицы Numeric Scorer и Scatter Plot.
6. При желании замените рисунки в отчёте на скриншоты из KNIME.

Ожидаемый порядок метрик при Linear 20% (Python / близко к KNIME): R² ≈ 0.94, MAPE ≈ 8–9 %.  
В методичке и примере указано R² = 0.957 — это эталонный скрин из практикума; у вас могут быть небольшие отличия из‑за версии узла Partitioning.
