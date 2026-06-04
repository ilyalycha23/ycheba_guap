#!/usr/bin/env python3
"""Train LR model.pkl for Loginom LR predict score node."""
from __future__ import annotations

import pickle
import random
from pathlib import Path

import pandas as pd
import pyodbc
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parent
MDB = ROOT / "data" / "movies.mdb"
OUT = ROOT / "models" / "lr_sklearn" / "model.pkl"

FEATURES = [
    "spotify_popularity", "All_Time_Rank", "Track_Score", "Spotify_Streams",
    "Spotify_Playlist_Count", "Spotify_Playlist_Reach", "YouTube_Views",
    "YouTube_Likes", "TikTok_Posts", "TikTok_Likes", "TikTok_Views",
    "YouTube_Playlist_Reach", "Apple_Music_Playlist_Count", "AirPlay_Spins",
    "Deezer_Playlist_Count", "Deezer_Playlist_Reach", "Amazon_Playlist_Count",
    "Pandora_Streams", "Pandora_Track_Stations", "Explicit_Track",
    "q_popularity", "q_streams", "q_track_score",
    "q_popularity_1", "q_streams_1", "q_track_score_1",
]

COL_MAP = {
    "Spotify Popularity": "spotify_popularity",
    "All Time Rank": "All_Time_Rank",
    "Track Score": "Track_Score",
    "Spotify Streams": "Spotify_Streams",
    "Spotify Playlist Count": "Spotify_Playlist_Count",
    "Spotify Playlist Reach": "Spotify_Playlist_Reach",
    "YouTube Views": "YouTube_Views",
    "YouTube Likes": "YouTube_Likes",
    "TikTok Posts": "TikTok_Posts",
    "TikTok Likes": "TikTok_Likes",
    "TikTok Views": "TikTok_Views",
    "YouTube Playlist Reach": "YouTube_Playlist_Reach",
    "Apple Music Playlist Count": "Apple_Music_Playlist_Count",
    "AirPlay Spins": "AirPlay_Spins",
    "Deezer Playlist Count": "Deezer_Playlist_Count",
    "Deezer Playlist Reach": "Deezer_Playlist_Reach",
    "Amazon Playlist Count": "Amazon_Playlist_Count",
    "Pandora Streams": "Pandora_Streams",
    "Pandora Track Stations": "Pandora_Track_Stations",
    "Explicit Track": "Explicit_Track",
}


def to_num(s: pd.Series) -> pd.Series:
    t = s.astype(str).str.replace(",", "", regex=False).str.replace("?", "", regex=False)
    return pd.to_numeric(t, errors="coerce").fillna(0)


def load_movies() -> pd.DataFrame:
    conn = pyodbc.connect(
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + str(MDB) + ";"
    )
    df = pd.read_sql("SELECT * FROM spotify_songs", conn)
    conn.close()
    out = pd.DataFrame()
    for src, dst in COL_MAP.items():
        if src in df.columns:
            out[dst] = to_num(df[src]) if dst != "spotify_popularity" else pd.to_numeric(df[src], errors="coerce").fillna(0)
    streams = out["Spotify_Streams"]
    out["IsHit"] = (streams >= 100_000_000).astype(int)
    out = out[out["spotify_popularity"] >= 30].reset_index(drop=True)
    return out


def add_qbins(df: pd.DataFrame) -> pd.DataFrame:
    for src, dst in (
        ("spotify_popularity", "q_popularity"),
        ("Spotify_Streams", "q_streams"),
        ("Track_Score", "q_track_score"),
    ):
        num = df[src]
        try:
            bins = pd.qcut(num.rank(method="first"), q=5, labels=False, duplicates="drop")
        except Exception:
            bins = pd.Series(0, index=df.index)
        df[dst] = bins.fillna(0).astype(int)
        df[dst + "_1"] = df[dst]
    return df


def train() -> None:
    df = load_movies()
    df = add_qbins(df)
    X = df[FEATURES].astype(float)
    y = df["IsHit"]
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, y)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved {OUT} | rows={len(df)} | features={len(FEATURES)} | hits={y.sum()}")


if __name__ == "__main__":
    train()
