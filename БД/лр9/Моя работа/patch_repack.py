#!/usr/bin/env python3
"""Repack lr9_movies.lgp: XML-only units, union + meta-scaling patches."""
from __future__ import annotations

import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from patch_join import patch_join_node
from patch_meta_scaling import patch_unit1
from patch_movies_text import patch_movies_text
from patch_union import patch_union_node

ROOT = Path(__file__).resolve().parent
LGP = ROOT / "lr9_movies.lgp"
PKG_SRC = ROOT.parent / "Лаба" / "lr9_pathfix_src"

DROP_BINS = {
    "Unit_0/Unit.bin",
    "Unit_0/Info.bin",
    "Unit_1/Unit.bin",
    "Unit_1/Info.bin",
}


def repack() -> None:
    work = ROOT / "_repack"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(PKG_SRC, work)

    for xml in work.rglob("*.xml"):
        raw = patch_movies_text(xml.read_text(encoding="utf-8"))
        if xml.name == "Unit.xml" and xml.parent.name == "Unit_0":
            raw = patch_union_node(raw)
            raw = patch_join_node(raw)
        if xml.name == "Unit.xml" and xml.parent.name == "Unit_1":
            raw = patch_unit1(raw)
        xml.write_text(raw, encoding="utf-8")
        ET.parse(xml)

    for rel in DROP_BINS:
        p = work / rel
        if p.exists():
            p.unlink()

    backup = LGP.with_suffix(".lgp.bak")
    if LGP.exists():
        shutil.copy2(LGP, backup)
        LGP.unlink()

    with zipfile.ZipFile(LGP, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(work.rglob("*")):
            if fp.is_file():
                zf.write(fp, fp.relative_to(work).as_posix())

    shutil.rmtree(work)
    print(f"Repacked {LGP} (no Unit *.bin, union + meta-scaling patched)")


if __name__ == "__main__":
    repack()
