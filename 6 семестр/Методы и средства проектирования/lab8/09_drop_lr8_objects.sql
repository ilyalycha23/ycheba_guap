-- Снять объекты ЛР8.

DROP TRIGGER IF EXISTS lr8_trg_refresh_priem_stats ON прием;

DROP PROCEDURE IF EXISTS lr8_fill_priem_stats();
DROP PROCEDURE IF EXISTS lr8_reset_sovmest_old_priem();
DROP PROCEDURE IF EXISTS lr8_delete_demo_priem_cursor();

DROP FUNCTION IF EXISTS lr8_fn_refresh_priem_stats();

DROP TABLE IF EXISTS lr8_priem_stats;

-- === Результат выполнения скрипта (Data Output) ===
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public' AND routine_name LIKE 'lr8_%'
UNION ALL
SELECT table_name, 'TABLE'
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name LIKE 'lr8_%'
ORDER BY 1;
