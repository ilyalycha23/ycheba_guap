-- ЛР5, п. 5.1: UPDATE со скалярным подзапросом COUNT(*) (TEMP lr5_tmp_upd).
-- Перед выполнением: схема и данные (lab1+lab2 или lab4/main_schema.sql).

DROP TABLE IF EXISTS lr5_tmp_upd;

CREATE TEMP TABLE lr5_tmp_upd (
    ид int PRIMARY KEY,
    счётчик int NOT NULL DEFAULT 0
);

INSERT INTO lr5_tmp_upd (ид, счётчик)
SELECT ид, 0 FROM подразделение;

UPDATE lr5_tmp_upd u
SET счётчик = (
    SELECT COUNT(*)::int
    FROM прием пр
    WHERE пр.ид_подразделения = u.ид
);

SELECT * FROM lr5_tmp_upd ORDER BY ид;