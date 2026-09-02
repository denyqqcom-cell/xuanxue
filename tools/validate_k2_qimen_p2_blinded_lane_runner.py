#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_budget_enforcer as budget_validator
from k2_qimen_p2_blinded_lane_runner import (
    build_blinded_plan,
    canonical_sha256,
    execute_blinded,
    validate_runner_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_BLINDED_LANE_RUNNER_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools/testdata/qimen_p2_blinded_lane_runner_fixture.json"
RUNNER_PATH = ROOT / "tools/k2_qimen_p2_blinded_lane_runner.py"
TEST_PATH = ROOT / "tools/test_k2_qimen_p2_blinded_lane_runner.py"
V04_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V04.json"
V05_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V05.json"
V08_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V08.json"
V09_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V09.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "9a93bc02a8388651a50fd94423f1c89a36c984582ca4de272cfd118843758a3e"
EXPECTED_CONTRACT_BLOB = "7559ff1a25941f7c25589b275e3d1540200ec809"
EXPECTED_FIXTURE_BLOB = "0368ef67c989463a52c6a5646f1147d2d58e43e5"
EXPECTED_RUNNER_BLOB = "f827cb26541993a04a11fe435ab51d359f1a2334"
EXPECTED_TEST_BLOB = "6b399f99eb2d8a8241579a99bbae2e0d748c899d"
EXPECTED_V04_BLOB = "b8cba0c1bf45d96f5e52672997d354805acbadbb"
EXPECTED_V08_BLOB = "7833889c2f68b0d81981f3da84560eb9e3dd3fe3"
FAIL_FIRST_COMMIT = "587544036fcc858e7c21ff9879b3f52837d44363"
FAIL_FIRST_RUN = 33590110481
FAIL_FIRST_JOB = 100122199505


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
    # Live successor chain: 005 -> 004 -> Distillate/TBV source-grounding audit.
    budget_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    v04 = load_json(V04_PATH)
    v05 = load_json(V05_PATH)
    v08 = load_json(V08_PATH)
    v09 = load_json(V09_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "runner contract blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "runner fixture blob drift")
    require(git_blob_sha1(RUNNER_PATH) == EXPECTED_RUNNER_BLOB, "runner implementation blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "runner test blob drift")
    require(git_blob_sha1(V04_PATH) == EXPECTED_V04_BLOB, "V04 historical blob drift")
    require(git_blob_sha1(V08_PATH) == EXPECTED_V08_BLOB, "V08 historical blob drift")
    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "runner contract canonical hash drift")
    validate_runner_contract(contract)

    plan = build_blinded_plan(fixture["lane_payloads"], fixture["execution_order_seed"])
    result = execute_blinded(plan)
    require(len(result.get("execution_log", [])) == 3, "runner did not execute three blinded lanes")
    require(result.get("outcome_data_used") is False, "runner used outcome data")
    require(result.get("shared_mutable_state_used") is False, "runner used shared mutable state")
    require(plan.get("identity_map_storage") == "SEPARATE_COORDINATOR_ONLY", "identity map storage drift")
    for row in result["execution_log"]:
        require("P2-" not in json.dumps(row, sort_keys=True), "execution log leaked lane id")
        require(row["input_snapshot_sha256"] == canonical_sha256(plan["snapshots"][row["blind_id"]]), "input snapshot hash drift")

    reversed_plan = build_blinded_plan(fixture["lane_payloads"], fixture["execution_order_seed"])
    reversed_plan["execution_order"] = list(reversed(reversed_plan["execution_order"]))
    reversed_result = execute_blinded(reversed_plan)
    left = {x["blind_id"]: x["output_sha256"] for x in result["execution_log"]}
    right = {x["blind_id"]: x["output_sha256"] for x in reversed_result["execution_log"]}
    require(left == right, "lane output changed with execution order")

    require(v05.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V05", "V05 id drift")
    require(v05.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V04.json", "V05 must append V04")
    require(v05.get("closed_blockers", [])[-1].get("blocker_id") == "P2-EXEC-006", "V05 blocker closure drift")
    require(v05.get("open_blockers") == ["P2-EXEC-007","P2-EXEC-008","P2-EXEC-009"], "V05 open blocker drift")
    require(v05.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V05 source-local audit marker drift")
    require(v05.get("execution_substrate_ready") is False, "P2 substrate cannot be ready before 007..009")

    require(v09.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V09", "V09 id drift")
    require(v09.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V08", "V09 must append V08")
    require(v09.get("closed_execution_blockers") == ["P2-EXEC-001","P2-EXEC-002","P2-EXEC-003","P2-EXEC-004","P2-EXEC-005","P2-EXEC-006"], "V09 closed blockers drift")
    require(v09.get("open_execution_blockers") == ["P2-EXEC-007","P2-EXEC-008","P2-EXEC-009"], "V09 open blockers drift")
    require(v09.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V09 source-local audit marker drift")

    for obj, label in ((contract, "contract"), (v05, "V05"), (v09, "V09")):
        require(obj.get("batch") == "NONE", f"{label} batch must remain NONE")
        require(obj.get("freeze") == "NONE", f"{label} freeze must remain NONE")
        require(obj.get("outcome") == "NONE", f"{label} outcome must remain NONE")
        require(obj.get("empirical_credit") == "NONE", f"{label} empirical credit must remain NONE")
        require(obj.get("claim_extraction") == "BLOCKED", f"{label} claim extraction must remain BLOCKED")

    require(not [x for x in batches if x.get("plan_id") == "K2PV-QRM-002" or x.get("hypothesis_id") == "QRM-H1"], "P2 Batch exists before substrate closure")
    require(not [x for x in freezes if x.get("plan_id") == "K2PV-QRM-002"], "P2 Freeze exists before substrate closure")

    evidence = v05.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit evidence drift")
    require(evidence.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run evidence drift")
    require(evidence.get("job_id") == FAIL_FIRST_JOB, "fail-first job evidence drift")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-blinded-lane-runner: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-blinded-lane-runner: PASS")
    print("closed=P2-EXEC-001..006 open=P2-EXEC-007..009 negative_cases=12 source_local_overgeneralization=PASS execution_substrate_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE")


if __name__ == "__main__":
    main()
