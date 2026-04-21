-- ЛР8 (опционально): пример разграничения доступа только на чтение представлений.
-- Выполнять под суперпользователем (postgres) и подставить имя своей БД при необходимости.
-- По умолчанию всё закомментировано — не ломает учебную установку одним \i.

/*
CREATE ROLE lr8_reader;

GRANT CONNECT ON DATABASE postgres TO lr8_reader;  -- замените postgres на имя вашей БД

GRANT USAGE ON SCHEMA public TO lr8_reader;

GRANT SELECT ON lr8_vw_priyom_details TO lr8_reader;
GRANT SELECT ON lr8_vw_shtat_enriched TO lr8_reader;
GRANT SELECT ON lr8_vw_subdept_tree TO lr8_reader;

-- Проверка: \c база lr8_reader — затем SELECT * FROM lr8_vw_priyom_details LIMIT 1;
-- Прямой SELECT к таблице прием для этой роли должен завершиться отказом (если не выдавали прав).
*/
