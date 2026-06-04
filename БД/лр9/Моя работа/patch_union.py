#!/usr/bin/env python3
"""Fix Union node «11. Объединение train + test» in lr9_movies.lgp."""
from __future__ import annotations

import re
import shutil
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LGP = ROOT / "lr9_movies.lgp"

UNION_NODE = "da71781d-3950-4d3f-8a83-fe030a69e7aa"
PORT_MAIN = "e028600d-9dca-3604-89ce-cd2fdadb4c1c"
PORT_JOIN = "54ae772d-7bcb-36bb-88ac-976dcae031bc"

UNION_COLUMNS = [
    "SAMPLE",
    "IsHit",
    "spotify_popularity",
    "q_popularity",
    "q_streams",
    "q_track_score",
    "Artist",
    "Track",
    "Album_Name",
    "Release_Date",
    "ISRC",
    "All_Time_Rank",
    "Track_Score",
    "Spotify_Streams",
    "Spotify_Playlist_Count",
    "Spotify_Playlist_Reach",
    "YouTube_Views",
    "YouTube_Likes",
    "TikTok_Posts",
    "TikTok_Likes",
    "TikTok_Views",
    "YouTube_Playlist_Reach",
    "Apple_Music_Playlist_Count",
    "AirPlay_Spins",
    "SiriusXM_Spins",
    "Deezer_Playlist_Count",
    "Deezer_Playlist_Reach",
    "Amazon_Playlist_Count",
    "Pandora_Streams",
    "Pandora_Track_Stations",
    "Soundcloud_Streams",
    "Shazam_Counts",
    "TIDAL_Popularity",
    "Explicit_Track",
    "region",
    "market_size",
]


def union_links_block() -> str:
    items = []
    for col in UNION_COLUMNS:
        item_guid = str(uuid.uuid4())
        items.append(
            f'\t\t\t\t\t\t\t<Item Guid="{item_guid}">\n'
            f'\t\t\t\t\t\t\t\t<Link Guid="{PORT_MAIN}" Name="{col}"/>\n'
            f'\t\t\t\t\t\t\t\t<Link Guid="{PORT_JOIN}" Name="{col}"/>\n'
            f"\t\t\t\t\t\t\t</Item>"
        )
    return "\t\t\t\t\t\t<Links>\n" + "\n".join(items) + "\n\t\t\t\t\t\t</Links>"


def patch_union_node(text: str) -> str:
    node_re = re.compile(
        rf'(<Item Guid="{re.escape(UNION_NODE)}"[\s\S]*?</Item>\s*)'
        rf'(?=<Item Guid="5e6f7081)',
    )
    m = node_re.search(text)
    if not m:
        raise RuntimeError(f"Union node {UNION_NODE} not found")

    node = m.group(1)
    node = re.sub(
        r'(<Item Guid="e028600d-9dca-3604-89ce-cd2fdadb4c1c" Name="MainDataSource"[\s\S]*?'
        r'<DataSource SyncThroughColumns="true">\s*)<ColumnDefs>[\s\S]*?</ColumnDefs>',
        r"\1<ColumnDefs/>",
        node,
        count=1,
    )
    node = re.sub(
        r'(<Item Guid="54ae772d-7bcb-36bb-88ac-976dcae031bc" Name="JoinedDataSource"[\s\S]*?'
        r'<DataSource SyncThroughColumns="true">\s*)<ColumnDefs>[\s\S]*?</ColumnDefs>',
        r"\1<ColumnDefs/>",
        node,
        count=1,
    )
    node = re.sub(
        r'(<Engine xsi:type="TBGUnionDataEngine"[^>]*>\s*)<Links>[\s\S]*?</Links>',
        rf"\1{union_links_block()}",
        node,
        count=1,
    )
    return text[: m.start(1)] + node + text[m.end(1) :]


def patch_lgp(lgp: Path) -> None:
    work = ROOT / "_union_patch"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    with zipfile.ZipFile(lgp) as zf:
        zf.extractall(work)

    unit = work / "Unit_0" / "Unit.xml"
    unit.write_text(patch_union_node(unit.read_text(encoding="utf-8")), encoding="utf-8")
    ET.parse(unit)

    for bin_name in ("Unit_0/Unit.bin", "Unit_0/Info.bin"):
        p = work / bin_name
        if p.exists():
            p.unlink()

    backup = lgp.with_suffix(".lgp.bak")
    shutil.copy2(lgp, backup)
    lgp.unlink()

    with zipfile.ZipFile(lgp, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(work.rglob("*")):
            if fp.is_file():
                zf.write(fp, fp.relative_to(work).as_posix())

    shutil.rmtree(work)
    print(f"Patched {lgp} ({len(UNION_COLUMNS)} union columns, backup: {backup.name})")


if __name__ == "__main__":
    if not LGP.is_file():
        raise SystemExit(f"Missing {LGP}")
    patch_lgp(LGP)
