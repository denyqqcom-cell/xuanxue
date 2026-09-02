#!/usr/bin/env python3
import json
from pathlib import Path

AUDIT = Path("knowledge/K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V01.json")
EXPECTED_SHARED_ROLES = {"asker", "organization", "superior", "peer", "subordinate"}
EXPECTED_CURRENT_LAYERS = ["奇仪", "八门", "八神", "九星"]
EXPECTED_WORKPLACE_FACTORS = ["天时", "地利", "人和", "神助", "格局"]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    require(AUDIT.exists(), "missing production-domain source-parity audit artifact")
    data = json.loads(AUDIT.read_text(encoding="utf-8"))

    require(data.get("audit_id") == "K2-QIMEN-P2-DOMAIN-SOURCE-PARITY-V01", "audit id drift")
    require(data.get("plan_id") == "K2PV-QRM-002", "plan id drift")
    require(data.get("hypothesis_id") == "QRM-H1", "hypothesis id drift")
    require(data.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "candidate domain drift")
    require(data.get("research_scope") == "LOW_RISK_OBSERVATIONAL_ONLY_NO_EMPLOYMENT_DECISION_ADVICE", "research scope guard missing")

    sources = data.get("source_inputs", [])
    require(sources == ["QM-SRC-0003", "QM-SRC-0021"], "source input set/order drift")

    role = data.get("role_parity", {})
    require(role.get("status") == "PASS_SHARED_ROLE_INTERSECTION", "role parity must pass only on shared source intersection")
    rows = role.get("shared_roles", [])
    require({row.get("role_id") for row in rows} == EXPECTED_SHARED_ROLES, "shared role intersection drift")
    for row in rows:
        refs = row.get("source_refs", {})
        require(set(refs) == {"QM-SRC-0003", "QM-SRC-0021"}, f"role {row.get('role_id')} must bind both sources")
        require(all(isinstance(v, list) and v for v in refs.values()), f"role {row.get('role_id')} source refs missing")

    layer = data.get("layer_parity", {})
    require(layer.get("status") == "BLOCKED_SOURCE_ONTOLOGY_MISMATCH", "layer parity blocker must remain explicit")
    require(layer.get("p2_current_shared_layer_vocabulary") == EXPECTED_CURRENT_LAYERS, "current P2 layer vocabulary drift")
    require(layer.get("qm_src_0003_fixed_priority") == EXPECTED_CURRENT_LAYERS, "QM-SRC-0003 fixed priority drift")
    require(layer.get("qm_src_0021_workplace_factor_ontology") == EXPECTED_WORKPLACE_FACTORS, "QM-SRC-0021 workplace factor ontology drift")
    require(layer.get("exact_crosswalk_preregistered") is False, "unreviewed factor-to-layer crosswalk detected")
    require(layer.get("silent_crosswalk_forbidden") is True, "silent source-ontology crosswalk must be forbidden")
    require(layer.get("source_faithful_topology_layer_priority_available") is False, "unsupported topology priority must not be synthesized")

    decision = data.get("production_decision", {})
    require(decision.get("domain_source_parity_ready") is False, "domain/source parity must remain blocked")
    require(decision.get("production_representation_materialization_allowed") is False, "production representation must remain blocked")
    require(decision.get("production_complexity_profile_materialization_allowed") is False, "production complexity profile must remain blocked")
    require(decision.get("production_abstention_profile_materialization_allowed") is False, "production abstention profile must remain blocked")
    require(decision.get("statistical_preregistration_allowed") is False, "statistical preregistration must remain blocked")

    require(data.get("outcome_data_used") is False, "outcome data use detected")
    require(data.get("batch") == "NONE", "batch must remain NONE")
    require(data.get("freeze") == "NONE", "freeze must remain NONE")
    require(data.get("outcome") == "NONE", "outcome must remain NONE")
    require(data.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(data.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")

    print(
        "k2-qimen-p2-domain-source-parity: PASS "
        "role_parity=PASS layer_parity=BLOCKED_SOURCE_ONTOLOGY_MISMATCH "
        "production_representation=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
