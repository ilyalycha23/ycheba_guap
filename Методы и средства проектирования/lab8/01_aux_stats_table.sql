-- ЛР8 (методичка, гл. 8): вспомогательная таблица сводной статистики по приёмам.
-- Аналог «сводной» таблицы из п. 8.1 методички; заполняется процедурой с курсором (02).

CREATE TABLE IF NOT EXISTS lr8_priem_stats (
    ид_подразделения int NOT NULL,
    ид_должности int NOT NULL,
    всего_приемов int NOT NULL DEFAULT 0,
    совместителей int NOT NULL DEFAULT 0,
    PRIMARY KEY (ид_подразделения, ид_должности)
);

COMMENT ON TABLE lr8_priem_stats IS
    'ЛР8: сводка по приёмам (подразделение × должность), заполняется курсором.';

-- === Результат выполнения скрипта (Data Output) ===
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'lr8_priem_stats'
ORDER BY ordinal_position;

SELECT COUNT(*)::bigint AS строк_в_сводке FROM lr8_priem_stats;
