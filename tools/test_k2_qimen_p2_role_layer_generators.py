#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_generate_mapping import (
    FIXED_GLOBAL_PRIORITY,
    LANE_IDS,
    ContaminationError,
    MappingBoundaryError,
    RoleLayerSession,
    SourceLocalityError,
    generate_all_lane_mappings,
    validate_pre_plate_input,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_role_layer_generator_fixture.json"


def must_fail(exc_type, fn, label):
    try:
        fn()
    except exc_type:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert fixture["fixture_only"] is True
    pre = fixture["pre_plate_input"]

    validate_pre_plate_input(pre)
    first = generate_all_lane_mappings(pre)
    second = generate_all_lane_mappings(copy.deepcopy(pre))
    assert first == second, "same pre-plate input must reproduce exact maps"
    assert tuple(first) == LANE_IDS

    lane_a = first["P2-A"]
    lane_ap = first["P2-A_PRIME"]
    lane_b = first["P2-B"]

    assert lane_a["model_name"] == "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01"
    assert lane_ap["model_name"] == "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01"
    assert lane_b["model_name"] == "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01"

    assert lane_a["layer_priority"] == list(FIXED_GLOBAL_PRIORITY)
    assert lane_ap["layer_priority"] == list(FIXED_GLOBAL_PRIORITY)
    assert lane_b["layer_priority"] == pre["topology_layer_priority"]["priority"]

    expected_catalog_roles = sorted(x["role_id"] for x in pre["source_role_catalog"])
    assert [x["role_id"] for x in lane_a["roles"]] == expected_catalog_roles

    assert lane_ap["roles"] == lane_b["roles"]
    assert lane_ap["correction_registry"] == lane_b["correction_registry"]
    assert lane_ap["competing_mappings"] == lane_b["competing_mappings"]

    compare_keys = {
        "mapping_input_sha256",
        "roles",
        "correction_registry",
        "competing_mappings",
        "role_binding_policy",
    }
    for key in compare_keys:
        assert lane_ap[key] == lane_b[key], f"P2-C2 drift outside layer priority: {key}"

    negative_cases = 0

    x = copy.deepcopy(pre)
    x["current_plate_symbol_values"] = {"fixture": "forbidden"}
    must_fail(MappingBoundaryError, lambda: validate_pre_plate_input(x), "plate values before mapping")
    negative_cases += 1

    x = copy.deepcopy(pre)
    x["topology_role_candidates"][0]["source_scope"] = "GLOBAL"
    must_fail(SourceLocalityError, lambda: validate_pre_plate_input(x), "source-local role globalization")
    negative_cases += 1

    x = copy.deepcopy(pre)
    x["correction_registry"][0]["source_scope"] = "GLOBAL"
    must_fail(SourceLocalityError, lambda: validate_pre_plate_input(x), "source-local correction globalization")
    negative_cases += 1

    x = copy.deepcopy(pre)
    del x["topology_role_candidates"][0]["symbol_instance_selector"]["plate_layer"]
    must_fail(MappingBoundaryError, lambda: validate_pre_plate_input(x), "unqualified symbol instance")
    negative_cases += 1

    session = RoleLayerSession(copy.deepcopy(pre))
    must_fail(MappingBoundaryError, lambda: session.read_plate_values({"fixture": 1}), "plate read before freeze")
    negative_cases += 1

    session = RoleLayerSession(copy.deepcopy(pre))
    session.freeze_mappings()
    session.read_plate_values({"fixture": 1})
    must_fail(ContaminationError, lambda: session.attempt_role_map_edit("late role remap"), "late Role Map edit")
    assert session.contamination_ledger[-1]["kind"] == "LATE_ROLE_MAP_EDIT"
    negative_cases += 1

    session = RoleLayerSession(copy.deepcopy(pre))
    session.freeze_mappings()
    session.read_plate_values({"fixture": 1})
    session.read_feedback({"fixture_outcome": "known"})
    must_fail(ContaminationError, lambda: session.attempt_role_switch("topology_peer"), "post-feedback role switch")
    assert session.contamination_ledger[-1]["kind"] == "POST_FEEDBACK_ROLE_SWITCH"
    negative_cases += 1

    must_fail(
        ContaminationError,
        lambda: session.attempt_correction_registry_edit({"correction_id": "posthoc"}),
        "post-feedback correction edit",
    )
    assert session.contamination_ledger[-1]["kind"] == "POST_FEEDBACK_CORRECTION_EDIT"
    negative_cases += 1

    session = RoleLayerSession(copy.deepcopy(pre))
    must_fail(
        ContaminationError,
        lambda: session.select_unfrozen_competing_mapping(
            "fixture_parent_role_option_a", selection_basis="OUTCOME_HIT"
        ),
        "outcome-selected competing mapping",
    )
    assert session.contamination_ledger[-1]["kind"] == "UNFROZEN_COMPETING_MAPPING_OUTCOME_SELECTION"
    negative_cases += 1

    assert negative_cases == 9
    print(
        "k2-qimen-p2-role-layer-generator-tests: PASS "
        f"negative_cases={negative_cases} lanes={','.join(LANE_IDS)}"
    )


if __name__ == "__main__":
    main()
