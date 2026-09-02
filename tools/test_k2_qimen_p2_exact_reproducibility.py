#!/usr/bin/env python3
import copy
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from k2_qimen_p2_exact_reproducibility import (
    ReproducibilityError,
    fixture_sha256,
    run_pipeline,
    validate_contract,
    validate_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_EXACT_REPRODUCIBILITY_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_exact_reproducibility_fixture.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def expect_fail(name, fn):
    try:
        fn()
    except ReproducibilityError:
        return
    raise AssertionError(f"negative case did not fail: {name}")


def reordered_dict(value):
    if isinstance(value, dict):
        return {k: reordered_dict(value[k]) for k in reversed(list(value.keys()))}
    if isinstance(value, list):
        return [reordered_dict(x) for x in value]
    return value


def main():
    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)

    validate_contract(contract)
    validate_fixture(fixture, contract)

    baseline_hash = fixture_sha256(fixture)
    first = run_pipeline(fixture, contract, expected_fixture_sha256=baseline_hash)
    second = run_pipeline(copy.deepcopy(fixture), copy.deepcopy(contract), expected_fixture_sha256=baseline_hash)
    assert first == second, "repeat execution bytes differ"

    reordered = reordered_dict(copy.deepcopy(fixture))
    reordered["cases"] = list(reversed(reordered["cases"]))
    reordered_bytes = run_pipeline(reordered, reordered_dict(copy.deepcopy(contract)), expected_fixture_sha256=baseline_hash)
    assert reordered_bytes == first, "dict/case insertion order changed canonical bytes"

    old_tz = os.environ.get("TZ")
    try:
        os.environ["TZ"] = "UTC"
        if hasattr(time, "tzset"):
            time.tzset()
        utc_bytes = run_pipeline(copy.deepcopy(fixture), contract, expected_fixture_sha256=baseline_hash)
        os.environ["TZ"] = "America/New_York"
        if hasattr(time, "tzset"):
            time.tzset()
        ny_bytes = run_pipeline(copy.deepcopy(fixture), contract, expected_fixture_sha256=baseline_hash)
        assert utc_bytes == ny_bytes == first, "host timezone changed canonical output"
    finally:
        if old_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old_tz
        if hasattr(time, "tzset"):
            time.tzset()

    negative_cases = []

    c = copy.deepcopy(contract)
    c["canonicalization"]["json_sort_keys"] = False
    negative_cases.append(("dict_order_contract_disabled", lambda c=c: validate_contract(c)))

    c = copy.deepcopy(contract)
    c["canonicalization"]["allow_float"] = True
    negative_cases.append(("float_contract_enabled", lambda c=c: validate_contract(c)))

    f = copy.deepcopy(fixture)
    f["cases"] = f["cases"][:-1]
    negative_cases.append(("missing_required_boundary_case", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["payload"]["nondeterministic_float"] = 0.1
    negative_cases.append(("float_payload", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["time_source"]["local_datetime"] = "2030-01-01T12:00:00"
    negative_cases.append(("local_datetime_without_offset", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["time_source"]["utc_offset"] = "+09:00"
    negative_cases.append(("utc_offset_mismatch", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    del f["cases"][0]["frozen_input"]["time_source"]["timezone"]
    negative_cases.append(("missing_explicit_timezone", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["time_source"]["host_timezone"] = "SYSTEM"
    negative_cases.append(("host_timezone_dependency", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["now"] = "runtime"
    negative_cases.append(("system_now_dependency", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    del f["cases"][0]["frozen_input"]["nondeterminism_seed"]
    negative_cases.append(("missing_frozen_seed", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["runtime_timestamp"] = "2030-01-01T00:00:00Z"
    negative_cases.append(("runtime_timestamp_in_input", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["outcome"] = "KNOWN"
    negative_cases.append(("outcome_in_reproducibility_input", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][1]["fixture_case_id"] = f["cases"][0]["fixture_case_id"]
    negative_cases.append(("duplicate_fixture_case_id", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["calendar_boundary"]["boundary_kind"] = "UNKNOWN_BOUNDARY"
    negative_cases.append(("unknown_boundary_kind", lambda f=f: validate_fixture(f, contract)))

    f = copy.deepcopy(fixture)
    f["cases"][0]["frozen_input"]["nondeterminism_seed"] += 1
    negative_cases.append((
        "post_freeze_seed_mutation",
        lambda f=f: run_pipeline(f, contract, expected_fixture_sha256=baseline_hash),
    ))

    f = copy.deepcopy(fixture)
    f["fixture_only"] = False
    negative_cases.append(("fixture_promoted_to_production_claim", lambda f=f: validate_fixture(f, contract)))

    for name, fn in negative_cases:
        expect_fail(name, fn)

    assert len(negative_cases) == 16
    print(
        "k2-qimen-p2-exact-reproducibility-tests: PASS "
        "negative_cases=16 boundary_cases=4 byte_exact=true "
        "dict_order_invariant=true host_timezone_invariant=true"
    )


if __name__ == "__main__":
    main()
