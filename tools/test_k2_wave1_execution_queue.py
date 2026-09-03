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
    legacy = q.completed_source_ids(ROOT)
    composite = q.composite_closed_source_ids(ROOT)
    resolved = q.execution_resolved_source_ids(ROOT)

    assert resolved == legacy | composite
    assert set(source_ids) == expected - resolved, (
        "queue must equal authoritative Wave1 selection minus "
        "legacy terminal units and validated composite-exception execution closures"
    )
    assert rows == sorted(rows, key=semantic_sort_key)

    # Composite closure does not mutate legacy completion semantics.
    assert q.completed_source_ids(ROOT) == legacy

    assert q._primary_domain(sources["ZW-SRC-0036"]) == "liuren"
    assert q._primary_domain(sources["BZ-SRC-0122"]) == "liuyao"

    required = {
        "source_id","domain","execution_lane","relation","work_id",
        "deep_reading_reusable","mixed_voice_policy","segmented_carrier","next_action",
    }
    for row in rows:
        assert set(row) == required,row
        assert row["execution_lane"] in {"TEXT_DIRECT","VISUAL_REQUIRED","ACCESS_REVIEW"}
        assert isinstance(row["deep_reading_reusable"],bool)
        assert isinstance(row["segmented_carrier"],bool)
        assert row["next_action"] in {
            "REUSE_VERIFIED_DEEP_READING",
            "TEXT_PAGE_REVIEW_REQUIRED",
            "VISUAL_PAGE_REVIEW_REQUIRED",
            "ACCESS_REVIEW_REQUIRED",
        }

    # Legacy terminal progress shrinks the actionable queue.
    if source_ids:
        simulated=source_ids[0]
        original=q.completed_source_ids
        try:
            q.completed_source_ids=lambda root=ROOT:set(legacy)|{simulated}
            future=q.build_queue(ROOT)
        finally:
            q.completed_source_ids=original
        assert {r["source_id"] for r in future}==set(source_ids)-{simulated}

    # Composite-exception closure also shrinks the actionable queue,
    # without pretending to add a legacy COMPLETE row.
    current=[r["source_id"] for r in q.build_queue(ROOT)]
    if current:
        simulated=current[0]
        original=q.composite_closed_source_ids
        try:
            q.composite_closed_source_ids=lambda root=ROOT:set(composite)|{simulated}
            future=q.build_queue(ROOT)
        finally:
            q.composite_closed_source_ids=original
        assert {r["source_id"] for r in future}==set(current)-{simulated}
        assert simulated not in legacy

    print("k2-wave1-execution-queue-tests: PASS")
    print(f"remaining={len(rows)} legacy_terminal={len(legacy)} composite_closed={len(composite)}")


if __name__ == "__main__":
    main()
