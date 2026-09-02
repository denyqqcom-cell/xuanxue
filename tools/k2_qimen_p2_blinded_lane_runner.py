#!/usr/bin/env python3
import copy
import hashlib
import json

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
BLIND_IDS = ("BLIND-001", "BLIND-002", "BLIND-003")
FORBIDDEN_INPUT_KEYS = {
    "outcome", "feedback", "score", "winner_lane", "control_lane",
    "lane_peer_output", "lane_peer_intermediate_output",
}
SEMANTIC_LABEL_TOKENS = ("control", "baseline", "treatment", "winner", "better_lane")


class LaneIsolationError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise LaneIsolationError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _walk_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


def _reject_forbidden(value, label):
    keys = {k.lower() for k in _walk_keys(value)}
    bad = sorted(keys & FORBIDDEN_INPUT_KEYS)
    _require(not bad, f"{label} contains forbidden field(s): {bad}")


def validate_runner_contract(contract):
    _require(contract.get("capability") == "P2-EXEC-006", "capability drift")
    _require(contract.get("failure_policy") == "FAIL_CLOSED", "runner must fail closed")
    b = contract.get("blinding_contract", {})
    i = contract.get("isolation_contract", {})
    r = contract.get("randomization_contract", {})
    s = contract.get("input_snapshot_contract", {})
    _require(b.get("worker_receives_blind_id_not_lane_id") is True, "worker blinding missing")
    _require(b.get("worker_must_not_receive_identity_map") is True, "worker identity map exposure forbidden")
    _require(b.get("execution_logs_must_not_contain_lane_id") is True, "execution log lane identity must be forbidden")
    _require(b.get("identity_map_stored_separately") is True and b.get("identity_map_not_exposed_to_worker") is True, "identity map must remain separate")
    _require(i.get("shared_mutable_state_forbidden") is True, "shared mutable state must be forbidden")
    _require(i.get("cross_lane_cache_forbidden") is True, "cross-lane cache must be forbidden")
    _require(i.get("peer_intermediate_output_forbidden") is True, "peer intermediate output must be forbidden")
    _require(i.get("fresh_worker_state_per_lane") is True, "fresh worker state required")
    _require(i.get("order_invariance_required") is True, "order invariance required")
    _require(r.get("order_source") == "PRE_FREEZE_EXECUTION_ORDER_SEED", "execution order seed boundary drift")
    _require(r.get("order_must_not_depend_on_lane_output") is True, "execution order must not depend on lane output")
    _require(r.get("order_must_not_depend_on_outcome") is True, "execution order must not depend on outcome")
    _require(r.get("all_three_lanes_exactly_once") is True, "all lanes exactly once required")
    _require(s.get("canonical_sha256_required") is True and s.get("snapshot_immutable_after_bind") is True, "snapshot hash/immutability required")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def build_blinded_plan(lane_payloads, execution_order_seed):
    _require(set(lane_payloads) == set(LANE_IDS), "lane set drift")
    _require(isinstance(execution_order_seed, str) and execution_order_seed, "pre-freeze execution order seed required")
    question_ids = {payload.get("question_id") for payload in lane_payloads.values()}
    _require(len(question_ids) == 1 and None not in question_ids, "same question identity required")
    for lane_id, payload in lane_payloads.items():
        _require(isinstance(payload, dict), f"{lane_id} payload must be object")
        _reject_forbidden(payload, f"{lane_id} snapshot")
        _require("lane_id" not in payload, "lane identity must not be embedded in worker snapshot")

    randomized_lanes = sorted(
        LANE_IDS,
        key=lambda lane: hashlib.sha256(f"{execution_order_seed}|identity|{lane}".encode()).hexdigest(),
    )
    identity_map = {blind_id: lane for blind_id, lane in zip(BLIND_IDS, randomized_lanes)}
    snapshots = {}
    hashes = {}
    for blind_id, lane_id in identity_map.items():
        snap = copy.deepcopy(lane_payloads[lane_id])
        snapshots[blind_id] = snap
        hashes[blind_id] = canonical_sha256(snap)

    execution_order = sorted(
        BLIND_IDS,
        key=lambda blind_id: hashlib.sha256(f"{execution_order_seed}|order|{blind_id}".encode()).hexdigest(),
    )
    return {
        "plan_version": "P2_BLINDED_LANE_PLAN_V01",
        "identity_map": identity_map,
        "identity_map_sha256": canonical_sha256(identity_map),
        "identity_map_storage": "SEPARATE_COORDINATOR_ONLY",
        "execution_order_seed_sha256": hashlib.sha256(execution_order_seed.encode()).hexdigest(),
        "execution_order": execution_order,
        "snapshots": snapshots,
        "snapshot_sha256": hashes,
        "worker_context": {},
    }


def _worker(blind_id, snapshot):
    _reject_forbidden(snapshot, "worker snapshot")
    _require(blind_id in BLIND_IDS, "invalid blind id")
    worker_state = {}
    result = {
        "status": "EXECUTED",
        "question_id": snapshot["question_id"],
        "representation_sha256": snapshot.get("representation_sha256"),
        "mapping_sha256": snapshot.get("mapping_sha256"),
        "budget_decision_sha256": snapshot.get("budget_decision_sha256"),
        "payload_digest": canonical_sha256(snapshot.get("payload")),
        "worker_state_size": len(worker_state),
    }
    _reject_forbidden(result, "worker result")
    text = canonical_json(result).lower()
    _require(not any(token in text for token in SEMANTIC_LABEL_TOKENS), "worker result contains semantic arm label")
    return result


def execute_blinded(plan):
    _require(plan.get("identity_map_storage") == "SEPARATE_COORDINATOR_ONLY", "identity map storage boundary drift")
    context = plan.get("worker_context") or {}
    _require("identity_map" not in context, "worker context exposes identity map")
    _require("lane_peer_output" not in context and "lane_peer_intermediate_output" not in context, "worker context exposes peer output")
    _require("shared_mutable_state" not in plan, "shared mutable state forbidden")
    _require("cross_lane_cache" not in plan, "cross-lane cache forbidden")

    order = plan.get("execution_order")
    _require(isinstance(order, list) and len(order) == 3 and set(order) == set(BLIND_IDS), "execution order must contain each blind lane exactly once")
    snapshots = plan.get("snapshots", {})
    bound_hashes = plan.get("snapshot_sha256", {})
    _require(set(snapshots) == set(BLIND_IDS) == set(bound_hashes), "snapshot set drift")

    execution_log = []
    for blind_id in order:
        snapshot = copy.deepcopy(snapshots[blind_id])
        _require(canonical_sha256(snapshot) == bound_hashes[blind_id], "snapshot hash mismatch after bind")
        result = _worker(blind_id, snapshot)
        row = {
            "blind_id": blind_id,
            "input_snapshot_sha256": bound_hashes[blind_id],
            "output_sha256": canonical_sha256(result),
            "result": result,
        }
        row_text = canonical_json(row)
        _require(not any(lane in row_text for lane in LANE_IDS), "execution log leaks lane identity")
        _require(not any(token in row_text.lower() for token in SEMANTIC_LABEL_TOKENS), "execution log leaks semantic arm label")
        execution_log.append(row)

    return {
        "execution_log": execution_log,
        "identity_map": copy.deepcopy(plan["identity_map"]),
        "identity_map_sha256": plan["identity_map_sha256"],
        "outcome_data_used": False,
        "shared_mutable_state_used": False,
    }
