-- ЛР6, п. 6.3: табличная функция (непосредственно подчинённые подразделения).

CREATE OR REPLACE FUNCTION lr6_direct_subdepts(p_родитель int)
RETURNS TABLE(ид int, наименование varchar(200))
LANGUAGE sql
STABLE
AS $$
    SELECT п.ид, п.наименование
    FROM подразделение п
    WHERE (p_родитель IS NULL AND п.ид_родительское IS NULL)
       OR (p_родитель IS NOT NULL AND п.ид_родительское = p_родитель);
$$;

-- p_родитель = ид родителя (например, 1 — дочерние у «Промтех»).
-- p_родитель IS NULL — только «корневые» подразделения (ид_родительское IS NULL).

-- Пример:
-- SELECT * FROM lr6_direct_subdepts(1);
