-- старое ограничение снято и то же по ссылке, но явно прописано ON DELETE NO ACTION и ON UPDATE CASCADE
ALTER TABLE дети DROP CONSTRAINT IF EXISTS дети_ид_сотрудника_fkey;

ALTER TABLE дети ADD CONSTRAINT дети_ид_сотрудника_fkey
    FOREIGN KEY (ид_сотрудника) REFERENCES сотрудник (ид)
    ON DELETE NO ACTION ON UPDATE CASCADE;