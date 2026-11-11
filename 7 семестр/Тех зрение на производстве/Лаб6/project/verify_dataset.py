# -*- coding: utf-8 -*-
"""Проверка набора: счётчики рамок, наличие классов, независимость роликов."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("dataset")
NAMES = {0: "wrench", 1: "hammer", 2: "pliers"}


def scene_of(stem: str) -> str:
    return stem.rsplit("_", 1)[0]


def main():
    report = {}
    scenes_by_split = {}
    for split in ("train", "valid", "test"):
        boxes = Counter()
        scenes = set()
        n_img = 0
        empty = 0
        for lp in sorted((ROOT / split / "labels").glob("*.txt")):
            n_img += 1
            scenes.add(scene_of(lp.stem))
            lines = [ln for ln in lp.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if not lines:
                empty += 1
            for ln in lines:
                c = int(float(ln.split()[0]))
                boxes[NAMES[c]] += 1
            img = ROOT / split / "images" / f"{lp.stem}.jpg"
            if not img.exists():
                raise FileNotFoundError(img)
        scenes_by_split[split] = sorted(scenes)
        report[split] = {
            "n_images": n_img,
            "empty_labels": empty,
            "boxes": dict(boxes),
            "scenes": sorted(scenes),
            "missing_classes": [n for n in NAMES.values() if boxes[n] == 0],
        }
    # leakage by scene
    overlap = set(scenes_by_split["train"]) & set(scenes_by_split["valid"])
    overlap |= set(scenes_by_split["train"]) & set(scenes_by_split["test"])
    overlap |= set(scenes_by_split["valid"]) & set(scenes_by_split["test"])
    report["scene_overlap"] = sorted(overlap)
    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "dataset_stats.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if overlap:
        raise SystemExit(f"Ошибка: ролики в нескольких выборках: {overlap}")
    for split, info in report.items():
        if split == "scene_overlap":
            continue
        if info["missing_classes"]:
            raise SystemExit(f"Ошибка: в {split} нет классов {info['missing_classes']}")
    print("OK: split по роликам, все классы присутствуют")


if __name__ == "__main__":
    main()
