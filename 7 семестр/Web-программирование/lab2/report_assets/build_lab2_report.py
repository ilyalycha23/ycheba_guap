# -*- coding: utf-8 -*-
"""Собирает отчёт ЛР2 по шаблону титула ЛР1."""

from __future__ import annotations

import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(r"D:\ycheba_guap\7 семестр\Web-программирование")
TEMPLATE = ROOT / "lab1" / "ЛР1_Веб_Лаврешин.docx"
OUT = ROOT / "lab2" / "ЛР2_Веб_Лаврешин.docx"
ASSETS = ROOT / "lab2" / "report_assets"
SRC = ROOT / "lab2" / "signalboard"


def set_run_font(run, size=14, bold=False, name="Times New Roman"):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.get_or_add_rFonts()
    r_fonts.set(qn("w:ascii"), name)
    r_fonts.set(qn("w:hAnsi"), name)
    r_fonts.set(qn("w:cs"), name)
    r_fonts.set(qn("w:eastAsia"), name)


def fmt_para(p, *, justify=False, indent=True, line=1.5):
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25) if indent else Cm(0)
    p.paragraph_format.line_spacing = line
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)


def add_heading(doc, num: str, title: str):
    p = doc.add_paragraph()
    fmt_para(p, indent=True, line=1.5)
    r1 = p.add_run(f"{num} ")
    set_run_font(r1, bold=True)
    r2 = p.add_run(title)
    set_run_font(r2, bold=True)
    return p


def add_body(doc, text: str):
    p = doc.add_paragraph()
    fmt_para(p, justify=True, indent=True)
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_center(doc, text: str, bold=False, size=14):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt_para(p, indent=False)
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold)
    return p


def add_file_title(doc, text: str):
    p = doc.add_paragraph()
    fmt_para(p, indent=False)
    r = p.add_run(text)
    set_run_font(r, bold=True)
    return p


def add_picture(doc, name: str, caption: str, width=16.0):
    path = ASSETS / name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt_para(p, indent=False)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width))
    add_center(doc, caption)


def add_code(doc, text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    for line in lines or [""]:
        p = doc.add_paragraph()
        fmt_para(p, indent=False, line=1.0)
        r = p.add_run(line if line != "" else " ")
        set_run_font(r, size=10, name="Courier New")


def add_table(doc, header, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(header))
    table.style = "Table Grid"
    for i, h in enumerate(header):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        set_run_font(r, bold=True, size=12)
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            cell = table.rows[ri].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(val)
            set_run_font(r, size=12)
    doc.add_paragraph()


def clear_from_goal(doc: Document):
    body = doc.element.body
    children = list(body)
    start = None
    for child in children:
        if child.tag != qn("w:p"):
            continue
        text = "".join(t.text or "" for t in child.iter(qn("w:t")))
        if text.startswith("1 Цель работы"):
            start = child
            break
    if start is None:
        raise RuntimeError("Не найден абзац «1 Цель работы»")
    removing = False
    for child in children:
        if child is start:
            removing = True
        if not removing:
            continue
        if child.tag == qn("w:sectPr"):
            continue
        body.remove(child)


def patch_title(doc: Document):
    cell = doc.tables[1].rows[0].cells[0]
    for p in cell.paragraphs:
        for r in p.runs:
            if r.text.strip() == "1":
                r.text = "2"
            if "СОЗДАНИЕ ПРОЕКТА NEXT.JS" in r.text:
                r.text = (
                    "СОЗДАНИЕ СТРУКТУРЫ ВЕБ-ПРИЛОЖЕНИЯ С ПОМОЩЬЮ APP ROUTER. "
                    "ПРОЕКТИРОВАНИЕ АВТОРИЗАЦИИ"
                )


def read_src(*parts: str) -> str:
    return (SRC.joinpath(*parts)).read_text(encoding="utf-8")


def build():
    shutil.copyfile(TEMPLATE, OUT)
    doc = Document(str(OUT))
    patch_title(doc)
    clear_from_goal(doc)

    add_heading(doc, "1", "Цель работы")
    add_body(
        doc,
        "Разработать структуру многостраничного веб-приложения SignalBoard "
        "с помощью App Router, настроить общую навигацию, создать динамический "
        "маршрут предметной сущности «сигнал» и реализовать клиентский прототип "
        "интерфейса входа и регистрации с явным пониманием различий между "
        "аутентификацией, управлением сессией и авторизацией.",
    )

    add_heading(doc, "2", "Задание")
    add_body(
        doc,
        "Продолжить проект лабораторной работы № 1. Спроектировать набор разделов "
        "приложения. В каталоге app создать страницы и вложенные маршруты, задействовав "
        "общий корневой layout и навигацию на основе компонента Link. Добавить "
        "динамический маршрут для отдельного сигнала. Разделить Server Components и "
        "Client Components. Создать учебный контекст пользователя, формы входа и "
        "регистрации, разные состояния интерфейса для гостя и вошедшего пользователя. "
        "Объяснить ограничения клиентского прототипа. Проверить проект командами "
        "npm run lint и npm run build.",
    )

    add_heading(doc, "3", "Ход выполнения задания")
    add_body(
        doc,
        "В рамках курса разрабатывается приложение SignalBoard – доска локальных "
        "сигналов для соседей. Приложение решает проблему потери объявлений вида "
        "«ищу», «отдаю», «предупреждаю» в разрозненных чатах дома и двора. Целевая "
        "аудитория – жители одного дома, двора или ЖК. Главная предметная сущность – "
        "сигнал. Тематика отлична от примеров TheraCity и StudySpace: вместо каталога "
        "учебных мест используется лента соседских сигналов.",
    )
    add_body(
        doc,
        "Каркас из двух страниц лабораторной работы № 1 превращён в связанное "
        "многостраничное приложение. Новый create-next-app не запускался: сохранены "
        "TypeScript, ESLint, App Router, отсутствие Tailwind CSS и каталога src. "
        "Версии среды: Node.js v24.19.0, npm 11.17.0.",
    )
    add_body(
        doc,
        "Соответствие разделов каталога app и URL приведено в таблице. Корневой "
        "маршрут / через redirect() из next/navigation переводит пользователя на "
        "/start. Лента сигналов размещена по адресу /signals, карточка отдельного "
        "объекта – по адресу /signals/[id]. Неизвестный идентификатор, например "
        "/signals/unknown, вызывает notFound().",
    )

    add_table(
        doc,
        ["Назначение", "Каталог app", "URL"],
        [
            ["Редирект на старт", "page.tsx", "/ → /start"],
            ["Стартовая страница", "start/page.tsx", "/start"],
            ["Лента сигналов", "signals/page.tsx", "/signals"],
            ["Карточка сигнала", "signals/[id]/page.tsx", "/signals/{id}"],
            ["О проекте", "about/page.tsx", "/about"],
            ["Личный кабинет", "cabinet/page.tsx", "/cabinet"],
            ["Вход", "auth/login/page.tsx", "/auth/login"],
            ["Регистрация", "auth/register/page.tsx", "/auth/register"],
        ],
    )

    add_body(
        doc,
        "Файл page.tsx задаёт содержимое сегмента URL. Файл layout.tsx задаёт общую "
        "оболочку: html, body, метаданные, DemoAuthProvider и компонент навигации "
        "AppNav. Layout не пересоздаётся полностью при переходах между вложенными "
        "страницами, поэтому состояние учебного пользователя сохраняется, пока открыта "
        "вкладка. Квадратные скобки в имени каталога [id] объявляют динамический "
        "сегмент. В актуальном App Router params приходят как Promise, поэтому "
        "идентификатор читается через await params.",
    )
    add_body(
        doc,
        "Данные хранятся в типизированном массиве neighborSignals файла "
        "app/data/signals.ts. Это не база данных. У объекта есть id, title, summary "
        "и предметное поле category со значениями «ищу», «отдаю», «предупреждаю». "
        "Страницы /start, /signals, /signals/[id] и /about остаются Server Components. "
        "Директива «use client» стоит у AppNav, DemoAuthProvider, форм и кабинета, "
        "потому что им нужны useState, usePathname и обработчики событий.",
    )

    add_picture(doc, "fig_tree.png", "Рисунок 1 – Структура каталога app")

    add_body(
        doc,
        "Компонент Link из next/link выполняет клиентские переходы без полной "
        "перезагрузки документа и сохраняет layout. Активный пункт навигации "
        "отмечается через usePathname и атрибут aria-current=\"page\".",
    )
    add_picture(doc, "fig_signals.png", "Рисунок 2 – Лента сигналов /signals")
    add_picture(
        doc,
        "fig_signal_id.png",
        "Рисунок 3 – Динамическая страница /signals/lost-keys",
    )

    add_body(
        doc,
        "DemoAuthProvider хранит объект User | null в useState и отдаёт функции "
        "login, register и logout через React Context. Функция login берёт отображаемое "
        "имя из локальной части email, register – из поля имени. Пароль на клиенте "
        "не сохраняется. После обновления страницы состояние обнуляется, cookie-сессии "
        "нет, сервер пароль не проверяет. Это прототип интерфейса, а не средство "
        "безопасности: скрытие кнопки «Выйти» не защищает данные и будущие операции.",
    )
    add_picture(
        doc,
        "fig_login_error.png",
        "Рисунок 4 – Форма входа с ошибкой короткого пароля",
    )
    add_picture(
        doc,
        "fig_cabinet.png",
        "Рисунок 5 – Личный кабинет после учебного входа",
    )

    add_body(
        doc,
        "Различия понятий, которые методичка требует явно зафиксировать, сведены "
        "в таблицу. Реализованный прототип закрывает только первый столбец на уровне "
        "интерфейса и не подменяет серверную сессию и авторизацию лабораторных работ "
        "№ 6–7.",
    )
    add_table(
        doc,
        ["Понятие", "Смысл", "В данной работе"],
        [
            [
                "Аутентификация",
                "Проверка, что пользователь тот, за кого себя выдаёт",
                "Форма принимает email и пароль, пароль на сервер не уходит",
            ],
            [
                "Сессия",
                "Сохранение факта входа между запросами",
                "useState в провайдере; после reload пользователь исчезает",
            ],
            [
                "Авторизация",
                "Проверка права выполнить операцию",
                "Условный рендер кнопок; серверной проверки нет",
            ],
        ],
    )

    add_body(
        doc,
        "Выполнены проверки npm run lint и npm run build. ESLint завершился без "
        "ошибок. Production-сборка скомпилировалась успешно. Маршруты /start, /signals, "
        "/about, /cabinet, /auth/login и /auth/register сформированы как статические, "
        "маршрут /signals/[id] – как динамический (server-rendered on demand).",
    )

    add_heading(doc, "4", "Контрольные вопросы")
    answers = [
        (
            "Как каталог app преобразуется в URL?",
            "Каждый вложенный каталог становится сегментом пути. Файл page.tsx "
            "в этом каталоге обслуживает соответствующий адрес: app/signals/page.tsx "
            "даёт /signals, app/auth/login/page.tsx даёт /auth/login.",
        ),
        (
            "Чем page.tsx отличается от layout.tsx?",
            "page.tsx – содержимое конкретного маршрута. layout.tsx – общая оболочка "
            "сегмента и всех вложенных страниц; он принимает children и сохраняется "
            "при клиентских переходах.",
        ),
        (
            "Для чего используются квадратные скобки в имени каталога?",
            "Они объявляют динамический сегмент. Каталог signals/[id] обрабатывает "
            "любой адрес вида /signals/lost-keys, а значение id доступно в params.",
        ),
        (
            "Почему params в актуальном App Router получают через await?",
            "В используемых версиях Next.js params передан как Promise. Без await "
            "TypeScript и runtime не отдают готовый объект с полем id.",
        ),
        (
            "Когда требуется директива \"use client\"?",
            "Когда модуль использует клиентские хуки или обработчики браузерных "
            "событий: useState, usePathname, onClick, onSubmit. Серверные страницы "
            "ленты и карточки сигнала в этой директиве не нуждаются.",
        ),
        (
            "Какие преимущества даёт Link по сравнению с полной перезагрузкой?",
            "Клиентский переход сохраняет layout и состояние провайдера, не скачивает "
            "документ заново и может заранее подгружать маршрут.",
        ),
        (
            "Чем аутентификация отличается от авторизации?",
            "Аутентификация отвечает на вопрос «кто это?». Авторизация отвечает на "
            "вопрос «имеет ли этот субъект право выполнить действие?».",
        ),
        (
            "Для чего нужна сессия?",
            "Чтобы не заставлять пользователя предъявлять учётные данные на каждый "
            "запрос и чтобы сервер мог связать последующие обращения с уже проверенным "
            "пользователем. В ЛР2 сессия имитируется только в памяти вкладки.",
        ),
        (
            "Почему скрытая кнопка не защищает серверную операцию?",
            "Клиентский интерфейс можно обойти прямым HTTP-запросом. Решение о доступе "
            "должно приниматься на сервере по проверенной сессии, а не по видимости "
            "элемента в React.",
        ),
        (
            "Почему DemoAuthProvider сбрасывается после обновления страницы?",
            "Состояние хранится в useState. Обновление документа уничтожает дерево "
            "React и создаёт провайдер заново с user = null.",
        ),
        (
            "Какие части прототипа будут заменены после подключения PostgreSQL и Prisma?",
            "Массив сигналов – таблицами базы, DemoAuthProvider – проверкой пароля, "
            "cookie-сессией и маршрутами /api/auth, условный рендер кабинета – "
            "серверной авторизацией защищённых операций.",
        ),
    ]
    for question, answer in answers:
        add_body(doc, f"{question} {answer}")

    add_heading(doc, "5", "Вывод")
    add_body(
        doc,
        "В ходе работы каркас SignalBoard расширен до многостраничного приложения "
        "на App Router. Реализованы общая навигация, лента сигналов, динамический "
        "маршрут отдельного объекта, учебные формы входа и регистрации и условный "
        "интерфейс кабинета. Прототип явно отделён от защищённой авторизации: пароль "
        "не проверяется сервером, сессия не переживает обновление страницы, скрытие "
        "элементов UI не считается контролем доступа. Проверки lint и production-сборка "
        "завершились без ошибок.",
    )

    add_center(doc, "ПРИЛОЖЕНИЕ А", bold=True)
    add_center(doc, "Листинг с кодом программы", bold=True)

    listings = [
        ("Файл app/data/signals.ts", read_src("app", "data", "signals.ts")),
        ("Файл app/signals/page.tsx", read_src("app", "signals", "page.tsx")),
        ("Файл app/signals/[id]/page.tsx", read_src("app", "signals", "[id]", "page.tsx")),
        (
            "Файл app/providers/DemoAuthProvider.tsx",
            read_src("app", "providers", "DemoAuthProvider.tsx"),
        ),
        ("Файл app/auth/login/page.tsx", read_src("app", "auth", "login", "page.tsx")),
        (
            "Файл app/auth/register/page.tsx",
            read_src("app", "auth", "register", "page.tsx"),
        ),
        ("Файл app/layout.tsx", read_src("app", "layout.tsx")),
        ("Файл app/ui/AppNav.tsx", read_src("app", "ui", "AppNav.tsx")),
        ("Файл app/page.tsx", read_src("app", "page.tsx")),
        ("Файл app/cabinet/page.tsx", read_src("app", "cabinet", "page.tsx")),
    ]
    for title, code in listings:
        add_file_title(doc, title)
        add_code(doc, code)

    doc.save(str(OUT))
    print("saved", OUT)


if __name__ == "__main__":
    build()
