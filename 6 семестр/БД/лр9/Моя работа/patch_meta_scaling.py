#!/usr/bin/env python3
"""Unit_1: import from data/данные.txt; schema for meta-scaling + cleanup Python."""
from __future__ import annotations

import html
import re

DATA_FILE = "D:/ycheba_guap/БД/лр9/Моя работа/data/данные.txt"
IMPORT_GUID = "e7f8a901-1122-4345-6789-abcdef012347"
REF_GUID = "5cb2521a-a56c-44cc-9276-aa417ed3f9f3"
CLEAN_GUID = "d1e2f3a4-b5c6-4789-d012-3456789abcde"
SCALER_GUID = "c12cfa3e-be40-4435-971f-b78451401827"
PORT_DATASET = "58f7e6c3-511e-39d7-8853-036e0a1a7612"
PORT_DS_IN = "9dc72a3f-56bf-3bfc-84ec-f979daf4da6b"
META_NODE = "6b45fb4e-d320-4f68-879b-f0f0b671fa0f"

TEXT_COLUMNS = {
    "Artist",
    "Track",
    "Album_Name",
    "Release_Date",
    "ISRC",
    "SAMPLE",
    "region",
    "market_size",
    "OBJECT",
}

IMPORT_COLUMNS: list[tuple[str, str, str]] = [
    ("IsTestSet", "dtBoolean", "dkDiscrete"),
    ("OBJECT", "dtString", "dkDiscrete"),
    ("SAMPLE", "dtString", "dkDiscrete"),
    ("IsHit", "dtInteger", "dkDiscrete"),
    ("spotify_popularity", "dtFloat", "dkContinuous"),
    ("Artist", "dtString", "dkDiscrete"),
    ("Track", "dtString", "dkDiscrete"),
    ("Album_Name", "dtString", "dkDiscrete"),
    ("Release_Date", "dtDateTime", "dkContinuous"),
    ("ISRC", "dtString", "dkDiscrete"),
    ("All_Time_Rank", "dtInteger", "dkContinuous"),
    ("Track_Score", "dtFloat", "dkContinuous"),
    ("Spotify_Streams", "dtString", "dkDiscrete"),
    ("Spotify_Playlist_Count", "dtString", "dkDiscrete"),
    ("Spotify_Playlist_Reach", "dtString", "dkDiscrete"),
    ("YouTube_Views", "dtString", "dkDiscrete"),
    ("YouTube_Likes", "dtString", "dkDiscrete"),
    ("TikTok_Posts", "dtString", "dkDiscrete"),
    ("TikTok_Likes", "dtString", "dkDiscrete"),
    ("TikTok_Views", "dtString", "dkDiscrete"),
    ("YouTube_Playlist_Reach", "dtString", "dkDiscrete"),
    ("Apple_Music_Playlist_Count", "dtFloat", "dkContinuous"),
    ("AirPlay_Spins", "dtString", "dkDiscrete"),
    ("SiriusXM_Spins", "dtFloat", "dkContinuous"),
    ("Deezer_Playlist_Count", "dtFloat", "dkContinuous"),
    ("Deezer_Playlist_Reach", "dtString", "dkDiscrete"),
    ("Amazon_Playlist_Count", "dtFloat", "dkContinuous"),
    ("Pandora_Streams", "dtString", "dkDiscrete"),
    ("Pandora_Track_Stations", "dtString", "dkDiscrete"),
    ("Soundcloud_Streams", "dtString", "dkDiscrete"),
    ("Shazam_Counts", "dtString", "dkDiscrete"),
    ("TIDAL_Popularity", "dtString", "dkDiscrete"),
    ("Explicit_Track", "dtInteger", "dkContinuous"),
    ("region", "dtString", "dkDiscrete"),
    ("market_size", "dtString", "dkDiscrete"),
    ("q_popularity", "dtInteger", "dkDiscrete"),
    ("q_streams", "dtInteger", "dkDiscrete"),
    ("q_track_score", "dtInteger", "dkDiscrete"),
]


def cleanup_output_columns() -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for name, dtype, dkind in IMPORT_COLUMNS:
        if name in TEXT_COLUMNS:
            out.append((name, "dtString", "dkDiscrete"))
        elif name in ("IsTestSet", "IsHit", "q_popularity", "q_streams", "q_track_score"):
            out.append((name, dtype, dkind))
        elif dtype == "dtString":
            out.append((name, "dtFloat", "dkContinuous"))
        else:
            out.append((name, dtype, dkind))
    return out


CLEANUP_OUTPUT_COLUMNS = cleanup_output_columns()

MODEL_INPUT_NODE_EMPTY = (
    '\t\t\t\t\t\t\t\t\t<Item __derived="true" __baseGuid="21a614fa-ff55-4464-83ec-778470325b7e" '
    'GlobalNodeID="9bd3da85-f419-4f1a-b024-6e3aab33f09a"/>'
)

META_INPUT_SOCKETS_BLOCK_RE = re.compile(
    r"\t\t\t\t\t<InputSockets xsi:type=\"TBGModelGenericInputSocketItems\.DerivedSchemeType\" __derived=\"true\">\s*"
    r"\t\t\t\t\t\t<Item __derived=\"true\" __baseGuid=\"f68189c9-46bb-478d-80b4-4054b45784e9\">[\s\S]*?"
    r"\t\t\t\t\t</InputSockets>\s*",
)

MODEL_INPUT_NODE_RE = re.compile(
    r'\t\t\t\t\t\t\t\t\t<Item __derived="true" __baseGuid="21a614fa-ff55-4464-83ec-778470325b7e" '
    r'GlobalNodeID="9bd3da85-f419-4f1a-b024-6e3aab33f09a">[\s\S]*?'
    r"\t\t\t\t\t\t\t\t\t</Item>",
)

IMPORT_ENGINE_RE = re.compile(
    r'\t\t\t\t\t<Engine xsi:type="TBGImportTextFile" FileName="[^"]*data/данные\.txt"[^>]*/>\s*'
    r"|\t\t\t\t\t<Engine xsi:type=\"TBGImportTextFile\" FileName=\"[^\"]*data/данные\.txt\"[^>]*>"
    r"[\s\S]*?\t\t\t\t\t</Engine>",
)

CLEAN_NODE_RE = re.compile(
    rf'<Item Guid="{CLEAN_GUID}"[\s\S]*?</Item>\s*(?=<Item Guid="{SCALER_GUID}")',
)

COLUMN_DEFS_RE = re.compile(r"<ColumnDefs(?:/>|>\s*[\s\S]*?</ColumnDefs>)")

OLD_PREPARE_SNIPPET = (
    "if isinstance(OutputTable, builtin_data.ConfigurableOutputTableClass):&#10;"
    "    if OutputTable.ColumnCount == 0:&#10;"
    "        prepare_compatible_table(OutputTable, output_frame, with_index=False)"
)

NEW_PREPARE_SNIPPET = (
    "if isinstance(OutputTable, builtin_data.ConfigurableOutputTableClass):&#10;"
    "    prepare_compatible_table(OutputTable, output_frame, with_index=False)"
)


def column_items(columns: list[tuple[str, str, str]], indent: str) -> str:
    return "\n".join(
        f'{indent}<Item Name="{name}" DataType="{dtype}" DataKind="{dkind}" UsageType="utActive"/>'
        for name, dtype, dkind in columns
    )


def column_defs_block(columns: list[tuple[str, str, str]], indent: str) -> str:
    items = column_items(columns, indent + "\t")
    return f"{indent}<ColumnDefs>\n{items}\n{indent}</ColumnDefs>"


def import_engine_xml() -> str:
    items = column_items(IMPORT_COLUMNS, "\t\t\t\t\t\t\t")
    return (
        f'\t\t\t\t\t<Engine xsi:type="TBGImportTextFile" FileName="{DATA_FILE}" CodePage="65001">\n'
        f"\t\t\t\t\t\t<ColumnDefs>\n{items}\n\t\t\t\t\t\t</ColumnDefs>\n"
        f"\t\t\t\t\t</Engine>"
    )


def import_node_xml() -> str:
    out_cols = column_defs_block(IMPORT_COLUMNS, "\t\t\t\t\t\t\t\t")
    return f"""
\t\t\t<Item Guid="{IMPORT_GUID}" DisplayName="Импорт data/данные.txt" VendorGuid="dd767700-1321-4c70-ab92-2acfc4db4492" GenerateNodeTitle="false">
\t\t\t\t<InputPorts>
\t\t\t\t\t<Item Guid="78ce58f4-e818-3754-bc2e-6af868677420" Name="Connection" DisplayName="Подключение"/>
\t\t\t\t\t<Item Guid="455b65c3-0587-3a9c-b47e-9b0d285bff3c" Name="ControlVariables" DisplayName="Управляющие переменные"/>
\t\t\t\t</InputPorts>
\t\t\t\t<OutputPorts>
\t\t\t\t\t<Item Guid="{PORT_DATASET}" Name="DataSet" DisplayName="Набор данных"/>
\t\t\t\t</OutputPorts>
\t\t\t\t<ServiceInputPorts>
\t\t\t\t\t<Item Guid="00bd0b43-e4b5-3ac1-b95a-ac1bee14f858" Name="SynchronizationInputPort" DisplayName="Порядок выполнения"/>
\t\t\t\t</ServiceInputPorts>
\t\t\t\t<ServiceOutputPorts>
\t\t\t\t\t<Item Guid="ca080ff0-2342-32b0-b480-586f9747bace" Name="SynchronizationOutputPort" DisplayName="Порядок выполнения"/>
\t\t\t\t\t<Item Guid="e98be5ba-c627-3a55-af82-a399dd13c73b" Name="ComponentOutputPort" DisplayName="Компонент"/>
\t\t\t\t\t<Item Guid="58922a98-d1ea-36de-9099-3ce26fe160e2" Name="DependentNodeOutputPort" DisplayName="Зависимые узлы"/>
\t\t\t\t</ServiceOutputPorts>
\t\t\t\t<Component>
\t\t\t\t\t<InputSockets>
\t\t\t\t\t\t<Item Guid="78ce58f4-e818-3754-bc2e-6af868677420" Name="Connection" DisplayName="Подключение">
\t\t\t\t\t\t\t<Socket xsi:type="TBGConnectionInputSocket" Virgin="true">
\t\t\t\t\t\t\t\t<Constraints/>
\t\t\t\t\t\t\t</Socket>
\t\t\t\t\t\t</Item>
\t\t\t\t\t\t<Item Guid="455b65c3-0587-3a9c-b47e-9b0d285bff3c" Name="ControlVariables" DisplayName="Управляющие переменные">
\t\t\t\t\t\t\t<Socket xsi:type="TBGTuneVariablesSocket" Virgin="true">
\t\t\t\t\t\t\t\t<Constraints/>
\t\t\t\t\t\t\t\t<Variables SyncThroughVariables="true">
\t\t\t\t\t\t\t\t\t<Elements/>
\t\t\t\t\t\t\t\t</Variables>
\t\t\t\t\t\t\t</Socket>
\t\t\t\t\t\t</Item>
\t\t\t\t\t</InputSockets>
\t\t\t\t\t<OutputSockets>
\t\t\t\t\t\t<Item Guid="{PORT_DATASET}" Name="DataSet" DisplayName="Набор данных">
\t\t\t\t\t\t\t<Socket xsi:type="TBGDataSetOutputSocket">
\t\t\t\t\t\t\t\t<DataSource SyncThroughColumns="true">
{out_cols}
\t\t\t\t\t\t\t\t</DataSource>
\t\t\t\t\t\t\t</Socket>
\t\t\t\t\t\t</Item>
\t\t\t\t\t</OutputSockets>
{import_engine_xml()}
\t\t\t\t</Component>
\t\t\t\t<Position Left="24" Top="200"/>
\t\t\t</Item>"""


def meta_input_sockets_block() -> str:
    cols = column_defs_block(CLEANUP_OUTPUT_COLUMNS, "\t\t\t\t\t\t\t\t")
    return f"""\t\t\t\t\t<InputSockets xsi:type="TBGModelGenericInputSocketItems.DerivedSchemeType" __derived="true">
\t\t\t\t\t\t<Item __derived="true" __baseGuid="f68189c9-46bb-478d-80b4-4054b45784e9">
\t\t\t\t\t\t\t<Socket xsi:type="TBGTuneDataSourceSocket.DerivedSchemeType" __derived="true">
\t\t\t\t\t\t\t\t<DataSource __derived="true" SyncThroughColumns="true">
{cols}
\t\t\t\t\t\t\t\t</DataSource>
\t\t\t\t\t\t\t</Socket>
\t\t\t\t\t\t</Item>
\t\t\t\t\t</InputSockets>
"""


def model_input_node_block() -> str:
    cols = column_defs_block(CLEANUP_OUTPUT_COLUMNS, "\t\t\t\t\t\t\t\t\t\t\t\t\t")
    return (
        '\t\t\t\t\t\t\t\t\t<Item __derived="true" __baseGuid="21a614fa-ff55-4464-83ec-778470325b7e" '
        'GlobalNodeID="9bd3da85-f419-4f1a-b024-6e3aab33f09a">\n'
        "\t\t\t\t\t\t\t\t\t\t<Component __derived=\"true\">\n"
        "\t\t\t\t\t\t\t\t\t\t\t<InputSockets __derived=\"true\">\n"
        '\t\t\t\t\t\t\t\t\t\t\t\t<Item __derived="true" __baseGuid="9dc72a3f-56bf-3bfc-84ec-f979daf4da6b">\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t<Socket xsi:type="TBGTuneDataSourceSocket.DerivedSchemeType" __derived="true">\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t<DataSource __derived="true" SyncThroughColumns="true">\n'
        f"{cols}\n"
        "\t\t\t\t\t\t\t\t\t\t\t\t\t\t</DataSource>\n"
        "\t\t\t\t\t\t\t\t\t\t\t\t\t</Socket>\n"
        "\t\t\t\t\t\t\t\t\t\t\t\t</Item>\n"
        "\t\t\t\t\t\t\t\t\t\t\t</InputSockets>\n"
        "\t\t\t\t\t\t\t\t\t\t</Component>\n"
        "\t\t\t\t\t\t\t\t\t</Item>"
    )


def revert_meta_scaling(text: str) -> str:
    """Stock meta-scaling: no Component-level InputSockets (see lr9_check/pathfix)."""
    text, _ = META_INPUT_SOCKETS_BLOCK_RE.subn("", text)
    text, _ = MODEL_INPUT_NODE_RE.subn(MODEL_INPUT_NODE_EMPTY, text, count=1)
    return text


def replace_socket_columns(block: str, section: str, item_marker: str, replacement: str) -> str:
    sec_m = re.search(rf"<{section}>([\s\S]*?)</{section}>", block)
    if not sec_m:
        raise RuntimeError(f"{section} not found in cleanup node")
    section_body = sec_m.group(1)
    pat = (
        rf"({re.escape(item_marker)}[\s\S]*?<DataSource SyncThroughColumns=\"true\">\s*)"
        + COLUMN_DEFS_RE.pattern
    )
    new_body, n = re.subn(pat, rf"\1{replacement}", section_body, count=1)
    if n != 1:
        raise RuntimeError(f"ColumnDefs replace failed in {section}")
    return block[: sec_m.start(1)] + new_body + block[sec_m.end(1) :]


def patch_cleanup_node(text: str) -> str:
    m = CLEAN_NODE_RE.search(text)
    if not m:
        raise RuntimeError("cleanup node not found")

    block = m.group(0)
    out_cols = column_defs_block(CLEANUP_OUTPUT_COLUMNS, "\t\t\t\t\t\t\t\t")

    block = replace_socket_columns(
        block,
        "OutputSockets",
        '<Item Guid="58f7e6c3-511e-39d7-8853-036e0a1a7612" Name="DataSet"',
        out_cols.strip(),
    )
    block = replace_socket_columns(
        block,
        "InputSockets",
        '<Item Guid="9dc72a3f-56bf-3bfc-84ec-f979daf4da6b" Name="DataSource"',
        "<ColumnDefs/>",
    )
    block = re.sub(
        rf"(<Engine xsi:type=\"TBGPythonEngine\"[\s\S]*?){COLUMN_DEFS_RE.pattern}",
        r"\1<ColumnDefs/>",
        block,
        count=1,
    )

    if OLD_PREPARE_SNIPPET in block:
        block = block.replace(OLD_PREPARE_SNIPPET, NEW_PREPARE_SNIPPET, 1)
    else:
        raise RuntimeError("cleanup Python prepare snippet not found")

    return text[: m.start()] + block + text[m.end() :]


def fill_import_output_cols(text: str) -> str:
    if IMPORT_GUID not in text:
        return text
    start = text.find(f'Item Guid="{IMPORT_GUID}"')
    end = text.find(f'Item Guid="{CLEAN_GUID}"', start)
    block = text[start:end]
    out_cols = column_defs_block(IMPORT_COLUMNS, "\t\t\t\t\t\t\t\t").strip()
    block = replace_socket_columns(
        block,
        "OutputSockets",
        f'<Item Guid="{PORT_DATASET}" Name="DataSet"',
        out_cols,
    )
    return text[:start] + block + text[end:]


def patch_dataset_import(text: str) -> str:
    if IMPORT_GUID in text:
        text, n = IMPORT_ENGINE_RE.subn(import_engine_xml(), text, count=1)
        if n != 1:
            raise RuntimeError(f"import engine replace: {n} (expected 1)")
        text = fill_import_output_cols(text)
    else:
        anchor = f'\t\t\t<Item Guid="{CLEAN_GUID}"'
        if anchor not in text:
            raise RuntimeError("cleanup node anchor not found")
        text = text.replace(anchor, import_node_xml() + anchor, 1)

    old_src = f'<SourcePort NodeGuid="{REF_GUID}" PortGuid="4ba0e2c2-69ad-3a32-bbdc-75714efe7a51"/>'
    new_src = f'<SourcePort NodeGuid="{IMPORT_GUID}" PortGuid="{PORT_DATASET}"/>'
    if old_src in text:
        text = text.replace(old_src, new_src, 1)
    elif new_src not in text:
        raise RuntimeError("dataset link not patched")

    note = (
        '\t\t\t<Item Guid="c7d6e5f4-a3b2-4291-8c7d-6e5f4a3b2c1e" StyleNum="6" '
        'Text="Импорт data/данные.txt — файл создаётся сценарием «Подготовка выборок». '
        'Unit_1 можно запускать после одного успешного прогона Unit_0.">\n'
        '\t\t\t\t<Position Left="24" Top="120" Width="360" Height="48"/>\n'
        '\t\t\t\t</Item>\n'
    )
    if "c7d6e5f4-a3b2-4291-8c7d-6e5f4a3b2c1e" not in text:
        text = text.replace("\t\t</Annotations>", note + "\n\t\t</Annotations>", 1)

    return text


def patch_unit1(text: str) -> str:
    text = patch_cleanup_node(text)
    text = revert_meta_scaling(text)
    return patch_dataset_import(text)
