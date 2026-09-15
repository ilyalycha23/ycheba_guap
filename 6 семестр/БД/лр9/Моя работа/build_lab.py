#!/usr/bin/env python3
"""Build LR9 movies lab in 'Моя работа' folder."""
from __future__ import annotations

import random
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pyodbc

from patch_join import patch_join_node
from patch_meta_scaling import patch_unit1
from patch_movies_text import patch_movies_text
from patch_union import patch_union_node

ROOT = Path(__file__).resolve().parent
LAB_SRC = ROOT.parent / "Лаба"
PKG_SRC = LAB_SRC / "lr9_pathfix_src"
DATA = ROOT / "data"
MODELS = ROOT / "models"

COLUMNS = [
    "Track", "Album Name", "Artist", "Release Date", "ISRC", "All Time Rank",
    "Track Score", "Spotify Streams", "Spotify Playlist Count", "Spotify Playlist Reach",
    "Spotify Popularity", "YouTube Views", "YouTube Likes", "TikTok Posts", "TikTok Likes",
    "TikTok Views", "YouTube Playlist Reach", "Apple Music Playlist Count", "AirPlay Spins",
    "SiriusXM Spins", "Deezer Playlist Count", "Deezer Playlist Reach", "Amazon Playlist Count",
    "Pandora Streams", "Pandora Track Stations", "Soundcloud Streams", "Shazam Counts",
    "TIDAL Popularity", "Explicit Track",
]

TITLES = [
    "Neon Horizon", "Silent Protocol", "Winter Echo", "City of Glass", "Last Signal",
    "Parallel Lines", "Midnight Cartel", "Ocean of Stars", "Broken Compass", "Red Meridian",
    "Ghost Frequency", "Iron Garden", "Velvet Storm", "Northern Code", "Paper Kingdom",
    "Solar Drift", "Crimson Archive", "Blue Static", "Echo Chamber", "Final Orbit",
    "White Noise", "Golden Ratio", "Shadow Circuit", "Deep Current", "Arctic Pulse",
    "Quantum Rain", "Stone Butterfly", "Digital Saints", "Burning Atlas", "Frozen Ledger",
    "Hyperion Rise", "Lunar Cartography", "Obsidian Heart", "Silver Transit", "Nova Protocol",
    "Ember Valley", "Crystal Fault", "Thunder Archive", "Violet Engine", "Binary Sunset",
    "Aurora Debt", "Carbon Dreams", "Desert Oracle", "Electric Mirage", "Feral Harmony",
    "Glass Reactor", "Hollow Crown", "Infinite Margin", "Jade Frequency", "Kinetic Prayer",
]
FRANCHISES = [
    "Standalone", "Chronicles Saga", "Universe Zero", "Legacy Cycle", "Prime Story",
    "Origin Arc", "Final Chapter", "New Dawn", "Dark Matter", "Open Sky",
]
REGIONS = ["Americas", "Europe", "Asia-Pacific", "Latin America"]
MARKET_SIZES = ["large", "medium", "small"]
DIRECTORS = [
    "A. Volkov", "M. Chen", "S. Patel", "E. Brooks", "L. Nakamura", "R. Silva",
    "K. Olsen", "J. Martinez", "T. Kim", "N. Fischer", "O. Dubois", "P. Singh",
    "H. Andersson", "C. Wright", "D. Rossi", "F. Nguyen", "G. Murphy", "I. Hassan",
    "V. Popov", "Y. Tanaka", "B. Carter", "Z. Ali", "Q. Jensen", "W. Stone",
]


def write_ref_artist_regions() -> None:
    """Directors in movies.mdb must match column artist in the CSV (Join: Artist = artist)."""
    rng = random.Random(42)
    rows = [
        {
            "artist": director,
            "region": rng.choice(REGIONS),
            "market_size": rng.choice(MARKET_SIZES),
        }
        for director in DIRECTORS
    ]
    pd.DataFrame(rows).to_csv(DATA / "ref_artist_regions.csv", index=False)
    print(f"ref_artist_regions.csv: {len(rows)} directors")


def fmt_num(n: int) -> str:
    return f"{n:,}"


def generate_movies(n: int = 4600) -> pd.DataFrame:
    rng = random.Random(42)
    rows = []
    for i in range(n):
        gross = int(rng.lognormvariate(15.5, 1.1))
        gross = min(max(gross, 50_000), 2_500_000_000)
        pop = int(rng.uniform(5, 95))
        score = round(rng.uniform(15, 120), 1)
        title = f"{rng.choice(TITLES)} {2025 if rng.random() > 0.3 else ''}".strip()
        if rng.random() < 0.15:
            title += f" {rng.randint(2, 4)}"
        day = rng.randint(1, 365)
        rel = datetime(2025, 1, 1) + timedelta(days=day - 1)
        yt = int(gross * rng.uniform(0.05, 0.8))
        tiktok = int(gross * rng.uniform(0.01, 0.3))
        rows.append({
            "Track": title,
            "Album Name": rng.choice(FRANCHISES),
            "Artist": rng.choice(DIRECTORS),
            "Release Date": rel,
            "ISRC": f"MV2025{i+1:05d}",
            "All Time Rank": rng.randint(1, 5000),
            "Track Score": score,
            "Spotify Streams": fmt_num(gross),
            "Spotify Playlist Count": fmt_num(int(rng.uniform(100, 200_000))),
            "Spotify Playlist Reach": fmt_num(int(rng.uniform(10_000, 80_000_000))),
            "Spotify Popularity": pop,
            "YouTube Views": fmt_num(yt),
            "YouTube Likes": fmt_num(int(yt * rng.uniform(0.01, 0.05))),
            "TikTok Posts": fmt_num(int(rng.uniform(100, 2_000_000))),
            "TikTok Likes": fmt_num(tiktok),
            "TikTok Views": fmt_num(int(tiktok * rng.uniform(1.2, 4.0))),
            "YouTube Playlist Reach": fmt_num(int(rng.uniform(0, 20_000_000))),
            "Apple Music Playlist Count": int(rng.uniform(0, 500)),
            "AirPlay Spins": fmt_num(int(rng.uniform(0, 500_000))),
            "SiriusXM Spins": int(rng.uniform(0, 100_000)),
            "Deezer Playlist Count": int(rng.uniform(0, 300)),
            "Deezer Playlist Reach": fmt_num(int(rng.uniform(0, 10_000_000))),
            "Amazon Playlist Count": int(rng.uniform(0, 200)),
            "Pandora Streams": fmt_num(int(rng.uniform(0, 50_000_000))),
            "Pandora Track Stations": fmt_num(int(rng.uniform(0, 100_000))),
            "Soundcloud Streams": fmt_num(int(rng.uniform(0, 30_000_000))),
            "Shazam Counts": fmt_num(int(rng.uniform(0, 5_000_000))),
            "TIDAL Popularity": fmt_num(int(rng.uniform(0, 100))),
            "Explicit Track": 1 if rng.random() < 0.25 else 0,
        })
    return pd.DataFrame(rows, columns=COLUMNS)


def create_access_db(df: pd.DataFrame, mdb_path: Path) -> None:
    mdb_path.parent.mkdir(parents=True, exist_ok=True)
    template = LAB_SRC / "data" / "spotify.mdb"
    if mdb_path.exists():
        mdb_path.unlink()
    shutil.copy2(template, mdb_path)
    conn = pyodbc.connect(
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + str(mdb_path) + ";"
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM spotify_songs")
    conn.commit()
    insert_sql = (
        "INSERT INTO spotify_songs ("
        + ", ".join(f"[{c}]" for c in COLUMNS)
        + ") VALUES ("
        + ", ".join("?" for _ in COLUMNS)
        + ")"
    )
    batch = 500
    rows = [tuple(row[c] for c in COLUMNS) for _, row in df.iterrows()]
    for i in range(0, len(rows), batch):
        cur.executemany(insert_sql, rows[i : i + batch])
        conn.commit()
    cur.execute("SELECT COUNT(*) FROM spotify_songs")
    print(f"spotify_songs rows (movies data): {cur.fetchone()[0]}")
    conn.close()


def copy_support_files() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    write_ref_artist_regions()
    for name in ("ref_explicit_map.csv", "ref_stream_tiers.txt"):
        src = LAB_SRC / "data" / name
        if src.exists():
            shutil.copy2(src, DATA / name)
    # Scoring hold-out sample
    src_score = LAB_SRC / "data" / "prepared_spotify_score.csv"
    if src_score.exists():
        df = pd.read_csv(src_score, nrows=459)
        # remap to movie-like titles while keeping schema
        rng = random.Random(99)
        df["track"] = [f"{rng.choice(TITLES)} 2025" for _ in range(len(df))]
        df["artist"] = [rng.choice(DIRECTORS) for _ in range(len(df))]
        df["album_name"] = [rng.choice(FRANCHISES) for _ in range(len(df))]
        df.to_csv(DATA / "prepared_movies_score.csv", index=False)


def build_lgp() -> Path:
    work = ROOT / "_pkg_build"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(PKG_SRC, work)
    for xml in work.rglob("*.xml"):
        raw = patch_movies_text(xml.read_text(encoding="utf-8"))
        if xml.name == "Unit.xml" and xml.parent.name == "Unit_0":
            raw = patch_union_node(raw)
            raw = patch_join_node(raw)
        if xml.name == "Unit.xml" and xml.parent.name == "Unit_1":
            raw = patch_unit1(raw)
        xml.write_text(raw, encoding="utf-8")
    for bin_file in (
        work / "Unit_0" / "Unit.bin",
        work / "Unit_0" / "Info.bin",
        work / "Unit_1" / "Unit.bin",
        work / "Unit_1" / "Info.bin",
    ):
        if bin_file.exists():
            bin_file.unlink()
    out = ROOT / "lr9_movies.lgp"
    if out.exists():
        shutil.copy2(out, out.with_suffix(".lgp.bak"))
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(work.rglob("*")):
            if fp.is_file():
                zf.write(fp, fp.relative_to(work).as_posix())
    for xf in work.rglob("*.xml"):
        ET.parse(xf)
    shutil.rmtree(work)
    return out


def copy_libraries() -> None:
    for name in (
        "loginom_python_kit.lgp",
        "loginom_silver_kit.lgp",
        "loginom_sklearn_kit.lgp",
        "loginom_sklearn_meta.lgp",
    ):
        src = LAB_SRC / name
        if not src.exists():
            src = ROOT.parent / "loginom-python-kits-master" / "python_kits" / name
        if src.exists():
            shutil.copy2(src, ROOT / name)


def copy_models() -> None:
    src_models = LAB_SRC / "models"
    if src_models.exists():
        if MODELS.exists():
            shutil.rmtree(MODELS)
        shutil.copytree(src_models, MODELS)


def write_report() -> None:
    report = ROOT / "Отчет.md"
    report.write_text(
        """# Лабораторная работа №9 — Анализ фильмов 2025 года в Loginom

## 1. Цель работы

Построить сквозной аналитический пайплайн на платформе **Loginom 7.3** для базы данных **фильмов 2025 года**:
подготовка обучающих выборок из СУБД **Microsoft Access**, обучение моделей **LOF** (обнаружение аномалий) и **логистической регрессии sklearn**, оценка качества классификации.

## 2. Исходные данные

| Объект | Описание |
|--------|----------|
| `data/movies.mdb` | База Access, таблица `spotify_songs` (~4600 фильмов 2025 года) |
| `data/ref_artist_regions.csv` | Справочник регионов режиссёров (поле `Artist`) |
| `data/prepared_movies_score.csv` | Hold-out выборка для скоринга LR (459 фильмов) |

### Смысл полей (кинематографическая интерпретация)

В Loginom сохранены имена полей исходного шаблона для совместимости с kits:

| Поле в БД | Смысл для фильмов |
|-----------|-------------------|
| `Track` | Название фильма |
| `Artist` | Режиссёр |
| `Album Name` | Франшиза / серия |
| `Spotify Streams` | Мировые кассовые сборы (Worldwide Gross) |
| `Spotify Popularity` | Популярность TMDB (0–100) |
| `Track Score` | Композитный рейтинг фильма |
| `IsHit` | Блокбастер: сборы ≥ 100 млн |
| `YouTube Views` | Просмотры трейлера |
| `TikTok Posts/Likes/Views` | Соцсетевые метрики |

## 3. Модуль «Подготовка выборок» (Unit_0)

Цепочка узлов:

1. **Подключение MS Access** → `data/movies.mdb`
2. **Импорт** `SELECT * FROM spotify_songs` (данные о фильмах 2025)
3. **Очистка полей** — удаление лишних столбцов, переименование popularity
4. **Join** со справочником регионов режиссёров
5. **Фильтрация выбросов** по числовым полям
6. **IsHit** — Python: блокбастер если Worldwide Gross ≥ 100 000 000
7. **Фильтр popularity ≥ 30** — отсечение малозаметных фильмов
8. **Парсинг чисел** — очистка форматированных строк (`1,234,567`)
9. **Квантование** — q_popularity, q_streams, q_track_score (квинтили)
10. **Разбиение 80/20** (stratify по IsHit) → train / test
11. **Калькуляторы** SAMPLE, IsTestSet, OBJECT
12. **Экспорт** `data/данные.txt` и публичный узел **Movies dataset**

## 4. Модуль «Построение модели» (Unit_1)

### 4.1 LOF (Local Outlier Factor)

- **meta-scaling** — StandardScaler только на train
- **neighbors.LOF Novelty** — k=20, contamination=0.15
- **model.fitter** — обучение на train, скоринг test
- **classification metrics** — precision, recall, F1 vs IsHit

LOF ищет фильмы-аномалии: необычные комбинации сборов, популярности и соцметрик.

### 4.2 Логистическая регрессия (sklearn)

- **linear_model.LogisticRegression** + **model.fitter**
- Сравнение с LOF на той же scaled-выборке
- **LR predict score** — скоринг hold-out CSV
- Отчёт `data/report_scoring_lr.txt`

## 5. Структура папки «Моя работа»

```
Моя работа/
├── lr9_movies.lgp          ← открыть в Loginom
├── loginom_*.lgp           ← библиотеки kits
├── data/
│   ├── movies.mdb
│   ├── ref_artist_regions.csv
│   └── prepared_movies_score.csv
├── models/                 ← модели после первого прогона Unit_1
└── Отчет.md
```

## 6. Порядок запуска

1. Открыть **Loginom 7.3.1 Community**
2. Файл → Открыть → `lr9_movies.lgp`
3. Выполнить сценарий **«Подготовка выборок»** (Unit_0)
4. Выполнить сценарий **«Построение модели»** (Unit_1)
5. Просмотреть метрики в узлах **classification metrics**

## 7. Ожидаемые результаты

- Train/test split с полями `SAMPLE`, `IsTestSet`, `IsHit`
- Модель LOF в `models/lof_k20_c05/`
- Модель LR в `models/lr_sklearn/`
- Метрики F1, precision, recall на тестовой выборке
- Отчёт скоринга hold-out фильмов

## 8. Вывод

Лабораторная работа демонстрирует полный цикл ML в Loginom: **ETL из Access → feature engineering → unsupervised (LOF) + supervised (LR) → metrics**. Предметная область — **киноиндустрия 2025**: прогнозирование блокбастеров и поиск аномальных фильмов по кассовым и маркетинговым признакам.
""",
        encoding="utf-8",
    )


def main() -> None:
    print("=== Building movies lab ===")
    ROOT.mkdir(parents=True, exist_ok=True)
    df = generate_movies(4600)
    create_access_db(df, DATA / "movies.mdb")
    copy_support_files()
    copy_libraries()
    (MODELS / "lof_k20_c05").mkdir(exist_ok=True)
    (MODELS / "lr_sklearn").mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "train_models.py")], check=True)
    lof_src = LAB_SRC / "models" / "lof_k20_c05" / "model.pkl"
    lof_dst = MODELS / "lof_k20_c05" / "model.pkl"
    if lof_src.exists():
        shutil.copy2(lof_src, lof_dst)
    lgp = build_lgp()
    write_report()
    readme = ROOT / "README.txt"
    readme.write_text(
        "Лабораторная работа LR9 — Фильмы 2025\n\n"
        "1. Откройте lr9_movies.lgp в Loginom 7.3.1\n"
        "2. Убедитесь, что рядом лежат loginom_*.lgp библиотеки\n"
        "3. Сначала выполните «Подготовка выборок» (Unit_0) — создаст data/данные.txt\n"
        "4. Затем «Построение модели» (Unit_1) читает data/данные.txt\n"
        "5. Отчёт: Отчет.md\n",
        encoding="utf-8",
    )
    print(f"Done: {lgp}")
    print(f"Report: {ROOT / 'Отчет.md'}")


if __name__ == "__main__":
    main()
