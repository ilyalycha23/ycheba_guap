-- ЛР6, п. 6.1: управляющие конструкции (IF, WHILE) — в PostgreSQL как анонимный блок DO.
-- Аналог «пакета» (ПЗ): один блок на сервер.

DO $$
DECLARE
    v_ид int;
    v_cnt int := 0;
BEGIN
    FOR v_ид IN SELECT пд.ид FROM подразделение пд ORDER BY пд.ид
    LOOP
        IF EXISTS (SELECT 1 FROM прием пр WHERE пр.ид_подразделения = v_ид) THEN
            v_cnt := v_cnt + 1;
        END IF;
    END LOOP;

    RAISE NOTICE 'Подразделений с хотя бы одним приёмом: %', v_cnt;

    -- WHILE: обратный отсчёт для демонстрации цикла
    v_cnt := 3;
    WHILE v_cnt > 0 LOOP
        RAISE NOTICE 'while step %', v_cnt;
        v_cnt := v_cnt - 1;
    END LOOP;
END;
$$;
