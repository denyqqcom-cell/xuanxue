#!/usr/bin/env python3
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_FACTOR_LAYER_CROSSWALK_AUDIT_V01.json"
EVIDENCE = ROOT / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl"

EXPECTED_FACTORS = ["天时", "地利", "人和", "神助", "格局"]
EXPECTED_LAYERS = ["奇仪", "八门", "八神", "九星"]
REQUIRED_EVIDENCE = {
    "K2E-W1-QM-0003-0065",
    "K2E-W1-QM-0021-0239",
    "K2E-W1-QM-0021-0249",
    "K2E-W1-QM-0021-0347",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def evidence_ids():
    ids = set()
    with EVIDENCE.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("evidence_id"):
                ids.add(row["evidence_id"])
    return ids


def validate(audit, known_ids):
    require(audit.get("audit_id") == "K2-QIMEN-P2-FACTOR-LAYER-CROSSWALK-AUDIT-V01", "wrong audit id")
    require(audit.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "domain drift")
    require(audit.get("source_inputs") == ["QM-SRC-0003", "QM-SRC-0021"], "source panel drift")
    require(set(audit.get("source_evidence_refs", [])) == REQUIRED_EVIDENCE, "source evidence set drift")
    require(REQUIRED_EVIDENCE <= known_ids, "required evidence ids missing from reviewed evidence ledger")

    ontology = audit.get("ontology_audit", {})
    require(ontology.get("qm_src_0021_factor_ontology") == EXPECTED_FACTORS, "0021 factor ontology drift")
    require(ontology.get("current_p2_layer_vocabulary") == EXPECTED_LAYERS, "P2 layer vocabulary drift")
    require(ontology.get("qm_src_0003_fixed_priority") == EXPECTED_LAYERS, "0003 fixed priority drift")
    require(ontology.get("exact_factor_layer_crosswalk") == "NOT_ESTABLISHED", "exact crosswalk must remain unestablished")
    require(ontology.get("silent_crosswalk_forbidden") is True, "silent crosswalk must be forbidden")
    require(ontology.get("semantic_resemblance_is_not_equivalence") is True, "semantic resemblance cannot be promoted to equivalence")

    entries = ontology.get("factor_entries", [])
    require([e.get("factor_id") for e in entries] == EXPECTED_FACTORS, "factor entries must preserve all five factors")
    by_factor = {e["factor_id"]: e for e in entries}
    for factor in ("天时", "人和", "神助"):
        entry = by_factor[factor]
        require(entry.get("status") == "UNRESOLVED_SEMANTIC_RESEMBLANCE_ONLY", f"{factor} must remain unresolved")
        require(entry.get("candidate_layer") in {"九星", "八门", "八神"}, f"{factor} candidate layer missing")
        require(entry.get("equivalence_claimed") is False, f"{factor} cannot claim equivalence")
        require(entry.get("basis") == "SEMANTIC_RESEMBLANCE_ONLY_NOT_SOURCE_EQUIVALENCE", f"{factor} basis drift")
    require(by_factor["天时"].get("candidate_layer") == "九星", "天时 candidate drift")
    require(by_factor["人和"].get("candidate_layer") == "八门", "人和 candidate drift")
    require(by_factor["神助"].get("candidate_layer") == "八神", "神助 candidate drift")

    dili = by_factor["地利"]
    require(dili.get("status") == "UNMATCHED_FIRST_CLASS_SPATIAL_FACTOR", "地利 must stay unmatched first-class")
    require(dili.get("candidate_layer") is None, "地利 cannot be arbitrarily mapped")
    require(dili.get("equivalence_claimed") is False, "地利 cannot claim equivalence")

    geju = by_factor["格局"]
    require(geju.get("status") == "COMPOSITE_UNRESOLVED", "格局 must remain composite unresolved")
    require(geju.get("candidate_layer") is None, "格局 cannot be collapsed to a single layer")
    require(geju.get("equivalence_claimed") is False, "格局 cannot claim equivalence")
    require(geju.get("decomposition_source_grounded") is False, "格局 decomposition is not source-grounded")

    layer_coverage = ontology.get("layer_coverage", {})
    require(layer_coverage.get("奇仪") == "NO_EXACT_QM_SRC_0021_FACTOR_MATCH", "奇仪 unmatched status drift")
    require(layer_coverage.get("九星") == "SEMANTIC_CANDIDATE_ONLY", "九星 status drift")
    require(layer_coverage.get("八门") == "SEMANTIC_CANDIDATE_ONLY", "八门 status drift")
    require(layer_coverage.get("八神") == "SEMANTIC_CANDIDATE_ONLY", "八神 status drift")

    freeze = audit.get("freeze_and_contamination_guards", {})
    require(freeze.get("crosswalk_must_be_frozen_before_plate_values") is True, "crosswalk must freeze before plate values")
    require(freeze.get("plate_values_allowed_for_crosswalk_selection") is False, "plate values cannot select crosswalk")
    require(freeze.get("outcome_or_feedback_allowed_for_crosswalk_selection") is False, "outcome/feedback cannot select crosswalk")
    require(freeze.get("post_feedback_crosswalk_switch") == "CONTAMINATION_FAIL_CLOSED", "post-feedback switch must fail closed")

    decision = audit.get("production_decision", {})
    for key in (
        "production_representation_materialization_allowed",
        "production_complexity_profile_materialization_allowed",
        "production_abstention_profile_materialization_allowed",
        "statistical_preregistration_allowed",
        "batch_creation_allowed",
    ):
        require(decision.get(key) is False, f"{key} must remain false")
    require(decision.get("next_blocker") == "P2-ONTOLOGY-002_DECIDE_ADDITIVE_REPRESENTATION_V02_OR_ALTERNATE_DOMAIN", "next blocker drift")

    require(audit.get("source_local_overgeneralization_check") == "PASS", "source-local overgeneralization guard failed")
    require(audit.get("outcome_data_used") is False, "outcome data must not be used")
    require(audit.get("batch") == "NONE", "Batch must remain NONE")
    require(audit.get("freeze") == "NONE", "Freeze must remain NONE")
    require(audit.get("outcome") == "NONE", "Outcome must remain NONE")
    require(audit.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(audit.get("claim_extraction") == "BLOCKED", "Claim Extraction must remain blocked")


def expect_fail(base, known_ids, mutate):
    candidate = copy.deepcopy(base)
    mutate(candidate)
    try:
        validate(candidate, known_ids)
    except AssertionError:
        return
    raise AssertionError("negative case unexpectedly passed")


def main():
    require(AUDIT.exists(), "missing factor/layer crosswalk audit artifact")
    require(EVIDENCE.exists(), "missing reviewed Qimen evidence ledger")
    known_ids = evidence_ids()
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(audit, known_ids)

    cases = [
        lambda x: x["ontology_audit"].__setitem__("exact_factor_layer_crosswalk", "ESTABLISHED"),
        lambda x: x["ontology_audit"]["factor_entries"][0].__setitem__("equivalence_claimed", True),
        lambda x: x["ontology_audit"]["factor_entries"][0].__setitem__("basis", "SOURCE_EQUIVALENCE"),
        lambda x: x["ontology_audit"]["factor_entries"].pop(1),
        lambda x: x["ontology_audit"]["factor_entries"][1].__setitem__("candidate_layer", "八门"),
        lambda x: x["ontology_audit"]["factor_entries"][4].__setitem__("status", "ATOMIC_LAYER"),
        lambda x: x["ontology_audit"]["factor_entries"][4].__setitem__("candidate_layer", "奇仪"),
        lambda x: x["ontology_audit"]["layer_coverage"].__setitem__("奇仪", "EXACT_MATCH"),
        lambda x: x["freeze_and_contamination_guards"].__setitem__("plate_values_allowed_for_crosswalk_selection", True),
        lambda x: x["freeze_and_contamination_guards"].__setitem__("outcome_or_feedback_allowed_for_crosswalk_selection", True),
        lambda x: x["production_decision"].__setitem__("production_representation_materialization_allowed", True),
        lambda x: x.__setitem__("empirical_credit", "POSITIVE"),
        lambda x: x.__setitem__("batch", "CREATED"),
        lambda x: x.__setitem__("source_evidence_refs", ["K2E-W1-QM-0003-0065"]),
        lambda x: x.__setitem__("source_local_overgeneralization_check", "FAIL"),
        lambda x: x["production_decision"].__setitem__("batch_creation_allowed", True),
    ]
    for mutate in cases:
        expect_fail(audit, known_ids, mutate)

    print(
        "k2-qimen-p2-factor-layer-crosswalk-audit: PASS "
        f"negative_cases={len(cases)} exact_crosswalk=NOT_ESTABLISHED "
        "unmatched=地利 composite_unresolved=格局 production_representation=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
