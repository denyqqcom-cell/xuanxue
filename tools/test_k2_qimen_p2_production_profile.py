#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_materialize_production_profile import (
    ProductionProfileError,
    materialize_production_bundle,
    validate_contract_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT = K / "K2_QIMEN_P2_PRODUCTION_PROFILE_CONTRACT_V01.json"
PARITY = K / "K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V02.json"
REP_V02_CONTRACT = K / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json"
COMPLEXITY_CONTRACT = K / "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json"
ABSTAIN_CONTRACT = K / "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json"
PRODUCTION_SOURCE = K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_SOURCE_V01.json"
PRODUCTION_REPRESENTATION = K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_V01.json"
SHARED_PROFILES = K / "K2_QIMEN_P2_SHARED_PROFILES_V01.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def must_fail(fn, *args):
    try:
        fn(*args)
    except ProductionProfileError:
        return
    raise AssertionError("invalid production-profile case unexpectedly passed")


def bundle_inputs():
    return (
        load(CONTRACT),
        load(PRODUCTION_SOURCE),
        load(SHARED_PROFILES),
        load(REP_V02_CONTRACT),
        load(PARITY),
        load(COMPLEXITY_CONTRACT),
        load(ABSTAIN_CONTRACT),
    )


def main():
    contract = load(CONTRACT)
    rep_v02_contract = load(REP_V02_CONTRACT)
    parity = load(PARITY)
    complexity_contract = load(COMPLEXITY_CONTRACT)
    abstain_contract = load(ABSTAIN_CONTRACT)

    validate_contract_bundle(
        copy.deepcopy(contract),
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )

    assert PRODUCTION_SOURCE.exists(), "missing restricted production representation source"
    assert PRODUCTION_REPRESENTATION.exists(), "missing restricted production representation artifact"
    assert SHARED_PROFILES.exists(), "missing restricted production shared profiles artifact"

    args = bundle_inputs()
    first = materialize_production_bundle(*copy.deepcopy(args))
    second = materialize_production_bundle(*copy.deepcopy(args))
    assert first == second, "production-profile materialization must be deterministic"
    assert first["representation"] == load(PRODUCTION_REPRESENTATION)
    assert first["shared_profiles"] == load(SHARED_PROFILES)
    assert first["production_representation_materialized"] is True
    assert first["production_complexity_profile_materialized"] is True
    assert first["production_abstention_profile_materialized"] is True
    assert first["statistical_preregistration_ready"] is False
    assert first["batch_creation_allowed"] is False
    assert first["batch"] == first["freeze"] == first["outcome"] == "NONE"
    assert first["empirical_credit"] == "NONE"

    negative_cases = 0

    x = copy.deepcopy(contract)
    x["restricted_scope"]["high_impact_employment_decision_use_forbidden"] = False
    must_fail(
        validate_contract_bundle,
        x,
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["restricted_scope"]["eligible_question_topologies"].append("SALARY_DECISION")
    must_fail(
        validate_contract_bundle,
        x,
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["production_representation_requirements"]["shared_atomic_context_universe"] = ["奇仪", "八门", "八神", "九星"]
    must_fail(
        validate_contract_bundle,
        x,
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["production_representation_requirements"]["P2_A_ranked_subset"].append("九宫")
    must_fail(
        validate_contract_bundle,
        x,
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["production_representation_requirements"]["P2_B_primary_set_internal_order"] = "奇仪>八门"
    must_fail(
        validate_contract_bundle,
        x,
        copy.deepcopy(rep_v02_contract),
        copy.deepcopy(parity),
        copy.deepcopy(complexity_contract),
        copy.deepcopy(abstain_contract),
    )
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[1])
    x["symbol_vocabulary"]["atomic_context_layers"] = ["奇仪", "八门", "八神", "九星"]
    args[1] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[1])
    x["eligible_rule_pool"]["lane_specific_additions"] = True
    args[1] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[1])
    x["world_variable_manifest"]["high_impact_employment_decision_use_forbidden"] = False
    args[1] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    for field in (
        "max_roles_per_question",
        "max_layers_per_question",
        "max_symbol_instances_per_question",
        "max_total_units_per_lane",
        "max_role_bindings_per_symbol_instance",
    ):
        args = list(bundle_inputs())
        x = copy.deepcopy(args[2])
        if field == "max_total_units_per_lane":
            x["complexity_profile"][field] = 14
        elif field == "max_role_bindings_per_symbol_instance":
            x["complexity_profile"][field] = 2
        else:
            x["complexity_profile"][field] = 4
        args[2] = x
        must_fail(materialize_production_bundle, *args)
        negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[2])
    x["complexity_profile"]["lane_overrides"] = {"P2-B": {"max_total_units_per_lane": 99}}
    args[2] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[2])
    x["abstention_profile"]["fixture_synthetic_values"] = True
    args[2] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[2])
    x["abstention_profile"]["abstain_metric_value"] = 1.0
    args[2] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    args = list(bundle_inputs())
    x = copy.deepcopy(args[2])
    x["abstention_profile"]["lane_overrides"] = {"P2-B": {"abstain_metric_value": 1.0}}
    args[2] = x
    must_fail(materialize_production_bundle, *args)
    negative_cases += 1

    assert negative_cases == 16
    print(
        "k2-qimen-p2-production-profile-tests: PASS "
        "negative_cases=16 scope=WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE "
        "atomic_layers=5 roles=5 complexity_total=15 abstain_metric=0.0 "
        "production_representation=true statistical_preregistration=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
