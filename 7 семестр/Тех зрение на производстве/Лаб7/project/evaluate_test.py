# -*- coding: utf-8 -*-
"""Шаг 4 ЛР7: итоговая оценка на test + mAP."""
from pathlib import Path
import json
import torch
from ultralytics import YOLO
from evaluate_frames import evaluate

cfg = json.loads(Path("results/lr7_mode.json").read_text(encoding="utf-8"))
device = 0 if torch.cuda.is_available() else "cpu"
model = YOLO(cfg["weights"])
result = evaluate(
    model,
    "dataset/test/images",
    "dataset/test/labels",
    cfg["conf"],
    cfg["imgsz"],
    device,
    cfg["match_iou"],
)
metrics = model.val(
    data="dataset/data.yaml",
    split="test",
    imgsz=cfg["imgsz"],
    device=device,
    batch=1,
    workers=0,
    conf=0.001,
    iou=cfg["nms_iou"],
    plots=True,
    project="runs/lr7",
    name="test_final",
)
result.update(map50=float(metrics.box.map50), map50_95=float(metrics.box.map))
Path("results/lr7_test.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(result)
