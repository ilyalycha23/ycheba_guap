-- ЛР5, п. 5.1: DELETE с EXISTS на таблице увольнение (TEMP lr5_tmp_del).
-- Перед выполнением: схема и данные (lab1+lab2 или lab4/main_schema.sql).

DROP TABLE IF EXISTS lr5_tmp_del;

CREATE TEMP TABLE lr5_tmp_del (
    ид int PRIMARY KEY
);

INSERT INTO lr5_tmp_del (ид)
SELECT с.ид FROM сотрудник с WHERE с.ид <= 3;

DELETE FROM lr5_tmp_del d
WHERE EXISTS (
    SELECT 1
    FROM увольнение у
    WHERE у.ид_сотрудника = d.ид
);

SELECT * FROM lr5_tmp_del ORDER BY ид;