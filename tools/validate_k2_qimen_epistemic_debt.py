#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
LEDGER = K / "K2_QIMEN_EPISTEMIC_DEBT.jsonl"
PROTOCOL = K / "K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md"
AUDIT = K / "K2_QIMEN_RETREAT_AUDIT_2026-08-28.md"
BIAS_LEDGER = K / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl"
SCHEMA = K / "schema" / "qimen_epistemic_debt.schema.json"

EXPECTED_CATEGORIES = {
    "SOURCE_AUTHORITY",
    "SELF_INFERENCE_PRIVILEGE",
    "COUNT_BASED_PROMOTION",
    "UNCALIBRATED_PARAMETER",
    "RETROSPECTIVE_REPAIR",
    "TRADITION_IMMUNITY",
    "KNOWN_BIAS_RECURRENCE",
}
EXPECTED_FIELDS = {
    "schema_version",
    "debt_id",
    "category",
    "learning_record_refs",
    "historical_bias_refs",
    "observed_pattern",
    "why_prior_reflection_failed",
    "epistemic_failure",
    "prohibited_shortcut",
    "promotion_status",
    "required_before_release",
    "theory_impact",
    "resolution_status",
    "empirical_credit",
}
RELEASE_FIELDS = {
    "predefined_protocol",
    "unknown_outcome",
    "independence_assessment",
    "baseline_or_counterfactual",
    "negative_evidence",
    "falsification_rule",
    "sample_adequacy_rule",
}
REQUIRED_PROTOCOL_INVARIANTS = (
    "SOURCE_FIDELITY != EMPIRICAL_VALIDITY",
    "SELF_GENERATED_INFERENCE != EPISTEMIC_PRIVILEGE",
    "KNOWN_OUTCOME_REPAIR != VALIDATION",
    "CASE_COUNT != INDEPENDENCE",
    "THREE_SUCCESSES != VALIDATION",
    "UNCALIBRATED_WEIGHT != MODEL",
    "TRADITIONAL_STATUS != IMMUNITY_FROM_FALSIFICATION",
    "REFLECTION_RECORD != CORRECTION",
    "RECURRENT_BIAS => PROMOTION_BLOCKED",
    "NEGATIVE_EVIDENCE_IS_FIRST_CLASS",
    "BASELINE_OR_COUNTERFACTUAL_REQUIRED",
)
ALLOWED_IMPACT = {
    "REWRITE_REQUIRED",
    "DOWNGRADE_IF_FAILS",
    "REMOVE_IF_FAILS",
    "RETAIN_AS_HYPOTHESIS_ONLY",
}
ALLOWED_RESOLUTION = {"OPEN", "PARTIALLY_REPAIRED", "REPAIRED"}


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


def ref_path(ref: str) -> str:
    return ref.split("#", 1)[0]


def known_bias_ids(root: Path):
    return {
        row.get("bias_id")
        for row in load_jsonl(root / "knowledge" / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl")
        if isinstance(row.get("bias_id"), str)
    }


def validate_schema_contract(schema: dict):
    issues = []
    required = schema.get("required")
    if not isinstance(required, list) or set(required) != EXPECTED_FIELDS:
        issues.append("epistemic-debt schema required fields drift")
    props = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    if props.get("schema_version", {}).get("const") != "k2-qimen-epistemic-debt-v1":
        issues.append("schema_version const drift")
    if props.get("promotion_status", {}).get("const") != "BLOCKED":
        issues.append("schema must fail closed with promotion_status=BLOCKED")
    if props.get("empirical_credit", {}).get("const") != "NONE":
        issues.append("schema must keep empirical_credit=NONE")
    release = props.get("required_before_release", {})
    release_required = release.get("required")
    if not isinstance(release_required, list) or set(release_required) != RELEASE_FIELDS:
        issues.append("required_before_release schema fields drift")
    release_props = release.get("properties") if isinstance(release.get("properties"), dict) else {}
    for gate in (
        "predefined_protocol",
        "unknown_outcome",
        "independence_assessment",
        "baseline_or_counterfactual",
        "negative_evidence",
    ):
        if release_props.get(gate, {}).get("const") is not True:
            issues.append(f"schema release gate must be const true: {gate}")
    return issues


def validate_rows(rows: list[dict], root: Path, bias_ids: set[str]):
    issues = []
    seen_ids = set()
    seen_categories = set()
    for idx, row in enumerate(rows, 1):
        did = row.get("debt_id") or f"row-{idx}"
        if set(row) != EXPECTED_FIELDS:
            issues.append(f"{did}: field contract drift")
        if row.get("schema_version") != "k2-qimen-epistemic-debt-v1":
            issues.append(f"{did}: schema_version mismatch")
        if not isinstance(row.get("debt_id"), str) or not re.fullmatch(r"QED-[0-9]{3}", row.get("debt_id", "")):
            issues.append(f"{did}: invalid debt_id")
        elif row["debt_id"] in seen_ids:
            issues.append(f"{did}: duplicate debt_id")
        else:
            seen_ids.add(row["debt_id"])

        category = row.get("category")
        if category not in EXPECTED_CATEGORIES:
            issues.append(f"{did}: invalid category {category}")
        else:
            seen_categories.add(category)

        refs = row.get("learning_record_refs")
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            issues.append(f"{did}: learning_record_refs must be non-empty unique list")
        else:
            for ref in refs:
                if not isinstance(ref, str) or not ref:
                    issues.append(f"{did}: invalid learning_record_ref")
                    continue
                path = root / ref_path(ref)
                if not path.exists():
                    issues.append(f"{did}: missing learning record {ref_path(ref)}")

        hist = row.get("historical_bias_refs")
        if not isinstance(hist, list) or not hist or len(hist) != len(set(hist)):
            issues.append(f"{did}: historical_bias_refs must be non-empty unique list")
        else:
            unknown = sorted(set(hist) - bias_ids)
            if unknown:
                issues.append(f"{did}: unknown historical bias refs {unknown}")

        for field in (
            "observed_pattern",
            "why_prior_reflection_failed",
            "epistemic_failure",
            "prohibited_shortcut",
        ):
            value = row.get(field)
            if not isinstance(value, str) or len(value.strip()) < 10:
                issues.append(f"{did}: weak/missing {field}")

        if row.get("promotion_status") != "BLOCKED":
            issues.append(f"{did}: unresolved epistemic debt must remain promotion BLOCKED")
        if row.get("empirical_credit") != "NONE":
            issues.append(f"{did}: epistemic audit cannot grant empirical credit")
        if row.get("theory_impact") not in ALLOWED_IMPACT:
            issues.append(f"{did}: invalid theory_impact")
        if row.get("resolution_status") not in ALLOWED_RESOLUTION:
            issues.append(f"{did}: invalid resolution_status")

        release = row.get("required_before_release")
        if not isinstance(release, dict) or set(release) != RELEASE_FIELDS:
            issues.append(f"{did}: release field contract drift")
        else:
            for gate in (
                "predefined_protocol",
                "unknown_outcome",
                "independence_assessment",
                "baseline_or_counterfactual",
                "negative_evidence",
            ):
                if release.get(gate) is not True:
                    issues.append(f"{did}: release gate must remain true: {gate}")
            for field in ("falsification_rule", "sample_adequacy_rule"):
                if not isinstance(release.get(field), str) or len(release.get(field, "").strip()) < 20:
                    issues.append(f"{did}: weak/missing release {field}")

        # A recurrence debt is not closed just because somebody wrote a reflection.
        if category == "KNOWN_BIAS_RECURRENCE" and row.get("resolution_status") == "REPAIRED":
            issues.append(f"{did}: recurrence debt cannot be REPAIRED before prospective release evidence exists")

    if seen_categories != EXPECTED_CATEGORIES:
        issues.append(f"epistemic debt category coverage mismatch: missing={sorted(EXPECTED_CATEGORIES-seen_categories)}")
    if len(rows) < len(EXPECTED_CATEGORIES):
        issues.append("epistemic debt ledger must instantiate every required recurrence category")
    if not any(row.get("resolution_status") == "OPEN" for row in rows):
        issues.append("an all-repaired retreat ledger is not credible before prospective validation")
    return issues


def validate_protocol(protocol: str):
    issues = []
    for invariant in REQUIRED_PROTOCOL_INVARIANTS:
        if invariant not in protocol:
            issues.append(f"epistemic debt protocol missing invariant: {invariant}")
    for needle in (
        "source fidelity",
        "unknown-outcome",
        "ablation",
        "baseline",
        "negative evidence",
        "empirical_credit = NONE",
    ):
        if needle.lower() not in protocol.lower():
            issues.append(f"epistemic debt protocol missing control concept: {needle}")
    return issues


def validate_audit(audit: str):
    issues = []
    for did in [f"QED-{n:03d}" for n in range(1, 8)]:
        if did not in audit:
            issues.append(f"retreat audit missing debt reference {did}")
    for needle in (
        "过去不是“没有反省”，而是“反省没有形成复发门禁”",
        "Empirical Credit: `NONE`",
        "自己长出理论",
    ):
        if needle not in audit:
            issues.append(f"retreat audit missing conclusion: {needle}")
    return issues


def validate(repo: Path = ROOT):
    k = repo / "knowledge"
    required = [
        k / "K2_QIMEN_EPISTEMIC_DEBT.jsonl",
        k / "K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md",
        k / "K2_QIMEN_RETREAT_AUDIT_2026-08-28.md",
        k / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl",
        k / "schema" / "qimen_epistemic_debt.schema.json",
    ]
    missing = [str(path.relative_to(repo)) for path in required if not path.exists()]
    if missing:
        return [f"missing epistemic-debt artifact(s): {missing}"]

    rows = load_jsonl(k / "K2_QIMEN_EPISTEMIC_DEBT.jsonl")
    schema = load_json(k / "schema" / "qimen_epistemic_debt.schema.json")
    protocol = (k / "K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md").read_text(encoding="utf-8")
    audit = (k / "K2_QIMEN_RETREAT_AUDIT_2026-08-28.md").read_text(encoding="utf-8")

    issues = []
    issues.extend(validate_schema_contract(schema))
    issues.extend(validate_rows(rows, repo, known_bias_ids(repo)))
    issues.extend(validate_protocol(protocol))
    issues.extend(validate_audit(audit))
    return issues


def main():
    try:
        issues = validate(ROOT)
    except Exception as exc:
        print(f"k2-qimen-epistemic-debt: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if issues:
        print("k2-qimen-epistemic-debt: FAIL", file=sys.stderr)
        for issue in issues[:60]:
            print(f"- {issue}", file=sys.stderr)
        raise SystemExit(1)
    rows = load_jsonl(LEDGER)
    open_count = sum(1 for row in rows if row.get("resolution_status") == "OPEN")
    print("k2-qimen-epistemic-debt: PASS")
    print(f"debts={len(rows)} open={open_count} promotion=BLOCKED empirical_credit=NONE")


if __name__ == "__main__":
    main()
