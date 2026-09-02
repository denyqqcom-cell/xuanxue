#!/usr/bin/env python3
import copy
import hashlib
import json
import re
from datetime import datetime, timezone

REQUIRED_BOUNDARY_KINDS = {
    "LEAP_MONTH_BOUNDARY",
    "SOLAR_TERM_BOUNDARY",
    "ZI_HOUR_23_DAY_ROLLOVER",
    "EMPTY_PLATE_BOUNDARY",
}
FORBIDDEN_INPUT_KEYS = {
    "outcome",
    "feedback",
    "current_time",
    "now",
    "runtime_timestamp",
    "host_timezone",
    "process_id",
    "pid",
    "random_seed_from_system",
    "filesystem_listing_order",
}
UTC_OFFSET_RE = re.compile(r"^[+-](?:0\d|1\d|2[0-3]):[0-5]\d$")


class ReproducibilityError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise ReproducibilityError(message)


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
            raise ReproducibilityError(f"{label} contains float; exact reproducibility forbids floats")


def _reject_forbidden_keys(value, label):
    bad = sorted(
        item.lower()
        for kind, item in _walk(value)
        if kind == "key" and item.lower() in FORBIDDEN_INPUT_KEYS
    )
    _require(not bad, f"{label} contains forbidden runtime/environment field(s): {bad}")


def canonical_json(value):
    _reject_floats(value, "canonical value")
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_bytes(value):
    return canonical_json(value).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_contract(contract):
    _require(contract.get("capability") == "P2-EXEC-008", "capability drift")
    _require(contract.get("failure_policy") == "FAIL_CLOSED", "pipeline must fail closed")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")

    c = contract.get("canonicalization", {})
    _require(c.get("encoding") == "UTF-8", "canonical encoding drift")
    _require(c.get("json_sort_keys") is True, "dict key sorting is required")
    _require(c.get("json_separators") == [",", ":"], "canonical separators drift")
    _require(c.get("ensure_ascii") is False, "ensure_ascii must remain false")
    _require(c.get("allow_float") is False, "floats must remain forbidden")
    _require(c.get("allow_nan_or_infinity") is False, "NaN/Infinity must remain forbidden")
    _require(c.get("case_output_order") == "SORT_BY_FIXTURE_CASE_ID", "case ordering drift")
    _require(c.get("hash_algorithm") == "SHA256", "hash algorithm drift")
    _require(c.get("byte_for_byte_repeatability_required") is True, "byte-exact replay required")

    t = contract.get("time_and_calendar_boundary", {})
    _require(t.get("explicit_time_source_required") is True, "explicit time source required")
    _require(t.get("explicit_timezone_required") is True, "explicit timezone required")
    _require(t.get("explicit_utc_offset_required") is True, "explicit UTC offset required")
    _require(t.get("host_timezone_dependency_forbidden") is True, "host timezone dependency forbidden")
    _require(t.get("system_now_dependency_forbidden") is True, "system now dependency forbidden")
    _require(t.get("calendar_boundary_fields_frozen_input_only") is True, "calendar boundary must be frozen input")
    _require(set(t.get("required_boundary_kinds", [])) == REQUIRED_BOUNDARY_KINDS, "required boundary set drift")
    _require(
        t.get("boundary_fixture_semantics") == "REPRODUCIBILITY_SENTINEL_NOT_CALENDAR_CORRECTNESS_CLAIM",
        "boundary fixture semantics drift",
    )

    s = contract.get("seed_and_environment", {})
    _require(s.get("nondeterminism_seed_required") is True, "frozen nondeterminism seed required")
    _require(s.get("seed_frozen_in_input") is True, "seed must be frozen in input")
    _require(s.get("random_unseeded_forbidden") is True, "unseeded randomness forbidden")
    _require(s.get("locale_dependency_forbidden") is True, "locale dependency forbidden")
    _require(s.get("process_id_dependency_forbidden") is True, "process-id dependency forbidden")
    _require(s.get("filesystem_order_dependency_forbidden") is True, "filesystem-order dependency forbidden")

    out = contract.get("pipeline_output", {})
    _require(out.get("artifact_kind") == "P2_EXACT_REPRODUCIBILITY_FIXTURE_REPORT", "artifact kind drift")
    _require(out.get("include_contract_sha256") is True, "contract hash required")
    _require(out.get("include_fixture_sha256") is True, "fixture hash required")
    _require(out.get("include_case_input_sha256") is True, "case input hash required")
    _require(out.get("include_case_output_sha256") is True, "case output hash required")
    _require(out.get("runtime_timestamp_forbidden") is True, "runtime timestamp forbidden")
    _require(out.get("outcome_field_forbidden") is True, "outcome field forbidden")

    b = contract.get("source_semantics_boundary", {})
    _require(b.get("may_validate_execution_determinism_only") is True, "scope must remain determinism-only")
    _require(b.get("may_create_or_promote_qimen_semantics") is False, "pipeline cannot create Qimen semantics")
    _require(b.get("boundary_fixture_values_are_source_claims") is False, "fixture values cannot gain source credit")
    _require(b.get("boundary_fixture_values_are_empirical_claims") is False, "fixture values cannot gain empirical credit")
    _require(b.get("source_local_overgeneralization_forbidden") is True, "source-local overgeneralization guard missing")

    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def _parse_explicit_time(time_source):
    _require(isinstance(time_source, dict), "time_source must be object")
    _reject_forbidden_keys(time_source, "time_source")
    required = {"source_id", "local_datetime", "timezone", "utc_offset"}
    _require(required.issubset(time_source), "time_source missing explicit fields")
    _require(isinstance(time_source["source_id"], str) and time_source["source_id"], "source_id required")
    _require(isinstance(time_source["timezone"], str) and time_source["timezone"], "timezone required")
    offset = time_source["utc_offset"]
    _require(isinstance(offset, str) and UTC_OFFSET_RE.match(offset), "explicit utc_offset invalid")
    raw = time_source["local_datetime"]
    _require(isinstance(raw, str) and raw, "local_datetime required")
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ReproducibilityError(f"invalid local_datetime: {raw}") from exc
    _require(dt.tzinfo is not None and dt.utcoffset() is not None, "local_datetime must include explicit offset")
    actual = dt.strftime("%z")
    actual = f"{actual[:3]}:{actual[3:]}"
    _require(actual == offset, f"local_datetime offset {actual} != frozen utc_offset {offset}")
    return dt


def _normalized_fixture(fixture):
    clone = copy.deepcopy(fixture)
    clone["cases"] = sorted(clone.get("cases", []), key=lambda x: x.get("fixture_case_id", ""))
    return clone


def validate_fixture(fixture, contract):
    validate_contract(contract)
    _require(fixture.get("fixture_only") is True, "fixture_only must remain true")
    _require(
        fixture.get("boundary_semantics") == "REPRODUCIBILITY_SENTINEL_NOT_CALENDAR_CORRECTNESS_CLAIM",
        "fixture boundary semantics drift",
    )
    cases = fixture.get("cases")
    _require(isinstance(cases, list) and cases, "fixture cases required")
    _reject_floats(fixture, "fixture")
    _reject_forbidden_keys(fixture, "fixture")

    ids = []
    kinds = []
    for case in cases:
        case_id = case.get("fixture_case_id")
        frozen = case.get("frozen_input")
        _require(isinstance(case_id, str) and case_id, "fixture_case_id required")
        _require(isinstance(frozen, dict), f"{case_id}: frozen_input required")
        ids.append(case_id)
        _parse_explicit_time(frozen.get("time_source"))
        boundary = frozen.get("calendar_boundary")
        _require(isinstance(boundary, dict), f"{case_id}: calendar_boundary required")
        kind = boundary.get("boundary_kind")
        _require(kind in REQUIRED_BOUNDARY_KINDS, f"{case_id}: invalid boundary kind")
        _require(boundary.get("fixture_synthetic_label") is True, f"{case_id}: boundary must be synthetic sentinel")
        _require(isinstance(boundary.get("boundary_marker"), str) and boundary.get("boundary_marker"), f"{case_id}: boundary marker required")
        _require(isinstance(frozen.get("nondeterminism_seed"), int) and not isinstance(frozen.get("nondeterminism_seed"), bool), f"{case_id}: integer nondeterminism_seed required")
        _require(isinstance(frozen.get("question_id"), str) and frozen.get("question_id"), f"{case_id}: question_id required")
        kinds.append(kind)

    _require(len(set(ids)) == len(ids), "duplicate fixture_case_id")
    _require(set(kinds) == REQUIRED_BOUNDARY_KINDS, "fixture must cover exactly the required boundary kinds")


def fixture_sha256(fixture):
    return canonical_sha256(_normalized_fixture(fixture))


def materialize_case(case):
    case_id = case["fixture_case_id"]
    frozen = copy.deepcopy(case["frozen_input"])
    dt = _parse_explicit_time(frozen["time_source"])
    input_sha = canonical_sha256(frozen)
    body = {
        "fixture_case_id": case_id,
        "question_id": frozen["question_id"],
        "boundary_kind": frozen["calendar_boundary"]["boundary_kind"],
        "boundary_marker": frozen["calendar_boundary"]["boundary_marker"],
        "time_source_id": frozen["time_source"]["source_id"],
        "local_datetime": frozen["time_source"]["local_datetime"],
        "timezone": frozen["time_source"]["timezone"],
        "utc_offset": frozen["time_source"]["utc_offset"],
        "normalized_utc_instant": dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "nondeterminism_seed": frozen["nondeterminism_seed"],
        "payload": frozen.get("payload", {}),
        "input_sha256": input_sha,
    }
    output_sha = canonical_sha256(body)
    return {**body, "output_sha256": output_sha}


def run_pipeline(fixture, contract, expected_fixture_sha256=None):
    validate_fixture(fixture, contract)
    normalized = _normalized_fixture(fixture)
    fixture_hash = canonical_sha256(normalized)
    if expected_fixture_sha256 is not None:
        _require(fixture_hash == expected_fixture_sha256, "frozen fixture hash drift")
    cases = [materialize_case(case) for case in normalized["cases"]]
    report = {
        "artifact_kind": "P2_EXACT_REPRODUCIBILITY_FIXTURE_REPORT",
        "contract_sha256": canonical_sha256(contract),
        "fixture_sha256": fixture_hash,
        "fixture_id": fixture["fixture_id"],
        "boundary_semantics": fixture["boundary_semantics"],
        "case_count": len(cases),
        "cases": cases,
        "outcome_data_used": False,
        "source_claim_credit": "NONE",
        "empirical_credit": "NONE",
    }
    return canonical_bytes(report)
