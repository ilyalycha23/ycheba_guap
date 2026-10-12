# -*- coding: utf-8 -*-
"""Временно убирает или возвращает исправления Lighthouse в ЛР4 для честного baseline."""

import shutil
import sys
from pathlib import Path

root = Path(r"D:\ycheba_guap\7 семестр\Web-программирование\lab4\signalboard\app\gallery\_components")
files = [root / "SignalsGallery.tsx", root / "PhotoMap.tsx"]
mode = sys.argv[1]

if mode == "revert":
    for f in files:
        shutil.copyfile(f, f.with_suffix(f.suffix + ".bak"))
    g = files[0].read_text(encoding="utf-8")
    g = g.replace("neighborSignals.map((signal, index) => (", "neighborSignals.map((signal) => (")
    g = "\n".join(
        line
        for line in g.split("\n")
        if "LCP-изображением" not in line
        and "loading={index" not in line
        and "fetchPriority={index" not in line
    )
    files[0].write_text(g, encoding="utf-8")
    m = files[1].read_text(encoding="utf-8")
    m = m.replace('        role="region"\n', "")
    files[1].write_text(m, encoding="utf-8")
    print("reverted")
elif mode == "restore":
    for f in files:
        bak = f.with_suffix(f.suffix + ".bak")
        shutil.copyfile(bak, f)
        bak.unlink()
    print("restored")
else:
    raise SystemExit("usage: toggle_lh_fixes.py revert|restore")
