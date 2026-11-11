# -*- coding: utf-8 -*-
"""
Вариант 9 (Алгоритм 3): сравнить SAVE_VIDEO=True и False.
В обоих режимах наносятся рамки (result.plot) и пишутся CSV;
меняется только запись annotated.mp4. По три прохода каждого режима.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "variant9_save_video"


def run_once(save_video: bool, pass_i: int) -> dict:
    out = RESULTS / f"{'on' if save_video else 'off'}_pass{pass_i}"
    if out.exists():
        # fresh directory required by run_video exist_ok=False
        import shutil

        shutil.rmtree(out)
    cmd = [
        sys.executable,
        "run_video.py",
        "--save-video",
        "1" if save_video else "0",
        "--output",
        str(out.relative_to(ROOT)).replace("\\", "/"),
    ]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    summary["pass"] = pass_i
    summary["mode"] = "SAVE_VIDEO=True" if save_video else "SAVE_VIDEO=False"
    summary["output"] = str(out.relative_to(ROOT)).replace("\\", "/")
    return summary


def median_summary(rows: list[dict]) -> dict:
    keys = [
        "predict_mean_ms",
        "cycle_mean_ms",
        "cycle_median_ms",
        "cycle_p95_ms",
        "processing_fps",
        "over_budget_percent",
    ]
    out = {k: float(np.median([r[k] for r in rows])) for k in keys}
    out["n_passes"] = len(rows)
    out["frames"] = rows[0]["frames"]
    out["source_fps"] = rows[0]["source_fps"]
    out["save_video"] = rows[0]["save_video"]
    return out


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    on_rows = [run_once(True, i) for i in range(1, 4)]
    off_rows = [run_once(False, i) for i in range(1, 4)]
    report = {
        "variant": 9,
        "description": "Сравнение SAVE_VIDEO=True/False при одинаковом нанесении рамок и записи CSV; 3 прохода каждого режима после прогрева.",
        "passes_true": on_rows,
        "passes_false": off_rows,
        "median_true": median_summary(on_rows),
        "median_false": median_summary(off_rows),
    }
    # delta
    report["delta_median_cycle_ms"] = (
        report["median_true"]["cycle_median_ms"] - report["median_false"]["cycle_median_ms"]
    )
    report["delta_median_p95_ms"] = (
        report["median_true"]["cycle_p95_ms"] - report["median_false"]["cycle_p95_ms"]
    )
    (RESULTS / "compare.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # copy first True run as primary lr7_video for report artifacts
    primary = ROOT / "results" / "lr7_video"
    import shutil

    if primary.exists():
        shutil.rmtree(primary)
    shutil.copytree(RESULTS / "on_pass1", primary)
    print(json.dumps(report["median_true"], ensure_ascii=False, indent=2))
    print(json.dumps(report["median_false"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
