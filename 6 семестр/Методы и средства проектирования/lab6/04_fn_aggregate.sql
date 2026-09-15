-- ЛР6, п. 6.4: вычисление и возврат агрегата (сумма штатных единиц по подразделению).

CREATE OR REPLACE FUNCTION lr6_sum_staff_units(p_подразделение int)
RETURNS bigint
LANGUAGE sql
STABLE
AS $$
    SELECT COALESCE(SUM(количество_единиц), 0)::bigint
    FROM штатное_расписание
    WHERE ид_подразделения = p_подразделение;
$$;

-- === Результат выполнения скрипта ===
SELECT
    пд.ид,
    пд.наименование,
    lr6_sum_staff_units(пд.ид) AS сумма_штатных_единиц
FROM подразделение пд
ORDER BY пд.ид;
