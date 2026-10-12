# -*- coding: utf-8 -*-
"""Схема бизнес-процесса и диаграмма вариантов использования для ИСУП."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent
BORDER = (40, 60, 100)
HEADER_BG = (214, 228, 247)
EVENT_BG = (255, 248, 220)
UC_BG = (232, 245, 233)
SYS_BG = (248, 250, 252)
TEXT = (20, 30, 45)
ARROW = (70, 90, 120)
DASH = (120, 120, 140)


def font(size: int, bold: bool = False):
    names = [
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def box(draw, xy, fill, outline=BORDER, w=2, r=10):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


def text_in(draw, xy, text, fnt, fill=TEXT):
    x0, y0, x1, y1 = xy
    lines = wrap(draw, text, fnt, x1 - x0 - 16)
    lh = fnt.size + 3
    total = lh * len(lines)
    y = (y0 + y1 - total) // 2
    for line in lines:
        tw = draw.textlength(line, font=fnt)
        draw.text(((x0 + x1 - tw) / 2, y), line, font=fnt, fill=fill)
        y += lh


def arrow(draw, a, b, dashed=False):
    if dashed:
        # simple dashed line
        x0, y0 = a
        x1, y1 = b
        segs = 16
        for i in range(segs):
            if i % 2:
                continue
            t0, t1 = i / segs, (i + 1) / segs
            p0 = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0)
            p1 = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
            draw.line([p0, p1], fill=DASH, width=2)
        color = DASH
    else:
        draw.line([a, b], fill=ARROW, width=3)
        color = ARROW
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = 11
    for da in (2.5, -2.5):
        ax = b[0] - L * math.cos(ang + da)
        ay = b[1] - L * math.sin(ang + da)
        draw.line([b, (ax, ay)], fill=color, width=3)


def stick(draw, cx, cy, label, fnt):
    # head
    draw.ellipse((cx - 12, cy - 34, cx + 12, cy - 10), outline=BORDER, width=2)
    # body
    draw.line([(cx, cy - 10), (cx, cy + 18)], fill=BORDER, width=2)
    # arms
    draw.line([(cx - 18, cy), (cx + 18, cy)], fill=BORDER, width=2)
    # legs
    draw.line([(cx, cy + 18), (cx - 14, cy + 40)], fill=BORDER, width=2)
    draw.line([(cx, cy + 18), (cx + 14, cy + 40)], fill=BORDER, width=2)
    lines = wrap(draw, label, fnt, 130)
    y = cy + 48
    for line in lines:
        tw = draw.textlength(line, font=fnt)
        draw.text((cx - tw / 2, y), line, font=fnt, fill=TEXT)
        y += fnt.size + 2


def oval(draw, xy, text, fnt):
    draw.ellipse(xy, fill=UC_BG, outline=BORDER, width=2)
    text_in(draw, xy, text, fnt)


def make_process_scheme():
    W, H = 1600, 980
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    title_f = font(26, True)
    head_f = font(18, True)
    cell_f = font(16)
    note_f = font(15)

    d.text((40, 20), "Рисунок 1 — Схема бизнес-процесса учёта платежей", font=title_f, fill=TEXT)

    cols = [
        "Внешнее событие",
        "Бухгалтер\nпо расчётам",
        "Согласующий\nруководитель",
        "Казначей",
        "Финансист",
    ]
    x0, y0 = 40, 70
    col_w = 300
    row_h = 150
    header_h = 70
    n_rows = 5

    # grid
    for i, name in enumerate(cols):
        x = x0 + i * col_w
        box(d, (x, y0, x + col_w, y0 + header_h), HEADER_BG, r=0)
        text_in(d, (x, y0, x + col_w, y0 + header_h), name.replace("\n", " "), head_f)
        d.rectangle((x, y0 + header_h, x + col_w, y0 + header_h + n_rows * row_h), outline=BORDER, width=2)

    # vertical lines
    for i in range(len(cols) + 1):
        x = x0 + i * col_w
        d.line([(x, y0), (x, y0 + header_h + n_rows * row_h)], fill=BORDER, width=2)

    # horizontal lines
    for r in range(n_rows + 1):
        y = y0 + header_h + r * row_h
        d.line([(x0, y), (x0 + len(cols) * col_w, y)], fill=BORDER, width=1)

    def cell(col, row):
        x = x0 + col * col_w + 10
        y = y0 + header_h + row * row_h + 12
        return (x, y, x + col_w - 20, y + row_h - 24)

    # Row content: events and UCs
    events = [
        (0, "E1: поступил счёт /\nзаявка на оплату"),
        (1, "E2: требуется\nсогласование"),
        (2, "E4: наступила дата\nоплаты / реестр"),
        (3, "E6: поступила\nбанковская выписка"),
        (4, "E7: нужен отчёт\nДДС за период"),
    ]
    for row, text in events:
        box(d, cell(0, row), EVENT_BG, r=8)
        text_in(d, cell(0, row), text.replace("\n", " "), cell_f)

    ucs = [
        (1, 0, "UC-1: Зарегистрировать\nплатёж / заявку"),
        (2, 1, "UC-2: Согласовать\nплатёж"),
        (3, 2, "UC-3: Сформировать реестр\nи отправить в банк"),
        (1, 3, "UC-4: Сверить платежи\nс выпиской"),
        (4, 4, "UC-5: Сформировать\nотчёт ДДС"),
    ]
    for col, row, text in ucs:
        box(d, cell(col, row), UC_BG, r=8)
        text_in(d, cell(col, row), text.replace("\n", " "), cell_f)

    # arrows event -> UC
    def mid(col, row, side="c"):
        x1, y1, x2, y2 = cell(col, row)
        cy = (y1 + y2) / 2
        if side == "l":
            return (x1, cy)
        if side == "r":
            return (x2, cy)
        return ((x1 + x2) / 2, cy)

    arrow(d, mid(0, 0, "r"), mid(1, 0, "l"))
    arrow(d, mid(0, 1, "r"), mid(2, 1, "l"))
    arrow(d, mid(0, 2, "r"), mid(3, 2, "l"))
    arrow(d, mid(0, 3, "r"), mid(1, 3, "l"))
    arrow(d, mid(0, 4, "r"), mid(4, 4, "l"))

    # sequence UC-1 -> UC-2 -> UC-3 -> UC-4
    arrow(d, mid(1, 0, "r"), (mid(2, 1, "l")[0] - 8, mid(1, 0)[1]))
    # vertical-ish via centers
    c12 = ((mid(1, 0)[0] + mid(2, 1)[0]) / 2, mid(1, 0)[1])
    # simpler sequential arrows between UC boxes centers vertically-ish
    arrow(d, (mid(1, 0)[0], cell(1, 0)[3]), (mid(2, 1)[0], cell(2, 1)[1]))
    arrow(d, (mid(2, 1)[0], cell(2, 1)[3]), (mid(3, 2)[0], cell(3, 2)[1]))
    arrow(d, (mid(3, 2)[0], cell(3, 2)[3]), (mid(1, 3)[0], cell(1, 3)[1]))

    note = (
        "E3 — платёж отклонён согласующим, расширение UC-2. "
        "E5 — банк исполнил/отклонил платёж, входит в постусловия UC-3 / старт UC-4. "
        "Администратор на схему операционного цикла не вынесен."
    )
    for i, line in enumerate(wrap(d, note, note_f, W - 80)):
        d.text((40, y0 + header_h + n_rows * row_h + 16 + i * 22), line, font=note_f, fill=TEXT)

    out = ASSETS / "fig_process.png"
    img.save(out)
    print("saved", out)
    return out


def make_uc_diagram():
    W, H = 1500, 950
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    title_f = font(26, True)
    uc_f = font(15)
    act_f = font(15)
    sys_f = font(18, True)

    d.text((40, 18), "Рисунок 2 — Диаграмма вариантов использования", font=title_f, fill=TEXT)

    # system boundary
    sys = (320, 80, 1180, 860)
    box(d, sys, SYS_BG, w=3, r=6)
    d.text((340, 95), "ИС учёта платежей", font=sys_f, fill=TEXT)

    # use cases positions
    ucs = [
        ((480, 160, 760, 250), "UC-1: Зарегистрировать платёж / заявку"),
        ((760, 280, 1040, 370), "UC-2: Согласовать платёж"),
        ((480, 400, 760, 490), "UC-3: Сформировать реестр и отправить в банк"),
        ((760, 520, 1040, 610), "UC-4: Сверить платежи с выпиской"),
        ((480, 640, 760, 730), "UC-5: Сформировать отчёт ДДС"),
        ((760, 740, 1040, 830), "UC-6: Настроить справочники и роли"),
    ]
    for xy, name in ucs:
        oval(d, xy, name, uc_f)

    # actors
    actors = [
        (140, 220, "Бухгалтер\nпо расчётам"),
        (140, 430, "Казначей"),
        (140, 640, "Администратор"),
        (1360, 300, "Согласующий\nруководитель"),
        (1360, 520, "Финансист"),
        (1360, 700, "Главный бухгалтер\n(участник)"),
    ]
    for cx, cy, label in actors:
        stick(d, cx, cy, label.replace("\n", " "), act_f)

    def uc_edge(idx, side):
        x0, y0, x1, y1 = ucs[idx][0]
        cy = (y0 + y1) / 2
        return (x0, cy) if side == "l" else (x1, cy)

    # associations primary
    links = [
        ((140, 220), uc_edge(0, "l"), False),  # accountant -> UC1
        ((140, 220), uc_edge(3, "l"), False),  # accountant -> UC4
        ((140, 430), uc_edge(2, "l"), False),  # treasurer -> UC3
        ((140, 640), uc_edge(5, "l"), False),  # admin -> UC6
        ((1360, 300), uc_edge(1, "r"), False),  # approver -> UC2
        ((1360, 520), uc_edge(4, "r"), False),  # financier -> UC5
        ((1360, 700), uc_edge(3, "r"), True),  # chief accountant participant UC4
    ]
    for a, b, dashed in links:
        arrow(d, a, b, dashed=dashed)

    # label for dashed
    d.text((1050, 680), "участник", font=font(14), fill=DASH)

    out = ASSETS / "fig_usecase.png"
    img.save(out)
    print("saved", out)
    return out


def main():
    make_process_scheme()
    make_uc_diagram()


if __name__ == "__main__":
    main()
