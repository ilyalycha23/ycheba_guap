# -*- coding: utf-8 -*-
"""Шаг 6 ЛР6: два сопоставимых опыта обучения (вариант 9 — YOLOv8n vs YOLOv8s)."""
from pathlib import Path
import csv
import json
import random
import time
import numpy as np
import torch
from ultralytics import YOLO

VARIANT = 9  # свой номер варианта
CASES = {
    1: ("imgsz", 416, 640),
    2: ("imgsz", 640, 960),
    3: ("epochs", 20, 40),
    4: ("freeze", 0, 10),
    5: ("hsv_v", 0.0, 0.3),
    6: ("fliplr", 0.0, 0.5),
    7: ("degrees", 0.0, 10.0),
    8: ("scale", 0.0, 0.3),
    9: ("model", "yolov8n.pt", "yolov8s.pt"),
    10: ("model", "yolov8n.pt", "yolov8n.yaml"),
}


def main():
    device = 0 if torch.cuda.is_available() else "cpu"
    root = Path.cwd()
    project = root / "runs" / "lr6"
    output = root / "results"
    output.mkdir(exist_ok=True)
    data = root / "dataset" / "data.yaml"
    common = dict(
        data=str(data),
        epochs=40,
        imgsz=640,
        batch=4,
        device=device,
        workers=0,
        seed=42,
        deterministic=True,
        amp=False,
        patience=0,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,
        freeze=0,
        mosaic=0.0,
        mixup=0.0,
        hsv_h=0.0,
        hsv_s=0.0,
        hsv_v=0.0,
        degrees=0.0,
        translate=0.0,
        scale=0.0,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.0,
        close_mosaic=0,
        plots=True,
        save=True,
        exist_ok=False,
    )
    factor, value_a, value_b = CASES[VARIANT]
    rows = []
    for tag, value in (("a", value_a), ("b", value_b)):
        name = f"v{VARIANT:02d}_{tag}"
        if (project / name).exists():
            raise FileExistsError(f"Каталог уже существует: {name}")
        random.seed(42)
        np.random.seed(42)
        torch.manual_seed(42)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(42)
        cfg = common.copy()
        source = "yolov8n.pt"
        if factor == "model":
            source = value
        else:
            cfg[factor] = value
        model = YOLO(source)
        started = time.perf_counter()
        model.train(project=str(project), name=name, **cfg)
        train_s = time.perf_counter() - started
        run = Path(model.trainer.save_dir)
        weights = run / "weights" / "best.pt"
        best = YOLO(str(weights))
        metrics = best.val(
            data=str(data),
            split="val",
            imgsz=cfg["imgsz"],
            batch=1,
            device=device,
            workers=0,
            conf=0.001,
            iou=0.7,
            plots=True,
            project=str(project),
            name=name + "_valid",
        )
        row = dict(
            run=name,
            factor=factor,
            value=value,
            source=source,
            imgsz=cfg["imgsz"],
            epochs=cfg["epochs"],
            train_s=round(train_s, 2),
            map50=float(metrics.box.map50),
            map50_95=float(metrics.box.map),
            weights_mb=round(weights.stat().st_size / 1e6, 3),
            weights=str(weights),
        )
        rows.append(row)
        (output / (name + ".json")).write_text(
            json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    with (output / "lr6_compare.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(rows)


if __name__ == "__main__":
    main()
