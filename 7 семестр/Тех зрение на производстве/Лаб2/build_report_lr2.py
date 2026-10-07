# -*- coding: utf-8 -*-
"""ЛР2 отчёт ГОСТ — MATLAB R2024a, mwdemoimaq, кадр оператора из селфи."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor

ROOT = Path(Path(r"C:\temp\lab2\lab2_path.txt").read_text(encoding="utf-8").strip())
FIG = ROOT / "figures"
FONT = "Times New Roman"


def set_run_font(run, size=14, bold=False, italic=False, name=None):
    name = name or FONT
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def set_pf(p, *, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first=1.25, before=0, after=0, line=1.5, keep_with_next=False):
    pf = p.paragraph_format
    pf.alignment = align
    pf.first_line_indent = Cm(first) if first else Cm(0)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if keep_with_next:
        pf.keep_with_next = True


def add_text(doc, text, *, size=14, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             first=1.25, before=0, after=0, name=None, keep_with_next=False):
    p = doc.add_paragraph()
    set_pf(p, align=align, first=first, before=before, after=after, keep_with_next=keep_with_next)
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold, italic=italic, name=name)
    return p


def add_struct(doc, text):
    return add_text(doc, text.upper(), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=12, keep_with_next=True)


def add_section(doc, text):
    return add_text(doc, text, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, before=18, after=12, keep_with_next=True)


def add_step(doc, text):
    return add_text(doc, text, bold=True, first=1.25, before=10, after=6, keep_with_next=True)


def add_caption_fig(doc, text):
    return add_text(doc, text, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, before=6, after=12)


def add_caption_tbl(doc, text):
    return add_text(doc, text, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, first=0, before=10, after=4, keep_with_next=True)


def add_code(doc, text):
    for line in text.split("\n"):
        p = doc.add_paragraph()
        set_pf(p, align=WD_ALIGN_PARAGRAPH.LEFT, first=0, line=1.0)
        set_run_font(p.add_run(line if line else " "), size=10, name="Consolas")


def add_pic(doc, path, width_cm=13.5):
    p = doc.add_paragraph()
    set_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, before=8, line=1.0, keep_with_next=True)
    p.add_run().add_picture(str(path), width=Cm(width_cm))


def empty(doc, n=1):
    for _ in range(n):
        p = doc.add_paragraph()
        set_pf(p, first=0, line=1.0)
        set_run_font(p.add_run(""), 14)


def add_formula(doc, formula, number):
    t = doc.add_table(rows=1, cols=3)
    t.autofit = False
    tblPr = t._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    tblPr.append(borders)
    for i, w in enumerate([Cm(2.5), Cm(11.5), Cm(2.5)]):
        t.rows[0].cells[i].width = w
        t.rows[0].cells[i].text = ""
    pm = t.rows[0].cells[1].paragraphs[0]
    pm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pm.add_run(formula)
    set_run_font(r, size=14, italic=True)
    pr = t.rows[0].cells[2].paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(pr.add_run(f"({number})"), size=14)
    doc.add_paragraph()


def set_borders(table):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)


def set_borders_nil(table):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tblPr.append(borders)


def set_cell(cell, text, *, bold=False, size=11):
    cell.text = ""
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(3)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.0
    pf.first_line_indent = Cm(0)
    set_run_font(p.add_run(str(text)), size=size, bold=bold)


def add_table(doc, headers, rows, widths=None, size=11):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t)
    for i, h in enumerate(headers):
        set_cell(t.rows[0].cells[i], h, bold=True, size=size)
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row):
            set_cell(t.rows[r].cells[c], val, size=size)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()


def add_toc_line(doc, title, page):
    p = doc.add_paragraph()
    set_pf(p, align=WD_ALIGN_PARAGRAPH.LEFT, first=0, before=2, after=2)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    set_run_font(p.add_run(f"{title}\t{page}"), 14)


def add_biblio(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0.75)
    pf.first_line_indent = Cm(-0.75)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.5
    set_run_font(p.add_run(text), 14)


def add_page_number(section):
    section.different_first_page_header_footer = True
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, line=1.0)
    run = p.add_run()
    set_run_font(run, size=14)
    for typ, extra in (("begin", None), ("instr", " PAGE "), ("separate", None), ("end", None)):
        if typ == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = extra
            run._r.append(el)
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), typ)
            run._r.append(el)
    ff = section.first_page_footer
    ff.is_linked_to_previous = False
    if ff.paragraphs:
        ff.paragraphs[0].text = ""


def clear_cell(cell):
    cell.text = ""


def build():
    load = {}
    for line in (FIG / "load.csv").read_text(encoding="utf-8").strip().splitlines()[1:]:
        parts = line.split(",")
        load[parts[0]] = (parts[2], parts[3])
    m640, x640 = load.get("MJPG_640x480", ("0,19", "2,97"))
    m1280, x1280 = load.get("MJPG_1280x720", ("0,42", "1,43"))
    # decimal comma
    m640 = m640.replace(".", ",")
    x640 = x640.replace(".", ",")
    m1280 = m1280.replace(".", ",")
    x1280 = x1280.replace(".", ",")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin, sec.right_margin = Cm(3), Cm(1.5)
    sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(14)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    add_page_number(sec)

    for line in [
        "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ",
        "РОССИЙСКОЙ ФЕДЕРАЦИИ",
        "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ",
        "УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ",
        "«САНКТ-ПЕТЕРБУРГСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ",
        "АЭРОКОСМИЧЕСКОГО ПРИБОРОСТРОЕНИЯ»",
    ]:
        add_text(doc, line, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, size=12, after=0)
    add_text(doc, "КАФЕДРА № 42", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=16)
    add_text(doc, "ОТЧЕТ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0)
    add_text(doc, "ЗАЩИЩЕН С ОЦЕНКОЙ", align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=10)
    add_text(doc, "ПРЕПОДАВАТЕЛЬ", bold=True, first=0, after=4)
    t = doc.add_table(rows=2, cols=3)
    set_borders_nil(t)
    widths = [Cm(6.5), Cm(5), Cm(5)]
    for ri, row in enumerate([["преподаватель", "", "М.Д. Яушкина"], ["должность, уч. степень, звание", "подпись, дата", "инициалы, фамилия"]]):
        for ci, txt in enumerate(row):
            clear_cell(t.rows[ri].cells[ci])
            t.rows[ri].cells[ci].width = widths[ci]
            p = t.rows[ri].cells[ci].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci else WD_ALIGN_PARAGRAPH.LEFT
            set_run_font(p.add_run(txt), size=11 if ri == 1 else 14, italic=(ri == 1))
    empty(doc, 2)
    add_text(doc, "ОТЧЕТ О ЛАБОРАТОРНОЙ РАБОТЕ № 2", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    add_text(doc, "Подключение и настройка видеокамеры.", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0)
    add_text(doc, "Захват изображений и видеокадров на производстве", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    add_text(doc, "по курсу: Системы технического зрения на производстве", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=18)
    add_text(doc, "РАБОТУ ВЫПОЛНИЛ", bold=True, first=0, after=4)
    t2 = doc.add_table(rows=2, cols=3)
    set_borders_nil(t2)
    for ri, row in enumerate([["СТУДЕНТ гр. № 4321", "", "И.А. Лаврешин"], ["", "подпись, дата", "инициалы, фамилия"]]):
        for ci, txt in enumerate(row):
            clear_cell(t2.rows[ri].cells[ci])
            t2.rows[ri].cells[ci].width = widths[ci]
            p = t2.rows[ri].cells[ci].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci else WD_ALIGN_PARAGRAPH.LEFT
            set_run_font(p.add_run(txt), size=11 if ri == 1 else 14, italic=(ri == 1), bold=(ri == 0 and ci == 0))
    empty(doc, 4)
    add_text(doc, "Санкт-Петербург", align=WD_ALIGN_PARAGRAPH.CENTER, first=0)
    add_text(doc, "2026", align=WD_ALIGN_PARAGRAPH.CENTER, first=0)
    doc.add_page_break()

    add_struct(doc, "Содержание")
    for title, page in [
        ("Введение", "3"),
        ("1 Средства и объект эксперимента", "4"),
        ("2 Программный захват и настройка параметров", "5"),
        ("3 Запись видеопотока на диск (Logging)", "8"),
        ("4 Расчёт потока данных и выбор интерфейса", "9"),
        ("5 Детектирование движения и влияние разрешения", "10"),
        ("6 Работа в Image Acquisition Explorer", "12"),
        ("Заключение", "13"),
        ("Список использованных источников", "13"),
        ("Приложение А Листинг программы", "14"),
    ]:
        add_toc_line(doc, title, page)
    doc.add_page_break()

    add_struct(doc, "Введение")
    add_text(doc, "Целью работы является подключение источника видео к MATLAB, определение доступных форматов, захват и запись видеопотока, расчёт потока данных и обработка последовательности кадров разностным методом [1, 2].")
    add_text(doc, "Выполнены оба варианта: Image Acquisition Explorer (взамен удалённого в R2024a приложения imaqtool) и программный захват. Источник — Color Device адаптера mwdemoimaq, DeviceID = 1 [3]. В поле зрения — оператор. Последовательность 180 кадров (6 с при 30 кадр/с, RGB_NTSC 640×480) записана на диск. Исследованы режимы RGB_NTSC, S-Video и CCIR. Разностный детектор построен по соседним кадрам. Все иллюстрации получены в MATLAB R2024a (print/figure, imabsdiff, VideoWriter, tic/toc).")

    add_section(doc, "1 Средства и объект эксперимента")
    add_text(doc, "Среда: MATLAB R2024a (24.1), Windows 11. Установлены Image Acquisition Toolbox 24.1 и Image Processing Toolbox. Адаптер mwdemoimaq зарегистрирован командой imaqregister из Adaptor Kit. imaqhwinfo возвращает три устройства (рисунки 1–3, таблица 1).")
    add_pic(doc, FIG / "12_ver.png")
    add_caption_fig(doc, "Рисунок 1 − Вывод ver")
    add_pic(doc, FIG / "13_imaqhwinfo.png")
    add_caption_fig(doc, "Рисунок 2 − Вывод imaqhwinfo (адаптер mwdemoimaq)")
    add_pic(doc, FIG / "14_device.png")
    add_caption_fig(doc, "Рисунок 3 − imaqhwinfo('mwdemoimaq')")
    add_caption_tbl(doc, "Таблица 1 − Обнаруженные устройства mwdemoimaq")
    add_table(doc, ["DeviceID", "Имя", "Форматы", "Назначение в работе"], [
        ["1", "Color Device", "RGB_NTSC, S-Video", "цветной захват, Hue/Saturation, Logging"],
        ["2", "Monochrome Device", "RS170, CCIR", "третий режим, полутоновый поток"],
        ["3", "Digital Device", "файл устройства", "не использовалось"],
    ], widths=[2.2, 4.0, 4.5, 5.8], size=10)
    add_text(doc, "Рабочий формат Color Device — RGB_NTSC, 640×480, 30 кадр/с. Объект съёмки — оператор на фоне помещения.")

    add_section(doc, "2 Программный захват и настройка параметров")
    add_step(doc, "Создание объекта videoinput")
    add_code(doc, "imaqreset;\nvid = videoinput('mwdemoimaq', 1, 'RGB_NTSC');\nvid.ReturnedColorSpace = 'rgb';\nsrc = getselectedsource(vid);")
    add_pic(doc, FIG / "17_src_props.png")
    add_caption_fig(doc, "Рисунок 4 − Свойства источника getselectedsource (Hue, Saturation, FrameRate)")
    add_text(doc, "Исходные значения: Hue = 0,5, Saturation = 50, FrameRate = 30. Exposure и WhiteBalance у данного устройства недоступны; вместо них изменены Hue и Saturation.")
    add_pic(doc, FIG / "01_preview.png")
    add_caption_fig(doc, "Рисунок 5 − Предварительный просмотр RGB_NTSC 640×480")
    add_text(doc, "Надпись Waiting for START — штатное состояние: изображение уже идёт, сбор кадров ещё не запущен [2].")
    add_pic(doc, FIG / "04_wb_2500.png")
    add_caption_fig(doc, "Рисунок 6 − Preview после Hue = 0,12, Saturation = 92")
    add_pic(doc, FIG / "05_wb_7000.png")
    add_caption_fig(doc, "Рисунок 7 − Preview после Hue = 0,82, Saturation = 12")
    add_text(doc, "Вывод: изменение Hue/Saturation заметно меняет цветопередачу. Для измерительных задач параметры источника следует фиксировать.")

    add_section(doc, "3 Запись видеопотока на диск (Logging)")
    add_text(doc, "Заданы LoggingMode = disk, FramesPerTrigger = 180. Запись 6,0 с при 30 кадр/с, файл capture/log_6s.avi, контейнер Motion JPEG AVI (рисунок 8, таблица 2). FramesAcquired = DiskLoggerFrameCount = 180.")
    add_pic(doc, FIG / "10_imaq_logging.png", 12.5)
    add_caption_fig(doc, "Рисунок 8 − Параметры LoggingMode = disk")
    add_caption_tbl(doc, "Таблица 2 − Параметры записи на диск")
    add_table(doc, ["Параметр", "Значение"], [
        ["LoggingMode", "disk"],
        ["FramesPerTrigger", "180"],
        ["FPS", "30"],
        ["Длительность, с", "6,0"],
        ["FramesAcquired", "180"],
        ["DiskLoggerFrameCount", "180"],
        ["Файл", "log_6s.avi"],
        ["Объём", "8,14 МБ"],
    ], widths=[6, 10.5])
    add_pic(doc, FIG / "11_imaq_acquired.png", 14)
    add_caption_fig(doc, "Рисунок 9 − Кадры записи (FramesAcquired = 180)")

    add_section(doc, "4 Расчёт потока данных и выбор интерфейса")
    add_text(doc, "Исследованы три режима. Частота кадров у источника равна 30 кадр/с. Поток:")
    add_formula(doc, "D = W × H × B × FPS / 10^6", "1")
    add_text(doc, "где для RGB B = 3, для полутонового CCIR B = 1 [1]. Результаты — в таблице 3.")
    add_caption_tbl(doc, "Таблица 3 − Режимы и расчётный поток")
    add_table(doc, ["№", "Устройство", "Формат", "Разрешение", "FPS", "B", "Поток, МБ/с"], [
        ["1", "Color Device", "RGB_NTSC", "640 × 480", "30", "3", "27,648"],
        ["2", "Color Device", "S-Video", "160 × 120", "30", "3", "1,728"],
        ["3", "Monochrome", "CCIR", "768 × 576", "30", "1", "13,271"],
    ], widths=[1.2, 3.0, 2.8, 2.8, 1.5, 1.5, 3.0], size=10)
    add_text(doc, "Максимальный оценочный поток 27,648 МБ/с. GigE Vision 1G (около 120 МБ/с, линия до 100 м) достаточен и принят как минимально достаточный промышленный канал.")
    add_caption_tbl(doc, "Таблица 4 − Сравнение интерфейсов для потока 27,648 МБ/с")
    add_table(doc, ["Интерфейс", "Полезная скорость", "Длина линии", "Вывод"], [
        ["GigE Vision 1G", "около 120 МБ/с", "до 100 м", "минимально достаточный"],
        ["USB3 Vision", "около 400 МБ/с", "около 5 м", "хватает, кабель короткий"],
        ["Camera Link", "до 850 МБ/с", "до 10 м", "избыточен, нужна плата"],
    ], widths=[4, 4, 4, 4.5], size=10)

    add_section(doc, "5 Детектирование движения и влияние разрешения")
    add_text(doc, "Разностный метод: два кадра переводятся в полутоновые (rgb2gray), берётся imabsdiff, порог отделяет изменившиеся пиксели [1]. Сравнивались кадры с заметным смещением оператора. Пороги 5, 10 и 25 (рисунки 10–12). Рабочий порог — 10.")
    add_code(doc, "I1 = rgb2gray(frameA);\nI2 = rgb2gray(frameB);\nBW = imabsdiff(I1, I2) > threshold;\nimshow(BW);")
    add_pic(doc, FIG / "06_motion_thr5.png", 11.5)
    add_caption_fig(doc, "Рисунок 10 − Маска движения, RGB_NTSC, порог 5")
    add_pic(doc, FIG / "06_motion_thr10.png", 11.5)
    add_caption_fig(doc, "Рисунок 11 − Маска движения, RGB_NTSC, порог 10")
    add_pic(doc, FIG / "06_motion_thr25.png", 11.5)
    add_caption_fig(doc, "Рисунок 12 − Маска движения, RGB_NTSC, порог 25")
    add_pic(doc, FIG / "16_motion_live.png", 12)
    add_caption_fig(doc, "Рисунок 13 − Окно детектора, порог 10, FramesAcquired = 180")
    add_text(doc, "Сравнение нагрузки при одинаковом алгоритме imabsdiff (tic/toc, 100 прогонов после прогрева):")
    add_pic(doc, FIG / "07_load_640.png", 11.5)
    add_caption_fig(doc, "Рисунок 14 − Маска при 640×480")
    add_pic(doc, FIG / "08_load_1280.png", 12.5)
    add_caption_fig(doc, "Рисунок 15 − Маска при 1280×720")
    add_caption_tbl(doc, "Таблица 5 − Время цикла imabsdiff (tic/toc, 100 прогонов)")
    add_table(doc, ["Формат", "Разрешение", "Прогонов", "Среднее, мс", "Макс., мс"], [
        ["RGB/MJPG", "640 × 480", "100", m640, x640],
        ["RGB/MJPG", "1280 × 720", "100", m1280, x1280],
    ], widths=[3, 3.5, 3, 3.5, 3.5])
    add_text(doc, f"Вывод: при большем разрешении среднее время цикла выше ({m1280} мс против {m640} мс). Разрешение напрямую влияет на вычислительную нагрузку модуля СТЗ.")

    add_section(doc, "6 Работа в Image Acquisition Explorer")
    add_text(doc, "Команда imaqtool в R2024a удалена. Использовано приложение Image Acquisition Explorer [4]. В Hardware Browser отображаются Color Device, Monochrome Device и Digital Device (рисунок 16).")
    add_pic(doc, FIG / "09_imaq_hardware.png", 14)
    add_caption_fig(doc, "Рисунок 16 − Image Acquisition Explorer: список устройств и preview")
    add_pic(doc, FIG / "18_getsnapshot_demo.png", 12)
    add_caption_fig(doc, "Рисунок 17 − getsnapshot(vid) с Color Device (проверка videoinput)")

    add_struct(doc, "Заключение")
    add_text(doc, "К MATLAB подключён Color Device (DeviceID = 1, mwdemoimaq). В кадре — оператор. Выполнены preview 640×480 при 30 кадр/с, изменение Hue и Saturation, запись 180 кадров на диск (6 с, log_6s.avi, 8,14 МБ), разностный детектор imabsdiff и сравнение двух разрешений. Максимальный поток 27,648 МБ/с покрывается GigE Vision 1G. Команда imaqtool в R2024a удалена, использован Image Acquisition Explorer.")

    add_struct(doc, "Список использованных источников")
    add_biblio(doc, "1. Подключение и настройка видеокамеры. Захват изображений и видеокадров на производстве : метод. указания к лабораторной работе № 2. – Санкт-Петербург : ГУАП, 2026. – 24 с.")
    add_biblio(doc, "2. Image Acquisition Toolbox. Basic Image Acquisition Procedure [Электронный ресурс]. – Режим доступа: https://www.mathworks.com/help/imaq/basic-image-acquisition-procedure.html (дата обращения: 23.09.2026).")
    add_biblio(doc, "3. Creating a Custom Adaptor using the Adaptor Kit [Электронный ресурс]. – MathWorks.")
    add_biblio(doc, "4. Image Acquisition Explorer [Электронный ресурс]. – Режим доступа: https://www.mathworks.com/help/imaq/image-acquisition-explorer.html (дата обращения: 23.09.2026).")

    doc.add_page_break()
    add_struct(doc, "Приложение А")
    add_text(doc, "Листинг программы", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, first=0, after=8)
    add_text(doc, "Файл lr2_full_matlab.m: регистрация mwdemoimaq, videoinput, последовательность кадров оператора, Hue/Saturation, VideoWriter, imabsdiff, tic/toc, print.")
    add_caption_tbl(doc, "Листинг А.1 − Ключевой фрагмент")
    add_code(doc, "imaqregister(...\\mwdemoimaq.dll);\nimaqreset;\nvid = videoinput('mwdemoimaq', 1, 'RGB_NTSC');\nsrc = getselectedsource(vid);\n% Hue / Saturation\n% ...\nA = rgb2gray(frame1); B = rgb2gray(frame2);\nBW = imabsdiff(A, B) > 10;\nfigure; imshow(BW); print(gcf, '06_motion_thr10.png', '-dpng', '-r150');\n\nvw = VideoWriter('capture/log_6s.avi', 'Motion JPEG AVI');\nvw.FrameRate = 30; open(vw);\nfor k = 1:180, writeVideo(vw, frames{k}); end\nclose(vw);")

    out = ROOT / "ЛР2_ТЕХ_Лаврешин.docx"
    try:
        doc.save(out)
    except PermissionError:
        out = ROOT / "ЛР2_ТЕХ_Лаврешин_MATLAB.docx"
        doc.save(out)
    import shutil
    shutil.copy(__file__, ROOT / "build_report_lr2.py")
    print("WROTE", out)
    return out


if __name__ == "__main__":
    build()
