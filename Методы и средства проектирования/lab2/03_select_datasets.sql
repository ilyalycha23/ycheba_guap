-- ЛР2, отчёт: «наборы данных» в таблицах (после 02_insert_test_data.sql)

SELECT 'подразделение' AS таблица, * FROM подразделение ORDER BY ид;
SELECT 'должность' AS таблица, * FROM должность ORDER BY ид;
SELECT 'штатное_расписание' AS таблица, * FROM штатное_расписание ORDER BY ид;
SELECT 'сотрудник' AS таблица, * FROM сотрудник ORDER BY ид;
SELECT 'дети' AS таблица, * FROM дети ORDER BY ид;
SELECT 'прием' AS таблица, * FROM прием ORDER BY ид;
SELECT 'перевод' AS таблица, * FROM перевод ORDER BY ид;
SELECT 'увольнение' AS таблица, * FROM увольнение ORDER BY ид;
