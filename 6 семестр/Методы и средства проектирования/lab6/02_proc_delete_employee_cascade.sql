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

-- === Результат выполнения скрипта ===
-- Демонстрация в транзакции: после ROLLBACK сотрудник 8 и связанные строки остаются в БД.
BEGIN;
SELECT ид, фио FROM сотрудник WHERE ид = 8;
CALL lr6_delete_employee(8);
SELECT CASE
    WHEN EXISTS (SELECT 1 FROM сотрудник WHERE ид = 8) THEN 'сотрудник 8 ещё в таблице'
    ELSE 'сотрудник 8 удалён (до ROLLBACK)'
END AS результат_в_транзакции;
ROLLBACK;
SELECT ид, фио FROM сотрудник WHERE ид = 8;
