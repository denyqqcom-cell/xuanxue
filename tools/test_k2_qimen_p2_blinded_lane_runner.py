#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from k2_qimen_p2_blinded_lane_runner import (
    LaneIsolationError,
    build_blinded_plan,
    canonical_sha256,
    execute_blinded,
    validate_runner_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT = json.loads((K / "K2_QIMEN_P2_BLINDED_LANE_RUNNER_CONTRACT_V01.json").read_text(encoding="utf-8"))
FIXTURE = json.loads((ROOT / "tools/testdata/qimen_p2_blinded_lane_runner_fixture.json").read_text(encoding="utf-8"))


def expect_fail(fn, contains):
    try:
        fn()
    except LaneIsolationError as exc:
        assert contains in str(exc), (contains, str(exc))
        return
    raise AssertionError(f"expected LaneIsolationError containing {contains!r}")


def main():
    validate_runner_contract(CONTRACT)
    plan = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    out = execute_blinded(plan)
    assert len(out["execution_log"]) == 3
    assert set(out["identity_map"].values()) == {"P2-A", "P2-A_PRIME", "P2-B"}
    assert all("P2-" not in json.dumps(row, sort_keys=True) for row in out["execution_log"])
    assert all(row["input_snapshot_sha256"] == canonical_sha256(plan["snapshots"][row["blind_id"]]) for row in out["execution_log"])

    c = copy.deepcopy(CONTRACT); c["isolation_contract"]["shared_mutable_state_forbidden"] = False
    expect_fail(lambda: validate_runner_contract(c), "shared mutable")
    c = copy.deepcopy(CONTRACT); c["isolation_contract"]["cross_lane_cache_forbidden"] = False
    expect_fail(lambda: validate_runner_contract(c), "cross-lane cache")
    c = copy.deepcopy(CONTRACT); c["blinding_contract"]["worker_must_not_receive_identity_map"] = False
    expect_fail(lambda: validate_runner_contract(c), "identity map")
    c = copy.deepcopy(CONTRACT); c["blinding_contract"]["execution_logs_must_not_contain_lane_id"] = False
    expect_fail(lambda: validate_runner_contract(c), "lane identity")
    c = copy.deepcopy(CONTRACT); c["randomization_contract"]["order_must_not_depend_on_lane_output"] = False
    expect_fail(lambda: validate_runner_contract(c), "lane output")
    c = copy.deepcopy(CONTRACT); c["randomization_contract"]["order_must_not_depend_on_outcome"] = False
    expect_fail(lambda: validate_runner_contract(c), "outcome")

    bad_payloads = copy.deepcopy(FIXTURE["lane_payloads"]); bad_payloads["P2-B"]["question_id"] = "other-question"
    expect_fail(lambda: build_blinded_plan(bad_payloads, FIXTURE["execution_order_seed"]), "question identity")

    bad_payloads = copy.deepcopy(FIXTURE["lane_payloads"]); bad_payloads["P2-A"]["lane_id"] = "P2-A"
    expect_fail(lambda: build_blinded_plan(bad_payloads, FIXTURE["execution_order_seed"]), "lane identity")

    plan2 = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    first = plan2["execution_order"][0]
    plan2["snapshots"][first]["payload"]["fixture_signal"] = 999
    expect_fail(lambda: execute_blinded(plan2), "snapshot hash")

    plan3 = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    plan3["worker_context"] = {"identity_map": plan3["identity_map"]}
    expect_fail(lambda: execute_blinded(plan3), "identity map")

    plan4 = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    plan4["shared_mutable_state"] = {"cache": {}}
    expect_fail(lambda: execute_blinded(plan4), "shared mutable")

    plan_peer = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    plan_peer["worker_context"] = {"lane_peer_output": {"blind_id": "BLIND-002"}}
    expect_fail(lambda: execute_blinded(plan_peer), "peer output")

    plan5 = build_blinded_plan(FIXTURE["lane_payloads"], FIXTURE["execution_order_seed"])
    plan5["execution_order"] = list(reversed(plan5["execution_order"]))
    out5 = execute_blinded(plan5)
    a = {r["blind_id"]: r["output_sha256"] for r in out["execution_log"]}
    b = {r["blind_id"]: r["output_sha256"] for r in out5["execution_log"]}
    assert a == b, "execution order changed lane outputs"

    print("k2-qimen-p2-blinded-lane-runner-tests: PASS negative_cases=12 lanes=3")


if __name__ == "__main__":
    main()
