# -*- coding: utf-8 -*-
"""Шаг 7 ЛР7: количественная оценка video_test."""
from pathlib import Path
import json
import torch
from ultralytics import YOLO
from evaluate_frames import evaluate

cfg = json.loads(Path("results/lr7_mode.json").read_text(encoding="utf-8"))
device = 0 if torch.cuda.is_available() else "cpu"
model = YOLO(cfg["weights"])
video_result = evaluate(
    model,
    "video_test/images",
    "video_test/labels",
    cfg["conf"],
    cfg["imgsz"],
    device,
    cfg["match_iou"],
)
Path("results/lr7_video_quality.json").write_text(
    json.dumps(video_result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(video_result)
