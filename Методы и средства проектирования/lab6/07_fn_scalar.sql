-- ЛР6, п. 6.3: скалярная функция пользователя.

CREATE OR REPLACE FUNCTION lr6_child_count(p_сотрудник int)
RETURNS int
LANGUAGE sql
STABLE
AS $$
    SELECT COUNT(*)::int FROM дети WHERE ид_сотрудника = p_сотрудник;
$$;

-- Пример:
-- SELECT с.ид, с.фио, lr6_child_count(с.ид) AS детей FROM сотрудник с ORDER BY с.ид;
