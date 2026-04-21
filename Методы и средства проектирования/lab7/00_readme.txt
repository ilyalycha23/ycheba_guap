Лабораторная работа №7 — по методичка.pdf (глава **7**, п. **7.4** «Лабораторная работа 7» — типично **триггеры**; при расхождении с методичкой скорректируйте формулировки в отчёте). Вариант 12. СУБД: **PostgreSQL 11+**.

Подготовка:
1) ../lab1/01_schema.sql  
2) ../lab2/01_insert_test_data.sql  

Порядок (объекты с префиксом `lr7_`):
1) `01_aux_audit_table.sql` — таблица журнала для AFTER-триггера.  
2) `02_trg_priyom_date_check.sql` — **BEFORE** INSERT/UPDATE на `прием`: дата приёма не в будущем.  
3) `03_trg_employee_audit.sql` — **AFTER** INSERT/UPDATE/DELETE на `сотрудник`: запись в `lr7_employee_audit`.  
4) `04_trg_deti_limit.sql` — **BEFORE** INSERT на `дети`: ограничение числа детей на одного сотрудника.  
5) `05_trg_subdept_delete_guard.sql` — **BEFORE** DELETE на `подразделение`: запрет удаления при наличии дочерних подразделений (понятное сообщение до срабатывания FK).  

6) `06_demo_triggers.sql` — примеры вызовов (в т.ч. ожидаемая ошибка).  

Снятие объектов ЛР7: `09_drop_lr7_objects.sql`.  

В отчёте: листинги `CREATE FUNCTION` / `CREATE TRIGGER`, условия срабатывания, скриншоты или вывод psql. Структура: `otchet_lr7_soderzhanie.txt`.  
Шаблон в Word: **otchet_lr7.docx** (в т.ч. **ход работы** текстом). Пересборка: `python build_lab_reports_5_8_docx.py` из корня каталога дисциплины.

**Синтаксис триггера в PG 11:** в конце указано `EXECUTE PROCEDURE … ()` (в PG 14+ допускается и `FUNCTION`).
