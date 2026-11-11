# -*- coding: utf-8 -*-
"""Шаг 3 ЛР7: выбор рабочего порога conf на valid."""
from pathlib import Path
import json
import torch
from ultralytics import YOLO
from evaluate_frames import evaluate

cfg = json.loads(Path("results/selected_model.json").read_text(encoding="utf-8"))
model = YOLO(cfg["weights"])
device = 0 if torch.cuda.is_available() else "cpu"
rows = []
for conf in (0.15, 0.35, 0.55):
    result = evaluate(
        model,
        "dataset/valid/images",
        "dataset/valid/labels",
        conf,
        cfg["imgsz"],
        device,
    )
    if result["F1"] is None:
        raise ValueError("В valid нет размеченных объектов")
    rows.append(dict(conf=conf, **result))
best = max(rows, key=lambda row: (row["F1"], row["P"], row["conf"]))
cfg.update(conf=best["conf"], nms_iou=0.7, match_iou=0.5)
Path("results/lr7_mode.json").write_text(
    json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8"
)
Path("results/lr7_thresholds.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("Выбранный порог:", best["conf"])
for row in rows:
    print(
        f"conf={row['conf']}: TP={row['TP']} FP={row['FP']} FN={row['FN']} "
        f"P={row['P']:.3f} R={row['R']:.3f} F1={row['F1']:.3f}"
    )
