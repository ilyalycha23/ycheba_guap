-- ЛР6, п. 6.4: удаление с «очисткой» / проверками — листовое подразделение
-- без дочерних подразделений, без штатного расписания и без приёмов.

CREATE OR REPLACE PROCEDURE lr6_delete_leaf_subdept(IN p_ид int)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM подразделение WHERE ид = p_ид) THEN
        RAISE EXCEPTION 'Подразделение % не найдено', p_ид;
    END IF;

    IF EXISTS (SELECT 1 FROM подразделение WHERE ид_родительское = p_ид) THEN
        RAISE EXCEPTION 'Подразделение %: есть дочерние записи', p_ид;
    END IF;

    IF EXISTS (SELECT 1 FROM штатное_расписание WHERE ид_подразделения = p_ид) THEN
        RAISE EXCEPTION 'Подразделение %: есть штатное расписание', p_ид;
    END IF;

    IF EXISTS (SELECT 1 FROM прием WHERE ид_подразделения = p_ид) THEN
        RAISE EXCEPTION 'Подразделение %: есть приёмы', p_ид;
    END IF;

    DELETE FROM подразделение WHERE ид = p_ид;
END;
$$;

-- Пример: сначала вставить пустое листовое подразделение с уникальным ид, затем:
-- CALL lr6_delete_leaf_subdept(…);
