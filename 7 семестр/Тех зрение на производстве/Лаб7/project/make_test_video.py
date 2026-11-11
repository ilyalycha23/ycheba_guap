# -*- coding: utf-8 -*-
"""
Шаг 5 ЛР7: новый ролик ≥20–30 с.
Чистые RGBA-вырезки (rembg) + жёсткая альфа-вклейка как в ЛР5 (без seamlessClone).
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import cv2
import numpy as np
from preprocess import prepare_frame

ROOT = Path(__file__).resolve().parent
CUT_DIR = ROOT / "data" / "cutouts_rembg"
OUT_VIDEO = ROOT / "data" / "video" / "test_video.mp4"
IMG_DIR = ROOT / "video_test" / "images"
LAB_DIR = ROOT / "video_test" / "labels"
META = ROOT / "results" / "video_test_meta.json"

NAMES = ["wrench", "hammer", "pliers"]
W, H = 1280, 720
FPS = 15
DURATION_S = 28
N_LABEL = 36


def load_cutouts():
    cuts = {n: [] for n in NAMES}
    for p in sorted(CUT_DIR.glob("*.png")):
        for n in NAMES:
            if p.name.startswith(n):
                im = cv2.imdecode(np.fromfile(str(p), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if im is None or im.ndim < 3 or im.shape[2] < 4:
                    break
                a = im[:, :, 3]
                ys, xs = np.where(a > 25)
                if len(xs) < 40:
                    break
                im = im[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
                # жёсткая альфа
                im = im.copy()
                im[:, :, 3] = np.where(im[:, :, 3] >= 128, 255, 0).astype(np.uint8)
                cuts[n].append(im)
                break
    for n in NAMES:
        if not cuts[n]:
            raise RuntimeError(f"нет вырезок {n} в {CUT_DIR}")
        print("cutouts", n, len(cuts[n]))
    return cuts


def make_bg(kind: int, rng: np.random.Generator):
    """Фоны спокойнее (меньше зерна), инструменты остаются чёткими."""
    if kind % 5 == 0:
        base = rng.integers(155, 175, (H, W, 3), dtype=np.uint8)
        noise = rng.integers(-4, 5, (H, W, 3), dtype=np.int16)
        img = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    elif kind % 5 == 1:
        img = np.zeros((H, W, 3), np.uint8)
        for y in range(H):
            shade = int(125 + 28 * np.sin(y / 18))
            img[y, :] = (shade - 28, shade - 8, shade + 8)
    elif kind % 5 == 2:
        img = np.full((H, W, 3), 92, np.uint8)
        for x in range(0, W, 80):
            cv2.line(img, (x, 0), (x, H), (72, 72, 76), 2)
        for y in range(0, H, 120):
            cv2.line(img, (0, y), (W, y), (62, 62, 66), 2)
    elif kind % 5 == 3:
        img = np.full((H, W, 3), 52, np.uint8)
    else:
        img = np.full((H, W, 3), (205, 208, 212), np.uint8)
        for _ in range(120):
            x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
            cv2.circle(img, (x, y), int(rng.integers(1, 3)), (190, 193, 196), -1)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W * 0.5, H * 0.45
    dist = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    vignette = np.clip(1.08 - 0.35 * dist, 0.82, 1.08)[..., None]
    return np.clip(img.astype(np.float32) * vignette, 0, 255).astype(np.uint8)


def scale_rgba(img, scale):
    h, w = img.shape[:2]
    nh, nw = max(20, int(h * scale)), max(20, int(w * scale))
    return cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)


def rotate_rgba(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos), int(h * cos + w * sin)
    M[0, 2] += (nw - w) / 2
    M[1, 2] += (nh - h) / 2
    return cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


def paste_rgba(bg, overlay, x, y):
    h, w = bg.shape[:2]
    oh, ow = overlay.shape[:2]
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(w, x + ow), min(h, y + oh)
    if x2 <= x1 or y2 <= y1:
        return None
    ox1, oy1 = x1 - x, y1 - y
    ox2, oy2 = ox1 + (x2 - x1), oy1 + (y2 - y1)
    roi = overlay[oy1:oy2, ox1:ox2]
    alpha = (roi[:, :, 3:4].astype(np.float32) / 255.0)
    alpha = (alpha >= 0.5).astype(np.float32)
    bgr = roi[:, :, :3].astype(np.float32)
    dst = bg[y1:y2, x1:x2].astype(np.float32)
    bg[y1:y2, x1:x2] = (alpha * bgr + (1 - alpha) * dst).astype(np.uint8)
    a = (roi[:, :, 3] >= 128).astype(np.uint8)
    ys, xs = np.where(a > 0)
    if len(xs) == 0:
        return None
    return int(x1 + xs.min()), int(y1 + ys.min()), int(x1 + xs.max()), int(y1 + ys.max())


def to_yolo(cls, x1, y1, x2, y2):
    xc = ((x1 + x2) / 2) / W
    yc = ((y1 + y2) / 2) / H
    bw = (x2 - x1) / W
    bh = (y2 - y1) / H
    return f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}"


def imwrite_u(path: Path, img):
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])[1].tofile(str(path))


def main():
    cuts = load_cutouts()
    rng = np.random.default_rng(2031)
    py = random.Random(2031)
    n_frames = FPS * DURATION_S
    OUT_VIDEO.parent.mkdir(parents=True, exist_ok=True)
    for d in (IMG_DIR, LAB_DIR):
        if d.exists():
            for f in d.glob("*"):
                f.unlink()
        d.mkdir(parents=True, exist_ok=True)

    writer = cv2.VideoWriter(
        str(OUT_VIDEO), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H)
    )
    label_indices = sorted(set(np.linspace(8, n_frames - 10, N_LABEL, dtype=int).tolist()))
    empty_zone = set(range(n_frames - 50, n_frames - 20))
    frame_meta = []

    for i in range(n_frames):
        section = i // max(1, n_frames // 5)
        bg = make_bg(section * 2 + i // 40, rng)
        gain = float(0.94 + 0.14 * (0.5 + 0.5 * np.sin(i / 40.0)))
        if section == 3:
            gain *= 0.92
        bg = np.clip(bg.astype(np.float32) * gain, 0, 255).astype(np.uint8)

        boxes = []
        empty = (i in empty_zone and i % 2 == 0) or (i % 25 == 0)
        if not empty:
            n_obj = int(rng.integers(1, 4))
            classes = [NAMES[i % 3]] + [py.choice(NAMES) for _ in range(n_obj - 1)]
            placements = []
            for cls_name in classes[:n_obj]:
                ov = cuts[cls_name][int(rng.integers(0, len(cuts[cls_name])))].copy()
                scale = float(rng.uniform(0.55, 0.95))
                ov = scale_rgba(ov, scale)
                ang = float(rng.uniform(-35, 35) + 8 * np.sin(i / 28.0))
                ov = rotate_rgba(ov, ang)
                oh, ow = ov.shape[:2]
                x = int((0.08 + 0.70 * abs(np.sin(i / 44.0 + NAMES.index(cls_name)))) * max(1, W - ow - 20)) + 10
                y = int((0.08 + 0.70 * abs(np.cos(i / 58.0 + NAMES.index(cls_name) * 0.7))) * max(1, H - oh - 20)) + 10
                if placements and rng.random() < 0.3:
                    px1, py1, px2, py2 = placements[-1]
                    x = int(np.clip((px1 + px2) / 2 + rng.integers(-80, 80) - ow / 2, 0, max(0, W - ow - 1)))
                    y = int(np.clip((py1 + py2) / 2 + rng.integers(-60, 60) - oh / 2, 0, max(0, H - oh - 1)))
                bbox = paste_rgba(bg, ov, x, y)
                if bbox is None:
                    continue
                placements.append(bbox)
                x1, y1, x2, y2 = bbox
                pad = 2
                x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
                x2, y2 = min(W - 1, x2 + pad), min(H - 1, y2 + pad)
                boxes.append(to_yolo(NAMES.index(cls_name), x1, y1, x2, y2))

        writer.write(bg)
        if i in label_indices:
            prepared = prepare_frame(bg)
            stem = f"test_video_{i:06d}"
            imwrite_u(IMG_DIR / f"{stem}.jpg", prepared)
            (LAB_DIR / f"{stem}.txt").write_text(
                "\n".join(boxes) + ("\n" if boxes else ""), encoding="utf-8"
            )
            counts = {n: 0 for n in NAMES}
            for line in boxes:
                counts[NAMES[int(line.split()[0])]] += 1
            frame_meta.append(
                {
                    "frame": i,
                    "file": stem,
                    "n_objects": len(boxes),
                    "boxes": counts,
                    "empty": len(boxes) == 0,
                }
            )

    writer.release()
    totals = {n: 0 for n in NAMES}
    empty_n = sum(1 for m in frame_meta if m["empty"])
    for m in frame_meta:
        for n in NAMES:
            totals[n] += m["boxes"][n]
    meta = {
        "video": "data/video/test_video.mp4",
        "fps": FPS,
        "duration_s": DURATION_S,
        "frames_total": n_frames,
        "resolution": [W, H],
        "labeled_frames": len(frame_meta),
        "empty_labeled": empty_n,
        "class_boxes": totals,
        "note": "RGBA rembg-вырезки + жёсткая альфа-вклейка (без seamlessClone). conf/модель/test не менялись.",
        "frames": frame_meta,
    }
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("video", OUT_VIDEO, "frames", n_frames)
    print("labeled", len(frame_meta), "boxes", totals, "empty", empty_n)


if __name__ == "__main__":
    main()
