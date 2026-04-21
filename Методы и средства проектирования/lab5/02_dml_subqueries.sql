-- ЛР5, п. 5.1: подзапросы в INSERT / UPDATE / DELETE (демонстрация).
-- Временные таблицы; в начале — удаление, чтобы скрипт можно было запускать повторно в той же сессии.

DROP TABLE IF EXISTS lr5_tmp_ins;
DROP TABLE IF EXISTS lr5_tmp_upd;
DROP TABLE IF EXISTS lr5_tmp_del;

CREATE TEMP TABLE lr5_tmp_ins (
    ид_сотрудника int PRIMARY KEY,
    комментарий text
);

INSERT INTO lr5_tmp_ins (ид_сотрудника, комментарий)
SELECT с.ид, 'есть дети'
FROM сотрудник с
WHERE EXISTS (SELECT 1 FROM дети д WHERE д.ид_сотрудника = с.ид);

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

SELECT * FROM lr5_tmp_ins ORDER BY ид_сотрудника;
SELECT * FROM lr5_tmp_upd ORDER BY ид;
SELECT * FROM lr5_tmp_del ORDER BY ид;
