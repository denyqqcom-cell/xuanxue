#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

REGISTRY = "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl"
REGISTRY_SHARD_DIR = "K2_QIMEN_TBV_REVIEW_REGISTRY.d"
CORRECTIONS = "K2_QIMEN_TBV_REVIEW_CORRECTIONS.jsonl"
STATE = "K2_QIMEN_TBV_STATE.json"
BACKLOG = "K2_UNKNOWN_TEXTUAL_BACKLOG.json"
DEEP_LEDGER = "K2_DEEP_READING_LEDGER.jsonl"
WORK_FAMILY = "K2_WORK_FAMILY_DISTILLATES.jsonl"
WORK_FAMILY_SHARD_DIR = "K2_WORK_FAMILY_DISTILLATES.d"
PROTOCOL = "K2_QIMEN_TBV_PROTOCOL.md"

EXPECTED_WAVE_A = {
    "QM-SRC-0015",
    "QM-SRC-0017",
    "QM-SRC-0019",
    "QM-SRC-0020",
    "QM-SRC-0021",
    "WF-QM-JIADUN-ZHENSHOU-001",
}
EXPECTED_WAVE_B_SEED = {
    "WF-QM-SANYUAN-QIMEN-001",
    "WF-QM-JINHAN-YUJING-001",
}

ALLOWED_UNIT_TYPES = {"DEEP_SOURCE", "WORK_FAMILY"}
ALLOWED_OPERATIONAL = {
    "SOURCE_LOCAL_CANDIDATE",
    "BOUNDARY_ONLY",
    "MIXED_STANCE_HOLD",
    "HISTORICAL_ONLY",
    "HOLD",
}
ALLOWED_CONTEXT = {"EXPLICIT", "PARTIAL", "UNCLEAR"}
ALLOWED_CREDIT = {"STRONG", "CANDIDATE", "NOT_TESTED"}
CORRECTION_FIELDS = {
    "schema_version",
    "correction_id",
    "review_id",
    "unit_id",
    "reason",
    "source_ref",
    "review_status",
    "patch",
}
ALLOWED_CORRECTION_PATCH_FIELDS = {
    "theory_core",
    "boundary_context",
    "validation",
    "scenario_contribution",
    "falsification_requirements",
    "source_anchor_refs",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            raise ValueError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"row must be object {path}:{line_no}")
        rows.append(row)
    return rows


def deep_visual_ids(rows):
    return {
        row.get("source_id")
        for row in rows
        if isinstance(row.get("source_id"), str)
        and row.get("source_id", "").startswith("QM-SRC-")
        and row.get("read_status") == "COMPLETE"
        and row.get("review_status") == "REVIEWED"
        and row.get("verification_mode") == "VISUAL_PAGE"
    }


def load_registry_rows(k: Path):
    rows = load_jsonl(k / REGISTRY)
    shard_dir = k / REGISTRY_SHARD_DIR
    if shard_dir.exists():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def load_effective_registry_rows(k: Path, repo: Path):
    raw_rows = load_registry_rows(k)
    issues = []
    correction_path = k / CORRECTIONS
    if not correction_path.exists():
        return raw_rows, [f"missing TBV correction overlay: {CORRECTIONS}"]

    corrections = load_jsonl(correction_path)
    by_review = {
        row.get("review_id"): copy.deepcopy(row)
        for row in raw_rows
        if isinstance(row.get("review_id"), str)
    }
    seen_ids = set()
    seen_targets = set()

    for idx, correction in enumerate(corrections, 1):
        cid = correction.get("correction_id") or f"correction-{idx}"
        if set(correction) != CORRECTION_FIELDS:
            issues.append(f"{cid}: TBV correction fields drift")
        if correction.get("schema_version") != "k2-qimen-tbv-review-correction-v1":
            issues.append(f"{cid}: TBV correction schema_version mismatch")
        if not isinstance(correction.get("correction_id"), str) or not correction.get("correction_id", "").startswith("QTBVC-"):
            issues.append(f"{cid}: invalid TBV correction_id")
        elif cid in seen_ids:
            issues.append(f"duplicate TBV correction_id: {cid}")
        else:
            seen_ids.add(cid)

        review_id = correction.get("review_id")
        unit_id = correction.get("unit_id")
        target_key = (review_id, unit_id)
        if target_key in seen_targets:
            issues.append(f"{cid}: duplicate TBV correction target {review_id}/{unit_id}")
        else:
            seen_targets.add(target_key)

        target = by_review.get(review_id)
        if target is None:
            issues.append(f"{cid}: unknown TBV correction review_id {review_id}")
        elif target.get("unit_id") != unit_id:
            issues.append(f"{cid}: TBV correction unit_id does not match target")

        reason = correction.get("reason")
        if not isinstance(reason, str) or len(reason.strip()) < 20:
            issues.append(f"{cid}: weak/missing TBV correction reason")
        if correction.get("review_status") != "REVIEWED":
            issues.append(f"{cid}: TBV correction must be REVIEWED")

        source_ref = correction.get("source_ref")
        if not isinstance(source_ref, str) or not source_ref:
            issues.append(f"{cid}: invalid TBV correction source_ref")
        else:
            source_path = repo / source_ref.split("#", 1)[0]
            if not source_path.exists():
                issues.append(f"{cid}: missing TBV correction source_ref {source_ref}")
            if not source_ref.startswith("knowledge/K2_DEEP_SOURCE_DISTILLATES.d/"):
                issues.append(f"{cid}: TBV correction source_ref must bind reviewed deep-source distillate")

        patch = correction.get("patch")
        if not isinstance(patch, dict) or not patch:
            issues.append(f"{cid}: TBV correction patch must be non-empty object")
            continue
        forbidden = set(patch) - ALLOWED_CORRECTION_PATCH_FIELDS
        if forbidden:
            issues.append(f"{cid}: forbidden TBV correction patch field(s): {sorted(forbidden)}")
        if target is not None and not forbidden:
            for field, value in patch.items():
                target[field] = copy.deepcopy(value)

    effective = []
    for raw in raw_rows:
        rid = raw.get("review_id")
        effective.append(by_review.get(rid, copy.deepcopy(raw)))
    return effective, issues


def load_work_family_rows(k: Path):
    rows = load_jsonl(k / WORK_FAMILY)
    shard_dir = k / WORK_FAMILY_SHARD_DIR
    if shard_dir.exists():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def validate_row(row: dict, idx: int, repo: Path, deep_ids: set[str], work_family_ids: set[str]):
    issues = []
    rid = row.get("review_id") or f"row-{idx}"
    if row.get("schema_version") != "k2-qimen-tbv-review-v1":
        issues.append(f"{rid}: schema_version mismatch")
    if not isinstance(row.get("review_id"), str) or not row.get("review_id", "").startswith("QTBV-"):
        issues.append(f"{rid}: invalid review_id")
    if row.get("unit_type") not in ALLOWED_UNIT_TYPES:
        issues.append(f"{rid}: invalid unit_type")
    unit_id = row.get("unit_id")
    if not isinstance(unit_id, str) or not unit_id:
        issues.append(f"{rid}: missing unit_id")
    elif row.get("unit_type") == "DEEP_SOURCE" and unit_id not in deep_ids:
        issues.append(f"{rid}: DEEP_SOURCE is not COMPLETE/REVIEWED/VISUAL_PAGE: {unit_id}")
    elif row.get("unit_type") == "WORK_FAMILY" and unit_id not in work_family_ids:
        issues.append(f"{rid}: unknown reviewed work family: {unit_id}")

    if row.get("universalization_status") != "BLOCKED":
        issues.append(f"{rid}: universalization must remain BLOCKED")
    if row.get("operational_status") not in ALLOWED_OPERATIONAL:
        issues.append(f"{rid}: invalid operational_status")
    if row.get("claim_extraction_blocked") is not True:
        issues.append(f"{rid}: Claim Extraction must remain blocked")
    if row.get("empirical_credit") != "NONE":
        issues.append(f"{rid}: empirical_credit must remain NONE")

    for field in ("theory_core", "scenario_contribution", "falsification_requirements", "source_anchor_refs", "source_refs"):
        value = row.get(field)
        if not isinstance(value, list) or not value:
            issues.append(f"{rid}: {field} must be non-empty list")

    for ref in row.get("source_refs", []):
        if not isinstance(ref, str) or not ref:
            issues.append(f"{rid}: invalid source_ref")
            continue
        if not (repo / ref.split("#", 1)[0]).exists():
            issues.append(f"{rid}: missing source_ref path {ref}")

    boundary = row.get("boundary_context")
    if not isinstance(boundary, dict):
        issues.append(f"{rid}: missing boundary_context")
    else:
        required = {
            "question_domains",
            "method_layers",
            "role_frames",
            "temporal_models",
            "source_school_context",
            "prerequisites",
            "exclusions",
            "context_status",
        }
        if set(boundary) != required:
            issues.append(f"{rid}: boundary_context fields drift")
        for field in ("question_domains", "method_layers", "role_frames", "temporal_models", "prerequisites", "exclusions"):
            if not isinstance(boundary.get(field), list) or not boundary.get(field):
                issues.append(f"{rid}: boundary {field} must be non-empty list")
        if not isinstance(boundary.get("source_school_context"), str) or len(boundary.get("source_school_context", "").strip()) < 10:
            issues.append(f"{rid}: weak source_school_context")
        if boundary.get("context_status") not in ALLOWED_CONTEXT:
            issues.append(f"{rid}: invalid context_status")
        if boundary.get("context_status") == "UNCLEAR" and row.get("operational_status") != "HOLD":
            issues.append(f"{rid}: UNCLEAR boundary requires HOLD")

    validation = row.get("validation")
    if not isinstance(validation, dict):
        issues.append(f"{rid}: missing validation")
    else:
        required = {"source_credit", "structure_credit", "method_credit", "empirical_credit", "validation_limits"}
        if set(validation) != required:
            issues.append(f"{rid}: validation fields drift")
        expected_source_credit = "FULL_SOURCE_VISUAL_REVIEWED" if row.get("unit_type") == "DEEP_SOURCE" else "FULL_WORK_FAMILY_REVIEWED"
        if validation.get("source_credit") != expected_source_credit:
            issues.append(f"{rid}: source_credit mismatch for unit_type")
        if validation.get("structure_credit") not in ALLOWED_CREDIT:
            issues.append(f"{rid}: invalid structure_credit")
        if validation.get("method_credit") not in ALLOWED_CREDIT:
            issues.append(f"{rid}: invalid method_credit")
        if validation.get("empirical_credit") != "NONE":
            issues.append(f"{rid}: nested empirical_credit must remain NONE")
        if not isinstance(validation.get("validation_limits"), list) or not validation.get("validation_limits"):
            issues.append(f"{rid}: validation_limits must be non-empty")
    return issues


def validate(repo: Path = ROOT):
    k = repo / "knowledge"
    required_paths = [
        k / REGISTRY,
        k / CORRECTIONS,
        k / STATE,
        k / BACKLOG,
        k / DEEP_LEDGER,
        k / WORK_FAMILY,
        k / PROTOCOL,
        k / "schema" / "qimen_tbv_review.schema.json",
        k / "schema" / "qimen_tbv_review_correction.schema.json",
        k / "schema" / "qimen_tbv_state.schema.json",
    ]
    missing = [str(p.relative_to(repo)) for p in required_paths if not p.exists()]
    if missing:
        return [f"missing TBV artifact(s): {missing}"]

    registry, correction_issues = load_effective_registry_rows(k, repo)
    state = load_json(k / STATE)
    backlog = load_json(k / BACKLOG)
    deep_rows = load_jsonl(k / DEEP_LEDGER)
    family_rows = load_work_family_rows(k)
    protocol = (k / PROTOCOL).read_text(encoding="utf-8")

    deep_ids = deep_visual_ids(deep_rows)
    work_family_by_id = {
        r.get("work_family_key"): r
        for r in family_rows
        if isinstance(r.get("work_family_key"), str)
    }
    work_family_ids = set(work_family_by_id)
    issues = list(correction_issues)

    seen_review_ids = set()
    seen_units = set()
    for idx, row in enumerate(registry, 1):
        rid = row.get("review_id")
        uid = row.get("unit_id")
        if rid in seen_review_ids:
            issues.append(f"duplicate review_id: {rid}")
        seen_review_ids.add(rid)
        if uid in seen_units:
            issues.append(f"duplicate TBV unit: {uid}")
        seen_units.add(uid)
        issues.extend(validate_row(row, idx, repo, deep_ids, work_family_ids))

    if not EXPECTED_WAVE_A.issubset(seen_units):
        issues.append(f"Wave A coverage missing: {sorted(EXPECTED_WAVE_A-seen_units)}")
    if not EXPECTED_WAVE_B_SEED.issubset(seen_units):
        issues.append(f"Wave B seed coverage missing: {sorted(EXPECTED_WAVE_B_SEED-seen_units)}")

    if state.get("schema_version") != "k2-qimen-tbv-state-v1":
        issues.append("TBV state schema_version mismatch")
    if state.get("status") not in {"PARTIAL", "COMPLETE"}:
        issues.append("invalid TBV state status")
    if state.get("claim_extraction_blocked") is not True:
        issues.append("TBV state must keep Claim Extraction blocked")
    if state.get("empirical_credit") != "NONE":
        issues.append("TBV state empirical_credit must remain NONE")
    if state.get("universalized_rule_count") != 0:
        issues.append("TBV cannot universalize rules during K2B")
    if state.get("empirical_validated_rule_count") != 0:
        issues.append("TBV cannot create empirically validated rules")

    registry_deep_ids = {r.get("unit_id") for r in registry if r.get("unit_type") == "DEEP_SOURCE"}
    registry_family_ids = {r.get("unit_id") for r in registry if r.get("unit_type") == "WORK_FAMILY"}
    if state.get("reviewed_unit_count") != len(registry):
        issues.append("reviewed_unit_count drift")
    if state.get("reviewed_deep_source_count") != len(registry_deep_ids):
        issues.append("reviewed_deep_source_count drift")
    if state.get("reviewed_work_family_count") != len(registry_family_ids):
        issues.append("reviewed_work_family_count drift")
    if state.get("reviewed_deep_source_ids") != sorted(registry_deep_ids):
        issues.append("reviewed_deep_source_ids drift")
    if state.get("reviewed_work_family_ids") != sorted(registry_family_ids):
        issues.append("reviewed_work_family_ids drift")
    if state.get("known_deep_visual_reviewed_source_count") != len(deep_ids):
        issues.append("known_deep_visual_reviewed_source_count drift")

    family_member_deep_ids = set()
    for family_id in registry_family_ids:
        family = work_family_by_id.get(family_id)
        if not family:
            continue
        refs = family.get("member_refs")
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if not isinstance(ref, str) or not ref:
                continue
            source_id = ref.split("#", 1)[0]
            if source_id in deep_ids:
                family_member_deep_ids.add(source_id)

    effective_deep_ids = registry_deep_ids | family_member_deep_ids
    remaining_deep_ids = deep_ids - effective_deep_ids
    if state.get("effective_deep_source_coverage_count") != len(effective_deep_ids):
        issues.append("effective_deep_source_coverage_count drift")
    if state.get("effective_deep_source_coverage_ids") != sorted(effective_deep_ids):
        issues.append("effective_deep_source_coverage_ids drift")
    if state.get("remaining_deep_source_tbv_ids") != sorted(remaining_deep_ids):
        issues.append("remaining_deep_source_tbv_ids drift")

    remaining = backlog.get("remaining_unknown_textual_source_count")
    if state.get("global_unknown_textual_backlog") != remaining:
        issues.append("TBV state/backlog count drift")
    expected_full = not remaining_deep_ids and remaining == 0
    if state.get("full_reviewed_material_tbv_coverage") is not expected_full:
        issues.append(f"full_reviewed_material_tbv_coverage must be {str(expected_full).lower()}")
    expected_status = "COMPLETE" if expected_full else "PARTIAL"
    if state.get("status") != expected_status:
        issues.append(f"TBV state status must be {expected_status}")

    for needle in (
        "Theory — Boundary — Validation",
        "SOURCE CONTAINS RULE != RULE IS UNIVERSAL",
        "SOURCE ENDORSES RULE != RULE IS EMPIRICALLY VALID",
        "universalization_status = BLOCKED",
        "empirical_credit = NONE",
        "GLOBAL_UNKNOWN_BACKLOG = MACHINE_DERIVED",
        "KNOWN_OUTCOME_TRAINING != PROSPECTIVE_EVALUATION",
        "COVERAGE CREDIT != INDEPENDENT EVIDENCE VOTE",
        "PREDEFINED PROCEDURAL BRANCHING != POST-HOC INTERPRETIVE SEARCH",
        "CALCULATION CONSISTENCY != REAL-WORLD VALIDITY",
        "TEXTUAL PRECISION != EMPIRICAL VALIDATION",
        "EDITORIAL REPETITION != INDEPENDENT CORROBORATION",
        "SOURCE CONTAINS METHOD != SOURCE ENDORSES METHOD",
    ):
        if needle not in protocol:
            issues.append(f"TBV protocol missing invariant: {needle}")
    return issues


def main():
    try:
        issues = validate(ROOT)
    except Exception as exc:
        print(f"k2-qimen-tbv: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if issues:
        print("k2-qimen-tbv: FAIL", file=sys.stderr)
        for issue in issues[:50]:
            print(f"- {issue}", file=sys.stderr)
        raise SystemExit(1)
    state = load_json(K / STATE)
    corrections = load_jsonl(K / CORRECTIONS)
    print("k2-qimen-tbv: PASS")
    print(
        f"status={state['status']} reviewed_units={state['reviewed_unit_count']} "
        f"deep_units={state['reviewed_deep_source_count']} "
        f"effective_deep_sources={state['effective_deep_source_coverage_count']}/{state['known_deep_visual_reviewed_source_count']} "
        f"corrections={len(corrections)} unknown_backlog={state['global_unknown_textual_backlog']} empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
