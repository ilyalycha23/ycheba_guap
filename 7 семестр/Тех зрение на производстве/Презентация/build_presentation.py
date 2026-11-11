# -*- coding: utf-8 -*-
"""Тема 7 — финальная презентация: уникальные слайды, корректные рамки, 16:9."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Inches, Pt

ROOT = Path(__file__).resolve().parent
SL = ROOT / "assets" / "slides"
OUT = ROOT / "Тема7_Разметка_и_датасет_СТЗ.pptx"
OUT_ALT = ROOT / "Тема7_Разметка_и_датасет_СТЗ_FINAL.pptx"

BG = RGBColor(0x0B, 0x0C, 0x0F)
INK = RGBColor(0xF7, 0xF8, 0xFA)
DIM = RGBColor(0xA8, 0xAE, 0xBA)
ACC = RGBColor(0x5C, 0xF2, 0xC8)
WARN = RGBColor(0xFF, 0x6B, 0x5A)
FH, FB = "Bahnschrift", "Segoe UI"


def R(p, text, size=18, bold=False, color=INK, font=FB):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font


def fill(sh, c):
    sh.fill.solid()
    sh.fill.fore_color.rgb = c
    sh.line.fill.background()


def rect(slide, l, t, w, h, c):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    fill(sh, c)
    return sh


def roundr(slide, l, t, w, h, c):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    try:
        sh.adjustments[0] = 0.08
    except Exception:
        pass
    fill(sh, c)
    return sh


def tb(slide, l, t, w, h):
    return slide.shapes.add_textbox(l, t, w, h).text_frame


def notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    tf.clear()
    R(tf.paragraphs[0], text, size=11)


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    W, H = prs.slide_width, prs.slide_height
    slides = []

    def bleed(name):
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(str(SL / name), 0, 0, width=W, height=H)
        slides.append(s)
        return s

    def line(s, y, color=ACC):
        rect(s, Cm(1.5), y, Cm(1.2), Cm(0.1), color)

    def caption(s, title, sub=None, y=None, color_line=ACC):
        if y is None:
            y = H - Cm(5.2)
        line(s, y, color_line)
        tf = tb(s, Cm(1.5), y + Cm(0.35), Cm(28), Cm(4.2))
        tf.word_wrap = True
        R(tf.paragraphs[0], title, size=28, bold=True, color=INK, font=FH)
        if sub:
            p = tf.add_paragraph()
            p.space_before = Pt(10)
            R(p, sub, size=15, color=DIM)

    def pagenum(s, i, n):
        tf = tb(s, W - Cm(2.2), H - Cm(0.65), Cm(1.8), Cm(0.4))
        tf.paragraphs[0].alignment = PP_ALIGN.RIGHT
        R(tf.paragraphs[0], f"{i}/{n}", size=10, color=DIM)

    # 1 Hook
    s = bleed("01_hook.jpg")
    caption(
        s,
        "Представьте учебник с ошибочными ответами",
        "Плохая разметка для нейросети — это ровно такая же «истина»",
    )
    notes(s, "Хук")

    # 2 Title — clean, no overlap
    s = bleed("02_title.jpg")
    # solid caption panel so text never fights the photo
    rect(s, 0, H - Cm(4.8), W, Cm(4.8), BG)
    line(s, H - Cm(4.3))
    tf = tb(s, Cm(1.5), H - Cm(4.0), Cm(8), Cm(0.5))
    R(tf.paragraphs[0], "ТЕМА 07", size=13, bold=True, color=ACC, font=FH)
    tf = tb(s, Cm(1.5), H - Cm(3.3), Cm(29), Cm(2.8))
    tf.word_wrap = True
    R(tf.paragraphs[0], "Разметка данных и сбор датасета\nдля производственной СТЗ", size=28, bold=True, color=INK, font=FH)
    tf = tb(s, Cm(1.5), H - Cm(1.0), Cm(29), Cm(0.6))
    R(tf.paragraphs[0], "Ground truth · bbox / mask · YOLO · leakage · split по роликам", size=13, color=DIM)
    notes(s, "Титул")

    # 3 Ground truth
    s = bleed("03_ground.jpg")
    caption(
        s,
        "Ground truth — не «правда мира», а записанная метка",
        "Сеть учится повторять аннотации. Качество модели ≤ качество разметки (ЛР5).",
    )

    # 4 Types — panels already have CLASS/BBOX/MASK; only bottom caption (no top bar overlap)
    s = bleed("04_types.jpg")
    rect(s, 0, H - Cm(1.7), W, Cm(1.7), BG)
    tf = tb(s, Cm(1.5), H - Cm(1.25), Cm(30), Cm(1))
    R(
        tf.paragraphs[0],
        "Три вида разметки · берём минимально достаточный: CLASS / BBOX / MASK",
        size=16,
        bold=True,
        color=INK,
        font=FH,
    )

    # 5 Rules with REAL correct boxes
    s = bleed("05_rules.jpg")
    caption(
        s,
        "Плотная рамка · окклюзия целиком · конкретные имена классов",
        "Рамка без лишнего фона и без обрезки. Закрытый объект — как будто виден полностью. wrench / hammer / pliers.",
    )

    # 6 Compare
    s = bleed("06_compare.jpg")
    rect(s, 0, 0, W / 2, Cm(1.2), RGBColor(0x28, 0x0E, 0x0E))
    rect(s, W / 2, 0, W / 2, Cm(1.2), RGBColor(0x0E, 0x28, 0x1C))
    tf = tb(s, Cm(0.7), Cm(0.25), Cm(14), Cm(0.8))
    R(tf.paragraphs[0], "×  ошибка разметчика", size=16, bold=True, color=WARN, font=FH)
    tf = tb(s, W / 2 + Cm(0.7), Cm(0.25), Cm(14), Cm(0.8))
    R(tf.paragraphs[0], "✓  корректные плотные рамки", size=16, bold=True, color=ACC, font=FH)
    rect(s, 0, H - Cm(2.8), W, Cm(2.8), BG)
    tf = tb(s, Cm(1.5), H - Cm(2.15), Cm(29), Cm(1.6))
    tf.word_wrap = True
    R(tf.paragraphs[0], "Для модели ошибка разметки — не мусор, а целевой ответ в loss.", size=24, bold=True, color=INK, font=FH)

    # 7 Formats
    s = bleed("07_formats.jpg")
    tf = tb(s, Cm(1.5), Cm(1.6), Cm(15), Cm(1.2))
    R(tf.paragraphs[0], "YOLO · VOC · COCO", size=28, bold=True, color=INK, font=FH)
    tf = tb(s, Cm(1.5), Cm(3.0), Cm(15), Cm(1.2))
    tf.word_wrap = True
    R(tf.paragraphs[0], "Одна геометрия объекта — три формата записи.", size=15, color=DIM)
    roundr(s, Cm(1.5), Cm(5.0), Cm(15.5), Cm(7.5), RGBColor(0x12, 0x14, 0x1A))
    tf = tb(s, Cm(2.2), Cm(5.6), Cm(14), Cm(6.2))
    tf.word_wrap = True
    p = tf.paragraphs[0]
    R(p, "YOLO (формат ЛР6)", size=13, color=ACC, font="Consolas")
    p2 = tf.add_paragraph()
    p2.space_before = Pt(14)
    R(p2, "0  0.51  0.43  0.18  0.27", size=22, bold=True, color=INK, font="Consolas")
    p3 = tf.add_paragraph()
    p3.space_before = Pt(14)
    R(p3, "class  xc  yc  w  h\nнормировано в [0…1]\n\nVOC — XML  ·  COCO — JSON", size=14, color=DIM, font="Consolas")

    # 8 Part 2
    s = bleed("08_part2.jpg")
    caption(
        s,
        "Часть 2. Как собрать датасет, который не обманет метрики",
        "Разнообразие условий · соседние кадры · train/valid/test · leakage · баланс · negatives",
        color_line=WARN,
    )

    # 9 Diversity
    s = bleed("09_diversity.jpg")
    caption(
        s,
        "Разнообразие условий важнее «просто большого числа файлов»",
        "Свет, ракурс, фон, перекрытия, другая смена/камера — иначе модель выучит одну сцену.",
        color_line=WARN,
    )

    # 10 Adjacent / duplicates
    s = bleed("10_duplicates.jpg")
    caption(
        s,
        "500 соседних кадров хуже, чем 100 разных",
        "Почти копии мало дают новых признаков и помогают запомнить фон. Нарезка — так, чтобы кадры отличались.",
        color_line=WARN,
    )

    # 11 Leakage
    s = bleed("11_leakage.jpg")
    caption(
        s,
        "Data leakage: почти одинаковые кадры одного ролика в train и test",
        "Метрики завышены. Решение ЛР5: split по роликам, не шаффлить соседние кадры.",
        color_line=WARN,
    )

    # 12 Solutions
    s = bleed("12_negatives.jpg")
    tf = tb(s, Cm(1.5), Cm(1.4), Cm(15), Cm(1.1))
    R(tf.paragraphs[0], "Практика: что делать", size=26, bold=True, color=INK, font=FH)
    tips = [
        ("1. Split по роликам", "Все кадры videoXX — только в одной выборке"),
        ("2. Баланс классов", "Kд = Nmax/Nmin, ориентир ≤ 3"),
        ("3. Negative images", "Кадры без объектов — чтобы не было ложных детекций"),
        ("4. Проверка split", "Каждый класс должен быть в train / valid / test"),
    ]
    for i, (t, d) in enumerate(tips):
        y = Cm(3.0 + i * 2.7)
        roundr(s, Cm(1.5), y, Cm(15.5), Cm(2.4), RGBColor(0x12, 0x14, 0x1A))
        tf = tb(s, Cm(2.1), y + Cm(0.35), Cm(14), Cm(0.7))
        R(tf.paragraphs[0], t, size=15, bold=True, color=ACC, font=FH)
        tf = tb(s, Cm(2.1), y + Cm(1.15), Cm(14), Cm(0.9))
        R(tf.paragraphs[0], d, size=13, color=DIM)

    # 13 End
    s = bleed("13_end.jpg")
    caption(
        s,
        "Разметка задаёт, чему учится модель.\nДатасет задаёт, чему она сможет.",
        "Спасибо. Вопросы?",
    )

    n = len(slides)
    assert n == 13
    for i, s in enumerate(slides, 1):
        if i not in (1, 2, 8, 13):
            pagenum(s, i, n)

    # content checklist embedded in notes of slide 2
    notes(
        slides[1],
        "Содержание темы 7: GT; class/bbox/mask; плотная рамка; окклюзии; имена; YOLO/VOC/COCO; "
        "ошибка→истина; разнообразие; соседние кадры; train/valid/test; leakage; баланс; negatives; split по роликам.",
    )

    try:
        prs.save(str(OUT))
        print("saved", OUT, "slides", n)
    except PermissionError:
        prs.save(str(OUT_ALT))
        print("locked -> saved", OUT_ALT, "slides", n)


if __name__ == "__main__":
    build()
