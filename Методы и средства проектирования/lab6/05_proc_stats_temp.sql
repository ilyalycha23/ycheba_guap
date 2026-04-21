-- ЛР6, п. 6.4: статистика во временной таблице (по каждому подразделению).

CREATE OR REPLACE PROCEDURE lr6_fill_stats_temp()
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS lr6_stat;
    CREATE TEMP TABLE lr6_stat (
        ид_подразделения int PRIMARY KEY,
        наименование varchar(200) NOT NULL,
        строк_штат int NOT NULL,
        сумма_штатных_единиц bigint NOT NULL,
        работников_по_приему bigint NOT NULL
    );

    INSERT INTO lr6_stat (ид_подразделения, наименование, строк_штат, сумма_штатных_единиц, работников_по_приему)
    SELECT
        пд.ид,
        пд.наименование,
        (SELECT COUNT(*)::int FROM штатное_расписание ш WHERE ш.ид_подразделения = пд.ид),
        lr6_sum_staff_units(пд.ид),
        (SELECT COUNT(DISTINCT пр.ид_сотрудника)::bigint FROM прием пр WHERE пр.ид_подразделения = пд.ид)
    FROM подразделение пд;
END;
$$;

-- После вызова в той же сессии:
-- CALL lr6_fill_stats_temp();
-- SELECT * FROM lr6_stat ORDER BY ид_подразделения;
