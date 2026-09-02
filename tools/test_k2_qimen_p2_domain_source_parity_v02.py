#!/usr/bin/env python3
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V02.json"
CONTRACT = ROOT / "knowledge" / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json"
ONTOLOGY = ROOT / "knowledge" / "K2_QIMEN_P2_ONTOLOGY_DECISION_V01.json"
EVIDENCE = ROOT / "knowledge" / "K2_EVIDENCE_WAVE1.jsonl"

ATOMIC = ["奇仪", "八门", "八神", "九星", "九宫"]
ROLES = ["asker", "organization", "superior", "peer", "subordinate"]
REQUIRED_EVIDENCE = {
    "K2E-W1-QM-0003-0007",
    "K2E-W1-QM-0003-0009",
    "K2E-W1-QM-0003-0010",
    "K2E-W1-QM-0003-0017",
    "K2E-W1-QM-0003-0018",
    "K2E-W1-QM-0003-0019",
    "K2E-W1-QM-0003-0020",
    "K2E-W1-QM-0003-0065",
    "K2E-W1-QM-0021-0007",
    "K2E-W1-QM-0021-0239",
    "K2E-W1-QM-0021-0240",
    "K2E-W1-QM-0021-0242",
    "K2E-W1-QM-0021-0346",
    "K2E-W1-QM-0021-0347",
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
            if row.get("evidence_id"):
                rows[row["evidence_id"]] = row
    return rows


def validate(audit, evidence):
    require(audit.get("audit_id") == "K2-QIMEN-P2-DOMAIN-SOURCE-PARITY-V02", "wrong V02 parity audit id")
    require(audit.get("capability") == "P2-PREBATCH-PARITY-002", "wrong capability")
    require(audit.get("plan_id") == "K2PV-QRM-002", "plan drift")
    require(audit.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    require(audit.get("representation_contract_ref") == "knowledge/K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json", "V02 contract ref drift")
    require(audit.get("historical_v01_audit_ref") == "knowledge/K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V01.json", "historical V01 audit must remain referenced")
    require(audit.get("historical_v01_audit_preserved") is True, "historical V01 audit must be preserved")
    require(set(audit.get("source_evidence_refs", [])) == REQUIRED_EVIDENCE, "source evidence set drift")
    require(REQUIRED_EVIDENCE <= set(evidence), "required source evidence missing")

    role = audit.get("role_parity", {})
    require(role.get("status") == "PASS_SHARED_ROLE_INTERSECTION", "role parity must pass")
    require(role.get("shared_role_ids") == ROLES, "shared role order/set drift")
    require(role.get("same_role_universe_available_all_lanes") is True, "same role universe required")
    require(role.get("feedback_dependent_role_switch_forbidden") is True, "feedback role switch forbidden")

    layer = audit.get("atomic_context_parity", {})
    require(layer.get("status") == "PASS_SHARED_SUPERSET_SOURCE_COVERAGE", "atomic context parity must pass")
    require(layer.get("shared_atomic_context_universe") == ATOMIC, "atomic universe drift")
    for source in ("QM-SRC-0003", "QM-SRC-0021"):
        require(layer.get("source_coverage", {}).get(source) == ATOMIC, f"{source} atomic coverage drift")
    require(layer.get("derived_composites") == ["格局"], "derived composite drift")
    require(layer.get("格局_atomic") is False, "格局 cannot be atomic")
    require(layer.get("九宫_first_class") is True, "九宫 must remain first-class")

    priority = audit.get("priority_policy_parity", {})
    require(priority.get("status") == "PASS_SOURCE_FAITHFUL_PARTIAL_POLICY_FOR_RESTRICTED_SCOPE", "priority policy parity must pass only in restricted scope")
    a = priority.get("P2-A", {})
    require(a.get("source_ref") == "K2E-W1-QM-0003-0065", "P2-A source ref drift")
    require(a.get("ranked_subset") == ["奇仪", "八门", "八神", "九星"], "P2-A ranking drift")
    require(a.get("visible_unranked_context") == ["九宫"], "P2-A 九宫 visibility drift")
    require(a.get("invent_rank_for_九宫_forbidden") is True, "P2-A cannot invent 九宫 rank")
    b = priority.get("P2-B", {})
    require(b.get("primary_relation_source_ref") == "K2E-W1-QM-0021-0240", "P2-B primary relation source drift")
    require(b.get("primary_atomic_context_set") == ["奇仪", "八门"], "P2-B primary context set drift")
    require(b.get("primary_set_internal_order") == "UNORDERED", "P2-B primary set cannot invent internal order")
    require(b.get("supporting_visible_context") == ["八神", "九星", "九宫"], "P2-B supporting context drift")
    require(b.get("workplace_total_order_status") == "NOT_SOURCE_ESTABLISHED", "P2-B total order must remain unestablished")
    require(b.get("unsupported_topology_action") == "ABSTAIN_OR_OUT_OF_SCOPE_FAIL_CLOSED", "unsupported topology must fail closed")
    require(b.get("outcome_or_feedback_selected_priority_forbidden") is True, "outcome-selected priority forbidden")

    scope = audit.get("production_scope", {})
    require(scope.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "candidate domain drift")
    require(scope.get("eligible_question_topologies") == ["JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE", "ORGANIZATIONAL_RELATIONSHIP"], "eligible topology set drift")
    require(scope.get("requires_explicit_asker_and_work_object") is True, "explicit asker/work object required")
    require(scope.get("high_impact_employment_decision_use_forbidden") is True, "employment decision use must be forbidden")
    require(scope.get("unsupported_topology") == "ABSTAIN_OR_OUT_OF_SCOPE", "unsupported topology handling drift")

    estimand = audit.get("estimand_parity", {})
    require(estimand.get("same_representation_digest_required") is True, "same representation digest required")
    require(estimand.get("same_atomic_context_visibility_required") is True, "same context visibility required")
    require(estimand.get("same_complexity_formula_required") is True, "same complexity formula required")
    require(estimand.get("C2_only_priority_policy_may_differ") is True, "C2 estimand drift")
    require(estimand.get("lane_specific_feature_addition_forbidden") is True, "lane-specific feature addition forbidden")

    decision = audit.get("production_decision", {})
    require(decision.get("domain_source_parity_ready") is True, "V02 domain/source parity should be ready")
    require(decision.get("production_representation_materialization_allowed") is True, "production representation materialization should be allowed next")
    require(decision.get("production_complexity_profile_materialization_allowed") is False, "complexity profile must wait for production representation")
    require(decision.get("production_abstention_profile_materialization_allowed") is False, "abstention profile must wait")
    require(decision.get("statistical_preregistration_allowed") is False, "statistical prereg must wait")
    require(decision.get("batch_creation_allowed") is False, "Batch creation must remain forbidden")
    require(decision.get("next_required_work") == "P2-PREBATCH-PROFILE-003_MATERIALIZE_RESTRICTED_PRODUCTION_REPRESENTATION_AND_SHARED_PROFILES_FAIL_FIRST", "next work drift")

    require(audit.get("source_local_overgeneralization_check") == "PASS", "source-local overgeneralization guard must pass")
    require(audit.get("outcome_data_used") is False, "outcome data must not be used")
    require(audit.get("batch") == "NONE", "Batch must remain NONE")
    require(audit.get("freeze") == "NONE", "Freeze must remain NONE")
    require(audit.get("outcome") == "NONE", "Outcome must remain NONE")
    require(audit.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(audit.get("claim_extraction") == "BLOCKED", "Claim Extraction must remain blocked")


def expect_fail(base, evidence, mutate):
    x = copy.deepcopy(base)
    mutate(x)
    try:
        validate(x, evidence)
    except AssertionError:
        return
    raise AssertionError("negative V02 parity case unexpectedly passed")


def main():
    require(CONTRACT.exists(), "missing Representation V02 contract")
    require(ONTOLOGY.exists(), "missing ontology decision")
    require(EVIDENCE.exists(), "missing reviewed evidence ledger")
    require(AUDIT.exists(), "missing Representation V02 domain/source parity audit")
    evidence = load_evidence()
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(audit, evidence)

    cases = [
        lambda x: x["role_parity"].__setitem__("status", "BLOCKED"),
        lambda x: x["role_parity"]["shared_role_ids"].append("invented_role"),
        lambda x: x["atomic_context_parity"]["shared_atomic_context_universe"].remove("九宫"),
        lambda x: x["atomic_context_parity"].__setitem__("格局_atomic", True),
        lambda x: x["atomic_context_parity"]["source_coverage"].__setitem__("QM-SRC-0021", ["八门"]),
        lambda x: x["priority_policy_parity"]["P2-A"]["ranked_subset"].append("九宫"),
        lambda x: x["priority_policy_parity"]["P2-B"]["primary_atomic_context_set"].append("九宫"),
        lambda x: x["priority_policy_parity"]["P2-B"].__setitem__("primary_set_internal_order", "奇仪>八门"),
        lambda x: x["priority_policy_parity"]["P2-B"].__setitem__("workplace_total_order_status", "ESTABLISHED"),
        lambda x: x["priority_policy_parity"]["P2-B"].__setitem__("unsupported_topology_action", "INVENT_ORDER"),
        lambda x: x["production_scope"].__setitem__("unsupported_topology", "FORCE_PREDICTION"),
        lambda x: x["estimand_parity"].__setitem__("same_atomic_context_visibility_required", False),
        lambda x: x["production_decision"].__setitem__("production_complexity_profile_materialization_allowed", True),
        lambda x: x["production_decision"].__setitem__("statistical_preregistration_allowed", True),
        lambda x: x["production_decision"].__setitem__("batch_creation_allowed", True),
        lambda x: x.__setitem__("empirical_credit", "POSITIVE"),
        lambda x: x.__setitem__("batch", "CREATED"),
    ]
    for mutate in cases:
        expect_fail(audit, evidence, mutate)

    print(
        "k2-qimen-p2-domain-source-parity-v02: PASS "
        f"negative_cases={len(cases)} role_parity=PASS atomic_context_parity=PASS "
        "priority_policy_parity=PASS_RESTRICTED_SCOPE total_order=NOT_SOURCE_ESTABLISHED "
        "production_representation_allowed=true production_profiles=false prereg=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
