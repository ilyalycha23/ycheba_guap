-- ЛР8: триггер с курсором (аналог п. 8.1 методички — пересчёт сводки после DML).
-- AFTER STATEMENT на прием: полный пересчёт lr8_priem_stats курсором.

CREATE OR REPLACE FUNCTION lr8_fn_refresh_priem_stats()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_подр int;
    v_дол int;
    v_всего int;
    v_совм int;
    cur_ref CURSOR FOR
        SELECT
            пр.ид_подразделения,
            пр.ид_должности,
            COUNT(*)::int,
            COUNT(*) FILTER (WHERE пр.совместительство = B'1')::int
        FROM прием пр
        GROUP BY пр.ид_подразделения, пр.ид_должности;
BEGIN
    DELETE FROM lr8_priem_stats;

    OPEN cur_ref;
    LOOP
        FETCH cur_ref INTO v_подр, v_дол, v_всего, v_совм;
        EXIT WHEN NOT FOUND;

        INSERT INTO lr8_priem_stats (ид_подразделения, ид_должности, всего_приемов, совместителей)
        VALUES (v_подр, v_дол, v_всего, v_совм);
    END LOOP;
    CLOSE cur_ref;

    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS lr8_trg_refresh_priem_stats ON прием;

CREATE TRIGGER lr8_trg_refresh_priem_stats
    AFTER INSERT OR UPDATE OR DELETE ON прием
    FOR EACH STATEMENT
    EXECUTE PROCEDURE lr8_fn_refresh_priem_stats();

-- === Результат выполнения скрипта (Data Output) ===
SELECT trigger_name, action_timing, event_manipulation, action_orientation
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name = 'lr8_trg_refresh_priem_stats';

CALL lr8_fill_priem_stats();

SELECT COUNT(*)::bigint AS строк_в_сводке_после_создания_триггера
FROM lr8_priem_stats;
