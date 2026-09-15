-- ЛР8, п. 8.3: UPDATE … WHERE CURRENT OF <курсор> (курсор FOR UPDATE).
-- Для приёмов до 2016-01-01 сбрасываем признак совместительства в B'0'.

CREATE OR REPLACE PROCEDURE lr8_reset_sovmest_old_priem()
LANGUAGE plpgsql
AS $$
DECLARE
    v_ид int;
    v_n int := 0;
    cur_upd CURSOR FOR
        SELECT пр.ид
        FROM прием пр
        WHERE пр.дата_приема < DATE '2016-01-01'
          AND пр.совместительство = B'1'
        FOR UPDATE OF пр;
BEGIN
    OPEN cur_upd;
    LOOP
        FETCH cur_upd INTO v_ид;
        EXIT WHEN NOT FOUND;

        UPDATE прием
        SET совместительство = B'0'
        WHERE CURRENT OF cur_upd;

        v_n := v_n + 1;
    END LOOP;
    CLOSE cur_upd;

    RAISE NOTICE 'lr8: UPDATE WHERE CURRENT OF — изменено строк: %', v_n;
END;
$$;

-- === Результат выполнения скрипта (Data Output) ===
-- Приём 8: дата 2000-01-01 (< 2016) — подходит под условие процедуры.
UPDATE прием SET совместительство = B'1' WHERE ид = 8;

SELECT ид, дата_приема, совместительство::text AS до
FROM прием
WHERE ид = 8;

CALL lr8_reset_sovmest_old_priem();

SELECT ид, дата_приема, совместительство::text AS после
FROM прием
WHERE ид = 8;

SELECT COUNT(*)::int AS всего_сброшено_совместителей
FROM прием
WHERE дата_приема < DATE '2016-01-01' AND совместительство = B'1';
