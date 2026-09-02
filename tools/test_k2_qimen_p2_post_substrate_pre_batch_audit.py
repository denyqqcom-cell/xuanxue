#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

from k2_qimen_p2_freeze_serializer_v02 import (
    FreezeSerializationError,
    canonical_sha256,
    serialize_freeze_candidate,
    validate_contract,
    validate_document,
    verify_serialized_freeze,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

SUBSTRATE_SHA = "bee308bfb52e18829f558d576e6ea581aae0580de625aa6206bdbf84ef5fa3d5"
AMENDMENT_SHA = "d39db1528905b2d008720e2c1f45c2d723ce20aaf1df99c8b7fb7ed132e13de3"
SCHEMA_V02_SHA = "955d8c107cf5a4a7d830868b26967817aa8d85474f08b73203c43cf85d139c01"
SERIALIZER_CONTRACT_SHA = "d8d2e289f057d62e0961cc8014d3e0ca2f82f458f1b50c1b804d7f75b888e4a4"
FIXTURE_SHA = "f70f8a10e2a38384a33902c1964068abed7f23e3468c7ef4e1a7ff548d8afde3"
FIXTURE_PAYLOAD_SHA = "02c905ebbb8ae955c02fb265921d98c03a119881a67c26b0a36b638ae04dce06"
EXPECTED_SERIALIZED_SHA = "e05021971e943d707762f98a5dd0ae14bb668b7ea3b7002f6a3e128ba3510a37"

HISTORICAL_CONTRACT_HASHES = {
    "K2_QIMEN_P2_EXECUTION_CONTRACT_V01.json": "218bf3dbc8e83421db34d3d8678a17b93c7e1ed981d28ba70ede02c1c145264b",
    "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json": "1a7128dd4c1ba5846c1d74f78645ff7b1ea87032898bbd83f61859283182393d",
    "K2_QIMEN_P2_ROLE_LAYER_GENERATOR_CONTRACT_V01.json": "5bca2e5544cadf3e1dad2f8e150dffd93b0a12b1d3295d8ab01f56b0ff18bf63",
    "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json": "ae54cb165af4c5ed999b24fad425e18051e0379809b6cbec816cd839be68439a",
    "K2_QIMEN_P2_BLINDED_LANE_RUNNER_CONTRACT_V01.json": "9a93bc02a8388651a50fd94423f1c89a36c984582ca4de272cfd118843758a3e",
    "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json": "1bf117aff2ab7a54570382292b7c75d6e00fe5e28bbef595f3dcb41c7b288c25",
    "K2_QIMEN_P2_EXACT_REPRODUCIBILITY_CONTRACT_V01.json": "17473e7d22f187eb7ca3a76de82edc160d24cdae919b1c4f27109ac60f5c889b",
    "K2_QIMEN_P2_FREEZE_SERIALIZER_CONTRACT_V01.json": "94824fb4774c57254c3546d86534156daadd8404af3a47ca4aee17fbd49570a7",
}
LEGACY_BUDGET_FIELDS = {
    "role_multiplicity_budget", "reasoning_branch_budget", "rule_trace_budget",
    "interpreter_information_budget", "tool_access_budget",
}
MODERN_BUDGET_FIELDS = {
    "formula_id", "contract_sha256", "profile_id", "profile_sha256",
    "max_roles_per_question", "max_layers_per_question",
    "max_symbol_instances_per_question", "max_total_units_per_lane",
    "max_role_bindings_per_symbol_instance",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            rows.append(json.loads(raw))
    return rows


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def expect_failure(fn, label):
    try:
        fn()
    except (FreezeSerializationError, AssertionError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"negative case unexpectedly passed: {label}")


def validate_repository():
    for filename, expected in HISTORICAL_CONTRACT_HASHES.items():
        actual = canonical_sha256(load_json(K / filename))
        require(actual == expected, f"historical contract hash drift: {filename}")

    historical_schema = load_json(K / "schema" / "qimen_p2_execution_freeze.schema.json")
    historical_budget = set(historical_schema["properties"]["complexity_budget"]["required"])
    require(historical_budget == LEGACY_BUDGET_FIELDS, "historical V01 Freeze schema was silently rewritten")

    plans = load_jsonl(K / "K2_PROSPECTIVE_TEST_PLANS.jsonl")
    qrm = [row for row in plans if row.get("plan_id") == "K2PV-QRM-002" and row.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm) == 1, "historical active base plan identity drift")
    require(LEGACY_BUDGET_FIELDS.issubset(set(qrm[0].get("freeze_required_fields", []))), "base plan historical freeze fields were silently rewritten")

    substrate = load_json(K / "K2_QIMEN_P2_EXECUTION_SUBSTRATE_MANIFEST_V01.json")
    require(canonical_sha256(substrate) == SUBSTRATE_SHA, "execution substrate manifest hash drift")
    require(substrate.get("closed_capabilities") == [f"P2-EXEC-{i:03d}" for i in range(1, 10)], "execution substrate capability closure drift")
    require(substrate.get("execution_substrate_ready") is True, "substrate must remain ready")
    require(substrate.get("batch_creation_allowed") is False, "substrate alone cannot authorize Batch")

    amendment = load_json(K / "K2_QIMEN_P2_ROLE_MAP_PLAN_AMENDMENT_V01.json")
    require(canonical_sha256(amendment) == AMENDMENT_SHA, "plan amendment hash drift")
    require(amendment.get("historical_base_plan_mutation_forbidden") is True, "historical plan mutation guard missing")
    require(amendment.get("trigger_fail_first_commit") == "220c3f917e3f3bd1bcfb4a55c83fd8cad3da7e11", "fail-first trigger binding drift")
    require(len(amendment.get("confirmed_binding_drifts", [])) == 5, "binding-drift finding count drift")

    schema_v02 = load_json(K / "schema" / "qimen_p2_execution_freeze_v02.schema.json")
    require(canonical_sha256(schema_v02) == SCHEMA_V02_SHA, "V02 Freeze schema hash drift")
    modern_budget = set(schema_v02["properties"]["complexity_budget"]["required"])
    require(modern_budget == MODERN_BUDGET_FIELDS, "V02 complexity budget binding shape drift")
    shared_required = set(schema_v02["properties"]["shared_representation"]["required"])
    require({"representation_id", "combined_representation_sha256", "representation_contract_sha256"}.issubset(shared_required), "V02 representation identity not fully bound")
    require("contract_sha256" in schema_v02["properties"]["blinding"]["required"], "V02 blinding contract hash missing")
    require({"contract_sha256", "abstention_scoring_profile_sha256"}.issubset(set(schema_v02["properties"]["denominator_policy"]["required"])), "V02 denominator/scoring binding missing")

    contract = load_json(K / "K2_QIMEN_P2_FREEZE_SERIALIZER_CONTRACT_V02.json")
    fixture = load_json(ROOT / "tools" / "testdata" / "qimen_p2_freeze_serializer_v02_fixture.json")
    require(canonical_sha256(contract) == SERIALIZER_CONTRACT_SHA, "V02 serializer contract hash drift")
    require(canonical_sha256(fixture) == FIXTURE_SHA, "V02 serializer fixture hash drift")
    require(canonical_sha256(fixture["freeze_payload"]) == FIXTURE_PAYLOAD_SHA, "V02 fixture payload hash drift")
    require(contract["fixture_binding"]["fixture_canonical_sha256"] == FIXTURE_SHA, "contract fixture binding drift")
    require(contract["fixture_binding"]["fixture_payload_sha256"] == FIXTURE_PAYLOAD_SHA, "contract fixture payload binding drift")
    validate_contract(contract)
    validate_document(fixture, contract)

    raw1, sha1 = serialize_freeze_candidate(fixture, contract)
    raw2, sha2 = serialize_freeze_candidate(copy.deepcopy(fixture), contract)
    require(raw1 == raw2 and sha1 == sha2, "V02 serialization not byte-exact")
    require(sha1 == EXPECTED_SERIALIZED_SHA, "V02 serialized fixture sha drift")
    envelope = verify_serialized_freeze(raw1, sha1, contract)
    require(envelope["serializer_contract_sha256"] == SERIALIZER_CONTRACT_SHA, "serialized contract binding drift")
    require(envelope["freeze_payload_sha256"] == FIXTURE_PAYLOAD_SHA, "serialized payload binding drift")
    require(envelope["production_freeze_created"] is False, "serializer cannot persist Freeze")

    prebatch = load_json(K / "K2_QIMEN_P2_PRE_BATCH_BINDING_CONTRACT_V01.json")
    require(prebatch.get("status") == "ACTIVE_PRE_BATCH_BINDING", "pre-Batch binding authority status drift")
    require(prebatch["authority_chain"]["plan_amendment_sha256"] == AMENDMENT_SHA, "pre-Batch amendment binding drift")
    require(prebatch["authority_chain"]["execution_substrate_manifest_sha256"] == SUBSTRATE_SHA, "pre-Batch substrate binding drift")
    require(prebatch["authority_chain"]["freeze_schema_sha256"] == SCHEMA_V02_SHA, "pre-Batch schema binding drift")
    require(prebatch["authority_chain"]["freeze_serializer_contract_sha256"] == SERIALIZER_CONTRACT_SHA, "pre-Batch serializer binding drift")
    require(prebatch.get("post_substrate_binding_ready") is True, "post-substrate binding closure not declared")
    require(prebatch.get("statistical_preregistration_ready") is False, "binding repair must not fake statistical preregistration")
    require(prebatch.get("batch_ready") is False and prebatch.get("batch_creation_allowed") is False, "Batch must remain blocked")
    require(prebatch.get("batch") == prebatch.get("freeze") == prebatch.get("outcome") == "NONE", "pre-Batch state mutation")
    require(prebatch.get("empirical_credit") == "NONE", "binding repair cannot grant empirical credit")

    negative_cases = []
    case = copy.deepcopy(fixture); case["freeze_payload"]["plan_amendment_sha256"] = "0" * 64
    negative_cases.append(("amendment_hash_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["execution_substrate_manifest_sha256"] = "0" * 64
    negative_cases.append(("substrate_hash_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); del case["freeze_payload"]["shared_representation"]["combined_representation_sha256"]
    negative_cases.append(("missing_combined_representation", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["shared_representation"]["representation_contract_sha256"] = "0" * 64
    negative_cases.append(("representation_contract_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["formula_id"] = "POST_HOC_FORMULA"
    negative_cases.append(("budget_formula_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["contract_sha256"] = "0" * 64
    negative_cases.append(("budget_contract_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["profile_sha256"] = "0" * 64
    negative_cases.append(("budget_profile_hash_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["max_roles_per_question"] = 0
    negative_cases.append(("nonpositive_budget", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["role_multiplicity_budget"] = 4
    negative_cases.append(("legacy_budget_field_reintroduced", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["complexity_budget"]["max_layers_per_question"] = 4.0
    negative_cases.append(("float_budget", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["blinding"]["contract_sha256"] = "0" * 64
    negative_cases.append(("blinding_contract_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["blinding"]["lane_blinding_protocol"] = "VISIBLE_LANES"
    negative_cases.append(("blinding_protocol_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["denominator_policy"]["contract_sha256"] = "0" * 64
    negative_cases.append(("denominator_contract_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["denominator_policy"]["primary_denominator_policy"] = "PREDICTED_ONLY"
    negative_cases.append(("denominator_policy_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["denominator_policy"]["abstention_scoring_profile_sha256"] = "not-a-hash"
    negative_cases.append(("abstention_profile_hash_invalid", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["reproducibility"]["contract_sha256"] = "0" * 64
    negative_cases.append(("repro_contract_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["reproducibility"]["fixture_hash"] = "0" * 64
    negative_cases.append(("repro_fixture_drift", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["freeze_payload"]["outcome"] = "KNOWN"
    negative_cases.append(("outcome_field_forbidden", lambda case=case: validate_document(case, contract)))
    case = copy.deepcopy(fixture); case["fixture_only"] = False
    negative_cases.append(("production_without_production_batch", lambda case=case: validate_document(case, contract)))
    mutated = bytearray(raw1); mutated[-1] = ord(" ")
    negative_cases.append(("byte_mutation", lambda: verify_serialized_freeze(bytes(mutated), sha1, contract)))

    for label, fn in negative_cases:
        expect_failure(fn, label)

    source = (ROOT / "tools" / "k2_qimen_p2_freeze_serializer_v02.py").read_text(encoding="utf-8")
    for token in ("write_text(", "write_bytes(", "open("):
        require(token not in source, f"V02 serializer gained persistence surface: {token}")

    print(
        "k2-qimen-p2-post-substrate-pre-batch-audit: PASS "
        f"binding_repairs=5 negative_cases={len(negative_cases)} "
        "post_substrate_binding_ready=true statistical_preregistration_ready=false "
        "batch_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-post-substrate-pre-batch-audit: FAIL: {exc}", file=sys.stderr)
        raise
