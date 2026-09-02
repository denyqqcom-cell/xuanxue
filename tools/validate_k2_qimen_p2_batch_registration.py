#!/usr/bin/env python3
import copy
import json
import subprocess
from pathlib import Path

from k2_qimen_p2_batch_registration import (
    bind_batch_registration_candidate,
    canonical_sha256,
    validate_batch_registration_contract,
    validate_registration_input,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
T = ROOT / "tools"

EXPECTED_BLOBS = {
    K / "K2_QIMEN_P2_BATCH_REGISTRATION_CONTRACT_V01.json": "f092bffe03faccfbf145f8d4eb60f410910c3a54",
    T / "k2_qimen_p2_batch_registration.py": "04f3d6fb6bf946f7e6a804d51f22e680a171782f",
    T / "test_k2_qimen_p2_batch_registration.py": "c4594dd72019f0a86a35ca4fa1eb2d2c3ae7da2c",
    K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V17.json": "2e92116a825b74ceb51d5b34ad7692a83dd7e952",
    K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V21.json": "e55abbf8b5e7e8225b90b4996276b155dc57ada4",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def git_blob(path):
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


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
    contract = load(K / "K2_QIMEN_P2_BATCH_REGISTRATION_CONTRACT_V01.json")
    prereg = load(K / "K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_V01.json")
    implementation = load(K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V17.json")
    protocol = load(K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V21.json")

    validate_batch_registration_contract(copy.deepcopy(contract), copy.deepcopy(prereg))
    source = fixture_input(prereg)
    validate_registration_input(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), True)
    first = bind_batch_registration_candidate(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), True)
    second = bind_batch_registration_candidate(copy.deepcopy(source), copy.deepcopy(contract), copy.deepcopy(prereg), True)
    require(first == second, "Batch registration fixture is not deterministic")
    require(first.get("fixture_only") is True, "fixture_only marker drift")
    require(first.get("production_batch_created") is False, "fixture created production Batch")
    require(first.get("registry_persisted") is False, "fixture persisted registry")
    require(first.get("outcome_data_used") is False, "fixture used outcome data")
    require(first.get("statistical_preregistration_sha256") == canonical_sha256(prereg), "preregistration content hash binding drift")
    payload = {k: v for k, v in first.items() if k != "registration_candidate_sha256"}
    require(first.get("registration_candidate_sha256") == canonical_sha256(payload), "candidate digest drift")

    for path, expected in EXPECTED_BLOBS.items():
        require(path.exists(), f"missing Batch-registration closure artifact: {path.relative_to(ROOT)}")
        require(git_blob(path) == expected, f"git blob drift: {path.relative_to(ROOT)}")

    require(implementation.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V17", "implementation id drift")
    gate = implementation.get("p2_prebatch_batch_005", {})
    require(gate.get("status") == "CLOSED_BATCH_REGISTRATION_MACHINERY_ONLY", "Batch-registration machinery closure missing")
    require(gate.get("binder_pure") is True and gate.get("binder_does_not_persist_registry") is True, "binder purity/persistence guard drift")
    require(gate.get("binder_does_not_create_batch") is True, "binder creation guard drift")
    require(gate.get("production_mode_attempt_fails_closed_without_explicit_future_authorization") is True, "production-mode authorization guard drift")
    require(gate.get("negative_test_count") == 13, "negative test count drift")
    require(implementation.get("statistical_preregistration_ready") is True, "statistical preregistration readiness lost")
    require(implementation.get("batch_registration_machinery_ready") is True, "Batch registration machinery readiness missing")
    require(implementation.get("production_batch_registration_authorized") is False, "production Batch authorization must remain false")
    require(implementation.get("production_batch_registered") is False, "production Batch must remain unregistered")
    require(implementation.get("batch_ready") is False and implementation.get("batch_creation_allowed") is False, "Batch gate unexpectedly opened")

    require(protocol.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V21", "protocol id drift")
    require(protocol.get("status") == "BATCH_REGISTRATION_MACHINERY_CLOSED_AWAIT_EXPLICIT_PRODUCTION_BATCH_AUTHORIZATION", "protocol state drift")
    machinery = protocol.get("batch_registration_machinery", {})
    require(machinery.get("status") == "CLOSED_MACHINERY_ONLY", "protocol machinery closure missing")
    require(machinery.get("pure_deterministic_binder") is True, "protocol deterministic binder guard missing")
    require(machinery.get("registry_persistence_side_effect_forbidden") is True, "protocol registry side-effect guard missing")
    require(machinery.get("runtime_current_time_selection_forbidden") is True, "protocol runtime-now guard missing")
    require(protocol.get("production_batch_registration_authorized") is False, "protocol production Batch authorization must remain false")
    require(protocol.get("production_batch_registered") is False, "protocol production Batch must remain unregistered")
    require(protocol.get("batch_ready") is False and protocol.get("batch_creation_allowed") is False, "protocol Batch gate unexpectedly opened")

    for artifact in (contract, implementation, protocol):
        require(artifact.get("outcome_data_used") is False, "outcome data use detected")
        require(artifact.get("batch") == artifact.get("freeze") == artifact.get("outcome") == "NONE", "Batch/Freeze/Outcome mutation detected")
        require(artifact.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
        require(artifact.get("claim_extraction") == "BLOCKED", "claim extraction must remain blocked")

    print(
        "k2-qimen-p2-batch-registration-validator: PASS "
        "gate=CLOSED_BATCH_REGISTRATION_MACHINERY_ONLY negative_cases=13 deterministic=true fixture_only=true "
        "production_batch_authorized=false production_batch_registered=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
