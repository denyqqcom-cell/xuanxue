#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_k2_prospective_validation as base

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

HARDENING_FREEZE_FIELDS = {"outcome_ontology", "factor_budget", "path_budget", "abstain_lock"}
OUTCOME_ONTOLOGY_FIELDS = {
    "target_domain", "target_variable", "event_definition", "direction", "event_window",
    "threshold", "tolerance", "unit", "scale", "subject_binding", "matching_rule",
    "missingness_handling", "censoring_handling", "scorable_conditions", "non_scorable_conditions",
}
EVENT_WINDOW_FIELDS = {"start_at_utc", "end_at_utc"}
ABSTAIN_LOCK_FIELDS = {
    "decision", "allowed_reason_codes", "selected_reason_code",
    "coverage_denominator", "rewrite_policy",
}
ABSTAIN_DECISIONS = {"PREDICT", "ABSTAIN"}
ABSTAIN_REASON_CODES = {
    "INPUT_PROVENANCE_INSUFFICIENT",
    "FACTOR_PATH_CONFLICT",
    "FACTOR_OUTSIDE_FROZEN_SET",
    "BUDGET_OR_STOP_RULE_EXCEEDED",
}
ABSTAIN_COVERAGE_DENOMINATOR = "ALL_FROZEN_CASES"
ABSTAIN_REWRITE_POLICY = "IMMUTABLE_PRE_OUTCOME_DECISION"
MACHINE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")


def positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def unique_string_list(value, allow_empty=False):
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(base.nonempty_text(item) for item in value)
        and len(value) == len(set(value))
    )


def plan_routes(distillates):
    hypothesis_routes = {}
    for distillate in distillates:
        routes = base.effective_domain_routes(distillate)
        for hypothesis in distillate.get("testable_hypotheses") or []:
            if isinstance(hypothesis, dict) and base.nonempty_text(hypothesis.get("hypothesis_id")):
                hypothesis_routes[hypothesis["hypothesis_id"]] = routes
    return hypothesis_routes


def validate_outcome_ontology(owner_id, ontology, governed_routes):
    issues = []
    if not isinstance(ontology, dict):
        return [(owner_id, "outcome_ontology must be machine-evaluable object")]

    if set(ontology) != OUTCOME_ONTOLOGY_FIELDS:
        issues.append((
            owner_id,
            "outcome_ontology fields mismatch "
            f"missing={sorted(OUTCOME_ONTOLOGY_FIELDS - set(ontology))} "
            f"extra={sorted(set(ontology) - OUTCOME_ONTOLOGY_FIELDS)}",
        ))

    target_domain = ontology.get("target_domain")
    if not base.nonempty_text(target_domain):
        issues.append((owner_id, "outcome_ontology target_domain must be non-empty text"))
    elif governed_routes and target_domain not in governed_routes:
        issues.append((owner_id, f"target_domain outside governed routes: {target_domain}"))

    for field in [
        "target_variable", "event_definition", "subject_binding", "matching_rule",
        "missingness_handling", "censoring_handling",
    ]:
        if not base.nonempty_text(ontology.get(field)):
            issues.append((owner_id, f"outcome_ontology {field} must be non-empty text"))

    for field in ["target_variable", "direction", "matching_rule"]:
        value = ontology.get(field)
        if not isinstance(value, str) or not MACHINE_KEY_RE.match(value):
            issues.append((owner_id, f"outcome_ontology {field} must be uppercase machine key"))

    if not base.nonempty_text(ontology.get("direction")):
        issues.append((owner_id, "outcome_ontology direction must be non-empty text"))

    window = ontology.get("event_window")
    if not isinstance(window, dict):
        issues.append((owner_id, "outcome_ontology event_window must be machine-evaluable object"))
    else:
        if set(window) != EVENT_WINDOW_FIELDS:
            issues.append((
                owner_id,
                "event_window fields mismatch "
                f"missing={sorted(EVENT_WINDOW_FIELDS - set(window))} "
                f"extra={sorted(set(window) - EVENT_WINDOW_FIELDS)}",
            ))
        start = base.utc_value(window.get("start_at_utc"))
        end = base.utc_value(window.get("end_at_utc"))
        if start is None:
            issues.append((owner_id, "event_window start_at_utc must be UTC second timestamp ending Z"))
        if end is None:
            issues.append((owner_id, "event_window end_at_utc must be UTC second timestamp ending Z"))
        if start is not None and end is not None and end <= start:
            issues.append((owner_id, "event_window end must be after start"))

    for field in ["threshold", "tolerance"]:
        value = ontology.get(field)
        if value is not None and not base.finite_number(value):
            issues.append((owner_id, f"{field} must be null or finite numeric"))
    tolerance = ontology.get("tolerance")
    if base.finite_number(tolerance) and tolerance < 0:
        issues.append((owner_id, "tolerance must be non-negative when numeric"))

    unit = ontology.get("unit")
    if unit is not None and not base.nonempty_text(unit):
        issues.append((owner_id, "outcome_ontology unit must be null or non-empty text"))
    if not base.nonempty_text(ontology.get("scale")):
        issues.append((owner_id, "outcome_ontology scale must be non-empty text"))

    for field in ["scorable_conditions", "non_scorable_conditions"]:
        if not unique_string_list(ontology.get(field)):
            issues.append((owner_id, f"outcome_ontology {field} must be non-empty unique string array"))

    return issues


def validate_abstain_lock(owner_id, lock, payload):
    issues = []
    if not isinstance(lock, dict):
        return [(owner_id, "abstain_lock must be machine-evaluable object")]

    if set(lock) != ABSTAIN_LOCK_FIELDS:
        issues.append((
            owner_id,
            "abstain_lock fields mismatch "
            f"missing={sorted(ABSTAIN_LOCK_FIELDS - set(lock))} "
            f"extra={sorted(set(lock) - ABSTAIN_LOCK_FIELDS)}",
        ))

    decision = lock.get("decision")
    if decision not in ABSTAIN_DECISIONS:
        issues.append((owner_id, f"abstain decision must be one of {sorted(ABSTAIN_DECISIONS)}"))

    allowed = lock.get("allowed_reason_codes")
    if not unique_string_list(allowed) or set(allowed) != ABSTAIN_REASON_CODES:
        issues.append((owner_id, "allowed abstain reasons must equal governed reason-code set"))

    selected = lock.get("selected_reason_code")
    if decision == "PREDICT":
        if selected is not None:
            issues.append((owner_id, "PREDICT decision cannot carry selected abstain reason"))
        if payload.get("prediction") == "ABSTAIN":
            issues.append((owner_id, "PREDICT abstain_lock cannot freeze ABSTAIN prediction"))
    elif decision == "ABSTAIN":
        if selected not in ABSTAIN_REASON_CODES or not isinstance(allowed, list) or selected not in allowed:
            issues.append((owner_id, "selected abstain reason must be predeclared governed code"))
        if payload.get("prediction") != "ABSTAIN":
            issues.append((owner_id, "ABSTAIN decision requires frozen prediction=ABSTAIN"))

    if lock.get("coverage_denominator") != ABSTAIN_COVERAGE_DENOMINATOR:
        issues.append((owner_id, "coverage_denominator must retain all frozen cases"))
    if lock.get("rewrite_policy") != ABSTAIN_REWRITE_POLICY:
        issues.append((owner_id, "abstain rewrite_policy must forbid post-outcome decision rewrite"))

    return issues


def validate_hardening(distillates, plans, batches, freezes, outcomes):
    del batches
    issues = []
    routes_by_hypothesis = plan_routes(distillates)
    plan_by_id = {}
    freeze_by_id = {}

    for plan in plans:
        plan_id = plan.get("plan_id") or "<missing>"
        plan_by_id[plan_id] = plan
        required = plan.get("freeze_required_fields")
        if isinstance(required, list):
            missing = HARDENING_FREEZE_FIELDS - set(required)
            if missing:
                issues.append((plan_id, f"freeze_required_fields missing hardening fields: {sorted(missing)}"))
        else:
            issues.append((plan_id, "freeze_required_fields missing hardening fields"))

    for freeze in freezes:
        freeze_id = freeze.get("freeze_id") or "<missing>"
        freeze_by_id[freeze_id] = freeze
        plan = plan_by_id.get(freeze.get("plan_id"))
        governed_routes = routes_by_hypothesis.get(plan.get("hypothesis_id"), []) if plan else []
        payload = freeze.get("frozen_payload")
        if not isinstance(payload, dict):
            continue

        issues.extend(validate_outcome_ontology(freeze_id, payload.get("outcome_ontology"), governed_routes))

        factor_budget = payload.get("factor_budget")
        if not positive_int(factor_budget):
            issues.append((freeze_id, "factor_budget must be positive integer"))
        eligible = payload.get("eligible_rule_set")
        if not unique_string_list(eligible):
            issues.append((freeze_id, "eligible_rule_set must be non-empty unique string array for budget audit"))
        elif positive_int(factor_budget) and len(eligible) > factor_budget:
            issues.append((freeze_id, "eligible_rule_set exceeds factor_budget"))

        path_budget = payload.get("path_budget")
        if not positive_int(path_budget):
            issues.append((freeze_id, "path_budget must be positive integer"))
        path = payload.get("interpretation_path")
        if not unique_string_list(path):
            issues.append((freeze_id, "interpretation_path must be non-empty unique string array for budget audit"))
        elif positive_int(path_budget) and len(path) > path_budget:
            issues.append((freeze_id, "interpretation_path exceeds path_budget"))

        issues.extend(validate_abstain_lock(freeze_id, payload.get("abstain_lock"), payload))

    for outcome in outcomes:
        outcome_id = outcome.get("outcome_id") or "<missing>"
        freeze = freeze_by_id.get(outcome.get("freeze_id"))
        payload = freeze.get("frozen_payload") if isinstance(freeze, dict) else None
        lock = payload.get("abstain_lock") if isinstance(payload, dict) else None
        if not isinstance(lock, dict):
            continue
        decision = lock.get("decision")
        evaluation = outcome.get("evaluation")
        if decision == "PREDICT" and evaluation == "ABSTAIN":
            issues.append((outcome_id, "post-outcome PREDICT to ABSTAIN rewrite forbidden"))
        if decision == "ABSTAIN" and evaluation != "ABSTAIN":
            issues.append((outcome_id, "pre-outcome ABSTAIN decision cannot be rescored as evaluable"))
        if decision == "ABSTAIN" and outcome.get("score_components") not in ({}, None):
            issues.append((outcome_id, "pre-outcome ABSTAIN decision cannot carry evaluable score components"))

    return issues


def fail(message):
    print(f"k2-prospective-hardening: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    project = base.load_json(K / "PROJECT_STATE.json")
    if project.get("phase") != "K2_EVIDENCE_EXTRACTION":
        fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:
        fail("Claim Extraction must remain blocked")

    distillates = base.load_work_family_distillates(ROOT)
    plans = base.load_jsonl(K / "K2_PROSPECTIVE_TEST_PLANS.jsonl")
    batches = base.load_jsonl(K / "K2_PROSPECTIVE_BATCHES.jsonl")
    freezes = base.load_jsonl(K / "K2_PROSPECTIVE_FREEZES.jsonl")
    outcomes = base.load_jsonl(K / "K2_PROSPECTIVE_OUTCOMES.jsonl")
    policies = base.load_empirical_credit_policies(ROOT)

    base_issues = base.validate_records(distillates, plans, batches, freezes, outcomes, policies)
    if base_issues:
        fail(f"base prospective contract issues={len(base_issues)} first={base_issues[0][0]}: {base_issues[0][1]}")

    issues = validate_hardening(distillates, plans, batches, freezes, outcomes)
    if issues:
        fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")

    print("k2-prospective-hardening: PASS")
    print(f"plans={len(plans)} freezes={len(freezes)} outcomes={len(outcomes)} issues=0")
    print("scope=OUTCOME_ONTOLOGY_FREEZE+FACTOR_PATH_BUDGETS+ABSTAIN_COVERAGE_LOCK")
    print("versioned_preoutcome_revision=NOT_IMPLEMENTED")
    print("abstain_coverage_lock=IMPLEMENTED")
    print("empirical_credit_upgrade_blocked=true")


if __name__ == "__main__":
    main()
