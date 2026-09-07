#!/usr/bin/env python3
"""Prepare repo-external visual page artifacts for K2 VISUAL_REQUIRED PDFs.

This helper closes one execution-surface gap only:

canonical local bytes -> fresh SHA256 -> physical PDF page count -> PDF render

It does not perform OCR, does not inspect page semantics, does not create a
Reading Ledger row, and does not create Evidence, Distillates, Claims, Batch,
Freeze, Outcome, or empirical credit. A successful render means only that the
original PDF pages are available as local images for a separate visual-capable
reviewer.

All output is forced outside the repository. The manifest intentionally omits
raw local source paths and source text. Restricted source policy remains in
force across rendering; this helper never changes `packaged`, `local_only`, or
`record_scope` state.
"""

import argparse
import importlib
import json
import sys
from pathlib import Path

import build_k2_local_page_packets as base

MIN_DPI = 72
MAX_DPI = 400
VISUAL_READABILITY = {"SCAN", "OCR_WEAK", "OCR_FAIL"}
REQUIRED_POLICY_FIELDS = {
    "readability",
    "source_type",
    "copyright",
    "local_only",
    "packaged",
    "record_scope",
}


def fail(msg):
    print(f"k2-local-visual-pages: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def validate_dpi(value):
    if not isinstance(value, int) or isinstance(value, bool):
        fail("dpi must be an integer")
    if value < MIN_DPI or value > MAX_DPI:
        fail(f"dpi must be between {MIN_DPI} and {MAX_DPI}")
    return value


def validate_visual_plan(plan):
    """Require the C2-entry source/policy snapshot before visual preparation."""
    base.validate_plan(plan)
    for item in plan:
        sid = item["source_id"]
        if item.get("execution_lane") != "VISUAL_REQUIRED":
            fail(f"{sid}: visual renderer only accepts VISUAL_REQUIRED sources")
        if item.get("readability") not in VISUAL_READABILITY:
            fail(f"{sid}: VISUAL_REQUIRED plan must carry SCAN/OCR_WEAK/OCR_FAIL readability")
        pages = item.get("pages")
        if not isinstance(pages, int) or isinstance(pages, bool) or pages <= 0:
            fail(f"{sid}: visual plan requires positive integer pages")
        missing = sorted(field for field in REQUIRED_POLICY_FIELDS if field not in item)
        if missing:
            fail(f"{sid}: visual plan missing source policy fields: {missing}")
        if "author_basis" not in item and "attribution_basis" not in item:
            fail(f"{sid}: visual plan requires author_basis or attribution_basis")
        if not isinstance(item.get("local_only"), bool):
            fail(f"{sid}: local_only must be boolean")
        if not isinstance(item.get("packaged"), bool):
            fail(f"{sid}: packaged must be boolean")
        for field in ("source_type", "copyright", "record_scope"):
            if not isinstance(item.get(field), str) or not item.get(field):
                fail(f"{sid}: {field} must be non-empty string")


def policy_snapshot(item):
    out = {
        "readability": item.get("readability"),
        "source_type": item.get("source_type"),
        "copyright": item.get("copyright"),
        "local_only": item.get("local_only"),
        "packaged": item.get("packaged"),
        "record_scope": item.get("record_scope"),
    }
    if "author_basis" in item:
        out["author_basis"] = item.get("author_basis")
    else:
        out["attribution_basis"] = item.get("attribution_basis")
    return out


def classify_rendered_page_count(actual_pages, expected_pages):
    if actual_pages == expected_pages:
        return None, None
    return (
        "PDF_RENDER_PAGE_COUNT_MISMATCH",
        f"rendered PDF page count {actual_pages} != verified physical PDF pages {expected_pages}",
    )


def _prepare_output_dir(path: Path):
    resolved = base.ensure_local_only(path)
    if resolved.exists():
        try:
            if any(resolved.iterdir()):
                fail(f"visual output directory must be empty: {resolved}")
        except OSError as exc:
            fail(f"cannot inspect visual output directory {resolved}: {exc}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _safe_close(obj):
    if obj is None:
        return
    close = getattr(obj, "close", None)
    if callable(close):
        try:
            close()
        except Exception:
            pass


def _sanitize_reason(reason, local_path=None):
    text = str(reason or "")
    if local_path is not None:
        candidates = {str(local_path)}
        try:
            candidates.add(str(local_path.resolve()))
        except OSError:
            pass
        for candidate in sorted(candidates, key=len, reverse=True):
            if candidate:
                text = text.replace(candidate, "<LOCAL_CARRIER>")
    return text[:800]


def render_pdf_pdfium(path: Path, output_dir: Path, source_id: str, source_hash: str, dpi: int):
    """Render original PDF pages without OCR using pypdfium2 + Pillow."""
    try:
        pdfium = importlib.import_module("pypdfium2")
        importlib.import_module("PIL.Image")
    except Exception as exc:
        return (
            None,
            None,
            "PDF_RENDER_SURFACE_UNAVAILABLE",
            _sanitize_reason(
                f"pypdfium2/Pillow unavailable: {type(exc).__name__}: {exc}", path
            ),
        )

    out = _prepare_output_dir(output_dir)
    document = None
    rows = []
    try:
        document = pdfium.PdfDocument(str(path))
        page_count = len(document)
        if not isinstance(page_count, int) or page_count < 0:
            raise ValueError(f"invalid PDFium page count: {page_count!r}")
        scale = dpi / 72.0
        for page_index in range(page_count):
            page = None
            bitmap = None
            pil_image = None
            try:
                page = document[page_index]
                bitmap = page.render(scale=scale)
                pil_image = bitmap.to_pil()
                image = out / f"page-{page_index + 1:04d}.png"
                pil_image.save(str(image), format="PNG")
                width, height = pil_image.size
                rows.append({
                    "source_id": source_id,
                    "source_file_sha256": source_hash,
                    "page": page_index + 1,
                    "image_file": image.name,
                    "image_sha256": base.sha_file(image),
                    "width_px": int(width),
                    "height_px": int(height),
                    "dpi": dpi,
                    "renderer": "PYPDFIUM2",
                })
            finally:
                _safe_close(pil_image)
                _safe_close(bitmap)
                _safe_close(page)
    except Exception as exc:
        return (
            rows or None,
            "PYPDFIUM2",
            "PDF_RENDER_FAILED",
            _sanitize_reason(
                f"PDFium render failed: {type(exc).__name__}: {exc}", path
            ),
        )
    finally:
        _safe_close(document)

    return rows, "PYPDFIUM2", None, None


def blocked_row(
    item,
    source_file_sha256,
    code,
    reason,
    *,
    identity_mode=None,
    material_page_count=None,
    material_page_counter=None,
    renderer=None,
    rendered_page_count=None,
):
    return {
        "source_id": item["source_id"],
        "source_file_sha256": source_file_sha256,
        "identity_mode": identity_mode,
        "execution_lane": item.get("execution_lane"),
        "execution_status": "EXECUTION_BLOCKED",
        "blocker_code": code,
        "blocker_reason": reason,
        "material_page_count": material_page_count,
        "material_page_counter": material_page_counter,
        "renderer": renderer,
        "rendered_page_count": rendered_page_count,
        "visual_manifest_file": None,
        "visual_manifest_sha256": None,
        "policy_snapshot": policy_snapshot(item),
        "reading_credit": "NONE",
    }


def write_visual_manifest(path: Path, rows):
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return base.sha_file(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--intake-root", type=Path)
    ap.add_argument(
        "--search-root", type=Path, action="append", default=[],
        help="repeatable local corpus root used for canonical SHA256 discovery",
    )
    ap.add_argument(
        "--python-deps-dir", type=Path,
        help="optional repo-external dependency dir containing pypdfium2/Pillow",
    )
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--dpi", type=int, default=160)
    args = ap.parse_args()

    dpi = validate_dpi(args.dpi)
    output_dir = base.ensure_local_only(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base.configure_python_deps(args.python_deps_dir)

    plan = base.load_jsonl(args.plan)
    validate_visual_plan(plan)
    private = base.private_source_index(args.intake_root)

    target_hashes = {item["file_sha256"] for item in plan}
    search_roots = [base.normalize_local_path(str(p)) for p in args.search_root]
    search_roots = [p for p in search_roots if p is not None]
    hash_matches = (
        base.discover_hash_matches(search_roots, target_hashes, output_dir)
        if search_roots
        else {h: [] for h in target_hashes}
    )

    manifest = []
    for item in plan:
        sid = item["source_id"]
        local_path, actual_hash, identity_mode = base.resolve_source(
            sid, item, private, hash_matches
        )
        if local_path is None:
            manifest.append(blocked_row(
                item,
                item["file_sha256"],
                "FILE_MISSING",
                "canonical bytes not resolved from private K1 registry or explicit search roots",
            ))
            continue

        if local_path.suffix.lower() != ".pdf":
            manifest.append(blocked_row(
                item,
                actual_hash,
                "VISUAL_CARRIER_NOT_PDF",
                "local visual-page renderer currently supports PDF carriers only",
                identity_mode=identity_mode,
            ))
            continue

        material_page_count, material_page_counter, code, reason = (
            base.inspect_pdf_material_page_count(local_path)
        )
        if material_page_count is None:
            manifest.append(blocked_row(
                item,
                actual_hash,
                code,
                _sanitize_reason(reason, local_path),
                identity_mode=identity_mode,
                material_page_count=material_page_count,
                material_page_counter=material_page_counter,
            ))
            continue

        code, reason = base.classify_pdf_material_page_count(
            material_page_count, item.get("pages")
        )
        if code is not None:
            manifest.append(blocked_row(
                item,
                actual_hash,
                code,
                _sanitize_reason(reason, local_path),
                identity_mode=identity_mode,
                material_page_count=material_page_count,
                material_page_counter=material_page_counter,
            ))
            continue

        source_out = output_dir / sid
        rows, renderer, code, reason = render_pdf_pdfium(
            local_path, source_out, sid, actual_hash, dpi
        )
        if code is not None:
            manifest.append(blocked_row(
                item,
                actual_hash,
                code,
                reason,
                identity_mode=identity_mode,
                material_page_count=material_page_count,
                material_page_counter=material_page_counter,
                renderer=renderer,
                rendered_page_count=len(rows) if rows is not None else None,
            ))
            continue

        code, reason = classify_rendered_page_count(len(rows), material_page_count)
        if code is not None:
            manifest.append(blocked_row(
                item,
                actual_hash,
                code,
                reason,
                identity_mode=identity_mode,
                material_page_count=material_page_count,
                material_page_counter=material_page_counter,
                renderer=renderer,
                rendered_page_count=len(rows),
            ))
            continue

        visual_manifest = source_out / "visual-pages.jsonl"
        visual_hash = write_visual_manifest(visual_manifest, rows)
        manifest.append({
            "source_id": sid,
            "source_file_sha256": actual_hash,
            "identity_mode": identity_mode,
            "execution_lane": item.get("execution_lane"),
            "execution_status": "VISUAL_PAGES_READY",
            "blocker_code": None,
            "blocker_reason": None,
            "material_page_count": material_page_count,
            "material_page_counter": material_page_counter,
            "renderer": renderer,
            "dpi": dpi,
            "rendered_page_count": len(rows),
            "visual_manifest_file": f"{sid}/visual-pages.jsonl",
            "visual_manifest_sha256": visual_hash,
            "policy_snapshot": policy_snapshot(item),
            "reading_credit": "NONE",
        })

    manifest_path = output_dir / "manifest.jsonl"
    manifest_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in manifest),
        encoding="utf-8",
    )
    ready = sum(1 for row in manifest if row["execution_status"] == "VISUAL_PAGES_READY")
    blocked = len(manifest) - ready

    print("k2-local-visual-pages: PASS")
    print(
        f"plan_units={len(plan)} visual_pages_ready={ready} blocked={blocked} "
        f"output={output_dir}"
    )
    print("reading_credit=NONE")
    print(f"manifest={manifest_path}")


if __name__ == "__main__":
    main()
