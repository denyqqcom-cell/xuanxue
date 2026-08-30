#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from validate_k2_qimen_role_map_comparative import (
    ValidationError,
    validate_audit_object,
    validate_protocol_object,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json"
AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json"


def mutate_lane(p, lane_id, key, value):
    for lane in p["lanes"]:
        if lane["lane_id"] == lane_id:
            lane[key] = value
            return
    raise AssertionError(lane_id)


def mutate_contrast(p, contrast_id, key, value):
    for contrast in p["attribution_contrasts"]:
        if contrast["contrast_id"] == contrast_id:
            contrast[key] = value
            return
    raise AssertionError(contrast_id)


def expect_protocol_fail(base, name, mutator):
    p = copy.deepcopy(base)
    mutator(p)
    try:
        validate_protocol_object(p)
    except ValidationError:
        return
    raise AssertionError(f"negative protocol case did not fail closed: {name}")


def expect_audit_fail(base, name, mutator):
    a = copy.deepcopy(base)
    mutator(a)
    try:
        validate_audit_object(a)
    except ValidationError:
        return
    raise AssertionError(f"negative audit case did not fail closed: {name}")


def main():
    base = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    validate_protocol_object(base)
    validate_audit_object(audit)

    cases = [
        ("protocol-id-drift", lambda p: p.__setitem__("protocol_id", "OTHER")),
        ("version-drift", lambda p: p.__setitem__("version", "0.3")),
        ("status-promotion", lambda p: p.__setitem__("status", "VALIDATED")),
        ("empirical-credit-laundering", lambda p: p.__setitem__("empirical_credit", "PROVISIONAL")),
        ("claim-extraction-opened", lambda p: p.__setitem__("claim_extraction", "READY")),
        ("batch-created", lambda p: p.__setitem__("batch", "BATCH-001")),
        ("freeze-created", lambda p: p.__setitem__("freeze", "FREEZE-001")),
        ("outcome-created", lambda p: p.__setitem__("outcome", "AVAILABLE")),
        ("batch-ready-flipped", lambda p: p.__setitem__("batch_ready", True)),
        ("batch-gate-opened", lambda p: p.__setitem__("batch_gate", "OPEN")),
        ("v01-history-lost", lambda p: p.__setitem__("supersedes_protocol_id", "NONE")),
        ("mapping-after-plate", lambda p: p["mapping_input_boundary"].__setitem__("mapping_before_plate_value_access", False)),
        ("plate-before-mapping", lambda p: p["mapping_input_boundary"].__setitem__("plate_value_access_before_mapping", True)),
        ("plate-values-allowed", lambda p: p["mapping_input_boundary"]["forbidden_before_mapping_freeze"].remove("current_plate_symbol_values")),
        ("peer-output-allowed", lambda p: p["mapping_input_boundary"]["forbidden_before_mapping_freeze"].remove("lane_peer_intermediate_output")),
        ("shared-role-catalog-removed", lambda p: p["shared_controls"].remove("source_role_catalog")),
        ("shared-world-manifest-removed", lambda p: p["shared_controls"].remove("world_variable_manifest")),
        ("shared-feature-manifest-removed", lambda p: p["shared_controls"].remove("feature_extraction_manifest")),
        ("bridge-lane-deleted", lambda p: p.__setitem__("lanes", [x for x in p["lanes"] if x["lane_id"] != "P2-A_PRIME"])),
        ("comparator-renamed", lambda p: mutate_lane(p, "P2-A", "model_name", "WEAK_STRAWMAN")),
        ("source-faithful-guard-disabled", lambda p: mutate_lane(p, "P2-A", "preserve_qm_src_0003_domain_roles", False)),
        ("global-priority-reordered", lambda p: mutate_lane(p, "P2-A", "layer_priority", ["八门", "奇仪", "八神", "九星"])),
        ("bridge-not-mandatory", lambda p: mutate_lane(p, "P2-A_PRIME", "bridge_ablation_required", False)),
        ("bridge-role-ablation-disabled", lambda p: mutate_lane(p, "P2-A_PRIME", "role_binding_policy", "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY")),
        ("bridge-priority-drift", lambda p: mutate_lane(p, "P2-A_PRIME", "layer_priority", ["奇仪", "八门", "九星", "八神"])),
        ("candidate-role-policy-drift", lambda p: mutate_lane(p, "P2-B", "role_binding_policy", "FREE_SELECTION")),
        ("candidate-layer-policy-drift", lambda p: mutate_lane(p, "P2-B", "layer_priority_policy", "POSTHOC_SELECTION")),
        ("lane-mapping-order-disabled", lambda p: mutate_lane(p, "P2-B", "mapping_must_precede_plate_values", False)),
        ("estimand-c1-expanded", lambda p: p["estimand_lock"]["P2-C1"].__setitem__("only_allowed_difference", "ROLE_PLUS_EXTRA_RULES")),
        ("estimand-c2-equality-disabled", lambda p: p["estimand_lock"]["P2-C2"].__setitem__("all_other_dimensions_equal", False)),
        ("c1-credit-laundering", lambda p: mutate_contrast(p, "P2-C1", "credit_scope", "FULL_BUNDLE")),
        ("c2-comparator-drift", lambda p: mutate_contrast(p, "P2-C2", "comparator", "P2-A")),
        ("c3-component-credit-laundering", lambda p: mutate_contrast(p, "P2-C3", "credit_scope", "TOPOLOGY_ROLE_BINDING_ONLY")),
        ("world-variable-parity-disabled", lambda p: p["representation_parity"].__setitem__("world_variable_manifest_shared", False)),
        ("lane-variable-expansion-enabled", lambda p: p["representation_parity"].__setitem__("lane_specific_world_variable_addition_forbidden", False)),
        ("symbol-vocabulary-parity-disabled", lambda p: p["representation_parity"].__setitem__("symbol_vocabulary_shared", False)),
        ("prediction-schema-parity-disabled", lambda p: p["representation_parity"].__setitem__("prediction_schema_shared", False)),
        ("priority-can-hide-layers", lambda p: p["layer_priority_semantics"].__setitem__("all_four_layers_visible_to_all_lanes", False)),
        ("priority-can-change-eligibility", lambda p: p["layer_priority_semantics"].__setitem__("priority_may_not_change_rule_eligibility", False)),
        ("priority-early-stop-enabled", lambda p: p["layer_priority_semantics"].__setitem__("priority_may_not_enable_early_stop", False)),
        ("role-budget-asymmetry", lambda p: p["complexity_budget"].__setitem__("role_multiplicity_budget_equal", False)),
        ("branch-budget-asymmetry", lambda p: p["complexity_budget"].__setitem__("reasoning_branch_budget_equal", False)),
        ("tool-budget-asymmetry", lambda p: p["complexity_budget"].__setitem__("tool_access_budget_equal", False)),
        ("candidate-extra-rules", lambda p: p["complexity_budget"].__setitem__("candidate_extra_rules_forbidden", False)),
        ("lane-label-unblinded", lambda p: p["blinding_and_isolation"].__setitem__("neutral_lane_labels_for_interpreters", False)),
        ("cross-lane-output-enabled", lambda p: p["blinding_and_isolation"].__setitem__("no_cross_lane_intermediate_output", False)),
        ("unblind-before-freeze", lambda p: p["blinding_and_isolation"].__setitem__("all_predictions_frozen_before_unblinding", False)),
        ("lane-specific-exclusion-enabled", lambda p: p["denominator_and_abstention"].__setitem__("lane_specific_case_exclusion_forbidden", False)),
        ("abstention-drops-denominator", lambda p: p["denominator_and_abstention"].__setitem__("abstain_never_silently_drops_case", False)),
        ("coverage-penalty-removed", lambda p: p["denominator_and_abstention"].__setitem__("coverage_penalized_metric_required", False)),
        ("generator-hash-disabled", lambda p: p["determinism_controls"].__setitem__("mapping_generators_versioned_and_hashed", False)),
        ("seed-not-frozen", lambda p: p["determinism_controls"].__setitem__("nondeterminism_seed_frozen", False)),
        ("repro-fixture-removed", lambda p: p["determinism_controls"].__setitem__("pre_batch_reproducibility_fixture_required", False)),
        ("post-outcome-mapping-selection", lambda p: p["abstention_policy"].__setitem__("post_outcome_mapping_selection_forbidden", False)),
        ("plan-repin-blocker-cleared", lambda p: p["plan_alignment"].__setitem__("status", "ALIGNED")),
        ("batch-creation-allowed", lambda p: p["plan_alignment"].__setitem__("batch_creation_allowed", True)),
        ("future-symbol-hash-removed", lambda p: p["future_batch_freeze_required"].remove("symbol_vocabulary_hash")),
        ("future-denominator-policy-removed", lambda p: p["future_batch_freeze_required"].remove("primary_denominator_policy")),
        ("future-repro-hash-removed", lambda p: p["future_batch_freeze_required"].remove("reproducibility_fixture_hash")),
    ]

    for name, mutator in cases:
        expect_protocol_fail(base, name, mutator)

    audit_cases = [
        ("audit-target-drift", lambda a: a.__setitem__("audit_target", "OTHER")),
        ("unsafe-verdict-erased", lambda a: a.__setitem__("audit_result", "V01_BATCH_SAFE")),
        ("premature-status-reassessment-erased", lambda a: a.__setitem__("prior_status_reassessment", "DESIGN_READY_WAS_CORRECT")),
        ("audit-batch-ready", lambda a: a.__setitem__("batch_ready", True)),
        ("audit-remediation-drift", lambda a: a.__setitem__("remediation_protocol", "NONE")),
        ("finding-deleted", lambda a: a.__setitem__("findings", [x for x in a["findings"] if x["finding_id"] != "P2-AUD-006"])),
        ("plan-blocker-falsely-closed", lambda a: next(x for x in a["findings"] if x["finding_id"] == "P2-AUD-012").__setitem__("status", "CLOSED_IN_V02")),
    ]
    for name, mutator in audit_cases:
        expect_audit_fail(audit, name, mutator)

    print(f"k2-qimen-role-map-comparative-negative-tests: PASS ({len(cases)} protocol + {len(audit_cases)} audit cases)")


if __name__ == "__main__":
    main()
