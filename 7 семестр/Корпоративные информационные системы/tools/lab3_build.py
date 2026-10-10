# -*- coding: utf-8 -*-
"""ЛР3: UML-моделирование АИС «МебельПро» — качественные диаграммы + ГОСТ-отчёт."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle,
    Ellipse,
    FancyArrowPatch,
    FancyBboxPatch,
    Polygon,
    Rectangle,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_doc import (
    add_caption,
    add_heading_gost,
    add_picture,
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

# Палитра (спокойная, читаемая на печати)
INK = "#1f2937"
MUTED = "#64748b"
LINE = "#334155"
TITLE = "#0f172a"
UC_FILL = "#eff6ff"
UC_EDGE = "#2563eb"
CLS_HEAD = "#1e40af"
CLS_FILL = "#ffffff"
CLS_EDGE = "#1e3a8a"
ST_FILL = "#f0fdf4"
ST_EDGE = "#15803d"
ACT_FILL = "#fff7ed"
ACT_EDGE = "#c2410c"
SEQ_HEAD = "#1d4ed8"
ACTOR = {
    "Заказчик": "#2563eb",
    "Менеджер": "#7c3aed",
    "Директор": "#b45309",
    "Технолог": "#0d9488",
    "Кладовщик": "#dc2626",
}


def _new(w=16.0, h=11.0, *, equal=False):
    fig, ax = plt.subplots(figsize=(w, h), dpi=240)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    if equal:
        ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    return fig, ax


def _save(fig, name: str) -> Path:
    path = FIG / name
    fig.savefig(path, bbox_inches="tight", facecolor="white", edgecolor="none", pad_inches=0.25)
    plt.close(fig)
    return path


def _title(ax, text: str, y=96.5):
    ax.text(50, y, text, ha="center", va="top", fontsize=16, fontweight="bold", color=TITLE, zorder=20)
    ax.plot([12, 88], [y - 3.2, y - 3.2], color="#cbd5e1", lw=1.0, zorder=1)


def _arrow(ax, x1, y1, x2, y2, *, color=LINE, lw=1.8, style="-|>", ls="-", ms=14, z=5):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
            linestyle=ls, shrinkA=0, shrinkB=0, zorder=z,
        )
    )


def _line(ax, pts, *, color=LINE, lw=1.8, z=4):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z)


def _actor(ax, x, y, name: str, color: str):
    """Крупная цветная фигурка актёра."""
    r = 1.55
    ax.add_patch(Circle((x, y + 8.4), r, fill=True, facecolor=color, edgecolor=color, lw=0, zorder=6, alpha=0.95))
    ax.plot([x, x], [y + 8.4 - r, y + 3.2], color=color, lw=2.4, zorder=6, solid_capstyle="round")
    ax.plot([x - 2.6, x + 2.6], [y + 6.2, y + 6.2], color=color, lw=2.4, zorder=6, solid_capstyle="round")
    ax.plot([x, x - 2.1], [y + 3.2, y + 0.3], color=color, lw=2.4, zorder=6, solid_capstyle="round")
    ax.plot([x, x + 2.1], [y + 3.2, y + 0.3], color=color, lw=2.4, zorder=6, solid_capstyle="round")
    ax.text(x, y - 1.8, name, ha="center", va="top", fontsize=11, fontweight="bold", color=color, zorder=7)


def _uc(ax, x, y, text: str, *, w=18.5, h=6.4):
    e = Ellipse((x, y), w, h, facecolor=UC_FILL, edgecolor=UC_EDGE, lw=2.0, zorder=5)
    ax.add_patch(e)
    ax.text(x, y, text, ha="center", va="center", fontsize=10, color=TITLE, zorder=6, fontweight="medium", linespacing=1.2)
    return {"x": x, "y": y, "w": w, "h": h}


def _uc_side(u, side: str):
    x, y, w, h = u["x"], u["y"], u["w"], u["h"]
    return {
        "l": (x - w / 2, y),
        "r": (x + w / 2, y),
        "t": (x, y + h / 2),
        "b": (x, y - h / 2),
    }[side]


def fig_use_case() -> Path:
    fig, ax = _new(17.5, 12.5, equal=True)
    _title(ax, "Диаграмма вариантов использования АИС «МебельПро»")

    ax.add_patch(FancyBboxPatch(
        (26, 10), 48, 76,
        boxstyle="round,pad=0.35,rounding_size=1.4",
        facecolor="#f8fafc", edgecolor="#334155", lw=2.4, zorder=1,
    ))
    ax.text(50, 83.2, "АИС «МебельПро»", ha="center", va="center",
            fontsize=14, fontweight="bold", color=TITLE, zorder=2)

    actors = {
        "Заказчик": (8, 72),
        "Менеджер": (8, 46),
        "Директор": (8, 20),
        "Технолог": (92, 62),
        "Кладовщик": (92, 24),
    }
    for name, (x, y) in actors.items():
        _actor(ax, x, y, name, ACTOR[name])

    # Левая колонка — офис; правая — производство/склад. Без лишних пересечений.
    u_app = _uc(ax, 40, 70, "Оформить заявку", w=19, h=6.6)
    u_agr = _uc(ax, 62, 70, "Согласовать смету", w=19, h=6.6)
    u_calc = _uc(ax, 62, 56, "Рассчитать смету", w=18, h=6.0)
    u_st = _uc(ax, 40, 56, "Просмотреть\nстатус заказа", w=19, h=6.6)
    u_ord = _uc(ax, 40, 40, "Вести заказы\nи договоры", w=19, h=6.6)
    u_rep = _uc(ax, 40, 24, "Просматривать\nотчёты", w=19, h=6.6)
    u_sp = _uc(ax, 66, 40, "Формировать\nспецификацию", w=18.5, h=6.6)
    u_job = _uc(ax, 66, 25, "Запускать\nпроизводственное\nзадание", w=19.5, h=7.4)
    u_res = _uc(ax, 66, 12, "Резервировать\nматериалы", w=18.5, h=6.2)
    u_out = _uc(ax, 40, 12, "Отпускать\nматериалы в цех", w=19, h=6.2)

    def attach(actor, uc, *, port="l", ay=None):
        """Прямая короткая связь актёр → порт прецедента (минимум изломов)."""
        col = ACTOR[actor]
        ax_x, ax_y = actors[actor]
        ty = uc["y"] if ay is None else ay
        if port == "l":
            p0 = (ax_x + 3.6, ax_y + 4.6)
            target = (_uc_side(uc, "l")[0], ty)
        else:
            p0 = (ax_x - 3.6, ax_y + 4.6)
            target = (_uc_side(uc, "r")[0], ty)
        _line(ax, [p0, target], color=col, lw=2.2)
        ax.add_patch(Circle(target, 0.42, facecolor=col, edgecolor=col, zorder=8))

    # Заказчик — верхние точки входа
    attach("Заказчик", u_app, ay=u_app["y"] + 1.4)
    attach("Заказчик", u_agr, ay=u_agr["y"] + 1.4)
    attach("Заказчик", u_st, ay=u_st["y"] + 1.4)
    # Менеджер — нижние точки тех же прецедентов + свои
    attach("Менеджер", u_app, ay=u_app["y"] - 1.4)
    attach("Менеджер", u_agr, ay=u_agr["y"] - 1.4)
    attach("Менеджер", u_st, ay=u_st["y"] - 1.4)
    attach("Менеджер", u_ord)
    attach("Менеджер", u_rep, ay=u_rep["y"] + 1.1)
    attach("Директор", u_rep, ay=u_rep["y"] - 1.1)
    attach("Технолог", u_sp, port="r")
    attach("Технолог", u_job, port="r")
    attach("Кладовщик", u_res, port="r")
    attach("Кладовщик", u_out, port="r")

    # UML include: согласование сметы всегда включает её расчёт
    _arrow(ax, 62, 66.5, 62, 59.2, color="#7c3aed", lw=2.0, ls="--", ms=14)
    ax.text(
        72.5, 63.0, "«включает»",
        ha="center", va="center", fontsize=9, color="#6d28d9", fontweight="bold", zorder=10,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#7c3aed", lw=1.2),
    )

    lx, ly = 26, 4.0
    ax.text(lx, ly + 2.4, "Цвет связи = роль актёра; пунктир «включает» — обязательное включение",
            fontsize=9, color=MUTED, ha="left")
    cx = lx
    for name, col in ACTOR.items():
        ax.add_patch(Circle((cx, ly), 0.75, facecolor=col, edgecolor=col, zorder=8))
        ax.text(cx + 1.2, ly, name, fontsize=9, va="center", color=col, fontweight="bold")
        cx += 13.8

    return _save(fig, "01_use_case.png")


def _class(ax, x, y_bottom, w, name, attrs, methods):
    """Класс UML: низ блока сразу под последней строкой."""
    head = 3.2
    row = 1.22
    gap = 0.22  # отступ от разделителя до первой/после последней строки
    attr_h = gap + len(attrs) * row + gap
    meth_h = gap + len(methods) * row + gap
    h = head + attr_h + meth_h
    y = y_bottom

    ax.add_patch(Rectangle((x, y), w, h, facecolor=CLS_FILL, edgecolor=CLS_EDGE, lw=1.7, zorder=5))
    ax.add_patch(Rectangle((x, y + h - head), w, head, facecolor=CLS_HEAD, edgecolor=CLS_EDGE, lw=0, zorder=6))
    ax.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y], color=CLS_EDGE, lw=1.7, zorder=6)
    ax.text(x + w / 2, y + h - head / 2, name, ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="white", zorder=7)

    y_div1 = y + h - head
    y_div2 = y_div1 - attr_h
    ax.plot([x, x + w], [y_div1, y_div1], color=CLS_EDGE, lw=1.2, zorder=6)
    ax.plot([x, x + w], [y_div2, y_div2], color=CLS_EDGE, lw=1.2, zorder=6)

    ay = y_div1 - gap
    for a in attrs:
        ax.text(x + 0.5, ay - 0.05, a, ha="left", va="top", fontsize=7.8, color=INK,
                family="DejaVu Sans Mono", zorder=7)
        ay -= row
    my = y_div2 - gap
    for m in methods:
        ax.text(x + 0.5, my - 0.05, m, ha="left", va="top", fontsize=7.8, color=INK,
                family="DejaVu Sans Mono", zorder=7)
        my -= row
    return {"x": x, "y": y, "w": w, "h": h, "cx": x + w / 2, "cy": y + h / 2}


def _side(b, s):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {
        "l": (x, y + h / 2),
        "r": (x + w, y + h / 2),
        "t": (x + w / 2, y + h),
        "b": (x + w / 2, y),
    }[s]


def _diamond_at(ax, x, y, *, toward="r"):
    s = 1.55
    if toward == "r":
        pts = [(x, y), (x + s, y + 0.85), (x + 2 * s, y), (x + s, y - 0.85)]
    else:
        pts = [(x, y), (x - s, y + 0.85), (x - 2 * s, y), (x - s, y - 0.85)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=CLS_EDGE, edgecolor=CLS_EDGE, zorder=8))


def _lab(ax, x, y, text, *, color="#166534", size=8.5):
    """Подпись на белом фоне — не перекрывается линией."""
    ax.text(
        x, y, text, ha="center", va="center", fontsize=size, color=color, fontweight="medium", zorder=12,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.96),
    )


def fig_classes() -> Path:
    fig, ax = _new(17.5, 11.5)
    _title(ax, "Диаграмма классов АИС «МебельПро»")

    # верхний ряд выровнен по низу шапок через одинаковый y_bottom с запасом
    c_cli = _class(ax, 1.5, 72, 17.5, "Клиент",
                   ["− id: int", "− наименование: string", "− телефон: string"],
                   ["+ оформитьЗаявку()"])
    c_ord = _class(ax, 26, 68, 19.5, "Заказ",
                   ["− номер: string", "− дата: date", "− статус: enum", "− сумма: money"],
                   ["+ рассчитатьСмету()", "+ сменитьСтатус()"])
    c_spc = _class(ax, 53, 74, 17.5, "Спецификация",
                   ["− id: int", "− версия: int"],
                   ["+ добавитьПозицию()"])
    c_itm = _class(ax, 78.5, 70, 18.5, "ПозицияСпецификации",
                   ["− изделие: string", "− кол-во: int", "− цена: money"],
                   ["+ пересчитать()"])

    c_shp = _class(ax, 1.5, 20, 17.5, "Отгрузка",
                   ["− дата: date", "− документ: string"],
                   ["+ оформить()"])
    c_tsk = _class(ax, 26, 16, 19.5, "ПроизводственноеЗадание",
                   ["− номер: string", "− участок: enum", "− срок: date"],
                   ["+ запустить()"])
    c_mat = _class(ax, 53, 14, 17.5, "Материал",
                   ["− артикул: string", "− название: string", "− едИзм: string", "− остаток: float"],
                   ["+ зарезервировать()"])
    c_usr = _class(ax, 78.5, 18, 18.5, "Пользователь",
                   ["− id: int", "− логин: string", "− роль: enum"],
                   ["+ войти()", "+ сменитьПароль()"])

    # Клиент — Заказ
    y_top = min(c_cli["y"] + c_cli["h"], c_ord["y"] + c_ord["h"]) - 1.8
    _line(ax, [(c_cli["x"] + c_cli["w"], y_top), (c_ord["x"], y_top)], color="#2563eb", lw=2.0)
    _lab(ax, 23, y_top + 2.4, "1  размещает  *", color="#2563eb", size=8.2)

    # Заказ ◆ Спецификация
    y2 = min(c_ord["y"] + c_ord["h"], c_spc["y"] + c_spc["h"]) - 1.8
    _diamond_at(ax, c_ord["x"] + c_ord["w"], y2, toward="r")
    _line(ax, [(c_ord["x"] + c_ord["w"] + 3.1, y2), (c_spc["x"], y2)], color=CLS_EDGE, lw=2.0)
    _lab(ax, 49.5, y2 + 2.4, "1    1", color=CLS_EDGE, size=8.2)

    # Спецификация ◆ Позиция
    y3 = min(c_spc["y"] + c_spc["h"], c_itm["y"] + c_itm["h"]) - 1.8
    _diamond_at(ax, c_spc["x"] + c_spc["w"], y3, toward="r")
    _line(ax, [(c_spc["x"] + c_spc["w"] + 3.1, y3), (c_itm["x"], y3)], color=CLS_EDGE, lw=2.0)
    _lab(ax, 74.5, y3 + 2.4, "1    *", color=CLS_EDGE, size=8.2)

    # Позиция → Материал: правый край canvas, без пересечений
    _line(ax, [
        _side(c_itm, "r"), (98.5, _side(c_itm, "r")[1]), (98.5, 40),
        (_side(c_mat, "t")[0], 40), _side(c_mat, "t"),
    ], color="#0d9488", lw=2.0)
    _lab(ax, 90, 43.2, "* ссылается 1", color="#0d9488", size=8.0)

    # Заказ → Задание (прямо вниз)
    _line(ax, [_side(c_ord, "b"), _side(c_tsk, "t")], color="#7c3aed", lw=2.0)
    _lab(ax, 41.5, (c_ord["y"] + c_tsk["y"] + c_tsk["h"]) / 2, "1 → 0..1", color="#7c3aed", size=8.2)

    # Заказ → Отгрузка: левый коридор x=20
    mid_y = (_side(c_ord, "l")[1] + _side(c_shp, "t")[1]) / 2
    _line(ax, [
        _side(c_ord, "l"), (20.5, _side(c_ord, "l")[1]), (20.5, _side(c_shp, "t")[1] + 1.5),
        (_side(c_shp, "t")[0], _side(c_shp, "t")[1] + 1.5), _side(c_shp, "t"),
    ], color="#b45309", lw=2.0)
    _lab(ax, 13.5, mid_y, "1 → 0..1", color="#b45309", size=8.2)

    # Пользователь → Заказ: коридор x=73, выше связи с материалом
    ob = _side(c_ord, "b")
    _line(ax, [
        _side(c_usr, "l"), (73, _side(c_usr, "l")[1]), (73, 54), (ob[0], 54), ob,
    ], color="#dc2626", lw=2.0)
    _lab(ax, 55, 56.5, "1  обрабатывает  *", color="#dc2626", size=8.2)

    ax.add_patch(FancyBboxPatch(
        (14, 2.5), 72, 4.0, boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor="#f1f5f9", edgecolor="#cbd5e1", lw=1.0, zorder=1,
    ))
    ax.text(50, 4.5, "◆ композиция: спецификация принадлежит заказу; позиции — спецификации",
            ha="center", va="center", fontsize=9.5, color=MUTED)

    return _save(fig, "02_classes.png")


def fig_sequence() -> Path:
    fig, ax = plt.subplots(figsize=(16.5, 15.0), dpi=240)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    # заголовок высоко; участники заметно ниже
    ax.text(50, 116, "Диаграмма последовательности: оформление заказа",
            ha="center", va="top", fontsize=16, fontweight="bold", color=TITLE, zorder=20)
    ax.plot([12, 88], [111.5, 111.5], color="#cbd5e1", lw=1.0, zorder=1)

    names = ["Менеджер", "ФормаЗаказа", "Заказ", "Спецификация"]
    xs = [12, 36, 60, 84]
    colors = ["#7c3aed", "#2563eb", "#15803d", "#c2410c"]
    head_y = 98
    life_top, life_bot = 96, 6

    for x, name, col in zip(xs, names, colors):
        ax.add_patch(FancyBboxPatch(
            (x - 8.5, head_y), 17, 5.5, boxstyle="round,pad=0.1,rounding_size=0.4",
            facecolor=col, edgecolor=col, lw=0, zorder=6,
        ))
        ax.text(x, head_y + 2.75, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white", zorder=7)
        ax.plot([x, x], [life_top, life_bot], color="#94a3b8", lw=1.5, ls=(0, (4, 4)), zorder=1)

    def actbar(x, y1, y2, col):
        ax.add_patch(Rectangle((x - 0.65, y2), 1.3, y1 - y2, facecolor=col, edgecolor=col, alpha=0.18, lw=0, zorder=2))
        ax.add_patch(Rectangle((x - 0.65, y2), 1.3, y1 - y2, fill=False, edgecolor=col, lw=1.2, zorder=3))

    actbar(xs[1], 90, 34, colors[1])
    actbar(xs[2], 80, 52, colors[2])
    actbar(xs[3], 72, 60, colors[3])

    def call(i, j, y, text, *, ret=False):
        x1, x2 = xs[i], xs[j]
        col = colors[j] if not ret else colors[i]
        ls = "--" if ret else "-"
        _arrow(ax, x1, y, x2, y, color=col, lw=1.8, ls=ls, ms=10)
        ax.text(
            (x1 + x2) / 2, y + 1.7, text,
            ha="center", va="bottom", fontsize=8.6, color=TITLE, zorder=12,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="#e2e8f0", lw=0.6),
        )

    call(0, 1, 88, "1: создатьЗаявку(клиент, размеры)")
    call(1, 2, 78, "2: new Заказ()")
    call(1, 3, 70, "3: рассчитатьСпецификацию()")
    call(3, 1, 62, "4: состав и смета", ret=True)
    call(1, 2, 52, "5: сохранить(смета, статус=«расчёт»)")
    call(1, 0, 42, "6: показать смету", ret=True)

    # alt: две ветки со стрелками (заливка прозрачная — lifeline видны)
    ax.add_patch(FancyBboxPatch(
        (3.5, 7), 93, 28, boxstyle="round,pad=0.1,rounding_size=0.3",
        facecolor="#fff7ed", edgecolor="#ea580c", lw=1.6, alpha=0.25, zorder=3,
    ))
    ax.add_patch(Rectangle((3.5, 31.5), 7.5, 3.5, facecolor="#ea580c", edgecolor="#ea580c", lw=0, zorder=4))
    ax.text(7.25, 33.25, "alt", ha="center", va="center", fontsize=10, fontweight="bold", color="white", zorder=5)

    ax.text(14, 30.5, "[отклоняет]", ha="left", fontsize=8.5, color="#9a3412", fontweight="bold", zorder=5)
    _arrow(ax, xs[0], 26, xs[1], 26, color="#dc2626", lw=1.6, ms=9)
    ax.text((xs[0] + xs[1]) / 2, 27.5, "7a: отклонитьСмету()", ha="center", fontsize=8.2, color="#991b1b",
            zorder=12, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
    _arrow(ax, xs[1], 21, xs[2], 21, color="#dc2626", lw=1.6, ms=9)
    ax.text((xs[1] + xs[2]) / 2, 22.5, "8a: статус = «отменён»", ha="center", fontsize=8.2, color="#991b1b",
            zorder=12, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))

    ax.plot([3.5, 96.5], [17, 17], color="#ea580c", lw=1.0, ls="--", zorder=4)
    ax.text(14, 15.2, "[подтверждает]", ha="left", fontsize=8.5, color="#166534", fontweight="bold", zorder=5)
    _arrow(ax, xs[0], 11, xs[1], 11, color="#15803d", lw=1.6, ms=9)
    ax.text((xs[0] + xs[1]) / 2, 12.5, "7b: подтвердитьСмету()", ha="center", fontsize=8.2, color="#166534",
            zorder=12, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
    _arrow(ax, xs[1], 11, xs[2], 11, color="#15803d", lw=1.6, ls="--", ms=9)
    ax.text((xs[1] + xs[2]) / 2, 9.2, "далее — договор / состояния", ha="center", fontsize=7.8, color="#166534",
            zorder=12, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))

    return _save(fig, "03_sequence.png")


def fig_states() -> Path:
    fig, ax = _new(17.5, 12.5)
    _title(ax, "Диаграмма состояний объекта «Заказ»")

    def state(x, y, name, w=13.0, h=5.8):
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.2,rounding_size=1.1",
            facecolor=ST_FILL, edgecolor=ST_EDGE, lw=1.9, zorder=5,
        ))
        ax.text(x, y, name, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#14532d", zorder=6)
        return x, y, w, h

    def R(s): return s[0] + s[2] / 2, s[1]
    def L(s): return s[0] - s[2] / 2, s[1]
    def T(s): return s[0], s[1] + s[3] / 2
    def B(s): return s[0], s[1] - s[3] / 2

    def go(p1, p2, label, *, lo=(0, 2.6), col=ST_EDGE):
        _arrow(ax, p1[0], p1[1], p2[0], p2[1], color=col, lw=1.8, ms=10)
        _lab(ax, (p1[0] + p2[0]) / 2 + lo[0], (p1[1] + p2[1]) / 2 + lo[1], label, color=col, size=7.8)

    ax.add_patch(Circle((4.5, 90), 1.4, facecolor=INK, zorder=6))
    ax.add_patch(Circle((4.5, 8), 1.7, fill=False, lw=1.9, edgecolor=INK, zorder=6))
    ax.add_patch(Circle((4.5, 8), 1.0, facecolor=INK, zorder=7))

    # верх: Новый → Расчёт → Согласован → В пр-ве
    n = state(16, 90, "Новый")
    c = state(38, 90, "Расчёт")
    o = state(60, 90, "Согласован")
    p = state(86, 90, "В производстве", w=14.5)
    # середина: отмена слева; контроль справа
    x = state(16, 58, "Отменён", w=12)
    q = state(86, 58, "На контроле", w=14.5)
    # низ: Готов ← Отгружен ← Закрыт
    g = state(86, 28, "Готов")
    s = state(52, 28, "Отгружен")
    z = state(18, 8, "Закрыт")

    _arrow(ax, 6.0, 90, L(n)[0], 90, color=ST_EDGE, lw=1.8)
    _lab(ax, 9.5, 92.4, "создать()", color=ST_EDGE, size=7.8)

    go(R(n), L(c), "рассчитатьСмету()")
    go(R(c), L(o), "заказчик подтвердил")
    go(R(o), L(p), "запуститьВЦех()")

    # расчёт → отменён (прямо вниз)
    _line(ax, [B(c), (38, T(x)[1] + 4)], color="#dc2626", lw=1.8)
    _line(ax, [(38, T(x)[1] + 4), (16, T(x)[1] + 4)], color="#dc2626", lw=1.8)
    _arrow(ax, 16, T(x)[1] + 4, 16, T(x)[1], color="#dc2626", lw=1.8)
    _lab(ax, 28, T(x)[1] + 5.5, "отклонена смета", color="#dc2626", size=7.8)

    # согласован → отменён (коридор y=74)
    _line(ax, [B(o), (60, 74), (16, 74)], color="#dc2626", lw=1.8)
    _arrow(ax, 16, 74, 16, T(x)[1], color="#dc2626", lw=1.8)
    _lab(ax, 40, 76.2, "отмена договора", color="#dc2626", size=7.8)

    go(B(p), T(q), "сдатьНаОТК()", lo=(4.0, 0))

    # возврат: слева от контроля вверх, вход снизу в «В производстве»
    _line(ax, [L(q), (74, 58), (74, B(p)[1] - 1.2), (B(p)[0], B(p)[1] - 1.2)], color="#c2410c", lw=1.8)
    _arrow(ax, B(p)[0], B(p)[1] - 1.2, B(p)[0], B(p)[1], color="#c2410c", lw=1.8)
    _lab(ax, 68, 72, "возврат в цех", color="#c2410c", size=7.8)

    go(B(q), T(g), "ОТК: годен", lo=(4.0, 0))
    go(L(g), R(s), "оформитьОтгрузку()")

    _line(ax, [B(s), (52, 8), (R(z)[0], 8)], color=ST_EDGE, lw=1.8)
    _arrow(ax, R(z)[0] + 0.1, 8, R(z)[0], 8, color=ST_EDGE, lw=1.8)
    _lab(ax, 38, 11, "получить оплату", color=ST_EDGE, size=7.8)

    _arrow(ax, L(z)[0], 8, 6.3, 8, color=ST_EDGE, lw=1.8)
    _lab(ax, 11, 5.2, "архивировать()", color=ST_EDGE, size=7.8)

    return _save(fig, "04_states.png")


def fig_activity() -> Path:
    fig, ax = plt.subplots(figsize=(12.5, 14.5), dpi=240)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    _title(ax, "Диаграмма деятельности: отчёт об остатках материалов", y=136)

    def action(x, y, text, w=48, h=10):
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.3,rounding_size=1.0",
            facecolor=ACT_FILL, edgecolor=ACT_EDGE, lw=2.0, zorder=5,
        ))
        ax.text(x, y, text, ha="center", va="center", fontsize=11, color="#7c2d12",
                fontweight="medium", zorder=6, linespacing=1.25)
        return x, y

    def diamond(x, y, text, s=9):
        pts = [(x, y + s), (x + s, y), (x, y - s), (x - s, y)]
        ax.add_patch(Polygon(pts, closed=True, facecolor="#fefce8", edgecolor="#ca8a04", lw=2.0, zorder=5))
        ax.text(x, y, text, ha="center", va="center", fontsize=10, color="#854d0e", fontweight="bold", zorder=6)
        return x, y

    ax.add_patch(Circle((50, 128), 2.0, facecolor=INK, zorder=6))
    ax.add_patch(Circle((50, 8), 2.3, fill=False, lw=2.0, edgecolor=INK, zorder=6))
    ax.add_patch(Circle((50, 8), 1.3, facecolor=INK, zorder=7))

    action(50, 116, "Пользователь выбирает\n«Отчёт об остатках»")
    action(50, 98, "Система запрашивает\nсклад и период")
    action(50, 80, "Пользователь задаёт фильтры\nи нажимает «Сформировать»")
    diamond(50, 60, "данные\nкорректны?")
    action(18, 60, "Показать сообщение\nоб ошибке ввода", w=30, h=11)
    action(50, 38, "Построить выборку остатков\nпо регистру материалов")
    action(50, 20, "Вывести отчёт на экран\nи предложить печать / файл")

    _arrow(ax, 50, 125.8, 50, 121.2, color=ACT_EDGE, lw=2.0)
    _arrow(ax, 50, 110.8, 50, 103.2, color=ACT_EDGE, lw=2.0)
    _arrow(ax, 50, 92.8, 50, 85.2, color=ACT_EDGE, lw=2.0)
    _arrow(ax, 50, 74.8, 50, 69.2, color=ACT_EDGE, lw=2.0)
    _arrow(ax, 50, 51.0, 50, 43.2, color="#15803d", lw=2.0)
    ax.text(54.5, 47.5, "да", fontsize=11, color="#15803d", fontweight="bold")
    _arrow(ax, 50, 32.8, 50, 25.2, color=ACT_EDGE, lw=2.0)
    _arrow(ax, 50, 14.8, 50, 10.5, color=ACT_EDGE, lw=2.0)

    _arrow(ax, 41, 60, 33, 60, color="#dc2626", lw=2.0)
    ax.text(37, 63.2, "нет", fontsize=11, color="#dc2626", fontweight="bold")
    _line(ax, [(18, 65.5), (18, 98)], color="#dc2626", lw=2.0)
    _arrow(ax, 18, 98, 26, 98, color="#dc2626", lw=2.0)

    return _save(fig, "05_activity.png")


def write_report(figs: list[Path]) -> Path:
    doc = make_document()
    add_title_page(doc, 3, "Изучение методологии структурного моделирования UML")

    add_heading_gost(doc, "1 Цель работы")
    add_text(
        doc,
        "Целью лабораторной работы является изучение методологии структурного моделирования UML "
        "и построение набора взаимосвязанных UML-спецификаций, раскрывающих структурные и "
        "поведенческие особенности автоматизированной информационной системы «МебельПро».",
    )

    add_heading_gost(doc, "2 Задание", new_page=True)
    add_text(doc, "Согласно методическим указаниям необходимо:")
    add_text(
        doc,
        "1) изучить основные положения языка UML (сущности, отношения, виды диаграмм, "
        "принципы абстрагирования, многомодельности и иерархического построения);",
    )
    add_text(
        doc,
        "2) выбрать один из форматов отчёта: реферат (не менее 10 страниц и 4 вида моделей) "
        "либо сквозной авторский пример моделирования информационной системы;",
    )
    add_text(
        doc,
        "3) при выборе авторского примера — кратко описать информационную систему (1–2 абзаца) "
        "и представить не менее пяти нотаций UML, раскрывающих её структурные особенности;",
    )
    add_text(doc, "4) оформить отчёт с титульным листом и разместить в LMS.")
    add_text(
        doc,
        "В настоящей работе выбран второй формат — сквозной авторский пример. "
        "Инструмент построения диаграмм — Python (matplotlib), оформление соответствует "
        "стандартной нотации UML.",
    )

    add_heading_gost(doc, "3 Описание информационной системы", new_page=True)
    add_text(
        doc,
        "Автоматизированная информационная система «МебельПро» предназначена для учёта заказов "
        "и сопровождения производства корпусной мебели на заказ. Основные возможности: учёт "
        "клиентов и заявок, расчёт спецификации и сметы, резервирование и отпуск материалов, "
        "запуск производственных заданий, контроль статусов заказа, отгрузка и формирование "
        "отчётов об остатках.",
    )
    add_text(
        doc,
        "Предметная область согласована с лабораторными работами №1 и №2 того же курса. "
        "Ниже приведены пять UML-нотаций: диаграмма вариантов использования, диаграмма классов, "
        "диаграмма последовательности, диаграмма состояний объекта «Заказ» и диаграмма "
        "деятельности формирования отчёта об остатках.",
    )

    add_heading_gost(doc, "4 Диаграмма вариантов использования", new_page=True)
    add_text(
        doc,
        "Диаграмма задаёт границы системы и роли пользователей. Актёры: заказчик, менеджер, "
        "директор, технолог и кладовщик. Заказчик оформляет заявку, согласовывает смету и "
        "просматривает статус заказа. Менеджер выполняет те же действия по работе с заказом, "
        "а также ведёт договоры и просматривает отчёты. Директор получает отчёты. Технолог "
        "формирует спецификацию и запускает производственное задание. Кладовщик резервирует "
        "и отпускает материалы в цех. Пунктирная связь «включает» показывает, что согласование "
        "сметы обязательно включает её расчёт. Цвет связи совпадает с цветом актёра.",
    )
    add_picture(doc, figs[0], 16.5)
    add_caption(doc, "Рисунок 1 – UML-диаграмма вариантов использования")

    add_heading_gost(doc, "5 Диаграмма классов", new_page=True)
    add_text(
        doc,
        "Диаграмма классов отражает структуру предметных сущностей АИС. Клиент размещает "
        "множество заказов. Заказ композиционно включает спецификацию; спецификация — набор "
        "позиций. Позиция ссылается на материал со склада. У заказа могут быть производственное "
        "задание и отгрузка. Пользователь системы обрабатывает заказы в соответствии с ролью. "
        "Композиция обозначена заполненным ромбом со стороны целого.",
    )
    add_picture(doc, figs[1], 16.5)
    add_caption(doc, "Рисунок 2 – UML-диаграмма классов")

    add_heading_gost(doc, "6 Диаграмма последовательности", new_page=True)
    add_text(
        doc,
        "Диаграмма описывает сценарий оформления заказа менеджером. Участники: менеджер, "
        "форма заказа, объект «Заказ» и объект «Спецификация». Менеджер создаёт заявку; форма "
        "порождает заказ, запрашивает расчёт спецификации, сохраняет смету со статусом «расчёт» "
        "и показывает результат на согласование. Во фрагменте alt зафиксирована альтернатива: "
        "при отклонении сметы заказчиком статус становится «отменён», новый расчёт не сохраняется.",
    )
    add_picture(doc, figs[2], 16.5)
    add_caption(doc, "Рисунок 3 – UML-диаграмма последовательности «Оформление заказа»")

    add_heading_gost(doc, "7 Диаграмма состояний объекта «Заказ»", new_page=True)
    add_text(
        doc,
        "Диаграмма состояний показывает жизненный цикл заказа: новый → расчёт → согласован → "
        "в производстве → на контроле → готов → отгружен → закрыт. Из состояний «расчёт» и "
        "«согласован» возможен переход в «отменён». С контроля при выявлении дефекта заказ "
        "возвращается в производство — это соответствует обратной связи ОТК в модели IDEF0 "
        "лабораторной работы №2. Завершение жизненного цикла — архивирование закрытого заказа.",
    )
    add_picture(doc, figs[3], 16.5)
    add_caption(doc, "Рисунок 4 – UML-диаграмма состояний объекта «Заказ»")

    add_heading_gost(doc, "8 Диаграмма деятельности", new_page=True)
    add_text(
        doc,
        "Диаграмма деятельности описывает алгоритм формирования отчёта об остатках материалов "
        "(право менеджера и директора). Пользователь выбирает отчёт, система запрашивает склад "
        "и период, пользователь задаёт фильтры. При некорректных данных выводится сообщение "
        "об ошибке и выполняется возврат к вводу параметров. При успешной проверке строится "
        "выборка по регистру материалов, отчёт выводится на экран с возможностью печати "
        "или сохранения в файл.",
    )
    add_picture(doc, figs[4], 14.8)
    add_caption(doc, "Рисунок 5 – UML-диаграмма деятельности формирования отчёта об остатках")

    add_heading_gost(doc, "Заключение", new_page=True)
    add_text(
        doc,
        "В результате работы изучена методология UML и построен сквозной авторский пример "
        "моделирования АИС «МебельПро». Пятью нотациями описаны роли и прецеденты, структура "
        "классов, сценарий оформления заказа, жизненный цикл заказа и алгоритм отчёта "
        "об остатках. Набор соответствует требованию методички (достаточно пяти нотаций) "
        "и согласован с моделями лабораторных работ №1 и №2.",
    )

    out = LAB / "Отчет_ЛР3_UML_Лаврешин.docx"
    try:
        doc.save(out)
    except PermissionError:
        out = LAB / "Отчет_ЛР3_UML_Лаврешин_new.docx"
        doc.save(out)
    return out


def write_explanation():
    (LAB / "ОБЪЯСНЕНИЕ.md").write_text(
        """# ЛР3 — UML АИС «МебельПро»

Сквозной авторский пример (5 нотаций). Диаграммы цветные, с крупными подписями.

| № | Диаграмма | Файл |
|---|---|---|
| 1 | Вариантов использования | `figures/01_use_case.png` |
| 2 | Классов | `figures/02_classes.png` |
| 3 | Последовательности | `figures/03_sequence.png` |
| 4 | Состояний «Заказ» | `figures/04_states.png` |
| 5 | Деятельности | `figures/05_activity.png` |

Отчёт: `Отчет_ЛР3_UML_Лаврешин.docx`  
Пересборка: `python tools/lab3_build.py`
""",
        encoding="utf-8",
    )


def main():
    figs = [fig_use_case(), fig_classes(), fig_sequence(), fig_states(), fig_activity()]
    rep = write_report(figs)
    write_explanation()
    print("DOC", rep)
    for f in figs:
        print(f)


if __name__ == "__main__":
    main()
