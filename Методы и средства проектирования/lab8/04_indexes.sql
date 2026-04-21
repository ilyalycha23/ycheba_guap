-- ЛР8: вспомогательные индексы B-tree для ускорения выборок по внешним ключам и фильтрам.
-- (Схема из ЛР1 уже имеет PK/UNIQUE; здесь — дополнительные одно-столбцовые индексы.)

CREATE INDEX IF NOT EXISTS lr8_idx_priyom_sotr ON прием (ид_сотрудника);
CREATE INDEX IF NOT EXISTS lr8_idx_priyom_podr ON прием (ид_подразделения);
CREATE INDEX IF NOT EXISTS lr8_idx_priyom_dolzh ON прием (ид_должности);

CREATE INDEX IF NOT EXISTS lr8_idx_deti_sotr ON дети (ид_сотрудника);
CREATE INDEX IF NOT EXISTS lr8_idx_perevod_sotr ON перевод (ид_сотрудника);
CREATE INDEX IF NOT EXISTS lr8_idx_uvoln_sotr ON увольнение (ид_сотрудника);

CREATE INDEX IF NOT EXISTS lr8_idx_shtat_podr ON штатное_расписание (ид_подразделения);

COMMENT ON INDEX lr8_idx_priyom_sotr IS 'ЛР8: поиск приёмов по сотруднику.';
COMMENT ON INDEX lr8_idx_priyom_podr IS 'ЛР8: поиск приёмов по подразделению.';
