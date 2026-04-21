-- ЛР6, п. 6.4: «каскадное удаление» вручную — при no action на FK сначала
-- удаляются зависимые строки (перевод, увольнение, прием, дети), затем сотрудник.

CREATE OR REPLACE PROCEDURE lr6_delete_employee(IN p_ид int)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM сотрудник WHERE ид = p_ид) THEN
        RAISE EXCEPTION 'Сотрудник % не найден', p_ид;
    END IF;

    DELETE FROM перевод WHERE ид_сотрудника = p_ид;
    DELETE FROM увольнение WHERE ид_сотрудника = p_ид;
    DELETE FROM прием WHERE ид_сотрудника = p_ид;
    DELETE FROM дети WHERE ид_сотрудника = p_ид;
    DELETE FROM сотрудник WHERE ид = p_ид;
END;
$$;

-- Внимание: вызов удаляет реальные данные учебной БД. Для проверки лучше копия БД или свой тестовый ид.
-- Пример (закомментировано): CALL lr6_delete_employee(90);
