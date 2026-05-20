-- ЛР6, п. 6.1: управляющие конструкции (IF, WHILE) — в PostgreSQL как анонимный блок DO.

-- Аналог «пакета» (ПЗ): один блок на сервер.


DROP TABLE IF EXISTS _lr6_script_result;
CREATE TEMP TABLE _lr6_script_result (
    шаг text NOT NULL,
    значение text NOT NULL
);

DO $$
DECLARE
    v_ид int;
    v_cnt int := 0;
    v_step int;
BEGIN
    FOR v_ид IN SELECT пд.ид FROM подразделение пд ORDER BY пд.ид
    LOOP
        IF EXISTS (SELECT 1 FROM прием пр WHERE пр.ид_подразделения = v_ид) THEN
            v_cnt := v_cnt + 1;
        END IF;
    END LOOP;

    INSERT INTO _lr6_script_result
    VALUES ('подразделений с хотя бы одним приёмом', v_cnt::text);

    v_step := 3;
    WHILE v_step > 0 LOOP
        INSERT INTO _lr6_script_result
        VALUES ('while step ' || v_step::text, v_step::text);
        v_step := v_step - 1;
    END LOOP;
END;
$$;


-- === Результат выполнения скрипта ===

SELECT шаг, значение FROM _lr6_script_result ORDER BY шаг;