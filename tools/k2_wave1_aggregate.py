#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE_LEDGER = "K2_READING_LEDGER_WAVE1.jsonl"
BASE_EVIDENCE = "K2_EVIDENCE_WAVE1.jsonl"
BASE_DISTILLATES = "K2_BOOK_DISTILLATES_WAVE1.jsonl"

SHARD_DIRS = {
    "ledger": "K2_READING_LEDGER_WAVE1.d",
    "evidence": "K2_EVIDENCE_WAVE1.d",
    "distillate": "K2_BOOK_DISTILLATES_WAVE1.d",
}

ID_FIELDS = {
    "ledger": "reading_id",
    "evidence": "evidence_id",
    "distillate": "distillate_id",
}


def fail(msg):
    print(f"k2-wave1-aggregate: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def display_path(path, root=ROOT):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            fail(f"invalid JSONL {path}:{line_no}: {exc}")
        if not isinstance(row, dict):
            fail(f"row must be object {path}:{line_no}")
        rows.append(row)
    return rows


def validate_shard_rows(kind, path, rows, root=ROOT):
    source_id = path.stem
    if not rows:
        fail(f"empty {kind} shard: {display_path(path, root)}")
    if kind in {"ledger", "distillate"} and len(rows) != 1:
        fail(f"{kind} shard must contain exactly one row: {display_path(path, root)}")
    for row in rows:
        if row.get("source_id") != source_id:
            fail(
                f"{kind} shard/source mismatch: file={source_id} row={row.get('source_id')}"
            )
    return source_id


def collect_shards(kind, root=ROOT):
    shard_dir = root / "knowledge" / SHARD_DIRS[kind]
    out = []
    source_ids = []
    if not shard_dir.exists():
        return out, source_ids
    for path in sorted(shard_dir.glob("*.jsonl")):
        rows = load_jsonl(path)
        source_id = validate_shard_rows(kind, path, rows, root)
        out.extend(rows)
        source_ids.append(source_id)
    return out, source_ids


def ensure_unique(rows, id_field, label):
    seen = set()
    for row in rows:
        value = row.get(id_field)
        if not isinstance(value, str) or not value.strip():
            fail(f"{label}: missing {id_field}")
        if value in seen:
            fail(f"{label}: duplicate {id_field}: {value}")
        seen.add(value)


def ensure_unique_source(rows, label):
    seen = set()
    for row in rows:
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            fail(f"{label}: missing source_id")
        if source_id in seen:
            fail(f"{label}: duplicate source_id: {source_id}")
        seen.add(source_id)


def _source_set(rows):
    return {row.get("source_id") for row in rows if isinstance(row.get("source_id"), str)}


def _reject_split_storage(kind, base_rows, shard_sources):
    overlap = _source_set(base_rows).intersection(shard_sources)
    if overlap:
        fail(f"{kind} source already exists in base and shard: {sorted(overlap)}")


def aggregate_wave1(root=ROOT):
    root = Path(root).resolve()
    k = root / "knowledge"

    base_ledger = load_jsonl(k / BASE_LEDGER)
    base_evidence = load_jsonl(k / BASE_EVIDENCE)
    base_distillates = load_jsonl(k / BASE_DISTILLATES)

    shard_ledger, ledger_sources = collect_shards("ledger", root)
    shard_evidence, evidence_sources = collect_shards("evidence", root)
    shard_distillates, distillate_sources = collect_shards("distillate", root)

    if len(ledger_sources) != len(set(ledger_sources)):
        fail("duplicate source represented by multiple Reading shards")
    if len(evidence_sources) != len(set(evidence_sources)):
        fail("duplicate source represented by multiple Evidence shards")
    if len(distillate_sources) != len(set(distillate_sources)):
        fail("duplicate source represented by multiple Distillate shards")

    _reject_split_storage("Reading", base_ledger, ledger_sources)
    _reject_split_storage("Evidence", base_evidence, evidence_sources)
    _reject_split_storage("Distillate", base_distillates, distillate_sources)

    ledger = base_ledger + shard_ledger
    evidence = base_evidence + shard_evidence
    distillates = base_distillates + shard_distillates

    ensure_unique(ledger, ID_FIELDS["ledger"], "ledger")
    ensure_unique(evidence, ID_FIELDS["evidence"], "evidence")
    ensure_unique(distillates, ID_FIELDS["distillate"], "distillates")
    ensure_unique_source(ledger, "ledger")
    ensure_unique_source(distillates, "distillates")

    ledger_sources_all = _source_set(ledger)
    for source_id in _source_set(evidence):
        if source_id not in ledger_sources_all:
            fail(f"Evidence has no aggregate Reading row: {source_id}")
    for source_id in _source_set(distillates):
        if source_id not in ledger_sources_all:
            fail(f"Distillate has no aggregate Reading row: {source_id}")

    return ledger, evidence, distillates
