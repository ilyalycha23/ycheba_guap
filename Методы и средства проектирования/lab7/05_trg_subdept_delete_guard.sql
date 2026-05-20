-- ЛР7: BEFORE DELETE — явный запрет удаления подразделения, пока есть дочерние записи
-- (сообщение триггера понятнее, чем только ответ СУБД по FK).

CREATE OR REPLACE FUNCTION lr7_fn_subdept_delete_guard()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_child int;
BEGIN
    SELECT п.ид INTO v_child
    FROM подразделение п
    WHERE п.ид_родительское = OLD.ид
    LIMIT 1;

    IF v_child IS NOT NULL THEN
        RAISE EXCEPTION 'lr7: подразделение % (%) нельзя удалить: есть дочернее подразделение с ид %',
            OLD.ид, OLD.наименование, v_child
            USING ERRCODE = '23503'; -- foreign_key_violation
    END IF;

    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS lr7_trg_subdept_delete_guard ON подразделение;

CREATE TRIGGER lr7_trg_subdept_delete_guard
    BEFORE DELETE ON подразделение
    FOR EACH ROW
    EXECUTE PROCEDURE lr7_fn_subdept_delete_guard();

-- === Результат выполнения скрипта ===
SELECT trigger_name, action_timing, event_manipulation
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name = 'lr7_trg_subdept_delete_guard';

DROP TABLE IF EXISTS _lr7_script_result;
CREATE TEMP TABLE _lr7_script_result (
    демонстрация text NOT NULL,
    статус text NOT NULL,
    сообщение text
);

DO $$
BEGIN
    DELETE FROM подразделение WHERE ид = 1;
    INSERT INTO _lr7_script_result
    VALUES ('удаление подразделения 1', 'неожиданно: удалено', NULL);
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_script_result
        VALUES ('удаление подразделения 1', 'отклонено (ожидаемо)', SQLERRM);
END;
$$;

SELECT * FROM _lr7_script_result;
