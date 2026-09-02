#!/usr/bin/env python3
import copy
import json
import subprocess
from pathlib import Path

from k2_qimen_p2_statistical_preregistration import (
    validate_preregistration,
    validate_statistical_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
T = ROOT / "tools"

EXPECTED = {
    K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_CONTRACT_V01.json": "212f4955927870c140a91bf6b6763a9c9938ddad",
    K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_V01.json": "4cc3de63c8509fb00893d9cf788f17224f389014",
    T / "k2_qimen_p2_statistical_preregistration.py": "041c160c9e0c4aa6de8867913b9f921070a4fe00",
    T / "test_k2_qimen_p2_statistical_preregistration.py": "963c46dd8b9ce82595fad3227e48ae12724eeed8",
    K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V16.json": "fced9823d77f8b879fcb0980982e0270e537da6c",
    K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V20.json": "1e71c0c8cf4ef848372ca91f3f3e7f4c7a50b1ae",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    contract = load(K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_CONTRACT_V01.json")
    prereg = load(K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_V01.json")
    profile_contract = load(K / "K2_QIMEN_P2_PRODUCTION_PROFILE_CONTRACT_V01.json")
    representation = load(K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_V01.json")
    profiles = load(K / "K2_QIMEN_P2_SHARED_PROFILES_V01.json")
    implementation = load(K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V16.json")
    protocol = load(K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V20.json")

    validate_statistical_contract(
        copy.deepcopy(contract),
        copy.deepcopy(profile_contract),
        copy.deepcopy(representation),
        copy.deepcopy(profiles),
    )
    validate_preregistration(copy.deepcopy(prereg), copy.deepcopy(contract))

    for path, expected in EXPECTED.items():
        require(path.exists(), f"missing closure artifact: {path.relative_to(ROOT)}")
        require(git_blob(path) == expected, f"git blob drift: {path.relative_to(ROOT)}")

    binding = prereg.get("profile_metric_binding", {})
    require(binding.get("status") == "BOUND_BY_THIS_PREREGISTRATION_WITHOUT_REWRITING_SHARED_PROFILES_V01", "metric/profile binding status drift")
    require(binding.get("primary_metric_id") == "COVERAGE_PENALIZED_BINARY_ACCURACY_V01", "bound metric drift")
    require(binding.get("metric_range") == [0.0, 1.0], "bound metric range drift")
    require(binding.get("abstain_metric_value") == 0.0, "bound ABSTAIN score drift")
    require(binding.get("technical_unevaluable_metric_value") == 0.0, "bound technical UNEVALUABLE score drift")
    require(binding.get("compatibility") == "PASS_EXACT_ZERO_VALUE_MATCH", "metric/profile compatibility missing")

    eligibility = prereg.get("eligibility_and_dependence_guard", {})
    required_fields = {
        "case_id",
        "question_topology",
        "asker_identity_hash",
        "target_object_hash",
        "case_freeze_timestamp",
        "outcome_deadline_timestamp",
        "outcome_ascertainment_route",
        "eligibility_reason_code",
    }
    require(eligibility.get("eligibility_must_be_decidable_before_lane_execution") is True, "pre-lane eligibility guard missing")
    require(set(eligibility.get("required_pre_lane_fields", [])) == required_fields, "eligibility manifest fields drift")
    require(eligibility.get("one_included_case_per_asker_per_future_batch") is True, "repeat-asker dependence guard missing")
    require(eligibility.get("duplicate_target_event_record_forbidden") is True, "duplicate target-event guard missing")
    require(eligibility.get("outcome_ascertainment_route_must_be_frozen_pre_lane") is True, "outcome ascertainment freeze guard missing")
    require(eligibility.get("outcome_known_or_partially_revealed_at_freeze_forbidden") is True, "known outcome leakage guard missing")
    require(eligibility.get("post_prediction_replacement_forbidden") is True, "post-prediction replacement guard missing")

    require(implementation.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V16", "implementation id drift")
    require(implementation.get("p2_prebatch_stat_004", {}).get("status") == "CLOSED_CONCRETE_STATISTICAL_PREREGISTRATION", "STAT-004 implementation closure missing")
    require(implementation.get("closure_self_audit", {}).get("guard_weakening_used") is False, "closure weakened a guard")
    require(implementation.get("closure_self_audit", {}).get("outcome_data_consulted") is False, "outcome leakage in closure self-audit")
    require(implementation.get("statistical_preregistration_ready") is True, "implementation preregistration readiness missing")
    require(implementation.get("batch_ready") is False and implementation.get("batch_creation_allowed") is False, "implementation must not open Batch")

    require(protocol.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V20", "protocol id drift")
    require(protocol.get("status") == "CONCRETE_STATISTICAL_PREREGISTRATION_CLOSED_PRE_BATCH_REGISTRY", "protocol closure state drift")
    require(protocol.get("statistical_preregistration", {}).get("status") == "CLOSED_CONCRETE_PREREGISTRATION", "protocol preregistration closure missing")
    require(protocol.get("statistical_preregistration", {}).get("one_included_case_per_asker_per_future_batch") is True, "protocol repeat-asker guard drift")
    require(protocol.get("closure_self_audit", {}).get("guard_weakening_used") is False, "protocol closure weakened a guard")
    require(protocol.get("statistical_preregistration_ready") is True, "protocol preregistration readiness missing")
    require(protocol.get("batch_ready") is False and protocol.get("batch_creation_allowed") is False, "protocol must not open Batch")

    for artifact in (contract, prereg, implementation, protocol):
        require(artifact.get("outcome_data_used") is False, "outcome data use detected")
        require(artifact.get("batch") == artifact.get("freeze") == artifact.get("outcome") == "NONE", "Batch/Freeze/Outcome mutation detected")
        require(artifact.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
        if "claim_extraction" in artifact:
            require(artifact.get("claim_extraction") == "BLOCKED", "claim extraction must remain blocked")

    provenance = contract.get("design_provenance", {})
    require(provenance.get("statistical_choices_origin") == "PROJECT_GENERATED_METHODOLOGICAL_PREREGISTRATION", "statistics provenance drift")
    require(provenance.get("qimen_source_semantic_credit") == "NONE", "statistical choices cannot receive Qimen source-semantic credit")

    print(
        "k2-qimen-p2-statistical-preregistration-validator: PASS "
        "gate=CLOSED_CONCRETE_STATISTICAL_PREREGISTRATION metric=COVERAGE_PENALIZED_BINARY_ACCURACY_V01 "
        "test=EXACT_ONE_SIDED_MCNEMAR_BINOMIAL_V01 target_n=240 one_case_per_asker=true "
        "statistical_preregistration_ready=true batch_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
