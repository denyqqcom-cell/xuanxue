#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

DOMAINS = {
    "ziwei": "ZW-SRC-",
    "bazi": "BZ-SRC-",
    "qimen": "QM-SRC-",
    "liuyao": "LY-SRC-",
    "liuren": "LR-SRC-",
    "fengshui": "FS-SRC-",
}
READABILITY = {"TEXT_OK", "SCAN", "OCR_WEAK", "OCR_FAIL", "UNOPENED", "METADATA_ONLY"}
STATUS = {"DISCOVERED", "INDEXED", "PARTIALLY_READ", "READ", "DUPLICATE", "BLOCKED"}
SOURCE_TYPES = {"BOOK", "COURSE", "ANCIENT_TEXT", "ARTICLE", "NOTE", "CODE", "CASE_COLLECTION", "OTHER"}
FORBIDDEN_EXT = {".pdf", ".epub", ".doc", ".docx", ".ttf", ".otf", ".woff", ".woff2", ".jpg", ".jpeg", ".png", ".webp"}
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(msg: str):
    print(f"k1-intake: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot parse {path}: {e}")


def load_jsonl(path: Path):
    rows = []
    try:
        for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except Exception as e:
                fail(f"invalid JSONL {path}:{n}: {e}")
            if not isinstance(row, dict):
                fail(f"JSONL row must be object {path}:{n}")
            rows.append(row)
    except UnicodeDecodeError as e:
        fail(f"non-UTF8 intake text {path}: {e}")
    return rows


def pick(row, *keys):
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return None


def validate_source(row, domain, prefix, seen_ids):
    required = [
        "source_id", "domain", "title", "author", "source_type", "era", "edition",
        "local_path", "file_sha256", "pages", "size_bytes", "readability", "school_ids",
        "copyright", "local_only", "status", "duplicate_of", "sampled_locations", "notes",
    ]
    missing = [k for k in required if k not in row]
    if missing:
        fail(f"{domain} source missing fields {missing}: {row.get('source_id')}")
    sid = row["source_id"]
    if not isinstance(sid, str) or not sid.startswith(prefix):
        fail(f"{domain}: invalid source_id {sid!r}, expected prefix {prefix}")
    if sid in seen_ids:
        fail(f"duplicate canonical source_id across intake: {sid}")
    seen_ids.add(sid)
    if row["domain"] != domain:
        fail(f"{sid}: domain mismatch {row['domain']!r}")
    if row["source_type"] not in SOURCE_TYPES:
        fail(f"{sid}: invalid source_type {row['source_type']!r}")
    if row["readability"] not in READABILITY:
        fail(f"{sid}: invalid readability {row['readability']!r}")
    if row["status"] not in STATUS:
        fail(f"{sid}: invalid status {row['status']!r}")
    if row["status"] == "DUPLICATE":
        fail(f"{sid}: canonical sources.jsonl may not contain status=DUPLICATE")
    if row["local_only"] is not True:
        fail(f"{sid}: local intake source must set local_only=true")
    sha = row["file_sha256"]
    if sha is not None and not (isinstance(sha, str) and HEX64.fullmatch(sha)):
        fail(f"{sid}: file_sha256 must be null or 64 hex chars")
    size = row["size_bytes"]
    if size is not None and (not isinstance(size, int) or size < 0):
        fail(f"{sid}: size_bytes must be non-negative integer or null")
    pages = row["pages"]
    if pages is not None and (not isinstance(pages, int) or pages < 1):
        fail(f"{sid}: pages must be positive integer or null")
    if not isinstance(row["school_ids"], list):
        fail(f"{sid}: school_ids must be array")
    if not isinstance(row["sampled_locations"], list):
        fail(f"{sid}: sampled_locations must be array")
    if row["status"] == "READ" and row["source_type"] in {"BOOK", "COURSE", "ANCIENT_TEXT"} and not row["sampled_locations"]:
        fail(f"{sid}: READ long-form source requires sampled_locations evidence")
    # Intake may contain private local paths, but must not contain source-body dumps.
    notes = row.get("notes") or ""
    if isinstance(notes, str) and len(notes) > 3000:
        fail(f"{sid}: notes field is suspiciously long (>3000 chars); keep source text out of intake metadata")
    return sha


def validate_domain(root: Path, domain: str, prefix: str, seen_ids: set):
    d = root / domain
    required_files = [
        "sources.jsonl", "duplicates.jsonl", "unread_queue.jsonl", "cross_domain.jsonl",
        "K1_REPORT.md", "K1_SELF_AUDIT.md",
    ]
    for name in required_files:
        p = d / name
        if not p.is_file() or p.stat().st_size == 0:
            fail(f"{domain}: missing/non-empty required file {name}")

    sources = load_jsonl(d / "sources.jsonl")
    duplicates = load_jsonl(d / "duplicates.jsonl")
    load_jsonl(d / "unread_queue.jsonl")
    load_jsonl(d / "cross_domain.jsonl")
    if len(sources) == 0:
        fail(f"{domain}: sources.jsonl is empty")

    hashes = set()
    for row in sources:
        sha = validate_source(row, domain, prefix, seen_ids)
        if sha:
            if sha in hashes:
                fail(f"{domain}: same canonical SHA appears twice in sources.jsonl: {sha}")
            hashes.add(sha)

    canonical_ids = {r["source_id"] for r in sources}
    for i, row in enumerate(duplicates, 1):
        canonical = pick(row, "canonical_source_id", "duplicate_of", "canonical_id", "source_id")
        if not canonical:
            fail(f"{domain}: duplicates.jsonl row {i} lacks canonical source reference")
        if canonical not in canonical_ids:
            fail(f"{domain}: duplicate row {i} references unknown canonical source {canonical}")
        dsha = pick(row, "duplicate_sha256", "file_sha256", "sha256", "hash")
        if dsha is not None and not (isinstance(dsha, str) and HEX64.fullmatch(dsha)):
            fail(f"{domain}: duplicate row {i} has invalid SHA256")

    return {
        "sources": len(sources),
        "duplicates": len(duplicates),
        "canonical_hashes": hashes,
        "source_ids": canonical_ids,
    }


def validate_accounting(root: Path, domain_stats):
    accounting_path = root / "K1_ACCOUNTING.json"
    ledger_path = root / "inventory_ledger.jsonl"
    if not accounting_path.is_file() or not ledger_path.is_file():
        fail("global accounting required: add K1_ACCOUNTING.json and inventory_ledger.jsonl")
    accounting = load_json(accounting_path)
    ledger = load_jsonl(ledger_path)
    scanned = accounting.get("scanned_files_total")
    distinct = accounting.get("distinct_sha256_total")
    if not isinstance(scanned, int) or scanned < 1:
        fail("K1_ACCOUNTING.scanned_files_total must be positive integer")
    if not isinstance(distinct, int) or distinct < 1:
        fail("K1_ACCOUNTING.distinct_sha256_total must be positive integer")
    if len(ledger) != scanned:
        fail(f"accounting mismatch: ledger rows={len(ledger)} scanned_files_total={scanned}")

    allowed_disp = {"CANONICAL", "DUPLICATE", "EXCLUDED", "CROSS_DOMAIN", "OTHER"}
    ledger_hashes = set()
    ledger_source_ids = set()
    for i, row in enumerate(ledger, 1):
        sha = row.get("sha256")
        if not isinstance(sha, str) or not HEX64.fullmatch(sha):
            fail(f"inventory_ledger row {i}: invalid sha256")
        ledger_hashes.add(sha)
        disp = row.get("disposition")
        if disp not in allowed_disp:
            fail(f"inventory_ledger row {i}: invalid disposition {disp!r}")
        sid = row.get("source_id")
        if disp == "CANONICAL":
            if not sid:
                fail(f"inventory_ledger row {i}: CANONICAL requires source_id")
            ledger_source_ids.add(sid)
        if disp in {"EXCLUDED", "OTHER"} and not row.get("reason"):
            fail(f"inventory_ledger row {i}: {disp} requires reason")
    if len(ledger_hashes) != distinct:
        fail(f"accounting mismatch: ledger distinct SHA={len(ledger_hashes)} declared={distinct}")

    source_ids = set().union(*(x["source_ids"] for x in domain_stats.values()))
    missing = source_ids - ledger_source_ids
    if missing:
        fail(f"canonical source IDs missing CANONICAL ledger entries: {sorted(missing)[:10]}")

    classified = sum(x["sources"] + x["duplicates"] for x in domain_stats.values())
    return {
        "scanned_files_total": scanned,
        "distinct_sha256_total": distinct,
        "domain_sources_plus_duplicates": classified,
        "ledger_rows": len(ledger),
        "ledger_distinct_sha": len(ledger_hashes),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate local-only K1 corpus intake before sanitized import")
    parser.add_argument("intake", type=Path)
    parser.add_argument("--write-summary", type=Path)
    args = parser.parse_args()
    root = args.intake.resolve()
    if not root.is_dir():
        fail(f"intake directory not found: {root}")

    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in FORBIDDEN_EXT:
            fail(f"forbidden source/binary copied into intake delivery: {p.relative_to(root)}")

    seen_ids = set()
    stats = {}
    for domain, prefix in DOMAINS.items():
        stats[domain] = validate_domain(root, domain, prefix, seen_ids)
    accounting = validate_accounting(root, stats)

    summary = {
        "result": "PASS",
        "domains": {d: {"sources": s["sources"], "duplicates": s["duplicates"]} for d, s in stats.items()},
        "accounting": accounting,
    }
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.write_summary:
        args.write_summary.write_text(text + "\n", encoding="utf-8")
    print("k1-intake: PASS")
    print(text)


if __name__ == "__main__":
    main()
