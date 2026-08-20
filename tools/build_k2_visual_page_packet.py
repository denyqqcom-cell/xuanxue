#!/usr/bin/env python3
"""Render canonical VISUAL_REQUIRED K2 sources into local-only page images.

This helper is deliberately mechanical. It does NOT perform OCR, semantic
reading, Evidence extraction, interpretation, or Reading-Credit assignment.
Its sole purpose is to make the exact canonical PDF pages visible to the main
reviewer while keeping copyrighted research binaries and rendered pages outside
the repository.

Resolution follows the existing K2 local packet helper:
1. optional private K1 intake registry;
2. canonical SHA256 discovery under explicit --search-root paths.

A successful packet means READY_FOR_VISUAL_REVIEW, never COMPLETE/READ.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import build_k2_local_page_packets as packets

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def fail(msg):
    print(f"k2-visual-page-packet: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def require_source(plan, source_id):
    matches = [row for row in plan if row.get("source_id") == source_id]
    if not matches:
        fail(f"source_id not found in plan: {source_id}")
    if len(matches) != 1:
        fail(f"plan contains duplicate source_id: {source_id}")
    row = matches[0]
    if row.get("execution_lane") != "VISUAL_REQUIRED":
        fail(
            f"{source_id}: visual renderer only accepts VISUAL_REQUIRED; "
            f"got {row.get('execution_lane')!r}"
        )
    pages = row.get("pages")
    if not isinstance(pages, int) or pages <= 0:
        fail(f"{source_id}: plan must provide a positive integer page count")
    expected_hash = row.get("file_sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        fail(f"{source_id}: plan missing canonical file_sha256")
    return row


def load_renderer():
    try:
        import pypdfium2 as pdfium
    except Exception as exc:
        fail(f"pypdfium2 unavailable: {type(exc).__name__}: {exc}")
    try:
        from PIL import Image  # noqa: F401
    except Exception as exc:
        fail(f"Pillow unavailable: {type(exc).__name__}: {exc}")
    return pdfium


def render_pdf(pdfium, source_path, source_id, output_dir, expected_pages, dpi):
    try:
        document = pdfium.PdfDocument(str(source_path))
    except Exception as exc:
        fail(f"{source_id}: cannot open PDF: {type(exc).__name__}: {exc}")

    try:
        actual_pages = len(document)
        if actual_pages != expected_pages:
            fail(
                f"{source_id}: PDF page count {actual_pages} != registered pages {expected_pages}"
            )

        scale = dpi / 72.0
        page_rows = []
        for index in range(actual_pages):
            page_no = index + 1
            page = None
            bitmap = None
            image = None
            try:
                page = document[index]
                bitmap = page.render(scale=scale)
                image = bitmap.to_pil()
                filename = f"{source_id}.p{page_no:04d}.png"
                image_path = output_dir / filename
                image.save(image_path, format="PNG")
                page_rows.append({
                    "page": page_no,
                    "image_file": filename,
                    "image_sha256": packets.sha_file(image_path),
                    "width_px": int(image.width),
                    "height_px": int(image.height),
                })
            except Exception as exc:
                fail(
                    f"{source_id}: render failed at page {page_no}: "
                    f"{type(exc).__name__}: {exc}"
                )
            finally:
                if image is not None:
                    try:
                        image.close()
                    except Exception:
                        pass
                if bitmap is not None:
                    try:
                        bitmap.close()
                    except Exception:
                        pass
                if page is not None:
                    try:
                        page.close()
                    except Exception:
                        pass
        return page_rows
    finally:
        try:
            document.close()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--intake-root", type=Path)
    ap.add_argument(
        "--search-root",
        type=Path,
        action="append",
        default=[],
        help="repeatable local corpus root used for canonical SHA256 discovery",
    )
    ap.add_argument(
        "--python-deps-dir",
        type=Path,
        help="optional external local-only dependency target",
    )
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--dpi", type=int, default=144)
    args = ap.parse_args()

    if not SOURCE_ID_RE.fullmatch(args.source_id):
        fail("source_id contains characters unsafe for local packet filenames")
    if args.dpi < 72 or args.dpi > 300:
        fail("dpi must be between 72 and 300")

    output_dir = packets.ensure_local_only(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    packets.configure_python_deps(args.python_deps_dir)

    plan = packets.load_jsonl(args.plan)
    packets.validate_plan(plan)
    item = require_source(plan, args.source_id)

    private = packets.private_source_index(args.intake_root)
    search_roots = [packets.normalize_local_path(str(p)) for p in args.search_root]
    search_roots = [p for p in search_roots if p is not None]
    expected_hash = item["file_sha256"]
    hash_matches = (
        packets.discover_hash_matches(search_roots, {expected_hash}, output_dir)
        if search_roots
        else {expected_hash: []}
    )
    source_path, actual_hash, identity_mode = packets.resolve_source(
        args.source_id, item, private, hash_matches
    )
    if source_path is None:
        fail(
            f"{args.source_id}: canonical bytes not resolved from private K1 registry "
            "or explicit search roots"
        )
    if source_path.suffix.lower() != ".pdf":
        fail(f"{args.source_id}: VISUAL_REQUIRED renderer currently requires a PDF")
    if actual_hash != expected_hash:
        fail(f"{args.source_id}: resolved SHA256 differs from Wave1 plan")

    pdfium = load_renderer()
    page_rows = render_pdf(
        pdfium,
        source_path,
        args.source_id,
        output_dir,
        item["pages"],
        args.dpi,
    )

    manifest = {
        "schema_version": "k2-visual-page-packet-v1",
        "source_id": args.source_id,
        "source_file_sha256": actual_hash,
        "identity_mode": identity_mode,
        "execution_lane": "VISUAL_REQUIRED",
        "packet_status": "READY_FOR_VISUAL_REVIEW",
        "renderer": "PYPDFIUM2_ORIGINAL_PAGE_RENDER",
        "dpi": args.dpi,
        "registered_page_count": item["pages"],
        "rendered_page_count": len(page_rows),
        "review_credit_granted": False,
        "ocr_performed": False,
        "semantic_extraction_performed": False,
        "local_source_path_recorded": False,
        "pages": page_rows,
    }
    manifest_path = output_dir / f"{args.source_id}.visual_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print("k2-visual-page-packet: PASS")
    print(f"source_id={args.source_id}")
    print(f"source_file_sha256={actual_hash}")
    print(f"rendered_pages={len(page_rows)} dpi={args.dpi}")
    print(f"packet_status=READY_FOR_VISUAL_REVIEW review_credit_granted=false")
    print(f"manifest={manifest_path.name}")


if __name__ == "__main__":
    main()
