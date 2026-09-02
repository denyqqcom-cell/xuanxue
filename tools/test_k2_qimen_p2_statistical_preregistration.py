#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_statistical_preregistration import (
    StatisticalPreregistrationError,
    evaluate_contrast,
    exact_binomial_upper_tail,
    validate_preregistration,
    validate_statistical_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT = K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_CONTRACT_V01.json"
PREREG = K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_V01.json"
PRODUCTION_PROFILE_CONTRACT = K / "K2_QIMEN_P2_PRODUCTION_PROFILE_CONTRACT_V01.json"
PRODUCTION_REPRESENTATION = K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_V01.json"
SHARED_PROFILES = K / "K2_QIMEN_P2_SHARED_PROFILES_V01.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def must_fail(fn, *args):
    try:
        fn(*args)
    except StatisticalPreregistrationError:
        return
    raise AssertionError("invalid statistical preregistration case unexpectedly passed")


def main():
    contract = load(CONTRACT)
    profile_contract = load(PRODUCTION_PROFILE_CONTRACT)
    representation = load(PRODUCTION_REPRESENTATION)
    profiles = load(SHARED_PROFILES)

    validate_statistical_contract(
        copy.deepcopy(contract),
        copy.deepcopy(profile_contract),
        copy.deepcopy(representation),
        copy.deepcopy(profiles),
    )

    assert PREREG.exists(), "missing concrete P2 statistical preregistration artifact"
    prereg = load(PREREG)
    validate_preregistration(copy.deepcopy(prereg), copy.deepcopy(contract))

    assert exact_binomial_upper_tail(80, 0) == 1.0
    assert 0.5 < exact_binomial_upper_tail(80, 40) < 0.6
    assert exact_binomial_upper_tail(80, 60) < contract["confirmatory_test"]["per_contrast_alpha"]

    passing = evaluate_contrast(
        denominator=240,
        candidate_wins=62,
        comparator_wins=18,
        resolved_outcome_cases_total=200,
        resolved_outcome_cases_by_topology={"JOB_SEARCH": 70, "PROMOTION": 65, "TRANSFER_OR_ROLE_CHANGE": 65},
        contamination=False,
        contract=copy.deepcopy(contract),
    )
    assert passing["discordant_pairs"] == 80
    assert passing["paired_accuracy_delta"] > 0.05
    assert passing["information_floor_met"] is True
    assert passing["contrast_pass"] is True

    negative_cases = 0

    for path, bad_value in (
        (("primary_scope", "primary_batch_topologies"), ["JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE", "ORGANIZATIONAL_RELATIONSHIP"]),
        (("outcome_contract", "event_horizon_days"), 120),
        (("primary_metric", "abstain_score"), 0.5),
        (("confirmatory_test", "multiplicity_correction"), "NONE"),
        (("confirmatory_test", "practical_effect_floor_paired_accuracy_delta"), 0.0),
        (("sampling_rule", "target_cases_per_topology"), 100),
        (("sampling_rule", "outcome_dependent_case_selection_forbidden"), False),
        (("stopping_rule", "maximum_acquisition_window_days"), 730),
        (("stopping_rule", "closed_acquisition_may_not_reopen"), False),
        (("minimum_information_floor", "discordant_pairs_per_contrast"), 20),
        (("contrast_attribution", "component_credit_requires_own_contrast_pass"), False),
    ):
        x = copy.deepcopy(contract)
        x[path[0]][path[1]] = bad_value
        must_fail(validate_statistical_contract, x, copy.deepcopy(profile_contract), copy.deepcopy(representation), copy.deepcopy(profiles))
        negative_cases += 1

    x = copy.deepcopy(prereg)
    x["primary_metric"]["metric_id"] = "POST_HOC_METRIC"
    must_fail(validate_preregistration, x, copy.deepcopy(contract))
    negative_cases += 1

    low_info = evaluate_contrast(
        denominator=240,
        candidate_wins=55,
        comparator_wins=15,
        resolved_outcome_cases_total=200,
        resolved_outcome_cases_by_topology={"JOB_SEARCH": 70, "PROMOTION": 65, "TRANSFER_OR_ROLE_CHANGE": 65},
        contamination=False,
        contract=copy.deepcopy(contract),
    )
    assert low_info["discordant_pairs"] == 70
    assert low_info["information_floor_met"] is False
    assert low_info["contrast_pass"] is False
    negative_cases += 1

    low_effect = evaluate_contrast(
        denominator=240,
        candidate_wins=45,
        comparator_wins=35,
        resolved_outcome_cases_total=200,
        resolved_outcome_cases_by_topology={"JOB_SEARCH": 70, "PROMOTION": 65, "TRANSFER_OR_ROLE_CHANGE": 65},
        contamination=False,
        contract=copy.deepcopy(contract),
    )
    assert low_effect["discordant_pairs"] == 80
    assert low_effect["paired_accuracy_delta"] < 0.05
    assert low_effect["contrast_pass"] is False
    negative_cases += 1

    contaminated = evaluate_contrast(
        denominator=240,
        candidate_wins=62,
        comparator_wins=18,
        resolved_outcome_cases_total=200,
        resolved_outcome_cases_by_topology={"JOB_SEARCH": 70, "PROMOTION": 65, "TRANSFER_OR_ROLE_CHANGE": 65},
        contamination=True,
        contract=copy.deepcopy(contract),
    )
    assert contaminated["contrast_pass"] is False
    assert contaminated["contamination_gate_pass"] is False
    negative_cases += 1

    insufficient_outcome = evaluate_contrast(
        denominator=240,
        candidate_wins=62,
        comparator_wins=18,
        resolved_outcome_cases_total=170,
        resolved_outcome_cases_by_topology={"JOB_SEARCH": 60, "PROMOTION": 55, "TRANSFER_OR_ROLE_CHANGE": 55},
        contamination=False,
        contract=copy.deepcopy(contract),
    )
    assert insufficient_outcome["information_floor_met"] is False
    assert insufficient_outcome["contrast_pass"] is False
    negative_cases += 1

    assert negative_cases == 16
    print(
        "k2-qimen-p2-statistical-preregistration-tests: PASS "
        "negative_cases=16 metric=COVERAGE_PENALIZED_BINARY_ACCURACY_V01 "
        "test=EXACT_ONE_SIDED_MCNEMAR_BINOMIAL_V01 alpha=0.016666666666666666 "
        "effect_floor=0.05 target_n=240 discordant_floor=80 outcome_floor=180 "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
