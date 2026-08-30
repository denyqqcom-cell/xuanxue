#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"
EVIDENCE = ROOT / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl"
PLANS = ROOT / "knowledge" / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
HYPOTHESES = ROOT / "knowledge" / "K2_QIMEN_PROJECT_HYPOTHESES.jsonl"
KNOWLEDGE_CI = ROOT / ".github" / "workflows" / "knowledge-engine-ci.yml"
COGNITIVE_CI = ROOT / ".github" / "workflows" / "k2-qimen-cognitive-reconstruction.yml"


class ValidationError(RuntimeError):
    pass


def fail(message: str):
    raise ValidationError(message)


def require(condition: bool, message: str):
    if not condition:
        fail(message)


def load_jsonl(path: Path):
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL {path}:{line_no}: {exc}")
    return rows


def validate_protocol_object(p: dict):
    require(p.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01", "protocol_id drift")
    require(p.get("version") == "0.1", "version drift")
    require(p.get("status") == "DESIGN_READY", "protocol must remain DESIGN_READY")
    require(p.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(p.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")
    for key in ("batch", "freeze", "outcome"):
        require(p.get(key) == "NONE", f"{key} must remain NONE before preregistration")

    h = p.get("hypothesis", {})
    require(h.get("hypothesis_id") == "QRM-H1", "QRM-H1 identity drift")
    require(h.get("plan_id") == "K2PV-QRM-001", "QRM plan identity drift")
    require(h.get("status") == "UNTESTED", "QRM-H1 must remain UNTESTED")

    boundary = p.get("mapping_input_boundary", {})
    require(boundary.get("mapping_before_plate_value_access") is True, "mapping must freeze before plate values")
    require(boundary.get("plate_value_access_before_mapping") is False, "plate values may not precede mapping")
    forbidden = set(boundary.get("forbidden_before_mapping_freeze", []))
    for item in ("current_plate_symbol_values", "current_plate_strength_or_auspiciousness", "prediction", "outcome", "feedback", "unregistered_external_omen"):
        require(item in forbidden, f"missing forbidden mapping input: {item}")

    controls = set(p.get("shared_controls", []))
    for item in ("reality_anchor", "scenario_graph", "observation_cutoff", "engine_commit", "plate_identity", "source_role_catalog", "eligible_rule_pool", "outcome_definition", "scoring_rule", "paired_abstention_policy"):
        require(item in controls, f"missing shared control: {item}")

    lanes = p.get("lanes", [])
    require(len(lanes) == 3, "exactly three lanes are required")
    by_id = {x.get("lane_id"): x for x in lanes}
    require(set(by_id) == {"P2-A", "P2-A_PRIME", "P2-B"}, "lane identity drift")
    a, bridge, b = by_id["P2-A"], by_id["P2-A_PRIME"], by_id["P2-B"]
    require(a.get("model_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "comparator identity drift")
    require(a.get("preserve_qm_src_0003_domain_roles") is True, "source-faithful comparator guard missing")
    require(a.get("source_role_catalog_required") is True, "comparator must retain source role catalog")
    expected_priority = ["奇仪", "八门", "八神", "九星"]
    require(a.get("layer_priority") == expected_priority, "global priority anchor drift")
    require(a.get("layer_priority_policy") == "FIXED_GLOBAL", "comparator priority must remain fixed-global")
    require(bridge.get("model_name") == "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "bridge identity drift")
    require(bridge.get("bridge_ablation_required") is True, "bridge ablation may not be removed")
    require(bridge.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "bridge must isolate topology role binding")
    require(bridge.get("layer_priority") == expected_priority, "bridge must retain fixed global priority")
    require(b.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "candidate identity drift")
    require(b.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "candidate role policy drift")
    require(b.get("layer_priority_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "candidate layer policy drift")
    require(all(x.get("mapping_must_precede_plate_values") is True for x in lanes), "all lanes must freeze mapping before plate values")

    contrasts = {x.get("contrast_id"): x for x in p.get("attribution_contrasts", [])}
    require(set(contrasts) == {"P2-C1", "P2-C2", "P2-C3"}, "attribution contrast family drift")
    require((contrasts["P2-C1"].get("candidate"), contrasts["P2-C1"].get("comparator"), contrasts["P2-C1"].get("credit_scope")) == ("P2-A_PRIME", "P2-A", "TOPOLOGY_ROLE_BINDING_ONLY"), "P2-C1 attribution drift")
    require((contrasts["P2-C2"].get("candidate"), contrasts["P2-C2"].get("comparator"), contrasts["P2-C2"].get("credit_scope")) == ("P2-B", "P2-A_PRIME", "TOPOLOGY_CONDITIONED_LAYER_PRIORITY_ONLY"), "P2-C2 attribution drift")
    require((contrasts["P2-C3"].get("candidate"), contrasts["P2-C3"].get("comparator"), contrasts["P2-C3"].get("credit_scope")) == ("P2-B", "P2-A", "FULL_BUNDLE_ONLY_NOT_COMPONENT_ATTRIBUTION"), "P2-C3 may not launder component credit")

    abstain = p.get("abstention_policy", {})
    require(abstain.get("competing_mappings_must_be_preserved_or_abstain") is True, "competing mappings guard missing")
    require(abstain.get("post_outcome_mapping_selection_forbidden") is True, "post-outcome mapping selection must be forbidden")
    require(abstain.get("unevaluable_if_mapping_order_not_auditable") is True, "mapping-order audit failure must be UNEVALUABLE")

    future = set(p.get("future_batch_freeze_required", []))
    for item in ("source_role_catalog_hash", "comparator_mapping_generator", "bridge_mapping_generator", "candidate_mapping_generator", "topology_feature_manifest", "interpreter_protocol", "primary_metric", "decision_threshold", "sampling_rule", "stopping_rule", "contamination_ledger_policy"):
        require(item in future, f"future Batch freeze field missing: {item}")

    leak = set(p.get("leakage_controls", []))
    for item in ("source_faithful_comparator_no_strawman", "bridge_ablation_is_mandatory", "P2-C1_C2_C3_scored_separately", "combined_gain_cannot_be_laundered_into_component_credit", "post_feedback_role_layer_rule_path_changes_are_contamination_only", "failed_abstained_unevaluable_cases_are_retained"):
        require(item in leak, f"leakage control missing: {item}")

    require(p.get("high_risk_policy") == "RESEARCH_ONLY", "high-risk policy must remain RESEARCH_ONLY")
    exclusions = set(p.get("high_risk_exclusions", []))
    require({"medical", "legal", "financial", "personal_safety", "major_relationship", "criminal_attribution"}.issubset(exclusions), "high-risk exclusions weakened")

    source_basis = p.get("source_basis", [])
    anchors = {x.get("evidence_id") for x in source_basis}
    for evidence_id in ("K2E-W1-QM-0003-0065", "K2E-W1-QM-0003-0009", "K2E-W1-QM-0003-0063", "K2E-W1-QM-0003-0068", "K2E-W1-QM-0021-0239", "K2E-W1-QM-0021-0327", "K2E-W1-QM-0021-0330"):
        require(evidence_id in anchors, f"source anchor missing from protocol: {evidence_id}")


def validate_repository(root: Path = ROOT):
    protocol_path = root / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"
    require(protocol_path.exists(), "P2 machine protocol missing")
    p = json.loads(protocol_path.read_text(encoding="utf-8"))
    validate_protocol_object(p)

    evidence_rows = load_jsonl(root / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl")
    evidence = {row.get("evidence_id"): row for row in evidence_rows}
    for anchor in p["source_basis"]:
        row = evidence.get(anchor["evidence_id"])
        require(row is not None, f"source evidence not found: {anchor['evidence_id']}")
        require(row.get("source_id") == anchor["source_id"], f"source identity mismatch: {anchor['evidence_id']}")
        require(row.get("review_status") == "REVIEWED", f"source anchor not reviewed: {anchor['evidence_id']}")

    plans = {x.get("plan_id"): x for x in load_jsonl(root / "knowledge" / "K2_PROSPECTIVE_TEST_PLANS.jsonl")}
    plan = plans.get("K2PV-QRM-001")
    require(plan is not None, "K2PV-QRM-001 missing")
    require(plan.get("hypothesis_id") == "QRM-H1", "plan-hypothesis mismatch")
    require(plan.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "plan candidate mismatch")
    require(plan.get("comparator_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "plan comparator mismatch")
    require(plan.get("status") == "DESIGN_READY", "plan must remain DESIGN_READY")
    require(plan.get("empirical_credit") == "NONE", "plan empirical credit must remain NONE")
    freeze_fields = set(plan.get("freeze_required_fields", []))
    for item in ("mapping_input_manifest", "mapping_before_plate_value_access", "plate_value_access_before_mapping", "comparator_role_map", "bridge_role_map", "candidate_role_map", "attribution_contrasts"):
        require(item in freeze_fields, f"plan freeze field missing: {item}")

    hypotheses = {x.get("hypothesis_id"): x for x in load_jsonl(root / "knowledge" / "K2_QIMEN_PROJECT_HYPOTHESES.jsonl")}
    h = hypotheses.get("QRM-H1")
    require(h is not None, "QRM-H1 hypothesis registry row missing")
    require(h.get("status") == "UNTESTED", "QRM-H1 must remain UNTESTED")
    require(h.get("empirical_credit") == "NONE", "QRM-H1 empirical credit must remain NONE")
    require(h.get("baseline_required") is True, "QRM-H1 baseline is mandatory")

    for workflow in (root / ".github" / "workflows" / "knowledge-engine-ci.yml", root / ".github" / "workflows" / "k2-qimen-cognitive-reconstruction.yml"):
        text = workflow.read_text(encoding="utf-8")
        require("tools/test_k2_qimen_role_map_comparative.py" in text, f"P2 negative tests missing from {workflow.name}")
        require("tools/validate_k2_qimen_role_map_comparative.py" in text, f"P2 validator missing from {workflow.name}")

    print("k2-qimen-role-map-comparative: PASS")


def main():
    try:
        validate_repository(ROOT)
    except (ValidationError, json.JSONDecodeError) as exc:
        raise SystemExit(f"k2-qimen-role-map-comparative: FAIL: {exc}")


if __name__ == "__main__":
    main()
