#!/usr/bin/env python3
import copy
import hashlib
import json

from k2_qimen_p2_abstain_denominator_scorer import ScoringError, validate_profile as validate_abstention_profile
from k2_qimen_p2_budget_enforcer import BudgetError, freeze_budget, validate_contract as validate_budget_contract
from k2_qimen_p2_materialize_representation_v02 import (
    ValidationError as RepresentationError,
    materialize_representation_v02,
)

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
ROLE_IDS = ("asker", "organization", "superior", "peer", "subordinate")
ATOMIC_LAYERS = ("奇仪", "八门", "八神", "九星", "九宫")
DERIVED_COMPOSITES = ("格局",)
ELIGIBLE_TOPOLOGIES = (
    "JOB_SEARCH",
    "PROMOTION",
    "TRANSFER_OR_ROLE_CHANGE",
    "ORGANIZATIONAL_RELATIONSHIP",
)
P2_A_RANKED = ("奇仪", "八门", "八神", "九星")
P2_B_PRIMARY = ("奇仪", "八门")
P2_B_SUPPORTING = ("八神", "九星", "九宫")
EXPECTED_ROLE_BINDINGS = {
    "asker": ["日干"],
    "organization": ["开门"],
    "superior": ["年干", "值符"],
    "peer": ["月干"],
    "subordinate": ["时干"],
}
EXPECTED_COMPLEXITY = {
    "profile_id": "P2-WORKPLACE-COMPLEXITY-PROFILE-V01",
    "fixture_synthetic_limits": False,
    "research_design_choice": True,
    "max_roles_per_question": 5,
    "max_layers_per_question": 5,
    "max_symbol_instances_per_question": 5,
    "max_total_units_per_lane": 15,
    "max_role_bindings_per_symbol_instance": 1,
}
EXPECTED_ABSTENTION = {
    "profile_id": "P2-WORKPLACE-ABSTENTION-SCORING-PROFILE-V01",
    "fixture_synthetic_values": False,
    "frozen_before_outcome_scoring": True,
    "same_for_all_blind_outputs": True,
    "abstain_metric_value": 0.0,
    "technical_unevaluable_metric_value": 0.0,
    "coverage_penalty_mode": "COUNT_IN_PRIMARY_DENOMINATOR_WITH_FROZEN_METRIC_VALUE",
}


class ProductionProfileError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise ProductionProfileError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _wrap_external(fn, *args):
    try:
        return fn(*args)
    except (BudgetError, ScoringError, RepresentationError) as exc:
        raise ProductionProfileError(str(exc)) from exc


def validate_contract_bundle(contract, representation_v02_contract, parity_v02, complexity_contract, abstention_contract):
    _require(contract.get("contract_id") == "K2-QIMEN-P2-PRODUCTION-PROFILE-CONTRACT-V01", "production profile contract id drift")
    _require(contract.get("capability") == "P2-PREBATCH-PROFILE-003", "production profile capability drift")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    _require(contract.get("representation_v02_contract_ref") == "knowledge/K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json", "Representation V02 ref drift")
    _require(contract.get("domain_source_parity_v02_ref") == "knowledge/K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V02.json", "parity V02 ref drift")
    _require(contract.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V14.json", "prior implementation drift")

    _require(representation_v02_contract.get("contract_id") == "K2-QIMEN-P2-REPRESENTATION-CONTRACT-V02", "Representation V02 contract drift")
    _require(parity_v02.get("audit_id") == "K2-QIMEN-P2-DOMAIN-SOURCE-PARITY-V02", "parity V02 audit drift")
    _require(parity_v02.get("role_parity", {}).get("status") == "PASS_SHARED_ROLE_INTERSECTION", "role parity not closed")
    _require(parity_v02.get("atomic_context_parity", {}).get("status") == "PASS_SHARED_SUPERSET_SOURCE_COVERAGE", "atomic context parity not closed")
    _require(parity_v02.get("priority_policy_parity", {}).get("status") == "PASS_SOURCE_FAITHFUL_PARTIAL_POLICY_FOR_RESTRICTED_SCOPE", "priority parity not closed")
    _require(parity_v02.get("production_decision", {}).get("production_representation_materialization_allowed") is True, "production representation not authorized")
    _require(parity_v02.get("outcome_data_used") is False, "parity audit used outcome data")

    scope = contract.get("restricted_scope", {})
    _require(scope.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "candidate domain drift")
    _require(scope.get("research_scope") == "LOW_RISK_OBSERVATIONAL_ONLY_NO_EMPLOYMENT_DECISION_ADVICE", "research scope drift")
    _require(scope.get("eligible_question_topologies") == list(ELIGIBLE_TOPOLOGIES), "eligible topology set drift")
    _require(scope.get("requires_explicit_asker_and_work_object") is True, "explicit asker/work object guard missing")
    _require(scope.get("unsupported_topology_action") == "ABSTAIN_OR_OUT_OF_SCOPE_FAIL_CLOSED", "unsupported topology must fail closed")
    _require(scope.get("high_impact_employment_decision_use_forbidden") is True, "high-impact employment use must be forbidden")
    _require(scope.get("scope_may_not_expand_after_outcome") is True, "post-outcome scope expansion guard missing")

    req = contract.get("production_representation_requirements", {})
    _require(req.get("representation_id") == "QRM-P2-WORKPLACE-RESTRICTED-PRODUCTION-REPRESENTATION-V01", "production representation id drift")
    _require(req.get("shared_role_ids") == list(ROLE_IDS), "shared role universe drift")
    _require(req.get("shared_atomic_context_universe") == list(ATOMIC_LAYERS), "shared atomic universe drift")
    _require(req.get("derived_composites") == list(DERIVED_COMPOSITES), "derived composite drift")
    _require(req.get("same_feature_universe_all_lanes") is True, "feature parity missing")
    _require(req.get("lane_specific_feature_or_rule_addition_forbidden") is True, "lane feature/rule additions must be forbidden")
    _require(req.get("P2_A_ranked_subset") == list(P2_A_RANKED), "P2-A ranked subset drift")
    _require(req.get("P2_A_visible_unranked_context") == ["九宫"], "P2-A 九宫 visibility drift")
    _require(req.get("P2_A_PRIME_ranked_subset") == list(P2_A_RANKED), "P2-A_PRIME ranked subset drift")
    _require(req.get("P2_A_PRIME_visible_unranked_context") == ["九宫"], "P2-A_PRIME 九宫 visibility drift")
    _require(req.get("P2_B_primary_atomic_context_set") == list(P2_B_PRIMARY), "P2-B primary set drift")
    _require(req.get("P2_B_primary_set_internal_order") == "UNORDERED", "P2-B primary pair cannot gain invented order")
    _require(req.get("P2_B_supporting_visible_context") == list(P2_B_SUPPORTING), "P2-B supporting context drift")
    _require(req.get("workplace_total_order_status") == "NOT_SOURCE_ESTABLISHED", "workplace total order must remain unestablished")

    c = contract.get("shared_complexity_profile", {})
    _require(c.get("profile_id") == EXPECTED_COMPLEXITY["profile_id"], "complexity profile id drift")
    for key in ("max_roles_per_question", "max_layers_per_question", "max_symbol_instances_per_question", "max_total_units_per_lane", "max_role_bindings_per_symbol_instance"):
        _require(c.get(key) == EXPECTED_COMPLEXITY[key], f"{key} production envelope drift")
    _require(c.get("lane_overrides_forbidden") is True, "complexity lane override guard missing")
    _require(c.get("derivation") == "STRUCTURAL_ENVELOPE_FROM_SHARED_ROLE_CARDINALITY_AND_ATOMIC_CONTEXT_UNIVERSE", "complexity derivation drift")
    _require(c.get("universal_qimen_limit_claimed") is False, "complexity envelope cannot become Qimen doctrine")

    a = contract.get("shared_abstention_profile", {})
    _require(a.get("profile_id") == EXPECTED_ABSTENTION["profile_id"], "abstention profile id drift")
    for key, expected in EXPECTED_ABSTENTION.items():
        _require(a.get(key) == expected, f"abstention profile contract drift: {key}")
    _require(a.get("universal_abstain_penalty_claimed") is False, "abstention penalty cannot become universal doctrine")
    _require("compatible scale" in a.get("metric_binding_note", ""), "future metric-scale binding guard missing")

    boundary = contract.get("freeze_boundary", {})
    for key in (
        "production_representation_and_profiles_before_plate_values",
        "production_representation_and_profiles_before_outcome",
        "post_outcome_edit_forbidden",
        "lane_specific_profile_override_forbidden",
        "profile_change_requires_new_version_before_future_batch",
    ):
        _require(boundary.get(key) is True, f"freeze boundary missing: {key}")

    _wrap_external(validate_budget_contract, complexity_contract)
    _require(abstention_contract.get("contract_id") == "K2-QIMEN-P2-ABSTAIN-DENOMINATOR-CONTRACT-V01", "abstention denominator contract drift")
    _require(abstention_contract.get("capability") == "P2-EXEC-007", "abstention denominator capability drift")
    _require(abstention_contract.get("denominator_policy", {}).get("abstain_counts_in_primary_denominator") is True, "ABSTAIN denominator guard drift")
    _require(abstention_contract.get("denominator_policy", {}).get("technical_unevaluable_counts_in_primary_denominator") is True, "technical UNEVALUABLE denominator guard drift")

    _require(contract.get("research_only") is True, "production profile remains research-only")
    _require(contract.get("outcome_data_used") is False, "production profile cannot use outcome data")
    _require(contract.get("statistical_preregistration_ready") is False, "profile materialization cannot claim statistical preregistration")
    _require(contract.get("batch_creation_allowed") is False, "profile materialization cannot create Batch")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state drift")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def _validate_production_source(source, contract, parity_v02):
    req = contract["production_representation_requirements"]
    _require(source.get("representation_id") == req["representation_id"], "production representation source id drift")
    world = source.get("world_variable_manifest", {})
    scope = contract["restricted_scope"]
    for key in (
        "candidate_domain",
        "research_scope",
        "eligible_question_topologies",
        "requires_explicit_asker_and_work_object",
        "unsupported_topology_action",
        "high_impact_employment_decision_use_forbidden",
        "scope_may_not_expand_after_outcome",
    ):
        _require(world.get(key) == scope.get(key), f"production world-variable scope drift: {key}")

    features = source.get("feature_extraction_manifest", {})
    _require(features.get("shared_role_ids") == list(ROLE_IDS), "production feature role universe drift")
    _require(features.get("shared_role_binding_candidates") == EXPECTED_ROLE_BINDINGS, "production role binding candidate drift")
    _require(features.get("pre_plate_disambiguation_required_for") == ["superior"], "superior pre-plate disambiguation guard drift")
    _require(features.get("feedback_dependent_role_switch_forbidden") is True, "post-feedback role switching must remain forbidden")
    parity_refs = set(parity_v02.get("source_evidence_refs", []))
    _require(set(features.get("source_refs", [])).issubset(parity_refs), "production feature source refs escape reviewed parity evidence")

    rule_pool = source.get("eligible_rule_pool", {})
    _require(rule_pool.get("rule_scope") == "RESTRICTED_SOURCE_REVIEWED_WORKPLACE_ONLY", "production rule scope drift")
    _require(rule_pool.get("lane_specific_additions") is False, "lane-specific production rule additions forbidden")
    _require(rule_pool.get("source_local_scope_preserved") is True, "source-local rule scope must be preserved")
    _require(rule_pool.get("outcome_or_feedback_selected_rule_forbidden") is True, "outcome-selected rule forbidden")
    _require(set(rule_pool.get("source_refs", [])) == parity_refs, "production eligible rule pool must bind exact reviewed parity evidence set")

    schema = source.get("prediction_schema", {})
    _require(schema.get("type") == "object", "production prediction schema type drift")
    _require(schema.get("required") == ["prediction", "confidence", "abstain"], "production prediction schema required fields drift")
    _require(schema.get("outcome_scoring_definition") == "PENDING_STATISTICAL_PREREGISTRATION", "statistical scoring must remain pending")
    _require(schema.get("confidence", {}).get("minimum") == 0.0 and schema.get("confidence", {}).get("maximum") == 1.0, "confidence scale drift")

    return _wrap_external(materialize_representation_v02, source)


def _budget_envelope_source():
    instances = [
        {
            "symbol_type": "pre_plate_role_binding",
            "plate_layer": "PRE_PLATE_SELECTOR",
            "instance_role": role_id,
            "relation_direction": "ROLE_TO_ASKED_OBJECT",
        }
        for role_id in ROLE_IDS
    ]
    return {
        "question_id": "PRODUCTION_PROFILE_ENVELOPE_VALIDATION",
        "question_domain": "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE",
        "asked_object": "RESTRICTED_WORKPLACE_OBJECT",
        "method_layer": "PREDICTIVE_INTERPRETATION",
        "role_candidates": [
            {"role_id": role_id, "symbol_instance_selector": copy.deepcopy(instances[index])}
            for index, role_id in enumerate(ROLE_IDS)
        ],
        "layer_ids": list(ATOMIC_LAYERS),
        "symbol_instances": instances,
    }


def _validate_shared_profiles(profiles, contract, complexity_contract, abstention_contract):
    expected_fields = {
        "artifact_id",
        "capability",
        "plan_id",
        "hypothesis_id",
        "complexity_profile",
        "abstention_profile",
        "profile_parity",
        "statistical_metric_binding",
        "outcome_data_used",
        "batch",
        "freeze",
        "outcome",
        "empirical_credit",
    }
    _require(set(profiles) == expected_fields, "shared profile artifact fields drift")
    _require(profiles.get("artifact_id") == "K2-QIMEN-P2-SHARED-PROFILES-V01", "shared profile artifact id drift")
    _require(profiles.get("capability") == "P2-PREBATCH-PROFILE-003", "shared profile capability drift")
    _require(profiles.get("plan_id") == "K2PV-QRM-002", "shared profile plan drift")
    _require(profiles.get("hypothesis_id") == "QRM-H1", "shared profile hypothesis drift")

    complexity_profile = profiles.get("complexity_profile", {})
    _require(complexity_profile == EXPECTED_COMPLEXITY, "production complexity profile drift from frozen restricted envelope")
    frozen = _wrap_external(freeze_budget, _budget_envelope_source(), complexity_profile, complexity_contract)
    _require(frozen.get("counts", {}).get("per_question", {}).get("role_count") == 5, "production role envelope count drift")
    _require(frozen.get("counts", {}).get("per_question", {}).get("layer_count") == 5, "production layer envelope count drift")
    _require(frozen.get("counts", {}).get("per_question", {}).get("symbol_instance_count") == 5, "production symbol-instance envelope count drift")
    _require({row.get("total_units") for row in frozen.get("counts", {}).get("per_lane", [])} == {15}, "production total complexity envelope drift")

    abstention_profile = profiles.get("abstention_profile", {})
    _require(abstention_profile == EXPECTED_ABSTENTION, "production abstention profile drift")
    _wrap_external(validate_abstention_profile, abstention_profile, abstention_contract)

    parity = profiles.get("profile_parity", {})
    _require(parity.get("same_complexity_profile_all_lanes") is True, "complexity profile must be shared")
    _require(parity.get("same_abstention_profile_all_blind_outputs") is True, "abstention profile must be shared")
    _require(parity.get("lane_or_blind_override_forbidden") is True, "profile overrides must be forbidden")
    _require(parity.get("frozen_before_plate_values") is True, "profiles must freeze before plate values")
    _require(parity.get("frozen_before_outcome") is True, "profiles must freeze before outcome")

    metric = profiles.get("statistical_metric_binding", {})
    _require(metric.get("status") == "PENDING_STATISTICAL_PREREGISTRATION", "statistical metric binding cannot be pre-claimed")
    _require(metric.get("require_metric_scale_compatible_with_abstain_value") is True, "metric scale compatibility guard missing")
    _require(metric.get("profile_change_requires_new_version_before_batch") is True, "profile version guard missing")

    _require(profiles.get("outcome_data_used") is False, "shared profiles cannot use outcome data")
    _require(profiles.get("batch") == profiles.get("freeze") == profiles.get("outcome") == "NONE", "shared profiles cannot create research state")
    _require(profiles.get("empirical_credit") == "NONE", "shared profiles cannot gain empirical credit")


def materialize_production_bundle(contract, representation_source, shared_profiles, representation_v02_contract, parity_v02, complexity_contract, abstention_contract):
    validate_contract_bundle(
        contract,
        representation_v02_contract,
        parity_v02,
        complexity_contract,
        abstention_contract,
    )
    representation = _validate_production_source(representation_source, contract, parity_v02)
    _validate_shared_profiles(shared_profiles, contract, complexity_contract, abstention_contract)

    profile_hashes = {
        "complexity_profile_sha256": canonical_sha256(shared_profiles["complexity_profile"]),
        "abstention_profile_sha256": canonical_sha256(shared_profiles["abstention_profile"]),
        "shared_profiles_sha256": canonical_sha256(shared_profiles),
    }
    bundle_identity = {
        "representation_sha256": representation["shared_representation_sha256"],
        **profile_hashes,
        "contract_sha256": canonical_sha256(contract),
        "domain_source_parity_v02_sha256": canonical_sha256(parity_v02),
    }
    return {
        "artifact_kind": "P2_RESTRICTED_PRODUCTION_PROFILE_BUNDLE_V01",
        "representation": representation,
        "shared_profiles": copy.deepcopy(shared_profiles),
        "profile_hashes": profile_hashes,
        "production_bundle_sha256": canonical_sha256(bundle_identity),
        "production_representation_materialized": True,
        "production_complexity_profile_materialized": True,
        "production_abstention_profile_materialized": True,
        "statistical_preregistration_ready": False,
        "batch_creation_allowed": False,
        "outcome_data_used": False,
        "batch": "NONE",
        "freeze": "NONE",
        "outcome": "NONE",
        "empirical_credit": "NONE",
        "claim_extraction": "BLOCKED",
    }
