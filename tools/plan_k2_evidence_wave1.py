#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path

import validate_k2_evidence as v

ROOT = Path(__file__).resolve().parents[1]


def execution_lane(source):
    readability = source.get("readability")
    if readability == "TEXT_OK":
        return "TEXT_DIRECT"
    if readability in {"SCAN", "OCR_WEAK", "OCR_FAIL"}:
        return "VISUAL_REQUIRED"
    return "ACCESS_REVIEW"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=ROOT)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo_root.resolve()
    sources = v.source_index(repo)
    lineage = v.lineage_index(repo)
    selected = v.wave1_expected(sources, lineage)
    rows = []
    lanes = Counter()
    for sid in sorted(selected):
        source = sources[sid]
        lin = lineage[sid]
        lane = execution_lane(source)
        lanes[lane] += 1
        rows.append(
            {
                "source_id": sid,
                "work_id": lin.get("work_id"),
                "relation": lin.get("relation"),
                "read_priority": lin.get("read_priority"),
                "knowledge_domains": source.get("knowledge_domains"),
                "title": source.get("title"),
                "pages": source.get("pages"),
                "readability": source.get("readability"),
                "copyright": source.get("copyright"),
                "execution_lane": lane,
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print("k2-wave1-plan: PASS")
    print(f"selected_reading_units={len(rows)} output={args.output}")
    print("execution_lanes=" + json.dumps(dict(sorted(lanes.items())), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
