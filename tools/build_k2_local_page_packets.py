#!/usr/bin/env python3
"""Build local-only page packets for K2B Wave1.

This tool never writes into the repository knowledge tree. It is intentionally a
mechanical extraction helper: it finds the private K1 source path, extracts the
existing text layer page-by-page for TEXT_DIRECT sources, and records honest
blockers for sources that require page vision.

It does not create Evidence or Claims.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_PATH_RE = re.compile(r"^([A-Za-z]):[\\/](.*)$")


def fail(msg):
    print(f"k2-local-page-packets: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_jsonl(path):
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


def ensure_local_only(path: Path):
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return resolved
    fail(f"output must stay outside repository: {resolved}")


def normalize_local_path(raw):
    if not isinstance(raw, str) or not raw.strip():
        return None
    value = raw.strip()
    match = WINDOWS_PATH_RE.match(value)
    if match:
        drive = match.group(1).lower()
        rest = match.group(2).replace("\\", "/")
        return Path(f"/mnt/{drive}/{rest}")
    return Path(value).expanduser()


def private_source_index(intake_root: Path):
    out = {}
    for path in sorted(intake_root.glob("*/sources.jsonl")):
        for row in load_jsonl(path):
            sid = row.get("source_id")
            if isinstance(sid, str) and sid:
                if sid in out:
                    fail(f"duplicate private source_id: {sid}")
                out[sid] = row
    return out


def sha_text(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_pdf_text(path: Path):
    exe = shutil.which("pdftotext")
    if not exe:
        return None, "TEXT_EXTRACTION_FAILED", "pdftotext is not installed"
    proc = subprocess.run(
        [exe, "-layout", str(path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        return None, "TEXT_EXTRACTION_FAILED", err[:240] or f"pdftotext exit {proc.returncode}"
    text = proc.stdout.decode("utf-8", errors="replace")
    pages = text.split("\f")
    if pages and pages[-1] == "":
        pages.pop()
    return pages, None, None


def write_packet(path: Path, source_id: str, pages):
    with path.open("w", encoding="utf-8") as fh:
        for page_no, text in enumerate(pages, 1):
            row = {
                "source_id": source_id,
                "page": page_no,
                "text": text,
                "text_sha256": sha_text(text),
                "char_count": len(text),
            }
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--intake-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    output_dir = ensure_local_only(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = load_jsonl(args.plan)
    private = private_source_index(args.intake_root.expanduser().resolve())

    manifest = []
    for item in plan:
        sid = item.get("source_id")
        lane = item.get("execution_lane")
        if sid not in private:
            manifest.append({
                "source_id": sid,
                "execution_lane": lane,
                "packet_status": "BLOCKED",
                "blocker_code": "FILE_MISSING",
                "blocker_reason": "source_id not found in private K1 intake",
                "packet_file": None,
            })
            continue

        src = private[sid]
        local_path = normalize_local_path(src.get("local_path"))
        if local_path is None or not local_path.is_file():
            manifest.append({
                "source_id": sid,
                "execution_lane": lane,
                "packet_status": "BLOCKED",
                "blocker_code": "FILE_MISSING",
                "blocker_reason": "private source path is missing or unreadable",
                "packet_file": None,
            })
            continue

        if lane == "VISUAL_REQUIRED":
            manifest.append({
                "source_id": sid,
                "execution_lane": lane,
                "packet_status": "BLOCKED",
                "blocker_code": "VISION_UNAVAILABLE",
                "blocker_reason": "source requires original-page visual verification; text/OCR alone is insufficient",
                "packet_file": None,
            })
            continue

        if lane != "TEXT_DIRECT":
            manifest.append({
                "source_id": sid,
                "execution_lane": lane,
                "packet_status": "BLOCKED",
                "blocker_code": "ACCESS_UNAVAILABLE",
                "blocker_reason": "source is not classified for direct text-layer extraction",
                "packet_file": None,
            })
            continue

        suffix = local_path.suffix.lower()
        expected_pages = item.get("pages")
        if suffix == ".pdf":
            pages, code, reason = extract_pdf_text(local_path)
            if pages is None:
                manifest.append({
                    "source_id": sid,
                    "execution_lane": lane,
                    "packet_status": "BLOCKED",
                    "blocker_code": code,
                    "blocker_reason": reason,
                    "packet_file": None,
                })
                continue
            if isinstance(expected_pages, int) and len(pages) != expected_pages:
                manifest.append({
                    "source_id": sid,
                    "execution_lane": lane,
                    "packet_status": "BLOCKED",
                    "blocker_code": "TEXT_EXTRACTION_FAILED",
                    "blocker_reason": f"text-layer page count {len(pages)} != registered PDF pages {expected_pages}",
                    "packet_file": None,
                })
                continue
        else:
            try:
                pages = [local_path.read_text(encoding="utf-8")]
            except UnicodeDecodeError:
                manifest.append({
                    "source_id": sid,
                    "execution_lane": lane,
                    "packet_status": "BLOCKED",
                    "blocker_code": "TEXT_EXTRACTION_FAILED",
                    "blocker_reason": "non-PDF TEXT_OK source is not UTF-8 readable",
                    "packet_file": None,
                })
                continue

        packet_file = output_dir / f"{sid}.pages.jsonl"
        write_packet(packet_file, sid, pages)
        manifest.append({
            "source_id": sid,
            "execution_lane": lane,
            "packet_status": "READY",
            "blocker_code": None,
            "blocker_reason": None,
            "packet_file": packet_file.name,
            "page_count": len(pages),
            "total_chars": sum(len(text) for text in pages),
        })

    manifest_path = output_dir / "manifest.jsonl"
    manifest_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in manifest),
        encoding="utf-8",
    )
    ready = sum(1 for row in manifest if row["packet_status"] == "READY")
    blocked = len(manifest) - ready
    print("k2-local-page-packets: PASS")
    print(f"plan_units={len(plan)} ready={ready} blocked={blocked} output={output_dir}")
    print(f"manifest={manifest_path}")


if __name__ == "__main__":
    main()
