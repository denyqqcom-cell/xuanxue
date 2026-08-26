#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
PROTOCOL = K / "K2_QIMEN_PRACTICE_INPUT_INTEGRITY_PROTOCOL.md"
MAPPING_SCHEMA = K / "schema" / "qimen_symbolic_mapping.schema.json"
SCENARIO_SCHEMA = K / "schema" / "qimen_scenario_reasoning.schema.json"

REQUIRED_MAPPING_FIELDS = {
    "world_variable",
    "candidate_symbolic_role",
    "symbol_type",
    "symbol_value",
    "plate_layer",
    "palace",
    "dun_mode",
    "readback_status",
    "source_method_basis",
    "plate_layer_semantics",
    "semantics_status",
    "alternatives",
    "boundary",
    "failure_condition",
    "instance_collapse_blocked",
}
REQUIRED_PLATE_VALUES = {
    "SKY_PLATE",
    "EARTH_PLATE",
    "OTHER_EXPLICIT_LAYER",
    "NOT_APPLICABLE",
    "UNRESOLVED",
}
REQUIRED_DUN_VALUES = {"YANG_DUN", "YIN_DUN", "NOT_APPLICABLE", "UNRESOLVED"}
REQUIRED_READBACK_VALUES = {"VERIFIED", "SINGLE_READ", "CONTESTED", "NOT_APPLICABLE"}
REQUIRED_SEMANTICS_VALUES = {"SOURCE_LOCAL", "UNRESOLVED", "NOT_APPLICABLE"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(repo: Path = ROOT):
    k = repo / "knowledge"
    protocol_path = k / "K2_QIMEN_PRACTICE_INPUT_INTEGRITY_PROTOCOL.md"
    mapping_path = k / "schema" / "qimen_symbolic_mapping.schema.json"
    scenario_path = k / "schema" / "qimen_scenario_reasoning.schema.json"
    missing = [str(p.relative_to(repo)) for p in (protocol_path, mapping_path, scenario_path) if not p.exists()]
    if missing:
        return [f"missing practice-input artifact(s): {missing}"]

    issues = []
    protocol = protocol_path.read_text(encoding="utf-8")
    mapping = load_json(mapping_path)
    scenario = load_json(scenario_path)

    for needle in (
        "FREEZE INTEGRITY != INPUT CORRECTNESS",
        "SYMBOL TYPE != SYMBOL INSTANCE",
        "SAME STEM != SAME STATE",
        "DUN MODE != ROTATION DIRECTION ONLY",
        "PLATE LAYER TAG != PLATE LAYER SEMANTICS",
        "DETERMINISTIC MULTI-OUTPUT != UNIQUE DECISION",
        "instance_collapse_blocked=true",
        "Empirical Credit 始终保持：`NONE`",
    ):
        if needle not in protocol:
            issues.append(f"practice input protocol missing invariant: {needle}")

    if mapping.get("$id") != "qimen_symbolic_mapping.schema.json":
        issues.append("symbolic mapping schema id mismatch")
    if mapping.get("type") != "object" or mapping.get("additionalProperties") is not False:
        issues.append("symbolic mapping must be closed object")
    required = mapping.get("required")
    if not isinstance(required, list) or not REQUIRED_MAPPING_FIELDS.issubset(set(required)):
        issues.append("symbolic mapping required-field contract incomplete")
    props = mapping.get("properties") if isinstance(mapping.get("properties"), dict) else {}
    if set(props.get("plate_layer", {}).get("enum", [])) != REQUIRED_PLATE_VALUES:
        issues.append("plate_layer enum drift")
    if set(props.get("dun_mode", {}).get("enum", [])) != REQUIRED_DUN_VALUES:
        issues.append("dun_mode enum drift")
    if set(props.get("readback_status", {}).get("enum", [])) != REQUIRED_READBACK_VALUES:
        issues.append("readback_status enum drift")
    if set(props.get("semantics_status", {}).get("enum", [])) != REQUIRED_SEMANTICS_VALUES:
        issues.append("semantics_status enum drift")
    if props.get("instance_collapse_blocked", {}).get("const") is not True:
        issues.append("same-symbol instance collapse must remain blocked")

    sprops = scenario.get("properties") if isinstance(scenario.get("properties"), dict) else {}
    mappings = sprops.get("symbolic_mapping_hypotheses") if isinstance(sprops.get("symbolic_mapping_hypotheses"), dict) else {}
    if mappings.get("type") != "array" or mappings.get("minItems", 0) < 1:
        issues.append("scenario must require at least one symbolic mapping hypothesis")
    if mappings.get("items", {}).get("$ref") != "qimen_symbolic_mapping.schema.json":
        issues.append("scenario symbolic mappings must bind qimen_symbolic_mapping schema")
    tie = sprops.get("decision_tie_break_policy") if isinstance(sprops.get("decision_tie_break_policy"), dict) else {}
    if tie.get("type") != "object" or tie.get("additionalProperties") is not False:
        issues.append("scenario decision tie-break policy must be closed object")
    if sprops.get("empirical_credit", {}).get("const") != "NONE":
        issues.append("practice input integrity cannot grant empirical credit")
    return issues


def main():
    try:
        issues = validate(ROOT)
    except Exception as exc:
        print(f"k2-qimen-practice-input-integrity: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if issues:
        print("k2-qimen-practice-input-integrity: FAIL", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-practice-input-integrity: PASS")
    print("plate_layer_tagging=true dun_mode_tagging=true instance_collapse_blocked=true tie_break_freeze=true empirical_credit=NONE")


if __name__ == "__main__":
    main()
