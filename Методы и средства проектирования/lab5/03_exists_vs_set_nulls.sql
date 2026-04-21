-- ЛР5, п. 5.3: те же задачи, что UNION / INTERSECT / EXCEPT (п. 4.2), через EXISTS / NOT EXISTS;
-- плюс замечание про NULL (в сравнениях «= NULL» строки не находятся — нужен IS NULL).

-- --- Аналог INTERSECT (сотрудники с приёмом и в подразделении 2, и в 4) ---
SELECT DISTINCT пр.ид_сотрудника
FROM прием пр
WHERE пр.ид_подразделения = 2
  AND EXISTS (
      SELECT 1
      FROM прием пр2
      WHERE пр2.ид_сотрудника = пр.ид_сотрудника
        AND пр2.ид_подразделения = 4
  )
ORDER BY 1;

-- --- Аналог EXCEPT (сотрудники из приёма, которых нет в увольнение) ---
SELECT DISTINCT пр.ид_сотрудника
FROM прием пр
WHERE NOT EXISTS (
    SELECT 1
    FROM увольнение у
    WHERE у.ид_сотрудника = пр.ид_сотрудника
)
ORDER BY 1;

-- --- NULL: «WHERE столбец = NULL» почти никогда не даст строк; NOT EXISTS с «= NULL» тоже ---
-- Сравните число строк с «IS NULL» и с «= NULL».
SELECT x AS только_is_null
FROM (VALUES (NULL::int), (1)) AS t(x)
WHERE x IS NULL;

SELECT x AS равно_null_почти_всегда_пусто
FROM (VALUES (NULL::int), (1)) AS t2(x)
WHERE x = NULL;
