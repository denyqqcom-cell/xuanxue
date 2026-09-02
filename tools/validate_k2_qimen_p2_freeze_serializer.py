#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_exact_reproducibility as reproducibility_validator
from k2_qimen_p2_freeze_serializer import (
    serialize_freeze_candidate,
    validate_contract,
    validate_document,
    verify_serialized_freeze,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_FREEZE_SERIALIZER_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_freeze_serializer_fixture.json"
EXPECTED_REPRO_HASH = "88968c2388163efa009640ba91c9a67b68049fcbb573d86ed725a319c3130977"


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be object: {path}")
    return value


def validate_repository():
    reproducibility_validator.validate_repository()
    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    validate_contract(contract)
    validate_document(fixture, contract, EXPECTED_REPRO_HASH)
    raw, digest = serialize_freeze_candidate(fixture, contract, EXPECTED_REPRO_HASH)
    verify_serialized_freeze(raw, digest, contract, EXPECTED_REPRO_HASH)


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-freeze-serializer: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-freeze-serializer: PASS")


if __name__ == "__main__":
    main()
