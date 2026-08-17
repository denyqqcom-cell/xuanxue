#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
PATH_LEAK = re.compile(r"(?i)(?:[A-Z]:[\\/]|/(?:home|Users|mnt)/)")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
SAFE_FIELDS = [
    "source_id", "domain", "title", "author", "author_basis", "author_evidence",
    "source_type", "era", "edition", "file_sha256", "pages", "pages_basis",
    "readability", "school_ids", "school_basis", "school_evidence", "evidence_role",
    "copyright", "status",
]
FORBIDDEN_KEYS = {"local_path", "size_bytes", "sampled_locations", "notes"}


def fail(msg: str):
    print(f"k1-sanitize: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_jsonl(path: Path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as e:
            fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row, dict):
            fail(f"row is not object: {path}:{n}")
        rows.append(row)
    return rows


def reject_path_leak(value, field: str, sid: str):
    if isinstance(value, str) and PATH_LEAK.search(value):
        fail(f"{sid}: local path leaked through {field}")
    if isinstance(value, list):
        for item in value:
            reject_path_leak(item, field, sid)


def sanitize_row(row: dict, domain: str) -> dict:
    sid = row.get("source_id", "<unknown>")
    if row.get("domain") != domain:
        fail(f"{sid}: domain mismatch")
    out = {k: row.get(k) for k in SAFE_FIELDS}
    out["local_only"] = True
    out["record_scope"] = "SANITIZED_METADATA_ONLY"
    out["packaged"] = False
    out["duplicate_of"] = None
    sha = out.get("file_sha256")
    if sha is not None and not (isinstance(sha, str) and HEX64.fullmatch(sha)):
        fail(f"{sid}: invalid file_sha256")
    if not isinstance(out.get("school_ids"), list):
        fail(f"{sid}: school_ids must be array")
    for key, value in out.items():
        reject_path_leak(value, key, sid)
        if isinstance(value, str) and len(value) > 800:
            fail(f"{sid}: suspiciously long metadata field {key}")
    serialized = json.dumps(out, ensure_ascii=False)
    for key in FORBIDDEN_KEYS:
        if f'"{key}"' in serialized:
            fail(f"{sid}: forbidden local-only key survived sanitization: {key}")
    return out


def main():
    parser = argparse.ArgumentParser(description="Create public-safe K1 metadata registries from local intake")
    parser.add_argument("intake", type=Path)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    intake = args.intake.resolve()
    repo = args.repo_root.resolve()
    validator = repo / "tools" / "validate_k1_intake.py"
    if not validator.is_file():
        fail(f"missing intake validator: {validator}")
    subprocess.run([sys.executable, str(validator), str(intake)], check=True)

    manifest = {
        "schema_version": "k1-sanitized-import-v1",
        "source": "LOCAL_K1_MACHINE_VALIDATED",
        "domains": {},
        "total_sources": 0,
        "privacy": "LOCAL_PATHS_STRIPPED",
        "copyright_scope": "METADATA_ONLY",
    }

    global_hashes = set()
    for domain in DOMAINS:
        rows = load_jsonl(intake / domain / "sources.jsonl")
        sanitized = [sanitize_row(row, domain) for row in rows]
        sanitized.sort(key=lambda x: x["source_id"])

        seen_ids = set()
        for row in sanitized:
            sid = row["source_id"]
            if sid in seen_ids:
                fail(f"{domain}: duplicate source_id {sid}")
            seen_ids.add(sid)
            sha = row.get("file_sha256")
            if sha:
                if sha in global_hashes:
                    fail(f"canonical SHA appears in more than one sanitized source: {sha}")
                global_hashes.add(sha)

        target = repo / "knowledge" / "domains" / domain / "sources.jsonl"
        target.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in sanitized) + "\n"
        if PATH_LEAK.search(text):
            fail(f"{domain}: path leak detected in serialized registry")
        target.write_text(text, encoding="utf-8")
        manifest["domains"][domain] = {
            "sources": len(sanitized),
            "registry_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
        manifest["total_sources"] += len(sanitized)

    manifest_path = args.manifest or (repo / "knowledge" / "K1_SANITIZED_IMPORT.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("k1-sanitize: PASS")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
