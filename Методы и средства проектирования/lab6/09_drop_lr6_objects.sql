-- Снять все объекты ЛР6 (перед повторной установкой).
DROP PROCEDURE IF EXISTS lr6_insert_hire_with_position(integer, integer, integer, date, bit(1));
DROP PROCEDURE IF EXISTS lr6_delete_employee(integer);
DROP PROCEDURE IF EXISTS lr6_delete_leaf_subdept(integer);
DROP PROCEDURE IF EXISTS lr6_fill_stats_temp();
DROP FUNCTION IF EXISTS lr6_sum_staff_units(integer);
DROP FUNCTION IF EXISTS lr6_child_count(integer);
DROP FUNCTION IF EXISTS lr6_direct_subdepts(integer);

-- === Результат выполнения скрипта ===
SELECT routine_schema, routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public' AND routine_name LIKE 'lr6_%'
ORDER BY routine_name;
