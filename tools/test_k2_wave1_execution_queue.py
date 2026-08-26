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
    assert len(rows) == 32, len(rows)

    source_ids = [row["source_id"] for row in rows]
    assert len(source_ids) == len(set(source_ids)), "duplicate source_id in execution queue"
    assert rows == sorted(rows, key=semantic_sort_key), (
        "queue must sort by semantic domain, then execution lane, then source_id"
    )

    # Intake prefixes are not semantic domains. These two real corpus rows are
    # regressions for the old prefix-based ordering bug.
    by_id = {row["source_id"]: row for row in rows}
    assert by_id["ZW-SRC-0036"]["domain"] == "liuren"
    assert by_id["BZ-SRC-0122"]["domain"] == "liuyao"
    assert source_ids.index("BZ-SRC-0122") > source_ids.index("LY-SRC-0003")
    assert source_ids.index("ZW-SRC-0036") > source_ids.index("LR-SRC-0005")

    completed = q.completed_source_ids(ROOT)
    assert not (set(source_ids) & completed), "completed Wave1 units must not remain in queue"

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

    reusable = [row for row in rows if row["deep_reading_reusable"]]

    print("k2-wave1-execution-queue-tests: PASS")
    print(f"remaining={len(rows)} deep_reusable={len(reusable)}")
    for row in rows:
        print("queue=" + json.dumps(row, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
