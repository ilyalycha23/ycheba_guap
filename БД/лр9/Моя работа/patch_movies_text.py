#!/usr/bin/env python3
"""Replace Spotify/music wording with movies terminology in Loginom XML."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK_BASE_FWD = "D:/ycheba_guap/БД/лр9/Моя работа"
WORK_BASE_BSL = r"D:\ycheba_guap\БД\лр9\Моя работа"

# Longer strings first where order matters.
TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    # Paths and package ids
    ("D:/ycheba_guap/БД/лр9/Лаба", WORK_BASE_FWD),
    (r"D:\ycheba_guap\БД/лр9\Лаба", WORK_BASE_BSL),
    (r"D:\ycheba_guap\БД\лр9\Лаба", WORK_BASE_BSL),
    ("data/spotify.mdb", "data/movies.mdb"),
    ('Name="lr9_spotify"', 'Name="lr9_movies"'),
    ("lr9_spotify", "lr9_movies"),
    ("prepared_spotify_score.csv", "prepared_movies_score.csv"),
    ("prepared_spotify_tracks.csv", "prepared_movies_tracks.csv"),
    ("report: LR scoring (prepared_spotify_score.csv)", "report: LR scoring (prepared_movies_score.csv)"),
    # Node titles
    ("Импорт из Access (spotify_songs)", "Импорт из Access (фильмы 2025)"),
    ("↶Spotify dataset (публичный)", "↶Movies dataset (публичный)"),
    ("Spotify dataset (публичный)", "Movies dataset (публичный)"),
    ("3. Консолидация: ref_artist_regions.csv", "3. Консолидация: регионы режиссёров"),
    ("4. Join artist → region", "4. Join режиссёр → region"),
    ("8. IsHit (streams ≥ порога)", "8. IsHit (кассовые сборы ≥ порога)"),
    ("9. Отбор popularity ≥ 30", "9. Отбор TMDB popularity ≥ 30"),
    # Column display names (Name= stays unchanged for pipeline compatibility)
    ('DisplayName="Spotify Playlist Count"', 'DisplayName="Theater Count"'),
    ('DisplayName="Spotify Playlist Reach"', 'DisplayName="Box Office Reach"'),
    ('DisplayName="Spotify Streams"', 'DisplayName="Worldwide Gross"'),
    ('DisplayName="Spotify Popularity"', 'DisplayName="TMDB Popularity"'),
    ('DisplayName="Track Score"', 'DisplayName="Film Score"'),
    ('DisplayName="Pandora Track Stations"', 'DisplayName="TV Stations"'),
    ('DisplayName="Explicit Track"', 'DisplayName="Rated R"'),
    ('DisplayName="Apple Music Playlist Count"', 'DisplayName="VOD Platforms"'),
    ('DisplayName="Album Name"', 'DisplayName="Franchise"'),
    ('DisplayName="AirPlay Spins"', 'DisplayName="Radio Airings"'),
    ('DisplayName="SiriusXM Spins"', 'DisplayName="Cable Airings"'),
    ('DisplayName="Deezer Playlist Count"', 'DisplayName="Secondary VOD Count"'),
    ('DisplayName="Deezer Playlist Reach"', 'DisplayName="Secondary VOD Reach"'),
    ('DisplayName="Amazon Playlist Count"', 'DisplayName="Retail VOD Count"'),
    ('DisplayName="Pandora Streams"', 'DisplayName="Cable Views"'),
    ('DisplayName="Soundcloud Streams"', 'DisplayName="Social Views"'),
    ('DisplayName="Shazam Counts"', 'DisplayName="Search Queries"'),
    ('DisplayName="TIDAL Popularity"', 'DisplayName="Critics Score"'),
    # Annotations — Unit_0
    (
        'Text="ЛР9 Spotify (Loginom 7.3): ETL в Unit_0 → модель LOF в Unit_1.&#10;'
        "Источник: MS Access (spotify.mdb). Целевая переменная IsHit (streams ≥ 100M).&#10;"
        "Сделано: join с регионами артистов, очистка/пропуски/выбросы, отбор popularity≥30,&#10;"
        "квантование q_*, split train/test/valid, txt-снимки QC, экспорт data/данные.txt.&#10;"
        'Unit_1: scaling → LOF (k=20, contamination=0.15) → метрики vs IsHit на test+valid."',
        'Text="ЛР9 Фильмы 2025 (Loginom 7.3): ETL в Unit_0 → модель LOF в Unit_1.&#10;'
        "Источник: MS Access (movies.mdb). Целевая переменная IsHit (кассовые сборы ≥ 100 млн).&#10;"
        "Сделано: join с регионами режиссёров, очистка/пропуски/выбросы, отбор TMDB popularity≥30,&#10;"
        "квантование q_*, split train/test/valid, txt-снимки QC, экспорт data/данные.txt.&#10;"
        'Unit_1: scaling → LOF (k=20, contamination=0.15) → метрики vs IsHit на test+valid."',
    ),
    (
        'Text="3. Консолидация&#10;Загрузка ref_artist_regions.csv (artist → region, market_size)&#10;'
        '4. Join&#10;LEFT JOIN по полю Artist; добавляются region, market_size"',
        'Text="3. Консолидация&#10;Загрузка ref_artist_regions.csv (режиссёр → region, market_size)&#10;'
        '4. Join&#10;LEFT JOIN по полю Artist (режиссёр); добавляются region, market_size"',
    ),
    (
        'Text="8. IsHit&#10;IsHit = 1, если Spotify_Streams ≥ 100 000 000&#10;'
        '9. Отбор&#10;Оставляем только spotify_popularity ≥ 30 → ~3441 строк"',
        'Text="8. IsHit&#10;IsHit = 1, если Worldwide Gross ≥ 100 000 000&#10;'
        '9. Отбор&#10;Оставляем только TMDB popularity ≥ 30 → ~3350 фильмов"',
    ),
    (
        'Text="9b. Числовые метрики&#10;Парсинг строк с запятыми/? в числа&#10;'
        '9c. Квантование&#10;5 бинов (0–4): q_popularity, q_streams, q_track_score"',
        'Text="9b. Числовые метрики&#10;Парсинг строк с запятыми/? в числа&#10;'
        '9c. Квантование&#10;5 бинов (0–4): q_popularity (TMDB), q_streams (сборы), q_film_score (рейтинг)"',
    ),
    (
        'Text="8. Разбиение 80/20&#10;Stratify по IsHit; train ~80%, test ~20%&#10;'
        "9 / 10. SAMPLE&#10;Метки train и test&#10;11. Объединение&#10;"
        "Склейка train + test в один поток&#10;11b. Valid&#10;~18.75% от train → SAMPLE = valid (516 стр",
        'Text="8. Разбиение 80/20&#10;Stratify по IsHit; train ~80%, test ~20%&#10;'
        "9 / 10. SAMPLE&#10;Метки train и test&#10;11. Объединение&#10;"
        "Склейка train + test в один поток&#10;11b. Valid&#10;~18.75% от train → SAMPLE = valid (516 фильмов)",
    ),
    # Annotations — Unit_1
    (
        'Text="Метки для metrics (0/1)&#10;LOF: −1→1 (аномалия), +1→0 (норма) — бинарная метка для metrics&#10;'
        "Только test для metrics&#10;Фильтр IsTestSet=True (фактически test + valid, 1204 строки)&#10;"
        '↶classification metrics&#10;precision, recall, F1, confusion matrix vs IsHit"',
        'Text="Метки для metrics (0/1)&#10;LOF: −1→1 (аномалия), +1→0 (норма) — бинарная метка для metrics&#10;'
        "Только test для metrics&#10;Фильтр IsTestSet=True (фактически test + valid, 1204 фильма)&#10;"
        '↶classification metrics&#10;precision, recall, F1, confusion matrix vs IsHit"',
    ),
    (
        'Text="Скоринг hold-out (459 треков) без union в meta-scaling. '
        "Калькулятор: имена полей + SAMPLE=score. Замена: null→0. "
        'Python: q-бины + prob0/prob1. Отчёт report_scoring_lr.txt"',
        'Text="Скоринг hold-out (459 фильмов) без union в meta-scaling. '
        "Калькулятор: имена полей + SAMPLE=score. Замена: null→0. "
        'Python: q-бины + prob0/prob1. Отчёт report_scoring_lr.txt"',
    ),
]


def patch_movies_text(text: str) -> str:
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    return text
