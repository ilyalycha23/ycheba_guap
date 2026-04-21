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
