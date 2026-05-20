-- ЛР8, п. 8.3: DELETE … WHERE CURRENT OF <курсор>.

CREATE OR REPLACE PROCEDURE lr8_delete_demo_priem_cursor()
LANGUAGE plpgsql
AS $$
DECLARE
    v_ид int;
    v_n int := 0;
    cur_del CURSOR FOR
        SELECT пр.ид
        FROM прием пр
        WHERE пр.ид >= 900
        FOR UPDATE OF пр;
BEGIN
    OPEN cur_del;
    LOOP
        FETCH cur_del INTO v_ид;
        EXIT WHEN NOT FOUND;

        DELETE FROM прием
        WHERE CURRENT OF cur_del;

        v_n := v_n + 1;
    END LOOP;
    CLOSE cur_del;

    RAISE NOTICE 'lr8: DELETE WHERE CURRENT OF — удалено строк: %', v_n;
END;
$$;

-- === Результат выполнения скрипта (Data Output) ===
DELETE FROM прием WHERE ид >= 900;

INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
VALUES
    (900, 8, 4, 3, CURRENT_DATE, B'0'),
    (901, 8, 2, 1, CURRENT_DATE, B'0')
ON CONFLICT (ид) DO NOTHING;

SELECT ид, ид_сотрудника FROM прием WHERE ид >= 900 ORDER BY ид;

CALL lr8_delete_demo_priem_cursor();

SELECT COUNT(*)::bigint AS осталось_демо_строк_ид_ge_900
FROM прием
WHERE ид >= 900;
