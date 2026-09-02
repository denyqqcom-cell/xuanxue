#!/usr/bin/env python3
import copy

from k2_qimen_p2_materialize_production_profile import (
    materialize_production_bundle,
    validate_contract_bundle,
)
from test_k2_qimen_p2_production_profile import bundle_inputs, must_fail


def main():
    args = bundle_inputs()
    first = materialize_production_bundle(*copy.deepcopy(args))
    second = materialize_production_bundle(*copy.deepcopy(args))
    assert first == second, "production-profile materialization must be deterministic"
    assert first["production_representation_materialized"] is True
    assert first["production_complexity_profile_materialized"] is True
    assert first["production_abstention_profile_materialized"] is True
    assert first["statistical_preregistration_ready"] is False
    assert first["batch_creation_allowed"] is False
    assert first["batch"] == first["freeze"] == first["outcome"] == "NONE"
    assert first["empirical_credit"] == "NONE"

    negative_cases = 0

    xargs = list(bundle_inputs())
    xargs[0] = copy.deepcopy(xargs[0])
    xargs[0]["restricted_scope"]["high_impact_employment_decision_use_forbidden"] = False
    must_fail(validate_contract_bundle, xargs[0], xargs[3], xargs[4], xargs[5], xargs[6])
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[0] = copy.deepcopy(xargs[0])
    xargs[0]["restricted_scope"]["eligible_question_topologies"].append("SALARY_DECISION")
    must_fail(validate_contract_bundle, xargs[0], xargs[3], xargs[4], xargs[5], xargs[6])
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[0] = copy.deepcopy(xargs[0])
    xargs[0]["production_representation_requirements"]["shared_atomic_context_universe"] = ["奇仪", "八门", "八神", "九星"]
    must_fail(validate_contract_bundle, xargs[0], xargs[3], xargs[4], xargs[5], xargs[6])
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[0] = copy.deepcopy(xargs[0])
    xargs[0]["production_representation_requirements"]["P2_A_ranked_subset"].append("九宫")
    must_fail(validate_contract_bundle, xargs[0], xargs[3], xargs[4], xargs[5], xargs[6])
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[0] = copy.deepcopy(xargs[0])
    xargs[0]["production_representation_requirements"]["P2_B_primary_set_internal_order"] = "奇仪>八门"
    must_fail(validate_contract_bundle, xargs[0], xargs[3], xargs[4], xargs[5], xargs[6])
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[1] = copy.deepcopy(xargs[1])
    xargs[1]["symbol_vocabulary"]["atomic_context_layers"] = ["奇仪", "八门", "八神", "九星"]
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[1] = copy.deepcopy(xargs[1])
    xargs[1]["eligible_rule_pool"]["lane_specific_additions"] = True
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[1] = copy.deepcopy(xargs[1])
    xargs[1]["world_variable_manifest"]["high_impact_employment_decision_use_forbidden"] = False
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    for field, value in (
        ("max_roles_per_question", 4),
        ("max_layers_per_question", 4),
        ("max_symbol_instances_per_question", 4),
        ("max_total_units_per_lane", 14),
        ("max_role_bindings_per_symbol_instance", 2),
    ):
        xargs = list(bundle_inputs())
        xargs[2] = copy.deepcopy(xargs[2])
        xargs[2]["complexity_profile"][field] = value
        must_fail(materialize_production_bundle, *xargs)
        negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[2] = copy.deepcopy(xargs[2])
    xargs[2]["complexity_profile"]["lane_overrides"] = {"P2-B": {"max_total_units_per_lane": 99}}
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[2] = copy.deepcopy(xargs[2])
    xargs[2]["abstention_profile"]["fixture_synthetic_values"] = True
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[2] = copy.deepcopy(xargs[2])
    xargs[2]["abstention_profile"]["abstain_metric_value"] = 1.0
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    xargs = list(bundle_inputs())
    xargs[2] = copy.deepcopy(xargs[2])
    xargs[2]["abstention_profile"]["lane_overrides"] = {"P2-B": {"abstain_metric_value": 1.0}}
    must_fail(materialize_production_bundle, *xargs)
    negative_cases += 1

    assert negative_cases == 17
    print(
        "k2-qimen-p2-production-profile-tests-v02: PASS "
        f"negative_cases={negative_cases} scope=WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE "
        "atomic_layers=5 roles=5 complexity_total=15 abstain_metric=0.0 "
        "production_representation=true statistical_preregistration=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
