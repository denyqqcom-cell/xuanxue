#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_abstain_denominator_scorer import (
    ScoringError,
    score_cases,
    validate_contrast_bindings,
    validate_scorer_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT = json.loads((K / "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json").read_text(encoding="utf-8"))
EXECUTION = json.loads((K / "K2_QIMEN_P2_EXECUTION_CONTRACT_V01.json").read_text(encoding="utf-8"))
FIXTURE = json.loads((ROOT / "tools/testdata/qimen_p2_abstain_denominator_fixture.json").read_text(encoding="utf-8"))


def expect_fail(fn, label):
    try:
        fn()
    except (ScoringError, KeyError, TypeError, ValueError):
        return
    raise AssertionError(f"negative case did not fail: {label}")


def run_positive():
    validate_scorer_contract(CONTRACT, EXECUTION)
    validate_contrast_bindings(
        FIXTURE["contrast_bindings"],
        FIXTURE["contrast_binding_frozen_before_outcome_scoring"],
        FIXTURE["validator_only_identity_map"],
        EXECUTION,
    )
    result = score_cases(
        FIXTURE["cases"],
        FIXTURE["frozen_case_ids"],
        FIXTURE["contrast_bindings"],
        FIXTURE["abstention_scoring_profile"],
        CONTRACT,
    )
    rows = {row["contrast_id"]: row for row in result["contrast_results"]}
    assert {row["denominator"] for row in rows.values()} == {FIXTURE["expected"]["denominator_per_contrast"]}
    for cid in ("P2-C1", "P2-C2", "P2-C3"):
        expected = FIXTURE["expected"][cid]
        actual = rows[cid]
        assert actual["paired_primary_delta"] == expected["paired_primary_delta"]
        assert actual["predicted_pair_count"] == expected["predicted_pair_count"]
        assert actual["abstain_case_count"] == expected["abstain_case_count"]
        assert actual["technical_unevaluable_case_count"] == expected["technical_unevaluable_case_count"]
    assert rows["P2-C3"]["component_credit_eligible"] is False
    assert result["lane_identity_visible_to_scorer"] is False
    assert result["empirical_credit"] == "NONE"


def main():
    run_positive()
    negative = []

    mutated = copy.deepcopy(FIXTURE["cases"])
    mutated[0]["lane_id"] = "P2-A"
    negative.append(lambda: score_cases(mutated, FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated = copy.deepcopy(FIXTURE["cases"])
    mutated[0]["model_name"] = "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01"
    negative.append(lambda: score_cases(mutated, FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["estimand_alignment"]["P2-C1"]["candidate"] = "P2-B"
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    mutated_bindings = copy.deepcopy(FIXTURE["contrast_bindings"])
    del mutated_bindings["P2-C3"]
    negative.append(lambda: validate_contrast_bindings(mutated_bindings, True, FIXTURE["validator_only_identity_map"], EXECUTION))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["denominator_policy"]["abstain_counts_in_primary_denominator"] = False
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["denominator_policy"]["lane_specific_case_exclusion_forbidden"] = False
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["denominator_policy"]["coverage_penalized_metric_required"] = False
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    mutated_profile = copy.deepcopy(FIXTURE["abstention_scoring_profile"])
    mutated_profile["per_blind_overrides"] = {"BLIND-003": {"abstain_metric_value": 1.0}}
    negative.append(lambda: score_cases(FIXTURE["cases"], FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], mutated_profile, CONTRACT))

    mutated_ids = list(FIXTURE["frozen_case_ids"])
    mutated_ids.remove("Q-FIX-002")
    negative.append(lambda: score_cases(FIXTURE["cases"], mutated_ids, FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated = copy.deepcopy(FIXTURE["cases"])
    mutated[2]["blind_outputs"]["BLIND-003"] = {"status": "PREDICTED", "metric_value": 0.1}
    negative.append(lambda: score_cases(mutated, FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated = copy.deepcopy(FIXTURE["cases"])
    mutated.append(copy.deepcopy(mutated[0]))
    negative.append(lambda: score_cases(mutated, FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated = copy.deepcopy(FIXTURE["cases"])
    mutated[1]["blind_outputs"]["BLIND-002"]["metric_value"] = 0.9
    negative.append(lambda: score_cases(mutated, FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated_bindings = copy.deepcopy(FIXTURE["contrast_bindings"])
    mutated_bindings["P2-C1"]["winner_lane"] = "P2-A_PRIME"
    negative.append(lambda: score_cases(FIXTURE["cases"], FIXTURE["frozen_case_ids"], mutated_bindings, FIXTURE["abstention_scoring_profile"], CONTRACT))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["estimand_alignment"]["P2-C3"]["component_credit_forbidden"] = False
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    mutated_profile = copy.deepcopy(FIXTURE["abstention_scoring_profile"])
    mutated_profile["frozen_before_outcome_scoring"] = False
    negative.append(lambda: score_cases(FIXTURE["cases"], FIXTURE["frozen_case_ids"], FIXTURE["contrast_bindings"], mutated_profile, CONTRACT))

    mutated_contract = copy.deepcopy(CONTRACT)
    mutated_contract["denominator_policy"]["technical_unevaluable_counts_in_primary_denominator"] = False
    negative.append(lambda: validate_scorer_contract(mutated_contract, EXECUTION))

    for idx, fn in enumerate(negative, 1):
        expect_fail(fn, f"case-{idx}")

    print(
        "k2-qimen-p2-abstain-denominator-tests: PASS "
        f"negative_cases={len(negative)} contrasts=P2-C1,P2-C2,P2-C3 denominator=ALL_FROZEN_INCLUDED_CASES"
    )


if __name__ == "__main__":
    main()
