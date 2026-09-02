#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_role_layer_generators as role_validator
from k2_qimen_p2_budget_enforcer import (
    enforce_budget,
    freeze_budget,
    validate_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_complexity_budget_fixture.json"
V03_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V03.json"
V04_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V04.json"
V07_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V07.json"
ENFORCER_PATH = ROOT / "tools" / "k2_qimen_p2_budget_enforcer.py"
TEST_PATH = ROOT / "tools" / "test_k2_qimen_p2_budget_enforcer.py"
V08_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V08.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "ae54cb165af4c5ed999b24fad425e18051e0379809b6cbec816cd839be68439a"
EXPECTED_V03_BLOB = "dd626fc6c7726487839b3353c72e3d58f1abc57b"
EXPECTED_V07_BLOB = "a590d381c17d083049afb508b6cf1435089b02e4"
EXPECTED_CONTRACT_BLOB = "458522d22c9f63cf92d58b2fe541fa4335b89ef9"
EXPECTED_ENFORCER_BLOB = "c46255e8bc59daa4e8ab2ff683e9ab0378bb0d2e"
EXPECTED_TEST_BLOB = "904d7a09321c13a9f909160bed9168486bed3ab3"
EXPECTED_FIXTURE_BLOB = "332de7b78d68d4b2e1b45bbd2aa2b3d4a05aa6e2"
FAIL_FIRST_COMMIT = "dd7aa28254331a30bee84ed253f4e8e041df0525"
FAIL_FIRST_RUN = 33589374396
FAIL_FIRST_JOB = 100120051816


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


def canonical_sha256(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def git_blob_sha1(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate_repository():
    # Successor validation deliberately re-runs the entire P2-EXEC-004 validator.
    # That validator re-reads the Wave1/deep/work-family distillates, Shantiadao
    # acceptance and Qimen TBV state; therefore the source-local audit is live,
    # not a hand-written PASS carried forward from V03/V07.
    role_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    v03 = load_json(V03_PATH)
    v04 = load_json(V04_PATH)
    v07 = load_json(V07_PATH)
    v08 = load_json(V08_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(V03_PATH) == EXPECTED_V03_BLOB, "V03 historical blob drift")
    require(git_blob_sha1(V07_PATH) == EXPECTED_V07_BLOB, "V07 historical blob drift")
    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "budget contract blob drift")
    require(git_blob_sha1(ENFORCER_PATH) == EXPECTED_ENFORCER_BLOB, "budget enforcer blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "budget test blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "budget fixture blob drift")
    require(contract.get("contract_id") == "K2-QIMEN-P2-COMPLEXITY-BUDGET-CONTRACT-V01", "budget contract id drift")
    require(contract.get("capability") == "P2-EXEC-005", "budget capability drift")
    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "budget contract canonical hash drift")
    validate_contract(contract)

    frozen = freeze_budget(
        fixture["pre_freeze_budget_input"],
        fixture["budget_profile"],
        contract,
    )
    result = enforce_budget(frozen, fixture["pre_freeze_budget_input"], contract)
    require(result.get("decision") == "ALLOW" and result.get("over_budget") is False, "fixture budget decision drift")
    require(
        len({row["total_units"] for row in result["per_lane"]}) == 1,
        "lane complexity formula asymmetry",
    )
    require(frozen.get("budget_frozen_before_mapping") is True, "budget must freeze before Role Map freeze")
    require(frozen.get("outcome_data_used") is False, "budget enforcer accessed outcome data")

    require(v04.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V04", "V04 id drift")
    require(v04.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V03.json", "V04 must append V03")
    require(v04.get("closed_blockers", [])[-1].get("blocker_id") == "P2-EXEC-005", "V04 blocker closure drift")
    require(v04.get("open_blockers") == ["P2-EXEC-006","P2-EXEC-007","P2-EXEC-008","P2-EXEC-009"], "V04 open blocker drift")
    require(v04.get("execution_substrate_ready") is False, "P2 substrate cannot be ready before 006..009")
    require(v04.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V04 source-local audit marker drift")

    require(v08.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V08", "V08 id drift")
    require(v08.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V07", "V08 must append V07")
    require(v08.get("closed_execution_blockers") == [
        "P2-EXEC-001","P2-EXEC-002","P2-EXEC-003","P2-EXEC-004","P2-EXEC-005"
    ], "V08 closed blockers drift")
    require(v08.get("open_execution_blockers") == [
        "P2-EXEC-006","P2-EXEC-007","P2-EXEC-008","P2-EXEC-009"
    ], "V08 open blockers drift")
    require(v08.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V08 source-local audit marker drift")

    for obj, label in ((contract, "contract"), (v04, "V04"), (v08, "V08")):
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
        "P2 Freeze exists before execution substrate closure",
    )

    evidence = v04.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit evidence drift")
    require(evidence.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run evidence drift")
    require(evidence.get("job_id") == FAIL_FIRST_JOB, "fail-first job evidence drift")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-complexity-budget: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-complexity-budget: PASS")
    print(
        "closed=P2-EXEC-001..005 open=P2-EXEC-006..009 "
        "negative_cases=11 source_local_overgeneralization=PASS "
        "execution_substrate_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
