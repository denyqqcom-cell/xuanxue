#!/usr/bin/env python3
import copy
import hashlib
import json
import re
from datetime import datetime, timezone

SHA64 = re.compile(r"^[0-9a-f]{64}$")
UTC_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PRIMARY_TOPOLOGIES = ("JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE")
REQUIRED_FIELDS = {
    "batch_id",
    "batch_start_timestamp_utc",
    "batch_start_boundary_source",
    "eligibility_manifest_schema_sha256",
    "case_identity_policy_id",
    "acquisition_window_days",
    "outcome_followup_days",
    "target_cases_per_topology",
    "primary_topologies",
    "statistical_preregistration_sha256",
}
FORBIDDEN_FIELDS = {
    "outcome",
    "outcome_value",
    "observed_outcome",
    "feedback",
    "score",
    "winner_lane",
    "current_time",
    "now",
    "runtime_timestamp",
    "selected_after_outcome",
    "post_prediction_replacement",
}


class BatchRegistrationError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise BatchRegistrationError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _validate_sha(value, label):
    _require(isinstance(value, str) and SHA64.fullmatch(value) is not None, f"{label} must be sha256")


def _validate_utc_z(value):
    _require(isinstance(value, str) and UTC_Z.fullmatch(value) is not None, "batch_start_timestamp_utc must be RFC3339 UTC Z with whole seconds")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise BatchRegistrationError("invalid batch_start_timestamp_utc") from exc
    _require(parsed.tzinfo == timezone.utc, "batch_start_timestamp_utc must be UTC")


def validate_batch_registration_contract(contract, prereg):
    _require(isinstance(contract, dict), "Batch registration contract must be object")
    _require(contract.get("contract_id") == "K2-QIMEN-P2-BATCH-REGISTRATION-CONTRACT-V01", "contract id drift")
    _require(contract.get("capability") == "P2-PREBATCH-BATCH-005", "capability drift")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    _require(contract.get("prior_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V20.json", "prior protocol drift")
    _require(contract.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V16.json", "prior implementation drift")
    _require(contract.get("statistical_preregistration_git_blob") == "4cc3de63c8509fb00893d9cf788f17224f389014", "preregistration blob drift")

    boundary = contract.get("registration_boundary", {})
    for key in (
        "binder_is_pure",
        "binder_does_not_persist_registry",
        "binder_does_not_create_batch",
        "production_registration_requires_explicit_future_authorization",
        "production_registration_requires_statistical_preregistration_ready",
        "registration_before_any_lane_execution",
        "registration_before_any_outcome_access",
        "start_boundary_must_be_explicit_input",
        "runtime_now_or_current_time_selection_forbidden",
    ):
        _require(boundary.get(key) is True, f"registration boundary drift: {key}")

    spec = contract.get("registration_input", {})
    _require(set(spec.get("required_fields", [])) == REQUIRED_FIELDS, "required registration field set drift")
    _require(set(spec.get("forbidden_fields", [])) == FORBIDDEN_FIELDS, "forbidden registration field set drift")
    _require(spec.get("batch_start_boundary_source") == "EXPLICIT_PRE_OUTCOME_BATCH_REGISTRATION_INPUT", "start-boundary source drift")
    _require(spec.get("timestamp_format") == "RFC3339_UTC_Z_ONLY", "timestamp format drift")
    _require(spec.get("primary_topologies") == list(PRIMARY_TOPOLOGIES), "primary topology set drift")
    _require(spec.get("acquisition_window_days") == 365, "acquisition window drift")
    _require(spec.get("outcome_followup_days") == 90, "outcome followup drift")
    _require(spec.get("target_cases_per_topology") == 80, "target cases drift")
    _require(spec.get("case_identity_policy_id") == "ONE_INCLUDED_CASE_PER_ASKER_PER_BATCH_V01", "case identity policy drift")

    output = contract.get("registration_output", {})
    _require(output.get("artifact_kind") == "P2_BATCH_REGISTRATION_CANDIDATE", "output artifact kind drift")
    _require(output.get("canonical_serialization") == "UTF8_JSON_SORT_KEYS_COMPACT", "canonicalization drift")
    _require(output.get("hash_algorithm") == "SHA256", "hash algorithm drift")
    _require(output.get("production_batch_created") is False, "contract cannot create production Batch")
    _require(output.get("registry_persisted") is False, "contract cannot persist registry")
    _require(output.get("outcome_data_used") is False, "contract cannot use outcome data")

    prod = contract.get("production_policy", {})
    _require(prod.get("actual_batch_id_must_not_be_generated_by_test_fixture") is True, "fixture batch-id isolation guard missing")
    _require(prod.get("actual_batch_start_must_be_explicitly_authorized_later") is True, "future authorization guard missing")
    _require(prod.get("actual_registry_write_is_separate_mutation") is True, "registry-write separation missing")
    _require(prod.get("actual_registry_write_not_authorized_by_this_contract") is True, "registry write must remain unauthorized")
    _require(prod.get("actual_batch_freeze_requires_preexisting_registered_batch") is True, "Freeze must require preexisting registered Batch")

    _require(prereg.get("preregistration_id") == "K2-QIMEN-P2-STATISTICAL-PREREGISTRATION-V01", "preregistration id drift")
    _require(prereg.get("statistical_preregistration_ready") is True, "statistical preregistration is not ready")
    _require(prereg.get("batch_ready") is False and prereg.get("batch_creation_allowed") is False, "preregistration unexpectedly opened Batch")
    _require(prereg.get("batch") == prereg.get("freeze") == prereg.get("outcome") == "NONE", "preregistration state mutation")
    _require(prereg.get("outcome_data_used") is False, "preregistration used outcome data")

    _require(contract.get("research_only") is True, "contract must remain research-only")
    _require(contract.get("outcome_data_used") is False, "contract outcome data use detected")
    _require(contract.get("batch_registration_machinery_ready") is False, "fail-first contract cannot preclaim machinery readiness")
    _require(contract.get("batch_ready") is False and contract.get("batch_creation_allowed") is False, "contract cannot open Batch")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "contract state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain blocked")


def validate_registration_input(source, contract, prereg, fixture_only):
    validate_batch_registration_contract(contract, prereg)
    _require(isinstance(source, dict), "registration input must be object")
    keys = set(source)
    _require(not (keys & FORBIDDEN_FIELDS), "registration input contains forbidden outcome/runtime fields")
    _require(keys == REQUIRED_FIELDS, "registration input field set drift")
    _require(isinstance(fixture_only, bool), "fixture_only must be boolean")

    batch_id = source.get("batch_id")
    _require(isinstance(batch_id, str) and batch_id, "batch_id required")
    if fixture_only:
        _require(batch_id.startswith("FIXTURE-"), "fixture batch_id must start FIXTURE-")
    else:
        _require(not batch_id.startswith("FIXTURE-"), "production candidate cannot use fixture batch_id")
        raise BatchRegistrationError("production Batch registration requires separate explicit future authorization")

    _validate_utc_z(source.get("batch_start_timestamp_utc"))
    _require(source.get("batch_start_boundary_source") == contract["registration_input"]["batch_start_boundary_source"], "batch start boundary source drift")
    _validate_sha(source.get("eligibility_manifest_schema_sha256"), "eligibility manifest schema hash")
    _require(source.get("case_identity_policy_id") == contract["registration_input"]["case_identity_policy_id"], "case identity policy drift")
    _require(source.get("acquisition_window_days") == contract["registration_input"]["acquisition_window_days"], "acquisition window drift")
    _require(source.get("outcome_followup_days") == contract["registration_input"]["outcome_followup_days"], "outcome followup drift")
    _require(source.get("target_cases_per_topology") == contract["registration_input"]["target_cases_per_topology"], "target cases per topology drift")
    _require(source.get("primary_topologies") == list(PRIMARY_TOPOLOGIES), "primary topology list drift")
    _validate_sha(source.get("statistical_preregistration_sha256"), "statistical preregistration hash")
    _require(source.get("statistical_preregistration_sha256") == canonical_sha256(prereg), "statistical preregistration content hash mismatch")


def _candidate_payload(source, contract, prereg):
    return {
        "artifact_kind": "P2_BATCH_REGISTRATION_CANDIDATE",
        "fixture_only": True,
        "canonical_serialization": "UTF8_JSON_SORT_KEYS_COMPACT",
        "hash_algorithm": "SHA256",
        "plan_id": contract["plan_id"],
        "hypothesis_id": contract["hypothesis_id"],
        "protocol_ref": contract["prior_protocol_ref"],
        "implementation_ref": contract["prior_implementation_ref"],
        "statistical_preregistration_ref": contract["statistical_preregistration_ref"],
        "statistical_preregistration_git_blob": contract["statistical_preregistration_git_blob"],
        "statistical_preregistration_sha256": canonical_sha256(prereg),
        "production_representation_ref": contract["production_representation_ref"],
        "production_representation_git_blob": contract["production_representation_git_blob"],
        "shared_profiles_ref": contract["shared_profiles_ref"],
        "shared_profiles_git_blob": contract["shared_profiles_git_blob"],
        "batch_id": source["batch_id"],
        "batch_start_timestamp_utc": source["batch_start_timestamp_utc"],
        "batch_start_boundary_source": source["batch_start_boundary_source"],
        "eligibility_manifest_schema_sha256": source["eligibility_manifest_schema_sha256"],
        "case_identity_policy_id": source["case_identity_policy_id"],
        "acquisition_window_days": source["acquisition_window_days"],
        "outcome_followup_days": source["outcome_followup_days"],
        "target_cases_per_topology": source["target_cases_per_topology"],
        "primary_topologies": copy.deepcopy(source["primary_topologies"]),
        "production_batch_created": False,
        "registry_persisted": False,
        "outcome_data_used": False,
    }


def bind_batch_registration_candidate(source, contract, prereg, fixture_only=True):
    validate_registration_input(source, contract, prereg, fixture_only)
    payload = _candidate_payload(source, contract, prereg)
    result = copy.deepcopy(payload)
    result["registration_candidate_sha256"] = canonical_sha256(payload)
    return result
