#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_budget_enforcer import (
    BudgetError,
    enforce_budget,
    freeze_budget,
    validate_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_complexity_budget_fixture.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def must_fail(fn, *args):
    try:
        fn(*args)
    except BudgetError:
        return
    raise AssertionError("invalid complexity-budget case unexpectedly passed")


def main():
    contract = load(CONTRACT_PATH)
    fixture = load(FIXTURE_PATH)
    source = fixture["pre_freeze_budget_input"]
    profile = fixture["budget_profile"]

    validate_contract(copy.deepcopy(contract))
    first = freeze_budget(copy.deepcopy(source), copy.deepcopy(profile), copy.deepcopy(contract))
    second = freeze_budget(copy.deepcopy(source), copy.deepcopy(profile), copy.deepcopy(contract))
    assert first == second, "budget freeze must be deterministic"
    result = enforce_budget(copy.deepcopy(first), copy.deepcopy(source), copy.deepcopy(contract))
    assert result["decision"] == "ALLOW"
    assert result["over_budget"] is False
    assert result["lane_ids"] == ["P2-A", "P2-A_PRIME", "P2-B"]
    lane_totals = {row["total_units"] for row in result["per_lane"]}
    assert len(lane_totals) == 1, "all lanes must use one identical complexity formula"

    negative_cases = 0

    x = copy.deepcopy(contract)
    x["budget_domain"]["lane_formula_overrides"] = {"P2-B": "role_count * 2"}
    must_fail(validate_contract, x)
    negative_cases += 1

    x = copy.deepcopy(source)
    x["current_plate_symbol_values"] = {"乾": "fixture"}
    must_fail(freeze_budget, x, copy.deepcopy(profile), copy.deepcopy(contract))
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["shared_formula"]["total_units_per_lane"] = "role_count + outcome"
    must_fail(validate_contract, x)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["enforcement_policy"]["over_budget_action"] = "DEGRADE_AND_RUN"
    must_fail(validate_contract, x)
    negative_cases += 1

    frozen = freeze_budget(copy.deepcopy(source), copy.deepcopy(profile), copy.deepcopy(contract))
    x = copy.deepcopy(frozen)
    x["budget_profile"]["max_roles_per_question"] += 1
    must_fail(enforce_budget, x, copy.deepcopy(source), copy.deepcopy(contract))
    negative_cases += 1

    frozen = freeze_budget(copy.deepcopy(source), copy.deepcopy(profile), copy.deepcopy(contract))
    x = copy.deepcopy(source)
    x["role_candidates"].append({
        "role_id": "late_role",
        "symbol_instance_selector": {
            "symbol_type": "stem",
            "plate_layer": "heaven_plate",
            "instance_role": "late_role",
            "relation_direction": "FROM_ASKER_TO_ROLE"
        }
    })
    must_fail(enforce_budget, copy.deepcopy(frozen), x, copy.deepcopy(contract))
    negative_cases += 1

    x = copy.deepcopy(profile)
    x["max_roles_per_question"] = 1
    must_fail(freeze_budget, copy.deepcopy(source), x, copy.deepcopy(contract))
    negative_cases += 1

    x = copy.deepcopy(profile)
    x["max_total_units_per_lane"] = 7
    must_fail(freeze_budget, copy.deepcopy(source), x, copy.deepcopy(contract))
    negative_cases += 1

    xsource = copy.deepcopy(source)
    xsource["role_candidates"][1]["symbol_instance_selector"] = copy.deepcopy(
        xsource["role_candidates"][0]["symbol_instance_selector"]
    )
    xprofile = copy.deepcopy(profile)
    xprofile["max_role_bindings_per_symbol_instance"] = 1
    must_fail(freeze_budget, xsource, xprofile, copy.deepcopy(contract))
    negative_cases += 1

    x = copy.deepcopy(profile)
    x["lane_overrides"] = {"P2-B": {"max_total_units_per_lane": 999}}
    must_fail(freeze_budget, copy.deepcopy(source), x, copy.deepcopy(contract))
    negative_cases += 1

    x = copy.deepcopy(source)
    x["lane_output"] = {"P2-A": "peek"}
    must_fail(freeze_budget, x, copy.deepcopy(profile), copy.deepcopy(contract))
    negative_cases += 1

    assert negative_cases >= 8
    print(
        "k2-qimen-p2-complexity-budget-tests: PASS "
        f"negative_cases={negative_cases} lanes=3 formula=P2_SHARED_COMPLEXITY_FORMULA_V01"
    )


if __name__ == "__main__":
    main()
