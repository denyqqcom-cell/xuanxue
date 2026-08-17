#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = {
    "ziwei": "ZW-SRC-",
    "bazi": "BZ-SRC-",
    "qimen": "QM-SRC-",
    "liuyao": "LY-SRC-",
    "liuren": "LR-SRC-",
    "fengshui": "FS-SRC-",
}
PATH_LEAK = re.compile(r"(?i)(?:[A-Z]:[\\/]|/(?:home|Users|mnt)/)")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
FORBIDDEN_KEYS = {"local_path", "size_bytes", "sampled_locations", "notes"}


def fail(msg: str):
    print(f"k1-sanitized: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot parse {path}: {e}")


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
            fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description="Validate sanitized K1 registries before L1 promotion")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    k = repo / "knowledge"
    state = load_json(k / "PROJECT_STATE.json")
    expected = load_json(k / "K1_LOCAL_VALIDATION.json")
    manifest_path = k / "K1_SANITIZED_IMPORT.json"

    if not manifest_path.is_file():
        if args.force or state.get("sanitized_import") == "COMPLETE":
            fail("sanitized import manifest missing")
        print("k1-sanitized: PASS (import pending; no sanitized registry claimed complete)")
        return

    manifest = load_json(manifest_path)
    if manifest.get("schema_version") != "k1-sanitized-import-v1":
        fail("unexpected sanitized import schema_version")
    if manifest.get("privacy") != "LOCAL_PATHS_STRIPPED" or manifest.get("copyright_scope") != "METADATA_ONLY":
        fail("sanitized manifest privacy/copyright contract mismatch")

    all_ids = set()
    all_hashes = set()
    total = 0
    for domain, prefix in DOMAINS.items():
        path = k / "domains" / domain / "sources.jsonl"
        if not path.is_file():
            fail(f"missing sanitized registry: {path.relative_to(repo)}")
        text = path.read_text(encoding="utf-8")
        if PATH_LEAK.search(text):
            fail(f"{domain}: local path leaked into sanitized registry")
        rows = load_jsonl(path)
        expected_count = expected["domains"][domain]["sources"]
        if len(rows) != expected_count:
            fail(f"{domain}: source count {len(rows)} != expected local K1 count {expected_count}")
        manifest_row = manifest.get("domains", {}).get(domain, {})
        if manifest_row.get("sources") != expected_count:
            fail(f"{domain}: manifest count mismatch")
        actual_registry_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if manifest_row.get("registry_sha256") != actual_registry_sha:
            fail(f"{domain}: manifest registry_sha256 mismatch")
        for row in rows:
            sid = row.get("source_id")
            if not isinstance(sid, str) or not sid.startswith(prefix):
                fail(f"{domain}: invalid source_id {sid!r}")
            if sid in all_ids:
                fail(f"duplicate source_id across domains: {sid}")
            all_ids.add(sid)
            if row.get("domain") != domain:
                fail(f"{sid}: registry domain mismatch")
            if row.get("record_scope") != "SANITIZED_METADATA_ONLY" or row.get("packaged") is not False:
                fail(f"{sid}: sanitized/package boundary mismatch")
            if row.get("local_only") is not True:
                fail(f"{sid}: source must remain local_only=true")
            for key in FORBIDDEN_KEYS:
                if key in row:
                    fail(f"{sid}: forbidden local-only key present: {key}")
            sha = row.get("file_sha256")
            if sha is not None:
                if not isinstance(sha, str) or not HEX64.fullmatch(sha):
                    fail(f"{sid}: invalid file_sha256")
                if sha in all_hashes:
                    fail(f"canonical SHA duplicated across sanitized registries: {sha}")
                all_hashes.add(sha)
        total += len(rows)

    if total != expected["accounting"]["canonical_sources_total"]:
        fail(f"total sanitized sources {total} != accepted canonical total {expected['accounting']['canonical_sources_total']}")
    if manifest.get("total_sources") != total:
        fail("manifest total_sources mismatch")

    print("k1-sanitized: PASS")
    print(f"sources={total} domains={len(DOMAINS)}")


if __name__ == "__main__":
    main()
