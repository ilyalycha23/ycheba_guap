# -*- coding: utf-8 -*-
"""Шаг 3 ЛР6: проверка структуры набора и нормализация data.yaml."""
from pathlib import Path
import shutil
import yaml

root = Path("dataset").resolve()
path = root / "data.yaml"
cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
names = cfg["names"]
if isinstance(names, dict):
    names = {int(k): v for k, v in names.items()}
    if sorted(names) != list(range(len(names))):
        raise ValueError("Номера классов должны идти от 0 подряд")
else:
    names = dict(enumerate(names))
if not names or len(set(names.values())) != len(names):
    raise ValueError("Проверьте перечень классов")
for split in ("train", "valid", "test"):
    for subdir in ("images", "labels"):
        if not (root / split / subdir).is_dir():
            raise FileNotFoundError(root / split / subdir)
backup = root / "data_original.yaml"
if not backup.exists():
    shutil.copy2(path, backup)
cfg = dict(
    path=str(root),
    train="train/images",
    val="valid/images",
    test="test/images",
    names=names,
)
path.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
print(path)
print(names)
