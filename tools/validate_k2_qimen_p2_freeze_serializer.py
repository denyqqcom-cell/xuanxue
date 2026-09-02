#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_exact_reproducibility as reproducibility_validator
from k2_qimen_p2_freeze_serializer import (
    canonical_sha256,
    serialize_freeze_candidate,
    validate_contract,
    validate_document,
    verify_serialized_freeze,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_FREEZE_SERIALIZER_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_freeze_serializer_fixture.json"
SERIALIZER_PATH = ROOT / "tools" / "k2_qimen_p2_freeze_serializer.py"
TEST_PATH = ROOT / "tools" / "test_k2_qimen_p2_freeze_serializer.py"
SCHEMA_PATH = K / "schema" / "qimen_p2_execution_freeze.schema.json"
V07_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V07.json"
V08_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V08.json"
V11_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V11.json"
V12_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V12.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "94824fb4774c57254c3546d86534156daadd8404af3a47ca4aee17fbd49570a7"
EXPECTED_FIXTURE_HASH = "80166c6082b2e82268b87bac84a10400236b2fd8f50c069eb6953365702cd9e6"
EXPECTED_REPRO_HASH = "88968c2388163efa009640ba91c9a67b68049fcbb573d86ed725a319c3130977"
EXPECTED_PAYLOAD_HASH = "b4a617bfec59873509dad8cd1783b70178d1b2998146a15b6592e8d5bc36c09e"
EXPECTED_SERIALIZED_HASH = "fb26e03da226459d5012b803f17b803bb25d729bc124dbaeabb6988ffd49a379"
EXPECTED_CONTRACT_BLOB = "8eea57d05fd97b58aed047d512977b7265712a01"
EXPECTED_FIXTURE_BLOB = "ed3a1f2cd5a64748b71a88b23164178082bab750"
EXPECTED_SERIALIZER_BLOB = "3c3f884e864101aaff538095516a67da4bdc243d"
EXPECTED_TEST_BLOB = "233c38fed22fb5a6208e938dcf32b7d5f24740ab"
EXPECTED_SCHEMA_BLOB = "7e3a595f88080c9d46c55d4f609b8305ef26376a"
EXPECTED_V07_BLOB = "c1552fadac8a9d3aa9bc692c012485d82ab0bd82"
EXPECTED_V11_BLOB = "a36f099ab59cfc77a93e71415644e59c188b8bb0"
EXPECTED_V08_BLOB = "7db26d64e35f408d0dd3513e2f2e563ba2108ef7"
EXPECTED_V12_BLOB = "705093543005deb47e88a6231880294db238b5f6"
FAIL_FIRST_COMMIT = "8c996e24c3f40070396ddd83a16014797fa0ac31"
FAIL_FIRST_RUN = 33592721754
FAIL_FIRST_JOB = 100129826117

EXPECTED_CLOSED = [
    "P2-EXEC-001",
    "P2-EXEC-002",
    "P2-EXEC-003",
    "P2-EXEC-004",
    "P2-EXEC-005",
    "P2-EXEC-006",
    "P2-EXEC-007",
    "P2-EXEC-008",
    "P2-EXEC-009",
]


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
    # Live successor chain: 009 -> 008 -> ... -> 004 -> Distillate/TBV source audit.
    reproducibility_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    schema = load_json(SCHEMA_PATH)
    v07 = load_json(V07_PATH)
    v08 = load_json(V08_PATH)
    v11 = load_json(V11_PATH)
    v12 = load_json(V12_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "Freeze serializer contract blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "Freeze serializer fixture blob drift")
    require(git_blob_sha1(SERIALIZER_PATH) == EXPECTED_SERIALIZER_BLOB, "Freeze serializer implementation blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "Freeze serializer test blob drift")
    require(git_blob_sha1(SCHEMA_PATH) == EXPECTED_SCHEMA_BLOB, "historical Freeze schema blob drift")
    require(git_blob_sha1(V07_PATH) == EXPECTED_V07_BLOB, "V07 historical blob drift")
    require(git_blob_sha1(V11_PATH) == EXPECTED_V11_BLOB, "V11 historical blob drift")
    require(git_blob_sha1(V08_PATH) == EXPECTED_V08_BLOB, "V08 blob drift")
    require(git_blob_sha1(V12_PATH) == EXPECTED_V12_BLOB, "V12 blob drift")

    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "Freeze serializer contract canonical hash drift")
    require(canonical_sha256(fixture) == EXPECTED_FIXTURE_HASH, "Freeze serializer fixture canonical hash drift")
    validate_contract(contract)
    validate_document(fixture, contract, EXPECTED_REPRO_HASH)

    schema_required = set(schema.get("required", []))
    payload_keys = set(fixture.get("freeze_payload", {}))
    require(schema_required == payload_keys, "fixture payload and Freeze schema required-field set diverged")
    props = schema.get("properties", {})
    require(props.get("artifact_kind", {}).get("const") == "P2_EXECUTION_FREEZE", "Freeze schema artifact kind drift")
    require(props.get("plan_id", {}).get("const") == "K2PV-QRM-002", "Freeze schema plan drift")
    require(props.get("hypothesis_id", {}).get("const") == "QRM-H1", "Freeze schema hypothesis drift")
    require(props.get("research_only", {}).get("const") is True, "Freeze schema research_only drift")
    require(props.get("outcome_data_used", {}).get("const") is False, "Freeze schema outcome guard drift")

    raw1, digest1 = serialize_freeze_candidate(fixture, contract, EXPECTED_REPRO_HASH)
    raw2, digest2 = serialize_freeze_candidate(fixture, contract, EXPECTED_REPRO_HASH)
    require(raw1 == raw2 and digest1 == digest2, "Freeze serializer not byte-exact on repeated input")
    require(canonical_sha256(fixture["freeze_payload"]) == EXPECTED_PAYLOAD_HASH, "fixture Freeze payload hash drift")
    require(digest1 == EXPECTED_SERIALIZED_HASH, "serialized Freeze fixture hash drift")
    envelope = verify_serialized_freeze(raw1, EXPECTED_SERIALIZED_HASH, contract, EXPECTED_REPRO_HASH)
    require(envelope.get("mode") == "FIXTURE_ONLY", "closure fixture must remain fixture-only")
    require(envelope.get("production_freeze_created") is False, "serializer persisted production Freeze")
    require(envelope.get("batch_binding", {}).get("production_batch") is False, "fixture became production Batch")
    require(envelope.get("freeze_payload_sha256") == EXPECTED_PAYLOAD_HASH, "serialized payload hash drift")

    source = SERIALIZER_PATH.read_text(encoding="utf-8")
    # Registry names may legitimately appear in rejection guards. Detect write surfaces, not guard literals.
    for forbidden_token in ("write_text(", "write_bytes(", "open("):
        require(forbidden_token not in source, f"serializer gained persistence surface: {forbidden_token}")

    require(v08.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V08", "V08 id drift")
    require(v08.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V07.json", "V08 must append V07")
    require([row.get("blocker_id") for row in v08.get("closed_blockers", [])] == EXPECTED_CLOSED, "V08 closed blocker set drift")
    require(v08.get("open_blockers") == [], "V08 must have no open P2-EXEC blocker")
    require(v08.get("execution_substrate_ready") is True, "execution substrate should be machine-ready after 009")
    require(v08.get("batch_ready") is False and v08.get("batch_creation_allowed") is False, "substrate readiness cannot authorize Batch")
    require(v08.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V08 source-local audit marker drift")
    require(v08.get("freeze_serializer_semantics", {}).get("expected_serialized_fixture_sha256") == EXPECTED_SERIALIZED_HASH, "V08 serialized hash drift")
    require(v08.get("freeze_serializer_semantics", {}).get("fixture_hash_values_are_source_or_empirical_claims") is False, "V08 fixture overclaim drift")

    require(v12.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V12", "V12 id drift")
    require(v12.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V11", "V12 must append V11")
    require(v12.get("closed_execution_blockers") == EXPECTED_CLOSED, "V12 closed blockers drift")
    require(v12.get("open_execution_blockers") == [], "V12 open blocker drift")
    require(v12.get("execution_substrate_ready") is True, "V12 substrate readiness drift")
    require(v12.get("batch_ready") is False and v12.get("batch_creation_allowed") is False, "V12 must keep Batch blocked")
    require(v12.get("batch_gate") == "BLOCKED_PENDING_POST_SUBSTRATE_PRE_BATCH_AUDIT_AND_EXPLICIT_BATCH_AUTHORIZATION", "V12 Batch gate drift")
    require(v12.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V12 source-local audit marker drift")
    boundary = v12.get("freeze_serializer_boundary", {})
    require(boundary.get("serializer_does_not_create_batch") is True, "V12 serializer Batch-creation guard drift")
    require(boundary.get("serializer_does_not_persist_freeze") is True, "V12 serializer persistence guard drift")
    require(boundary.get("outcome_feedback_runtime_fields_forbidden") is True, "V12 outcome/feedback guard drift")

    for obj, label in ((contract, "contract"), (v08, "V08"), (v12, "V12")):
        require(obj.get("batch") == "NONE", f"{label} batch must remain NONE")
        require(obj.get("freeze") == "NONE", f"{label} freeze must remain NONE")
        require(obj.get("outcome") == "NONE", f"{label} outcome must remain NONE")
        require(obj.get("empirical_credit") == "NONE", f"{label} empirical credit must remain NONE")
        require(obj.get("claim_extraction") == "BLOCKED", f"{label} claim extraction must remain BLOCKED")

    require(
        not [x for x in batches if x.get("plan_id") == "K2PV-QRM-002" or x.get("hypothesis_id") == "QRM-H1"],
        "P2 production Batch exists at serializer closure",
    )
    require(
        not [x for x in freezes if x.get("plan_id") == "K2PV-QRM-002"],
        "P2 production Freeze exists at serializer closure",
    )

    evidence = v08.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit evidence drift")
    require(evidence.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run evidence drift")
    require(evidence.get("job_id") == FAIL_FIRST_JOB, "fail-first job evidence drift")
    require(evidence.get("expected_failure") == "ModuleNotFoundError: No module named 'k2_qimen_p2_freeze_serializer'", "fail-first error evidence drift")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-freeze-serializer: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-freeze-serializer: PASS")
    print(
        "closed=P2-EXEC-001..009 open=NONE negative_cases=20 "
        "byte_exact=true batch_binding=true persistence=false "
        "source_local_overgeneralization=PASS execution_substrate_ready=true "
        "batch_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
