#!/usr/bin/env python3
import json
from pathlib import Path

import k2_wave1_aggregate as agg
import validate_k2_evidence_base as evidence

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

DOMAIN_ORDER = {
    "ziwei": 0,
    "bazi": 1,
    "qimen": 2,
    "liuyao": 3,
    "liuren": 4,
    "fengshui": 5,
}
PREFIX_DOMAIN = {
    "ZW": "ziwei",
    "BZ": "bazi",
    "QM": "qimen",
    "LY": "liuyao",
    "LR": "liuren",
    "FS": "fengshui",
}


def load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        if not isinstance(row, dict):
            raise ValueError(f"row must be object: {path}:{line_no}")
        rows.append(row)
    return rows


def queue_sort_key(source_id):
    prefix = str(source_id).split("-", 1)[0]
    domain = PREFIX_DOMAIN.get(prefix, "")
    return (DOMAIN_ORDER.get(domain, 99), str(source_id))


def completed_source_ids(root=ROOT):
    ledger, _, _ = agg.aggregate_wave1(root)
    return {
        row.get("source_id")
        for row in ledger
        if row.get("read_status") in {"COMPLETE", "BLOCKED"}
    }


def _deep_complete(root):
    rows = load_jsonl(Path(root) / "knowledge" / "K2_DEEP_READING_LEDGER.jsonl")
    return {
        row.get("source_id")
        for row in rows
        if row.get("read_status") == "COMPLETE"
        and row.get("review_status") == "REVIEWED"
        and row.get("verification_mode") in {"VISUAL_PAGE", "TEXT_LAYER_FULL", "WHOLE_TEXT_DOCUMENT"}
    }


def _holds(root):
    rows = load_jsonl(Path(root) / "knowledge" / "K2_MIXED_VOICE_HOLDS.jsonl")
    return {row.get("source_id"): row.get("hold_policy") for row in rows if row.get("source_id")}


def _segmented_sources(root):
    rows = load_jsonl(Path(root) / "knowledge" / "K2_SOURCE_SEGMENTS.jsonl")
    return {row.get("source_id") for row in rows if row.get("source_id")}


def _primary_domain(source):
    domains = source.get("knowledge_domains") or []
    governed = [d for d in domains if d in DOMAIN_ORDER]
    if not governed:
        return "unknown"
    return sorted(governed, key=lambda d: DOMAIN_ORDER[d])[0]


def build_queue(root=ROOT):
    root = Path(root).resolve()
    sources = evidence.source_index(root)
    lineage = evidence.lineage_index(root)
    expected = evidence.wave1_expected(sources, lineage)
    completed = completed_source_ids(root)
    deep = _deep_complete(root)
    holds = _holds(root)
    segmented = _segmented_sources(root)

    rows = []
    for source_id in sorted(expected - completed, key=queue_sort_key):
        src = sources[source_id]
        lin = lineage[source_id]
        lane = evidence.expected_execution_lane(src)
        reusable = source_id in deep
        if reusable:
            next_action = "REUSE_VERIFIED_DEEP_READING"
        elif lane == "TEXT_DIRECT":
            next_action = "TEXT_PAGE_REVIEW_REQUIRED"
        elif lane == "VISUAL_REQUIRED":
            next_action = "VISUAL_PAGE_REVIEW_REQUIRED"
        else:
            next_action = "ACCESS_REVIEW_REQUIRED"

        rows.append(
            {
                "source_id": source_id,
                "domain": _primary_domain(src),
                "execution_lane": lane,
                "relation": lin.get("relation"),
                "work_id": lin.get("work_id"),
                "deep_reading_reusable": reusable,
                "mixed_voice_policy": holds.get(source_id),
                "segmented_carrier": source_id in segmented,
                "next_action": next_action,
            }
        )
    return rows


def main():
    rows = build_queue(ROOT)
    reusable = sum(1 for row in rows if row["deep_reading_reusable"])
    print("k2-wave1-execution-queue: PASS")
    print(f"remaining={len(rows)} deep_reusable={reusable}")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
