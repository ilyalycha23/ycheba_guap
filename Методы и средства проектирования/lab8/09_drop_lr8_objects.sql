-- Снять объекты ЛР8 (сначала представления, затем индексы).

DROP VIEW IF EXISTS lr8_vw_subdept_tree;
DROP VIEW IF EXISTS lr8_vw_shtat_enriched;
DROP VIEW IF EXISTS lr8_vw_priyom_details;

DROP INDEX IF EXISTS lr8_idx_priyom_sotr;
DROP INDEX IF EXISTS lr8_idx_priyom_podr;
DROP INDEX IF EXISTS lr8_idx_priyom_dolzh;
DROP INDEX IF EXISTS lr8_idx_deti_sotr;
DROP INDEX IF EXISTS lr8_idx_perevod_sotr;
DROP INDEX IF EXISTS lr8_idx_uvoln_sotr;
DROP INDEX IF EXISTS lr8_idx_shtat_podr;

-- Если создавали роль из 06_grants_example.sql:
-- DROP OWNED BY lr8_reader;
-- DROP ROLE IF EXISTS lr8_reader;
