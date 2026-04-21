-- ЛР6, п. 6.4: вставка с «пополнением справочника» (аналог: студент + группа).
-- Приём на работу: если в справочнике «должность» нет строки с данным ид,
-- она добавляется, затем вставляется строка в «прием».

CREATE OR REPLACE PROCEDURE lr6_insert_hire_with_position(
    IN p_сотрудник int,
    IN p_подразделение int,
    IN p_должность int,
    IN p_дата date,
    IN p_совместительство bit(1)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_next int;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM сотрудник WHERE ид = p_сотрудник) THEN
        RAISE EXCEPTION 'Сотрудник % не найден', p_сотрудник;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM подразделение WHERE ид = p_подразделение) THEN
        RAISE EXCEPTION 'Подразделение % не найдено', p_подразделение;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM должность WHERE ид = p_должность) THEN
        INSERT INTO должность (ид, наименование, категория)
        VALUES (
            p_должность,
            'LR6 должность id ' || p_должность::text,
            'прочее'
        );
    END IF;

    SELECT COALESCE(MAX(ид), 0) + 1 INTO v_next FROM прием;

    INSERT INTO прием (ид, ид_сотрудника, ид_подразделения, ид_должности, дата_приема, совместительство)
    VALUES (v_next, p_сотрудник, p_подразделение, p_должность, p_дата, p_совместительство);
END;
$$;

-- Пример: новая должность с ид 90 (если её ещё нет — добавится в справочник).
-- CALL lr6_insert_hire_with_position(1, 2, 90, CURRENT_DATE, B'0');
