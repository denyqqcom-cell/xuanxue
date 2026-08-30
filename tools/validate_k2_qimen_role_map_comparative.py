#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
V01 = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"
V02 = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json"
V03 = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V03.json"
AUDIT = K / "K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json"
REPIN = K / "K2_QIMEN_P2_ROLE_MAP_PLAN_REPIN_V01.json"
HISTORY = K / "K2_QIMEN_P2_ROLE_MAP_PLAN_HISTORY.jsonl"
EVIDENCE = K / "K2_EVIDENCE_WAVE1.jsonl"
PLANS = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES = K / "K2_PROSPECTIVE_BATCHES.jsonl"
HYPOTHESES = K / "K2_QIMEN_PROJECT_HYPOTHESES.jsonl"
WORKFLOWS = (
    ROOT / ".github" / "workflows" / "knowledge-engine-ci.yml",
    ROOT / ".github" / "workflows" / "k2-qimen-cognitive-reconstruction.yml",
)


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc


def load_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            raise ValidationError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
        require(isinstance(row, dict), f"JSONL row must be object: {path}:{line_no}")
        rows.append(row)
    return rows


def require_true(obj: dict, fields, prefix: str):
    for field in fields:
        require(obj.get(field) is True, f"{prefix}.{field} must remain true")


def required_v02_freeze_fields(p: dict):
    fields = p.get("future_batch_freeze_required")
    require(isinstance(fields, list) and fields, "V02 future_batch_freeze_required missing")
    require(len(fields) == len(set(fields)), "V02 future freeze fields contain duplicates")
    required = {
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
    }
    require(required.issubset(set(fields)), f"V02 future freeze fields missing: {sorted(required-set(fields))}")
    return set(fields)


def validate_v02_protocol(p: dict):
    require(p.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V02", "V02 protocol_id drift")
    require(p.get("version") == "0.2", "V02 version drift")
    require(p.get("status") == "ADVERSARIAL_HARDENED", "V02 historical status drift")
    require(p.get("empirical_credit") == "NONE", "V02 cannot gain empirical credit")
    require(p.get("claim_extraction") == "BLOCKED", "V02 claim extraction must remain blocked")
    for key in ("batch", "freeze", "outcome"):
        require(p.get(key) == "NONE", f"V02 {key} must remain NONE")
    require(p.get("batch_ready") is False, "V02 historical state was not Batch-ready")
    require(p.get("batch_gate") == "BLOCKED_PENDING_PLAN_REPIN", "V02 historical Batch gate drift")
    require(p.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01", "V02 must preserve V01 lineage")

    h = p.get("hypothesis", {})
    require(h.get("hypothesis_id") == "QRM-H1", "V02 hypothesis drift")
    require(h.get("plan_id") == "K2PV-QRM-001", "V02 must preserve historical plan identity")
    require(h.get("status") == "UNTESTED", "V02 QRM-H1 must remain untested")

    boundary = p.get("mapping_input_boundary", {})
    require(boundary.get("mapping_before_plate_value_access") is True, "mapping must precede plate values")
    require(boundary.get("plate_value_access_before_mapping") is False, "plate values may not precede mapping")
    forbidden = set(boundary.get("forbidden_before_mapping_freeze", []))
    for item in (
        "current_plate_symbol_values", "current_plate_strength_or_auspiciousness", "prediction",
        "outcome", "feedback", "unregistered_external_omen", "lane_peer_intermediate_output",
    ):
        require(item in forbidden, f"V02 forbidden mapping input missing: {item}")

    shared = set(p.get("shared_controls", []))
    for item in (
        "reality_anchor", "scenario_graph", "observation_cutoff", "engine_commit", "plate_identity",
        "source_role_catalog", "eligible_rule_pool", "world_variable_manifest", "symbol_vocabulary",
        "feature_extraction_manifest", "prediction_schema", "confidence_scale", "outcome_definition",
        "scoring_rule", "paired_abstention_policy",
    ):
        require(item in shared, f"V02 shared control missing: {item}")

    lanes = p.get("lanes", [])
    require(len(lanes) == 3, "V02 requires exactly three lanes")
    by_id = {x.get("lane_id"): x for x in lanes}
    require(set(by_id) == {"P2-A", "P2-A_PRIME", "P2-B"}, "V02 lane identities drifted")
    a, bridge, b = by_id["P2-A"], by_id["P2-A_PRIME"], by_id["P2-B"]
    fixed = ["奇仪", "八门", "八神", "九星"]
    require(a.get("model_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "V02 comparator identity drift")
    require(a.get("preserve_qm_src_0003_domain_roles") is True, "V02 comparator became a strawman")
    require(a.get("layer_priority") == fixed and a.get("layer_priority_policy") == "FIXED_GLOBAL", "V02 comparator priority drift")
    require(bridge.get("model_name") == "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "V02 bridge identity drift")
    require(bridge.get("bridge_ablation_required") is True, "V02 bridge ablation must remain mandatory")
    require(bridge.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "V02 bridge role policy drift")
    require(bridge.get("layer_priority") == fixed, "V02 bridge fixed priority drift")
    require(b.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "V02 candidate identity drift")
    require(b.get("role_binding_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "V02 candidate role policy drift")
    require(b.get("layer_priority_policy") == "QUESTION_TOPOLOGY_CONDITIONED", "V02 candidate priority policy drift")
    require(all(x.get("mapping_must_precede_plate_values") is True for x in lanes), "all V02 lanes must map before plate values")

    estimand = p.get("estimand_lock", {})
    require(estimand.get("P2-C1") == {
        "candidate": "P2-A_PRIME", "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_POLICY", "all_other_dimensions_equal": True,
    }, "P2-C1 single-difference lock drift")
    require(estimand.get("P2-C2") == {
        "candidate": "P2-B", "comparator": "P2-A_PRIME",
        "only_allowed_difference": "LAYER_PRIORITY_POLICY", "all_other_dimensions_equal": True,
    }, "P2-C2 single-difference lock drift")
    require(estimand.get("P2-C3") == {
        "candidate": "P2-B", "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_PLUS_LAYER_PRIORITY", "component_credit_forbidden": True,
    }, "P2-C3 bundle lock drift")

    parity = p.get("representation_parity", {})
    require_true(parity, (
        "world_variable_manifest_shared", "lane_specific_world_variable_addition_forbidden",
        "symbol_vocabulary_shared", "feature_extraction_manifest_shared", "eligible_rule_pool_shared",
        "prediction_schema_shared", "prediction_cardinality_shared", "confidence_scale_shared",
        "output_granularity_shared",
    ), "representation_parity")
    layer = p.get("layer_priority_semantics", {})
    require_true(layer, (
        "all_four_layers_visible_to_all_lanes", "same_feature_extraction_depth",
        "priority_may_not_change_rule_eligibility", "priority_may_not_enable_early_stop",
        "priority_is_aggregation_policy_only", "priority_output_frozen_before_plate_values",
    ), "layer_priority_semantics")
    budget = p.get("complexity_budget", {})
    require_true(budget, (
        "role_multiplicity_budget_equal", "max_competing_mapping_count_frozen_per_case",
        "reasoning_branch_budget_equal", "rule_trace_budget_equal", "interpreter_information_budget_equal",
        "tool_access_budget_equal", "new_role_outside_shared_catalog_forbidden", "candidate_extra_rules_forbidden",
    ), "complexity_budget")
    blind = p.get("blinding_and_isolation", {})
    require_true(blind, (
        "neutral_lane_labels_for_interpreters", "hypothesis_identity_hidden_from_interpreters",
        "lane_order_randomized_from_frozen_seed", "no_cross_lane_intermediate_output",
        "all_predictions_frozen_before_unblinding", "same_raw_input_manifest_for_all_lanes",
    ), "blinding_and_isolation")
    denom = p.get("denominator_and_abstention", {})
    require_true(denom, (
        "case_inclusion_frozen_before_lane_execution", "lane_specific_case_exclusion_forbidden",
        "abstain_never_silently_drops_case", "abstention_scoring_policy_must_be_frozen",
        "coverage_penalized_metric_required", "technical_unevaluable_reason_required",
        "shared_technical_failure_applies_symmetrically",
    ), "denominator_and_abstention")
    det = p.get("determinism_controls", {})
    require_true(det, (
        "mapping_generators_versioned_and_hashed", "layer_priority_generator_versioned_and_hashed",
        "nondeterminism_seed_frozen", "pre_batch_reproducibility_fixture_required",
        "same_input_same_lane_must_reproduce_exact_map",
    ), "determinism_controls")

    alignment = p.get("plan_alignment", {})
    require(alignment.get("current_plan_id") == "K2PV-QRM-001", "V02 must preserve pre-repin plan identity")
    require(alignment.get("status") == "REPIN_REQUIRED", "V02 historical repin requirement erased")
    require(alignment.get("batch_creation_allowed") is False, "V02 historical Batch creation must remain forbidden")
    return required_v02_freeze_fields(p)


def validate_audit_object(a: dict):
    require(a.get("audit_id") == "K2-QIMEN-P2-ROLE-MAP-ADVERSARIAL-AUDIT-V01", "audit id drift")
    require(a.get("audit_target") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01", "audit target drift")
    require(a.get("audit_target_plan") == "K2PV-QRM-001", "audit target plan drift")
    require(a.get("audit_stage") == "PRE_BATCH_PRE_FREEZE_PRE_OUTCOME", "audit stage drift")
    require(a.get("audit_result") == "V01_NOT_BATCH_SAFE", "V01 unsafe verdict erased")
    require(a.get("prior_status_reassessment") == "DESIGN_READY_WAS_PREMATURE", "self-correction verdict erased")
    require(a.get("empirical_credit") == "NONE", "audit cannot create empirical credit")
    require(a.get("batch_ready") is False, "audit cannot become Batch-ready")
    findings = {x.get("finding_id"): x for x in a.get("findings", [])}
    require(set(findings) == {f"P2-AUD-{i:03d}" for i in range(1, 13)}, "audit finding family drift")
    for i in range(1, 12):
        require(findings[f"P2-AUD-{i:03d}"].get("status") == "CLOSED_IN_V02", f"P2-AUD-{i:03d} remediation drift")
    require(findings["P2-AUD-012"].get("status") == "OPEN_BLOCKER", "historical audit must preserve plan-repin blocker")


def validate_repin_object(r: dict, required_fields: set):
    require(r.get("repin_id") == "K2-QIMEN-P2-ROLE-MAP-PLAN-REPIN-V01", "repin id drift")
    require(r.get("stage") == "PRE_BATCH_PRE_FREEZE_PRE_OUTCOME", "repin stage drift")
    require(r.get("trigger_finding") == "P2-AUD-012", "repin trigger drift")
    require(r.get("from_plan_id") == "K2PV-QRM-001" and r.get("to_plan_id") == "K2PV-QRM-002", "repin plan lineage drift")
    require(r.get("from_hypothesis_origin_key") == "P2-ROLE-MAP-v0.1", "repin old origin drift")
    require(r.get("to_hypothesis_origin_key") == "P2-ROLE-MAP-v0.2", "repin new origin drift")
    require(r.get("all_v02_future_freeze_fields_bound") is True, "repin field-binding claim missing")
    require(required_fields.issubset(set(r.get("required_freeze_fields", []))), "repin artifact does not carry all V02 fields")
    require(r.get("old_plan_removed_from_active_registry") is True, "old active-plan removal not recorded")
    require(r.get("old_plan_preserved") is True, "old plan preservation not recorded")
    require(r.get("batch_ready") is False, "repin cannot make Batch ready")
    require(r.get("batch_gate") == "BLOCKED_PENDING_POST_REPIN_AUDIT", "repin must keep post-audit gate")
    require(r.get("post_repin_audit_status") == "PENDING", "repin must not self-approve post audit")
    require(r.get("empirical_credit") == "NONE", "repin cannot create empirical credit")
    for key in ("batch", "freeze", "outcome"):
        require(r.get(key) == "NONE", f"repin {key} must remain NONE")


def validate_history_row(h: dict):
    require(h.get("history_id") == "K2-QRM-PLAN-HIST-001", "plan history id drift")
    require(h.get("plan_id") == "K2PV-QRM-001" and h.get("hypothesis_id") == "QRM-H1", "plan history identity drift")
    require(h.get("status") == "SUPERSEDED_PRE_BATCH", "old plan history status drift")
    require(h.get("retired_registry_blob_sha") == "c67e906f18dbbbff601174fcb0406a67a61e6076", "old registry blob identity drift")
    require(h.get("retired_at_parent_commit") == "2f578f597bb9ad8faed28d2179270dd819c8883b", "old-plan parent commit drift")
    require(h.get("superseding_plan_id") == "K2PV-QRM-002", "history superseding plan drift")
    require(h.get("retirement_trigger") == "P2-AUD-012", "history trigger drift")
    require(h.get("batch_count_at_retirement") == 0, "old plan had unexpected Batch")
    require(h.get("freeze_count_at_retirement") == 0, "old plan had unexpected Freeze")
    require(h.get("outcome_count_at_retirement") == 0, "old plan had unexpected Outcome")
    require(h.get("empirical_credit_at_retirement") == "NONE", "old plan history empirical credit drift")


def validate_v03_protocol(v: dict, required_fields: set):
    require(v.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V03", "V03 protocol id drift")
    require(v.get("version") == "0.3", "V03 version drift")
    require(v.get("status") == "PLAN_REPINNED_REAUDIT_REQUIRED", "V03 state drift")
    require(v.get("empirical_credit") == "NONE", "V03 cannot create empirical credit")
    require(v.get("claim_extraction") == "BLOCKED", "V03 claim extraction must remain blocked")
    for key in ("batch", "freeze", "outcome"):
        require(v.get(key) == "NONE", f"V03 {key} must remain NONE")
    require(v.get("batch_ready") is False, "V03 may not be Batch-ready")
    require(v.get("batch_gate") == "BLOCKED_PENDING_POST_REPIN_AUDIT", "V03 Batch gate drift")
    require(v.get("batch_creation_allowed") is False, "V03 Batch creation must remain forbidden")
    require(v.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V02", "V03 lineage drift")
    require(v.get("active_plan_id") == "K2PV-QRM-002" and v.get("retired_plan_id") == "K2PV-QRM-001", "V03 plan identities drift")
    require(v.get("hypothesis_id") == "QRM-H1", "V03 hypothesis drift")
    require(v.get("hypothesis_origin_key") == "P2-ROLE-MAP-v0.2", "V03 hypothesis origin drift")
    require(required_fields.issubset(set(v.get("required_plan_freeze_fields", []))), "V03 required plan fields incomplete")
    alignment = v.get("plan_alignment", {})
    require(alignment.get("status") == "REPINNED_TO_V02_FIELDS", "V03 plan alignment drift")
    require(alignment.get("active_plan_id") == "K2PV-QRM-002", "V03 alignment plan drift")
    require_true(alignment, ("old_plan_absent_from_active_registry", "old_plan_preserved_in_history", "all_v02_future_freeze_fields_bound"), "V03.plan_alignment")
    audit = v.get("post_repin_audit", {})
    require(audit.get("required") is True and audit.get("status") == "PENDING", "V03 post-repin audit must remain pending")
    require(len(audit.get("must_verify", [])) >= 5, "V03 post-repin audit scope too small")


def validate_repository(root: Path = ROOT):
    for path in (V01, V02, V03, AUDIT, REPIN, HISTORY, PLANS, HYPOTHESES):
        require(path.exists(), f"missing P2 artifact: {path.relative_to(root)}")

    v02 = load_json(V02)
    required_fields = validate_v02_protocol(v02)
    validate_audit_object(load_json(AUDIT))
    validate_repin_object(load_json(REPIN), required_fields)
    validate_v03_protocol(load_json(V03), required_fields)

    history_rows = load_jsonl(HISTORY)
    require(len(history_rows) == 1, "P2 plan history currently expects exactly one retired plan")
    validate_history_row(history_rows[0])

    evidence = {x.get("evidence_id"): x for x in load_jsonl(EVIDENCE)}
    for anchor in v02.get("source_basis", []):
        row = evidence.get(anchor.get("evidence_id"))
        require(row is not None, f"source anchor missing: {anchor.get('evidence_id')}")
        require(row.get("source_id") == anchor.get("source_id"), f"source anchor identity mismatch: {anchor.get('evidence_id')}")
        require(row.get("review_status") == "REVIEWED", f"source anchor not reviewed: {anchor.get('evidence_id')}")

    plans = [x for x in load_jsonl(PLANS) if x.get("hypothesis_id") == "QRM-H1"]
    require(len(plans) == 1, "QRM-H1 must have exactly one active prospective plan")
    plan = plans[0]
    require(plan.get("plan_id") == "K2PV-QRM-002", "active QRM plan was not repinned")
    require(plan.get("hypothesis_origin_type") == "PROJECT_GENERATED", "active QRM plan origin type drift")
    require(plan.get("hypothesis_origin_key") == "P2-ROLE-MAP-v0.2", "active QRM plan origin key drift")
    require(plan.get("hypothesis_origin_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.md#QRM-H1", "active QRM plan origin ref drift")
    require(plan.get("model_name") == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "active QRM candidate drift")
    require(plan.get("comparator_name") == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "active QRM comparator drift")
    require(plan.get("status") == "DESIGN_READY", "active QRM plan must remain DESIGN_READY at plan-schema layer")
    require(plan.get("empirical_credit") == "NONE", "active QRM plan cannot carry empirical credit")
    plan_fields = set(plan.get("freeze_required_fields", []))
    require(required_fields.issubset(plan_fields), f"repinned plan missing V02 freeze fields: {sorted(required_fields-plan_fields)}")
    require("K2PV-QRM-001" not in {x.get("plan_id") for x in load_jsonl(PLANS)}, "retired plan remains active")

    hypotheses = {x.get("hypothesis_id"): x for x in load_jsonl(HYPOTHESES)}
    h = hypotheses.get("QRM-H1")
    require(h is not None, "QRM-H1 hypothesis row missing")
    require(h.get("origin_type") == "PROJECT_GENERATED", "QRM-H1 origin type drift")
    require(h.get("origin_key") == "P2-ROLE-MAP-v0.2", "QRM-H1 origin key not repinned")
    require(h.get("origin_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.md#QRM-H1", "QRM-H1 origin ref not repinned")
    require(h.get("status") == "UNTESTED", "QRM-H1 must remain UNTESTED")
    require(h.get("empirical_credit") == "NONE", "QRM-H1 empirical credit must remain NONE")
    require(h.get("baseline_required") is True, "QRM-H1 baseline remains mandatory")

    for batch in load_jsonl(BATCHES):
        require(batch.get("plan_id") not in {"K2PV-QRM-001", "K2PV-QRM-002"}, "P2 Batch created before post-repin audit")

    for workflow in WORKFLOWS:
        text = workflow.read_text(encoding="utf-8")
        require("tools/test_k2_qimen_role_map_comparative.py" in text, f"P2 negative tests missing from {workflow.name}")
        require("tools/validate_k2_qimen_role_map_comparative.py" in text, f"P2 validator missing from {workflow.name}")

    print("k2-qimen-role-map-comparative: PASS (V02 hardened; K2PV-QRM-002 active; post-repin audit still required)")


def main():
    try:
        validate_repository(ROOT)
    except ValidationError as exc:
        raise SystemExit(f"k2-qimen-role-map-comparative: FAIL: {exc}")


if __name__ == "__main__":
    main()
