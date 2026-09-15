-- ЛР8, п. 8.1: курсор в ХП — ISO-синтаксис (DECLARE … OPEN … FETCH … CLOSE).
-- Обход агрегата по приёмам и заполнение lr8_priem_stats (как цикл WHILE в методичке).

CREATE OR REPLACE PROCEDURE lr8_fill_priem_stats()
LANGUAGE plpgsql
AS $$
DECLARE
    v_подр int;
    v_дол int;
    v_всего int;
    v_совм int;
    cur_stats CURSOR FOR
        SELECT
            пр.ид_подразделения,
            пр.ид_должности,
            COUNT(*)::int,
            COUNT(*) FILTER (WHERE пр.совместительство = B'1')::int
        FROM прием пр
        GROUP BY пр.ид_подразделения, пр.ид_должности
        ORDER BY пр.ид_подразделения, пр.ид_должности;
BEGIN
    DELETE FROM lr8_priem_stats;

    OPEN cur_stats;
    LOOP
        FETCH cur_stats INTO v_подр, v_дол, v_всего, v_совм;
        EXIT WHEN NOT FOUND;

        INSERT INTO lr8_priem_stats (ид_подразделения, ид_должности, всего_приемов, совместителей)
        VALUES (v_подр, v_дол, v_всего, v_совм);
    END LOOP;
    CLOSE cur_stats;
END;
$$;

-- === Результат выполнения скрипта (Data Output) ===
CALL lr8_fill_priem_stats();

SELECT
    с.ид_подразделения,
    пд.наименование AS подразделение,
    с.ид_должности,
    д.наименование AS должность,
    с.всего_приемов,
    с.совместителей
FROM lr8_priem_stats с
INNER JOIN подразделение пд ON пд.ид = с.ид_подразделения
INNER JOIN должность д ON д.ид = с.ид_должности
ORDER BY с.ид_подразделения, с.ид_должности;
