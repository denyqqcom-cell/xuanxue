#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_V01 = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json"
AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json"
EVIDENCE = ROOT / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl"
PLANS = ROOT / "knowledge" / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES = ROOT / "knowledge" / "K2_PROSPECTIVE_BATCHES.jsonl"
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
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL {path}:{line_no}: {exc}")
    return rows


def require_true_fields(obj: dict, fields, prefix: str):
    for field in fields:
        require(obj.get(field) is True, f"{prefix}.{field} must remain true")


def validate_protocol_object(p: dict):
    require(p.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V02", "protocol_id drift")
    require(p.get("version") == "0.2", "version drift")
    require(p.get("status") == "ADVERSARIAL_HARDENED", "protocol must remain adversarial-hardened")
    require(p.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(p.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")
    for key in ("batch", "freeze", "outcome"):
        require(p.get(key) == "NONE", f"{key} must remain NONE")
    require(p.get("batch_ready") is False, "V02 may not become batch-ready before plan repin")
    require(p.get("batch_gate") == "BLOCKED_PENDING_PLAN_REPIN", "batch gate must remain blocked")
    require(p.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01", "V01 historical identity lost")
    require(p.get("adversarial_audit_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json", "audit ref drift")

    h = p.get("hypothesis", {})
    require(h.get("hypothesis_id") == "QRM-H1", "QRM-H1 identity drift")
    require(h.get("plan_id") == "K2PV-QRM-001", "current plan identity drift")
    require(h.get("status") == "UNTESTED", "QRM-H1 must remain UNTESTED")

    boundary = p.get("mapping_input_boundary", {})
    require(boundary.get("mapping_before_plate_value_access") is True, "mapping must freeze before plate values")
    require(boundary.get("plate_value_access_before_mapping") is False, "plate values may not precede mapping")
    forbidden = set(boundary.get("forbidden_before_mapping_freeze", []))
    for item in (
        "current_plate_symbol_values", "current_plate_strength_or_auspiciousness", "prediction",
        "outcome", "feedback", "unregistered_external_omen", "lane_peer_intermediate_output",
    ):
        require(item in forbidden, f"missing forbidden mapping input: {item}")

    controls = set(p.get("shared_controls", []))
    for item in (
        "reality_anchor", "scenario_graph", "observation_cutoff", "engine_commit", "plate_identity",
        "source_role_catalog", "eligible_rule_pool", "world_variable_manifest", "symbol_vocabulary",
        "feature_extraction_manifest", "prediction_schema", "confidence_scale", "outcome_definition",
        "scoring_rule", "paired_abstention_policy",
    ):
        require(item in controls, f"missing shared control: {item}")

    lanes = p.get("lanes", [])
    require(len(lanes) == 3, "exactly three lanes are required")
    by_id = {x.get("lane_id"): x for x in lanes}
    require(set(by_id) == {"P2-A", "P2-A_PRIME", "P2-B"}, "lane identity drift")
    a, bridge, b = by_id["P2-A"], by_id["P2-A_PRIME"], by_id["P2-B"]
    expected_priority = ["奇仪", "八门", "八神", "九星"]
    require(a.get("model_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "comparator identity drift")
    require(a.get("preserve_qm_src_0003_domain_roles") is True, "source-faithful comparator guard missing")
    require(a.get("source_role_catalog_required") is True, "comparator must retain source role catalog")
    require(a.get("layer_priority") == expected_priority, "global priority anchor drift")
    require(a.get("layer_priority_policy") == "FIXED_GLOBAL", "comparator priority drift")
    require(bridge.get("model_name") == "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "bridge identity drift")
    require(bridge.get("bridge_ablation_required") is True, "bridge ablation may not be removed")
    require(bridge.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "bridge role policy drift")
    require(bridge.get("layer_priority") == expected_priority, "bridge priority drift")
    require(b.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "candidate identity drift")
    require(b.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "candidate role policy drift")
    require(b.get("layer_priority_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "candidate priority policy drift")
    require(all(x.get("mapping_must_precede_plate_values") is True for x in lanes), "all lanes must freeze mapping before plate values")

    estimand = p.get("estimand_lock", {})
    require(set(estimand) == {"P2-C1", "P2-C2", "P2-C3"}, "estimand lock family drift")
    require(estimand["P2-C1"] == {
        "candidate": "P2-A_PRIME", "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_POLICY", "all_other_dimensions_equal": True,
    }, "P2-C1 single-difference lock drift")
    require(estimand["P2-C2"] == {
        "candidate": "P2-B", "comparator": "P2-A_PRIME",
        "only_allowed_difference": "LAYER_PRIORITY_POLICY", "all_other_dimensions_equal": True,
    }, "P2-C2 single-difference lock drift")
    require(estimand["P2-C3"] == {
        "candidate": "P2-B", "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_PLUS_LAYER_PRIORITY", "component_credit_forbidden": True,
    }, "P2-C3 bundle lock drift")

    contrasts = {x.get("contrast_id"): x for x in p.get("attribution_contrasts", [])}
    require(set(contrasts) == {"P2-C1", "P2-C2", "P2-C3"}, "attribution contrast family drift")
    require((contrasts["P2-C1"].get("candidate"), contrasts["P2-C1"].get("comparator"), contrasts["P2-C1"].get("credit_scope")) == ("P2-A_PRIME", "P2-A", "TOPOLOGY_ROLE_BINDING_ONLY"), "P2-C1 attribution drift")
    require((contrasts["P2-C2"].get("candidate"), contrasts["P2-C2"].get("comparator"), contrasts["P2-C2"].get("credit_scope")) == ("P2-B", "P2-A_PRIME", "TOPOLOGY_CONDITIONED_LAYER_PRIORITY_ONLY"), "P2-C2 attribution drift")
    require((contrasts["P2-C3"].get("candidate"), contrasts["P2-C3"].get("comparator"), contrasts["P2-C3"].get("credit_scope")) == ("P2-B", "P2-A", "FULL_BUNDLE_ONLY_NOT_COMPONENT_ATTRIBUTION"), "P2-C3 component-credit laundering")

    parity = p.get("representation_parity", {})
    require_true_fields(parity, (
        "world_variable_manifest_shared", "lane_specific_world_variable_addition_forbidden",
        "symbol_vocabulary_shared", "feature_extraction_manifest_shared", "eligible_rule_pool_shared",
        "prediction_schema_shared", "prediction_cardinality_shared", "confidence_scale_shared",
        "output_granularity_shared",
    ), "representation_parity")

    layer = p.get("layer_priority_semantics", {})
    require_true_fields(layer, (
        "all_four_layers_visible_to_all_lanes", "same_feature_extraction_depth",
        "priority_may_not_change_rule_eligibility", "priority_may_not_enable_early_stop",
        "priority_is_aggregation_policy_only", "priority_output_frozen_before_plate_values",
    ), "layer_priority_semantics")

    budget = p.get("complexity_budget", {})
    require_true_fields(budget, (
        "role_multiplicity_budget_equal", "max_competing_mapping_count_frozen_per_case",
        "reasoning_branch_budget_equal", "rule_trace_budget_equal",
        "interpreter_information_budget_equal", "tool_access_budget_equal",
        "new_role_outside_shared_catalog_forbidden", "candidate_extra_rules_forbidden",
    ), "complexity_budget")
    metrics = set(budget.get("complexity_metrics_required", []))
    for item in ("bound_role_count", "competing_mapping_count", "active_rule_count", "feature_count", "reasoning_branch_count", "rule_trace_count"):
        require(item in metrics, f"missing complexity metric: {item}")

    blind = p.get("blinding_and_isolation", {})
    require_true_fields(blind, (
        "neutral_lane_labels_for_interpreters", "hypothesis_identity_hidden_from_interpreters",
        "lane_order_randomized_from_frozen_seed", "no_cross_lane_intermediate_output",
        "all_predictions_frozen_before_unblinding", "same_raw_input_manifest_for_all_lanes",
    ), "blinding_and_isolation")

    denom = p.get("denominator_and_abstention", {})
    require_true_fields(denom, (
        "case_inclusion_frozen_before_lane_execution", "lane_specific_case_exclusion_forbidden",
        "abstain_never_silently_drops_case", "abstention_scoring_policy_must_be_frozen",
        "coverage_penalized_metric_required", "technical_unevaluable_reason_required",
        "shared_technical_failure_applies_symmetrically",
    ), "denominator_and_abstention")

    det = p.get("determinism_controls", {})
    require_true_fields(det, (
        "mapping_generators_versioned_and_hashed", "layer_priority_generator_versioned_and_hashed",
        "nondeterminism_seed_frozen", "pre_batch_reproducibility_fixture_required",
        "same_input_same_lane_must_reproduce_exact_map",
    ), "determinism_controls")

    abstain = p.get("abstention_policy", {})
    require(abstain.get("competing_mappings_must_be_preserved_or_abstain") is True, "competing mappings guard missing")
    require(abstain.get("post_outcome_mapping_selection_forbidden") is True, "post-outcome mapping selection must be forbidden")
    require(abstain.get("unevaluable_if_mapping_order_not_auditable") is True, "mapping-order audit failure must be UNEVALUABLE")

    alignment = p.get("plan_alignment", {})
    require(alignment.get("current_plan_id") == "K2PV-QRM-001", "plan alignment current id drift")
    require(alignment.get("current_plan_origin") == "P2-ROLE-MAP-v0.1", "plan alignment origin drift")
    require(alignment.get("status") == "REPIN_REQUIRED", "plan repin blocker may not be cleared in V02")
    require(alignment.get("batch_creation_allowed") is False, "Batch creation must remain forbidden")
    require("REP" in str(alignment.get("required_action_before_batch", "")).upper(), "repin action missing")

    future = set(p.get("future_batch_freeze_required", []))
    for item in (
        "source_role_catalog_hash", "comparator_mapping_generator", "bridge_mapping_generator",
        "candidate_mapping_generator", "topology_feature_manifest", "world_variable_manifest_hash",
        "symbol_vocabulary_hash", "feature_extraction_manifest_hash", "eligible_rule_pool_hash",
        "layer_priority_generator_hash", "prediction_schema_hash", "prediction_cardinality",
        "confidence_scale", "role_multiplicity_budget", "reasoning_branch_budget", "rule_trace_budget",
        "interpreter_information_budget", "tool_access_budget", "lane_blinding_protocol",
        "lane_order_seed", "cross_lane_isolation_policy", "primary_denominator_policy",
        "abstention_scoring_policy", "technical_unevaluable_policy", "reproducibility_fixture_hash",
        "nondeterminism_seed_policy", "interpreter_protocol", "primary_metric", "decision_threshold",
        "sampling_rule", "stopping_rule", "minimum_information_floor", "contamination_ledger_policy",
    ):
        require(item in future, f"future Batch freeze field missing: {item}")

    leak = set(p.get("leakage_controls", []))
    for item in (
        "source_faithful_comparator_no_strawman", "bridge_ablation_is_mandatory",
        "P2-C1_C2_C3_scored_separately", "combined_gain_cannot_be_laundered_into_component_credit",
        "shared_world_variable_symbol_feature_prediction_manifests",
        "priority_changes_aggregation_only_not_visibility_or_eligibility",
        "equal_complexity_information_tool_and_rule_trace_budgets",
        "neutral_lane_blinding_and_cross_lane_isolation",
        "no_lane_specific_case_exclusion_or_abstention_denominator_drop",
        "deterministic_hashed_generators_with_reproducibility_fixture",
        "post_feedback_role_layer_rule_path_changes_are_contamination_only",
        "failed_abstained_unevaluable_cases_are_retained",
    ):
        require(item in leak, f"leakage control missing: {item}")

    require(p.get("high_risk_policy") == "RESEARCH_ONLY", "high-risk policy must remain RESEARCH_ONLY")
    exclusions = set(p.get("high_risk_exclusions", []))
    require({"medical", "legal", "financial", "personal_safety", "major_relationship", "criminal_attribution"}.issubset(exclusions), "high-risk exclusions weakened")

    anchors = {x.get("evidence_id") for x in p.get("source_basis", [])}
    for evidence_id in (
        "K2E-W1-QM-0003-0065", "K2E-W1-QM-0003-0009", "K2E-W1-QM-0003-0063",
        "K2E-W1-QM-0003-0068", "K2E-W1-QM-0021-0239", "K2E-W1-QM-0021-0327",
        "K2E-W1-QM-0021-0330",
    ):
        require(evidence_id in anchors, f"source anchor missing from protocol: {evidence_id}")


def validate_audit_object(a: dict):
    require(a.get("audit_id") == "K2-QIMEN-P2-ROLE-MAP-ADVERSARIAL-AUDIT-V01", "audit_id drift")
    require(a.get("audit_target") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01", "audit target drift")
    require(a.get("audit_target_plan") == "K2PV-QRM-001", "audit plan drift")
    require(a.get("audit_stage") == "PRE_BATCH_PRE_FREEZE_PRE_OUTCOME", "audit stage drift")
    require(a.get("audit_result") == "V01_NOT_BATCH_SAFE", "V01 unsafe verdict may not be erased")
    require(a.get("prior_status_reassessment") == "DESIGN_READY_WAS_PREMATURE", "self-correction verdict missing")
    require(a.get("empirical_credit") == "NONE", "audit cannot create empirical credit")
    require(a.get("batch_ready") is False, "audit may not declare Batch ready")
    require(a.get("remediation_protocol") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V02", "remediation protocol drift")
    require(a.get("remediation_status") == "PROTOCOL_HARDENED_PLAN_REPIN_PENDING", "remediation status drift")
    for key in ("batch", "freeze", "outcome"):
        require(a.get(key) == "NONE", f"audit {key} must remain NONE")
    findings = {x.get("finding_id"): x for x in a.get("findings", [])}
    expected = {f"P2-AUD-{i:03d}" for i in range(1, 13)}
    require(set(findings) == expected, "audit finding family drift")
    for fid in sorted(expected - {"P2-AUD-012"}):
        require(findings[fid].get("status") == "CLOSED_IN_V02", f"{fid} protocol remediation lost")
    require(findings["P2-AUD-012"].get("status") == "OPEN_BLOCKER", "plan-repin blocker may not be silently closed")


def validate_repository(root: Path = ROOT):
    v01 = root / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"
    protocol_path = root / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json"
    audit_path = root / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json"
    require(v01.exists(), "historical P2 V01 protocol must be retained")
    require(protocol_path.exists(), "P2 V02 hardened protocol missing")
    require(audit_path.exists(), "P2 adversarial audit missing")

    p = json.loads(protocol_path.read_text(encoding="utf-8"))
    a = json.loads(audit_path.read_text(encoding="utf-8"))
    validate_protocol_object(p)
    validate_audit_object(a)

    evidence_rows = load_jsonl(root / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl")
    evidence = {row.get("evidence_id"): row for row in evidence_rows}
    for anchor in p["source_basis"]:
        row = evidence.get(anchor["evidence_id"])
        require(row is not None, f"source evidence not found: {anchor['evidence_id']}")
        require(row.get("source_id") == anchor["source_id"], f"source identity mismatch: {anchor['evidence_id']}")
        require(row.get("review_status") == "REVIEWED", f"source anchor not reviewed: {anchor['evidence_id']}")

    plans = {x.get("plan_id"): x for x in load_jsonl(root / "knowledge" / "K2_PROSPECTIVE_TEST_PLANS.jsonl")}
    plan = plans.get("K2PV-QRM-001")
    require(plan is not None, "current historical-shell plan K2PV-QRM-001 missing")
    require(plan.get("hypothesis_id") == "QRM-H1", "plan-hypothesis mismatch")
    require(plan.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "plan candidate mismatch")
    require(plan.get("comparator_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "plan comparator mismatch")
    require(plan.get("status") == "DESIGN_READY", "historical plan row unexpectedly changed")
    require(plan.get("empirical_credit") == "NONE", "plan empirical credit must remain NONE")
    plan_freeze = set(plan.get("freeze_required_fields", []))
    v02_freeze = set(p.get("future_batch_freeze_required", []))
    require(bool(v02_freeze - plan_freeze), "V02 should stay blocked until the plan is explicitly repinned")

    batches = load_jsonl(root / "knowledge" / "K2_PROSPECTIVE_BATCHES.jsonl")
    require(not any(row.get("plan_id") == "K2PV-QRM-001" for row in batches), "QRM Batch created before V02 plan repin")

    hypotheses = {x.get("hypothesis_id"): x for x in load_jsonl(root / "knowledge" / "K2_QIMEN_PROJECT_HYPOTHESES.jsonl")}
    h = hypotheses.get("QRM-H1")
    require(h is not None, "QRM-H1 hypothesis registry row missing")
    require(h.get("status") == "UNTESTED", "QRM-H1 must remain UNTESTED")
    require(h.get("empirical_credit") == "NONE", "QRM-H1 empirical credit must remain NONE")
    require(h.get("baseline_required") is True, "QRM-H1 baseline is mandatory")

    for workflow in (
        root / ".github" / "workflows" / "knowledge-engine-ci.yml",
        root / ".github" / "workflows" / "k2-qimen-cognitive-reconstruction.yml",
    ):
        text = workflow.read_text(encoding="utf-8")
        require("tools/test_k2_qimen_role_map_comparative.py" in text, f"P2 negative tests missing from {workflow.name}")
        require("tools/validate_k2_qimen_role_map_comparative.py" in text, f"P2 validator missing from {workflow.name}")

    print("k2-qimen-role-map-comparative: PASS (V01 downgraded; V02 hardened; plan repin blocker open)")


def main():
    try:
        validate_repository(ROOT)
    except (ValidationError, json.JSONDecodeError) as exc:
        raise SystemExit(f"k2-qimen-role-map-comparative: FAIL: {exc}")


if __name__ == "__main__":
    main()
