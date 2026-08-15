#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_k1_intake.py"
DOMAINS = {
    "ziwei": "ZW-SRC-0001",
    "bazi": "BZ-SRC-0001",
    "qimen": "QM-SRC-0001",
    "liuyao": "LY-SRC-0001",
    "liuren": "LR-SRC-0001",
    "fengshui": "FS-SRC-0001",
}


def sha_for(text):
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()


def write_jsonl(path, rows):
    if rows:
        path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")
    else:
        path.write_text("\n", encoding="utf-8")


def build_valid(root: Path):
    ledger = []
    for domain, sid in DOMAINS.items():
        d = root / domain
        d.mkdir(parents=True)
        sha = sha_for(domain)
        source = {
            "source_id": sid,
            "domain": domain,
            "title": f"fixture-{domain}",
            "author": "UNKNOWN",
            "source_type": "BOOK",
            "era": "UNKNOWN",
            "edition": None,
            "local_path": f"/local/{domain}.pdf",
            "file_sha256": sha,
            "pages": 1,
            "size_bytes": 123,
            "readability": "TEXT_OK",
            "school_ids": [],
            "copyright": "RESEARCH_ONLY",
            "local_only": True,
            "status": "INDEXED",
            "duplicate_of": None,
            "sampled_locations": [],
            "notes": "metadata only",
        }
        write_jsonl(d / "sources.jsonl", [source])
        write_jsonl(d / "duplicates.jsonl", [])
        write_jsonl(d / "unread_queue.jsonl", [])
        write_jsonl(d / "cross_domain.jsonl", [])
        (d / "K1_REPORT.md").write_text("K1_INDEX_STATUS=PASS\n", encoding="utf-8")
        (d / "K1_SELF_AUDIT.md").write_text("fixture self-audit\n", encoding="utf-8")
        ledger.append({
            "path": f"/local/{domain}.pdf",
            "sha256": sha,
            "disposition": "CANONICAL",
            "domain": domain,
            "source_id": sid,
            "reason": "",
        })
    write_jsonl(root / "inventory_ledger.jsonl", ledger)
    (root / "K1_ACCOUNTING.json").write_text(json.dumps({
        "scanned_files_total": len(ledger),
        "distinct_sha256_total": len(ledger),
        "accounting_method": "fixture",
        "notes": "fixture",
    }), encoding="utf-8")


def run(root: Path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(root)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        build_valid(root)
        ok = run(root)
        if ok.returncode != 0 or "k1-intake: PASS" not in ok.stdout:
            raise SystemExit(f"positive fixture failed\nSTDOUT:\n{ok.stdout}\nSTDERR:\n{ok.stderr}")

        # Fail closed on a source/binary accidentally copied into intake delivery.
        bad = root / "ziwei" / "copied-scan.png"
        bad.write_bytes(b"not-an-image")
        blocked = run(root)
        if blocked.returncode == 0 or "forbidden source/binary" not in blocked.stderr:
            raise SystemExit("negative fixture did not block forbidden binary")
        bad.unlink()

        # Fail closed when accounting declares a file count different from the ledger.
        accounting = json.loads((root / "K1_ACCOUNTING.json").read_text(encoding="utf-8"))
        accounting["scanned_files_total"] += 1
        (root / "K1_ACCOUNTING.json").write_text(json.dumps(accounting), encoding="utf-8")
        mismatch = run(root)
        if mismatch.returncode == 0 or "ledger rows" not in mismatch.stderr:
            raise SystemExit("negative fixture did not block accounting mismatch")

    print("k1-intake-validator-tests: PASS")


if __name__ == "__main__":
    main()
