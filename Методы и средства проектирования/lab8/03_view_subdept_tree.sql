-- ЛР8: иерархия подразделений (корни — где ид_родительское IS NULL).

CREATE OR REPLACE VIEW lr8_vw_subdept_tree AS
WITH RECURSIVE tree AS (
    SELECT
        п.ид,
        п.наименование,
        п.ид_родительское,
        0 AS уровень,
        п.наименование::text AS путь_наименований
    FROM подразделение п
    WHERE п.ид_родительское IS NULL

    UNION ALL

    SELECT
        c.ид,
        c.наименование,
        c.ид_родительское,
        t.уровень + 1,
        t.путь_наименований || ' / ' || c.наименование::text
    FROM подразделение c
    INNER JOIN tree t ON c.ид_родительское = t.ид
)
SELECT * FROM tree;

COMMENT ON VIEW lr8_vw_subdept_tree IS 'ЛР8: обход дерева подразделений (уровень и цепочка наименований).';

-- Пример:
-- SELECT * FROM lr8_vw_subdept_tree ORDER BY уровень, ид;
