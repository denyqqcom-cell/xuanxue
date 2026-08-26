#!/usr/bin/env python3
import json
import re
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
CHARTER_PATH = K / "K2_QIMEN_DEEP_RETREAT_V12.md"
MODEL_PATH = K / "K2_QIMEN_SCRM_V02.md"

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
    "world_model_pre_symbolic_freeze_required",
    "comparator_information_parity_required",
    "model_version_freeze_required",
    "abstention_coverage_accounting_required",
    "dynamic_state_machine_derived_required",
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
    "information_order",
    "symbolic_mapping_hypotheses",
    "eligible_rule_set",
    "boundary_conditions",
    "competing_explanations",
    "comparator_parity",
    "counterfactual_checks",
    "sensitivity_checks",
    "decision_tie_break_policy",
    "model_freeze",
    "abstention_policy",
    "confidence_components",
    "prediction",
    "empirical_credit",
}
REQUIRED_TIE_BREAK_FIELDS = {
    "applies",
    "candidate_outputs",
    "selection_rule",
    "selected_output",
    "freeze_status",
}
REQUIRED_TIE_BREAK_STATUS = {"FROZEN", "NOT_APPLICABLE", "UNRESOLVED"}
REQUIRED_INFORMATION_ORDER_FIELDS = {
    "world_model_freeze_status",
    "symbolic_inputs_hidden_until_world_freeze",
    "outcome_known_at_freeze",
    "information_cutoff",
    "contamination_status",
}
REQUIRED_COMPARATOR_PARITY_FIELDS = {
    "shared_reality_information",
    "shared_information_cutoff",
    "symbolic_increment_isolated",
    "freeze_status",
}
REQUIRED_MODEL_FREEZE_FIELDS = {"scrm_version", "qcic_version", "method_variants", "freeze_status"}
REQUIRED_ABSTENTION_FIELDS = {"trigger_conditions", "decision_rule", "freeze_status", "coverage_accounting"}
DYNAMIC_BACKLOG_LITERAL = re.compile(
    r"(?i)(?:unknown|backlog)[^。；;\n]{0,60}\b\d+\b|\b\d+\b[^。；;\n]{0,60}(?:unknown|backlog)"
)


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
    if state.get("schema_version") != "k2-qimen-cognitive-reconstruction-v2":
        issues.append("state schema_version mismatch")
    if state.get("status") not in ALLOWED_STATUS:
        issues.append("invalid state status")
    if state.get("mode") != "COGNITIVE_RECONSTRUCTION":
        issues.append("mode must be COGNITIVE_RECONSTRUCTION")
    if state.get("active_framework") != "SCRM-v0.2":
        issues.append("active_framework must be SCRM-v0.2")
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
    narrative_fields = ("historical_pattern", "why_wrong", "current_control", "residual_risk", "next_test")
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
        for field in narrative_fields:
            value = row.get(field)
            if not isinstance(value, str) or len(value.strip()) < 10:
                issues.append(f"{bid}: weak/missing {field}")
                continue
            if DYNAMIC_BACKLOG_LITERAL.search(value):
                issues.append(f"{bid}: dynamic UNKNOWN/backlog state must remain machine-derived, not hard-coded in narrative")
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


def _closed_object_contract(props: dict, field: str, required_fields: set[str], issues: list[str]):
    obj = props.get(field, {})
    if obj.get("type") != "object" or obj.get("additionalProperties") is not False:
        issues.append(f"scenario {field} must be a closed object")
        return {}
    required = obj.get("required")
    if not isinstance(required, list) or set(required) != required_fields:
        issues.append(f"scenario {field} required-field contract drift")
    return obj.get("properties") if isinstance(obj.get("properties"), dict) else {}


def validate_scenario_schema(schema: dict):
    issues = []
    required = schema.get("required")
    if not isinstance(required, list) or set(required) != REQUIRED_SCENARIO_FIELDS:
        issues.append("scenario schema required-field contract drift")
    props = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    for field in REQUIRED_SCENARIO_FIELDS:
        if field not in props:
            issues.append(f"scenario schema missing property {field}")
    if props.get("schema_version", {}).get("const") != "qimen-scrm-case-v0.2":
        issues.append("scenario schema must freeze qimen-scrm-case-v0.2")
    if props.get("empirical_credit", {}).get("const") != "NONE":
        issues.append("scenario case must not auto-grant empirical credit")
    comp = props.get("competing_explanations", {})
    if comp.get("minItems", 0) < 2:
        issues.append("scenario contract requires at least two competing explanations")
    if props.get("counterfactual_checks", {}).get("minItems", 0) < 1:
        issues.append("scenario contract requires counterfactual checks")
    if props.get("sensitivity_checks", {}).get("minItems", 0) < 1:
        issues.append("scenario contract requires sensitivity checks")

    tie = props.get("decision_tie_break_policy", {})
    if tie.get("type") != "object" or tie.get("additionalProperties") is not False:
        issues.append("scenario tie-break policy must be a closed object")
    tie_required = tie.get("required")
    if not isinstance(tie_required, list) or set(tie_required) != REQUIRED_TIE_BREAK_FIELDS:
        issues.append("scenario tie-break required-field contract drift")
    tie_props = tie.get("properties") if isinstance(tie.get("properties"), dict) else {}
    if set(tie_props.get("freeze_status", {}).get("enum", [])) != REQUIRED_TIE_BREAK_STATUS:
        issues.append("scenario tie-break freeze_status enum drift")
    if tie_props.get("candidate_outputs", {}).get("type") != "array":
        issues.append("scenario tie-break candidate_outputs must be array")
    if not isinstance(tie.get("allOf"), list) or len(tie.get("allOf")) < 2:
        issues.append("scenario tie-break must fail closed for multi-output selection")

    info_props = _closed_object_contract(props, "information_order", REQUIRED_INFORMATION_ORDER_FIELDS, issues)
    if set(info_props.get("world_model_freeze_status", {}).get("enum", [])) != {"FROZEN", "UNRESOLVED"}:
        issues.append("information-order world model freeze enum drift")
    if info_props.get("symbolic_inputs_hidden_until_world_freeze", {}).get("type") != "boolean":
        issues.append("information-order symbolic reveal field must be boolean")
    if info_props.get("outcome_known_at_freeze", {}).get("type") != "boolean":
        issues.append("information-order outcome-known field must be boolean")

    parity_props = _closed_object_contract(props, "comparator_parity", REQUIRED_COMPARATOR_PARITY_FIELDS, issues)
    if parity_props.get("shared_reality_information", {}).get("const") is not True:
        issues.append("comparator parity requires shared reality information")
    if parity_props.get("symbolic_increment_isolated", {}).get("const") is not True:
        issues.append("comparator parity must isolate symbolic increment")

    model_props = _closed_object_contract(props, "model_freeze", REQUIRED_MODEL_FREEZE_FIELDS, issues)
    if model_props.get("scrm_version", {}).get("const") != "SCRM-v0.2":
        issues.append("model freeze must pin SCRM-v0.2")
    if model_props.get("method_variants", {}).get("minItems", 0) < 1:
        issues.append("model freeze requires at least one explicit method variant")

    abstain_props = _closed_object_contract(props, "abstention_policy", REQUIRED_ABSTENTION_FIELDS, issues)
    if abstain_props.get("coverage_accounting", {}).get("const") is not True:
        issues.append("abstention coverage must be accounted rather than treated as free escape")
    if abstain_props.get("trigger_conditions", {}).get("minItems", 0) < 1:
        issues.append("abstention policy requires predeclared trigger conditions")

    root_all_of = schema.get("allOf")
    if not isinstance(root_all_of, list) or len(root_all_of) < 1:
        issues.append("frozen cases must enforce clean pre-symbolic information order and freeze contracts")
    return issues


def validate_docs(charter: str, model: str):
    issues = []
    for needle in (
        "理论—边界—验证",
        "full_corpus_mastery_claim = false",
        "SCRM-v0.2",
        "WORLD MODEL BEFORE SYMBOLS",
        "COMPARATOR INFORMATION PARITY",
        "MODEL VERSION FREEZE",
        "ABSTENTION IS ACCOUNTED",
        "DYNAMIC STATE = MACHINE_DERIVED",
        "认知重构不等于理论已验证",
    ):
        if needle not in charter:
            issues.append(f"deep-retreat charter missing invariant: {needle}")
    for needle in (
        "CANDIDATE_UNTESTED",
        "Empirical Credit：`NONE`",
        "Scenario State Graph",
        "Competing Explanations",
        "Counterfactual Stress Test",
        "Sensitivity Analysis",
        "WORLD MODEL BEFORE SYMBOLS",
        "COMPARATOR INFORMATION PARITY",
        "ABSTENTION IS ACCOUNTED",
        "MODEL VERSION FREEZE",
        "SCRM-H9",
    ):
        if needle not in model:
            issues.append(f"SCRM v0.2 model missing invariant: {needle}")
    return issues


def validate(repo: Path = ROOT):
    k = repo / "knowledge"
    required_paths = [
        k / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json",
        k / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl",
        k / "K2_QIMEN_DEEP_RETREAT_V12.md",
        k / "K2_QIMEN_SCRM_V02.md",
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
    charter = (k / "K2_QIMEN_DEEP_RETREAT_V12.md").read_text(encoding="utf-8")
    model = (k / "K2_QIMEN_SCRM_V02.md").read_text(encoding="utf-8")

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
        for issue in issues[:60]:
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
