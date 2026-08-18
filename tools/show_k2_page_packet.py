#!/usr/bin/env python3
"""Print a verified slice of a local-only K2B page packet.

The helper is intentionally read-only and non-semantic. It lets a local
execution assistant expose a bounded page range to the project-side main agent
without summarizing or modifying the source text.
"""

import argparse
import json
import sys
from pathlib import Path

import build_k2_local_page_packets as packets

MAX_PAGES_PER_CALL = 25


def fail(msg):
    print(f"k2-page-packet-show: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest(packet_dir: Path):
    path = packet_dir / "manifest.jsonl"
    if not path.is_file():
        fail(f"manifest missing: {path}")
    rows = packets.load_jsonl(path)
    out = {}
    for row in rows:
        sid = row.get("source_id")
        if not isinstance(sid, str) or not sid:
            fail("manifest row missing source_id")
        if sid in out:
            fail(f"duplicate manifest source_id: {sid}")
        out[sid] = row
    return out


def load_packet(path: Path, source_id: str):
    rows = packets.load_jsonl(path)
    seen = set()
    for row in rows:
        if row.get("source_id") != source_id:
            fail(f"packet source_id mismatch in {path.name}")
        page = row.get("page")
        if not isinstance(page, int) or page < 1:
            fail(f"invalid page number in {path.name}")
        if page in seen:
            fail(f"duplicate page {page} in {path.name}")
        seen.add(page)
        text = row.get("text")
        if not isinstance(text, str):
            fail(f"page {page}: text must be string")
        if row.get("text_sha256") != packets.sha_text(text):
            fail(f"page {page}: text_sha256 mismatch")
        if row.get("char_count") != len(text):
            fail(f"page {page}: char_count mismatch")
    return rows


def select_pages(rows, start, end):
    by_page = {row["page"]: row for row in rows}
    missing = [p for p in range(start, end + 1) if p not in by_page]
    if missing:
        fail(f"requested page(s) missing: {missing[:10]}")
    return [by_page[p] for p in range(start, end + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet-dir", type=Path, required=True)
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    args = ap.parse_args()

    if args.start < 1 or args.end < args.start:
        fail("invalid page range")
    if args.end - args.start + 1 > MAX_PAGES_PER_CALL:
        fail(f"maximum {MAX_PAGES_PER_CALL} pages per call")

    packet_dir = args.packet_dir.expanduser().resolve()
    manifest = load_manifest(packet_dir)
    meta = manifest.get(args.source_id)
    if not meta:
        fail(f"source not present in manifest: {args.source_id}")
    if meta.get("packet_status") != "READY":
        fail(f"source is not READY: {meta.get('blocker_code')}")
    packet_name = meta.get("packet_file")
    if not isinstance(packet_name, str) or not packet_name:
        fail("READY source missing packet_file")
    packet_path = packet_dir / packet_name
    if not packet_path.is_file():
        fail(f"packet file missing: {packet_path}")
    actual_hash = packets.sha_file(packet_path)
    if actual_hash != meta.get("packet_sha256"):
        fail("packet_sha256 mismatch")

    rows = load_packet(packet_path, args.source_id)
    selected = select_pages(rows, args.start, args.end)
    print(json.dumps({
        "source_id": args.source_id,
        "source_file_sha256": meta.get("source_file_sha256"),
        "packet_sha256": actual_hash,
        "page_count": meta.get("page_count"),
        "range": {"start": args.start, "end": args.end},
    }, ensure_ascii=False, sort_keys=True))
    for row in selected:
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
