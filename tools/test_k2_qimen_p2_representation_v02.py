#!/usr/bin/env python3
import copy
import hashlib
import json
from pathlib import Path

from k2_qimen_p2_materialize_representation_v02 import (
    ATOMIC_CONTEXT_LAYERS,
    COMPONENT_FIELDS,
    DERIVED_COMPOSITES,
    LANE_IDS,
    ValidationError,
    materialize_representation_v02,
    validate_materialized_v02,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "knowledge" / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json"
EXPECTED_CONTRACT_SHA256 = "ad7b30fb42510132f03dd86dd5d98a0c59653715937a2a43d970b1d58a774180"

SOURCE = {
    "representation_id": "QRM-P2-SHARED-SUPERSET-REPRESENTATION-V02-FIXTURE",
    "world_variable_manifest": {
        "variables": [
            {"id": "W1", "name": "question_domain", "type": "categorical"},
            {"id": "W2", "name": "asked_object", "type": "categorical"},
            {"id": "W3", "name": "method_layer", "type": "categorical"},
        ]
    },
    "symbol_vocabulary": {
        "atomic_context_layers": ["奇仪", "八门", "八神", "九星", "九宫"],
        "derived_composites": ["格局"],
        "visibility": "ALL_LANES",
    },
    "feature_extraction_manifest": {
        "features": [
            "symbol_instance",
            "palace_identity",
            "palace_relation",
            "wangshuai",
            "season",
            "configuration_composite",
        ],
        "depth": "SHARED",
        "derived_composite_source": "SHARED_INPUTS_ONLY",
    },
    "eligible_rule_pool": {
        "rule_ids": ["R-SOURCE-ROLE", "R-PRIORITY-POLICY", "R-DERIVED-COMPOSITE"],
        "lane_specific_additions": False,
    },
    "prediction_schema": {
        "type": "object",
        "required": ["prediction", "confidence", "abstain"],
    },
    "priority_policy_schema": {
        "policy_forms": [
            "FIXED_RANKED_SUBSET_WITH_VISIBLE_UNRANKED_CONTEXT",
            "QUESTION_DOMAIN_CONDITIONED_PARTIAL_PRIORITY_OR_PRIMARY_LAYER",
        ],
        "ranked_subset_may_be_partial": True,
        "visible_unranked_context_required_when_not_ranked": True,
        "unsupported_total_order_action": "ABSTAIN_FAIL_CLOSED",
        "plate_value_selected_priority_forbidden": True,
        "outcome_or_feedback_selected_priority_forbidden": True,
    },
}


def canonical_sha256(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def source_must_fail(value):
    try:
        materialize_representation_v02(value)
    except ValidationError:
        return
    raise AssertionError("invalid V02 representation source unexpectedly passed")


def materialized_must_fail(value):
    try:
        validate_materialized_v02(value)
    except ValidationError:
        return
    raise AssertionError("invalid materialized V02 representation unexpectedly passed")


def main():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert canonical_sha256(contract) == EXPECTED_CONTRACT_SHA256, "V02 contract canonical hash drift"
    assert contract["representation_model"]["shared_atomic_context_universe"] == list(ATOMIC_CONTEXT_LAYERS)
    assert contract["representation_model"]["derived_composites"] == list(DERIVED_COMPOSITES)

    first = materialize_representation_v02(copy.deepcopy(SOURCE))
    second = materialize_representation_v02(copy.deepcopy(SOURCE))
    assert first == second, "same input must materialize byte-equivalent V02 data"
    validate_materialized_v02(first)

    assert first["artifact_kind"] == "P2_SHARED_SUPERSET_REPRESENTATION_MANIFEST_V02"
    assert set(first["shared_manifests"]) == set(COMPONENT_FIELDS)
    assert first["shared_atomic_context_universe"] == list(ATOMIC_CONTEXT_LAYERS)
    assert first["derived_composites"] == list(DERIVED_COMPOSITES)
    assert [x["lane_id"] for x in first["lane_bindings"]] == list(LANE_IDS)
    expected_hash = first["shared_representation_sha256"]
    for lane in first["lane_bindings"]:
        assert lane["shared_representation_sha256"] == expected_hash
        assert lane["shared_atomic_context_universe"] == list(ATOMIC_CONTEXT_LAYERS)
        assert lane["derived_composites"] == list(DERIVED_COMPOSITES)

    cases = []

    x = copy.deepcopy(SOURCE)
    x["symbol_vocabulary"]["atomic_context_layers"].remove("九宫")
    cases.append(("drop_九宫", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["symbol_vocabulary"]["atomic_context_layers"].append("格局")
    cases.append(("格局_as_atomic", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["symbol_vocabulary"]["derived_composites"] = []
    cases.append(("drop_格局_composite", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["symbol_vocabulary"]["visibility"] = "P2-B_ONLY"
    cases.append(("lane_specific_visibility", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["lane_overrides"] = {"P2-B": {"symbol_vocabulary": {"atomic_context_layers": ["八门"]}}}
    cases.append(("lane_override", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["priority_policy_schema"]["policy_forms"] = ["TOTAL_ORDER_ONLY"]
    cases.append(("total_order_only", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["priority_policy_schema"]["ranked_subset_may_be_partial"] = False
    cases.append(("forbid_partial_rank", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["priority_policy_schema"]["unsupported_total_order_action"] = "INVENT_ORDER"
    cases.append(("invent_total_order", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["priority_policy_schema"]["plate_value_selected_priority_forbidden"] = False
    cases.append(("plate_select_priority", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["priority_policy_schema"]["outcome_or_feedback_selected_priority_forbidden"] = False
    cases.append(("outcome_select_priority", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["eligible_rule_pool"]["lane_specific_additions"] = True
    cases.append(("lane_rule_addition", x, "source"))

    x = copy.deepcopy(SOURCE)
    x["production_domain_instance"] = {"domain": "WORKPLACE"}
    cases.append(("production_instance_smuggled_into_contract_fixture", x, "source"))

    x = copy.deepcopy(first)
    x["shared_atomic_context_universe"] = ["奇仪", "八门", "八神", "九星"]
    cases.append(("materialized_drop_九宫", x, "materialized"))

    x = copy.deepcopy(first)
    x["derived_composites"] = []
    cases.append(("materialized_drop_格局", x, "materialized"))

    x = copy.deepcopy(first)
    x["lane_bindings"][2]["shared_atomic_context_universe"] = ["八门"]
    cases.append(("lane_universe_drift", x, "materialized"))

    x = copy.deepcopy(first)
    x["lane_bindings"][2]["shared_representation_sha256"] = "0" * 64
    cases.append(("lane_digest_drift", x, "materialized"))

    x = copy.deepcopy(first)
    x["shared_manifest_hashes"]["priority_policy_schema"] = "f" * 64
    cases.append(("policy_schema_hash_drift", x, "materialized"))

    for _, candidate, kind in cases:
        if kind == "source":
            source_must_fail(candidate)
        else:
            materialized_must_fail(candidate)

    print(
        "k2-qimen-p2-representation-v02-tests: PASS "
        f"negative_cases={len(cases)} lanes={len(LANE_IDS)} shared_components={len(COMPONENT_FIELDS)} "
        "atomic_layers=5 derived_composites=1 partial_priority=true production_instance=false"
    )


if __name__ == "__main__":
    main()
