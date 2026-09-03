#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

import k2_wave1_aggregate as agg
import validate_k2_composite_source_closures as composite_closure_validator

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

BASE_LEDGER = agg.BASE_LEDGER
BASE_EVIDENCE = agg.BASE_EVIDENCE
BASE_DISTILLATES = agg.BASE_DISTILLATES
SHARD_DIRS = agg.SHARD_DIRS
ID_FIELDS = agg.ID_FIELDS
aggregate = agg.aggregate_wave1
ensure_unique = agg.ensure_unique


def fail(msg):
    print(f"k2-per-book-completion: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def run_existing_evidence_validator(root=ROOT):
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "validate_k2_evidence.py"),
            "--repo-root",
            str(root),
            "--force",
        ],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout).strip().replace("\n", " | ")
        fail(f"aggregate Evidence validator rejected authoritative view: {message}")
    return proc.stdout.strip()


def run_distillate_validator(ledger, evidence, distillates):
    sys.path.insert(0, str(ROOT / "tools"))
    import validate_k2_book_distillates as distillate_validator

    issues = distillate_validator.validate_rows(ledger, evidence, distillates)
    if issues:
        first = issues[0]
        fail(f"aggregate Book Distillate issues={len(issues)} first={first[0]}: {first[1]}")


def run_composite_closure_validator(root=ROOT):
    try:
        return composite_closure_validator.valid_closure_source_ids(root)
    except ValueError as exc:
        fail(f"composite source closure rejected: {exc}")


def main():
    project = json.loads((K / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    if project.get("phase") != "K2_EVIDENCE_EXTRACTION":
        fail("aggregate completion gate only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:
        fail("Claim Extraction must remain blocked")

    ledger, evidence, distillates = aggregate(ROOT)
    evidence_output = run_existing_evidence_validator(ROOT)
    run_distillate_validator(ledger, evidence, distillates)
    composite_closed = run_composite_closure_validator(ROOT)

    complete = sum(1 for row in ledger if row.get("read_status") == "COMPLETE")
    partial = sum(1 for row in ledger if row.get("read_status") == "PARTIAL")
    blocked = sum(1 for row in ledger if row.get("read_status") == "BLOCKED")

    print("k2-per-book-completion: PASS")
    print(
        f"aggregate ledger_rows={len(ledger)} evidence_rows={len(evidence)} "
        f"distillates={len(distillates)} complete={complete} partial={partial} blocked={blocked}"
    )
    print(f"composite_execution_closed={len(composite_closed)}")
    print("legacy_wave1_completion_semantics=unchanged")
    print("claim_extraction_blocked=true")
    for line in evidence_output.splitlines():
        if line.startswith("expected_reading_units=") or line.startswith("execution_lanes="):
            print(f"evidence_gate {line}")


if __name__ == "__main__":
    main()
