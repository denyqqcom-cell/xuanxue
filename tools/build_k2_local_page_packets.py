#!/usr/bin/env python3
"""Build local-only page packets for K2B Wave1.

This tool never writes into the repository knowledge tree. It is intentionally a
mechanical extraction helper: it finds the private K1 source path, verifies that
its bytes still match the canonical K1 SHA256, extracts the existing text layer
page-by-page for TEXT_DIRECT sources, and records honest blockers for sources
that require page vision.

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


def sha_file(path: Path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


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


def write_packet(path: Path, source_id: str, source_file_sha256: str, pages):
    with path.open("w", encoding="utf-8") as fh:
        for page_no, text in enumerate(pages, 1):
            row = {
                "source_id": source_id,
                "source_file_sha256": source_file_sha256,
                "page": page_no,
                "text": text,
                "text_sha256": sha_text(text),
                "char_count": len(text),
            }
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def validate_plan(plan):
    seen = set()
    for n, item in enumerate(plan, 1):
        sid = item.get("source_id")
        if not isinstance(sid, str) or not sid:
            fail(f"plan row {n}: missing source_id")
        if sid in seen:
            fail(f"plan contains duplicate source_id: {sid}")
        seen.add(sid)
        expected_hash = item.get("file_sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            fail(f"{sid}: plan missing canonical file_sha256")


def verify_source_identity(sid, item, private_row, local_path):
    plan_hash = item.get("file_sha256")
    private_hash = private_row.get("file_sha256")
    if not isinstance(private_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", private_hash):
        fail(f"{sid}: private K1 registry missing valid file_sha256")
    if private_hash != plan_hash:
        fail(f"{sid}: private K1 hash differs from official Wave1 plan")
    actual_hash = sha_file(local_path)
    if actual_hash != plan_hash:
        fail(f"{sid}: local file SHA256 mismatch; expected {plan_hash}, got {actual_hash}")
    return actual_hash


def blocked_row(sid, lane, source_file_sha256, code, reason):
    return {
        "source_id": sid,
        "source_file_sha256": source_file_sha256,
        "execution_lane": lane,
        "packet_status": "BLOCKED",
        "blocker_code": code,
        "blocker_reason": reason,
        "packet_file": None,
        "packet_sha256": None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--intake-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    output_dir = ensure_local_only(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = load_jsonl(args.plan)
    validate_plan(plan)
    private = private_source_index(args.intake_root.expanduser().resolve())

    manifest = []
    for item in plan:
        sid = item["source_id"]
        lane = item.get("execution_lane")
        if sid not in private:
            manifest.append(blocked_row(
                sid, lane, item.get("file_sha256"), "FILE_MISSING",
                "source_id not found in private K1 intake",
            ))
            continue

        src = private[sid]
        local_path = normalize_local_path(src.get("local_path"))
        if local_path is None or not local_path.is_file():
            manifest.append(blocked_row(
                sid, lane, item.get("file_sha256"), "FILE_MISSING",
                "private source path is missing or unreadable",
            ))
            continue

        actual_hash = verify_source_identity(sid, item, src, local_path)

        if lane == "VISUAL_REQUIRED":
            manifest.append(blocked_row(
                sid, lane, actual_hash, "VISION_UNAVAILABLE",
                "source requires original-page visual verification; text/OCR alone is insufficient",
            ))
            continue

        if lane != "TEXT_DIRECT":
            manifest.append(blocked_row(
                sid, lane, actual_hash, "ACCESS_UNAVAILABLE",
                "source is not classified for direct text-layer extraction",
            ))
            continue

        suffix = local_path.suffix.lower()
        expected_pages = item.get("pages")
        if suffix == ".pdf":
            pages, code, reason = extract_pdf_text(local_path)
            if pages is None:
                manifest.append(blocked_row(sid, lane, actual_hash, code, reason))
                continue
            if isinstance(expected_pages, int) and len(pages) != expected_pages:
                manifest.append(blocked_row(
                    sid, lane, actual_hash, "TEXT_EXTRACTION_FAILED",
                    f"text-layer page count {len(pages)} != registered PDF pages {expected_pages}",
                ))
                continue
        else:
            try:
                pages = [local_path.read_text(encoding="utf-8")]
            except UnicodeDecodeError:
                manifest.append(blocked_row(
                    sid, lane, actual_hash, "TEXT_EXTRACTION_FAILED",
                    "non-PDF TEXT_OK source is not UTF-8 readable",
                ))
                continue

        packet_file = output_dir / f"{sid}.pages.jsonl"
        write_packet(packet_file, sid, actual_hash, pages)
        packet_hash = sha_file(packet_file)
        manifest.append({
            "source_id": sid,
            "source_file_sha256": actual_hash,
            "execution_lane": lane,
            "packet_status": "READY",
            "blocker_code": None,
            "blocker_reason": None,
            "packet_file": packet_file.name,
            "packet_sha256": packet_hash,
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
