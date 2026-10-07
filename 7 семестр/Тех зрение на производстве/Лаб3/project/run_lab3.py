# -*- coding: utf-8 -*-
"""ЛР3 на реальном NEU-DET (Kaggle): предобработка OpenCV + метрики для отчёта."""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

NEU = Path(r"C:\temp\lab3_tv\kaggle\NEU-DET\train\images")
ROOT = Path(r"C:\temp\lab3_tv\project")
RAW = ROOT / "data" / "raw"
FRAMES = ROOT / "data" / "frames"
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"

CLASSES = [
    "scratches",
    "patches",
    "inclusion",
    "crazing",
    "pitted_surface",
    "rolled-in_scale",
]


def wipe(p: Path):
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)


def resize_with_padding(image, size=640, value=114):
    h, w = image.shape[:2]
    scale = min(size / w, size / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_AREA)
    top = (size - nh) // 2
    bottom = size - nh - top
    left = (size - nw) // 2
    right = size - nw - left
    return cv2.copyMakeBorder(
        resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(value, value, value)
    )


def mean_time_ms(func, frame, repeats=30):
    for _ in range(5):
        func(frame)
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(frame)
        times.append((time.perf_counter() - t0) * 1000)
    return float(np.mean(times)), float(np.max(times))


def to_rgb(bgr):
    if bgr.ndim == 2:
        return bgr
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def save_fig(path):
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def pick_images(n_per_class=5):
    chosen = []
    for cls in CLASSES:
        folder = NEU / cls
        files = sorted(folder.glob("*.jpg"))
        for f in files[:n_per_class]:
            chosen.append((cls, f))
    return chosen


def ensure_bgr(img):
    if img is None:
        raise FileNotFoundError("empty image")
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def main():
    for p in (RAW, FRAMES, PROCESSED, RESULTS):
        wipe(p)

    picks = pick_images(5)  # 6*5 = 30 images
    assert len(picks) >= 20

    # copy raw + build video frames list
    bgr_list = []
    for i, (cls, src) in enumerate(picks, 1):
        img = ensure_bgr(cv2.imread(str(src)))
        # unify to 1280x720 for report consistency (NEU is often ~200x200)
        h, w = img.shape[:2]
        # keep native for processing quality; report will state native size of working frame
        out_name = f"image_{i:02d}_{cls}.jpg"
        cv2.imwrite(str(RAW / out_name), img)
        bgr_list.append(img)

    # working frame: prefer scratches (clear defect) upscaled for demo of pipeline timing on larger frame
    # but methodology allows any - use native first image and also create HD version for timing budget discussion
    img0 = bgr_list[0]
    # Upscale working demo frame to typical camera size while keeping aspect (letterbox later)
    # For NEU small images, enlarge with INTER_CUBIC for visualization / timing at production-like size
    img = cv2.resize(img0, (1280, 720), interpolation=cv2.INTER_CUBIC)
    # blend a couple of different defects into video by cycling originals upscaled
    video_path = RAW / "neu_line.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(str(video_path), fourcc, 25.0, (1280, 720))
    for t in range(750):  # 30 s
        src = bgr_list[t % len(bgr_list)]
        fr = cv2.resize(src, (1280, 720), interpolation=cv2.INTER_CUBIC)
        vw.write(fr)
    vw.release()

    h, w = img.shape[:2]
    channels = img.shape[2]
    meta = {
        "object": "дефекты поверхности горячекатаной стали (датасет NEU-DET: scratches, patches, inclusion, crazing, pitted_surface, rolled-in_scale)",
        "dataset": "NEU-DET (Kaggle / Northeastern University)",
        "n_images": len(picks),
        "classes_used": CLASSES,
        "video": video_path.name,
        "video_duration_s": 30,
        "resolution": f"{w}x{h}",
        "native_sample": f"{img0.shape[1]}x{img0.shape[0]}",
        "channels": int(channels),
        "dtype": str(img.dtype),
        "fps": 25,
        "note": "Рабочий кадр приведён к 1280×720 (как типичный видеопоток стенда); исходники NEU сохранены в data/raw без предобработки классов.",
    }

    cv2.imwrite(str(RESULTS / "01_original.jpg"), img)
    # also save native collage of 6 classes
    thumbs = []
    for cls in CLASSES:
        f = next((NEU / cls).glob("*.jpg"))
        im = ensure_bgr(cv2.imread(str(f)))
        im = cv2.resize(im, (200, 200))
        cv2.putText(im, cls[:10], (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA)
        thumbs.append(im)
    row1 = np.hstack(thumbs[:3])
    row2 = np.hstack(thumbs[3:])
    collage = np.vstack([row1, row2])
    cv2.imwrite(str(RESULTS / "00_classes.jpg"), collage)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    cv2.imwrite(str(RESULTS / "02_gray.jpg"), gray)
    cv2.imwrite(str(RESULTS / "03_hue.jpg"), hue)
    cv2.imwrite(str(RESULTS / "04_saturation.jpg"), saturation)
    cv2.imwrite(str(RESULTS / "05_value.jpg"), value)

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    axes[0].imshow(to_rgb(img))
    axes[0].set_title("BGR (исходный)")
    axes[1].imshow(gray, cmap="gray")
    axes[1].set_title("Gray")
    axes[2].imshow(hue, cmap="gray")
    axes[2].set_title("HSV: Hue")
    axes[3].imshow(value, cmap="gray")
    axes[3].set_title("HSV: Value")
    for ax in axes:
        ax.axis("off")
    save_fig(RESULTS / "06_colorspaces.png")

    mean_g = float(gray.mean())
    std_g = float(gray.std())
    meta["gray_mean"] = round(mean_g, 2)
    meta["gray_std"] = round(std_g, 2)

    plt.figure(figsize=(7, 4))
    plt.hist(gray.ravel(), bins=256, range=(0, 256), color="steelblue")
    plt.xlabel("Яркость")
    plt.ylabel("Количество пикселей")
    plt.title(f"Гистограмма яркости (mean={mean_g:.1f}, std={std_g:.1f})")
    plt.grid(True, alpha=0.3)
    save_fig(RESULTS / "07_hist_original.png")

    linear = cv2.convertScaleAbs(img, alpha=1.15, beta=10)
    gamma = 0.8
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(256)]).astype("uint8")
    gamma_img = cv2.LUT(img, table)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    clahe_img = cv2.cvtColor(cv2.merge([l2, a, b]), cv2.COLOR_LAB2BGR)
    for name, im in [("08_linear.jpg", linear), ("09_gamma.jpg", gamma_img), ("10_clahe.jpg", clahe_img)]:
        cv2.imwrite(str(RESULTS / name), im)

    g_clahe = cv2.cvtColor(clahe_img, cv2.COLOR_BGR2GRAY)
    meta["clahe_mean"] = round(float(g_clahe.mean()), 2)
    meta["clahe_std"] = round(float(g_clahe.std()), 2)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, im, t in zip(
        axes.ravel(),
        [img, linear, gamma_img, clahe_img],
        ["Исходный", "Линейная α=1.15 β=10", "Гамма γ=0.8", "CLAHE 2.0 / 8×8"],
    ):
        ax.imshow(to_rgb(im))
        ax.set_title(t)
        ax.axis("off")
    save_fig(RESULTS / "11_corrections.png")

    # mild SP noise ONLY for filter comparison
    rng = np.random.default_rng(7)
    noisy = clahe_img.copy()
    n = int(0.004 * noisy.shape[0] * noisy.shape[1])
    ys = rng.integers(0, noisy.shape[0], n)
    xs = rng.integers(0, noisy.shape[1], n)
    noisy[ys, xs] = rng.choice([0, 255], size=(n, 1))
    cv2.imwrite(str(RESULTS / "12_noisy_for_filter_compare.jpg"), noisy)

    gaussian = cv2.GaussianBlur(noisy, (5, 5), 0)
    median = cv2.medianBlur(noisy, 5)
    bilateral = cv2.bilateralFilter(noisy, 9, 75, 75)
    for name, im in [
        ("13_gaussian.jpg", gaussian),
        ("14_median.jpg", median),
        ("15_bilateral.jpg", bilateral),
    ]:
        cv2.imwrite(str(RESULTS / name), im)

    t_g, _ = mean_time_ms(lambda x: cv2.GaussianBlur(x, (5, 5), 0), noisy, 30)
    t_m, _ = mean_time_ms(lambda x: cv2.medianBlur(x, 5), noisy, 30)
    t_b, _ = mean_time_ms(lambda x: cv2.bilateralFilter(x, 9, 75, 75), noisy, 30)
    meta["times_ms"] = {
        "gaussian_5x5": round(t_g, 3),
        "median_5x5": round(t_m, 3),
        "bilateral_9_75": round(t_b, 3),
    }

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, im, t in zip(
        axes.ravel(),
        [noisy, gaussian, median, bilateral],
        ["С шумом (сравнение)", f"Gaussian {t_g:.2f} мс", f"Median {t_m:.2f} мс", f"Bilateral {t_b:.2f} мс"],
    ):
        ax.imshow(to_rgb(im))
        ax.set_title(t)
        ax.axis("off")
    save_fig(RESULTS / "16_filters.png")

    prepared = resize_with_padding(median, 640)
    cv2.imwrite(str(RESULTS / "17_prepared_640.jpg"), prepared)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(to_rgb(median))
    axes[0].set_title(f"После фильтрации {w}×{h}")
    axes[0].axis("off")
    axes[1].imshow(to_rgb(prepared))
    axes[1].set_title("640×640 (padding=114)")
    axes[1].axis("off")
    save_fig(RESULTS / "18_resize.png")

    # extract frames from video
    cap = cv2.VideoCapture(str(video_path))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total // 50, 1)
    idx = saved = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            cv2.imwrite(str(FRAMES / f"frame_{idx:06d}.jpg"), frame)
            saved += 1
        idx += 1
    cap.release()
    meta["frames_saved"] = saved

    def pipeline(frame):
        lab_ = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_, a_, b_ = cv2.split(lab_)
        l2_ = clahe.apply(l_)
        frame = cv2.cvtColor(cv2.merge([l2_, a_, b_]), cv2.COLOR_LAB2BGR)
        frame = cv2.medianBlur(frame, 5)
        return resize_with_padding(frame, 640)

    t_pipe, _ = mean_time_ms(pipeline, img, 30)
    meta["pipeline_ms"] = round(t_pipe, 3)

    for i, file in enumerate(sorted(FRAMES.glob("*.jpg"))):
        frame = cv2.imread(str(file))
        out = pipeline(frame)
        cv2.imwrite(str(PROCESSED / file.name), out)
        if i < 3:
            left = cv2.resize(frame, (640, 360))
            canvas = np.full((640, 640, 3), 114, np.uint8)
            y0 = (640 - 360) // 2
            canvas[y0 : y0 + 360, :] = left
            pair = np.hstack([canvas, out])
            cv2.imwrite(str(RESULTS / f"19_pair_{i+1}.jpg"), pair)

    # three class examples raw/proc
    for i, cls in enumerate(["scratches", "patches", "inclusion"]):
        src = next((NEU / cls).glob("*.jpg"))
        fr = cv2.resize(ensure_bgr(cv2.imread(str(src))), (1280, 720), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(str(RESULTS / f"20_raw_{i+1:02d}.jpg"), fr)
        cv2.imwrite(str(RESULTS / f"21_proc_{i+1:02d}.jpg"), pipeline(fr))

    (RESULTS / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print("OK processed", len(list(PROCESSED.glob('*.jpg'))))


if __name__ == "__main__":
    main()
