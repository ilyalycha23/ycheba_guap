# -*- coding: utf-8 -*-
"""Контекстная диаграмма ИС учета платежей."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).with_name("fig_context.png")
W, H = 1400, 900
BG = (255, 255, 255)
BOX = (232, 240, 254)
CENTER = (208, 226, 248)
BORDER = (47, 84, 150)
TEXT = (20, 30, 50)
ARROW = (70, 90, 120)


def font(size: int):
    for name in (
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\timesbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded(draw, xy, fill, outline, width=2, radius=14):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, box, lines, fnt, fill=TEXT):
    x0, y0, x1, y1 = box
    line_h = fnt.size + 4
    total = line_h * len(lines)
    y = (y0 + y1 - total) // 2
    for line in lines:
        tw = draw.textlength(line, font=fnt)
        draw.text(((x0 + x1 - tw) / 2, y), line, font=fnt, fill=fill)
        y += line_h


def arrow(draw, start, end):
    draw.line([start, end], fill=ARROW, width=3)
    x1, y1 = end
    x0, y0 = start
    import math

    ang = math.atan2(y1 - y0, x1 - x0)
    L = 12
    for da in (2.5, -2.5):
        ax = x1 - L * math.cos(ang + da)
        ay = y1 - L * math.sin(ang + da)
        draw.line([(x1, y1), (ax, ay)], fill=ARROW, width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title_f = font(28)
    box_f = font(20)
    small_f = font(16)

    d.text((40, 24), "Рисунок — контекстная диаграмма ИС «Учет платежей»", font=title_f, fill=TEXT)

    center = (520, 220, 880, 420)
    rounded(d, center, CENTER, BORDER, width=3, radius=18)
    center_text(d, center, ["ИС учета платежей", "(Payment Accounting IS)"], box_f)

    actors = [
        ((80, 160, 320, 280), ["Бухгалтер /", "операционист"]),
        ((80, 460, 320, 580), ["Руководитель /", "финансист"]),
        ((1080, 120, 1320, 240), ["Плательщик /", "контрагент"]),
        ((1080, 300, 1320, 420), ["Банк /", "платежный шлюз"]),
        ((1080, 500, 1320, 620), ["Бухгалтерская", "система (1С)"]),
        ((520, 560, 880, 680), ["Администратор", "системы"]),
    ]
    for box, lines in actors:
        rounded(d, box, BOX, BORDER, width=2)
        center_text(d, box, lines, box_f)

    # arrows to/from center
    links = [
        ((320, 220), (520, 280), "ввод платежей"),
        ((320, 500), (520, 360), "отчеты, контроль"),
        ((880, 280), (1080, 180), "статус оплаты"),
        ((880, 320), (1080, 360), "проведение платежей"),
        ((880, 380), (1080, 540), "выгрузка проводок"),
        ((700, 420), (700, 560), "настройка, роли"),
    ]
    for a, b, label in links:
        arrow(d, a, b)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 14
        tw = d.textlength(label, font=small_f)
        d.text((mx - tw / 2, my), label, font=small_f, fill=ARROW)

    note = (
        "Пользователи работают через веб-браузер. Система хранит реестр платежей, "
        "счетов, контрагентов и формирует отчеты."
    )
    d.text((60, 760), note, font=small_f, fill=TEXT)
    img.save(OUT, "PNG")
    print("saved", OUT)


if __name__ == "__main__":
    main()
