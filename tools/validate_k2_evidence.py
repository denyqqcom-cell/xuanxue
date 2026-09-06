#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

import k2_wave1_aggregate as agg
import validate_k2_evidence_base as base
import k2_execution_routing as routing

routing.patch_validator_module(base)
from validate_k2_evidence_base import *  # re-export validator contract helpers for tests/importers

ROOT = Path(__file__).resolve().parents[1]
aggregate_wave1 = agg.aggregate_wave1
apply_verified_source_metadata = routing.apply_verified_source_metadata
load_execution_routing_corrections = routing.load_execution_routing_corrections

# Reading lifecycle state and execution-attempt diagnostics are separate. A
# transient local/runtime limitation must never become a source-level terminal
# BLOCKED row merely because the legacy validator has a blocker_code field.
EXECUTION_ONLY_BLOCKER_CODES = {
    "FILE_MISSING",
    "VISION_UNAVAILABLE",
    "TEXT_EXTRACTOR_STACK_UNAVAILABLE",
    "TEXT_EXTRACTION_FAILED",
    "TEXT_LAYER_UNUSABLE",
    "ACCESS_UNAVAILABLE",
}
TERMINAL_SOURCE_BLOCKER_CODES = {"CORRUPT_SOURCE"}

# validate_k2_evidence_base.main() performs the authoritative BLOCKED-row check
# against its module-level BLOCKER_CODES. Narrow that accepted set before main()
# runs, while retaining the execution-only taxonomy here for diagnostics/tests.
BLOCKER_CODES = set(TERMINAL_SOURCE_BLOCKER_CODES)
base.BLOCKER_CODES = set(TERMINAL_SOURCE_BLOCKER_CODES)


def read_blocker_scope(code):
    if code in TERMINAL_SOURCE_BLOCKER_CODES:
        return "SOURCE_TERMINAL"
    if code in EXECUTION_ONLY_BLOCKER_CODES:
        return "EXECUTION_ONLY"
    return "UNSUPPORTED"


def _write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    ledger, evidence, distillates = aggregate_wave1(repo)

    with tempfile.TemporaryDirectory(prefix="k2-evidence-authoritative-") as tmp:
        tmp_root = Path(tmp)
        shutil.copytree(repo / "knowledge", tmp_root / "knowledge")
        k = tmp_root / "knowledge"
        _write_jsonl(k / agg.BASE_LEDGER, ledger)
        _write_jsonl(k / agg.BASE_EVIDENCE, evidence)
        _write_jsonl(k / agg.BASE_DISTILLATES, distillates)
        for directory in agg.SHARD_DIRS.values():
            shutil.rmtree(k / directory, ignore_errors=True)

        previous_argv = sys.argv
        try:
            sys.argv = [str(Path(__file__).name), "--repo-root", str(tmp_root)]
            if args.force:
                sys.argv.append("--force")
            base.main()
        finally:
            sys.argv = previous_argv


if __name__ == "__main__":
    main()
