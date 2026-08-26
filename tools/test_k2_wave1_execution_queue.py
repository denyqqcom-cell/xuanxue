#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import generate_k2_wave1_execution_queue as q

LANE_ORDER = {"TEXT_DIRECT": 0, "VISUAL_REQUIRED": 1, "ACCESS_REVIEW": 2}


def semantic_sort_key(row):
    return (
        q.DOMAIN_ORDER.get(row["domain"], 99),
        LANE_ORDER[row["execution_lane"]],
        row["source_id"],
    )


def main():
    rows = q.build_queue(ROOT)
    source_ids = [row["source_id"] for row in rows]
    assert len(source_ids) == len(set(source_ids)), "duplicate source_id in execution queue"

    sources = q.evidence.source_index(ROOT)
    lineage = q.evidence.lineage_index(ROOT)
    expected = q.evidence.wave1_expected(sources, lineage)
    completed = q.completed_source_ids(ROOT)
    assert set(source_ids) == expected - completed, (
        "queue must equal authoritative Wave1 selection minus terminal COMPLETE/BLOCKED units"
    )
    assert rows == sorted(rows, key=semantic_sort_key), (
        "queue must sort by semantic domain, then execution lane, then source_id"
    )

    # Intake prefixes are not semantic domains. Verify the real corpus metadata,
    # then test ordering independently of whether these sources are still pending.
    assert q._primary_domain(sources["ZW-SRC-0036"]) == "liuren"
    assert q._primary_domain(sources["BZ-SRC-0122"]) == "liuyao"
    synthetic = [
        {"source_id": "ZW-SRC-0036", "domain": "liuren", "execution_lane": "VISUAL_REQUIRED"},
        {"source_id": "LR-SRC-0005", "domain": "liuren", "execution_lane": "TEXT_DIRECT"},
        {"source_id": "BZ-SRC-0122", "domain": "liuyao", "execution_lane": "VISUAL_REQUIRED"},
        {"source_id": "LY-SRC-0003", "domain": "liuyao", "execution_lane": "TEXT_DIRECT"},
    ]
    ordered = [row["source_id"] for row in sorted(synthetic, key=semantic_sort_key)]
    assert ordered == ["LY-SRC-0003", "BZ-SRC-0122", "LR-SRC-0005", "ZW-SRC-0036"], ordered

    required = {
        "source_id",
        "domain",
        "execution_lane",
        "relation",
        "work_id",
        "deep_reading_reusable",
        "mixed_voice_policy",
        "segmented_carrier",
        "next_action",
    }
    for row in rows:
        assert set(row) == required, row
        assert row["execution_lane"] in {"TEXT_DIRECT", "VISUAL_REQUIRED", "ACCESS_REVIEW"}
        assert isinstance(row["deep_reading_reusable"], bool)
        assert isinstance(row["segmented_carrier"], bool)
        assert row["next_action"] in {
            "REUSE_VERIFIED_DEEP_READING",
            "TEXT_PAGE_REVIEW_REQUIRED",
            "VISUAL_PAGE_REVIEW_REQUIRED",
            "ACCESS_REVIEW_REQUIRED",
        }
        if row["deep_reading_reusable"]:
            assert row["next_action"] == "REUSE_VERIFIED_DEEP_READING"

    # Progress must shrink the queue rather than break a frozen-count test.
    # Simulate one additional terminal unit without mutating repository data.
    if source_ids:
        simulated = source_ids[0]
        original_completed = q.completed_source_ids
        try:
            q.completed_source_ids = lambda root=ROOT: set(completed) | {simulated}
            future_rows = q.build_queue(ROOT)
        finally:
            q.completed_source_ids = original_completed
        future_ids = {row["source_id"] for row in future_rows}
        assert future_ids == set(source_ids) - {simulated}
        assert len(future_rows) == len(rows) - 1

    reusable = [row for row in rows if row["deep_reading_reusable"]]

    print("k2-wave1-execution-queue-tests: PASS")
    print(f"remaining={len(rows)} deep_reusable={len(reusable)}")
    for row in rows:
        print("queue=" + json.dumps(row, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
