-- ЛР7: примеры для отчёта (выполнять после 01–05).

-- 1) BEFORE прием: дата в будущем — ожидаемое исключение триггера (обрабатывается в DO, сессия остаётся рабочей)
DO $$
BEGIN
    INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
    VALUES (900, 1, 2, 1, CURRENT_DATE + 1, B'0');
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Ожидаемо (триггер lr7): %', SQLERRM;
END;
$$;

-- 2) AFTER сотрудник: между UPDATE и ROLLBACK строка в lr7_employee_audit видна в этой же сессии;
-- после ROLLBACK откатываются и правка сотрудника, и вставка в журнал (для скриншота — COMMIT на копии БД).
BEGIN;
UPDATE сотрудник SET фио = фио || ' ' WHERE ид = 8;
SELECT * FROM lr7_employee_audit ORDER BY id DESC LIMIT 5;
ROLLBACK;

-- 3) BEFORE дети: при 12 уже введённых детях следующая вставка упадёт (лимит в триггере — 12).

-- 4) BEFORE подразделение: удаление ид 1 («Промтех») с дочерними — ошибка lr7
-- BEGIN;
-- SAVEPOINT sp_del;
-- DELETE FROM подразделение WHERE ид = 1;
-- ROLLBACK TO SAVEPOINT sp_del;
-- ROLLBACK;
