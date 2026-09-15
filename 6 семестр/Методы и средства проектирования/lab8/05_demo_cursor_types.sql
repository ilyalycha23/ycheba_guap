-- ЛР8, п. 8.2–8.3: сравнение типов курсоров.
-- В PostgreSQL нет ключевых слов STATIC / KEYSET / DYNAMIC (это Transact-SQL).
-- Ниже — учебные аналоги + пояснения для отчёта (см. 00_readme.txt).

DROP TABLE IF EXISTS _lr8_cursor_demo;
CREATE TEMP TABLE _lr8_cursor_demo (
    тип_курсора text NOT NULL,
    шаг text NOT NULL,
    результат text NOT NULL
);

-- A) «Только вперёд» — NO SCROLL (аналог forward only / read only)
DO $$
DECLARE
    r RECORD;
    c CURSOR FOR
        SELECT пд.ид FROM подразделение пд ORDER BY пд.ид;
    v_first int;
    v_second int;
BEGIN
    OPEN c;
    FETCH c INTO r;
    v_first := r.ид;
    FETCH c INTO r;
    v_second := r.ид;
    CLOSE c;

    INSERT INTO _lr8_cursor_demo VALUES (
        'NO SCROLL (ISO, только FETCH NEXT)',
        'первые два ид',
        v_first::text || ', ' || v_second::text
    );
END;
$$;

-- B) SCROLL — можно FETCH PRIOR (аналог scroll в T-SQL)
DO $$
DECLARE
    r RECORD;
    c SCROLL CURSOR FOR
        SELECT пд.ид FROM подразделение пд ORDER BY пд.ид;
    v1 int;
    v2 int;
    v_back int;
BEGIN
    OPEN c;
    FETCH NEXT FROM c INTO r;
    v1 := r.ид;
    FETCH NEXT FROM c INTO r;
    v2 := r.ид;
    FETCH PRIOR FROM c INTO r;
    v_back := r.ид;
    CLOSE c;

    INSERT INTO _lr8_cursor_demo VALUES (
        'SCROLL (ISO)',
        'NEXT, NEXT, PRIOR',
        'после PRIOR ид=' || v_back::text || ' (должен совпасть с ' || v1::text || ')'
    );
END;
$$;

-- C) «Статический» снимок — копия в TEMP на момент открытия (аналог STATIC в T-SQL)
DO $$
DECLARE
    r RECORD;
    v_cnt_snap int;
    v_cnt_live int;
    c CURSOR FOR SELECT ш.ид FROM lr8_snap_static ш ORDER BY ш.ид;
BEGIN
    DROP TABLE IF EXISTS lr8_snap_static;
    CREATE TEMP TABLE lr8_snap_static AS
    SELECT ш.ид, ш.количество_единиц FROM штатное_расписание ш;

    v_cnt_snap := (SELECT COUNT(*) FROM lr8_snap_static);

    OPEN c;
    FETCH c INTO r;
    CLOSE c;

    UPDATE штатное_расписание SET количество_единиц = количество_единиц WHERE ид = r.ид;
    v_cnt_live := (SELECT COUNT(*) FROM штатное_расписание);

    INSERT INTO _lr8_cursor_demo VALUES (
        'STATIC (аналог через снимок TEMP)',
        'курсор по снимку',
        'строк в снимке: ' || v_cnt_snap::text || '; в живой таблице: ' || v_cnt_live::text
            || ' — изменения базы не меняют уже открытый снимок'
    );
END;
$$;

-- D) «Динамический» — курсор напрямую по таблице (видит актуальные данные при каждом FETCH)
DO $$
DECLARE
    r RECORD;
    v_before int;
    v_after int;
    c CURSOR FOR
        SELECT ш.количество_единиц FROM штатное_расписание ш WHERE ш.ид = 1;
BEGIN
    SELECT ш.количество_единиц INTO v_before FROM штатное_расписание ш WHERE ш.ид = 1;

    OPEN c;
    UPDATE штатное_расписание SET количество_единиц = количество_единиц + 1 WHERE ид = 1;
    FETCH c INTO r;
    v_after := r.количество_единиц;
    CLOSE c;

    UPDATE штатное_расписание SET количество_единиц = количество_единиц - 1 WHERE ид = 1;

    INSERT INTO _lr8_cursor_demo VALUES (
        'DYNAMIC (аналог: курсор по живой таблице)',
        'FETCH после UPDATE в той же сессии',
        'было ' || v_before::text || ', FETCH видит ' || v_after::text
    );
END;
$$;

-- E) FOR UPDATE — основа для WHERE CURRENT OF (в T-SQL близко к keyset + scroll_locks)
DO $$
BEGIN
    INSERT INTO _lr8_cursor_demo VALUES (
        'KEYSET (в T-SQL) / FOR UPDATE (PostgreSQL)',
        'см. 03_proc_update_where_current_of.sql',
        'изменение текущей строки: UPDATE … WHERE CURRENT OF'
    );
END;
$$;

-- === Результат выполнения скрипта (Data Output) ===
SELECT * FROM _lr8_cursor_demo ORDER BY тип_курсора, шаг;

SELECT
    'T-SQL STATIC' AS tsql,
    'снимок в tempdb, не видит чужие изменения' AS смысл
UNION ALL
SELECT 'T-SQL KEYSET', 'фиксированы ключи, данные строк могут меняться'
UNION ALL
SELECT 'T-SQL DYNAMIC', 'каждый FETCH видит актуальные данные'
UNION ALL
SELECT 'PostgreSQL', 'NO SCROLL / SCROLL / снимок TEMP / FOR UPDATE — см. демо выше';
