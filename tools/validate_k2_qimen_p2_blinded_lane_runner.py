#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_BLINDED_LANE_RUNNER_CONTRACT_V01.json"
V08_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V08.json"
IMPL_V04_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V04.json"
RUNNER_PATH = ROOT / "tools/k2_qimen_p2_blinded_lane_runner.py"


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fail_first_contract():
    contract = load(CONTRACT_PATH)
    v08 = load(V08_PATH)
    impl = load(IMPL_V04_PATH)
    require(contract.get("capability") == "P2-EXEC-006", "capability drift")
    require(contract.get("status") == "ACTIVE_FAIL_FIRST_CONTRACT", "contract status drift")
    require(contract.get("failure_policy") == "FAIL_CLOSED", "runner must fail closed")
    require(contract["blinding_contract"].get("worker_receives_blind_id_not_lane_id") is True, "worker blinding missing")
    require(contract["blinding_contract"].get("identity_map_stored_separately") is True, "separate identity map missing")
    require(contract["isolation_contract"].get("shared_mutable_state_forbidden") is True, "shared mutable state guard missing")
    require(contract["isolation_contract"].get("order_invariance_required") is True, "order invariance missing")
    require(contract["input_snapshot_contract"].get("canonical_sha256_required") is True, "snapshot hash binding missing")
    require(v08.get("open_execution_blockers", [None])[0] == "P2-EXEC-006", "V08 next blocker drift")
    require(impl.get("open_blockers", [None])[0] == "P2-EXEC-006", "V04 next blocker drift")
    require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    require(contract.get("empirical_credit") == "NONE" and contract.get("claim_extraction") == "BLOCKED", "epistemic guard drift")
    require(not RUNNER_PATH.exists(), "fail-first runner unexpectedly exists")
    print("k2-qimen-p2-blinded-lane-runner-contract: FAIL_FIRST_READY runner_missing=true")


if __name__ == "__main__":
    validate_fail_first_contract()
