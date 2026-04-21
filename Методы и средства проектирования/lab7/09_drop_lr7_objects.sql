-- Снять объекты ЛР7 (порядок: триггеры, затем функции, затем таблица).

DROP TRIGGER IF EXISTS lr7_trg_priyom_date_check ON прием;
DROP TRIGGER IF EXISTS lr7_trg_employee_audit ON сотрудник;
DROP TRIGGER IF EXISTS lr7_trg_deti_limit ON дети;
DROP TRIGGER IF EXISTS lr7_trg_subdept_delete_guard ON подразделение;

DROP FUNCTION IF EXISTS lr7_fn_priyom_date_check();
DROP FUNCTION IF EXISTS lr7_fn_employee_audit();
DROP FUNCTION IF EXISTS lr7_fn_deti_limit();
DROP FUNCTION IF EXISTS lr7_fn_subdept_delete_guard();

DROP TABLE IF EXISTS lr7_employee_audit;
