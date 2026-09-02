#!/usr/bin/env python3
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "knowledge" / "K2_QIMEN_P2_ONTOLOGY_DECISION_V01.json"
PRIOR_AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_FACTOR_LAYER_CROSSWALK_AUDIT_V01.json"
EVIDENCE = ROOT / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl"

REQUIRED_EVIDENCE = {
    "K2E-W1-QM-0003-0065",
    "K2E-W1-QM-0021-0007",
    "K2E-W1-QM-0021-0239",
    "K2E-W1-QM-0021-0346",
    "K2E-W1-QM-0021-0347",
}
EXPECTED_ATOMIC_UNIVERSE = ["奇仪", "八门", "八神", "九星", "九宫"]
EXPECTED_0003_PRIORITY = ["奇仪", "八门", "八神", "九星"]
EXPLICIT_0021_FACTOR_MAP = {
    "天时": "九星",
    "地利": "九宫",
    "人和": "八门",
    "神助": "八神",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_evidence():
    rows = {}
    with EVIDENCE.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            eid = row.get("evidence_id")
            if eid:
                rows[eid] = row
    return rows


def validate(decision, evidence_rows):
    require(decision.get("decision_id") == "K2-QIMEN-P2-ONTOLOGY-DECISION-V01", "wrong decision id")
    require(decision.get("capability") == "P2-ONTOLOGY-002", "wrong capability")
    require(decision.get("plan_id") == "K2PV-QRM-002", "plan drift")
    require(decision.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    require(decision.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "domain drift before re-audit")
    require(decision.get("prior_audit_ref") == "knowledge/K2_QIMEN_P2_FACTOR_LAYER_CROSSWALK_AUDIT_V01.json", "prior audit ref drift")
    require(set(decision.get("source_evidence_refs", [])) == REQUIRED_EVIDENCE, "source evidence set drift")
    require(REQUIRED_EVIDENCE <= set(evidence_rows), "required evidence missing")

    e0007 = evidence_rows["K2E-W1-QM-0021-0007"].get("normalized_fact", "")
    for token in ("九星天盘", "九宫地盘", "八门人盘", "八神神盘", "天时", "地利", "人和", "神助"):
        require(token in e0007, f"0021-0007 no longer supports explicit structure token: {token}")
    e0346 = evidence_rows["K2E-W1-QM-0021-0346"].get("normalized_fact", "")
    for token in ("星", "门", "神", "仪", "九宫"):
        require(token in e0346, f"0021-0346 missing condition-layer token: {token}")
    e0065 = evidence_rows["K2E-W1-QM-0003-0065"].get("normalized_fact", "")
    for token in EXPECTED_0003_PRIORITY:
        require(token in e0065, f"0003-0065 missing priority token: {token}")

    correction = decision.get("self_correction", {})
    require(correction.get("status") == "P2_ONTOLOGY_001_PARTIAL_CONCLUSION_SUPERSEDED", "self-correction status drift")
    require(correction.get("reason") == "OVERLOOKED_EXPLICIT_QM_SRC_0021_FOUR_PLATE_FACTOR_STRUCTURE", "self-correction reason drift")
    require(correction.get("prior_audit_preserved_as_historical_record") is True, "prior audit must be preserved")
    require(correction.get("silent_rewrite_forbidden") is True, "silent rewrite must be forbidden")
    require(correction.get("empirical_credit_delta") == "NONE", "source correction cannot create empirical credit")

    crosswalk = decision.get("source_grounded_crosswalk", {})
    require(crosswalk.get("status") == "PARTIAL_EXACT_STRUCTURE_ESTABLISHED_FULL_ONTOLOGY_NOT_ISOMORPHIC", "crosswalk status drift")
    entries = crosswalk.get("explicit_factor_component_map", [])
    require(len(entries) == 4, "must preserve four explicit factor/component relations")
    got = {e.get("factor_id"): e for e in entries}
    require(set(got) == set(EXPLICIT_0021_FACTOR_MAP), "explicit factor set drift")
    for factor, component in EXPLICIT_0021_FACTOR_MAP.items():
        entry = got[factor]
        require(entry.get("component_id") == component, f"{factor} component drift")
        require(entry.get("status") == "SOURCE_EXPLICIT_STRUCTURE", f"{factor} must be source explicit")
        require(entry.get("source_ref") == "K2E-W1-QM-0021-0007", f"{factor} source ref drift")
        require(entry.get("equivalence_scope") == "QM_SRC_0021_FOUR_PLATE_ANALYSIS_ROLE", f"{factor} equivalence scope drift")
    require(crosswalk.get("格局") == "DERIVED_COMPOSITE_NOT_ATOMIC_LAYER", "格局 must remain composite")
    require(crosswalk.get("奇仪") == "ATOMIC_CONTEXT_COMPONENT_NO_FIVE_FACTOR_EQUIVALENT", "奇仪 status drift")
    require(crosswalk.get("full_five_factor_to_existing_four_layer_isomorphism") is False, "full isomorphism must remain false")

    architecture = decision.get("architecture_decision", {})
    require(architecture.get("decision") == "BUILD_SHARED_SUPERSET_REPRESENTATION_V02", "wrong ontology route")
    require(architecture.get("rejected_route") == "SWITCH_DOMAIN_ONLY_TO_AVOID_ONTOLOGY_MISMATCH", "rejected route drift")
    require(architecture.get("shared_atomic_context_universe") == EXPECTED_ATOMIC_UNIVERSE, "shared atomic universe drift")
    require(architecture.get("derived_composites") == ["格局"], "derived composite set drift")
    require(architecture.get("same_feature_universe_all_lanes") is True, "lane feature universe must be shared")
    require(architecture.get("lane_specific_feature_vocabulary_forbidden") is True, "lane-specific vocabulary must be forbidden")
    require(architecture.get("格局_may_not_be_counted_as_atomic_layer") is True, "格局 cannot become atomic layer")
    require(architecture.get("九宫_may_not_be_dropped") is True, "九宫 cannot be dropped")

    policies = decision.get("priority_policy_implications", {})
    for lane in ("P2-A", "P2-A_PRIME"):
        lane_policy = policies.get(lane, {})
        require(lane_policy.get("source_ranked_subset") == EXPECTED_0003_PRIORITY, f"{lane} fixed priority drift")
        require(lane_policy.get("visible_but_unranked_context") == ["九宫"], f"{lane} must keep 九宫 visible but unranked")
        require(lane_policy.get("invent_rank_for_九宫_forbidden") is True, f"{lane} cannot invent 九宫 rank")
    b_policy = policies.get("P2-B", {})
    require(b_policy.get("source_priority_form") == "QUESTION_DOMAIN_CONDITIONED_PARTIAL_PRIORITY_OR_PRIMARY_LAYER", "P2-B policy form drift")
    require(b_policy.get("workplace_total_order_status") == "NOT_SOURCE_ESTABLISHED", "workplace total order must remain unestablished")
    require(b_policy.get("unsupported_total_order_action") == "ABSTAIN_FAIL_CLOSED", "unsupported total order must abstain")
    require(b_policy.get("outcome_selected_priority_forbidden") is True, "outcome-selected priority must remain forbidden")

    estimand = decision.get("estimand_guard", {})
    require(estimand.get("C2_only_priority_policy_may_differ") is True, "C2 estimand guard drift")
    require(estimand.get("shared_feature_visibility_required") is True, "feature visibility parity required")
    require(estimand.get("representation_v02_must_precede_domain_parity_rerun") is True, "V02 must precede parity rerun")
    require(estimand.get("production_profile_materialization_before_parity_rerun") == "FORBIDDEN", "production profile must remain forbidden")

    gate = decision.get("pre_batch_gate", {})
    require(gate.get("p2_ontology_002") == "CLOSED_ARCHITECTURE_DECISION", "ontology decision not closed")
    require(gate.get("representation_v02_design_authorized") is True, "V02 design should be authorized")
    require(gate.get("production_representation_materialized") is False, "production representation must not be materialized here")
    require(gate.get("domain_source_parity_ready") is False, "domain parity must be rerun")
    require(gate.get("statistical_preregistration_ready") is False, "statistical prereg must remain false")
    require(gate.get("batch_creation_allowed") is False, "Batch creation must remain false")
    require(gate.get("next_required_work") == "P2-PREBATCH-REP-001_SHARED_SUPERSET_REPRESENTATION_V02_CONTRACT_AND_FAIL_FIRST", "next work drift")

    require(decision.get("outcome_data_used") is False, "outcome data must not be used")
    require(decision.get("batch") == "NONE", "Batch must remain NONE")
    require(decision.get("freeze") == "NONE", "Freeze must remain NONE")
    require(decision.get("outcome") == "NONE", "Outcome must remain NONE")
    require(decision.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(decision.get("claim_extraction") == "BLOCKED", "Claim Extraction must remain blocked")


def expect_fail(base, evidence_rows, mutate):
    candidate = copy.deepcopy(base)
    mutate(candidate)
    try:
        validate(candidate, evidence_rows)
    except AssertionError:
        return
    raise AssertionError("negative case unexpectedly passed")


def main():
    require(PRIOR_AUDIT.exists(), "missing preserved P2-ONTOLOGY-001 audit")
    require(EVIDENCE.exists(), "missing reviewed evidence ledger")
    require(DECISION.exists(), "missing P2-ONTOLOGY-002 decision artifact")
    prior = json.loads(PRIOR_AUDIT.read_text(encoding="utf-8"))
    require(prior.get("audit_id") == "K2-QIMEN-P2-FACTOR-LAYER-CROSSWALK-AUDIT-V01", "historical audit identity drift")
    evidence_rows = load_evidence()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    validate(decision, evidence_rows)

    cases = [
        lambda x: x["self_correction"].__setitem__("status", "NO_CORRECTION"),
        lambda x: x["self_correction"].__setitem__("prior_audit_preserved_as_historical_record", False),
        lambda x: x["source_grounded_crosswalk"]["explicit_factor_component_map"][0].__setitem__("status", "SEMANTIC_RESEMBLANCE_ONLY"),
        lambda x: x["source_grounded_crosswalk"]["explicit_factor_component_map"][1].__setitem__("component_id", "八门"),
        lambda x: x["source_grounded_crosswalk"].__setitem__("格局", "ATOMIC_LAYER"),
        lambda x: x["source_grounded_crosswalk"].__setitem__("full_five_factor_to_existing_four_layer_isomorphism", True),
        lambda x: x["architecture_decision"]["shared_atomic_context_universe"].remove("九宫"),
        lambda x: x["architecture_decision"]["shared_atomic_context_universe"].append("格局"),
        lambda x: x["architecture_decision"].__setitem__("same_feature_universe_all_lanes", False),
        lambda x: x["architecture_decision"].__setitem__("lane_specific_feature_vocabulary_forbidden", False),
        lambda x: x["priority_policy_implications"]["P2-A"]["source_ranked_subset"].append("九宫"),
        lambda x: x["priority_policy_implications"]["P2-B"].__setitem__("workplace_total_order_status", "ESTABLISHED"),
        lambda x: x["priority_policy_implications"]["P2-B"].__setitem__("unsupported_total_order_action", "INVENT_ORDER"),
        lambda x: x["estimand_guard"].__setitem__("shared_feature_visibility_required", False),
        lambda x: x["pre_batch_gate"].__setitem__("production_representation_materialized", True),
        lambda x: x["pre_batch_gate"].__setitem__("batch_creation_allowed", True),
        lambda x: x.__setitem__("empirical_credit", "POSITIVE"),
        lambda x: x.__setitem__("batch", "CREATED"),
    ]
    for mutate in cases:
        expect_fail(decision, evidence_rows, mutate)

    print(
        "k2-qimen-p2-ontology-decision: PASS "
        f"negative_cases={len(cases)} correction=EXPLICIT_0021_STRUCTURE_RECOVERED "
        "route=SHARED_SUPERSET_REPRESENTATION_V02 atomic_layers=5 derived_composite=格局 "
        "workplace_total_order=NOT_SOURCE_ESTABLISHED production_representation=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
