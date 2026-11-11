# -*- coding: utf-8 -*-
"""Шаг 6 ЛР7: обработка видео, detections/timings, измерение цикла."""
from pathlib import Path
import argparse
import csv
import json
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from preprocess import prepare_frame

parser = argparse.ArgumentParser()
parser.add_argument("--save-video", type=int, choices=[0, 1], default=1)
parser.add_argument("--output", type=str, default="results/lr7_video")
parser.add_argument("--source", type=str, default="data/video/test_video.mp4")
args = parser.parse_args()

SOURCE = args.source
OUTPUT = Path(args.output)
SAVE_VIDEO = bool(args.save_video)
cfg = json.loads(Path("results/lr7_mode.json").read_text(encoding="utf-8"))
device = 0 if torch.cuda.is_available() else "cpu"
model = YOLO(cfg["weights"])


def sync():
    if device != "cpu":
        torch.cuda.synchronize(device)


def predict(frame):
    return model.predict(
        frame,
        imgsz=cfg["imgsz"],
        conf=cfg["conf"],
        iou=cfg["nms_iou"],
        device=device,
        rect=False,
        verbose=False,
    )[0]


OUTPUT.mkdir(parents=True, exist_ok=False)
cap = cv2.VideoCapture(SOURCE)
fps = cap.get(cv2.CAP_PROP_FPS)
ok, raw = cap.read()
if not ok or not np.isfinite(fps) or fps <= 0:
    cap.release()
    raise ValueError("Проверьте видео и его частоту кадров")
prepared = prepare_frame(raw)
height, width = prepared.shape[:2]
for _ in range(5):
    predict(prepared)
sync()
cap.release()
cap = cv2.VideoCapture(SOURCE)  # начать заново после прогрева
writer = None
if SAVE_VIDEO:
    writer = cv2.VideoWriter(
        str(OUTPUT / "annotated.mp4"),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Не удалось открыть запись видео")
times = []
predict_times = []
index = 0
try:
    with (OUTPUT / "detections.csv").open("w", newline="", encoding="utf-8-sig") as df, (
        OUTPUT / "timings.csv"
    ).open("w", newline="", encoding="utf-8-sig") as tf:
        detections = csv.writer(df)
        timings = csv.writer(tf)
        detections.writerow(["frame", "time_s", "class", "conf", "x1", "y1", "x2", "y2"])
        timings.writerow(["frame", "time_s", "predict_ms", "cycle_ms", "objects"])
        while True:
            sync()
            started = time.perf_counter()
            ok, raw = cap.read()
            if not ok:
                break
            frame = prepare_frame(raw)
            if frame.shape[:2] != (height, width):
                raise ValueError("Размер подготовленного кадра изменился")
            sync()
            before_predict = time.perf_counter()
            result = predict(frame)
            sync()
            predict_s = time.perf_counter() - before_predict
            boxes = result.boxes.cpu()
            annotated = result.plot()
            if writer is not None:
                writer.write(annotated)
            for cls, score, box in zip(
                boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist()
            ):
                detections.writerow(
                    [index, index / fps, model.names[int(cls)], score, *box]
                )
            cycle_s = time.perf_counter() - started
            times.append(cycle_s)
            predict_times.append(predict_s)
            timings.writerow(
                [index, index / fps, predict_s * 1000, cycle_s * 1000, len(boxes)]
            )
            index += 1
finally:
    cap.release()
    if writer is not None:
        writer.release()
if not times:
    raise RuntimeError("Нет обработанных кадров")
budget = 1.0 / fps
summary = dict(
    frames=index,
    source_fps=fps,
    imgsz=cfg["imgsz"],
    conf=cfg["conf"],
    device=str(device),
    save_video=SAVE_VIDEO,
    predict_mean_ms=float(np.mean(predict_times) * 1000),
    cycle_mean_ms=float(np.mean(times) * 1000),
    cycle_median_ms=float(np.median(times) * 1000),
    cycle_p95_ms=float(np.percentile(times, 95) * 1000),
    processing_fps=len(times) / sum(times),
    over_budget_percent=100 * sum(t > budget for t in times) / len(times),
)
(OUTPUT / "summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(summary)
