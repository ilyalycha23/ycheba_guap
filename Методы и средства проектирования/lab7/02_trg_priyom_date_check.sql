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
