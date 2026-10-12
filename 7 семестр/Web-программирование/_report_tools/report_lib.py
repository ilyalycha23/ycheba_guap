# -*- coding: utf-8 -*-
"""Общие функции сборки отчётов по шаблону титула ЛР1/ЛР2."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(r"D:\ycheba_guap\7 семестр\Web-программирование")
TEMPLATE = ROOT / "lab1" / "ЛР1_Веб_Лаврешин.docx"


def set_run_font(run, size=14, bold=False, name="Times New Roman", italic=False):
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.get_or_add_rFonts()
    for key in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        r_fonts.set(qn(key), name)


def fmt_para(p, *, justify=False, indent=True, line=1.5):
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25) if indent else Cm(0)
    p.paragraph_format.line_spacing = line
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)


TEACHER = {"доцент, канд. техн. наук": "ассистент", "Е. Л. Турнецкая": "В. В. Жукалин"}


def patch_teacher(doc):
    for cell in doc.tables[0]._cells:
        for p in cell.paragraphs:
            text = p.text.strip()
            if text in TEACHER and p.runs:
                p.runs[0].text = TEACHER[text]
                for run in p.runs[1:]:
                    run.text = ""


class Report:
    """Отчёт: титул из шаблона ЛР1, тело и листинги в едином стиле."""

    def __init__(self, lab: int, title_upper: str):
        self.lab = lab
        self.lab_dir = ROOT / f"lab{lab}"
        self.assets = self.lab_dir / "report_assets"
        self.src = self.lab_dir / "signalboard"
        self.out = self.lab_dir / f"ЛР{lab}_Веб_Лаврешин.docx"
        self.figure = 0
        self.headings = 0
        shutil.copyfile(TEMPLATE, self.out)
        self.doc = Document(str(self.out))
        self._patch_title(title_upper)
        self._clear_body()

    def _patch_title(self, title_upper: str):
        patch_teacher(self.doc)
        cell = self.doc.tables[1].rows[0].cells[0]
        for p in cell.paragraphs:
            for r in p.runs:
                if r.text.strip() == "1":
                    r.text = str(self.lab)
                if "СОЗДАНИЕ ПРОЕКТА NEXT.JS" in r.text:
                    r.text = title_upper

    def _clear_body(self):
        body = self.doc.element.body
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
            if removing and child.tag != qn("w:sectPr"):
                body.remove(child)

    def heading(self, num: str, title: str):
        if self.headings:
            self.page_break()
        self.headings += 1
        p = self.doc.add_paragraph()
        fmt_para(p)
        set_run_font(p.add_run(f"{num} "), bold=True)
        set_run_font(p.add_run(title), bold=True)

    def _runs_with_fill(self, p, text: str, bold=False):
        """Фрагменты [[...]] студент заполняет на своей машине: выделяем их красным курсивом."""
        for i, part in enumerate(re.split(r"\[\[(.*?)\]\]", text)):
            if not part:
                continue
            run = p.add_run(f"[{part}]" if i % 2 else part)
            if i % 2:
                set_run_font(run, italic=True, bold=bold)
                run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
            else:
                set_run_font(run, bold=bold)

    def body(self, text: str):
        p = self.doc.add_paragraph()
        fmt_para(p, justify=True)
        self._runs_with_fill(p, text)

    def bullets(self, items: list[str]):
        for item in items:
            p = self.doc.add_paragraph()
            fmt_para(p, justify=True)
            self._runs_with_fill(p, f"– {item}")

    def center(self, text: str, bold=False, size=14):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt_para(p, indent=False)
        set_run_font(p.add_run(text), size=size, bold=bold)

    def nxt(self, k: int = 1) -> int:
        """Номер рисунка, который будет добавлен через k вызовов picture/placeholder."""
        return self.figure + k

    def picture(self, name: str, caption: str, width=16.0):
        self.figure += 1
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt_para(p, indent=False)
        p.add_run().add_picture(str(self.assets / name), width=Cm(width))
        self.center(f"Рисунок {self.figure} – {caption}")

    def placeholder(self, caption: str, hint: str):
        """Рамка на месте скриншота, который снимается только на машине студента."""
        self.figure += 1
        table = self.doc.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        cell = table.rows[0].cells[0]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(36)
        run = p.add_run(f"[ВСТАВИТЬ СКРИНШОТ: {hint}]")
        set_run_font(run, size=12, italic=True)
        run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        self.center(f"Рисунок {self.figure} – {caption}")

    def table(self, header: list[str], rows: list[list[str]]):
        table = self.doc.add_table(rows=1 + len(rows), cols=len(header))
        table.style = "Table Grid"
        for i, h in enumerate(header):
            cell = table.rows[0].cells[i]
            cell.text = ""
            set_run_font(cell.paragraphs[0].add_run(h), bold=True, size=12)
        for ri, row in enumerate(rows, start=1):
            for ci, val in enumerate(row):
                cell = table.rows[ri].cells[ci]
                cell.text = ""
                for i, part in enumerate(re.split(r"\[\[(.*?)\]\]", val)):
                    if not part:
                        continue
                    run = cell.paragraphs[0].add_run(f"[{part}]" if i % 2 else part)
                    set_run_font(run, size=12, italic=bool(i % 2))
                    if i % 2:
                        run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        self.doc.add_paragraph()

    def code(self, text: str, size=10):
        lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
        for line in lines:
            p = self.doc.add_paragraph()
            fmt_para(p, indent=False, line=1.0)
            set_run_font(p.add_run(line if line else " "), size=size, name="Courier New")

    def page_break(self):
        p = self.doc.add_paragraph()
        run = p.add_run()
        br = OxmlElement("w:br")
        br.set(qn("w:type"), "page")
        run._element.append(br)

    def questions(self, num: str, pairs: list[tuple[str, str]]):
        """Контрольные вопросы в отчёт не включаются (ответы – в шпаргалке к защите)."""

    def appendix(self, files: list[str]):
        self.page_break()
        self.center("ПРИЛОЖЕНИЕ А", bold=True)
        self.center("Листинг с кодом программы", bold=True)
        for rel in files:
            p = self.doc.add_paragraph()
            fmt_para(p, indent=False)
            set_run_font(p.add_run(f"Файл {rel}"), bold=True)
            # В отчёт идёт код без комментариев — пояснения не нужны в листинге.
            self.code(strip_code_comments((self.src / rel).read_text(encoding="utf-8"), rel))

    def read_asset(self, name: str) -> str:
        return (self.assets / name).read_text(encoding="utf-8-sig", errors="replace")

    def save(self, pdf=True):
        self.doc.save(str(self.out))
        print("saved", self.out)
        if pdf:
            export_pdf(self.out)


def strip_code_comments(text: str, rel: str = "") -> str:
    """Убирает комментарии из листингов отчёта (исходники на диске не трогает)."""
    ext = Path(rel).suffix.lower()
    # Блочные /* ... */ и JSX {/* ... */}
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    lines: list[str] = []
    for line in text.splitlines():
        raw = line
        stripped = raw.lstrip()
        if stripped.startswith("//"):
            continue
        if ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
            # Хвостовой // вне строк — грубо, но достаточно для учебных файлов.
            in_str = None
            out = []
            i = 0
            while i < len(raw):
                ch = raw[i]
                if in_str:
                    out.append(ch)
                    if ch == "\\" and i + 1 < len(raw):
                        out.append(raw[i + 1])
                        i += 2
                        continue
                    if ch == in_str:
                        in_str = None
                    i += 1
                    continue
                if ch in ('"', "'", "`"):
                    in_str = ch
                    out.append(ch)
                    i += 1
                    continue
                if ch == "/" and i + 1 < len(raw) and raw[i + 1] == "/":
                    break
                out.append(ch)
                i += 1
            raw = "".join(out).rstrip()
            if not raw.strip():
                # сохраняем пустую строку только как разделитель блоков
                if lines and lines[-1] != "":
                    lines.append("")
                continue
            lines.append(raw)
        else:
            if not raw.strip():
                if lines and lines[-1] != "":
                    lines.append("")
                continue
            lines.append(raw.rstrip())
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def export_pdf(docx_path: Path):
    try:
        import win32com.client
    except ImportError:
        print("win32com недоступен, PDF не создан")
        return
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(docx_path.resolve()))
        doc.SaveAs(str(docx_path.with_suffix(".pdf").resolve()), FileFormat=17)
        doc.Close(False)
    finally:
        word.Quit()
    print("pdf", docx_path.with_suffix(".pdf"))
