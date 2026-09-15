-- ЛР7: вспомогательная таблица для демонстрации AFTER-триггера (аудит изменений сотрудника).

CREATE TABLE IF NOT EXISTS lr7_employee_audit (
    id bigserial PRIMARY KEY,
    ts timestamptz NOT NULL DEFAULT clock_timestamp(),
    op text NOT NULL,
    emp_id int,
    fio_old varchar(200),
    fio_new varchar(200),
    birth_old date,
    birth_new date,
    CONSTRAINT lr7_employee_audit_op_chk CHECK (op IN ('INSERT', 'UPDATE', 'DELETE'))
);

COMMENT ON TABLE lr7_employee_audit IS 'ЛР7: журнал DML по таблице сотрудник (триггер AFTER).';

-- === Результат выполнения скрипта ===
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'lr7_employee_audit'
ORDER BY ordinal_position;
SELECT COUNT(*)::bigint AS строк_в_журнале FROM lr7_employee_audit;
