#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

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
    print(f"k2-per-book-completion: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


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


def validate_shard_rows(kind, path, rows):
    source_id = path.stem
    if not rows:
        fail(f"empty {kind} shard: {path.relative_to(ROOT)}")
    if kind in {"ledger", "distillate"} and len(rows) != 1:
        fail(f"{kind} shard must contain exactly one row: {path.relative_to(ROOT)}")
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
        source_id = validate_shard_rows(kind, path, rows)
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


def aggregate(root=ROOT):
    k = root / "knowledge"
    base_ledger = load_jsonl(k / BASE_LEDGER)
    base_evidence = load_jsonl(k / BASE_EVIDENCE)
    base_distillates = load_jsonl(k / BASE_DISTILLATES)

    shard_ledger, ledger_sources = collect_shards("ledger", root)
    shard_evidence, evidence_sources = collect_shards("evidence", root)
    shard_distillates, distillate_sources = collect_shards("distillate", root)

    base_ledger_sources = {r.get("source_id") for r in base_ledger}
    duplicate_read_sources = base_ledger_sources.intersection(ledger_sources)
    if duplicate_read_sources:
        fail(f"Reading source already exists in base and shard: {sorted(duplicate_read_sources)}")
    if len(ledger_sources) != len(set(ledger_sources)):
        fail("duplicate source represented by multiple Reading shards")
    if len(distillate_sources) != len(set(distillate_sources)):
        fail("duplicate source represented by multiple Distillate shards")

    ledger = base_ledger + shard_ledger
    evidence = base_evidence + shard_evidence
    distillates = base_distillates + shard_distillates

    ensure_unique(ledger, ID_FIELDS["ledger"], "ledger")
    ensure_unique(evidence, ID_FIELDS["evidence"], "evidence")
    ensure_unique(distillates, ID_FIELDS["distillate"], "distillates")

    ledger_sources_all = {r.get("source_id") for r in ledger}
    for source_id in evidence_sources:
        if source_id not in ledger_sources_all:
            fail(f"Evidence shard has no aggregate Reading row: {source_id}")
    for source_id in distillate_sources:
        if source_id not in ledger_sources_all:
            fail(f"Distillate shard has no aggregate Reading row: {source_id}")

    return ledger, evidence, distillates


def write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def run_existing_evidence_validator(ledger, evidence):
    with tempfile.TemporaryDirectory(prefix="k2-per-book-") as tmp:
        tmp_root = Path(tmp)
        shutil.copytree(K, tmp_root / "knowledge")
        write_jsonl(tmp_root / "knowledge" / BASE_LEDGER, ledger)
        write_jsonl(tmp_root / "knowledge" / BASE_EVIDENCE, evidence)
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_k2_evidence.py"),
                "--repo-root",
                str(tmp_root),
                "--force",
            ],
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            message = (proc.stderr or proc.stdout).strip().replace("\n", " | ")
            fail(f"aggregate Evidence validator rejected union: {message}")
        return proc.stdout.strip()


def run_distillate_validator(ledger, evidence, distillates):
    sys.path.insert(0, str(ROOT / "tools"))
    import validate_k2_book_distillates as distillate_validator

    issues = distillate_validator.validate_rows(ledger, evidence, distillates)
    if issues:
        first = issues[0]
        fail(f"aggregate Book Distillate issues={len(issues)} first={first[0]}: {first[1]}")


def main():
    project = json.loads((K / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    if project.get("phase") != "K2_EVIDENCE_EXTRACTION":
        fail("aggregate completion gate only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:
        fail("Claim Extraction must remain blocked")

    ledger, evidence, distillates = aggregate(ROOT)
    evidence_output = run_existing_evidence_validator(ledger, evidence)
    run_distillate_validator(ledger, evidence, distillates)

    complete = sum(1 for row in ledger if row.get("read_status") == "COMPLETE")
    partial = sum(1 for row in ledger if row.get("read_status") == "PARTIAL")
    blocked = sum(1 for row in ledger if row.get("read_status") == "BLOCKED")

    print("k2-per-book-completion: PASS")
    print(
        f"aggregate ledger_rows={len(ledger)} evidence_rows={len(evidence)} "
        f"distillates={len(distillates)} complete={complete} partial={partial} blocked={blocked}"
    )
    print("claim_extraction_blocked=true")
    for line in evidence_output.splitlines():
        if line.startswith("expected_reading_units=") or line.startswith("execution_lanes="):
            print(f"evidence_gate {line}")


if __name__ == "__main__":
    main()
