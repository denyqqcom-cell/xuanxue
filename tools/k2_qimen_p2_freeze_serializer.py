#!/usr/bin/env python3
import copy
import hashlib
import json
import re

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_FIELDS = {
    "outcome",
    "outcome_value",
    "observed_outcome",
    "feedback",
    "score",
    "winner_lane",
    "post_feedback_edit",
    "runtime_timestamp",
    "now",
    "current_time",
    "persist",
    "output_path",
}
FREEZE_KEYS = {
    "schema_version",
    "artifact_kind",
    "plan_id",
    "hypothesis_id",
    "execution_contract_sha256",
    "mapping_boundary",
    "lane_bindings",
    "estimand_lock",
    "shared_representation",
    "complexity_budget",
    "blinding",
    "denominator_policy",
    "reproducibility_fixture_hash",
    "research_only",
    "outcome_data_used",
}
LANE_EXPECTATIONS = (
    (
        "P2-A",
        "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01",
        "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY",
        "FIXED_GLOBAL",
        ["奇仪", "八门", "八神", "九星"],
    ),
    (
        "P2-A_PRIME",
        "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01",
        "QUESTION_TOPOLOGY_CONDITIONED",
        "FIXED_GLOBAL",
        ["奇仪", "八门", "八神", "九星"],
    ),
    (
        "P2-B",
        "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01",
        "QUESTION_TOPOLOGY_CONDITIONED",
        "QUESTION_TOPOLOGY_CONDITIONED",
        None,
    ),
)
ESTIMAND_LOCK = {
    "P2-C1": {
        "candidate": "P2-A_PRIME",
        "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_POLICY",
        "all_other_dimensions_equal": True,
        "credit_scope": "TOPOLOGY_ROLE_BINDING_ONLY",
    },
    "P2-C2": {
        "candidate": "P2-B",
        "comparator": "P2-A_PRIME",
        "only_allowed_difference": "LAYER_PRIORITY_POLICY",
        "all_other_dimensions_equal": True,
        "credit_scope": "TOPOLOGY_CONDITIONED_LAYER_PRIORITY_ONLY",
    },
    "P2-C3": {
        "candidate": "P2-B",
        "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_PLUS_LAYER_PRIORITY",
        "component_credit_forbidden": True,
        "credit_scope": "FULL_BUNDLE_ONLY_NOT_COMPONENT_ATTRIBUTION",
    },
}


class FreezeSerializationError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise FreezeSerializationError(message)


def _walk(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield ("key", str(key))
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)
    else:
        yield ("value", value)


def _reject_floats(value, label):
    for kind, item in _walk(value):
        if kind == "value" and isinstance(item, float):
            raise FreezeSerializationError(f"{label} contains float")


def _reject_forbidden_fields(value, label):
    bad = sorted(
        item.lower()
        for kind, item in _walk(value)
        if kind == "key" and item.lower() in FORBIDDEN_FIELDS
    )
    _require(not bad, f"{label} contains forbidden field(s): {bad}")


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_bytes(value):
    _reject_floats(value, "canonical value")
    return canonical_json(value).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _require_sha256(value, label):
    _require(isinstance(value, str) and SHA256_RE.fullmatch(value) is not None, f"{label} must be sha256")


def validate_contract(contract):
    _require(contract.get("capability") == "P2-EXEC-009", "capability drift")
    _require(contract.get("failure_policy") == "FAIL_CLOSED", "serializer must fail closed")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    boundary = contract.get("serializer_boundary", {})
    _require(boundary.get("serializer_is_pure") is True, "serializer must be pure")
    _require(boundary.get("serializer_does_not_create_batch") is True, "serializer must not create Batch")
    _require(boundary.get("serializer_does_not_persist_freeze") is True, "serializer must not persist Freeze")
    _require(boundary.get("production_freeze_requires_preexisting_batch") is True, "preexisting Batch required")
    _require(boundary.get("batch_binding_included_in_serialized_bytes") is True, "batch binding must be serialized")
    canon = contract.get("canonicalization", {})
    _require(canon.get("encoding") == "UTF-8", "encoding drift")
    _require(canon.get("json_sort_keys") is True, "sort_keys required")
    _require(canon.get("separators") == [",", ":"], "compact separators required")
    _require(canon.get("ensure_ascii") is False, "ensure_ascii must remain false")
    _require(canon.get("floats_forbidden") is True, "floats must be forbidden")
    _require(canon.get("hash_algorithm") == "SHA256", "hash algorithm drift")
    imm = contract.get("immutability", {})
    _require(imm.get("verification_recomputes_sha256_over_exact_bytes") is True, "exact byte verification required")
    _require(imm.get("any_byte_mutation_invalidates") is True, "mutation invalidation required")
    _require(set(contract.get("forbidden_fields", [])) == FORBIDDEN_FIELDS, "forbidden field set drift")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def _validate_generator(generator, expected_lane):
    required = {
        "generator_id",
        "lane_id",
        "version",
        "implementation_ref",
        "implementation_sha256",
        "canonical_input_schema_sha256",
        "canonical_output_schema_sha256",
        "nondeterminism_policy",
        "seed",
    }
    _require(set(generator) == required, f"{expected_lane} generator shape drift")
    _require(generator.get("lane_id") == expected_lane, f"{expected_lane} generator lane drift")
    _require(isinstance(generator.get("generator_id"), str) and generator["generator_id"], "generator id required")
    _require(isinstance(generator.get("version"), str) and generator["version"], "generator version required")
    _require(isinstance(generator.get("implementation_ref"), str) and generator["implementation_ref"].startswith("tools/") and generator["implementation_ref"].endswith(".py"), "generator ref drift")
    for key in ("implementation_sha256", "canonical_input_schema_sha256", "canonical_output_schema_sha256"):
        _require_sha256(generator.get(key), f"{expected_lane} {key}")
    policy = generator.get("nondeterminism_policy")
    _require(policy in {"DETERMINISTIC", "SEEDED"}, "generator nondeterminism policy drift")
    if policy == "DETERMINISTIC":
        _require(generator.get("seed") is None, "deterministic generator seed must be null")
    else:
        _require(isinstance(generator.get("seed"), int) and not isinstance(generator.get("seed"), bool), "seeded generator seed must be integer")


def _validate_payload(payload, expected_reproducibility_fixture_hash=None):
    _require(isinstance(payload, dict), "freeze payload must be object")
    _require(set(payload) == FREEZE_KEYS, "freeze payload shape drift")
    _reject_floats(payload, "freeze payload")
    _reject_forbidden_fields(payload, "freeze payload")
    _require(payload.get("schema_version") == "0.1", "freeze schema version drift")
    _require(payload.get("artifact_kind") == "P2_EXECUTION_FREEZE", "freeze artifact kind drift")
    _require(payload.get("plan_id") == "K2PV-QRM-002", "freeze plan drift")
    _require(payload.get("hypothesis_id") == "QRM-H1", "freeze hypothesis drift")
    _require_sha256(payload.get("execution_contract_sha256"), "execution contract hash")
    mapping = payload.get("mapping_boundary", {})
    _require(mapping == {"mapping_before_plate_value_access": True, "plate_value_access_before_mapping": False}, "mapping boundary drift")

    lanes = payload.get("lane_bindings")
    _require(isinstance(lanes, list) and len(lanes) == 3, "exactly three lane bindings required")
    for lane, expected in zip(lanes, LANE_EXPECTATIONS):
        lane_id, model_name, role_policy, layer_policy, fixed_priority = expected
        required = {
            "lane_id",
            "model_name",
            "role_binding_policy",
            "layer_priority_policy",
            "fixed_layer_priority",
            "generator",
        }
        _require(isinstance(lane, dict) and set(lane) == required, f"{lane_id} lane shape drift")
        _require(lane.get("lane_id") == lane_id, "lane order/id drift")
        _require(lane.get("model_name") == model_name, f"{lane_id} model drift")
        _require(lane.get("role_binding_policy") == role_policy, f"{lane_id} role policy drift")
        _require(lane.get("layer_priority_policy") == layer_policy, f"{lane_id} layer policy drift")
        _require(lane.get("fixed_layer_priority") == fixed_priority, f"{lane_id} fixed priority drift")
        _validate_generator(lane.get("generator", {}), lane_id)

    _require(payload.get("estimand_lock") == ESTIMAND_LOCK, "estimand lock drift")
    rep = payload.get("shared_representation", {})
    rep_keys = {
        "world_variable_manifest_sha256",
        "symbol_vocabulary_sha256",
        "feature_extraction_manifest_sha256",
        "eligible_rule_pool_sha256",
        "prediction_schema_sha256",
    }
    _require(set(rep) == rep_keys, "shared representation shape drift")
    for key in sorted(rep_keys):
        _require_sha256(rep.get(key), key)

    budget = payload.get("complexity_budget", {})
    budget_keys = {
        "role_multiplicity_budget",
        "reasoning_branch_budget",
        "rule_trace_budget",
        "interpreter_information_budget",
        "tool_access_budget",
    }
    _require(set(budget) == budget_keys, "complexity budget shape drift")
    for key in sorted(budget_keys):
        value = budget.get(key)
        _require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"{key} must be non-negative integer")

    blinding = payload.get("blinding", {})
    _require(set(blinding) == {"lane_blinding_protocol", "lane_order_seed", "cross_lane_isolation_policy"}, "blinding shape drift")
    _require(isinstance(blinding.get("lane_blinding_protocol"), str) and blinding["lane_blinding_protocol"], "blinding protocol required")
    _require(isinstance(blinding.get("lane_order_seed"), int) and not isinstance(blinding.get("lane_order_seed"), bool), "lane order seed must be integer")
    _require(isinstance(blinding.get("cross_lane_isolation_policy"), str) and blinding["cross_lane_isolation_policy"], "isolation policy required")

    denominator = payload.get("denominator_policy", {})
    _require(set(denominator) == {"primary_denominator_policy", "abstention_scoring_policy", "technical_unevaluable_policy"}, "denominator policy shape drift")
    for key in sorted(denominator):
        _require(isinstance(denominator[key], str) and denominator[key], f"{key} required")

    _require_sha256(payload.get("reproducibility_fixture_hash"), "reproducibility fixture hash")
    if expected_reproducibility_fixture_hash is not None:
        _require(payload.get("reproducibility_fixture_hash") == expected_reproducibility_fixture_hash, "reproducibility fixture hash mismatch")
    _require(payload.get("research_only") is True, "research_only must remain true")
    _require(payload.get("outcome_data_used") is False, "outcome data must remain unused")


def validate_document(document, contract, expected_reproducibility_fixture_hash=None):
    validate_contract(contract)
    _require(isinstance(document, dict), "serializer input must be object")
    allowed = {"fixture_id", "fixture_only", "production_freeze_created", "purpose", "batch_binding", "freeze_payload"}
    _require(set(document).issubset(allowed), "serializer input contains unsupported field")
    _require({"fixture_only", "production_freeze_created", "batch_binding", "freeze_payload"}.issubset(document), "serializer input missing required field")
    _reject_floats(document, "serializer input")
    _reject_forbidden_fields(document, "serializer input")
    _require(document.get("production_freeze_created") is False, "serializer cannot accept/create persisted Freeze")

    fixture_only = document.get("fixture_only")
    _require(isinstance(fixture_only, bool), "fixture_only must be boolean")
    batch = document.get("batch_binding", {})
    required_batch = {"batch_id", "batch_ref", "batch_sha256", "batch_created", "production_batch"}
    _require(isinstance(batch, dict) and set(batch) == required_batch, "batch binding shape drift")
    _require(isinstance(batch.get("batch_id"), str) and batch["batch_id"], "batch id required")
    _require(isinstance(batch.get("batch_ref"), str) and batch["batch_ref"], "batch ref required")
    _require("K2_PROSPECTIVE_FREEZES" not in batch["batch_ref"], "batch ref cannot point at Freeze registry")
    _require_sha256(batch.get("batch_sha256"), "batch sha256")
    _require(batch.get("batch_created") is True, "Freeze serialization requires preexisting Batch binding")
    _require(isinstance(batch.get("production_batch"), bool), "production_batch must be boolean")
    if fixture_only:
        _require(batch.get("production_batch") is False, "fixture may bind synthetic Batch only")
        _require(isinstance(document.get("fixture_id"), str) and document["fixture_id"], "fixture_id required in fixture mode")
    else:
        _require(batch.get("production_batch") is True, "production candidate requires production Batch")
    _validate_payload(document.get("freeze_payload"), expected_reproducibility_fixture_hash)


def _envelope_from_document(document, contract):
    mode = "FIXTURE_ONLY" if document["fixture_only"] else "PRODUCTION_CANDIDATE"
    payload = copy.deepcopy(document["freeze_payload"])
    return {
        "serializer_contract_id": contract["contract_id"],
        "serializer_version": contract["version"],
        "mode": mode,
        "batch_binding": copy.deepcopy(document["batch_binding"]),
        "freeze_payload": payload,
        "freeze_payload_sha256": canonical_sha256(payload),
        "production_freeze_created": False,
    }


def serialize_freeze_candidate(document, contract, expected_reproducibility_fixture_hash=None):
    validate_document(document, contract, expected_reproducibility_fixture_hash)
    envelope = _envelope_from_document(document, contract)
    raw = canonical_bytes(envelope)
    return raw, hashlib.sha256(raw).hexdigest()


def verify_serialized_freeze(raw, expected_sha256, contract, expected_reproducibility_fixture_hash=None):
    _require(isinstance(raw, (bytes, bytearray)), "serialized Freeze must be bytes")
    raw = bytes(raw)
    _require_sha256(expected_sha256, "expected serialized sha256")
    _require(hashlib.sha256(raw).hexdigest() == expected_sha256, "serialized Freeze byte hash mismatch")
    try:
        decoded = raw.decode("utf-8")
        envelope = json.loads(decoded)
    except Exception as exc:
        raise FreezeSerializationError(f"serialized Freeze decode failure: {exc}") from exc
    _require(canonical_bytes(envelope) == raw, "serialized Freeze bytes are not canonical")
    _require(isinstance(envelope, dict), "serialized Freeze envelope must be object")
    required = {
        "serializer_contract_id",
        "serializer_version",
        "mode",
        "batch_binding",
        "freeze_payload",
        "freeze_payload_sha256",
        "production_freeze_created",
    }
    _require(set(envelope) == required, "serialized Freeze envelope shape drift")
    _require(envelope.get("serializer_contract_id") == contract.get("contract_id"), "serializer contract id drift")
    _require(envelope.get("serializer_version") == contract.get("version"), "serializer version drift")
    _require(envelope.get("mode") in {"FIXTURE_ONLY", "PRODUCTION_CANDIDATE"}, "serializer mode drift")
    _require(envelope.get("production_freeze_created") is False, "serializer cannot persist Freeze")
    _require(envelope.get("freeze_payload_sha256") == canonical_sha256(envelope.get("freeze_payload")), "freeze payload hash drift")
    document = {
        "fixture_only": envelope["mode"] == "FIXTURE_ONLY",
        "production_freeze_created": False,
        "batch_binding": envelope["batch_binding"],
        "freeze_payload": envelope["freeze_payload"],
    }
    if document["fixture_only"]:
        document["fixture_id"] = "VERIFIED-SERIALIZED-FIXTURE"
    validate_document(document, contract, expected_reproducibility_fixture_hash)
    return envelope
