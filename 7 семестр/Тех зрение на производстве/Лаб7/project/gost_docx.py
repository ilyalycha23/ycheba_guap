# -*- coding: utf-8 -*-
"""Оформление отчёта по ГОСТ 7.32 (учебный отчёт): поля, шрифт, интервал, номера страниц."""
from __future__ import annotations

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def set_run_font(run, name="Times New Roman", size=14, bold=False, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_page_numbers(doc: Document):
    """Номер страницы по центру нижнего колонтитула (с первой страницы)."""
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # clear
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    run = p.add_run()
    set_run_font(run, size=12)
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char_begin)
    run2 = p.add_run()
    set_run_font(run2, size=12)
    run2._r.append(instr)
    run3 = p.add_run()
    set_run_font(run3, size=12)
    run3._r.append(fld_char_end)


def init_gost_doc() -> Document:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(1.5)
    add_page_numbers(doc)
    return doc


def add_p(
    doc,
    text="",
    *,
    bold=False,
    center=False,
    size=14,
    first_line=True,
    space_after=6,
    italic=False,
):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    if first_line and not center:
        pf.first_line_indent = Cm(1.25)
    else:
        pf.first_line_indent = Cm(0)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_h(doc, text):
    """Заголовок раздела: полужирный, без абзацного отступа."""
    return add_p(doc, text, bold=True, first_line=False, space_after=8)


def add_fig(doc, path, caption: str, width_cm=15.0):
    from pathlib import Path

    path = Path(path)
    if not path.exists():
        add_p(doc, f"[нет файла: {path.name}]", first_line=False)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width_cm))
    # ГОСТ: подпись под рисунком, тире «−»
    cap = caption.replace(" - ", " − ").replace(" – ", " − ")
    if " − " not in cap and cap.startswith("Рисунок"):
        # "Рисунок N Caption" -> insert dash after number if missing
        parts = cap.split(" ", 2)
        if len(parts) >= 3 and parts[1].rstrip(".").isdigit():
            cap = f"{parts[0]} {parts[1]} − {parts[2]}"
    add_p(doc, cap, center=True, size=12, first_line=False, space_after=10)


def add_table(doc, headers, rows, caption: str | None = None):
    if caption:
        cap = caption.replace(" - ", " − ").replace(" – ", " − ")
        add_p(doc, cap, center=True, size=12, first_line=False, space_after=4)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        set_run_font(run, size=11, bold=True)
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            set_run_font(run, size=11)
    doc.add_paragraph()
