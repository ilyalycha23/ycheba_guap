# -*- coding: utf-8 -*-
"""Шаги 8–9: предсказания на valid, выбор модели, selected_model.json."""
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RUNS = ROOT / "runs" / "lr6"
VALID_IMG = ROOT / "dataset" / "valid" / "images"
VALID_LAB = ROOT / "dataset" / "valid" / "labels"
NAMES = ["wrench", "hammer", "pliers"]
COLS = [(92, 242, 200), (255, 107, 90), (240, 200, 90)]


def load_compare():
    rows = list(csv.DictReader((RESULTS / "lr6_compare.csv").open(encoding="utf-8-sig")))
    for r in rows:
        r["map50"] = float(r["map50"])
        r["map50_95"] = float(r["map50_95"])
        r["train_s"] = float(r["train_s"])
        r["weights_mb"] = float(r["weights_mb"])
        r["epochs"] = int(r["epochs"])
        r["imgsz"] = int(r["imgsz"])
    return rows


def choose(rows):
    a, b = rows[0], rows[1]
    diff = abs(a["map50_95"] - b["map50_95"])
    if diff <= 0.01:
        # менее затратная
        chosen = a if a["weights_mb"] <= b["weights_mb"] else b
        reason = (
            f"Разница mAP@0.5:0.95 = {diff:.4f} ≤ 0.01; "
            f"выбрана менее затратная модель {chosen['value']} "
            f"({chosen['weights_mb']} МБ, {chosen['train_s']} с)."
        )
    else:
        chosen = a if a["map50_95"] >= b["map50_95"] else b
        reason = (
            f"По правилу работы выбран опыт с большим mAP@0.5:0.95 на valid: "
            f"{chosen['run']} ({chosen['value']}) = {chosen['map50_95']:.4f} "
            f"против {a['map50_95'] if chosen is b else b['map50_95']:.4f} "
            f"(разница {diff:.4f} > 0.01)."
        )
    return chosen, reason


def yolo_boxes(label_path: Path, w: int, h: int):
    boxes = []
    for ln in label_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        c, xc, yc, bw, bh = map(float, ln.split())
        x1 = (xc - bw / 2) * w
        y1 = (yc - bh / 2) * h
        x2 = (xc + bw / 2) * w
        y2 = (yc + bh / 2) * h
        boxes.append((int(c), x1, y1, x2, y2))
    return boxes


def iou(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    return inter / (area_a + area_b - inter + 1e-9)


def analyze_image(gt, pred, iou_thr=0.5):
    """GT: (c,x1,y1,x2,y2); pred: (c,conf,x1,y1,x2,y2)."""
    matched_gt = set()
    matched_pr = set()
    correct = []
    wrong_class = []
    for pi, p in enumerate(pred):
        best_j, best_iou = -1, 0.0
        for ji, g in enumerate(gt):
            if ji in matched_gt:
                continue
            v = iou(p[2:], g[1:])
            if v > best_iou:
                best_iou, best_j = v, ji
        if best_j >= 0 and best_iou >= iou_thr:
            matched_gt.add(best_j)
            matched_pr.add(pi)
            if p[0] == gt[best_j][0]:
                correct.append((pi, best_j, best_iou))
            else:
                wrong_class.append((pi, best_j, best_iou, p[0], gt[best_j][0]))
    fp = [i for i in range(len(pred)) if i not in matched_pr]
    fn = [i for i in range(len(gt)) if i not in matched_gt]
    return correct, wrong_class, fp, fn


def draw(im, gt, pred, title=""):
    out = im.copy()
    for c, x1, y1, x2, y2 in gt:
        cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), (80, 80, 80), 2)
    for c, conf, x1, y1, x2, y2 in pred:
        color = COLS[c][::-1]
        cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        label = f"{NAMES[c]} {conf:.2f}"
        cv2.putText(
            out,
            label,
            (int(x1), max(20, int(y1) - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
        )
    if title:
        cv2.putText(out, title, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return out


def main():
    rows = load_compare()
    chosen, reason = choose(rows)
    print("chosen", chosen["run"], reason)

    pred_dir = RESULTS / "valid_predictions"
    if pred_dir.exists():
        shutil.rmtree(pred_dir)
    pred_dir.mkdir(parents=True)

    model = YOLO(chosen["weights"])
    notes = []
    conf_work = 0.25  # для визуального разбора (не порог mAP)
    for img_path in sorted(VALID_IMG.glob("*.jpg")):
        im = cv2.imdecode(np.fromfile(str(img_path), dtype=np.uint8), cv2.IMREAD_COLOR)
        h, w = im.shape[:2]
        gt = yolo_boxes(VALID_LAB / f"{img_path.stem}.txt", w, h)
        res = model.predict(
            source=im,
            imgsz=chosen["imgsz"],
            conf=conf_work,
            iou=0.7,
            verbose=False,
        )[0]
        pred = []
        if res.boxes is not None and len(res.boxes):
            for b in res.boxes:
                c = int(b.cls.item())
                conf = float(b.conf.item())
                x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
                pred.append((c, conf, x1, y1, x2, y2))
        correct, wrong_class, fp, fn = analyze_image(gt, pred)
        kinds = []
        if correct:
            kinds.append("TP")
        if fn:
            kinds.append("miss")
        if fp:
            kinds.append("extra")
        if wrong_class:
            kinds.append("wrong_class")
        note = {
            "image": img_path.name,
            "gt": len(gt),
            "pred": len(pred),
            "tp": len(correct),
            "miss": len(fn),
            "extra": len(fp),
            "wrong_class": [
                {"pred": NAMES[pc], "gt": NAMES[gc], "iou": round(iou_v, 3)}
                for _, _, iou_v, pc, gc in wrong_class
            ],
            "kinds": kinds,
        }
        notes.append(note)
        vis = draw(im, gt, pred, title=img_path.stem)
        out = pred_dir / f"{img_path.stem}_pred.jpg"
        ok, buf = cv2.imencode(".jpg", vis, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        buf.tofile(str(out))

    # copy curves
    for tag in ("a", "b"):
        src = RUNS / f"v09_{tag}" / "results.png"
        if src.exists():
            shutil.copy2(src, RESULTS / f"results_v09_{tag}.png")
        confm = RUNS / f"v09_{tag}_valid" / "confusion_matrix.png"
        if confm.exists():
            shutil.copy2(confm, RESULTS / f"confusion_v09_{tag}.png")

    env = json.loads((RESULTS / "environment.json").read_text(encoding="utf-8"))
    stats = json.loads((RESULTS / "dataset_stats.json").read_text(encoding="utf-8"))
    args = yaml.safe_load((RUNS / chosen["run"] / "args.yaml").read_text(encoding="utf-8"))
    data_yaml = yaml.safe_load((ROOT / "dataset" / "data.yaml").read_text(encoding="utf-8"))

    selected = {
        "weights": f"runs/lr6/{chosen['run']}/weights/best.pt",
        "imgsz": chosen["imgsz"],
        "dataset_version": "ЛР5_lab5_tools_scene_split_v1 (Roboflow ilyalycha_4321 / локальный экспорт yolov8, split по роликам)",
        "preprocessing": "prepare_frame: без изменений (BGR uint8). Разметка ЛР5 выполнена на кадрах без внешней коррекции яркости/фильтрации.",
        "classes": data_yaml["names"],
        "chosen_run": chosen["run"],
        "chosen_source": chosen["value"],
        "map50": chosen["map50"],
        "map50_95": chosen["map50_95"],
        "train_s": chosen["train_s"],
        "weights_mb": chosen["weights_mb"],
        "selection_rule": reason,
        "splits": stats,
        "environment": env,
        "args_yaml_key_fields": {
            k: args.get(k)
            for k in [
                "model",
                "epochs",
                "imgsz",
                "batch",
                "optimizer",
                "lr0",
                "seed",
                "device",
                "patience",
                "mosaic",
                "fliplr",
                "hsv_v",
            ]
        },
        "compare": rows,
        "valid_notes": notes,
        "valid_pred_conf": conf_work,
    }
    (RESULTS / "selected_model.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (RESULTS / "selection_reason.txt").write_text(reason, encoding="utf-8")
    print(json.dumps(notes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
