-- ЛР8: сравнение планов (для отчёта выполните в psql и сохраните вывод).
-- На учебной БД мало строк — выгода индекса может не проявиться; важна форма плана (Seq Scan vs Index Scan).

-- Выборка по индексируемому столбцу прием.ид_сотрудника
EXPLAIN (COSTS, VERBOSE, FORMAT TEXT)
SELECT пр.*
FROM прием пр
WHERE пр.ид_сотрудника = 1;

-- Через представление (часто — nested loop / hash join по размеру данных)
EXPLAIN (COSTS, FORMAT TEXT)
SELECT *
FROM lr8_vw_priyom_details v
WHERE v.сотрудник_ид = 1;

-- Агрегат по представлению штата
EXPLAIN (COSTS, FORMAT TEXT)
SELECT подразделение, SUM(количество_единиц) AS всего_единиц
FROM lr8_vw_shtat_enriched
GROUP BY подразделение;
