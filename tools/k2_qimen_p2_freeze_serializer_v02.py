#!/usr/bin/env python3
import copy
import hashlib
import json
import re

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_FIELDS = {
    "outcome", "outcome_value", "observed_outcome", "feedback", "score",
    "winner_lane", "post_feedback_edit", "runtime_timestamp", "now",
    "current_time", "persist", "output_path",
}
PLAN_AMENDMENT_SHA = "d39db1528905b2d008720e2c1f45c2d723ce20aaf1df99c8b7fb7ed132e13de3"
SUBSTRATE_SHA = "bee308bfb52e18829f558d576e6ea581aae0580de625aa6206bdbf84ef5fa3d5"
EXECUTION_CONTRACT_SHA = "218bf3dbc8e83421db34d3d8678a17b93c7e1ed981d28ba70ede02c1c145264b"
REPRESENTATION_CONTRACT_SHA = "1a7128dd4c1ba5846c1d74f78645ff7b1ea87032898bbd83f61859283182393d"
BUDGET_CONTRACT_SHA = "ae54cb165af4c5ed999b24fad425e18051e0379809b6cbec816cd839be68439a"
BLINDING_CONTRACT_SHA = "9a93bc02a8388651a50fd94423f1c89a36c984582ca4de272cfd118843758a3e"
DENOMINATOR_CONTRACT_SHA = "1bf117aff2ab7a54570382292b7c75d6e00fe5e28bbef595f3dcb41c7b288c25"
REPRO_CONTRACT_SHA = "17473e7d22f187eb7ca3a76de82edc160d24cdae919b1c4f27109ac60f5c889b"
REPRO_FIXTURE_SHA = "88968c2388163efa009640ba91c9a67b68049fcbb573d86ed725a319c3130977"
REPRO_REPORT_SHA = "d486819250c8690b9d205894b17522b58fcc266bec354252752c31e9bec646df"

ESTIMAND_LOCK = {
    "P2-C1": {"candidate": "P2-A_PRIME", "comparator": "P2-A", "only_allowed_difference": "ROLE_BINDING_POLICY", "all_other_dimensions_equal": True, "credit_scope": "TOPOLOGY_ROLE_BINDING_ONLY"},
    "P2-C2": {"candidate": "P2-B", "comparator": "P2-A_PRIME", "only_allowed_difference": "LAYER_PRIORITY_POLICY", "all_other_dimensions_equal": True, "credit_scope": "TOPOLOGY_CONDITIONED_LAYER_PRIORITY_ONLY"},
    "P2-C3": {"candidate": "P2-B", "comparator": "P2-A", "only_allowed_difference": "ROLE_BINDING_PLUS_LAYER_PRIORITY", "component_credit_forbidden": True, "credit_scope": "FULL_BUNDLE_ONLY_NOT_COMPONENT_ATTRIBUTION"},
}

LANE_EXPECTATIONS = (
    ("P2-A", "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY", "FIXED_GLOBAL", ["奇仪", "八门", "八神", "九星"]),
    ("P2-A_PRIME", "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "QUESTION_TOPOLOGY_CONDITIONED", "FIXED_GLOBAL", ["奇仪", "八门", "八神", "九星"]),
    ("P2-B", "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "QUESTION_TOPOLOGY_CONDITIONED", "QUESTION_TOPOLOGY_CONDITIONED", None),
)

PAYLOAD_KEYS = {
    "schema_version", "artifact_kind", "plan_id", "hypothesis_id",
    "plan_amendment_sha256", "execution_substrate_manifest_sha256",
    "execution_contract_sha256", "mapping_boundary", "lane_bindings",
    "estimand_lock", "shared_representation", "complexity_budget", "blinding",
    "denominator_policy", "reproducibility", "research_only", "outcome_data_used",
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
    _require(contract.get("contract_id") == "K2-QIMEN-P2-FREEZE-SERIALIZER-CONTRACT-V02", "contract id drift")
    _require(contract.get("version") == "0.2", "contract version drift")
    _require(contract.get("failure_policy") == "FAIL_CLOSED", "serializer must fail closed")
    _require(contract.get("base_plan_id") == "K2PV-QRM-002", "base plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    _require(contract.get("plan_amendment_sha256") == PLAN_AMENDMENT_SHA, "plan amendment binding drift")
    _require(contract.get("execution_substrate_manifest_sha256") == SUBSTRATE_SHA, "substrate binding drift")
    boundary = contract.get("serializer_boundary", {})
    for key in (
        "serializer_is_pure", "serializer_does_not_create_batch",
        "serializer_does_not_persist_freeze", "production_freeze_requires_preexisting_batch",
        "batch_binding_included_in_serialized_bytes", "serializer_contract_hash_included_in_serialized_bytes",
        "fixture_mode_requires_synthetic_batch",
    ):
        _require(boundary.get(key) is True, f"serializer boundary drift: {key}")
    payload_contract = contract.get("payload_contract", {})
    _require(payload_contract.get("schema_version") == "0.2", "payload schema version drift")
    _require(payload_contract.get("schema_canonical_sha256") == "955d8c107cf5a4a7d830868b26967817aa8d85474f08b73203c43cf85d139c01", "payload schema hash drift")
    _require(payload_contract.get("artifact_kind") == "P2_EXECUTION_FREEZE", "payload artifact kind drift")
    _require(payload_contract.get("research_only") is True, "payload research_only drift")
    _require(payload_contract.get("outcome_data_used") is False, "payload outcome access drift")
    canon = contract.get("canonicalization", {})
    _require(canon == {
        "encoding": "UTF-8", "json_sort_keys": True, "separators": [",", ":"],
        "ensure_ascii": False, "floats_forbidden": True, "hash_algorithm": "SHA256",
    }, "canonicalization drift")
    _require(set(contract.get("forbidden_fields", [])) == FORBIDDEN_FIELDS, "forbidden field set drift")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def _validate_generator(generator, expected_lane):
    required = {
        "generator_id", "lane_id", "version", "implementation_ref",
        "implementation_sha256", "canonical_input_schema_sha256",
        "canonical_output_schema_sha256", "nondeterminism_policy", "seed",
    }
    _require(isinstance(generator, dict) and set(generator) == required, f"{expected_lane} generator shape drift")
    _require(generator.get("lane_id") == expected_lane, f"{expected_lane} generator lane drift")
    _require(isinstance(generator.get("generator_id"), str) and generator["generator_id"], "generator id required")
    _require(isinstance(generator.get("version"), str) and generator["version"], "generator version required")
    _require(generator.get("implementation_ref") == "tools/k2_qimen_p2_generate_mapping.py", "generator implementation ref drift")
    for key in ("implementation_sha256", "canonical_input_schema_sha256", "canonical_output_schema_sha256"):
        _require_sha256(generator.get(key), f"{expected_lane} {key}")
    _require(generator.get("nondeterminism_policy") == "DETERMINISTIC", "production mapping generator must remain deterministic")
    _require(generator.get("seed") is None, "deterministic generator seed must be null")


def _validate_representation(rep):
    keys = {
        "representation_id", "representation_contract_sha256",
        "combined_representation_sha256", "world_variable_manifest_sha256",
        "symbol_vocabulary_sha256", "feature_extraction_manifest_sha256",
        "eligible_rule_pool_sha256", "prediction_schema_sha256",
    }
    _require(isinstance(rep, dict) and set(rep) == keys, "shared representation shape drift")
    _require(isinstance(rep.get("representation_id"), str) and rep["representation_id"], "representation_id required")
    _require(rep.get("representation_contract_sha256") == REPRESENTATION_CONTRACT_SHA, "representation contract drift")
    for key in keys - {"representation_id"}:
        _require_sha256(rep.get(key), key)
    shared_manifest_hashes = {
        "world_variable_manifest": rep["world_variable_manifest_sha256"],
        "symbol_vocabulary": rep["symbol_vocabulary_sha256"],
        "feature_extraction_manifest": rep["feature_extraction_manifest_sha256"],
        "eligible_rule_pool": rep["eligible_rule_pool_sha256"],
        "prediction_schema": rep["prediction_schema_sha256"],
    }
    expected = canonical_sha256({
        "representation_id": rep["representation_id"],
        "shared_manifest_hashes": shared_manifest_hashes,
    })
    _require(rep.get("combined_representation_sha256") == expected, "combined representation identity/hash drift")


def _validate_budget(budget):
    keys = {
        "formula_id", "contract_sha256", "profile_id", "profile_sha256",
        "max_roles_per_question", "max_layers_per_question",
        "max_symbol_instances_per_question", "max_total_units_per_lane",
        "max_role_bindings_per_symbol_instance",
    }
    _require(isinstance(budget, dict) and set(budget) == keys, "complexity budget V02 shape drift")
    _require(budget.get("formula_id") == "P2_SHARED_COMPLEXITY_FORMULA_V01", "complexity formula drift")
    _require(budget.get("contract_sha256") == BUDGET_CONTRACT_SHA, "complexity contract drift")
    _require(isinstance(budget.get("profile_id"), str) and budget["profile_id"], "complexity profile id required")
    _require_sha256(budget.get("profile_sha256"), "complexity profile sha256")
    limits = [
        "max_roles_per_question", "max_layers_per_question",
        "max_symbol_instances_per_question", "max_total_units_per_lane",
        "max_role_bindings_per_symbol_instance",
    ]
    for key in limits:
        value = budget.get(key)
        _require(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{key} must be positive integer")
    profile = {"profile_id": budget["profile_id"]}
    profile.update({key: budget[key] for key in limits})
    _require(budget["profile_sha256"] == canonical_sha256(profile), "complexity profile content/hash binding drift")


def _validate_blinding(blinding):
    expected_keys = {"contract_sha256", "lane_blinding_protocol", "lane_order_seed", "cross_lane_isolation_policy"}
    _require(isinstance(blinding, dict) and set(blinding) == expected_keys, "blinding V02 shape drift")
    _require(blinding.get("contract_sha256") == BLINDING_CONTRACT_SHA, "blinding contract drift")
    _require(blinding.get("lane_blinding_protocol") == "P2_BLINDED_ISOLATED_V01", "blinding protocol drift")
    seed = blinding.get("lane_order_seed")
    _require(isinstance(seed, int) and not isinstance(seed, bool), "lane order seed must be integer")
    _require(blinding.get("cross_lane_isolation_policy") == "FRESH_STATE_NO_CROSS_LANE_CACHE", "isolation policy drift")


def _validate_denominator(denominator):
    keys = {
        "contract_sha256", "primary_denominator_policy",
        "abstention_scoring_profile_id", "abstention_scoring_profile_sha256",
        "technical_unevaluable_policy",
    }
    _require(isinstance(denominator, dict) and set(denominator) == keys, "denominator V02 shape drift")
    _require(denominator.get("contract_sha256") == DENOMINATOR_CONTRACT_SHA, "denominator contract drift")
    _require(denominator.get("primary_denominator_policy") == "COUNT_ALL_FROZEN_INCLUDED_CASES_PER_CONTRAST", "primary denominator drift")
    _require(isinstance(denominator.get("abstention_scoring_profile_id"), str) and denominator["abstention_scoring_profile_id"], "abstention profile id required")
    _require_sha256(denominator.get("abstention_scoring_profile_sha256"), "abstention profile sha256")
    _require(denominator.get("technical_unevaluable_policy") == "RETAIN_SYMMETRICALLY", "technical UNEVALUABLE policy drift")


def _validate_reproducibility(repro):
    _require(isinstance(repro, dict) and set(repro) == {"contract_sha256", "fixture_hash", "expected_report_sha256"}, "reproducibility V02 shape drift")
    _require(repro.get("contract_sha256") == REPRO_CONTRACT_SHA, "reproducibility contract drift")
    _require(repro.get("fixture_hash") == REPRO_FIXTURE_SHA, "reproducibility fixture drift")
    _require(repro.get("expected_report_sha256") == REPRO_REPORT_SHA, "reproducibility report drift")


def _validate_payload(payload):
    _require(isinstance(payload, dict) and set(payload) == PAYLOAD_KEYS, "freeze payload V02 shape drift")
    _reject_floats(payload, "freeze payload")
    _reject_forbidden_fields(payload, "freeze payload")
    _require(payload.get("schema_version") == "0.2", "freeze schema version drift")
    _require(payload.get("artifact_kind") == "P2_EXECUTION_FREEZE", "freeze artifact kind drift")
    _require(payload.get("plan_id") == "K2PV-QRM-002", "freeze plan drift")
    _require(payload.get("hypothesis_id") == "QRM-H1", "freeze hypothesis drift")
    _require(payload.get("plan_amendment_sha256") == PLAN_AMENDMENT_SHA, "freeze plan amendment drift")
    _require(payload.get("execution_substrate_manifest_sha256") == SUBSTRATE_SHA, "freeze substrate drift")
    _require(payload.get("execution_contract_sha256") == EXECUTION_CONTRACT_SHA, "freeze execution contract drift")
    _require(payload.get("mapping_boundary") == {
        "mapping_before_plate_value_access": True,
        "plate_value_access_before_mapping": False,
    }, "mapping boundary drift")
    lanes = payload.get("lane_bindings")
    _require(isinstance(lanes, list) and len(lanes) == 3, "exactly three lanes required")
    for lane, expected in zip(lanes, LANE_EXPECTATIONS):
        lane_id, model_name, role_policy, layer_policy, fixed_priority = expected
        keys = {"lane_id", "model_name", "role_binding_policy", "layer_priority_policy", "fixed_layer_priority", "generator"}
        _require(isinstance(lane, dict) and set(lane) == keys, f"{lane_id} lane shape drift")
        _require(lane.get("lane_id") == lane_id, "lane identity/order drift")
        _require(lane.get("model_name") == model_name, f"{lane_id} model drift")
        _require(lane.get("role_binding_policy") == role_policy, f"{lane_id} role policy drift")
        _require(lane.get("layer_priority_policy") == layer_policy, f"{lane_id} layer policy drift")
        _require(lane.get("fixed_layer_priority") == fixed_priority, f"{lane_id} fixed priority drift")
        _validate_generator(lane.get("generator"), lane_id)
    _require(payload.get("estimand_lock") == ESTIMAND_LOCK, "estimand lock drift")
    _validate_representation(payload.get("shared_representation"))
    _validate_budget(payload.get("complexity_budget"))
    _validate_blinding(payload.get("blinding"))
    _validate_denominator(payload.get("denominator_policy"))
    _validate_reproducibility(payload.get("reproducibility"))
    _require(payload.get("research_only") is True, "research_only must remain true")
    _require(payload.get("outcome_data_used") is False, "outcome data must remain unused")


def validate_document(document, contract):
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
    batch = document.get("batch_binding")
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
    _validate_payload(document.get("freeze_payload"))


def _envelope_from_document(document, contract):
    return {
        "serializer_contract_id": contract["contract_id"],
        "serializer_version": contract["version"],
        "serializer_contract_sha256": canonical_sha256(contract),
        "mode": "FIXTURE_ONLY" if document["fixture_only"] else "PRODUCTION_CANDIDATE",
        "batch_binding": copy.deepcopy(document["batch_binding"]),
        "freeze_payload": copy.deepcopy(document["freeze_payload"]),
        "freeze_payload_sha256": canonical_sha256(document["freeze_payload"]),
        "production_freeze_created": False,
    }


def serialize_freeze_candidate(document, contract):
    validate_document(document, contract)
    envelope = _envelope_from_document(document, contract)
    raw = canonical_bytes(envelope)
    return raw, hashlib.sha256(raw).hexdigest()


def verify_serialized_freeze(raw, expected_sha256, contract):
    validate_contract(contract)
    _require(isinstance(raw, (bytes, bytearray)), "serialized Freeze must be bytes")
    raw = bytes(raw)
    _require_sha256(expected_sha256, "serialized Freeze sha256")
    _require(hashlib.sha256(raw).hexdigest() == expected_sha256, "serialized Freeze exact-byte hash mismatch")
    try:
        envelope = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise FreezeSerializationError(f"serialized Freeze invalid UTF-8 JSON: {exc}") from exc
    _require(raw == canonical_bytes(envelope), "serialized Freeze bytes are not canonical")
    expected_keys = {
        "serializer_contract_id", "serializer_version", "serializer_contract_sha256",
        "mode", "batch_binding", "freeze_payload", "freeze_payload_sha256",
        "production_freeze_created",
    }
    _require(isinstance(envelope, dict) and set(envelope) == expected_keys, "serialized envelope shape drift")
    _require(envelope.get("serializer_contract_id") == contract["contract_id"], "serialized contract id drift")
    _require(envelope.get("serializer_version") == contract["version"], "serialized contract version drift")
    _require(envelope.get("serializer_contract_sha256") == canonical_sha256(contract), "serialized contract hash drift")
    _require(envelope.get("freeze_payload_sha256") == canonical_sha256(envelope.get("freeze_payload")), "serialized payload hash drift")
    _require(envelope.get("production_freeze_created") is False, "serialized envelope cannot claim persisted Freeze")
    reconstructed = {
        "fixture_only": envelope["mode"] == "FIXTURE_ONLY",
        "production_freeze_created": False,
        "batch_binding": envelope["batch_binding"],
        "freeze_payload": envelope["freeze_payload"],
    }
    if reconstructed["fixture_only"]:
        reconstructed["fixture_id"] = "VERIFICATION-FIXTURE"
    validate_document(reconstructed, contract)
    return envelope
