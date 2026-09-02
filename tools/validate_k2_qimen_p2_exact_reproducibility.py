#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_abstain_denominator_scorer as scorer_validator
from k2_qimen_p2_exact_reproducibility import (
    canonical_sha256,
    fixture_sha256,
    run_pipeline,
    validate_contract,
    validate_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_EXACT_REPRODUCIBILITY_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_exact_reproducibility_fixture.json"
PIPELINE_PATH = ROOT / "tools" / "k2_qimen_p2_exact_reproducibility.py"
TEST_PATH = ROOT / "tools" / "test_k2_qimen_p2_exact_reproducibility.py"
V06_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V06.json"
V07_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V07.json"
V10_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V10.json"
V11_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V11.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "17473e7d22f187eb7ca3a76de82edc160d24cdae919b1c4f27109ac60f5c889b"
EXPECTED_FIXTURE_HASH = "88968c2388163efa009640ba91c9a67b68049fcbb573d86ed725a319c3130977"
EXPECTED_REPORT_HASH = "d486819250c8690b9d205894b17522b58fcc266bec354252752c31e9bec646df"
EXPECTED_CONTRACT_BLOB = "003691db6c6d6f361fe172452cda65b49bcaf9f4"
EXPECTED_FIXTURE_BLOB = "481353248fbfab51528393e73bd03f62251994e7"
EXPECTED_PIPELINE_BLOB = "e6aed9cb523c35ae03a11d346911aa2fd8d8a00a"
EXPECTED_TEST_BLOB = "a843c952da859768b0aaddd9af159ca565f043ce"
EXPECTED_V06_BLOB = "e0d00b5c15f5ff659186212f8f1fb578c4722868"
EXPECTED_V10_BLOB = "002ef0782e15cb78caf83cb6e3db274f26ea63a9"
FAIL_FIRST_COMMIT = "d7992f90ce107f05020945f2746edfab394eacd8"
FAIL_FIRST_RUN = 33591871889
FAIL_FIRST_JOB = 100127354747


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be object: {path}")
    return value


def load_jsonl(path):
    if not path.exists():
        return []
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            value = json.loads(raw)
            require(isinstance(value, dict), f"JSONL row must be object: {path}")
            rows.append(value)
    return rows


def git_blob_sha1(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate_repository():
    scorer_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    v06 = load_json(V06_PATH)
    v07 = load_json(V07_PATH)
    v10 = load_json(V10_PATH)
    v11 = load_json(V11_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(V06_PATH) == EXPECTED_V06_BLOB, "V06 historical blob drift")
    require(git_blob_sha1(V10_PATH) == EXPECTED_V10_BLOB, "V10 historical blob drift")
    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "reproducibility contract blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "reproducibility fixture blob drift")
    require(git_blob_sha1(PIPELINE_PATH) == EXPECTED_PIPELINE_BLOB, "reproducibility pipeline blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "reproducibility test blob drift")

    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "reproducibility contract canonical hash drift")
    validate_contract(contract)
    validate_fixture(fixture, contract)
    require(fixture_sha256(fixture) == EXPECTED_FIXTURE_HASH, "reproducibility fixture canonical hash drift")

    first = run_pipeline(fixture, contract, expected_fixture_sha256=EXPECTED_FIXTURE_HASH)
    second = run_pipeline(fixture, contract, expected_fixture_sha256=EXPECTED_FIXTURE_HASH)
    require(first == second, "same frozen input did not reproduce byte-exact report")
    report_hash = hashlib.sha256(first).hexdigest()
    require(report_hash == EXPECTED_REPORT_HASH, "reproducibility report sha256 drift")

    require(v07.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V07", "V07 id drift")
    require(v07.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V06.json", "V07 must append V06")
    require(v07.get("closed_blockers", [])[-1].get("blocker_id") == "P2-EXEC-008", "V07 blocker closure drift")
    require(v07.get("open_blockers") == ["P2-EXEC-009"], "V07 open blocker drift")
    require(v07.get("execution_substrate_ready") is False, "P2 substrate cannot be ready before 009")
    require(v07.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V07 source-local audit marker drift")
    require(v07.get("reproducibility_semantics", {}).get("expected_report_sha256") == EXPECTED_REPORT_HASH, "V07 report hash drift")
    require(v07.get("reproducibility_semantics", {}).get("boundary_fixture_values_are_calendar_correctness_claims") is False, "V07 boundary sentinel claim drift")

    require(v11.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V11", "V11 id drift")
    require(v11.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V10", "V11 must append V10")
    require(v11.get("closed_execution_blockers") == [
        "P2-EXEC-001","P2-EXEC-002","P2-EXEC-003","P2-EXEC-004",
        "P2-EXEC-005","P2-EXEC-006","P2-EXEC-007","P2-EXEC-008"
    ], "V11 closed blockers drift")
    require(v11.get("open_execution_blockers") == ["P2-EXEC-009"], "V11 open blocker drift")
    require(v11.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V11 source-local audit marker drift")
    require(v11.get("exact_reproducibility_boundary", {}).get("boundary_sentinels_validate_calendar_or_qimen_correctness") is False, "V11 boundary semantics overclaim")

    for obj, label in ((contract, "contract"), (v07, "V07"), (v11, "V11")):
        require(obj.get("batch") == "NONE", f"{label} batch must remain NONE")
        require(obj.get("freeze") == "NONE", f"{label} freeze must remain NONE")
        require(obj.get("outcome") == "NONE", f"{label} outcome must remain NONE")
        require(obj.get("empirical_credit") == "NONE", f"{label} empirical credit must remain NONE")
        require(obj.get("claim_extraction") == "BLOCKED", f"{label} claim extraction must remain BLOCKED")

    require(
        not [x for x in batches if x.get("plan_id") == "K2PV-QRM-002" or x.get("hypothesis_id") == "QRM-H1"],
        "P2 Batch exists before execution substrate closure",
    )
    require(
        not [x for x in freezes if x.get("plan_id") == "K2PV-QRM-002"],
        "P2 Freeze exists before P2-EXEC-009 closure",
    )

    evidence = v07.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit evidence drift")
    require(evidence.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run evidence drift")
    require(evidence.get("job_id") == FAIL_FIRST_JOB, "fail-first job evidence drift")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-exact-reproducibility: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-exact-reproducibility: PASS")
    print(
        "closed=P2-EXEC-001..008 open=P2-EXEC-009 "
        "negative_cases=16 boundary_cases=4 byte_exact=true "
        "source_local_overgeneralization=PASS execution_substrate_ready=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
