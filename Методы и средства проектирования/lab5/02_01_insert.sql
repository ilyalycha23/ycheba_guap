-- ЛР5, п. 5.1: INSERT … SELECT и подзапрос с EXISTS (TEMP lr5_tmp_ins).
-- Перед выполнением: схема и данные (lab1+lab2 или lab4/main_schema.sql).

DROP TABLE IF EXISTS lr5_tmp_ins;

CREATE TEMP TABLE lr5_tmp_ins (
    ид_сотрудника int PRIMARY KEY,
    комментарий text
);

INSERT INTO lr5_tmp_ins (ид_сотрудника, комментарий)
SELECT с.ид, 'есть дети'
FROM сотрудник с
WHERE EXISTS (SELECT 1 FROM дети д WHERE д.ид_сотрудника = с.ид);

SELECT * FROM lr5_tmp_ins ORDER BY ид_сотрудника;