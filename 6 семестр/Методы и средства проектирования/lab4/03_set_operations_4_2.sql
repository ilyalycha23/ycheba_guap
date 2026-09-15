-- ========== UNION: объединение как над множеством (дубликаты строк схлопываются) ==========
SELECT с.фио
FROM сотрудник с
WHERE с.фио LIKE 'И%'
UNION
SELECT с2.фио
FROM сотрудник с2
WHERE с2.фио LIKE '%ов%'
ORDER BY 1;

-- ========== UNION ALL: объединение мультимножеств (кратности суммируются) ==========
SELECT с.фио
FROM сотрудник с
WHERE с.фио LIKE 'И%'
UNION ALL
SELECT с2.фио
FROM сотрудник с2
WHERE с2.фио LIKE '%ов%'
ORDER BY 1;

-- Сравните число строк двух запросов выше (у «Иванов …» оба условия — UNION даст 1 строку, UNION ALL — 2).

-- ========== INTERSECT: пересечение множеств (уникальные общие строки) ==========
SELECT пр.ид_сотрудника
FROM прием пр
WHERE пр.ид_подразделения = 2
INTERSECT
SELECT пр2.ид_сотрудника
FROM прием пр2
WHERE пр2.ид_подразделения = 4
ORDER BY 1;

-- ========== EXCEPT: разность множеств ==========
SELECT DISTINCT пр.ид_сотрудника
FROM прием пр
EXCEPT
SELECT у.ид_сотрудника
FROM увольнение у
ORDER BY 1;

-- ========== INTERSECT ALL / EXCEPT ALL (мультимножества; PostgreSQL 15+) ==========
-- Правила кратностей — как в п. 4.2 методички; в MS SQL для INTERSECT/EXCEPT с ALL ограничения.
SELECT a
FROM (VALUES (1), (1), (2)) AS r(a)
INTERSECT ALL
SELECT a
FROM (VALUES (1), (1), (1)) AS s(a);

SELECT a
FROM (VALUES (1), (1), (2)) AS r2(a)
EXCEPT ALL
SELECT a
FROM (VALUES (1)) AS s2(a);
