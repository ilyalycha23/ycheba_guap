#!/usr/bin/env python3
"""Unit_0: artist→region join as LEFT JOIN (per workflow annotation)."""
from __future__ import annotations

import re

JOIN_GUID = "b80ba7a3-de11-4f32-8d57-c4418fa220fa"
JOIN_LINK = "8bebb345-8622-40d6-b92b-3cd5120075f3"

JOIN_BLOCK_RE = re.compile(
    rf'<Item Guid="{JOIN_GUID}"[\s\S]*?</Item>\s*(?=<Item Guid="2b3c4d5e-6f70-4819-a2b3-c4d5e6f70819")',
)
COLUMN_DEFS_RE = re.compile(r"<ColumnDefs>[\s\S]*?</ColumnDefs>")


def patch_join_node(text: str) -> str:
    m = JOIN_BLOCK_RE.search(text)
    if not m:
        raise RuntimeError("join node not found")

    block = m.group(0)
    if JOIN_LINK not in block:
        raise RuntimeError("join link not found")

    block = block.replace('JoinType="jtJoin"', 'JoinType="jtLeftJoin"', 1)

    def clear_input_cols(section: str, item_marker: str, src: str) -> str:
        sec_m = re.search(rf"<{section}>([\s\S]*?)</{section}>", src)
        if not sec_m:
            raise RuntimeError(f"{section} missing in join node")
        body = sec_m.group(1)
        pat = (
            rf"({re.escape(item_marker)}[\s\S]*?"
            rf'<DataSource SyncThroughColumns="true">\s*)'
            + COLUMN_DEFS_RE.pattern
        )
        new_body, n = re.subn(pat, r"\1<ColumnDefs/>", body, count=1)
        if n != 1:
            raise RuntimeError(f"failed to clear ColumnDefs in {section}")
        return src[: sec_m.start(1)] + new_body + src[sec_m.end(1) :]

    block = clear_input_cols(
        "InputSockets",
        '<Item Guid="e028600d-9dca-3604-89ce-cd2fdadb4c1c" Name="MainDataSource"',
        block,
    )
    block = clear_input_cols(
        "InputSockets",
        '<Item Guid="54ae772d-7bcb-36bb-88ac-976dcae031bc" Name="JoinedDataSource"',
        block,
    )

    return text[: m.start()] + block + text[m.end() :]
