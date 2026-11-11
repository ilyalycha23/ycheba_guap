# -*- coding: utf-8 -*-
"""Шаг 9: ≥5 кадров с разбором TP/пропусков/ложных рамок."""
from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
import torch
from ultralytics import YOLO
from evaluate_frames import iou, read_truth

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "error_examples"
NAMES = ["wrench", "hammer", "pliers"]
COLS = [(92, 242, 200), (255, 107, 90), (240, 200, 90)]


def main():
    cfg = json.loads((ROOT / "results" / "lr7_mode.json").read_text(encoding="utf-8"))
    device = 0 if torch.cuda.is_available() else "cpu"
    model = YOLO(cfg["weights"])
    OUT.mkdir(parents=True, exist_ok=True)
    notes = []
    # prefer video_test diversity, then test
    pools = [
        (ROOT / "video_test" / "images", ROOT / "video_test" / "labels"),
        (ROOT / "dataset" / "test" / "images", ROOT / "dataset" / "test" / "labels"),
    ]
    collected = {"TP": [], "miss": [], "extra": [], "wrong_class": []}
    for img_dir, lab_dir in pools:
        for path in sorted(img_dir.glob("*.jpg")):
            im = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
            h, w = im.shape[:2]
            truth = read_truth(lab_dir / f"{path.stem}.txt", w, h, len(model.names))
            res = model.predict(
                im,
                imgsz=cfg["imgsz"],
                conf=cfg["conf"],
                iou=cfg["nms_iou"],
                device=device,
                verbose=False,
            )[0]
            boxes = res.boxes.cpu()
            pred = [
                (int(c), float(s), box)
                for c, s, box in zip(boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist())
            ]
            used = set()
            tp = fp = 0
            wrong = 0
            vis = im.copy()
            for c, box in truth:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(vis, (x1, y1), (x2, y2), (90, 90, 90), 2)
            for c, s, box in sorted(pred, key=lambda x: -x[1]):
                candidates = [
                    (iou(box, other), j)
                    for j, (lab, other) in enumerate(truth)
                    if j not in used and lab == c
                ]
                overlap, j = max(candidates, default=(0.0, -1))
                color = COLS[c][::-1]
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    vis,
                    f"{NAMES[c]} {s:.2f}",
                    (x1, max(18, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    color,
                    2,
                )
                if j >= 0 and overlap >= cfg["match_iou"]:
                    used.add(j)
                    tp += 1
                else:
                    # check class confusion
                    cand2 = [
                        (iou(box, other), j2, lab)
                        for j2, (lab, other) in enumerate(truth)
                        if j2 not in used
                    ]
                    if cand2:
                        ov2, j2, lab = max(cand2)
                        if ov2 >= cfg["match_iou"] and lab != c:
                            wrong += 1
                    fp += 1
            fn = len(truth) - len(used)
            kinds = []
            if tp:
                kinds.append("TP")
            if fn:
                kinds.append("miss")
            if fp:
                kinds.append("extra")
            if wrong:
                kinds.append("wrong_class")
            note = {
                "image": path.name,
                "source": str(img_dir.name),
                "TP": tp,
                "FP": fp,
                "FN": fn,
                "wrong_class": wrong,
                "kinds": kinds,
            }
            for k in kinds:
                if len(collected[k]) < 3:
                    collected[k].append((note, vis))
            notes.append(note)

    # pick ≥5: prefer miss/extra/TP
    chosen = []
    for key in ("miss", "extra", "wrong_class", "TP"):
        for item in collected[key]:
            if item[0]["image"] not in [c[0]["image"] for c in chosen]:
                chosen.append(item)
            if len(chosen) >= 5:
                break
        if len(chosen) >= 5:
            break
    for i, (note, vis) in enumerate(chosen, 1):
        out = OUT / f"ex{i:02d}_{Path(note['image']).stem}.jpg"
        cv2.imencode(".jpg", vis, [int(cv2.IMWRITE_JPEG_QUALITY), 92])[1].tofile(str(out))
        note["file"] = out.name
    (OUT / "notes.json").write_text(
        json.dumps({"selected": [c[0] for c in chosen], "all": notes}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("saved", len(chosen), "examples")


if __name__ == "__main__":
    main()
