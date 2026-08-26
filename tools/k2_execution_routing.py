#!/usr/bin/env python3
"""Fail-closed post-K1 execution-routing corrections for K2.

K1 source metadata is historical intake and is never rewritten here. Reviewed
source-quality corrections are applied only to an in-memory effective source
view used by K2 routing. The persistent correction registry is intentionally
separate from K2_VERIFIED_SOURCE_METADATA.jsonl, whose existing contract is for
bibliographic metadata discovered during COMPLETE reading.
"""
import json
from pathlib import Path

CORRECTIONS_FILE = "K2_EXECUTION_ROUTING_CORRECTIONS.jsonl"
ROUTING_FIELDS = {"readability"}
DOWNGRADE_READABILITY = {"SCAN", "OCR_WEAK", "OCR_FAIL", "METADATA_ONLY", "UNKNOWN"}
PERSISTED_TOP_FIELDS = {
    "source_id",
    "canonical_sha256",
    "review_status",
    "verification_basis",
    "verified_fields",
    "reason_code",
}
VERIFICATION_BASES = {"POST_K1_SOURCE_QUALITY_REVIEW", "VISUAL_PAGE"}
REASON_CODES = {
    "TEXT_LAYER_NOT_SOURCE_BODY",
    "SEMANTIC_TEXT_LAYER_UNREADABLE",
    "VERIFIED_SCAN",
}


def _load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            raise ValueError(f"invalid routing-correction JSONL {path}:{line_no}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"routing-correction row must be object: {path}:{line_no}")
        rows.append(row)
    return rows


def validate_persisted_rows(sources, rows):
    issues = []
    seen = set()
    for row in rows:
        sid = row.get("source_id") or "<missing>"
        if sid in seen:
            issues.append((sid, "duplicate routing correction source_id"))
        seen.add(sid)
        extra = set(row) - PERSISTED_TOP_FIELDS
        if extra:
            issues.append((sid, f"unexpected routing-correction fields: {sorted(extra)}"))
        src = sources.get(sid)
        if not src:
            issues.append((sid, "unknown source_id"))
            continue
        if row.get("canonical_sha256") != src.get("file_sha256"):
            issues.append((sid, "canonical_sha256 mismatch"))
        if row.get("review_status") != "REVIEWED":
            issues.append((sid, "review_status must be REVIEWED"))
        if row.get("verification_basis") not in VERIFICATION_BASES:
            issues.append((sid, "unsupported verification_basis"))
        if row.get("reason_code") not in REASON_CODES:
            issues.append((sid, "unsupported reason_code"))
        fields = row.get("verified_fields")
        if not isinstance(fields, dict) or not fields:
            issues.append((sid, "verified_fields must be non-empty object"))
            continue
        unknown = set(fields) - ROUTING_FIELDS
        if unknown:
            issues.append((sid, f"unexpected routing verified_fields: {sorted(unknown)}"))
        readability = fields.get("readability")
        if readability not in DOWNGRADE_READABILITY:
            issues.append((sid, "routing correction may only fail-closed downgrade readability"))
        if readability == src.get("readability"):
            issues.append((sid, "routing correction must change intake readability"))
    return issues


def load_execution_routing_corrections(repo, sources=None):
    path = Path(repo) / "knowledge" / CORRECTIONS_FILE
    rows = _load_jsonl(path)
    if sources is not None:
        issues = validate_persisted_rows(sources, rows)
        if issues:
            sid, message = issues[0]
            raise ValueError(f"invalid K2 execution-routing corrections: issues={len(issues)} first={sid}: {message}")
    return rows


def apply_verified_source_metadata(sources, rows):
    """Apply reviewed routing fields to an in-memory source index.

    This small function is also the public contract exercised by
    test_k2_evidence.py. Persistent-registry shape/hash checks are performed by
    validate_persisted_rows before this function is called in production.
    """
    if not isinstance(sources, dict):
        raise ValueError("sources must be a source_id -> metadata mapping")
    if rows is None:
        return sources
    if not isinstance(rows, list):
        raise ValueError("verified source metadata corrections must be an array")

    seen = set()
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"verified source metadata correction {index} must be object")
        sid = row.get("source_id")
        if not isinstance(sid, str) or not sid:
            raise ValueError(f"verified source metadata correction {index} requires source_id")
        if sid in seen:
            raise ValueError(f"duplicate verified source metadata correction: {sid}")
        seen.add(sid)
        if sid not in sources:
            raise ValueError(f"verified source metadata references unknown source: {sid}")
        if row.get("review_status") != "REVIEWED":
            raise ValueError(f"verified source metadata correction must be REVIEWED: {sid}")
        fields = row.get("verified_fields")
        if not isinstance(fields, dict) or not fields:
            raise ValueError(f"verified source metadata correction requires verified_fields: {sid}")
        unknown = set(fields) - ROUTING_FIELDS
        if unknown:
            raise ValueError(f"verified source metadata routing field not allowed for {sid}: {sorted(unknown)}")

        if "readability" in fields:
            readability = fields["readability"]
            if readability not in DOWNGRADE_READABILITY:
                raise ValueError(f"readability correction must fail-closed downgrade for {sid}: {readability}")
            source = sources[sid]
            if "readability_intake" not in source:
                source["readability_intake"] = source.get("readability")
            source["readability"] = readability
            source["readability_basis"] = "K2_VERIFIED_SOURCE_METADATA"
            source["readability_review_status"] = "REVIEWED"
    return sources


def patch_validator_module(module):
    """Patch one validator module so source_index returns the effective K2 view."""
    if getattr(module, "_k2_execution_routing_patched", False):
        return module
    raw_source_index = module.source_index

    def effective_source_index(repo):
        sources = raw_source_index(repo)
        rows = load_execution_routing_corrections(repo, sources=sources)
        return apply_verified_source_metadata(sources, rows)

    module._k2_intake_source_index = raw_source_index
    module.source_index = effective_source_index
    module.apply_verified_source_metadata = apply_verified_source_metadata
    module.load_execution_routing_corrections = load_execution_routing_corrections
    module._k2_execution_routing_patched = True
    return module
