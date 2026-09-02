#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

from k2_qimen_p2_freeze_serializer import (
    FreezeSerializationError,
    canonical_sha256,
    serialize_freeze_candidate,
    validate_contract,
    validate_document,
    verify_serialized_freeze,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "knowledge" / "K2_QIMEN_P2_FREEZE_SERIALIZER_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_freeze_serializer_fixture.json"
EXPECTED_REPRO_HASH = "88968c2388163efa009640ba91c9a67b68049fcbb573d86ed725a319c3130977"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def expect_failure(fn, label):
    try:
        fn()
    except (FreezeSerializationError, ValueError, TypeError, KeyError):
        return
    raise AssertionError(f"negative case unexpectedly passed: {label}")


def main():
    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    validate_contract(contract)
    validate_document(fixture, contract, EXPECTED_REPRO_HASH)

    raw1, sha1 = serialize_freeze_candidate(fixture, contract, EXPECTED_REPRO_HASH)
    raw2, sha2 = serialize_freeze_candidate(copy.deepcopy(fixture), contract, EXPECTED_REPRO_HASH)
    assert raw1 == raw2
    assert sha1 == sha2
    envelope = verify_serialized_freeze(raw1, sha1, contract, EXPECTED_REPRO_HASH)
    assert envelope["mode"] == "FIXTURE_ONLY"
    assert envelope["production_freeze_created"] is False
    assert envelope["freeze_payload_sha256"] == canonical_sha256(fixture["freeze_payload"])

    reordered = {key: copy.deepcopy(fixture[key]) for key in reversed(list(fixture.keys()))}
    raw3, sha3 = serialize_freeze_candidate(reordered, contract, EXPECTED_REPRO_HASH)
    assert raw3 == raw1 and sha3 == sha1

    negative_cases = []

    case = copy.deepcopy(fixture)
    case["batch_binding"]["batch_created"] = False
    negative_cases.append(("batch_not_created", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    del case["batch_binding"]["batch_ref"]
    negative_cases.append(("missing_batch_ref", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["batch_binding"]["batch_sha256"] = "not-a-hash"
    negative_cases.append(("bad_batch_hash", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["batch_binding"]["production_batch"] = True
    negative_cases.append(("fixture_claims_production_batch", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["production_freeze_created"] = True
    negative_cases.append(("fixture_claims_production_freeze", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["outcome"] = "WIN"
    negative_cases.append(("outcome_field", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["batch_binding"]["feedback"] = "post-hoc"
    negative_cases.append(("feedback_field", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["complexity_budget"]["role_multiplicity_budget"] = 4.0
    negative_cases.append(("float_budget", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    del case["freeze_payload"]["reproducibility_fixture_hash"]
    negative_cases.append(("missing_repro_hash", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    negative_cases.append(("wrong_repro_hash_binding", lambda case=case: serialize_freeze_candidate(case, contract, "0" * 64)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["lane_bindings"].pop()
    negative_cases.append(("missing_lane", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["lane_bindings"][0], case["freeze_payload"]["lane_bindings"][1] = (
        case["freeze_payload"]["lane_bindings"][1],
        case["freeze_payload"]["lane_bindings"][0],
    )
    negative_cases.append(("lane_order_drift", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["mapping_boundary"]["mapping_before_plate_value_access"] = False
    negative_cases.append(("mapping_boundary_drift", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["persist"] = True
    negative_cases.append(("persist_attempt", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["batch_binding"]["runtime_timestamp"] = "2026-09-02T00:00:00Z"
    negative_cases.append(("runtime_timestamp", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["artifact_kind"] = "P2_EXECUTION_RESULT"
    negative_cases.append(("artifact_kind_drift", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["freeze_payload"]["outcome_data_used"] = True
    negative_cases.append(("outcome_data_used", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    mutated = bytearray(raw1)
    mutated[-1] = ord(" ")
    negative_cases.append(("byte_mutation", lambda: verify_serialized_freeze(bytes(mutated), sha1, contract, EXPECTED_REPRO_HASH)))

    noncanonical = raw1 + b"\n"
    import hashlib
    noncanonical_sha = hashlib.sha256(noncanonical).hexdigest()
    negative_cases.append(("noncanonical_bytes", lambda: verify_serialized_freeze(noncanonical, noncanonical_sha, contract, EXPECTED_REPRO_HASH)))

    case = copy.deepcopy(fixture)
    case["fixture_only"] = False
    negative_cases.append(("production_candidate_without_production_batch", lambda case=case: validate_document(case, contract, EXPECTED_REPRO_HASH)))

    for label, fn in negative_cases:
        expect_failure(fn, label)

    print(
        "k2-qimen-p2-freeze-serializer-tests: PASS "
        f"negative_cases={len(negative_cases)} byte_exact=true batch_binding=true persistence=false"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"k2-qimen-p2-freeze-serializer-tests: FAIL: {exc}", file=sys.stderr)
        raise
