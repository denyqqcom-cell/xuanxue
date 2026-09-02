#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_abstain_denominator_scorer as scorer_validator
from k2_qimen_p2_exact_reproducibility import (
    fixture_sha256,
    run_pipeline,
    validate_contract,
    validate_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_EXACT_REPRODUCIBILITY_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_exact_reproducibility_fixture.json"


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
    scorer_validator.validate_repository()
    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    validate_contract(contract)
    validate_fixture(fixture, contract)
    frozen_hash = fixture_sha256(fixture)
    first = run_pipeline(fixture, contract, expected_fixture_sha256=frozen_hash)
    second = run_pipeline(fixture, contract, expected_fixture_sha256=frozen_hash)
    require(first == second, "same fixture did not reproduce byte-exact output")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-exact-reproducibility: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-exact-reproducibility: PASS")


if __name__ == "__main__":
    main()
