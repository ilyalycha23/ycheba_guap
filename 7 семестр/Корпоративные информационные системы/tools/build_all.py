# -*- coding: utf-8 -*-
import runpy
from pathlib import Path

here = Path(__file__).resolve().parent
for name in ("lab1_build.py", "lab2_build.py", "lab3_build.py"):
    print("====", name, "====")
    runpy.run_path(str(here / name), run_name="__main__")
