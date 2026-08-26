#!/usr/bin/env python3
"""Reviewed post-K1 source-metadata overlays for K2 execution routing.

K1 intake metadata remains immutable historical input. This module derives an
in-memory effective source view for K2 after applying explicitly REVIEWED,
field-whitelisted corrections. The correction file contains sanitized metadata
only; it must never carry local paths or source text.
"""
import json
from pathlib import Path

VERIFIED_SOURCE_METADATA_FILE = "K2_VERIFIED_SOURCE_METADATA.jsonl"
ALLOWED_VERIFIED_FIELDS = {"readability"}
ALLOWED_READABILITY = {
    "TEXT_OK",
    "SCAN",
    "OCR_WEAK",
    "OCR_FAIL",
    "METADATA_ONLY",
    "UNKNOWN",
}
ALLOWED_VERIFICATION_MODES = {
    "VISUAL_PAGE",
    "TEXT_LAYER_FULL",
    "WHOLE_TEXT_DOCUMENT",
}


def load_verified_source_metadata(repo):
    path = Path(repo) / "knowledge" / VERIFIED_SOURCE_METADATA_FILE
    if not path.exists():
        return []
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            raise ValueError(f"invalid verified source metadata JSONL {path}:{line_no}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"verified source metadata row must be object: {path}:{line_no}")
        rows.append(row)
    return rows


def apply_verified_source_metadata(sources, rows):
    """Apply reviewed corrections to an in-memory source index, fail closed.

    The canonical source registry is not rewritten. When readability changes,
    the intake value is preserved as ``readability_intake`` and the effective
    value receives an explicit K2 provenance marker.
    """
    if not isinstance(sources, dict):
        raise ValueError("sources must be a source_id -> metadata mapping")
    if rows is None:
        return sources
    if not isinstance(rows, list):
        raise ValueError("verified source metadata must be an array of rows")

    seen = set()
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"verified source metadata row {index} must be an object")
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"verified source metadata row {index} requires source_id")
        if source_id in seen:
            raise ValueError(f"duplicate verified source metadata correction: {source_id}")
        seen.add(source_id)
        if source_id not in sources:
            raise ValueError(f"verified source metadata references unknown source: {source_id}")
        if row.get("review_status") != "REVIEWED":
            raise ValueError(f"verified source metadata must be REVIEWED: {source_id}")

        verified_fields = row.get("verified_fields")
        if not isinstance(verified_fields, dict) or not verified_fields:
            raise ValueError(f"verified source metadata requires verified_fields: {source_id}")
        unknown_fields = set(verified_fields) - ALLOWED_VERIFIED_FIELDS
        if unknown_fields:
            raise ValueError(
                f"verified source metadata field not allowed for {source_id}: {sorted(unknown_fields)}"
            )

        verification_mode = row.get("verification_mode")
        if verification_mode is not None and verification_mode not in ALLOWED_VERIFICATION_MODES:
            raise ValueError(f"invalid verified source metadata verification_mode: {source_id}")

        if "readability" in verified_fields:
            new_readability = verified_fields["readability"]
            if new_readability not in ALLOWED_READABILITY:
                raise ValueError(f"invalid verified readability for {source_id}: {new_readability}")
            # Upgrading a source to TEXT_OK is stronger than downgrading it to a
            # visual/access lane, so it requires a concrete verification mode.
            if new_readability == "TEXT_OK" and verification_mode is None:
                raise ValueError(f"TEXT_OK correction requires verification_mode: {source_id}")

            source = sources[source_id]
            if "readability_intake" not in source:
                source["readability_intake"] = source.get("readability")
            source["readability"] = new_readability
            source["readability_basis"] = "K2_VERIFIED_SOURCE_METADATA"
            source["readability_review_status"] = "REVIEWED"
            if verification_mode is not None:
                source["readability_verification_mode"] = verification_mode

    return sources


def patch_validator_module(module):
    """Make a validator module's source_index return the effective K2 view."""
    if getattr(module, "_k2_verified_source_metadata_patched", False):
        return module

    raw_source_index = module.source_index

    def effective_source_index(repo):
        sources = raw_source_index(repo)
        rows = load_verified_source_metadata(repo)
        return apply_verified_source_metadata(sources, rows)

    module._k2_intake_source_index = raw_source_index
    module.source_index = effective_source_index
    module.apply_verified_source_metadata = apply_verified_source_metadata
    module.load_verified_source_metadata = load_verified_source_metadata
    module._k2_verified_source_metadata_patched = True
    return module
