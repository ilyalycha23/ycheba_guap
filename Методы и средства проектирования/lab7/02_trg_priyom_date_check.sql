-- ЛР7: BEFORE INSERT OR UPDATE — дополнительное бизнес-правило целостности по дате.

CREATE OR REPLACE FUNCTION lr7_fn_priyom_date_check()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.дата_приема > CURRENT_DATE THEN
        RAISE EXCEPTION 'lr7: дата приёма не может быть позже текущей даты (получено: %)', NEW.дата_приема
            USING ERRCODE = '23514'; -- check_violation
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS lr7_trg_priyom_date_check ON прием;

CREATE TRIGGER lr7_trg_priyom_date_check
    BEFORE INSERT OR UPDATE OF дата_приема ON прием
    FOR EACH ROW
    EXECUTE PROCEDURE lr7_fn_priyom_date_check();

-- === Результат выполнения скрипта ===
SELECT trigger_name, action_timing, event_manipulation, action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name = 'lr7_trg_priyom_date_check'
ORDER BY event_manipulation;

DROP TABLE IF EXISTS _lr7_script_result;
CREATE TEMP TABLE _lr7_script_result (
    демонстрация text NOT NULL,
    статус text NOT NULL,
    сообщение text
);

DO $$
BEGIN
    INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
    VALUES (900, 1, 2, 1, CURRENT_DATE + 1, B'0');
    INSERT INTO _lr7_script_result
    VALUES ('дата приёма в будущем', 'неожиданно: вставка прошла', NULL);
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_script_result
        VALUES ('дата приёма в будущем', 'отклонено (ожидаемо)', SQLERRM);
END;
$$;

SELECT * FROM _lr7_script_result;
