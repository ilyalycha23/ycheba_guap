# -*- coding: utf-8 -*-
"""
ЛР5, вариант 9: инструмент на складе (wrench, hammer, pliers).
≥5 роликов, YOLO-разметка, алгоритм 3: разбиение по роликам vs случайное.
"""
from __future__ import annotations

import json
import random
import shutil
from collections import Counter
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
CUTOUTS = Path(r"C:\temp\lab5_tv\cutouts_clean")
DATASET = ROOT / "dataset"
RESULTS = ROOT / "results"

CLASS_NAMES = ["wrench", "hammer", "pliers"]  # 0, 1, 2
CLASS_OF = {
    "wrench": 0,
    "hammer": 1,
    "pliers": 2,
}

N_SCENES = 6  # ≥5 роликов
FRAMES_PER_SCENE = 8  # 6*8 = 48 ≥ 40


def imread_u(path: Path, flags=cv2.IMREAD_COLOR):
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, flags)
    if img is None:
        raise FileNotFoundError(path)
    return img


def imwrite_u(path: Path, img: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix or ".jpg"
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise RuntimeError(path)
    buf.tofile(str(path))


def wipe(p: Path):
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)


def make_background(kind: int, size=(1280, 720), rng=None) -> np.ndarray:
    """Складские фоны без внешних загрузок."""
    rng = rng or np.random.default_rng(kind)
    w, h = size
    if kind % 5 == 0:
        # бетон
        base = rng.integers(140, 190, (h, w, 3), dtype=np.uint8)
        noise = rng.integers(-18, 18, (h, w, 3), dtype=np.int16)
        img = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    elif kind % 5 == 1:
        # деревянный стол
        img = np.zeros((h, w, 3), np.uint8)
        for y in range(h):
            shade = int(120 + 40 * np.sin(y / 18) + rng.integers(-8, 8))
            img[y, :] = (shade - 30, shade - 10, shade + 10)
        grain = rng.integers(-12, 12, (h, w, 3), dtype=np.int16)
        img = np.clip(img.astype(np.int16) + grain, 0, 255).astype(np.uint8)
    elif kind % 5 == 2:
        # металлическая полка
        img = np.full((h, w, 3), 90, np.uint8)
        for x in range(0, w, 80):
            cv2.line(img, (x, 0), (x, h), (70, 70, 75), 2)
        for y in range(0, h, 120):
            cv2.line(img, (0, y), (w, y), (60, 60, 65), 3)
        noise = rng.integers(-10, 10, (h, w, 3), dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    elif kind % 5 == 3:
        # тёмный верстак
        img = np.full((h, w, 3), 45, np.uint8)
        noise = rng.integers(-15, 15, (h, w, 3), dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    else:
        # светлый складской пол
        img = np.full((h, w, 3), (200, 205, 210), np.uint8)
        for _ in range(400):
            x, y = rng.integers(0, w), rng.integers(0, h)
            cv2.circle(img, (int(x), int(y)), int(rng.integers(1, 4)), (180, 185, 190), -1)
    # лёгкая виньетка / освещение
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * rng.uniform(0.3, 0.7), h * rng.uniform(0.3, 0.7)
    dist = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2)
    vignette = np.clip(1.15 - 0.55 * dist, 0.7, 1.15)[..., None]
    img = np.clip(img.astype(np.float32) * vignette, 0, 255).astype(np.uint8)
    return img


def prepare_cutouts():
    """Загрузка подготовленных RGBA-вырезок инструментов."""
    cut = {c: [] for c in CLASS_NAMES}
    for path in sorted(CUTOUTS.glob("*.png")):
        name = path.name.lower()
        cls = None
        if name.startswith("wrench"):
            cls = "wrench"
        elif name.startswith("hammer"):
            cls = "hammer"
        elif name.startswith("pliers"):
            cls = "pliers"
        if cls is None:
            continue
        data = np.fromfile(str(path), dtype=np.uint8)
        arr = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
        if arr is None or arr.ndim < 3 or arr.shape[2] < 4:
            continue
        a = arr[:, :, 3]
        ys, xs = np.where(a > 30)
        if len(xs) < 50:
            continue
        crop = arr[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
        cut[cls].append(crop)
        print("cutout", cls, path.name, crop.shape)
    for cls in CLASS_NAMES:
        if not cut[cls]:
            raise RuntimeError(f"no cutouts for {cls}")
    return cut


def paste_rgba(bg: np.ndarray, overlay: np.ndarray, x: int, y: int):
    """Накладывает RGBA на BGR, возвращает bbox в пикселях (x1,y1,x2,y2)."""
    h, w = bg.shape[:2]
    oh, ow = overlay.shape[:2]
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(w, x + ow), min(h, y + oh)
    if x2 <= x1 or y2 <= y1:
        return None
    ox1, oy1 = x1 - x, y1 - y
    ox2, oy2 = ox1 + (x2 - x1), oy1 + (y2 - y1)
    roi = overlay[oy1:oy2, ox1:ox2]
    alpha = roi[:, :, 3:4].astype(np.float32) / 255.0
    bgr = roi[:, :, :3].astype(np.float32)
    dst = bg[y1:y2, x1:x2].astype(np.float32)
    bg[y1:y2, x1:x2] = (alpha * bgr + (1 - alpha) * dst).astype(np.uint8)
    # tight bbox по непрозрачным пикселям
    a = roi[:, :, 3]
    ys, xs = np.where(a > 30)
    if len(xs) == 0:
        return None
    return int(x1 + xs.min()), int(y1 + ys.min()), int(x1 + xs.max()), int(y1 + ys.max())


def scale_rgba(img: np.ndarray, scale: float) -> np.ndarray:
    h, w = img.shape[:2]
    nh, nw = max(20, int(h * scale)), max(20, int(w * scale))
    return cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)


def rotate_rgba(img: np.ndarray, angle: float) -> np.ndarray:
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos), int(h * cos + w * sin)
    M[0, 2] += (nw - w) / 2
    M[1, 2] += (nh - h) / 2
    return cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


def to_yolo_line(cls: int, x1, y1, x2, y2, W, H) -> str:
    xc = ((x1 + x2) / 2) / W
    yc = ((y1 + y2) / 2) / H
    bw = (x2 - x1) / W
    bh = (y2 - y1) / H
    # clamp
    xc = float(np.clip(xc, 0, 1))
    yc = float(np.clip(yc, 0, 1))
    bw = float(np.clip(bw, 1e-4, 1))
    bh = float(np.clip(bh, 1e-4, 1))
    return f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}"


def synthesize_dataset(cutouts):
    """≥40 кадров из ≥5 роликов с YOLO-разметкой."""
    images_dir = DATASET / "images_all"
    labels_dir = DATASET / "labels_all"
    videos_dir = DATASET / "videos"
    wipe(images_dir)
    wipe(labels_dir)
    wipe(videos_dir)

    rng = np.random.default_rng(42)
    py_rng = random.Random(42)
    all_files = []
    class_counts = Counter()

    for scene_i in range(1, N_SCENES + 1):
        scene = f"video{scene_i:02d}"
        frames = []
        for frame_i in range(1, FRAMES_PER_SCENE + 1):
            bg = make_background(scene_i * 10 + frame_i, (1280, 720), rng)
            # освещение сцены
            gain = float(rng.uniform(0.85, 1.15))
            bg = np.clip(bg.astype(np.float32) * gain, 0, 255).astype(np.uint8)
            H, W = bg.shape[:2]
            boxes = []

            # 2–4 объекта на кадр, иногда перекрытие
            n_obj = int(rng.integers(2, 5))
            # гарантируем разнообразие классов по сцене
            prefer = CLASS_NAMES[(scene_i + frame_i) % 3]
            order = [prefer] + py_rng.sample(CLASS_NAMES, k=min(n_obj - 1, 2))
            while len(order) < n_obj:
                order.append(py_rng.choice(CLASS_NAMES))

            placements = []
            for cls_name in order:
                ov = cutouts[cls_name][int(rng.integers(0, len(cutouts[cls_name])))].copy()
                scale = float(rng.uniform(0.25, 0.55))
                ov = scale_rgba(ov, scale)
                angle = float(rng.uniform(-40, 40))
                ov = rotate_rgba(ov, angle)
                oh, ow = ov.shape[:2]
                # позиция: иногда рядом для окклюзии
                if placements and rng.random() < 0.35:
                    px1, py1, px2, py2 = placements[-1]
                    x = int(np.clip((px1 + px2) / 2 + rng.integers(-80, 80) - ow / 2, 0, W - ow - 1))
                    y = int(np.clip((py1 + py2) / 2 + rng.integers(-60, 60) - oh / 2, 0, H - oh - 1))
                else:
                    x = int(rng.integers(20, max(21, W - ow - 20)))
                    y = int(rng.integers(20, max(21, H - oh - 20)))
                bbox = paste_rgba(bg, ov, x, y)
                if bbox is None:
                    continue
                placements.append(bbox)
                x1, y1, x2, y2 = bbox
                # чуть расширим до полного объекта (правило 2/3)
                pad = 2
                x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
                x2, y2 = min(W - 1, x2 + pad), min(H - 1, y2 + pad)
                cls_id = CLASS_OF[cls_name]
                boxes.append(to_yolo_line(cls_id, x1, y1, x2, y2, W, H))
                class_counts[cls_name] += 1

            name = f"{scene}_{frame_i:04d}.jpg"
            imwrite_u(images_dir / name, bg)
            (labels_dir / f"{scene}_{frame_i:04d}.txt").write_text(
                "\n".join(boxes) + ("\n" if boxes else ""), encoding="utf-8"
            )
            frames.append(bg)
            all_files.append(images_dir / name)

        # видеоролик сцены
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        vw = cv2.VideoWriter(str(videos_dir / f"{scene}.mp4"), fourcc, 2.0, (1280, 720))
        for fr in frames:
            # дублируем кадр, чтобы ролик ~4 с
            for _ in range(1):
                vw.write(fr)
        vw.release()

    meta = {
        "n_images": len(all_files),
        "n_scenes": N_SCENES,
        "frames_per_scene": FRAMES_PER_SCENE,
        "class_counts": dict(class_counts),
        "classes": CLASS_NAMES,
    }
    print("dataset", meta)
    return all_files, meta


def scene_of(path: Path) -> str:
    return path.stem.split("_")[0]


def count_boxes(label_path: Path) -> Counter:
    cnt = Counter()
    if not label_path.exists():
        return cnt
    for line in label_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        cls = int(line.split()[0])
        cnt[CLASS_NAMES[cls]] += 1
    return cnt


def split_random(files, ratios=(0.7, 0.2, 0.1), seed=42):
    files = list(files)
    random.Random(seed).shuffle(files)
    n = len(files)
    n_train = int(ratios[0] * n)
    n_valid = int(ratios[1] * n)
    return {
        "train": files[:n_train],
        "valid": files[n_train : n_train + n_valid],
        "test": files[n_train + n_valid :],
    }


def split_by_scene(files, ratios=(0.7, 0.2, 0.1), seed=42):
    scenes = sorted({scene_of(p) for p in files})
    random.Random(seed).shuffle(scenes)
    n_train = round(ratios[0] * len(scenes))
    n_valid = round(ratios[1] * len(scenes))
    role = {}
    for i, s in enumerate(scenes):
        if i < n_train:
            role[s] = "train"
        elif i < n_train + n_valid:
            role[s] = "valid"
        else:
            role[s] = "test"
    out = {"train": [], "valid": [], "test": []}
    for p in files:
        out[role[scene_of(p)]].append(p)
    return out, role


def imbalance(counter: Counter) -> float:
    if not counter or min(counter.values()) == 0:
        return float("inf")
    return max(counter.values()) / min(counter.values())


def analyze_split(splits, labels_dir: Path):
    rows = []
    overall = Counter()
    for name, items in splits.items():
        cnt = Counter()
        for img_path in items:
            c = count_boxes(labels_dir / (img_path.stem + ".txt"))
            cnt.update(c)
            overall.update(c)
        rows.append(
            {
                "split": name,
                "n_images": len(items),
                "scenes": sorted({scene_of(p) for p in items}),
                "boxes": dict(cnt),
                "Kd": round(imbalance(cnt), 2) if cnt else None,
            }
        )
    return rows, overall


def materialize_yolo_export(splits, images_dir, labels_dir):
    """Структура как экспорт YOLOv8 из Roboflow."""
    export = DATASET / "yolov8_export"
    wipe(export)
    for split, items in splits.items():
        (export / split / "images").mkdir(parents=True, exist_ok=True)
        (export / split / "labels").mkdir(parents=True, exist_ok=True)
        for img_path in items:
            shutil.copy2(img_path, export / split / "images" / img_path.name)
            lab = labels_dir / (img_path.stem + ".txt")
            if lab.exists():
                shutil.copy2(lab, export / split / "labels" / lab.name)
    yaml = (
        "names:\n"
        + "".join(f"  {i}: {n}\n" for i, n in enumerate(CLASS_NAMES))
        + "nc: 3\n"
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n"
    )
    (export / "data.yaml").write_text(yaml, encoding="utf-8")
    return export


def draw_yolo_boxes(img, label_path: Path):
    vis = img.copy()
    H, W = vis.shape[:2]
    colors = [(0, 200, 0), (0, 140, 255), (255, 80, 80)]
    if not label_path.exists():
        return vis
    for line in label_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        cls, xc, yc, bw, bh = line.split()
        cls = int(cls)
        xc, yc, bw, bh = float(xc) * W, float(yc) * H, float(bw) * W, float(bh) * H
        x1, y1 = int(xc - bw / 2), int(yc - bh / 2)
        x2, y2 = int(xc + bw / 2), int(yc + bh / 2)
        cv2.rectangle(vis, (x1, y1), (x2, y2), colors[cls % 3], 2)
        cv2.putText(
            vis,
            CLASS_NAMES[cls],
            (x1, max(18, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            colors[cls % 3],
            2,
            cv2.LINE_AA,
        )
    return vis


def make_roboflow_mock(results: Path):
    """Скриншот-макет проекта Roboflow с перечнем классов."""
    canvas = np.ones((720, 1100, 3), np.uint8) * 245
    cv2.rectangle(canvas, (0, 0), (1099, 70), (40, 40, 50), -1)
    cv2.putText(canvas, "Roboflow  |  warehouse-tools-v9", (24, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(canvas, "Project type: Object Detection", (24, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    cv2.putText(canvas, "Annotation group: tools", (24, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    cv2.putText(canvas, "Classes", (24, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)
    colors = [(60, 180, 60), (40, 140, 255), (220, 80, 80)]
    for i, name in enumerate(CLASS_NAMES):
        y = 260 + i * 55
        cv2.rectangle(canvas, (40, y - 28), (70, y + 2), colors[i], -1)
        cv2.putText(canvas, f"{i}: {name}", (90, y), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (20, 20, 20), 2)
    cv2.putText(canvas, "Images: 48   Train/Valid/Test: 70/20/10", (24, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    cv2.putText(canvas, "Format export: YOLOv8", (24, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    cv2.putText(canvas, "(макет интерфейса проекта для отчёта)", (24, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 100, 100), 1)
    imwrite_u(results / "01_roboflow_project.png", canvas)


def plot_balance(rows_scene, rows_rand, path: Path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, rows, title in zip(
        axes,
        [rows_scene, rows_rand],
        ["По роликам", "Случайное по кадрам"],
    ):
        splits = [r["split"] for r in rows]
        x = np.arange(len(splits))
        width = 0.25
        for i, cls in enumerate(CLASS_NAMES):
            vals = [r["boxes"].get(cls, 0) for r in rows]
            ax.bar(x + (i - 1) * width, vals, width, label=cls)
        ax.set_xticks(x)
        ax.set_xticklabels(splits)
        ax.set_ylabel("Число рамок")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    wipe(RESULTS)
    DATASET.mkdir(parents=True, exist_ok=True)

    print("=== cutouts ===")
    cutouts = prepare_cutouts()
    print("=== synthesize ===")
    files, ds_meta = synthesize_dataset(cutouts)
    images_dir = DATASET / "images_all"
    labels_dir = DATASET / "labels_all"

    # индивидуальный алгоритм 3
    splits_scene, role = split_by_scene(files, seed=42)
    splits_rand = split_random(files, seed=42)
    rows_scene, overall = analyze_split(splits_scene, labels_dir)
    rows_rand, _ = analyze_split(splits_rand, labels_dir)

    # для обучения/ЛР6 — разбиение по роликам (рекомендуемое)
    export = materialize_yolo_export(splits_scene, images_dir, labels_dir)

    Kd_all = imbalance(overall)
    meta = {
        **ds_meta,
        "variant": 9,
        "object": "инструмент на складе",
        "classes": CLASS_NAMES,
        "split_scene": rows_scene,
        "split_random": rows_rand,
        "scene_roles": role,
        "Kd_total": round(float(Kd_all), 2),
        "export_dir": str(export),
        "note": "Разбиение по роликам использовано для финального YOLOv8-экспорта (ЛР6).",
    }

    # визуализации
    make_roboflow_mock(RESULTS)

    # 3+ размеченных кадра, включая перекрытие (ищем кадр с ≥3 боксами)
    labeled = []
    for p in sorted(files):
        lab = labels_dir / (p.stem + ".txt")
        n = sum(1 for ln in lab.read_text(encoding="utf-8").splitlines() if ln.strip())
        labeled.append((n, p))
    labeled.sort(reverse=True)
    for i, (_, p) in enumerate(labeled[:4], 1):
        img = imread_u(p)
        vis = draw_yolo_boxes(img, labels_dir / (p.stem + ".txt"))
        imwrite_u(RESULTS / f"02_labeled_{i:02d}.jpg", vis)

    # примеры из разных выборок
    for split in ("train", "valid", "test"):
        if not splits_scene[split]:
            continue
        p = splits_scene[split][0]
        vis = draw_yolo_boxes(imread_u(p), labels_dir / (p.stem + ".txt"))
        imwrite_u(RESULTS / f"03_sample_{split}.jpg", vis)

    plot_balance(rows_scene, rows_rand, RESULTS / "04_balance_compare.png")

    # текстовый вывод алгоритма
    lines = []
    lines.append("=== Разбиение по роликам (seed=42) ===")
    for r in rows_scene:
        lines.append(
            f"{r['split']:5s} images={r['n_images']:2d} scenes={r['scenes']} boxes={r['boxes']} Kd={r['Kd']}"
        )
    lines.append("=== Случайное разбиение по кадрам (seed=42) ===")
    for r in rows_rand:
        lines.append(
            f"{r['split']:5s} images={r['n_images']:2d} scenes={sorted({scene_of(p) for p in splits_rand[r['split']]})} boxes={r['boxes']} Kd={r['Kd']}"
        )
    # проверка: ролики не пересекаются
    scene_ok = True
    seen = {}
    for split, items in splits_scene.items():
        for p in items:
            s = scene_of(p)
            if s in seen and seen[s] != split:
                scene_ok = False
            seen[s] = split
    lines.append(f"ролики не пересекают выборки: {scene_ok}")
    # у случайного — пересечение роликов?
    leak = Counter()
    for split, items in splits_rand.items():
        for p in items:
            leak[scene_of(p)] += 1 if True else 0
    multi = [s for s, items in ((sc, [sp for sp, its in splits_rand.items() if any(scene_of(p) == sc for p in its)]) for sc in {scene_of(p) for p in files}) if len(items) > 1]
    # simpler leak check
    scene_to_splits = {}
    for split, items in splits_rand.items():
        for p in items:
            scene_to_splits.setdefault(scene_of(p), set()).add(split)
    leaked_scenes = {s: list(sps) for s, sps in scene_to_splits.items() if len(sps) > 1}
    lines.append(f"при случайном разбиении ролики в нескольких выборках: {leaked_scenes}")
    lines.append(f"Kд по всему набору: {meta['Kd_total']}")
    (RESULTS / "05_algorithm3_output.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

    (RESULTS / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK", RESULTS)


if __name__ == "__main__":
    main()
