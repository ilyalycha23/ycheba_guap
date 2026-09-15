# -*- coding: utf-8 -*-
"""ЛР3: UML структурное моделирование АИС «МебельПро»."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle, Arc, PathPatch
from matplotlib.path import Path as MPath
import matplotlib.patches as mpatches

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
LAB = ROOT / "lab3"
FIG = LAB / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def new_fig(w=13.2, h=9.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=170)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    p = FIG / name
    fig.tight_layout(pad=0.2)
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


def stick_actor(ax, x, y, label):
    ax.add_patch(Circle((x, y + 8.2), 1.15, fill=False, lw=1.4, edgecolor="black"))
    ax.plot([x, x], [y + 7.05, y + 3.6], color="black", lw=1.4)
    ax.plot([x - 2.0, x + 2.0], [y + 6.1, y + 6.1], color="black", lw=1.4)
    ax.plot([x, x - 1.7], [y + 3.6, y + 1.3], color="black", lw=1.4)
    ax.plot([x, x + 1.7], [y + 3.6, y + 1.3], color="black", lw=1.4)
    ax.text(x, y + 0.2, label, ha="center", va="top", fontsize=8.5)


def oval(ax, x, y, w, h, text):
    e = Ellipse((x, y), w, h, facecolor="white", edgecolor="black", lw=1.2, zorder=3)
    ax.add_patch(e)
    ax.text(x, y, text, ha="center", va="center", fontsize=7.6, zorder=4)
    return (x, y)


def assoc(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color="black", lw=0.9, zorder=1)


def fig_usecase():
    fig, ax = new_fig(13.6, 9.4)
    ax.set_title("Диаграмма вариантов использования АИС «МебельПро»", fontsize=12, pad=8)
    ax.add_patch(Ellipse((50, 35), 64, 58, fill=False, lw=1.2))
    ax.text(50, 63.2, "АИС «МебельПро»", ha="center", fontsize=10, fontweight="bold")

    stick_actor(ax, 7, 46, "Заказчик")
    stick_actor(ax, 7, 22, "Менеджер")
    stick_actor(ax, 7, 4, "Директор")
    stick_actor(ax, 93, 46, "Кладовщик")
    stick_actor(ax, 93, 18, "Технолог")

    oval(ax, 30, 54, 20, 5.8, "Оформить заявку")
    oval(ax, 30, 44, 22, 5.8, "Согласовать смету")
    oval(ax, 52, 50, 20, 5.8, "Рассчитать смету")
    oval(ax, 30, 33, 22, 5.8, "Просмотреть статус заказа")
    oval(ax, 30, 21, 22, 5.8, "Вести заказы и договоры")
    oval(ax, 30, 10, 22, 5.8, "Просматривать отчёты")
    oval(ax, 62, 38, 22, 5.8, "Резервировать материалы")
    oval(ax, 62, 27, 22, 5.8, "Отпускать материалы в цех")
    oval(ax, 62, 16, 24, 5.8, "Формировать спецификацию")
    oval(ax, 62, 6, 26, 5.8, "Запускать производственное задание")

    assoc(ax, 9.2, 54.2, 20, 54)
    assoc(ax, 9.2, 53.5, 19, 44)
    assoc(ax, 9.2, 53.0, 19, 33)
    assoc(ax, 9.2, 30.2, 19, 21)
    assoc(ax, 9.2, 29.6, 19, 33)
    assoc(ax, 9.2, 29.2, 19, 10)
    assoc(ax, 9.2, 12.2, 19, 10)
    assoc(ax, 90.8, 54.2, 73, 38)
    assoc(ax, 90.8, 53.5, 73, 27)
    assoc(ax, 90.8, 26.2, 74, 16)
    assoc(ax, 90.8, 25.6, 75, 6)

    ax.annotate(
        "",
        xy=(42, 50),
        xytext=(41, 44.5),
        arrowprops=dict(arrowstyle="-|>", lw=0.95, linestyle=(0, (4, 3)), color="black"),
    )
    ax.text(43.5, 46.8, "<<include>>", fontsize=7, style="italic")
    return save(fig, "01_use_case.png")


def class_box(ax, x, y, w, name, attrs, methods=None):
    h_head = 4.2
    h_attr = 1.55 * max(len(attrs), 1) + 0.6
    h_m = 1.55 * max(len(methods or [" "]), 1) + 0.4
    h = h_head + h_attr + h_m
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor="black", lw=1.15, zorder=3))
    ax.plot([x, x + w], [y + h - h_head, y + h - h_head], color="black", lw=1)
    ax.plot([x, x + w], [y + h_m, y + h_m], color="black", lw=1)
    ax.text(x + w / 2, y + h - h_head / 2, name, ha="center", va="center", fontsize=8, fontweight="bold", zorder=4)
    ty = y + h - h_head - 1.1
    for a in attrs:
        ax.text(x + 0.5, ty, a, ha="left", va="center", fontsize=6.6, zorder=4)
        ty -= 1.45
    ty = y + h_m - 1.05
    for m in (methods or []):
        ax.text(x + 0.5, ty, m, ha="left", va="center", fontsize=6.6, zorder=4)
        ty -= 1.45
    return x + w / 2, y + h, x, y, w, h  # top center, bbox


def assoc_line(ax, x1, y1, x2, y2, m1="", m2="", label=""):
    ax.plot([x1, x2], [y1, y2], color="black", lw=0.95, zorder=2)
    if m1:
        ax.text(x1 + 0.4, y1 + 0.35, m1, fontsize=7)
    if m2:
        ax.text(x2 - 0.4, y2 + 0.35, m2, fontsize=7, ha="right")
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.5, label, fontsize=7, ha="center")


def fig_classes():
    fig, ax = new_fig(14.2, 9.8)
    ax.set_title("Диаграмма классов АИС «МебельПро»", fontsize=12, pad=6)

    class_box(ax, 2, 52, 22, "Пользователь",
              ["- id: int", "- логин: string", "- роль: enum"], ["+ войти()", "+ сменитьПароль()"])
    class_box(ax, 2, 18, 22, "Клиент",
              ["- id: int", "- наименование: string", "- телефон: string"], ["+ оформитьЗаявку()"])
    class_box(ax, 38, 50, 24, "Заказ",
              ["- номер: string", "- дата: date", "- статус: enum", "- сумма: money"],
              ["+ рассчитатьСмету()", "+ сменитьСтатус()"])
    class_box(ax, 38, 22, 24, "Спецификация",
              ["- id: int", "- версия: int"], ["+ добавитьПозицию()"])
    class_box(ax, 38, 2, 24, "ПозицияСпецификации",
              ["- изделие: string", "- кол-во: int", "- материал: string"], [])
    class_box(ax, 74, 52, 22, "Материал",
              ["- артикул: string", "- название: string", "- едИзм: string"], ["+ остаток()"])
    class_box(ax, 74, 26, 24, "ПроизводственноеЗадание",
              ["- номер: string", "- участок: enum", "- срок: date"], ["+ запустить()"])
    class_box(ax, 74, 4, 24, "Отгрузка",
              ["- дата: date", "- документ: string"], ["+ оформить()"])

    # Клиент 1 — * Заказ
    ax.plot([24, 38], [24, 58], color="black", lw=0.95)
    ax.text(26.5, 38.5, "1  размещает  *", fontsize=7)
    # Заказ 1 — 1 Спецификация
    ax.plot([50, 50], [50, 36.5], color="black", lw=0.95)
    ax.text(51.0, 43, "1    1", fontsize=7)
    # Спецификация 1 — * Позиция
    ax.plot([50, 50], [22, 14.5], color="black", lw=0.95)
    ax.text(51.0, 18.2, "1    *", fontsize=7)
    # Позиция * — 1 Материал
    ax.plot([62, 68, 68, 74], [8, 8, 60, 60], color="black", lw=0.95)
    ax.text(69, 33, "*    1", fontsize=7)
    # Заказ 1 — 1 Задание
    ax.plot([62, 74], [56, 40], color="black", lw=0.95)
    ax.text(66.5, 49.5, "1    1", fontsize=7)
    # Заказ 1 — 0..1 Отгрузка
    ax.plot([62, 70, 70, 74], [52, 52, 12, 12], color="black", lw=0.95)
    ax.text(71.2, 30, "1", fontsize=7)
    # Заказ * — 1 Материал
    ax.plot([62, 74], [64.2, 64.2], color="black", lw=0.95)
    ax.text(66, 65.3, "*  резервирует  1", fontsize=7)
    ax.set_ylim(0, 74)
    return save(fig, "02_classes.png")


def lifeline(ax, x, y0, y1, title):
    ax.add_patch(FancyBboxPatch((x - 8, y0), 16, 5.2, boxstyle="round,pad=0.15",
                                facecolor="#eef3f8", edgecolor="black", lw=1, zorder=3))
    ax.text(x, y0 + 2.6, title, ha="center", va="center", fontsize=8, zorder=4)
    ax.plot([x, x], [y0, y1], color="black", lw=0.9, linestyle=(0, (3, 3)), zorder=1)
    return x


def message(ax, x1, x2, y, text, dashed=False, ret=False):
    style = "-|>" if not ret else "->"
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle=style, lw=1.05,
                                linestyle="dashed" if dashed else "solid", color="black"),
                zorder=2)
    ax.text((x1 + x2) / 2, y + 0.7, text, ha="center", fontsize=7)


def activation(ax, x, y_top, y_bot):
    ax.add_patch(Rectangle((x - 0.6, y_bot), 1.2, y_top - y_bot, facecolor="white", edgecolor="black", lw=0.9, zorder=2))


def fig_sequence():
    fig, ax = new_fig(14.0, 9.4)
    ax.set_title("Диаграмма последовательности: оформление заказа", fontsize=12, pad=6)
    y_top, y_bot = 62, 6
    a = lifeline(ax, 12, y_top, y_bot, "Менеджер")
    b = lifeline(ax, 36, y_top, y_bot, "Форма заказа")
    c = lifeline(ax, 60, y_top, y_bot, "Заказ")
    d = lifeline(ax, 84, y_top, y_bot, "Спецификация")
    activation(ax, b, 56, 14)
    activation(ax, c, 48, 24)
    activation(ax, d, 40, 30)
    message(ax, a, b, 56, "1: создатьЗаявку(клиент, размеры)")
    message(ax, b, c, 48, "2: new Заказ()")
    message(ax, b, d, 40, "3: рассчитатьСпецификацию()")
    message(ax, d, b, 34, "4: состав и смета", dashed=True, ret=True)
    message(ax, b, c, 28, "5: сохранить(смета, статус=«расчёт»)")
    message(ax, b, a, 20, "6: показать смету на согласование", dashed=True, ret=True)
    ax.text(12, 10, "Альтернатива: заказчик отклоняет смету → статус «отменён», новые расчёты не сохраняются.",
            fontsize=8)
    return save(fig, "03_sequence.png")


def state(ax, x, y, w, h, name, init=False, end=False):
    if init:
        ax.add_patch(Circle((x, y), 0.9, facecolor="black", zorder=3))
        return x, y
    if end:
        ax.add_patch(Circle((x, y), 1.15, fill=False, lw=1.4, edgecolor="black", zorder=3))
        ax.add_patch(Circle((x, y), 0.65, facecolor="black", zorder=4))
        return x, y
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="white", edgecolor="black", lw=1.15, zorder=3))
    ax.text(x, y, name, ha="center", va="center", fontsize=8, zorder=4)
    return x, y


def trans(ax, x1, y1, x2, y2, label, rad=0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black",
                                connectionstyle=f"arc3,rad={rad}"), zorder=2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if rad:
        my += rad * 8
    ax.text(mx, my + 0.7, label, ha="center", fontsize=7)


def fig_states():
    fig, ax = new_fig(13.6, 8.8)
    ax.set_title("Диаграмма состояний объекта «Заказ»", fontsize=12, pad=6)
    state(ax, 8, 52, 0, 0, "", init=True)
    s_new = state(ax, 24, 52, 16, 7, "Новый")
    s_calc = state(ax, 48, 52, 16, 7, "Расчёт")
    s_agr = state(ax, 72, 52, 18, 7, "Согласован")
    s_prod = state(ax, 72, 32, 20, 7, "В производстве")
    s_qc = state(ax, 72, 16, 16, 7, "На контроле")
    s_ready = state(ax, 48, 16, 16, 7, "Готов")
    s_ship = state(ax, 24, 16, 16, 7, "Отгружен")
    s_close = state(ax, 24, 32, 16, 7, "Закрыт")
    s_can = state(ax, 48, 34, 16, 7, "Отменён")
    state(ax, 8, 32, 0, 0, "", end=True)

    trans(ax, 9.1, 52, 16, 52, "создать()")
    trans(ax, 32, 52, 40, 52, "рассчитатьСмету()")
    trans(ax, 56, 52, 63, 52, "заказчик подтвердил")
    trans(ax, 72, 48.4, 72, 35.6, "запуститьВЦех()")
    trans(ax, 72, 28.4, 72, 19.6, "сдатьНаОТК()")
    trans(ax, 64, 16, 56, 16, "ОТК: годен")
    trans(ax, 40, 16, 32, 16, "оформитьОтгрузку()")
    trans(ax, 24, 19.6, 24, 28.4, "получить оплату")
    trans(ax, 16, 32, 9.2, 32, "архивировать()")
    trans(ax, 48, 48.4, 48, 37.6, "отклонена смета")
    trans(ax, 63, 34, 57, 34, "отмена договора")
    ax.annotate(
        "",
        xy=(72, 28.6),
        xytext=(80.2, 16),
        arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black", connectionstyle="arc3,rad=-0.35"),
        zorder=2,
    )
    ax.text(86, 22, "возврат в цех", fontsize=7, ha="left")
    return save(fig, "04_states.png")


def act_box(ax, x, y, w, h, text):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.15,rounding_size=1.2",
                                facecolor="white", edgecolor="black", lw=1.15, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=8, zorder=4)


def diamond(ax, x, y, s, text):
    ax.add_patch(Polygon([(x, y + s), (x + s, y), (x, y - s), (x - s, y)],
                         closed=True, facecolor="white", edgecolor="black", lw=1.15, zorder=3))
    ax.text(x + s + 0.6, y, text, ha="left", va="center", fontsize=7.5)


def fig_activity():
    fig, ax = new_fig(12.6, 9.4)
    ax.set_title("Диаграмма деятельности: формирование отчёта об остатках материалов", fontsize=12, pad=6)
    ax.add_patch(Circle((50, 66), 1.05, facecolor="black"))
    act_box(ax, 50, 58.5, 28, 6.2, "Пользователь выбирает\n«Отчёт об остатках»")
    act_box(ax, 50, 49.5, 28, 6.2, "Система запрашивает\nсклад и период")
    act_box(ax, 50, 40.5, 28, 6.2, "Пользователь задаёт\nфильтры и нажимает «Сформировать»")
    diamond(ax, 50, 31.5, 2.4, "")
    ax.text(53.2, 31.5, "данные корректны?", fontsize=8)
    act_box(ax, 22, 31.5, 22, 6.0, "Показать сообщение\nоб ошибке ввода")
    act_box(ax, 50, 21.5, 30, 6.2, "Построить выборку остатков\nпо регистру материалов")
    act_box(ax, 50, 12.5, 28, 6.2, "Вывести отчёт на экран\nи предложить печать / файл")
    ax.add_patch(Circle((50, 4.8), 1.2, fill=False, lw=1.5, edgecolor="black"))
    ax.add_patch(Circle((50, 4.8), 0.65, facecolor="black"))

    def v(y1, y2):
        ax.annotate("", xy=(50, y2), xytext=(50, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black"))

    v(64.8, 61.7)
    v(55.3, 52.7)
    v(46.3, 43.7)
    v(37.3, 33.9)
    ax.annotate("", xy=(33.1, 31.5), xytext=(47.6, 31.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black"))
    ax.text(40, 32.6, "нет", fontsize=7)
    ax.annotate("", xy=(50, 24.7), xytext=(50, 29.1),
                arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black"))
    ax.text(51.2, 27.2, "да", fontsize=7)
    v(18.3, 15.7)
    v(9.3, 6.2)
    # loop back from error
    ax.annotate("", xy=(36, 49.5), xytext=(22, 34.6),
                arrowprops=dict(arrowstyle="-|>", lw=1.05, color="black",
                                connectionstyle="arc3,rad=0.25"))
    return save(fig, "05_activity.png")


def write_report(figs):
    doc = make_document()
    add_title_page(doc, 3, "Изучение методологии структурного моделирования UML")

    add_heading_gost(doc, "1 Постановка задачи")
    add_text(
        doc,
        "Необходимо разработать автоматизированную информационную систему учёта заказов и производства "
        "корпусной мебели «МебельПро». Основные возможности: учёт клиентов и заказов, расчёт спецификации "
        "и сметы, резервирование и отпуск материалов, запуск производственных заданий, контроль статусов "
        "заказа, отгрузка и отчёты об остатках. Предметная область совпадает с лабораторными работами 1 и 2.",
    )

    add_heading_gost(doc, "2 Диаграмма вариантов использования")
    add_text(
        doc,
        "На диаграмме пять акторов: заказчик, менеджер и директор слева; кладовщик и технолог справа. "
        "Заказчик оформляет заявку, согласовывает смету и смотрит статус. Менеджер ведёт заказы и договоры "
        "и просматривает отчёты. Кладовщик резервирует и отпускает материалы. Технолог формирует "
        "спецификацию и производственное задание. Директор получает отчёты. Связь «include» показывает, "
        "что прецедент «Согласовать смету» всегда включает «Рассчитать смету».",
    )
    add_picture(doc, figs[0], 16.5)
    add_caption(doc, "Рисунок 1 – UML-диаграмма вариантов использования")

    add_heading_gost(doc, "3 Диаграмма классов")
    add_text(
        doc,
        "Структура предметных сущностей: клиент размещает много заказов; у заказа одна спецификация "
        "с несколькими позициями; позиции ссылаются на материал; заказ порождает производственное задание "
        "и отгрузку. Пользователь моделирует роли входа в систему. Диаграмма задаёт каркас хранения данных "
        "и ответственности объектов (в методическом примере ту же роль играет ER-диаграмма плюс классы).",
    )
    add_picture(doc, figs[1], 16.5)
    add_caption(doc, "Рисунок 2 – UML-диаграмма классов")

    add_heading_gost(doc, "4 Диаграмма последовательности")
    add_text(
        doc,
        "Сценарий оформления заказа менеджером. Объекты: актор, форма, сущность «Заказ», сущность «Спецификация». "
        "Сообщения идут сверху вниз по времени. Возврат сметы на форму показан пунктиром. "
        "Альтернатива (отклонение сметы) вынесена подписью под диаграммой — без сохранения расчёта.",
    )
    add_picture(doc, figs[2], 16.5)
    add_caption(doc, "Рисунок 3 – UML-диаграмма последовательности «Оформление заказа»")

    add_heading_gost(doc, "5 Диаграмма состояний объекта «Заказ»")
    add_text(
        doc,
        "Жизненный цикл заказа: новый → расчёт → согласован → в производстве → на контроле → готов → "
        "отгружен → закрыт. Из «расчёта» и «согласован» возможна отмена. С контроля при дефекте "
        "заказ возвращается в производство — это тот же контур, что дуга возврата на IDEF0 A0/A4.",
    )
    add_picture(doc, figs[3], 16.5)
    add_caption(doc, "Рисунок 4 – UML-диаграмма состояний объекта «Заказ»")

    add_heading_gost(doc, "6 Диаграмма деятельности")
    add_text(
        doc,
        "Алгоритм получения отчёта об остатках материалов (право директора и менеджера, см. варианты использования). "
        "Ромб — проверка корректности фильтров: при ошибке система сообщает и возвращает к вводу; "
        "при успехе строится выборка и предлагается печать либо сохранение в файл.",
    )
    add_picture(doc, figs[4], 16.5)
    add_caption(doc, "Рисунок 5 – UML-диаграмма деятельности формирования отчёта об остатках")

    add_heading_gost(doc, "Заключение")
    add_text(
        doc,
        "Пятью нотациями UML описаны структурные и поведенческие особенности АИС «МебельПро»: "
        "роли и прецеденты, классы и связи, сценарий оформления заказа, жизненный цикл заказа, "
        "алгоритм отчёта. Этого достаточно для демонстрации практического умения по заданию "
        "(в методичке указано: достаточно пяти нотаций). Модель согласована с IDEF0 лабораторной работы 2 "
        "и с планом разработки лабораторной работы 1.",
    )
    out = LAB / "Отчет_ЛР3_UML_Лаврешин.docx"
    doc.save(out)
    return out


def write_explanation():
    (LAB / "ОБЪЯСНЕНИЕ.md").write_text(
        """# Что сделано в лабораторной работе 3

## Задание (по методичке)

Изучить UML. Снова два формата отчёта; выбран **сквозной авторский пример**, не реферат на 10 страниц. Нужно:

- своя информационная система, 1–2 абзаца описания;
- **достаточно 5 нотаций (рисунков)** UML, раскрывающих структурные особенности ИС;
- титул, LMS;
- инструмент любой, рекомендуется draw.io.

Виды диаграмм — на выбор. В примере методички их больше (ER, use case, sequence, robustness, state, activity). В задании явно сказано, что пяти хватает. Поэтому в отчёте ровно пять, без «лишней» теории.

## Что реализовано

Система та же: **АИС «МебельПро»**.

| № | Диаграмма | На что смотреть |
|---|---|---|
| 1 | Вариантов использования | Кто работает с системой и какие у него действия |
| 2 | Классов | Из каких сущностей состоит учёта (структура) |
| 3 | Последовательности | Как во времени оформляется заказ |
| 4 | Состояний | Как заказ меняет статус (в т.ч. возврат с ОТК) |
| 5 | Деятельности | Алгоритм отчёта об остатках |

Почему такой набор, а не пять sequence как в примере: задание просит **структурные** особенности ИС. Use case + классы дают структуру ролей и данных; sequence/state/activity показывают, как эта структура живёт. Пять одинаковых sequence структуру не раскрывают.

Связь с ЛР2: состояния заказа повторяют контур A1→A3→A4→A5 и возврат с контроля.

Отчёт: `Отчет_ЛР3_UML_Лаврешин.docx`. Рисунки: `figures/`.

## Чего я не могу сделать за вас

1. **Перерисовать диаграммы в draw.io / Visual Paradigm / StarUML**, если преподаватель требует файл конкретного редактора. Откройте https://app.diagrams.net/ → шаблоны UML и скопируйте подписи с рисунков. Use case и state там собираются быстрее всего.
2. **Реализацию в 1С.** В методическом примере система «на базе 1С:Предприятие 8.3». В задании это **не требование**, это свойство примера. Наша модель платформенно независима (как и сам UML). Если на защите спросят «а где 1С» — ответ: методичка разрешает любую ИС, 1С в примере, не в формулировке задания.
3. Титул / LMS — как в других лабах.

## Как защищать

- UML здесь «ручной» язык спецификаций (цитата методички), не генератор кода.
- Почему несколько диаграмм: принцип многомодельности из текста задания — одна модель не описывает и функции, и структуру, и время.
- Чем use case отличается от IDEF0: акторы и цели пользователей vs функции предприятия с ICOM.
- Где альтернативный поток: sequence (отклонение сметы) и activity (ошибка фильтров отчёта).
""",
        encoding="utf-8",
    )


def main():
    figs = [fig_usecase(), fig_classes(), fig_sequence(), fig_states(), fig_activity()]
    rep = write_report(figs)
    write_explanation()
    print("DOC", rep)
    for f in figs:
        print(f)


if __name__ == "__main__":
    main()
