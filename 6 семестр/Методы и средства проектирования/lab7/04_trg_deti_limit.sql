-- ЛР7: BEFORE INSERT — ограничение «не больше N записей о детях» на одного сотрудника
-- (демонстрация построчного триггера и обращения к NEW).

CREATE OR REPLACE FUNCTION lr7_fn_deti_limit()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_cnt int;
    v_max constant int := 12;
BEGIN
    SELECT COUNT(*)::int INTO v_cnt
    FROM дети
    WHERE ид_сотрудника = NEW.ид_сотрудника;

    IF v_cnt >= v_max THEN
        RAISE EXCEPTION 'lr7: у сотрудника % уже % детей в таблице (лимит %)',
            NEW.ид_сотрудника, v_cnt, v_max
            USING ERRCODE = '23514';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS lr7_trg_deti_limit ON дети;

CREATE TRIGGER lr7_trg_deti_limit
    BEFORE INSERT ON дети
    FOR EACH ROW
    EXECUTE PROCEDURE lr7_fn_deti_limit();

-- === Результат выполнения скрипта ===
SELECT trigger_name, action_timing, event_manipulation
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name = 'lr7_trg_deti_limit';

SELECT с.ид, с.фио, COUNT(д.ид)::int AS детей_в_таблице
FROM сотрудник с
LEFT JOIN дети д ON д.ид_сотрудника = с.ид
WHERE с.ид = 6
GROUP BY с.ид, с.фио;