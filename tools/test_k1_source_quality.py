#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_k1_source_quality.py"
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
PREFIX = {"ziwei":"ZW","bazi":"BZ","qimen":"QM","liuyao":"LY","liuren":"LR","fengshui":"FS"}


def good_row(domain, i=1):
    return {
        "source_id": f"{PREFIX[domain]}-SRC-{i:04d}",
        "domain": domain,
        "title": "示例资料 张三",
        "author": "张三",
        "author_basis": "FILENAME",
        "author_evidence": "文件名明确包含作者张三",
        "source_type": "BOOK",
        "era": "MODERN",
        "edition": "UNKNOWN",
        "file_sha256": f"{i:064x}"[-64:],
        "pages": 10,
        "pages_basis": "PDF_PAGE_COUNT",
        "readability": "TEXT_OK",
        "school_ids": ["UNKNOWN"],
        "school_basis": "UNKNOWN",
        "school_evidence": None,
        "copyright": "FORBIDDEN_TO_PACKAGE",
        "status": "INDEXED",
        "local_only": True,
        "record_scope": "SANITIZED_METADATA_ONLY",
        "packaged": False,
        "duplicate_of": None,
        "evidence_role": "TEXTUAL_SOURCE",
    }


def write_repo(root: Path, bad=False):
    k = root / "knowledge"
    (k / "domains").mkdir(parents=True)
    (k / "PROJECT_STATE.json").write_text(json.dumps({
        "source_quality": "COMPLETE",
        "k2_blocked": True,
    }), encoding="utf-8")
    for n, domain in enumerate(DOMAINS, 1):
        d = k / "domains" / domain
        d.mkdir(parents=True)
        row = good_row(domain, n)
        if bad and domain == "bazi":
            row["title"] = "八字论命苏民峰"
            row["author"] = "王亭之 / 苏民峰"
            row["author_basis"] = "FILENAME"
            row["author_evidence"] = "错误地从父目录继承王亭之"
            row["era"] = "modern"
            row["copyright"] = "modern_publication_or_scan"
            row.pop("pages_basis")
            row.pop("evidence_role")
        (d / "sources.jsonl").write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")


def run(root: Path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(root), "--force"],
        text=True,
        capture_output=True,
    )


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_repo(root, bad=False)
        ok = run(root)
        if ok.returncode != 0 or "k1-source-quality: PASS" not in ok.stdout:
            print(ok.stdout)
            print(ok.stderr, file=sys.stderr)
            raise SystemExit("positive K1 source quality fixture failed")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_repo(root, bad=True)
        bad = run(root)
        if bad.returncode == 0:
            raise SystemExit("bad attribution/schema fixture unexpectedly passed")
        combined = bad.stdout + bad.stderr
        required = ["era not canonical", "copyright not canonical", "FILENAME author tokens absent", "pages lacks trusted pages_basis", "missing/invalid evidence_role"]
        if not all(token in combined for token in required):
            print(combined)
            raise SystemExit("negative fixture did not expose all expected source-quality defects")

    print("k1-source-quality-tests: PASS")


if __name__ == "__main__":
    main()
