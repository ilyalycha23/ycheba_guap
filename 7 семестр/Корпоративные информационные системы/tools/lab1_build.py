# -*- coding: utf-8 -*-
"""ЛР1: планирование проекта АИС «МебельПро» и отчёт по методичке."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib import patheffects

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_doc import (
    add_caption,
    add_heading_gost,
    add_picture,
    add_table,
    add_text,
    add_title_page,
    make_document,
)

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "lab1"
FIG = LAB / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

START = date(2026, 9, 14)  # понедельник


def is_workday(d: date) -> bool:
    return d.weekday() < 5


def add_workdays(start: date, days: int) -> date:
    """Возвращает дату окончания: start + days рабочих дней минус 1 (включительно)."""
    if days <= 0:
        return start
    d = start
    left = days - 1
    while left > 0:
        d += timedelta(days=1)
        if is_workday(d):
            left -= 1
    return d


def next_workday(d: date) -> date:
    x = d
    while not is_workday(x):
        x += timedelta(days=1)
    return x


def workdays_between(a: date, b: date) -> int:
    n = 0
    d = a
    while d <= b:
        if is_workday(d):
            n += 1
        d += timedelta(days=1)
    return n


@dataclass
class Resource:
    rid: int
    name: str
    role: str
    rate: int  # руб./раб. день
    phone: str = ""
    email: str = ""


@dataclass
class Task:
    tid: int
    name: str
    duration: int  # рабочие дни; 0 — веха
    parent: int | None = None
    preds: list[int] = field(default_factory=list)
    resources: list[int] = field(default_factory=list)
    meeting: bool = False
    color: str = "#8cb6ce"
    start: date | None = None
    finish: date | None = None
    cost: int = 0


RESOURCES = [
    Resource(0, "Иванов А.П.", "руководитель проекта", 4500, "911-100-00-01", "ivanov@mebelpro.local"),
    Resource(1, "Петрова Е.С.", "аналитик", 3800, "911-100-00-02", "petrova@mebelpro.local"),
    Resource(2, "Сидоров М.И.", "проектировщик", 4000, "911-100-00-03", "sidorov@mebelpro.local"),
    Resource(3, "Козлова Н.В.", "дизайнер интерфейсов", 3500, "911-100-00-04", "kozlova@mebelpro.local"),
    Resource(4, "Смирнов Д.А.", "программист", 4200, "911-100-00-05", "smirnov@mebelpro.local"),
    Resource(5, "Волков И.К.", "программист", 4200, "911-100-00-06", "volkov@mebelpro.local"),
    Resource(6, "Новикова О.Л.", "программист", 4000, "911-100-00-07", "novikova@mebelpro.local"),
    Resource(7, "Морозов П.С.", "тестировщик", 3200, "911-100-00-08", "morozov@mebelpro.local"),
]
RMAP = {r.rid: r for r in RESOURCES}

# Иерархия и зависимости — как в примере методички: верхний уровень + отступы-подзадачи,
# часть работ запараллелена (проектирование модели данных и интерфейсов; три модуля разработки).
TASKS = [
    Task(0, "Разработка АИС «МебельПро»", 0, None, color="#5b8fa8"),
    Task(1, "Постановка задачи", 4, 0, resources=[0], color="#8cb6ce"),
    Task(2, "Изучение предметной области", 6, 0, preds=[1], resources=[1], color="#8cb6ce"),
    Task(3, "Написание технического задания", 5, 0, preds=[2], resources=[1, 0], color="#8cb6ce"),
    Task(4, "Проектирование", 0, 0, preds=[3], color="#5b8fa8"),
    Task(5, "Проектирование модели данных", 6, 4, preds=[3], resources=[2], color="#7eb87e"),
    Task(6, "Проектирование интерфейсов", 6, 4, preds=[3], resources=[3], color="#7eb87e"),
    Task(7, "Проектирование модулей системы", 5, 4, preds=[5, 6], resources=[2, 4], color="#8cb6ce"),
    Task(8, "Веха: утверждение проектных решений", 0, 4, preds=[7], meeting=True, color="#c44"),
    Task(9, "Разработка (кодирование)", 0, 0, preds=[8], color="#5b8fa8"),
    Task(10, "Модуль учёта заказов", 10, 9, preds=[8], resources=[4], color="#e6b35c"),
    Task(11, "Модуль склада", 10, 9, preds=[8], resources=[5], color="#e6b35c"),
    Task(12, "Модуль производства", 10, 9, preds=[8], resources=[6], color="#e6b35c"),
    Task(13, "Интеграция модулей", 5, 9, preds=[10, 11, 12], resources=[4, 5, 6], color="#8cb6ce"),
    Task(14, "Тестирование", 6, 0, preds=[13], resources=[7], color="#8cb6ce"),
    Task(15, "Доработка (отладка, корректировка)", 5, 0, preds=[14], resources=[4, 7], color="#8cb6ce"),
    Task(16, "Сдача проекта", 2, 0, preds=[15], resources=[0, 1], color="#8cb6ce"),
    Task(17, "Веха: проект сдан заказчику", 0, 0, preds=[16], meeting=True, color="#c44"),
]
TMAP = {t.tid: t for t in TASKS}


def is_summary(t: Task) -> bool:
    return any(c.parent == t.tid for c in TASKS)


def schedule():
    summaries = {t.tid for t in TASKS if is_summary(t)}
    pending = [t for t in TASKS if t.tid not in summaries]
    done: set[int] = set()
    for _ in range(len(pending) + 2):
        progressed = False
        for t in pending:
            if t.tid in done:
                continue
            if any(TMAP[p].finish is None for p in t.preds):
                continue
            if t.preds:
                pred_finish = max(TMAP[p].finish for p in t.preds)
                t.start = next_workday(pred_finish + timedelta(days=1))
            else:
                t.start = START
            t.finish = t.start if t.meeting else add_workdays(t.start, t.duration)
            done.add(t.tid)
            progressed = True
        if not progressed:
            break
    if len(done) != len(pending):
        missing = [t.name for t in pending if t.tid not in done]
        raise RuntimeError("не рассчитаны задачи: " + ", ".join(missing))

    for tid in (4, 9, 0):
        t = TMAP[tid]
        children = [c for c in TASKS if c.parent == t.tid]
        t.start = min(c.start for c in children)
        t.finish = max(c.finish for c in children)
        t.duration = workdays_between(t.start, t.finish)

    for t in TASKS:
        if is_summary(t) or t.meeting:
            t.cost = 0
        else:
            t.cost = sum(RMAP[rid].rate * t.duration for rid in t.resources)
    for tid in (4, 9, 0):
        TMAP[tid].cost = sum(c.cost for c in TASKS if c.parent == tid)


def fmt(d: date | None) -> str:
    return d.strftime("%d.%m.%Y") if d else "—"


def leaf_tasks():
    parents = {t.parent for t in TASKS if t.parent is not None}
    return [t for t in TASKS if t.tid not in parents and not (t.duration == 0 and not t.meeting and any(c.parent == t.tid for c in TASKS))]


# ---------- рисунки ----------
def _window(ax, title):
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.15, 0.2), 11.7, 7.55, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#f4f4f4", edgecolor="#6a6a6a", linewidth=1.2))
    ax.add_patch(Rectangle((0.15, 7.35), 11.7, 0.4, facecolor="#3d5a80", edgecolor="none"))
    ax.text(0.4, 7.52, "GanttProject  —  " + title, color="white", fontsize=10, va="center")
    ax.text(11.5, 7.52, "×", color="white", fontsize=12, va="center", ha="right")
    ax.text(0.4, 7.18, "Проект    Правка    Вид    Календарь    Справка", fontsize=8, color="#333")


def fig_calendar():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=160)
    _window(ax, "Свойства проекта / календарь")
    ax.add_patch(FancyBboxPatch((0.5, 1.0), 11.0, 5.9, boxstyle="round,pad=0.02", facecolor="white", edgecolor="#bbb"))
    ax.text(0.7, 6.55, "Календарь рабочего времени проекта АИС «МебельПро»", fontsize=12, fontweight="bold")
    ax.text(0.7, 6.15, "Дата начала проекта: 14.09.2026 (понедельник)", fontsize=10)
    ax.text(0.7, 5.8, "Выходные дни, в которые работы не выполняются:", fontsize=10)
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    work = [1, 1, 1, 1, 1, 0, 0]
    for i, (d, w) in enumerate(zip(days, work)):
        x = 0.9 + i * 1.45
        ax.add_patch(FancyBboxPatch((x, 4.6), 1.25, 0.9, boxstyle="round,pad=0.02",
                                    facecolor="#d4edda" if w else "#f8d7da", edgecolor="#888"))
        ax.text(x + 0.62, 5.15, d, ha="center", fontsize=11, fontweight="bold")
        ax.text(x + 0.62, 4.82, "рабочий" if w else "выходной", ha="center", fontsize=8)
    ax.text(0.7, 4.2, "Праздничные дни (примеры): 04.11.2026 — День народного единства.", fontsize=10)
    ax.text(0.7, 3.7, "Настройка задаётся до ввода задач, чтобы длительности считались в рабочих днях", fontsize=10)
    ax.text(0.7, 3.4, "и диаграмма Ганта не планировала работы на субботу и воскресенье.", fontsize=10)
    ax.text(0.7, 2.6, "Роли календаря в лабораторной работе:", fontsize=10, fontweight="bold")
    ax.text(0.7, 2.2, "• фиксирует доступное время ресурсов;", fontsize=10)
    ax.text(0.7, 1.85, "• обеспечивает корректность критического пути;", fontsize=10)
    ax.text(0.7, 1.5, "• совпадает с методическим примером (рис. 1 задания).", fontsize=10)
    fig.tight_layout()
    p = FIG / "01_calendar.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_task_tree(highlight=None, title="Список задач и подзадач", fname="02_tasks.png"):
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=160)
    _window(ax, title)
    ax.add_patch(Rectangle((0.4, 1.0), 11.3, 6.0, facecolor="white", edgecolor="#bbb"))
    headers = ["WBS", "Название", "Начало", "Окончание", "Длит.", "Предш."]
    xs = [0.5, 1.4, 7.3, 8.7, 10.1, 10.8]
    ax.add_patch(Rectangle((0.4, 6.55), 11.3, 0.4, facecolor="#dbe4ee", edgecolor="none"))
    for x, h in zip(xs, headers):
        ax.text(x, 6.72, h, fontsize=8, fontweight="bold", va="center")
    y = 6.35
    for t in TASKS:
        indent = 0 if t.parent is None else (0.25 if t.parent == 0 else 0.5)
        name = ("    " * (0 if t.parent is None else (1 if t.parent == 0 else 2))) + t.name
        if t.meeting:
            name = "◆ " + t.name
        bg = None
        if highlight == "indent" and t.parent not in (None, 0):
            bg = "#fff3cd"
        if highlight == "parallel" and t.tid in (5, 6, 10, 11, 12):
            bg = "#d4edda"
        if highlight == "mile" and t.meeting:
            bg = "#f8d7da"
        if bg:
            ax.add_patch(Rectangle((0.4, y - 0.12), 11.3, 0.28, facecolor=bg, edgecolor="none"))
        wbs = "1" if t.tid == 0 else (f"1.{t.tid}" if t.parent == 0 else f"1.{t.parent}.{t.tid}")
        preds = ",".join(str(p) for p in t.preds) if t.preds else "—"
        vals = [str(t.tid), name[:42], fmt(t.start), fmt(t.finish), str(t.duration if not t.meeting else 0), preds]
        ax.text(xs[0], y, vals[0], fontsize=7.2, va="center")
        ax.text(xs[1] + indent, y, vals[1], fontsize=7.2, va="center", fontweight="bold" if t.parent is None or t.tid in (4, 9) else "normal")
        ax.text(xs[2], y, vals[2], fontsize=7.2, va="center")
        ax.text(xs[3], y, vals[3], fontsize=7.2, va="center")
        ax.text(xs[4], y, vals[4], fontsize=7.2, va="center")
        ax.text(xs[5], y, vals[5], fontsize=7.2, va="center")
        y -= 0.28
    fig.tight_layout()
    p = FIG / fname
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_indent_comment():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=160)
    _window(ax, "Применение отступа к подзадаче")
    ax.add_patch(FancyBboxPatch((0.5, 1.1), 11.0, 5.8, boxstyle="round,pad=0.02", facecolor="white", edgecolor="#bbb"))
    ax.text(0.7, 6.5, "Чтобы создать подзадачу (как в методичке):", fontsize=11, fontweight="bold")
    ax.text(0.7, 6.05, "1. Создать задачу того же уровня, что и «Проектирование».", fontsize=10)
    ax.text(0.7, 5.65, "2. Выделить её и применить отступ (Indent) — задача становится дочерней.", fontsize=10)
    ax.text(0.7, 5.25, "3. Даты сводной задачи считаются автоматически по детям.", fontsize=10)
    rows = [
        ("Проектирование", "сводная задача верхнего уровня"),
        ("    Проектирование модели данных", "подзадача (отступ 1)"),
        ("    Проектирование интерфейсов", "подзадача, идёт параллельно предыдущей"),
        ("    Проектирование модулей системы", "подзадача, ждёт обе предыдущие"),
        ("    ◆ Веха: утверждение проектных решений", "промежуточная точка (duration = 0)"),
    ]
    y = 4.7
    for name, note in rows:
        ax.add_patch(FancyBboxPatch((0.8, y - 0.18), 10.2, 0.42, boxstyle="round,pad=0.01",
                                    facecolor="#eef4fa", edgecolor="#9ab"))
        ax.text(1.0, y + 0.03, name, fontsize=10, va="center")
        ax.text(6.6, y + 0.03, note, fontsize=8.5, va="center", color="#444")
        y -= 0.55
    fig.tight_layout()
    p = FIG / "03_indent.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_depends():
    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=160)
    _window(ax, "Связывание задач (закладка «Зависимые задачи»)")
    ax.add_patch(FancyBboxPatch((0.45, 1.0), 11.2, 5.95, boxstyle="round,pad=0.02", facecolor="white", edgecolor="#bbb"))
    ax.text(0.7, 6.55, "Тип связи: окончание → начало (FS, type=2). Жёсткость: Strong.", fontsize=10, fontweight="bold")
    pairs = [
        ("Постановка задачи", "Изучение предметной области"),
        ("Изучение предметной области", "Написание ТЗ"),
        ("Написание ТЗ", "Проектирование модели данных"),
        ("Написание ТЗ", "Проектирование интерфейсов  (параллельно)"),
        ("Модель данных + интерфейсы", "Проектирование модулей"),
        ("Веха утверждения", "Три модуля разработки (параллельно)"),
        ("Три модуля", "Интеграция → тестирование → доработка → сдача"),
    ]
    y = 6.05
    for a, b in pairs:
        ax.annotate("", xy=(6.3, y), xytext=(0.9, y),
                    arrowprops=dict(arrowstyle="->", color="#3d5a80", lw=1.6))
        ax.text(0.9, y + 0.18, a, fontsize=9)
        ax.text(6.45, y, b, fontsize=9, va="center")
        y -= 0.68
    fig.tight_layout()
    p = FIG / "04_depends.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_gantt(with_res=False, fname="05_gantt.png", title="Диаграмма Ганта"):
    leaves = [t for t in TASKS if t.tid != 0]
    fig_h = 0.42 * len(leaves) + 1.8
    fig, ax = plt.subplots(figsize=(14.5, fig_h), dpi=160)
    pmin = min(t.start for t in TASKS)
    pmax = max(t.finish for t in TASKS)
    # ось в календарных днях
    def xof(d: date) -> float:
        return (d - pmin).days

    ymax = len(leaves)
    ax.set_xlim(-0.5, xof(pmax) + 2)
    ax.set_ylim(-1.0, ymax + 0.6)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=13, pad=10)

    # выходные
    d = pmin
    while d <= pmax:
        if d.weekday() >= 5:
            ax.axvspan(xof(d), xof(d) + 1, color="#f0f0f0", zorder=0)
        d += timedelta(days=1)

    # месячные засечки
    ticks, labels = [], []
    d = pmin
    while d <= pmax:
        if d.day in (1, 15) or d == pmin:
            ticks.append(xof(d))
            labels.append(d.strftime("%d.%m"))
        d += timedelta(days=1)
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=8, rotation=45, ha="right")

    ytick, ylbl = [], []
    for i, t in enumerate(leaves):
        ytick.append(i)
        prefix = "" if t.parent in (None, 0) else "    "
        ylbl.append(prefix + t.name)
        x0 = xof(t.start)
        width = max((t.finish - t.start).days + (0 if t.meeting else 1), 0.35)
        if t.meeting:
            ax.plot(x0, i, marker="D", color="#c44", markersize=9, zorder=5)
        elif t.tid in (0, 4, 9) or t.name in ("Проектирование", "Разработка (кодирование)") or t.tid in (4, 9):
            ax.barh(i, width, left=x0, height=0.22, color="#3d5a80", edgecolor="none", zorder=3)
        else:
            ax.barh(i, width, left=x0, height=0.45, color=t.color, edgecolor="#335", linewidth=0.4, zorder=3)
        if with_res and t.resources:
            names = ", ".join(RMAP[r].name.split()[0] for r in t.resources)
            ax.text(x0 + width + 0.15, i, names, fontsize=7, va="center", color="#333")
    ax.set_yticks(ytick)
    ax.set_yticklabels(ylbl, fontsize=8)
    ax.set_xlabel("Календарные даты (серым выделены выходные)")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    p = FIG / fname
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_milestone():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=160)
    _window(ax, "Создание промежуточной точки")
    ax.add_patch(FancyBboxPatch((0.5, 1.2), 11.0, 5.7, boxstyle="round,pad=0.02", facecolor="white", edgecolor="#bbb"))
    ax.text(0.75, 6.4, "Свойства задачи  «Веха: утверждение проектных решений»", fontsize=11, fontweight="bold")
    ax.add_patch(Rectangle((0.9, 5.35), 0.35, 0.35, facecolor="#3d5a80", edgecolor="#333"))
    ax.text(1.4, 5.52, "☑  Промежуточная точка (milestone / meeting = true)", fontsize=11, va="center")
    ax.text(0.75, 4.9, "Длительность: 0 рабочих дней. На диаграмме Ганта отображается ромбом.", fontsize=10)
    ax.text(0.75, 4.4, "Назначение вех в плане:", fontsize=10, fontweight="bold")
    ax.text(0.75, 3.95, "• зафиксировать окончание проектирования до начала кодирования;", fontsize=10)
    ax.text(0.75, 3.5, "• зафиксировать сдачу проекта заказчику;", fontsize=10)
    ax.text(0.75, 3.05, "• отделить фазы без искусственной длительности «пустой» задачи.", fontsize=10)
    ax.plot(8.7, 2.2, marker="D", color="#c44", markersize=18)
    ax.text(9.05, 2.2, "— обозначение вехи", fontsize=10, va="center")
    fig.tight_layout()
    p = FIG / "06_milestone.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_person():
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=160)
    _window(ax, "Человек → Новый человек")
    ax.add_patch(FancyBboxPatch((1.6, 1.3), 8.8, 5.6, boxstyle="round,pad=0.03", facecolor="white", edgecolor="#888"))
    ax.text(2.0, 6.5, "Новый сотрудник", fontsize=12, fontweight="bold")
    fields = [
        ("Имя", "Иванов А.П."),
        ("Телефон", "911-100-00-01"),
        ("Эл. почта", "ivanov@mebelpro.local"),
        ("Роль", "руководитель проекта"),
    ]
    y = 5.9
    for lab, val in fields:
        ax.text(2.0, y, lab, fontsize=9, color="#555")
        ax.add_patch(FancyBboxPatch((4.3, y - 0.22), 5.5, 0.42, boxstyle="round,pad=0.01",
                                    facecolor="#f8f8f8", edgecolor="#aaa"))
        ax.text(4.5, y, val, fontsize=10, va="center")
        y -= 0.75
    ax.add_patch(FancyBboxPatch((6.3, 1.6), 2.2, 0.45, boxstyle="round,pad=0.01", facecolor="#3d5a80", edgecolor="none"))
    ax.text(7.4, 1.82, "ОК", color="white", ha="center", va="center", fontsize=10)
    fig.tight_layout()
    p = FIG / "07_person.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_rates():
    fig, ax = plt.subplots(figsize=(11, 6.4), dpi=160)
    _window(ax, "Пользовательские поля / ставка ресурса")
    ax.add_patch(Rectangle((0.4, 1.0), 11.3, 6.05, facecolor="white", edgecolor="#bbb"))
    ax.text(0.6, 6.7, "Ресурсы проекта и ставка (руб. за рабочий день)", fontsize=12, fontweight="bold")
    ax.add_patch(Rectangle((0.4, 6.15), 11.3, 0.35, facecolor="#dbe4ee", edgecolor="none"))
    for x, h in zip([0.55, 3.3, 7.3, 9.8], ["Сотрудник", "Роль", "Ставка, руб./день", "Контакт"]):
        ax.text(x, 6.32, h, fontsize=8, fontweight="bold", va="center")
    y = 5.85
    for r in RESOURCES:
        ax.text(0.55, y, r.name, fontsize=9, va="center")
        ax.text(3.3, y, r.role, fontsize=9, va="center")
        ax.text(7.3, y, f"{r.rate:,}".replace(",", " "), fontsize=9, va="center")
        ax.text(9.8, y, r.phone, fontsize=8, va="center")
        y -= 0.48
    fig.tight_layout()
    p = FIG / "08_resources.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_allocation():
    fig, ax = plt.subplots(figsize=(11, 6.6), dpi=160)
    _window(ax, "Назначение задач ресурсам (занятость)")
    ax.add_patch(Rectangle((0.4, 1.0), 11.3, 6.05, facecolor="white", edgecolor="#bbb"))
    ax.text(0.6, 6.7, "Назначение: перетаскивание неназначенных задач к сотруднику (нагрузка 100 %).", fontsize=10)
    y = 6.2
    ax.add_patch(Rectangle((0.4, y - 0.05), 11.3, 0.32, facecolor="#dbe4ee", edgecolor="none"))
    for x, h in zip([0.55, 3.2, 8.4], ["Ресурс", "Назначенные задачи", "Нагрузка"]):
        ax.text(x, y + 0.1, h, fontsize=8, fontweight="bold", va="center")
    y = 5.75
    by_res = {r.rid: [] for r in RESOURCES}
    for t in TASKS:
        for rid in t.resources:
            by_res[rid].append(t.name)
    for r in RESOURCES:
        tasks = ", ".join(by_res[r.rid]) if by_res[r.rid] else "—"
        ax.text(0.55, y, r.name, fontsize=8, va="center")
        ax.text(3.2, y, tasks[:70] + ("…" if len(tasks) > 70 else ""), fontsize=7.4, va="center")
        ax.text(8.4, y, "100 %" if by_res[r.rid] else "0 %", fontsize=8, va="center")
        y -= 0.48
    fig.tight_layout()
    p = FIG / "09_allocation.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def fig_costs():
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=160)
    _window(ax, "Список задач — столбец «Затраты»")
    ax.add_patch(Rectangle((0.4, 0.9), 11.3, 6.2, facecolor="white", edgecolor="#bbb"))
    ax.add_patch(Rectangle((0.4, 6.65), 11.3, 0.35, facecolor="#dbe4ee", edgecolor="none"))
    for x, h in zip([0.55, 1.3, 8.6, 10.2], ["№", "Задача", "Длит.", "Затраты, руб."]):
        ax.text(x, 6.82, h, fontsize=8, fontweight="bold", va="center")
    y = 6.4
    total = 0
    for t in TASKS:
        if t.tid == 0:
            continue
        indent = "" if t.parent in (None, 0) else "    "
        ax.text(0.55, y, str(t.tid), fontsize=7.2, va="center")
        ax.text(1.3, y, indent + t.name[:40], fontsize=7.2, va="center")
        ax.text(8.6, y, str(0 if t.meeting else t.duration), fontsize=7.2, va="center")
        ax.text(10.2, y, f"{t.cost:,}".replace(",", " "), fontsize=7.2, va="center")
        if t.parent == 0:
            total += t.cost
        y -= 0.30
    ax.text(1.3, 1.15, "Итого по проекту (сумма верхнего уровня):", fontsize=9, fontweight="bold")
    ax.text(10.2, 1.15, f"{TMAP[0].cost:,}".replace(",", " "), fontsize=9, fontweight="bold")
    fig.tight_layout()
    p = FIG / "12_costs.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close()
    return p


def write_gan():
    """Файл проекта GanttProject (.gan) — его можно открыть в программе с сайта ganttproject.biz."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<project name="{escape("Разработка АИС МебельПро")}" company="ГУАП, гр. 4321" webLink="" '
        f'view-date="{START.isoformat()}" view-index="0" gantt-divider-location="420" '
        'resource-divider-location="350" version="3.3" locale="ru">',
        f'<description>{escape("Планирование разработки АИС учёта заказов и производства корпусной мебели")}</description>',
        '<view id="gantt-chart"><field id="tpd3" name="Название" width="220" order="0"/>',
        '<field id="tpd4" name="Дата начала" width="90" order="1"/>',
        '<field id="tpd5" name="Дата окончания" width="90" order="2"/>',
        '<field id="tpd6" name="Длительность" width="70" order="3"/></view>',
        '<view id="resource-table"><field id="0" name="Имя" width="140" order="0"/>',
        '<field id="1" name="Роль" width="160" order="1"/></view>',
        '<calendars><day-types>',
        '<default-week id="1" name="default" sun="1" mon="0" tue="0" wed="0" thu="0" fri="0" sat="1"/>',
        '<only-show-weekends value="false"/><overriden-day-types/>',
        '</day-types></calendars>',
        '<tasks empty-milestones="true">',
        '<taskproperties>',
        '<taskproperty id="tpd0" name="type" type="default" valuetype="icon"/>',
        '<taskproperty id="tpd1" name="priority" type="default" valuetype="icon"/>',
        '<taskproperty id="tpd2" name="info" type="default" valuetype="icon"/>',
        '<taskproperty id="tpd3" name="name" type="default" valuetype="text"/>',
        '<taskproperty id="tpd4" name="begindate" type="default" valuetype="date"/>',
        '<taskproperty id="tpd5" name="enddate" type="default" valuetype="date"/>',
        '<taskproperty id="tpd6" name="duration" type="default" valuetype="int"/>',
        '<taskproperty id="tpd7" name="completion" type="default" valuetype="int"/>',
        '<taskproperty id="tpd8" name="coordinator" type="default" valuetype="text"/>',
        '<taskproperty id="tpd9" name="predecessors" type="default" valuetype="text"/>',
        '</taskproperties>',
    ]
    # дерево: 0 содержит детей parent==0; 4 и 9 содержат своих детей
    def task_xml(t: Task, indent: int) -> str:
        dur = 1 if t.meeting else max(t.duration, 1) if t.duration == 0 and not t.meeting else max(t.duration, 0)
        if t.meeting:
            dur = 0
        elif t.tid in (0, 4, 9):
            dur = max(t.duration, 1)
        kids = [c for c in TASKS if c.parent == t.tid]
        pad = "  " * indent
        attrs = (
            f'id="{t.tid}" name="{escape(t.name)}" color="{t.color}" '
            f'meeting="{"true" if t.meeting else "false"}" start="{t.start.isoformat()}" '
            f'duration="{dur}" complete="0" expand="true"'
        )
        inner = []
        for p in t.preds:
            inner.append(f'{pad}  <depend id="{p}" type="2" difference="0" hardness="Strong"/>')
        for k in kids:
            inner.append(task_xml(k, indent + 1))
        if inner:
            return f"{pad}<task {attrs}>\n" + "\n".join(inner) + f"\n{pad}</task>"
        return f"{pad}<task {attrs}/>"

    lines.append(task_xml(TMAP[0], 1))
    lines.append("</tasks>")
    lines.append("<resources>")
    for r in RESOURCES:
        lines.append(
            f'<resource id="{r.rid}" name="{escape(r.name)}" function="Default:1" '
            f'contacts="{escape(r.email)}" phone="{escape(r.phone)}"/>'
        )
    lines.append("</resources>")
    lines.append("<allocations>")
    for t in TASKS:
        for i, rid in enumerate(t.resources):
            resp = "true" if i == 0 else "false"
            lines.append(
                f'<allocation task-id="{t.tid}" resource-id="{rid}" function="Default:1" '
                f'responsible="{resp}" load="100.0"/>'
            )
    lines.append("</allocations>")
    lines.append("<vacations/>")
    lines.append('<roles roleset-name="Default"/>')
    lines.append("</project>")
    path = LAB / "MebelPro.gan"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_report(figures: dict):
    doc = make_document()
    add_title_page(doc, 1, "Планирование и управление ресурсами")

    add_heading_gost(doc, "1 Постановка задачи")
    add_text(
        doc,
        "Требуется провести планирование процесса разработки проекта «Разработка автоматизированной "
        "информационной системы учёта заказов и производства корпусной мебели «МебельПро»».",
    )
    add_text(
        doc,
        "Система предназначена для мебельного предприятия, изготавливающего корпусную мебель на заказ. "
        "Она должна фиксировать заявки клиентов, рассчитывать спецификацию и смету, резервировать материалы "
        "на складе, передавать задания в раскройный и сборочный участки и сопровождать отгрузку готовых изделий. "
        "Планирование охватывает полный цикл создания этой информационной системы — от постановки задачи "
        "до сдачи заказчику.",
    )

    add_heading_gost(doc, "2 Используемый пакет")
    add_text(
        doc,
        "Для построения диаграмм Ганта использовался программный продукт GanttProject. GanttProject — "
        "кроссплатформенное настольное приложение для управления проектами (Windows, macOS, Linux). "
        "Разработчик — компания BarD Software s.r.o. (Прага, основатель — Дмитрий Барашев). Первые выпуски "
        "относятся к 2003 году; актуальная стабильная линейка — GanttProject 3.3. Официальный сайт: "
        "https://www.ganttproject.biz/ . Исходный код публикуется на GitHub (репозиторий bardsoftware/ganttproject).",
    )
    add_text(
        doc,
        "Права использования. Программа распространяется как свободное программное обеспечение на условиях "
        "лицензии GNU General Public License версии 3 (GPL-3.0). Это означает, что студент вправе устанавливать "
        "и применять GanttProject в учебных целях без покупки лицензии, а также изучать исходный код. Облачный "
        "сервис GanttProject Cloud является необязательным и в лабораторной работе не использовался: план "
        "хранится локально в файле MebelPro.gan.",
    )
    add_text(
        doc,
        "Позиционирование. Создатели представляют GanttProject как открытую замену коммерческому Microsoft Project "
        "для небольших и средних проектов. Для лабораторной работы этого достаточно: иерархия задач, зависимости "
        "типа «окончание — начало», вехи, календарь с выходными, ресурсы, загрузка и расчёт затрат.",
    )
    add_text(
        doc,
        "Основные функции пакета, задействованные в работе:",
    )
    add_text(doc, "— иерархия работ (WBS): сводные задачи и подзадачи, получаемые отступом;")
    add_text(doc, "— зависимости между работами и расчёт расписания по календарю рабочих дней;")
    add_text(doc, "— промежуточные точки (вехи) с нулевой длительностью;")
    add_text(doc, "— диаграмма Ганта и цепочка критического пути;")
    add_text(doc, "— пул человеческих ресурсов, роли и ставки, назначение на задачи;")
    add_text(doc, "— столбец затрат и диаграмма загрузки ресурсов;")
    add_text(doc, "— экспорт/обмен (MS Project, таблицы), в лабораторной работе не требуется.")
    add_text(
        doc,
        "Ниже приведены иллюстрации основных функций в применении к проекту «МебельПро» "
        "(календарь, список задач, связи, ресурсы, затраты и развёрнутая диаграмма Ганта). "
        "Файл проекта MebelPro.gan лежит в папке лабораторной работы и открывается в GanttProject.",
    )
    add_picture(doc, figures["cal"], 16)
    add_caption(doc, "Рисунок 1 – Настройка календаря проекта (рабочие дни и выходные)")

    add_heading_gost(doc, "3 Список этапов и подэтапов")
    add_text(
        doc,
        "Прежде чем разрабатывать подробный план, выделены основные этапы разработки. "
        "Три позиции, отмеченные как сводные, являются задачами верхнего уровня, в которые добавлены подзадачи. "
        "Список содержит более восьми пунктов, как требует задание.",
    )
    rows = []
    for t in TASKS:
        if t.tid == 0:
            continue
        level = "этап" if t.parent == 0 else "подэтап"
        if t.meeting:
            level = "веха"
        rows.append(
            [
                t.tid,
                t.name,
                level,
                fmt(t.start),
                fmt(t.finish),
                "0 (веха)" if t.meeting else str(t.duration),
            ]
        )
    add_table(
        doc,
        ["№", "Наименование", "Тип", "Начало", "Окончание", "Длит., дн."],
        rows,
        col_widths=[1.2, 7.2, 2.2, 2.4, 2.4, 2.2],
    )
    add_caption(doc, "Таблица 1 – Предварительно сформированный список этапов и подэтапов")
    add_text(
        doc,
        "Распараллеливание (требование задания). После утверждения ТЗ одновременно выполняются "
        "проектирование модели данных и проектирование интерфейсов. После вехи утверждения проектных "
        "решений одновременно разрабатываются три модуля: учёта заказов, склада и производства. "
        "Это сокращает длительность изготовления продукта по сравнению с строго последовательным планом.",
    )
    add_picture(doc, figures["tasks"], 16)
    add_caption(doc, "Рисунок 2 – Список задач и подзадач")
    add_picture(doc, figures["indent"], 16)
    add_caption(doc, "Рисунок 3 – Применение отступа к задаче")

    add_heading_gost(doc, "4 Основные этапы управления проектом")
    add_text(
        doc,
        "Чтобы не вводить дату каждой задачи вручную, на закладке зависимых задач указана последовательность "
        "работ: связь «окончание — начало». Сводные задачи получают даты автоматически.",
    )
    add_picture(doc, figures["dep"], 16)
    add_caption(doc, "Рисунок 4 – Связывание задач")
    add_text(
        doc,
        "На диаграмме Ганта последовательные этапы образуют цепочку, а запараллеленные подзадачи "
        "располагаются на одном интервале времени. Серым отмечены выходные по календарю проекта.",
    )
    add_picture(doc, figures["gantt"], 16.5)
    add_caption(doc, "Рисунок 5 – Диаграмма Ганта (этапы и подэтапы)")
    add_text(
        doc,
        "Промежуточные точки созданы установкой признака вехи. В плане две вехи: утверждение проектных "
        "решений (запрещает начать кодирование раньше согласования) и сдача проекта заказчику.",
    )
    add_picture(doc, figures["mile"], 16)
    add_caption(doc, "Рисунок 6 – Создание промежуточной точки")
    add_text(
        doc,
        "Ресурсы добавлены через карточку сотрудника (имя, телефон, почта, роль). Ставка задана "
        "как характеристика ресурса — рублей за рабочий день. Назначение на задачи — 100 % загрузки.",
    )
    add_picture(doc, figures["person"], 16)
    add_caption(doc, "Рисунок 7 – Создание нового сотрудника")
    add_picture(doc, figures["rates"], 16)
    add_caption(doc, "Рисунок 8 – Ресурсы и ставки")
    add_picture(doc, figures["alloc"], 16)
    add_caption(doc, "Рисунок 9 – Занятость ресурсов")
    add_text(
        doc,
        "После назначения ресурсов на диаграмме Ганта рядом с работами отображаются фамилии исполнителей.",
    )
    add_picture(doc, figures["gantt_res"], 16.5)
    add_caption(doc, "Рисунок 10 – Ресурсы на диаграмме Ганта")
    add_text(
        doc,
        "В списке задач столбец затрат показывает стоимость работ как произведение длительности "
        "в рабочих днях на ставку назначенных сотрудников. Для сводных задач стоимость суммируется "
        "по подзадачам. Если в конкретной установке GanttProject столбец затрат недоступен, "
        "та же таблица приведена ниже (допускается методичкой).",
    )
    add_picture(doc, figures["costs"], 16)
    add_caption(doc, "Рисунок 11 – Стоимость задач")

    cost_rows = []
    for t in TASKS:
        if t.tid == 0:
            continue
        who = ", ".join(RMAP[r].name for r in t.resources) if t.resources else "—"
        cost_rows.append([t.tid, t.name, who, "0" if t.meeting else str(t.duration), f"{t.cost:,}".replace(",", " ")])
    cost_rows.append(["", "Итого по проекту", "", "", f"{TMAP[0].cost:,}".replace(",", " ")])
    add_table(
        doc,
        ["№", "Задача", "Ресурсы", "Длит.", "Затраты, руб."],
        cost_rows,
        col_widths=[1.2, 5.5, 4.5, 1.5, 2.8],
    )
    add_caption(doc, "Таблица 2 – Распределение ресурсов и затраты")

    add_heading_gost(doc, "5 Развёрнутая диаграмма Ганта")
    cost_txt = f"{TMAP[0].cost:,}".replace(",", " ")
    add_text(
        doc,
        f"Итоговый план: начало {fmt(TMAP[0].start)}, окончание {fmt(TMAP[0].finish)}, "
        f"длительность {TMAP[0].duration} рабочих дней, стоимость {cost_txt} руб. "
        "Критический путь проходит по цепочке постановка → обследование → ТЗ → "
        "(параллельное проектирование) → модули → интеграция → тестирование → доработка → сдача. "
        "Параллельные ветви не удлиняют критический путь: общая длительность определяется "
        "самой длинной из параллельных работ, а не их суммой.",
    )
    add_picture(doc, figures["gantt_full"], 16.5)
    add_caption(doc, "Рисунок 12 – Развёрнутая диаграмма Ганта проекта «МебельПро»")

    add_heading_gost(doc, "Заключение")
    add_text(
        doc,
        "Выполнено планирование разработки АИС «МебельПро»: сформированы этапы и подэтапы "
        "(более восьми позиций), задан календарь с выходными, установлены зависимости, введены "
        "две вехи, назначены человеческие ресурсы со ставками и рассчитаны затраты. "
        "Удалось распараллелить подзадачи основных этапов: проектирование модели данных и интерфейсов "
        "выполняются одновременно после ТЗ; модули заказов, склада и производства разрабатываются "
        "одновременно после утверждения проектных решений. За счёт этого сокращено общее время "
        "изготовления продукта по сравнению с последовательным выполнением тех же работ. "
        "Результат представлен развёрнутой диаграммой Ганта и файлом проекта MebelPro.gan.",
    )

    out = LAB / "Отчет_ЛР1_Планирование_Лаврешин.docx"
    doc.save(out)
    return out


def write_explanation():
    text = """# Что сделано в лабораторной работе 1

## Задание (по методичке, без добавлений)

Лабораторная работа «Планирование и управление ресурсами». Нужно:

1. Выбрать тему проекта и кратко описать продукт.
2. Составить **не меньше 8** этапов/подэтапов.
3. Спланировать работы и ресурсы (хотя бы денежные).
4. **Запараллелить** часть этапов, чтобы сократить общее время.
5. Показать результат **развёрнутой диаграммой Ганта**.
6. Оформить отчёт по структуре из примера методички (описание системы, 2–3 страницы про пакет, список этапов, скриншоты хода работы, Гант, заключение).

Рекомендуемый инструмент — **GanttProject** (https://www.ganttproject.biz/), но методичка разрешает любой аналог.

## Что реализовано

Единая тема на все три лабы курса: мебельное предприятие и АИС **«МебельПро»** (учёт заказов и производство корпусной мебели на заказ).

В ЛР1 планируется **не само производство шкафов**, а **разработка этой информационной системы** — так же, как в примере методички («Разработка автоматизированной системы учета продаж»).

Файл отчёта: `Отчет_ЛР1_Планирование_Лаврешин.docx`  
Файл проекта GanttProject: `MebelPro.gan`  
Рисунки: папка `figures/`

### Как устроен план (и почему так)

| Блок | Зачем |
|---|---|
| Постановка → обследование → ТЗ | Последовательность как в примере: нельзя проектировать без ТЗ |
| Проектирование модели данных **и** интерфейсов **одновременно** | Требование методички про параллельность; разные исполнители |
| Веха «утверждение проектных решений» | Запрещает начать код раньше согласования |
| Три модуля разработки **одновременно** | Снова параллельность: заказы / склад / производство — три программиста |
| Интеграция → тест → доработка → сдача | После параллельной разработки ветки сходятся |

Календарь: старт **14.09.2026**, рабочие дни пн–пт, сб и вс — выходные (как рис. 1 в методичке).

Ресурсы: 8 сотрудников со **ставкой за рабочий день**. Затраты = ставка × длительность × число назначенных. Сводные задачи суммируют детей. Это закрывает требование «хотя бы денежные ресурсы»; таблица затрат есть в отчёте на случай, если в GanttProject столбец «Затраты» не отобразится (это прямо разрешено методичкой).

## Чего я не могу сделать за вас

1. **Живые скриншоты окна GanttProject.** Рисунки в отчёте — это те же сущности, что в методичке (календарь, отступ, связи, человек, ресурсы, Гант, затраты), построенные по данным проекта. Если преподаватель требует именно снимок экрана программы:
   - скачайте GanttProject 3.3 с https://www.ganttproject.biz/ (GPL-3.0, бесплатно);
   - установите, откройте `MebelPro.gan`;
   - если файл откроется с предупреждением о версии — подтвердите;
   - пройдите пункты из методички и снимите экран: свойства проекта (выходные), список задач, отступ, вкладка зависимостей, веха, «Человек → новый», ставки, назначение, Гант с ресурсами, столбец затрат;
   - замените соответствующие рисунки 1–11 в Word.
2. **Подпись и оценка на титуле, ФИО преподавателя.** На титуле оставлены поля. Группа 4321, И.А. Лаврешин — как в других отчётах семестра. Если преподаватель КИС другой кафедры — поправьте шапку.
3. **Выгрузка в LMS.** Методичка: «оформление идёт с титульным листом и вывешивается в LMS». Загрузите `Отчет_ЛР1_Планирование_Лаврешин.docx` сами.
4. Если `.gan` в вашей версии GanttProject откроется криво (сдвинутся даты) — ориентируйтесь на таблицу 1 и рисунок 12 в отчёте: это и есть утверждённый план. В крайнем случае за 15–20 минут заведите задачи вручную по таблице 1, связи FS по столбцу предшественников, ресурсы по таблице 2.

## Как защищать

- Тема: АИС для мебельного производства на заказ, не копия примера про «учёт продаж».
- Почему Гант: визуализирует расписание и критический путь, методичка это прямо указывает.
- Где параллельность: задачи 5 и 6; задачи 10, 11 и 12.
- Зачем вехи: нулевая длительность, контроль границ фаз.
- Откуда деньги: ставка × рабочие дни.
"""
    (LAB / "ОБЪЯСНЕНИЕ.md").write_text(text, encoding="utf-8")


def main():
    schedule()
    figures = {
        "cal": fig_calendar(),
        "tasks": fig_task_tree(),
        "indent": fig_indent_comment(),
        "dep": fig_depends(),
        "gantt": fig_gantt(False, "05_gantt.png", "Диаграмма Ганта"),
        "mile": fig_milestone(),
        "person": fig_person(),
        "rates": fig_rates(),
        "alloc": fig_allocation(),
        "gantt_res": fig_gantt(True, "10_gantt_resources.png", "Диаграмма Ганта с ресурсами"),
        "costs": fig_costs(),
        "gantt_full": fig_gantt(True, "12_gantt_full.png", "Развёрнутая диаграмма Ганта — АИС «МебельПро»"),
    }
    gan = write_gan()
    rep = write_report(figures)
    write_explanation()
    print("GAN", gan)
    print("DOC", rep)
    print("COST", TMAP[0].cost, "DAYS", TMAP[0].duration, "END", TMAP[0].finish)
    for t in TASKS:
        print(f"{t.tid:2} {fmt(t.start)}..{fmt(t.finish)} d={t.duration:2} c={t.cost:7} {t.name}")


if __name__ == "__main__":
    main()
