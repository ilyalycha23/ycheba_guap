Лабораторная работа №8 — методичка.pdf, глава 8 (стр. 61–69), п. 8.3.
Вариант 12. СУБД: PostgreSQL 11+ (CREATE PROCEDURE, CALL, курсоры PL/pgSQL).

Подготовка:
1) ../lab1/01_schema.sql
2) ../lab2/01_insert_test_data.sql

Порядок (объекты lr8_*):
1) 01_aux_stats_table.sql      — таблица сводки lr8_priem_stats
2) 02_proc_fill_stats_iso_cursor.sql — ХП с курсором (ISO: DECLARE/OPEN/FETCH/CLOSE)
3) 03_proc_update_where_current_of.sql — UPDATE … WHERE CURRENT OF
4) 04_proc_delete_where_current_of.sql — DELETE … WHERE CURRENT OF
5) 05_demo_cursor_types.sql    — NO SCROLL / SCROLL / аналоги STATIC и DYNAMIC + T-SQL
6) 06_trg_refresh_stats_cursor.sql — триггер AFTER STATEMENT с курсором
7) 07_demo_all.sql             — сводная проверка

Перед повторной установкой: 09_drop_lr8_objects.sql

PostgreSQL и методичка (T-SQL):
- ISO-синтаксис курсора — полностью в 02–04.
- STATIC / KEYSET / DYNAMIC — ключевые слова MS SQL; в 05 даны учебные аналоги и таблица соответствий.
- WHERE CURRENT OF — в 03 и 04 (курсор FOR UPDATE).

В отчёте: листинги ХП/триггера, вывод Data Output, сравнение типов курсоров (п. 8.2).
Структура отчёта: otchet_lr8_soderzhanie.txt. Ход работы: лаба8_ход_работы.txt.
