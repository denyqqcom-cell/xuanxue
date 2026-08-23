#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
STATE_PATH = K / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json"
ERROR_LEDGER_PATH = K / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl"
BACKLOG_PATH = K / "K2_UNKNOWN_TEXTUAL_BACKLOG.json"
DEEP_LEDGER_PATH = K / "K2_DEEP_READING_LEDGER.jsonl"
SCENARIO_SCHEMA_PATH = K / "schema" / "qimen_scenario_reasoning.schema.json"
STATE_SCHEMA_PATH = K / "schema" / "qimen_cognitive_reconstruction_state.schema.json"
ERROR_SCHEMA_PATH = K / "schema" / "qimen_cognitive_error.schema.json"
CHARTER_PATH = K / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_CHARTER.md"
MODEL_PATH = K / "K2_QIMEN_SCRM_V01.md"

ALLOWED_STATUS = {"OPEN", "REVIEW_REQUIRED", "COMPLETE"}
ALLOWED_CORRECTION = {"CORRECTED", "PARTIALLY_CORRECTED", "OPEN"}
REQUIRED_CATEGORIES = {
    "PROVENANCE",
    "INDEPENDENCE",
    "ROUTING",
    "RULE_SEARCH",
    "METHOD_LAYER",
    "OBSERVATION",
    "RETROSPECTIVE",
    "COVERAGE",
    "SCENARIO",
    "VALIDATION",
    "CONFIDENCE",
    "THEORY_BUILDING",
}
REQUIRED_WORKSTREAMS = {
    "CRITICAL_RETROSPECTIVE",
    "CORPUS_COMPLETION",
    "SCENARIO_MODELING",
    "PROSPECTIVE_VALIDATION",
    "THEORY_ITERATION",
}
REQUIRED_GATES = {
    "theory_boundary_validation_required",
    "scenario_graph_required",
    "reality_anchor_required",
    "competing_explanations_required",
    "counterfactual_required",
    "sensitivity_required",
    "abstention_required",
    "prospective_validation_required",
    "no_book_rule_universalization",
    "no_innovation_credit_without_test",
}
REQUIRED_SCENARIO_FIELDS = {
    "schema_version",
    "case_id",
    "status",
    "question_definition",
    "decision_objective",
    "time_horizon",
    "known_facts",
    "unknowns",
    "actors",
    "constraints",
    "reality_anchor",
    "scenario_graph",
    "symbolic_mapping_hypotheses",
    "eligible_rule_set",
    "boundary_conditions",
    "competing_explanations",
    "counterfactual_checks",
    "sensitivity_checks",
    "abstention_condition",
    "confidence_components",
    "prediction",
    "empirical_credit",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            raise ValueError(f"invalid JSONL {path}:{n}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"row must be object {path}:{n}")
        rows.append(row)
    return rows


def evidence_ref_path(ref: str) -> str:
    return ref.split("#", 1)[0]


def validate_state(state: dict, backlog: dict, deep_rows: list[dict], bias_rows: list[dict]):
    issues = []
    if state.get("schema_version") != "k2-qimen-cognitive-reconstruction-v1":
        issues.append("state schema_version mismatch")
    if state.get("status") not in ALLOWED_STATUS:
        issues.append("invalid state status")
    if state.get("mode") != "COGNITIVE_RECONSTRUCTION":
        issues.append("mode must be COGNITIVE_RECONSTRUCTION")
    if state.get("active_framework") != "SCRM-v0.1":
        issues.append("active_framework must be SCRM-v0.1")
    if state.get("framework_status") != "CANDIDATE_UNTESTED":
        issues.append("framework must remain CANDIDATE_UNTESTED")
    if state.get("claim_extraction_blocked") is not True:
        issues.append("Claim Extraction must remain blocked")
    if state.get("empirical_credit") != "NONE":
        issues.append("cognitive reconstruction cannot grant empirical credit")

    remaining = backlog.get("remaining_unknown_textual_source_count")
    if not isinstance(remaining, int) or isinstance(remaining, bool) or remaining < 0:
        issues.append("invalid backlog remaining_unknown_textual_source_count")
    else:
        if state.get("global_unknown_textual_backlog") != remaining:
            issues.append("state/backlog count drift")
        expected_coverage = "COMPLETE" if remaining == 0 else "INCOMPLETE"
        if state.get("coverage_status") != expected_coverage:
            issues.append(f"coverage_status must be {expected_coverage}")
        if remaining > 0 and state.get("full_corpus_mastery_claim") is not False:
            issues.append("full corpus mastery cannot be claimed while UNKNOWN backlog remains")
        if remaining > 0 and state.get("status") == "COMPLETE":
            issues.append("reconstruction cannot be COMPLETE while UNKNOWN backlog remains")

    deep_ids = {
        r.get("source_id")
        for r in deep_rows
        if isinstance(r.get("source_id"), str)
        and r.get("source_id", "").startswith("QM-SRC-")
        and r.get("read_status") == "COMPLETE"
        and r.get("review_status") == "REVIEWED"
        and r.get("verification_mode") == "VISUAL_PAGE"
    }
    if state.get("deep_visual_reviewed_source_count") != len(deep_ids):
        issues.append(
            f"deep_visual_reviewed_source_count drift: state={state.get('deep_visual_reviewed_source_count')} actual={len(deep_ids)}"
        )
    if state.get("historical_bias_count") != len(bias_rows):
        issues.append("historical_bias_count drift")

    workstreams = state.get("workstreams")
    if not isinstance(workstreams, list) or set(workstreams) != REQUIRED_WORKSTREAMS or len(workstreams) != len(set(workstreams)):
        issues.append("workstreams must match exact reconstruction contract")
    gates = state.get("gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED_GATES or any(v is not True for v in gates.values()):
        issues.append("all reconstruction gates must exist and remain true")
    return issues


def validate_bias_rows(rows: list[dict], root: Path):
    issues = []
    seen = set()
    categories = set()
    for i, row in enumerate(rows, 1):
        bid = row.get("bias_id")
        if not isinstance(bid, str) or not bid.startswith("QCR-BIAS-"):
            issues.append(f"row {i}: invalid bias_id")
        elif bid in seen:
            issues.append(f"row {i}: duplicate bias_id {bid}")
        else:
            seen.add(bid)
        category = row.get("category")
        if category not in REQUIRED_CATEGORIES:
            issues.append(f"{bid}: invalid category {category}")
        else:
            categories.add(category)
        if row.get("correction_status") not in ALLOWED_CORRECTION:
            issues.append(f"{bid}: invalid correction_status")
        if row.get("empirical_credit") != "NONE":
            issues.append(f"{bid}: cognitive error repair cannot grant empirical credit")
        for field in ("historical_pattern", "why_wrong", "current_control", "residual_risk", "next_test"):
            value = row.get(field)
            if not isinstance(value, str) or len(value.strip()) < 10:
                issues.append(f"{bid}: weak/missing {field}")
        refs = row.get("evidence_refs")
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            issues.append(f"{bid}: evidence_refs must be non-empty unique list")
        else:
            for ref in refs:
                if not isinstance(ref, str) or not ref:
                    issues.append(f"{bid}: invalid evidence_ref")
                    continue
                p = root / evidence_ref_path(ref)
                if not p.exists():
                    issues.append(f"{bid}: missing evidence ref path {evidence_ref_path(ref)}")
    if categories != REQUIRED_CATEGORIES:
        issues.append(f"bias category coverage mismatch: missing={sorted(REQUIRED_CATEGORIES-categories)}")
    if not any(r.get("correction_status") == "OPEN" for r in rows):
        issues.append("ledger must preserve unresolved cognitive risk; all-corrected state is not credible yet")
    return issues


def validate_scenario_schema(schema: dict):
    issues = []
    required = schema.get("required")
    if not isinstance(required, list) or set(required) != REQUIRED_SCENARIO_FIELDS:
        issues.append("scenario schema required-field contract drift")
    props = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    for field in REQUIRED_SCENARIO_FIELDS:
        if field not in props:
            issues.append(f"scenario schema missing property {field}")
    if props.get("empirical_credit", {}).get("const") != "NONE":
        issues.append("scenario case must not auto-grant empirical credit")
    comp = props.get("competing_explanations", {})
    if comp.get("minItems", 0) < 2:
        issues.append("scenario contract requires at least two competing explanations")
    if props.get("counterfactual_checks", {}).get("minItems", 0) < 1:
        issues.append("scenario contract requires counterfactual checks")
    if props.get("sensitivity_checks", {}).get("minItems", 0) < 1:
        issues.append("scenario contract requires sensitivity checks")
    return issues


def validate_docs(charter: str, model: str):
    issues = []
    for needle in (
        "理论—边界—验证",
        "full_corpus_mastery_claim = false",
        "QCIC：Epistemic Control Shell",
        "SCRM：Scenario-Conditioned Relational Model",
        "92",
    ):
        if needle not in charter:
            issues.append(f"charter missing invariant: {needle}")
    for needle in (
        "CANDIDATE_UNTESTED",
        "Empirical Credit：`NONE`",
        "Scenario State Graph",
        "Competing Explanations",
        "Counterfactual Stress Test",
        "Sensitivity Analysis",
        "Abstention 是正式输出",
        "SCRM-H5",
    ):
        if needle not in model:
            issues.append(f"SCRM model missing invariant: {needle}")
    return issues


def validate(repo: Path = ROOT):
    k = repo / "knowledge"
    required_paths = [
        k / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json",
        k / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl",
        k / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_CHARTER.md",
        k / "K2_QIMEN_SCRM_V01.md",
        k / "K2_UNKNOWN_TEXTUAL_BACKLOG.json",
        k / "K2_DEEP_READING_LEDGER.jsonl",
        k / "schema" / "qimen_cognitive_reconstruction_state.schema.json",
        k / "schema" / "qimen_cognitive_error.schema.json",
        k / "schema" / "qimen_scenario_reasoning.schema.json",
    ]
    missing = [str(p.relative_to(repo)) for p in required_paths if not p.exists()]
    if missing:
        return [f"missing required artifact(s): {missing}"]

    state = load_json(k / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json")
    backlog = load_json(k / "K2_UNKNOWN_TEXTUAL_BACKLOG.json")
    deep_rows = load_jsonl(k / "K2_DEEP_READING_LEDGER.jsonl")
    bias_rows = load_jsonl(k / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl")
    scenario_schema = load_json(k / "schema" / "qimen_scenario_reasoning.schema.json")
    charter = (k / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_CHARTER.md").read_text(encoding="utf-8")
    model = (k / "K2_QIMEN_SCRM_V01.md").read_text(encoding="utf-8")

    issues = []
    issues.extend(validate_state(state, backlog, deep_rows, bias_rows))
    issues.extend(validate_bias_rows(bias_rows, repo))
    issues.extend(validate_scenario_schema(scenario_schema))
    issues.extend(validate_docs(charter, model))
    return issues


def main():
    try:
        issues = validate(ROOT)
    except Exception as exc:
        print(f"k2-qimen-cognitive-reconstruction: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if issues:
        print("k2-qimen-cognitive-reconstruction: FAIL", file=sys.stderr)
        for issue in issues[:40]:
            print(f"- {issue}", file=sys.stderr)
        raise SystemExit(1)
    state = load_json(STATE_PATH)
    print("k2-qimen-cognitive-reconstruction: PASS")
    print(
        f"status={state['status']} framework={state['active_framework']} empirical_credit=NONE "
        f"unknown_backlog={state['global_unknown_textual_backlog']} deep_visual_sources={state['deep_visual_reviewed_source_count']} "
        f"biases={state['historical_bias_count']}"
    )


if __name__ == "__main__":
    main()
