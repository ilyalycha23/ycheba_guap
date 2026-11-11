# -*- coding: utf-8 -*-
"""Unique 1920x1080 slide canvases; YOLO boxes redrawn after crop (no drift)."""
from __future__ import annotations

import hashlib
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "assets"
SL = ROOT / "assets" / "slides"
GEN = Path(r"C:\Users\ilyal\.cursor\projects\d-ycheba-guap-7\assets")
IMG = Path(r"D:\ycheba_guap\7 семестр\Тех зрение на производстве\Лаб5\project\dataset\images_all")
LAB = Path(r"D:\ycheba_guap\7 семестр\Тех зрение на производстве\Лаб5\project\dataset\labels_all")
CUT = Path(r"C:\temp\lab5_tv\cutouts_clean")

SL.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
NAMES = ["wrench", "hammer", "pliers"]
COLS = [(92, 242, 200), (255, 107, 90), (240, 200, 90)]  # RGB


def read(p: Path):
    im = cv2.imdecode(np.fromfile(str(p), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if im is None:
        raise RuntimeError(p)
    return im


def write(p: Path, im):
    ok, buf = cv2.imencode(".jpg", im, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    buf.tofile(str(p))


def cover(im, tw=W, th=H):
    h, w = im.shape[:2]
    scale = max(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    im2 = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA)
    x = max(0, (nw - tw) // 2)
    y = max(0, (nh - th) // 2)
    return im2[y : y + th, x : x + tw].copy()


def bottom_scrim(im, start=0.58, strength=0.92):
    out = im.astype(np.float32)
    h = out.shape[0]
    y0 = int(h * start)
    for i, y in enumerate(range(y0, h)):
        a = strength * ((i + 1) / max(1, h - y0))
        out[y] *= 1 - a
    return np.clip(out, 0, 255).astype(np.uint8)


def parse_labels(stem: str):
    rows = []
    for line in (LAB / f"{stem}.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c, xc, yc, bw, bh = map(float, line.split())
        rows.append((int(c), xc, yc, bw, bh))
    return rows


def pick_best_frame():
    """Prefer all 3 classes, centered, non-tiny, non-duplicate-heavy."""
    best, best_score = "video02_0007", -1e9
    for lp in sorted(LAB.glob("*.txt")):
        rows = parse_labels(lp.stem)
        if len(rows) < 2:
            continue
        classes = {r[0] for r in rows}
        xs, ys = [], []
        for c, xc, yc, bw, bh in rows:
            xs += [xc - bw / 2, xc + bw / 2]
            ys += [yc - bh / 2, yc + bh / 2]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        span = (max(xs) - min(xs)) * (max(ys) - min(ys))
        # penalize duplicate same-class piles
        dup_pen = max(0, len(rows) - len(classes)) * 6
        score = len(classes) * 20 + span * 25 - abs(cx - 0.5) * 35 - abs(cy - 0.5) * 35 - dup_pen
        if len(classes) == 3:
            score += 25
        if score > best_score:
            best_score, best = score, lp.stem
    return best


def crop_around_boxes(im, rows, pad=0.12, tw=W, th=H):
    """Zoom to annotation cluster, then cover-fit to target size. Returns image + remapped rows in pixel coords."""
    h0, w0 = im.shape[:2]
    xs, ys = [], []
    for c, xc, yc, bw, bh in rows:
        xs += [xc - bw / 2, xc + bw / 2]
        ys += [yc - bh / 2, yc + bh / 2]
    x1 = max(0.0, min(xs) - pad)
    y1 = max(0.0, min(ys) - pad)
    x2 = min(1.0, max(xs) + pad)
    y2 = min(1.0, max(ys) + pad)
    # expand crop to target aspect so cover barely trims
    aspect = tw / th
    cw, ch = x2 - x1, y2 - y1
    if cw / ch < aspect:
        need = ch * aspect
        mid = (x1 + x2) / 2
        x1, x2 = mid - need / 2, mid + need / 2
        if x1 < 0:
            x2 -= x1
            x1 = 0
        if x2 > 1:
            x1 -= x2 - 1
            x2 = 1
    else:
        need = cw / aspect
        mid = (y1 + y2) / 2
        y1, y2 = mid - need / 2, mid + need / 2
        if y1 < 0:
            y2 -= y1
            y1 = 0
        if y2 > 1:
            y1 -= y2 - 1
            y2 = 1
    x1, y1 = max(0.0, x1), max(0.0, y1)
    x2, y2 = min(1.0, x2), min(1.0, y2)
    px1, py1 = int(x1 * w0), int(y1 * h0)
    px2, py2 = int(x2 * w0), int(y2 * h0)
    crop = im[py1:py2, px1:px2]
    out = cover(crop, tw, th)
    # remap boxes into out pixels
    ch0, cw0 = crop.shape[:2]
    scale = max(tw / cw0, th / ch0)
    nw, nh = int(round(cw0 * scale)), int(round(ch0 * scale))
    xoff = max(0, (nw - tw) // 2)
    yoff = max(0, (nh - th) // 2)
    boxes = []
    for c, xc, yc, bw, bh in rows:
        # absolute in original
        ax1 = (xc - bw / 2) * w0 - px1
        ay1 = (yc - bh / 2) * h0 - py1
        ax2 = (xc + bw / 2) * w0 - px1
        ay2 = (yc + bh / 2) * h0 - py1
        bx1 = int(ax1 * scale - xoff)
        by1 = int(ay1 * scale - yoff)
        bx2 = int(ax2 * scale - xoff)
        by2 = int(ay2 * scale - yoff)
        boxes.append((c, max(0, bx1), max(0, by1), min(tw - 1, bx2), min(th - 1, by2)))
    return out, boxes


def draw_boxes(im, boxes, thickness=4):
    out = im.copy()
    for c, x1, y1, x2, y2 in boxes:
        color = COLS[c][::-1]
        cv2.rectangle(out, (x1, y1), (x2, y2), color, thickness)
        label = NAMES[c]
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        yy = max(th + 10, y1 - 10)
        cv2.rectangle(out, (x1, yy - th - 10), (x1 + tw + 12, yy + 4), color, -1)
        cv2.putText(out, label, (x1 + 6, yy - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (10, 10, 10), 2)
    return out


def make_three_types(stem: str):
    """CLASS / BBOX / MASK from a full Lab5 tool crop (not a chopped cutout)."""
    im = read(IMG / f"{stem}.jpg")[:, :, :3]
    h0, w0 = im.shape[:2]
    # pick pliers if present else largest box
    rows = parse_labels(stem)
    pick = max(rows, key=lambda r: (r[0] == 2, r[3] * r[4]))
    c, xc, yc, bw, bh = pick
    pad = 0.06
    x1 = max(0, int((xc - bw / 2 - pad) * w0))
    y1 = max(0, int((yc - bh / 2 - pad) * h0))
    x2 = min(w0, int((xc + bw / 2 + pad) * w0))
    y2 = min(h0, int((yc + bh / 2 + pad) * h0))
    crop = im[y1:y2, x1:x2].copy()
    ch, cw = crop.shape[:2]
    # object mask vs grid background
    # YOLO box inside padded crop
    yolo_bx1 = int(pad / (bw + 2 * pad) * cw)
    yolo_by1 = int(pad / (bh + 2 * pad) * ch)
    yolo_bx2 = cw - yolo_bx1 - 1
    yolo_by2 = ch - yolo_by1 - 1
    # GrabCut for clean silhouette (no grid speckles)
    gc = np.zeros(crop.shape[:2], np.uint8)
    rect = (
        max(1, yolo_bx1),
        max(1, yolo_by1),
        max(2, yolo_bx2 - yolo_bx1 - 1),
        max(2, yolo_by2 - yolo_by1 - 1),
    )
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(crop, gc, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
    mask = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8), 8)
    if n > 1:
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        mask = np.where(labels == largest, 255, 0).astype(np.uint8)
    # hard-clear outside YOLO rect so no bleed
    clear = np.zeros_like(mask)
    clear[yolo_by1:yolo_by2, yolo_bx1:yolo_bx2] = mask[yolo_by1:yolo_by2, yolo_bx1:yolo_bx2]
    mask = clear

    panel_w, panel_h = 560, 780
    canvas = np.full((panel_h, panel_w, 3), (18, 18, 22), np.uint8)
    scale = min((panel_w * 0.82) / cw, (panel_h * 0.82) / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    tool = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_AREA)
    msk = cv2.resize(mask, (nw, nh), interpolation=cv2.INTER_NEAREST)
    x0, y0 = (panel_w - nw) // 2, (panel_h - nh) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = tool
    # remap YOLO box for BBOX panel (tight GT), mask uses silhouette
    rx1 = x0 + int(yolo_bx1 * scale)
    ry1 = y0 + int(yolo_by1 * scale)
    rx2 = x0 + int(yolo_bx2 * scale)
    ry2 = y0 + int(yolo_by2 * scale)
    mask_full = np.zeros((panel_h, panel_w), np.uint8)
    mask_full[y0 : y0 + nh, x0 : x0 + nw] = msk

    class_img = canvas.copy()
    bbox_img = canvas.copy()
    mask_img = canvas.copy()
    cv2.rectangle(bbox_img, (rx1, ry1), (rx2, ry2), (200, 242, 92), 4)
    overlay = mask_img.copy()
    overlay[mask_full > 40] = (200, 242, 92)
    mask_img = cv2.addWeighted(mask_img, 0.4, overlay, 0.6, 0)
    cnts, _ = cv2.findContours((mask_full > 40).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask_img, cnts, -1, (200, 242, 92), 2)

    def frame(img, title):
        out = np.full((1080, 600, 3), (12, 12, 14), np.uint8)
        cv2.putText(out, title, (40, 78), cv2.FONT_HERSHEY_SIMPLEX, 1.55, (92, 242, 200), 3)
        ph, pw = img.shape[:2]
        scale2 = min(520 / pw, 820 / ph)
        nw2, nh2 = int(pw * scale2), int(ph * scale2)
        imr = cv2.resize(img, (nw2, nh2))
        xx = (600 - nw2) // 2
        yy = 120
        out[yy : yy + nh2, xx : xx + nw2] = imr
        cv2.rectangle(out, (xx - 2, yy - 2), (xx + nw2 + 2, yy + nh2 + 2), (55, 55, 65), 2)
        return out

    left, mid, right = frame(class_img, "CLASS"), frame(bbox_img, "BBOX"), frame(mask_img, "MASK")
    canvas_out = np.full((1080, 1920, 3), (10, 10, 12), np.uint8)
    gap = (1920 - 1800) // 4
    x = gap
    for part in (left, mid, right):
        canvas_out[:, x : x + 600] = part
        x += 600 + gap
    write(SL / "04_types.jpg", canvas_out)
    print("04_types", NAMES[c], "box", rx2 - rx1, ry2 - ry1)


def make_rules_slide(stem: str):
    im = read(IMG / f"{stem}.jpg")[:, :, :3]
    rows = parse_labels(stem)
    base, boxes = crop_around_boxes(im, rows, pad=0.14)
    annotated = draw_boxes(base, boxes, thickness=4)
    write(SL / "05_rules.jpg", bottom_scrim(annotated, 0.68, 0.9))
    print("05_rules", stem, "nboxes", len(boxes), [(NAMES[c], x2 - x1, y2 - y1) for c, x1, y1, x2, y2 in boxes])


def make_wrong_right(stem: str):
    im = read(IMG / f"{stem}.jpg")[:, :, :3]
    rows = parse_labels(stem)
    good_base, boxes = crop_around_boxes(im, rows, pad=0.14, tw=960, th=1080)
    bad = good_base.copy()
    good = draw_boxes(good_base, boxes, thickness=3)
    h, w = bad.shape[:2]
    cv2.rectangle(bad, (int(0.04 * w), int(0.1 * h)), (int(0.96 * w), int(0.9 * h)), (40, 90, 255), 5)
    cv2.putText(bad, "TOO WIDE", (int(0.08 * w), int(0.18 * h)), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (40, 90, 255), 3)
    cx, cy = int(0.48 * w), int(0.55 * h)
    cv2.rectangle(bad, (cx - 14, cy - 10), (cx + 14, cy + 10), (0, 0, 255), 3)
    cv2.putText(bad, "RANDOM CLICK", (cx - 110, cy - 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    # no baked BAD/GOOD — PPTX chrome owns headers (avoids double labels)
    write(SL / "06_compare.jpg", np.hstack([bad, good]))
    print("06_compare", stem)


def make_leakage(stem: str):
    """Leakage visual: one Lab5 frame + near-duplicate (tiny pan) = neighbor frames."""
    im = read(IMG / f"{stem}.jpg")[:, :, :3]
    h0, w0 = im.shape[:2]
    # slight pan/crop to mimic adjacent video frame
    shift = int(0.03 * w0)
    left = cover(im[:, : w0 - shift], 900, 900)
    right = cover(im[:, shift:], 900, 900)
    cv2.rectangle(left, (0, 0), (220, 70), (40, 180, 120), -1)
    cv2.putText(left, "TRAIN", (30, 48), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)
    cv2.rectangle(right, (0, 0), (180, 70), (40, 80, 255), -1)
    cv2.putText(right, "TEST", (30, 48), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3)
    canvas = np.full((1080, 1920, 3), (12, 12, 14), np.uint8)
    y = (1080 - 900) // 2 - 40
    canvas[y : y + 900, 40:940] = left
    canvas[y : y + 900, 980:1880] = right
    cv2.putText(
        canvas,
        "SAME VIDEO  ·  NEIGHBOR FRAMES",
        (520, 1020),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (180, 180, 190),
        2,
    )
    write(SL / "11_leakage.jpg", bottom_scrim(canvas, 0.85, 0.8))
    print("11_leakage", stem, "pan", shift)


def make_diversity_mosaic():
    names = [
        "video01_0001.jpg",
        "video02_0007.jpg",
        "video03_0002.jpg",
        "video04_0006.jpg",
        "video05_0003.jpg",
        "video06_0001.jpg",
    ]
    tiles = [cover(read(IMG / n)[:, :, :3], 640, 540) for n in names]
    mos = np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])])
    write(SL / "09_diversity.jpg", bottom_scrim(mos, 0.72, 0.92))
    print("09_diversity")


def main():
    # remove stale alternate names so nothing accidental gets reused
    for stale in ["06_wrong_right.jpg", "12_solutions.jpg", "10_adjacent.jpg"]:
        p = SL / stale
        if p.exists():
            p.unlink()

    mapping = {
        "01_hook.jpg": "viz_hand_label.jpg",
        "02_title.jpg": "bg_title.jpg",
        "03_ground.jpg": "viz_poison_label.jpg",
        "07_formats.jpg": "bg_formats.jpg",
        "08_part2.jpg": "bg_part2.jpg",
        "12_negatives.jpg": "viz_negative.jpg",
        "13_end.jpg": "bg_end.jpg",
        "10_duplicates.jpg": "viz_duplicate_frames.jpg",
    }
    for dst, src in mapping.items():
        src_path = GEN / src if (GEN / src).exists() else RAW / src
        start = 0.45 if dst == "12_negatives.jpg" else 0.58
        write(SL / dst, bottom_scrim(cover(read(src_path)[:, :, :3]), start, 0.92))
        print("bg", dst)

    for name in ["07_formats.jpg", "12_negatives.jpg"]:
        im = read(SL / name)[:, :, :3].astype(np.float32)
        for x in range(0, int(W * 0.48)):
            a = 0.78 * (1 - x / (W * 0.48))
            im[:, x] *= 1 - a
        write(SL / name, np.clip(im, 0, 255).astype(np.uint8))

    stem = pick_best_frame()
    print("best frame", stem)
    make_three_types(stem)
    make_rules_slide(stem)
    make_wrong_right(stem)
    make_diversity_mosaic()
    make_leakage(stem)

    files = sorted(SL.glob("*.jpg"))
    hashes = {}
    for f in files:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        hashes.setdefault(h, []).append(f.name)
    dups = {k: v for k, v in hashes.items() if len(v) > 1}
    print("files", [f.name for f in files])
    print("dups", dups or "none")
    assert not dups, dups
    needed = [
        "01_hook.jpg",
        "02_title.jpg",
        "03_ground.jpg",
        "04_types.jpg",
        "05_rules.jpg",
        "06_compare.jpg",
        "07_formats.jpg",
        "08_part2.jpg",
        "09_diversity.jpg",
        "10_duplicates.jpg",
        "11_leakage.jpg",
        "12_negatives.jpg",
        "13_end.jpg",
    ]
    missing = [n for n in needed if not (SL / n).exists()]
    assert not missing, missing


if __name__ == "__main__":
    main()
