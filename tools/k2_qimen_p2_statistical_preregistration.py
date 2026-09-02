#!/usr/bin/env python3
import copy
import json
import math

PRIMARY_TOPOLOGIES = ("JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE")
EXCLUDED_PRIMARY_TOPOLOGIES = ("ORGANIZATIONAL_RELATIONSHIP",)
LABELS = ("EVENT_OCCURS", "EVENT_DOES_NOT_OCCUR")
CONTRASTS = ("P2-C1", "P2-C2", "P2-C3")
EXPECTED_TOPOLOGY_EVENTS = {
    "JOB_SEARCH": "FORMAL_OFFER_RECEIVED_FOR_EXACT_PRE_FROZEN_TARGET_POSITION_OR_APPLICATION_WITHIN_HORIZON",
    "PROMOTION": "FORMAL_DOCUMENTED_PROMOTION_OR_LEVEL_INCREASE_EFFECTIVE_WITHIN_HORIZON",
    "TRANSFER_OR_ROLE_CHANGE": "FORMAL_DOCUMENTED_TEAM_ROLE_OR_REPORTING_LINE_CHANGE_EFFECTIVE_WITHIN_HORIZON",
}


class StatisticalPreregistrationError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise StatisticalPreregistrationError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def exact_binomial_upper_tail(discordant_pairs, candidate_wins):
    _require(isinstance(discordant_pairs, int) and not isinstance(discordant_pairs, bool) and discordant_pairs >= 0, "discordant_pairs must be a non-negative integer")
    _require(isinstance(candidate_wins, int) and not isinstance(candidate_wins, bool) and 0 <= candidate_wins <= discordant_pairs, "candidate_wins outside discordant range")
    if discordant_pairs == 0:
        return 1.0
    numerator = sum(math.comb(discordant_pairs, i) for i in range(candidate_wins, discordant_pairs + 1))
    return numerator / (2 ** discordant_pairs)


def validate_statistical_contract(contract, production_profile_contract, production_representation, shared_profiles):
    _require(isinstance(contract, dict), "statistical contract must be an object")
    _require(contract.get("contract_id") == "K2-QIMEN-P2-STATISTICAL-PREREGISTRATION-CONTRACT-V01", "statistical contract id drift")
    _require(contract.get("capability") == "P2-PREBATCH-STAT-004", "statistical capability drift")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")
    _require(contract.get("prior_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V19.json", "prior protocol drift")
    _require(contract.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V15.json", "prior implementation drift")

    scope = contract.get("primary_scope", {})
    _require(scope.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "primary domain drift")
    _require(scope.get("research_only") is True, "primary scope must remain research-only")
    _require(scope.get("no_employment_decision_advice") is True, "employment decision advice must be forbidden")
    _require(scope.get("primary_batch_topologies") == list(PRIMARY_TOPOLOGIES), "primary topology set drift")
    _require(scope.get("representation_supported_but_primary_batch_excluded") == list(EXCLUDED_PRIMARY_TOPOLOGIES), "primary excluded topology set drift")
    _require(scope.get("scope_expansion_after_batch_start_forbidden") is True, "post-start scope expansion guard missing")

    outcome = contract.get("outcome_contract", {})
    _require(outcome.get("event_horizon_days") == 90, "event horizon drift")
    _require(outcome.get("clock") == "CALENDAR_DAYS_FROM_CASE_FREEZE_TIMESTAMP", "outcome clock drift")
    _require(outcome.get("labels") == list(LABELS), "outcome label drift")
    _require(outcome.get("topology_events") == EXPECTED_TOPOLOGY_EVENTS, "topology outcome event drift")
    _require(outcome.get("target_object_must_be_unique_before_lane_execution") is True, "unique target object guard missing")
    _require(outcome.get("outcome_definition_must_be_frozen_before_lane_execution") is True, "outcome definition freeze guard missing")
    _require(outcome.get("outcome_value_must_be_unknown_at_prediction_freeze") is True, "unknown outcome-at-freeze guard missing")
    _require(outcome.get("outcome_missing_after_horizon") == "OUTCOME_UNEVALUABLE_RETAIN_IN_PRIMARY_DENOMINATOR_WITH_SYMMETRIC_ZERO_SCORE", "missing-outcome denominator policy drift")
    _require(outcome.get("raw_sensitive_document_storage_required") is False, "raw sensitive document storage cannot be required")
    _require(outcome.get("deidentified_outcome_record_required") is True, "deidentified outcome record guard missing")

    prediction = contract.get("prediction_contract", {})
    _require(prediction.get("labels") == list(LABELS), "prediction labels drift")
    _require(prediction.get("confidence_semantics") == "PROBABILITY_ASSIGNED_TO_PREDICTED_LABEL", "confidence semantics drift")
    _require(prediction.get("confidence_min") == 0.5 and prediction.get("confidence_max") == 1.0, "confidence range drift")
    _require(prediction.get("same_prediction_schema_all_lanes") is True, "prediction schema parity missing")
    _require(prediction.get("abstain_is_legal_output") is True, "ABSTAIN must remain legal")
    _require(prediction.get("technical_unevaluable_is_legal_output") is True, "technical UNEVALUABLE must remain legal")

    metric = contract.get("primary_metric", {})
    _require(metric.get("metric_id") == "COVERAGE_PENALIZED_BINARY_ACCURACY_V01", "primary metric drift")
    _require(metric.get("direction") == "HIGHER_IS_BETTER", "metric direction drift")
    for key, expected in (
        ("predicted_correct_score", 1.0),
        ("predicted_incorrect_score", 0.0),
        ("abstain_score", 0.0),
        ("technical_unevaluable_score", 0.0),
        ("outcome_unevaluable_score", 0.0),
    ):
        _require(metric.get(key) == expected, f"primary metric score drift: {key}")
    _require(metric.get("denominator") == "ALL_FROZEN_INCLUDED_CASES_PER_CONTRAST", "primary denominator drift")
    _require(metric.get("paired_delta") == "MEAN(CANDIDATE_CASE_SCORE - COMPARATOR_CASE_SCORE)", "paired delta definition drift")
    _require(metric.get("compatible_with_frozen_abstention_profile") is True, "frozen abstention compatibility guard missing")
    _require(metric.get("secondary_metrics_cannot_rescue_failed_primary") is True, "secondary rescue guard missing")

    confirm = contract.get("confirmatory_test", {})
    _require(confirm.get("test_id") == "EXACT_ONE_SIDED_MCNEMAR_BINOMIAL_V01", "confirmatory test drift")
    _require(confirm.get("discordant_definition") == "CASES_WHERE_CANDIDATE_AND_COMPARATOR_BINARY_CORRECTNESS_SCORES_DIFFER", "discordant definition drift")
    _require(confirm.get("null_conditional_candidate_win_probability") == 0.5, "null probability drift")
    _require(confirm.get("alternative") == "CANDIDATE_GREATER_THAN_COMPARATOR", "alternative drift")
    _require(confirm.get("family") == list(CONTRASTS), "contrast family drift")
    _require(confirm.get("familywise_alpha") == 0.05, "familywise alpha drift")
    _require(confirm.get("multiplicity_correction") == "BONFERRONI_THREE_ONE_SIDED_CONTRASTS", "multiplicity correction drift")
    _require(abs(confirm.get("per_contrast_alpha", -1.0) - (1.0 / 60.0)) < 1e-15, "per-contrast alpha drift")
    _require(confirm.get("p_value_rule") == "EXACT_BINOMIAL_UPPER_TAIL_ON_CANDIDATE_WINS_GIVEN_DISCORDANT_PAIRS", "p-value rule drift")
    _require(confirm.get("practical_effect_floor_paired_accuracy_delta") == 0.05, "practical effect floor drift")

    sampling = contract.get("sampling_rule", {})
    _require(sampling.get("rule_id") == "STRATIFIED_FIRST_ELIGIBLE_FIXED_QUOTA_V01", "sampling rule id drift")
    _require(sampling.get("target_cases_per_topology") == 80, "per-topology target drift")
    _require(sampling.get("target_total_cases") == 240, "total target drift")
    _require(sampling.get("within_topology_selection") == "FIRST_ELIGIBLE_CASES_BY_CASE_FREEZE_TIMESTAMP", "within-topology selection drift")
    _require(sampling.get("same_case_set_all_lanes") is True, "lane case-set parity missing")
    _require(sampling.get("case_inclusion_before_lane_execution") is True, "case inclusion freeze guard missing")
    _require(sampling.get("duplicate_case_id_forbidden") is True, "duplicate case guard missing")
    _require(sampling.get("same_asker_same_target_object_duplicate_forbidden") is True, "duplicate asker-target guard missing")
    _require(sampling.get("outcome_dependent_case_selection_forbidden") is True, "outcome-dependent selection must be forbidden")
    _require(sampling.get("post_prediction_case_replacement_forbidden") is True, "post-prediction replacement must be forbidden")

    stopping = contract.get("stopping_rule", {})
    _require(stopping.get("rule_id") == "NON_OUTCOME_DRIVEN_QUOTA_OR_TIME_CAP_V01", "stopping rule id drift")
    _require(stopping.get("maximum_acquisition_window_days") == 365, "acquisition window drift")
    _require(stopping.get("window_anchor") == "FUTURE_BATCH_START_TIMESTAMP", "acquisition window anchor drift")
    _require(stopping.get("outcome_values_may_not_change_acquisition") is True, "outcome-driven stopping must be forbidden")
    _require(stopping.get("closed_acquisition_may_not_reopen") is True, "closed acquisition reopen must be forbidden")
    _require(stopping.get("final_outcome_qc_wait_days_after_last_included_case") == 90, "final follow-up wait drift")
    _require(stopping.get("insufficient_information_may_not_trigger_same_batch_extension") is True, "same-Batch information extension must be forbidden")

    floor = contract.get("minimum_information_floor", {})
    _require(floor.get("resolved_outcome_cases_per_topology") == 60, "per-topology outcome floor drift")
    _require(floor.get("resolved_outcome_cases_total") == 180, "total outcome floor drift")
    _require(floor.get("discordant_pairs_per_contrast") == 80, "discordant-pair floor drift")
    _require(floor.get("all_floors_required") is True, "all information floors must be required")
    _require(floor.get("if_any_floor_fails") == "INSUFFICIENT_INFORMATION_NO_EMPIRICAL_CREDIT_NO_REOPEN", "insufficient information action drift")
    _require(floor.get("floor_values_are_project_research_design_choices_not_qimen_source_claims") is True, "information floor provenance guard missing")

    attribution = contract.get("contrast_attribution", {})
    _require(attribution.get("P2-C1", {}).get("candidate") == "P2-A_PRIME" and attribution.get("P2-C1", {}).get("comparator") == "P2-A", "C1 lane identity drift")
    _require(attribution.get("P2-C2", {}).get("candidate") == "P2-B" and attribution.get("P2-C2", {}).get("comparator") == "P2-A_PRIME", "C2 lane identity drift")
    _require(attribution.get("P2-C3", {}).get("candidate") == "P2-B" and attribution.get("P2-C3", {}).get("comparator") == "P2-A", "C3 lane identity drift")
    _require(attribution.get("P2-C3", {}).get("component_credit_forbidden") is True, "C3 component credit must be forbidden")
    _require(attribution.get("QRM_H1_bundle_support_requires") == "P2-C3_PASS", "QRM-H1 bundle decision rule drift")
    _require(attribution.get("component_credit_requires_own_contrast_pass") is True, "component credit own-contrast guard missing")
    _require(attribution.get("failed_component_contrast_cannot_be_rescued_by_C3") is True, "C3 component rescue must be forbidden")

    contamination = contract.get("contamination_gate", {})
    for key in (
        "post_feedback_role_switch",
        "post_feedback_priority_edit",
        "post_feedback_rule_edit",
        "lane_specific_case_exclusion",
        "cross_lane_intermediate_output",
        "outcome_selected_mapping",
        "outcome_selected_stopping_or_sample_extension",
    ):
        _require(contamination.get(key) == "FAIL", f"contamination gate drift: {key}")
    _require(contamination.get("profile_or_metric_change_after_batch_start") == "FAIL_AND_REQUIRE_FUTURE_VERSION", "post-start metric/profile mutation guard drift")

    provenance = contract.get("design_provenance", {})
    _require(provenance.get("statistical_choices_origin") == "PROJECT_GENERATED_METHODOLOGICAL_PREREGISTRATION", "statistical choice provenance drift")
    _require(provenance.get("qimen_source_semantic_credit") == "NONE", "statistical design cannot gain source-semantic credit")
    _require(provenance.get("empirical_credit_before_future_batch") == "NONE", "pre-Batch empirical credit drift")

    _require(production_profile_contract.get("contract_id") == "K2-QIMEN-P2-PRODUCTION-PROFILE-CONTRACT-V01", "production profile contract drift")
    _require(production_profile_contract.get("restricted_scope", {}).get("candidate_domain") == scope.get("candidate_domain"), "production/statistical domain mismatch")
    _require(production_profile_contract.get("restricted_scope", {}).get("eligible_question_topologies") == ["JOB_SEARCH", "PROMOTION", "TRANSFER_OR_ROLE_CHANGE", "ORGANIZATIONAL_RELATIONSHIP"], "production topology universe drift")
    _require(production_representation.get("representation_id") == "QRM-P2-WORKPLACE-RESTRICTED-PRODUCTION-REPRESENTATION-V01", "production representation drift")
    _require(production_representation.get("shared_representation_sha256") == "a440ef84f42b5798ab6bf8b8e5d802b554b2ba05a35810f67eb9f69eebd48fbb", "production representation digest drift")
    _require(shared_profiles.get("abstention_profile", {}).get("abstain_metric_value") == metric.get("abstain_score"), "ABSTAIN metric incompatible with frozen shared profile")
    _require(shared_profiles.get("abstention_profile", {}).get("technical_unevaluable_metric_value") == metric.get("technical_unevaluable_score"), "technical UNEVALUABLE metric incompatible with frozen shared profile")
    _require(shared_profiles.get("statistical_metric_binding", {}).get("status") == "PENDING_STATISTICAL_PREREGISTRATION", "shared profile statistical binding pre-state drift")

    _require(contract.get("outcome_data_used") is False, "statistical contract cannot use outcome data")
    _require(contract.get("statistical_preregistration_ready") is False, "fail-first contract cannot pre-claim readiness")
    _require(contract.get("batch_ready") is False and contract.get("batch_creation_allowed") is False, "fail-first contract cannot open Batch")
    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation detected")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain blocked")


def validate_preregistration(prereg, contract):
    _require(isinstance(prereg, dict), "statistical preregistration must be an object")
    _require(prereg.get("preregistration_id") == "K2-QIMEN-P2-STATISTICAL-PREREGISTRATION-V01", "preregistration id drift")
    _require(prereg.get("version") == "0.1", "preregistration version drift")
    _require(prereg.get("plan_id") == contract.get("plan_id"), "preregistration plan drift")
    _require(prereg.get("hypothesis_id") == contract.get("hypothesis_id"), "preregistration hypothesis drift")
    _require(prereg.get("contract_ref") == "knowledge/K2_QIMEN_P2_STATISTICAL_PREREGISTRATION_CONTRACT_V01.json", "preregistration contract ref drift")
    _require(prereg.get("contract_git_blob") == "212f4955927870c140a91bf6b6763a9c9938ddad", "preregistration contract blob drift")
    for section in (
        "primary_scope",
        "outcome_contract",
        "prediction_contract",
        "primary_metric",
        "confirmatory_test",
        "sampling_rule",
        "stopping_rule",
        "minimum_information_floor",
        "contrast_attribution",
        "contamination_gate",
        "design_provenance",
    ):
        _require(prereg.get(section) == contract.get(section), f"preregistration section drift: {section}")
    _require(prereg.get("locked_before_future_batch") is True, "preregistration lock marker missing")
    _require(prereg.get("outcome_data_used") is False, "preregistration cannot use outcome data")
    _require(prereg.get("statistical_preregistration_ready") is True, "statistical preregistration readiness missing")
    _require(prereg.get("batch_ready") is False and prereg.get("batch_creation_allowed") is False, "preregistration cannot create Batch")
    _require(prereg.get("batch") == prereg.get("freeze") == prereg.get("outcome") == "NONE", "preregistration research state mutation detected")
    _require(prereg.get("empirical_credit") == "NONE", "preregistration cannot gain empirical credit")
    _require(prereg.get("claim_extraction") == "BLOCKED", "preregistration cannot unblock claim extraction")


def evaluate_contrast(*, denominator, candidate_wins, comparator_wins, resolved_outcome_cases_total, resolved_outcome_cases_by_topology, contamination, contract):
    _require(isinstance(denominator, int) and not isinstance(denominator, bool) and denominator > 0, "denominator must be a positive integer")
    for name, value in (("candidate_wins", candidate_wins), ("comparator_wins", comparator_wins), ("resolved_outcome_cases_total", resolved_outcome_cases_total)):
        _require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"{name} must be a non-negative integer")
    _require(candidate_wins + comparator_wins <= denominator, "discordant pairs exceed primary denominator")
    _require(resolved_outcome_cases_total <= denominator, "resolved outcomes exceed primary denominator")
    _require(isinstance(resolved_outcome_cases_by_topology, dict), "resolved topology counts must be an object")
    _require(set(resolved_outcome_cases_by_topology) == set(PRIMARY_TOPOLOGIES), "resolved topology count set drift")
    _require(all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in resolved_outcome_cases_by_topology.values()), "resolved topology counts must be non-negative integers")
    _require(sum(resolved_outcome_cases_by_topology.values()) == resolved_outcome_cases_total, "resolved topology counts do not sum to total")
    _require(isinstance(contamination, bool), "contamination flag must be boolean")

    floor = contract["minimum_information_floor"]
    confirm = contract["confirmatory_test"]
    discordant = candidate_wins + comparator_wins
    delta = (candidate_wins - comparator_wins) / denominator
    p_value = exact_binomial_upper_tail(discordant, candidate_wins)
    outcome_floor_met = (
        resolved_outcome_cases_total >= floor["resolved_outcome_cases_total"]
        and all(resolved_outcome_cases_by_topology[topology] >= floor["resolved_outcome_cases_per_topology"] for topology in PRIMARY_TOPOLOGIES)
    )
    discordant_floor_met = discordant >= floor["discordant_pairs_per_contrast"]
    information_floor_met = outcome_floor_met and discordant_floor_met
    contamination_gate_pass = not contamination
    effect_floor_met = delta >= confirm["practical_effect_floor_paired_accuracy_delta"]
    p_value_pass = p_value <= confirm["per_contrast_alpha"]
    contrast_pass = information_floor_met and contamination_gate_pass and effect_floor_met and p_value_pass
    return {
        "denominator": denominator,
        "candidate_wins": candidate_wins,
        "comparator_wins": comparator_wins,
        "discordant_pairs": discordant,
        "paired_accuracy_delta": delta,
        "exact_one_sided_p_value": p_value,
        "outcome_floor_met": outcome_floor_met,
        "discordant_floor_met": discordant_floor_met,
        "information_floor_met": information_floor_met,
        "contamination_gate_pass": contamination_gate_pass,
        "effect_floor_met": effect_floor_met,
        "p_value_pass": p_value_pass,
        "contrast_pass": contrast_pass,
    }
