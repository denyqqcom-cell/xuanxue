#!/usr/bin/env python3
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_k2_qimen_cognitive_reconstruction as v
import test_k2_qimen_epistemic_debt as epistemic_debt_test


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def validate_theory_map_text(text):
    """Minimal guard only: the map is a synthesis index, never an empirical authority."""
    issues = []
    required_markers = {
        "NO_EMPIRICAL_CREDIT": "theory map must remain no-empirical-credit",
        "Claim Extraction：`BLOCKED`": "theory map must keep claim extraction blocked",
        "UNRESOLVED / PROSPECTIVE_COMPARISON_REQUIRED": "theory map must preserve unresolved competing models",
        "DO_NOT_FORCE-RESOLVE": "theory map must preserve source-local ontology conflicts",
        "不把本地图自身当作原创理论验证结果": "theory map must reject self-validation",
    }
    for marker, message in required_markers.items():
        if marker not in text:
            issues.append(message)
    return issues


def main():
    # Authoritative repository state must pass first.
    issues = v.validate(ROOT)
    assert not issues, issues

    state = load_json(ROOT / "knowledge" / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json")
    backlog = load_json(ROOT / "knowledge" / "K2_UNKNOWN_TEXTUAL_BACKLOG.json")
    deep = load_jsonl(ROOT / "knowledge" / "K2_DEEP_READING_LEDGER.jsonl")
    biases = load_jsonl(ROOT / "knowledge" / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl")

    # Fail closed: corpus mastery cannot be asserted while the machine backlog is nonzero.
    broken = copy.deepcopy(state)
    broken["full_corpus_mastery_claim"] = True
    issues = v.validate_state(broken, backlog, deep, biases)
    assert any("full corpus mastery" in x for x in issues), issues

    # Fail closed: reconstruction infrastructure never grants empirical credit.
    broken = copy.deepcopy(state)
    broken["empirical_credit"] = "VALIDATED"
    issues = v.validate_state(broken, backlog, deep, biases)
    assert any("empirical credit" in x for x in issues), issues

    # Fail closed: deep reading count is derived from the reviewed visual ledger, not hand-entered.
    broken = copy.deepcopy(state)
    broken["deep_visual_reviewed_source_count"] += 1
    issues = v.validate_state(broken, backlog, deep, biases)
    assert any("deep_visual_reviewed_source_count drift" in x for x in issues), issues

    # Fail closed: UNKNOWN backlog accounting is linked, not narrative metadata.
    broken = copy.deepcopy(state)
    broken["global_unknown_textual_backlog"] = 0
    issues = v.validate_state(broken, backlog, deep, biases)
    assert any("state/backlog count drift" in x for x in issues), issues

    # Fail closed: historical error ledger cannot rewrite a past bias as empirical validation.
    bad_biases = copy.deepcopy(biases)
    bad_biases[0]["empirical_credit"] = "SUPPORTED"
    issues = v.validate_bias_rows(bad_biases, ROOT)
    assert any("cannot grant empirical credit" in x for x in issues), issues

    # Fail closed: the ledger must preserve category breadth and unresolved residual risk.
    all_corrected = copy.deepcopy(biases)
    for row in all_corrected:
        row["correction_status"] = "CORRECTED"
    issues = v.validate_bias_rows(all_corrected, ROOT)
    assert any("all-corrected state" in x for x in issues), issues

    # Fail closed: SCRM cannot remove rival explanations, counterfactuals or sensitivity checks.
    schema = load_json(ROOT / "knowledge" / "schema" / "qimen_scenario_reasoning.schema.json")
    broken_schema = copy.deepcopy(schema)
    broken_schema["properties"]["competing_explanations"]["minItems"] = 1
    issues = v.validate_scenario_schema(broken_schema)
    assert any("at least two competing explanations" in x for x in issues), issues

    broken_schema = copy.deepcopy(schema)
    broken_schema["properties"]["counterfactual_checks"]["minItems"] = 0
    issues = v.validate_scenario_schema(broken_schema)
    assert any("counterfactual" in x for x in issues), issues

    broken_schema = copy.deepcopy(schema)
    broken_schema["properties"]["sensitivity_checks"]["minItems"] = 0
    issues = v.validate_scenario_schema(broken_schema)
    assert any("sensitivity" in x for x in issues), issues

    # Fail closed: multi-output decisions must carry an explicit tie-break contract.
    broken_schema = copy.deepcopy(schema)
    broken_schema["required"].remove("decision_tie_break_policy")
    issues = v.validate_scenario_schema(broken_schema)
    assert any("required-field contract drift" in x for x in issues), issues

    broken_schema = copy.deepcopy(schema)
    broken_schema["properties"]["decision_tie_break_policy"]["allOf"] = []
    issues = v.validate_scenario_schema(broken_schema)
    assert any("fail closed for multi-output selection" in x for x in issues), issues

    # Minimal theory-map closure: it is a source-grounded research index, not a new authority.
    theory_map_path = ROOT / "knowledge" / "K2_QIMEN_THEORY_MAP_V1.md"
    assert theory_map_path.exists(), "missing K2_QIMEN_THEORY_MAP_V1.md"
    theory_map = theory_map_path.read_text(encoding="utf-8")
    issues = validate_theory_map_text(theory_map)
    assert not issues, issues

    broken_map = theory_map.replace("NO_EMPIRICAL_CREDIT", "EMPIRICAL_CREDIT_GRANTED", 1)
    issues = validate_theory_map_text(broken_map)
    assert any("no-empirical-credit" in x for x in issues), issues

    broken_map = theory_map.replace(
        "UNRESOLVED / PROSPECTIVE_COMPARISON_REQUIRED",
        "RESOLVED_BY_EDITORIAL_PREFERENCE",
        1,
    )
    issues = validate_theory_map_text(broken_map)
    assert any("unresolved competing models" in x for x in issues), issues

    broken_map = theory_map.replace("DO_NOT_FORCE-RESOLVE", "FORCE_NORMALIZED", 1)
    issues = validate_theory_map_text(broken_map)
    assert any("source-local ontology conflicts" in x for x in issues), issues

    # Second-order closure: a bias that was already recognized must not re-enter
    # the theory under a new label without creating and discharging epistemic debt.
    epistemic_debt_test.main()

    print("k2-qimen-cognitive-reconstruction-tests: PASS")


if __name__ == "__main__":
    main()
