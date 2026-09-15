# -*- coding: utf-8 -*-
"""Run 1C external processing to fill demo data."""
import subprocess
import sys
from pathlib import Path

V8 = r"C:\Program Files (x86)\1cv8t\8.5.1.1150\bin\1cv8t.exe"
INFOBASE = Path(r"D:\ycheba_guap\КИСП\Курсовая")
SCRIPT_DIR = Path(__file__).resolve().parent
EPF = SCRIPT_DIR / "build" / "FillDemoData.epf"
LOG = SCRIPT_DIR / "build" / "fill-log.txt"
USER = "Администратор"

if not EPF.exists():
    print(f"EPF not found: {EPF}", file=sys.stderr)
    sys.exit(1)

LOG.parent.mkdir(parents=True, exist_ok=True)
if LOG.exists():
    LOG.unlink()

arguments = [
    "ENTERPRISE",
    "/F",
    str(INFOBASE),
    f'/N"{USER}"',
    "/Execute",
    str(EPF),
    "/DisableStartupDialogs",
    "/Out",
    str(LOG),
]

print("Running:", V8)
print("Args:", " ".join(arguments))

try:
    result = subprocess.run(
        [V8, *arguments],
        timeout=300,
    )
    print("Exit code:", result.returncode)
except subprocess.TimeoutExpired:
    print("Timeout: 1C did not finish in 300s", file=sys.stderr)
    sys.exit(2)

if LOG.exists():
    print("\n=== Log ===")
    print(LOG.read_text(encoding="utf-8-sig", errors="replace"))
else:
    print("Log file not created:", LOG)

sys.exit(result.returncode)
