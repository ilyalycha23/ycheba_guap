-- ЛР7: AFTER INSERT / UPDATE / DELETE — фиксация факта изменения в журнале.

CREATE OR REPLACE FUNCTION lr7_fn_employee_audit()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO lr7_employee_audit (op, emp_id, fio_old, birth_old)
        VALUES ('DELETE', OLD.ид, OLD.фио, OLD.дата_рождения);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO lr7_employee_audit (op, emp_id, fio_old, fio_new, birth_old, birth_new)
        VALUES ('UPDATE', NEW.ид, OLD.фио, NEW.фио, OLD.дата_рождения, NEW.дата_рождения);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO lr7_employee_audit (op, emp_id, fio_new, birth_new)
        VALUES ('INSERT', NEW.ид, NEW.фио, NEW.дата_рождения);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS lr7_trg_employee_audit ON сотрудник;

CREATE TRIGGER lr7_trg_employee_audit
    AFTER INSERT OR UPDATE OR DELETE ON сотрудник
    FOR EACH ROW
    EXECUTE PROCEDURE lr7_fn_employee_audit();
