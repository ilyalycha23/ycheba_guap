# -*- coding: utf-8 -*-
"""Шаг 2 ЛР7: сопоставление рамок, TP/FP/FN, P/R/F1."""
from pathlib import Path
import cv2


def iou(a, b):
    width = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = width * height
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - intersection
    return intersection / union if union > 0 else 0.0


def match_counts(truth, predicted, match_iou=0.5):
    used = set()
    tp = 0
    for cls, confidence, box in sorted(predicted, key=lambda item: item[1], reverse=True):
        candidates = [
            (iou(box, other), index)
            for index, (label, other) in enumerate(truth)
            if index not in used and label == cls
        ]
        overlap, index = max(candidates, default=(0.0, -1))
        if index >= 0 and overlap >= match_iou:
            used.add(index)
            tp += 1
    return tp, len(predicted) - tp, len(truth) - tp


def scores(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * tp / (2 * tp + fp + fn) if tp + fn else None
    return dict(TP=tp, FP=fp, FN=fn, P=precision, R=recall, F1=f1)


def read_truth(path, width, height, n_classes):
    truth = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 5:
            raise ValueError(f"Нужна рамочная разметка: {path}")
        cls = int(parts[0])
        xc, yc, bw, bh = map(float, parts[1:])
        if not 0 <= cls < n_classes or min(bw, bh) <= 0:
            raise ValueError(f"Некорректная разметка: {path}")
        box = [
            (xc - bw / 2) * width,
            (yc - bh / 2) * height,
            (xc + bw / 2) * width,
            (yc + bh / 2) * height,
        ]
        truth.append((cls, box))
    return truth


def evaluate(
    model,
    image_dir,
    label_dir,
    conf,
    size,
    device="cpu",
    match_iou=0.5,
    transform=None,
):
    extensions = {".jpg", ".jpeg", ".png", ".bmp"}
    files = [p for p in sorted(Path(image_dir).iterdir()) if p.suffix.lower() in extensions]
    if not files:
        raise ValueError("Нет изображений для оценки")
    counts = {cls: [0, 0, 0] for cls in model.names}
    for path in files:
        image = cv2.imread(str(path))
        if image is None:
            raise ValueError(f"Не читается изображение: {path}")
        height, width = image.shape[:2]
        label = Path(label_dir) / (path.stem + ".txt")
        truth = read_truth(label, width, height, len(model.names))
        if transform is not None:
            image = transform(image)
            if image.shape[:2] != (height, width):
                raise ValueError("Преобразование изменило геометрию")
        result = model.predict(
            image,
            imgsz=size,
            conf=conf,
            iou=0.7,
            device=device,
            rect=False,
            verbose=False,
        )[0]
        boxes = result.boxes.cpu()
        predicted = [
            (int(cls), float(score), box)
            for cls, score, box in zip(
                boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist()
            )
        ]
        for cls in counts:
            gt = [(c, b) for c, b in truth if c == cls]
            pr = [(c, s, b) for c, s, b in predicted if c == cls]
            values = match_counts(gt, pr, match_iou)
            counts[cls] = [a + b for a, b in zip(counts[cls], values)]
    total = [sum(values[i] for values in counts.values()) for i in range(3)]
    per_class = {model.names[cls]: scores(*values) for cls, values in counts.items()}
    return dict(images=len(files), **scores(*total), classes=per_class)


def self_check_match_counts():
    """Три простых случая из методички: (TP, FP, FN)."""
    box = [10.0, 10.0, 50.0, 50.0]
    # 1) одна правильная рамка
    assert match_counts([(0, box)], [(0, 0.9, box)]) == (1, 0, 0)
    # 2) две одинаковые рамки одного объекта
    assert match_counts([(0, box)], [(0, 0.9, box), (0, 0.8, box)]) == (1, 1, 0)
    # 3) рамка с неверным классом
    assert match_counts([(0, box)], [(1, 0.9, box)]) == (0, 1, 1)
    print("match_counts self-check OK:", (1, 0, 0), (1, 1, 0), (0, 1, 1))


if __name__ == "__main__":
    self_check_match_counts()
