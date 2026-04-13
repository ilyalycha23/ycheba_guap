-- ЛР2, п. 2.5: пример каскадного обновления по внешнему ключу (on update cascade).
-- п. 2.4: alter table — add / alter column / drop column, add/drop constraint, rename column (в PostgreSQL).

-- ---------- 1) ON UPDATE CASCADE (как в п. 1.3 методички для внешних ключей) ----------
BEGIN;

UPDATE подразделение
SET ид = 40
WHERE ид = 4;

-- Проверка: в дочерних таблицах значения внешних ключей, ссылавшиеся на ид=4, должны стать 40.
-- SELECT * FROM штатное_расписание WHERE ид_подразделения = 40;
-- SELECT * FROM прием WHERE ид_подразделения = 40;

UPDATE подразделение
SET ид = 4
WHERE ид = 40;

COMMIT;

-- ---------- 2) ON DELETE CASCADE (по смыслу п. 2.5 и примеру «Оценка» в п. 2.1 методички) ----------
-- В вашей схеме ЛР1 для большинства связей задано on delete no action, поэтому удаление, например,
-- сотрудника при наличии строк в «прием» будет отклонено. Каскадное удаление демонстрируется
-- на отдельной временной паре таблиц (не меняет основную предметную область):

CREATE TEMP TABLE lr2_demo_родитель (
    ид int PRIMARY KEY
);

CREATE TEMP TABLE lr2_demo_ребенок (
    ид int PRIMARY KEY,
    ид_родителя int NOT NULL REFERENCES lr2_demo_родитель (ид) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO lr2_demo_родитель (ид) VALUES (1);
INSERT INTO lr2_demo_ребенок (ид, ид_родителя) VALUES (10, 1), (11, 1);

DELETE FROM lr2_demo_родитель WHERE ид = 1;

-- После delete в lr2_demo_родитель строки в lr2_demo_ребенок должны исчезнуть автоматически.

DROP TABLE lr2_demo_ребенок;
DROP TABLE lr2_demo_родитель;

-- ---------- 3) ALTER TABLE (п. 2.4 методички) ----------
ALTER TABLE сотрудник
    ADD COLUMN телефон varchar(20) NULL;

UPDATE сотрудник
SET телефон = '+7-900-000-00-01'
WHERE ид = 1;

ALTER TABLE сотрудник
    ALTER COLUMN телефон TYPE varchar(30);

ALTER TABLE сотрудник
    ADD CONSTRAINT сотрудник_уник_телефон_демо UNIQUE (телефон);

ALTER TABLE сотрудник
    DROP CONSTRAINT IF EXISTS сотрудник_уник_телефон_демо;

ALTER TABLE сотрудник
    DROP COLUMN телефон;

-- Переименование столбца: в PostgreSQL — rename column; в методичке для MS SQL — sp_rename.
ALTER TABLE сотрудник
    RENAME COLUMN фио TO фио_полное;

ALTER TABLE сотрудник
    RENAME COLUMN фио_полное TO фио;
