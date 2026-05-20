-- ЛР7: сводная демонстрация триггеров. Выполнять ПОСЛЕ 01, 02, 03, 04, 05 (по порядку).
-- NOTICE «_lr7_demo_result does not exist» при первом DROP — норма.

-- === Проверка подготовки (Data Output) ===
SELECT
    obj.имя AS объект,
    CASE
        WHEN obj.тип = 'table' AND t.table_name IS NOT NULL THEN 'есть'
        WHEN obj.тип = 'trigger' AND tr.trigger_name IS NOT NULL THEN 'есть'
        ELSE 'НЕТ — выполните скрипты 01–05'
    END AS статус
FROM (
    VALUES
        ('lr7_employee_audit', 'table'),
        ('lr7_trg_priyom_date_check', 'trigger'),
        ('lr7_trg_employee_audit', 'trigger'),
        ('lr7_trg_deti_limit', 'trigger'),
        ('lr7_trg_subdept_delete_guard', 'trigger')
) AS obj(имя, тип)
LEFT JOIN information_schema.tables t
    ON obj.тип = 'table' AND t.table_schema = 'public' AND t.table_name = obj.имя
LEFT JOIN information_schema.triggers tr
    ON obj.тип = 'trigger' AND tr.trigger_schema = 'public' AND tr.trigger_name = obj.имя;

DROP TABLE IF EXISTS _lr7_demo_result;
CREATE TEMP TABLE _lr7_demo_result (
    n int NOT NULL,
    демонстрация text NOT NULL,
    статус text NOT NULL,
    сообщение text
);

-- 1) BEFORE прием: дата в будущем
DO $$
BEGIN
    INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
    VALUES (900, 1, 2, 1, CURRENT_DATE + 1, B'0');
    INSERT INTO _lr7_demo_result
    VALUES (1, 'дата приёма в будущем', 'неожиданно: вставка прошла', NULL);
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_demo_result
        VALUES (1, 'дата приёма в будущем', 'отклонено (ожидаемо)', SQLERRM);
END;
$$;

-- 2) AFTER сотрудник → lr7_employee_audit
DO $$
DECLARE
    v_cnt bigint;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'lr7_employee_audit'
    ) THEN
        INSERT INTO _lr7_demo_result
        VALUES (2, 'аудит сотрудника (UPDATE)', 'пропущено', 'нет таблицы — выполните 01_aux_audit_table.sql и 03_trg_employee_audit.sql');
        RETURN;
    END IF;

    UPDATE сотрудник SET фио = TRIM(фио) WHERE ид = 8;
    UPDATE сотрудник SET фио = фио || ' ' WHERE ид = 8;

    SELECT COUNT(*) INTO v_cnt FROM lr7_employee_audit;

    INSERT INTO _lr7_demo_result
    VALUES (
        2,
        'аудит сотрудника (UPDATE)',
        'в журнале есть записи',
        'строк в lr7_employee_audit: ' || v_cnt::text
    );
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_demo_result
        VALUES (2, 'аудит сотрудника (UPDATE)', 'ошибка', SQLERRM);
END;
$$;

-- 3) BEFORE дети: лимит 12
DO $$
BEGIN
    INSERT INTO дети (ид, ид_сотрудника, фио, пол, дата_рождения)
    VALUES (900, 6, 'LR7 лишний ребёнок', 'М', '2011-01-01');
    INSERT INTO _lr7_demo_result
    VALUES (3, '13-й ребёнок у сотрудника 6', 'неожиданно: вставка прошла', NULL);
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_demo_result
        VALUES (3, '13-й ребёнок у сотрудника 6', 'отклонено (ожидаемо)', SQLERRM);
END;
$$;

-- 4) BEFORE подразделение: удаление «Промтех»
DO $$
BEGIN
    DELETE FROM подразделение WHERE ид = 1;
    INSERT INTO _lr7_demo_result
    VALUES (4, 'удаление подразделения 1', 'неожиданно: удалено', NULL);
EXCEPTION
    WHEN others THEN
        INSERT INTO _lr7_demo_result
        VALUES (4, 'удаление подразделения 1', 'отклонено (ожидаемо)', SQLERRM);
END;
$$;

-- === Результат выполнения скрипта (Data Output) ===
SELECT * FROM _lr7_demo_result ORDER BY n;

DROP TABLE IF EXISTS _lr7_audit_show;
DO $q$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'lr7_employee_audit'
    ) THEN
        EXECUTE $s$
            CREATE TEMP TABLE _lr7_audit_show AS
            SELECT id, ts, op, emp_id, fio_old, fio_new
            FROM lr7_employee_audit
            ORDER BY id DESC
            LIMIT 5
        $s$;
    ELSE
        CREATE TEMP TABLE _lr7_audit_show (
            id bigint, ts timestamptz, op text, emp_id int,
            fio_old varchar(200), fio_new varchar(200)
        );
        INSERT INTO _lr7_audit_show (op, fio_new)
        VALUES ('—', 'выполните 01 и 03, затем снова 06');
    END IF;
END;
$q$;

SELECT * FROM _lr7_audit_show;

SELECT trigger_name, action_timing, event_manipulation
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name LIKE 'lr7_%'
ORDER BY trigger_name, event_manipulation;
