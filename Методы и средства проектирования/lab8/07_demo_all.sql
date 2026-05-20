-- ЛР8: сводный прогон (после 01–06). Data Output — последние SELECT.

-- === Проверка объектов ===
SELECT
    obj.имя,
    CASE
        WHEN obj.тип = 'table' AND t.table_name IS NOT NULL THEN 'есть'
        WHEN obj.тип = 'procedure' AND p.specific_name IS NOT NULL THEN 'есть'
        WHEN obj.тип = 'trigger' AND tr.trigger_name IS NOT NULL THEN 'есть'
        ELSE 'НЕТ'
    END AS статус
FROM (
    VALUES
        ('lr8_priem_stats', 'table'),
        ('lr8_fill_priem_stats', 'procedure'),
        ('lr8_reset_sovmest_old_priem', 'procedure'),
        ('lr8_delete_demo_priem_cursor', 'procedure'),
        ('lr8_trg_refresh_priem_stats', 'trigger')
) AS obj(имя, тип)
LEFT JOIN information_schema.tables t
    ON obj.тип = 'table' AND t.table_schema = 'public' AND t.table_name = obj.имя
LEFT JOIN information_schema.routines p
    ON obj.тип = 'procedure' AND p.routine_schema = 'public' AND p.routine_name = obj.имя
LEFT JOIN information_schema.triggers tr
    ON obj.тип = 'trigger' AND tr.trigger_schema = 'public' AND tr.trigger_name = obj.имя;

CALL lr8_fill_priem_stats();

SELECT 'сводка lr8_priem_stats' AS раздел, с.*, пд.наименование AS подразделение
FROM lr8_priem_stats с
INNER JOIN подразделение пд ON пд.ид = с.ид_подразделения
ORDER BY с.ид_подразделения, с.ид_должности;

-- Триггер пересчитает сводку при вставке демо-приёма
DELETE FROM прием WHERE ид = 902;
INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
VALUES (902, 8, 2, 3, CURRENT_DATE, B'0');

SELECT 'после INSERT 902 (триггер)' AS раздел, COUNT(*)::bigint AS строк_в_сводке
FROM lr8_priem_stats;

DELETE FROM прием WHERE ид = 902;

SELECT 'итог ЛР8' AS раздел, 'курсоры ISO, CURRENT OF, типы курсоров — скрипты 01–06' AS описание;
