#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from validate_k2_qimen_role_map_comparative import ValidationError, validate_protocol_object

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V01.json"


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


def expect_fail(base, name, mutator):
    p = copy.deepcopy(base)
    mutator(p)
    try:
        validate_protocol_object(p)
    except ValidationError:
        return
    raise AssertionError(f"negative case did not fail closed: {name}")


def main():
    base = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    validate_protocol_object(base)

    cases = [
        ("protocol-id-drift", lambda p: p.__setitem__("protocol_id", "OTHER")),
        ("version-drift", lambda p: p.__setitem__("version", "0.2")),
        ("status-promotion", lambda p: p.__setitem__("status", "VALIDATED")),
        ("empirical-credit-laundering", lambda p: p.__setitem__("empirical_credit", "PROVISIONAL")),
        ("claim-extraction-opened", lambda p: p.__setitem__("claim_extraction", "READY")),
        ("batch-created", lambda p: p.__setitem__("batch", "BATCH-001")),
        ("freeze-created", lambda p: p.__setitem__("freeze", "FREEZE-001")),
        ("outcome-created", lambda p: p.__setitem__("outcome", "AVAILABLE")),
        ("mapping-after-plate", lambda p: p["mapping_input_boundary"].__setitem__("mapping_before_plate_value_access", False)),
        ("plate-before-mapping", lambda p: p["mapping_input_boundary"].__setitem__("plate_value_access_before_mapping", True)),
        ("plate-values-allowed", lambda p: p["mapping_input_boundary"]["forbidden_before_mapping_freeze"].remove("current_plate_symbol_values")),
        ("shared-role-catalog-removed", lambda p: p["shared_controls"].remove("source_role_catalog")),
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
        ("c1-credit-laundering", lambda p: mutate_contrast(p, "P2-C1", "credit_scope", "FULL_BUNDLE")),
        ("c2-comparator-drift", lambda p: mutate_contrast(p, "P2-C2", "comparator", "P2-A")),
        ("c3-component-credit-laundering", lambda p: mutate_contrast(p, "P2-C3", "credit_scope", "TOPOLOGY_ROLE_BINDING_ONLY")),
        ("post-outcome-mapping-selection", lambda p: p["abstention_policy"].__setitem__("post_outcome_mapping_selection_forbidden", False)),
    ]

    for name, mutator in cases:
        expect_fail(base, name, mutator)

    print(f"k2-qimen-role-map-comparative-negative-tests: PASS ({len(cases)} cases)")


if __name__ == "__main__":
    main()
