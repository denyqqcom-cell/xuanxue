#!/usr/bin/env python3
import copy

from k2_qimen_p2_materialize_representation import (
    COMPONENT_FIELDS,
    LANE_IDS,
    ValidationError,
    materialize_representation,
    validate_materialized,
)

SOURCE = {
    "representation_id": "QRM-P2-REPRESENTATION-FIXTURE-V01",
    "world_variable_manifest": {
        "variables": [
            {"id": "W1", "name": "question_domain", "type": "categorical"},
            {"id": "W2", "name": "asked_object", "type": "categorical"},
        ]
    },
    "symbol_vocabulary": {
        "layers": ["奇仪", "八门", "八神", "九星"],
        "visibility": "ALL_LANES",
    },
    "feature_extraction_manifest": {
        "features": ["palace_relation", "wangshuai", "season", "configuration"],
        "depth": "SHARED",
    },
    "eligible_rule_pool": {
        "rule_ids": ["R-SOURCE-ROLE", "R-LAYER-AGGREGATION"],
        "lane_specific_additions": False,
    },
    "prediction_schema": {
        "type": "object",
        "required": ["prediction", "confidence", "abstain"],
    },
}


def source_must_fail(value):
    try:
        materialize_representation(value)
    except ValidationError:
        return
    raise AssertionError("invalid representation source unexpectedly passed")


def materialized_must_fail(value):
    try:
        validate_materialized(value)
    except ValidationError:
        return
    raise AssertionError("invalid materialized representation unexpectedly passed")


def main():
    first = materialize_representation(copy.deepcopy(SOURCE))
    second = materialize_representation(copy.deepcopy(SOURCE))
    assert first == second, "same input must materialize byte-equivalent data"
    validate_materialized(first)

    assert first["artifact_kind"] == "P2_SHARED_REPRESENTATION_MANIFEST"
    assert set(first["shared_manifests"]) == set(COMPONENT_FIELDS)
    assert set(first["shared_manifest_hashes"]) == set(COMPONENT_FIELDS)
    assert [x["lane_id"] for x in first["lane_bindings"]] == list(LANE_IDS)

    expected_hashes = first["shared_manifest_hashes"]
    expected_representation_hash = first["shared_representation_sha256"]
    for lane in first["lane_bindings"]:
        assert lane["shared_manifest_hashes"] == expected_hashes
        assert lane["shared_representation_sha256"] == expected_representation_hash

    negative_cases = 0

    x = copy.deepcopy(SOURCE)
    x["lane_overrides"] = {"P2-B": {"eligible_rule_pool": {"rule_ids": ["EXTRA"]}}}
    source_must_fail(x)
    negative_cases += 1

    x = copy.deepcopy(SOURCE)
    del x["prediction_schema"]
    source_must_fail(x)
    negative_cases += 1

    x = copy.deepcopy(first)
    x["lane_bindings"][2]["shared_manifest_hashes"] = dict(x["lane_bindings"][2]["shared_manifest_hashes"])
    x["lane_bindings"][2]["shared_manifest_hashes"]["eligible_rule_pool"] = "0" * 64
    materialized_must_fail(x)
    negative_cases += 1

    x = copy.deepcopy(first)
    x["lane_bindings"] = x["lane_bindings"][:2]
    materialized_must_fail(x)
    negative_cases += 1

    x = copy.deepcopy(first)
    x["shared_representation_sha256"] = "f" * 64
    materialized_must_fail(x)
    negative_cases += 1

    print(
        "k2-qimen-p2-representation-tests: PASS "
        f"negative_cases={negative_cases} lanes={len(LANE_IDS)} components={len(COMPONENT_FIELDS)}"
    )


if __name__ == "__main__":
    main()
