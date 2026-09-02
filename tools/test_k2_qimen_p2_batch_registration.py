#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_batch_registration import (
    BatchRegistrationError,
    bind_batch_registration_candidate,
    canonical_sha256,
    validate_batch_registration_contract,
    validate_registration_input,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT = K / "K2_QIMEN_P2_BATCH_REGISTRATION_CONTRACT_V01.json"
PREREG = K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_V01.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def must_fail(fn, *args):
    try:
        fn(*args)
    except BatchRegistrationError:
        return
    raise AssertionError("invalid Batch registration case unexpectedly passed")


def fixture_input(prereg):
    return {
        "batch_id": "FIXTURE-P2-QRM-001",
        "batch_start_timestamp_utc": "2030-01-01T00:00:00Z",
        "batch_start_boundary_source": "EXPLICIT_PRE_OUTCOME_BATCH_REGISTRATION_INPUT",
        "eligibility_manifest_schema_sha256": "1" * 64,
        "case_identity_policy_id": "ONE_INCLUDED_CASE_PER_ASKER_PER_BATCH_V01",
        "acquisition_window_days": 365,
        "outcome_followup_days": 90,
        "target_cases_per_topology": 80,
        "primary_topologies": ["JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE"],
        "statistical_preregistration_sha256": canonical_sha256(prereg),
    }


def main():
    contract = load(CONTRACT)
    prereg = load(PREREG)
    validate_batch_registration_contract(copy.deepcopy(contract), copy.deepcopy(prereg))

    source = fixture_input(prereg)
    validate_registration_input(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), True)
    first = bind_batch_registration_candidate(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), fixture_only=True)
    second = bind_batch_registration_candidate(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), fixture_only=True)
    assert first == second, "Batch registration candidate must be deterministic"
    assert first["artifact_kind"] == "P2_BATCH_REGISTRATION_CANDIDATE"
    assert first["production_batch_created"] is False
    assert first["registry_persisted"] is False
    assert first["outcome_data_used"] is False
    assert first["fixture_only"] is True
    assert first["statistical_preregistration_sha256"] == canonical_sha256(prereg)
    assert first["registration_candidate_sha256"] == canonical_sha256({k: v for k, v in first.items() if k != "registration_candidate_sha256"})

    negative_cases = 0

    x = fixture_input(prereg)
    x["outcome"] = "LEAK"
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["batch_start_timestamp_utc"] = "2030-01-01T08:00:00+08:00"
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["batch_start_boundary_source"] = "RUNTIME_NOW"
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["acquisition_window_days"] = 366
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["outcome_followup_days"] = 120
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["target_cases_per_topology"] = 100
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["primary_topologies"].append("ORGANIZATIONAL_RELATIONSHIP")
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["case_identity_policy_id"] = "ALLOW_REPEAT_ASKER"
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = fixture_input(prereg)
    x["statistical_preregistration_sha256"] = "2" * 64
    must_fail(validate_registration_input, x, copy.deepcopy(contract), copy.deepcopy(prereg), True)
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["registration_boundary"]["binder_does_not_create_batch"] = False
    must_fail(validate_batch_registration_contract, x, copy.deepcopy(prereg))
    negative_cases += 1

    x = copy.deepcopy(contract)
    x["production_policy"]["actual_registry_write_not_authorized_by_this_contract"] = False
    must_fail(validate_batch_registration_contract, x, copy.deepcopy(prereg))
    negative_cases += 1

    x = copy.deepcopy(prereg)
    x["statistical_preregistration_ready"] = False
    must_fail(validate_batch_registration_contract, copy.deepcopy(contract), x)
    negative_cases += 1

    production_attempt = fixture_input(prereg)
    production_attempt["batch_id"] = "P2-QRM-PROD-001"
    must_fail(validate_registration_input, production_attempt, copy.deepcopy(contract), copy.deepcopy(prereg), False)
    negative_cases += 1

    assert negative_cases == 13
    print(
        "k2-qimen-p2-batch-registration-tests: PASS "
        "negative_cases=13 fixture_only=true deterministic=true production_batch_created=false registry_persisted=false "
        "batch_registration_machinery_ready=true batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
