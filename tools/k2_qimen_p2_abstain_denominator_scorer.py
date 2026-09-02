#!/usr/bin/env python3
import hashlib
import json
import math

CONTRAST_IDS = ("P2-C1", "P2-C2", "P2-C3")
ALLOWED_STATUSES = {"PREDICTED", "ABSTAIN", "TECHNICAL_UNEVALUABLE"}
FORBIDDEN_RUNTIME_KEYS = {
    "lane_id",
    "model_name",
    "candidate_lane",
    "comparator_lane",
    "winner_lane",
    "control_lane",
    "baseline_lane",
    "treatment_lane",
    "hypothesis_label",
    "semantic_arm_label",
    "outcome_selected_lane",
}
SEMANTIC_ARM_TOKENS = ("baseline", "control", "treatment", "winner", "better_lane")


class ScoringError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise ScoringError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _walk_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


def _reject_runtime_identity(value, label):
    keys = {key.lower() for key in _walk_keys(value)}
    bad = sorted(keys & FORBIDDEN_RUNTIME_KEYS)
    _require(not bad, f"{label} leaks semantic lane identity: {bad}")
    text = canonical_json(value).lower()
    for token in SEMANTIC_ARM_TOKENS:
        _require(f'"{token}"' not in text, f"{label} leaks semantic arm token: {token}")


def validate_scorer_contract(contract, execution_contract):
    _require(contract.get("capability") == "P2-EXEC-007", "capability drift")
    _require(contract.get("failure_policy") == "FAIL_CLOSED", "scorer must fail closed")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis drift")

    estimands = contract.get("estimand_alignment", {})
    source_estimands = execution_contract.get("estimand_lock", {})
    _require(set(source_estimands) == set(CONTRAST_IDS), "execution estimand set drift")
    for contrast_id in CONTRAST_IDS:
        expected = source_estimands[contrast_id]
        actual = estimands.get(contrast_id, {})
        _require(actual.get("candidate") == expected.get("candidate"), f"{contrast_id} candidate drift")
        _require(actual.get("comparator") == expected.get("comparator"), f"{contrast_id} comparator drift")
        if contrast_id == "P2-C3":
            _require(actual.get("component_credit_forbidden") is True, "P2-C3 component credit must be forbidden")
            _require(expected.get("component_credit_forbidden") is True, "execution contract C3 component guard drift")

    blind = contract.get("scorer_blinding_boundary", {})
    _require(blind.get("runtime_receives_blind_ids_only") is True, "scorer must receive blind ids only")
    _require(blind.get("runtime_must_not_receive_lane_id") is True, "lane id visibility forbidden")
    _require(blind.get("runtime_must_not_receive_model_name") is True, "model name visibility forbidden")
    _require(blind.get("runtime_must_not_receive_semantic_arm_labels") is True, "semantic arm labels forbidden")
    _require(blind.get("contrast_binding_must_be_frozen_before_outcome_scoring") is True, "contrast binding must freeze before scoring")

    denom = contract.get("denominator_policy", {})
    _require(denom.get("case_inclusion_source") == "PRE_LANE_EXECUTION_FROZEN_CASE_SET", "case inclusion boundary drift")
    _require(denom.get("primary_denominator") == "COUNT_ALL_FROZEN_INCLUDED_CASES_PER_CONTRAST", "primary denominator drift")
    _require(denom.get("same_primary_denominator_for_C1_C2_C3") is True, "contrast denominator asymmetry")
    _require(denom.get("lane_specific_case_exclusion_forbidden") is True, "lane-specific exclusion must be forbidden")
    _require(denom.get("abstain_is_legal_output") is True, "ABSTAIN must be legal")
    _require(denom.get("abstain_counts_in_primary_denominator") is True, "ABSTAIN must count in denominator")
    _require(denom.get("abstain_silent_drop_forbidden") is True, "silent ABSTAIN drop must be forbidden")
    _require(denom.get("technical_unevaluable_retained") is True, "technical UNEVALUABLE must be retained")
    _require(denom.get("technical_unevaluable_counts_in_primary_denominator") is True, "technical UNEVALUABLE must count in denominator")
    _require(denom.get("technical_failure_must_apply_symmetrically") is True, "technical failure symmetry missing")
    _require(denom.get("coverage_penalized_metric_required") is True, "coverage-penalized metric required")
    _require(denom.get("abstention_scoring_policy_must_be_frozen") is True, "abstention scoring policy must be frozen")
    _require(denom.get("universal_abstain_penalty_claimed") is False, "fixture/profile penalty must not become Qimen doctrine")

    profile_contract = contract.get("abstention_scoring_profile_contract", {})
    required = set(profile_contract.get("required_fields", []))
    _require(
        required
        == {
            "profile_id",
            "fixture_synthetic_values",
            "frozen_before_outcome_scoring",
            "same_for_all_blind_outputs",
            "abstain_metric_value",
            "technical_unevaluable_metric_value",
            "coverage_penalty_mode",
        },
        "abstention scoring profile schema drift",
    )
    _require(
        profile_contract.get("coverage_penalty_mode")
        == "COUNT_IN_PRIMARY_DENOMINATOR_WITH_FROZEN_METRIC_VALUE",
        "coverage penalty mode drift",
    )
    _require(profile_contract.get("per_lane_or_per_blind_override_forbidden") is True, "lane/blind policy override must be forbidden")

    output = contract.get("output_contract", {})
    _require(output.get("contrast_ids") == list(CONTRAST_IDS), "output contrast order drift")
    _require(output.get("C3_component_credit_eligible") is False, "C3 component credit must remain false")

    _require(contract.get("batch") == contract.get("freeze") == contract.get("outcome") == "NONE", "research state mutation")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def validate_profile(profile, contract):
    required = set(contract["abstention_scoring_profile_contract"]["required_fields"])
    _require(set(profile) == required, "abstention scoring profile field drift")
    _require(isinstance(profile.get("profile_id"), str) and profile["profile_id"], "profile id required")
    _require(profile.get("frozen_before_outcome_scoring") is True, "profile must freeze before outcome scoring")
    _require(profile.get("same_for_all_blind_outputs") is True, "profile must be identical for all blind outputs")
    _require(
        profile.get("coverage_penalty_mode")
        == contract["abstention_scoring_profile_contract"]["coverage_penalty_mode"],
        "coverage penalty mode mismatch",
    )
    for key in ("abstain_metric_value", "technical_unevaluable_metric_value"):
        value = profile.get(key)
        _require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), f"{key} must be finite numeric")
    _reject_runtime_identity(profile, "abstention scoring profile")


def validate_contrast_bindings(contrast_bindings, frozen_before_outcome, identity_map, execution_contract):
    _require(frozen_before_outcome is True, "contrast bindings must be frozen before outcome scoring")
    _require(set(contrast_bindings) == set(CONTRAST_IDS), "contrast binding set drift")
    _require(set(identity_map) == {"P2-A", "P2-A_PRIME", "P2-B"}, "validator identity map drift")
    _require(len(set(identity_map.values())) == 3, "blind ids must be unique")
    expected = execution_contract["estimand_lock"]
    for contrast_id in CONTRAST_IDS:
        row = contrast_bindings[contrast_id]
        _require(set(row) == {"candidate_blind_id", "comparator_blind_id"}, f"{contrast_id} binding fields drift")
        _require(
            row["candidate_blind_id"] == identity_map[expected[contrast_id]["candidate"]],
            f"{contrast_id} candidate blind binding drift",
        )
        _require(
            row["comparator_blind_id"] == identity_map[expected[contrast_id]["comparator"]],
            f"{contrast_id} comparator blind binding drift",
        )
    _reject_runtime_identity(contrast_bindings, "contrast bindings")


def _metric_value(output, profile):
    status = output.get("status")
    _require(status in ALLOWED_STATUSES, f"invalid output status: {status}")
    value = output.get("metric_value")
    if status == "PREDICTED":
        _require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), "predicted metric_value must be finite numeric")
        return float(value)
    _require(value is None, f"{status} metric_value must be null")
    if status == "ABSTAIN":
        return float(profile["abstain_metric_value"])
    return float(profile["technical_unevaluable_metric_value"])


def score_cases(cases, frozen_case_ids, contrast_bindings, profile, contract):
    _reject_runtime_identity(cases, "scorer cases")
    _reject_runtime_identity(contrast_bindings, "scorer contrast bindings")
    validate_profile(profile, contract)

    _require(isinstance(frozen_case_ids, list) and frozen_case_ids, "frozen case set required")
    _require(len(frozen_case_ids) == len(set(frozen_case_ids)), "frozen case ids must be unique")
    _require(all(isinstance(x, str) and x for x in frozen_case_ids), "invalid frozen case id")

    case_ids = [case.get("case_id") for case in cases]
    _require(len(case_ids) == len(set(case_ids)), "duplicate case id")
    _require(set(case_ids) == set(frozen_case_ids), "scoring case set drift from frozen inclusion manifest")

    blind_ids = sorted(
        {
            value
            for row in contrast_bindings.values()
            for value in (row["candidate_blind_id"], row["comparator_blind_id"])
        }
    )
    _require(len(blind_ids) == 3, "three blind outputs required")

    aggregates = {
        cid: {
            "contrast_id": cid,
            "denominator": 0,
            "paired_delta_sum": 0.0,
            "predicted_pair_count": 0,
            "abstain_case_count": 0,
            "technical_unevaluable_case_count": 0,
            "component_credit_eligible": cid != "P2-C3",
        }
        for cid in CONTRAST_IDS
    }

    for case in cases:
        _require(case.get("included_before_lane_execution") is True, f"{case.get('case_id')} was not frozen-included")
        _require(set(case) == {"case_id", "included_before_lane_execution", "blind_outputs"}, "case field drift")
        outputs = case["blind_outputs"]
        _require(set(outputs) == set(blind_ids), f"{case['case_id']} blind output set drift")

        statuses = [outputs[blind_id].get("status") for blind_id in blind_ids]
        technical_count = sum(status == "TECHNICAL_UNEVALUABLE" for status in statuses)
        _require(technical_count in (0, len(blind_ids)), f"{case['case_id']} asymmetric technical UNEVALUABLE")

        for cid in CONTRAST_IDS:
            binding = contrast_bindings[cid]
            candidate = outputs[binding["candidate_blind_id"]]
            comparator = outputs[binding["comparator_blind_id"]]
            agg = aggregates[cid]
            agg["denominator"] += 1
            candidate_value = _metric_value(candidate, profile)
            comparator_value = _metric_value(comparator, profile)
            agg["paired_delta_sum"] += candidate_value - comparator_value
            statuses_pair = {candidate["status"], comparator["status"]}
            if candidate["status"] == comparator["status"] == "PREDICTED":
                agg["predicted_pair_count"] += 1
            if "ABSTAIN" in statuses_pair:
                agg["abstain_case_count"] += 1
            if "TECHNICAL_UNEVALUABLE" in statuses_pair:
                agg["technical_unevaluable_case_count"] += 1

    denominator_values = {row["denominator"] for row in aggregates.values()}
    _require(denominator_values == {len(frozen_case_ids)}, "contrast denominator drift")
    results = []
    for cid in CONTRAST_IDS:
        row = aggregates[cid]
        row["paired_delta_sum"] = round(row["paired_delta_sum"], 12)
        row["paired_primary_delta"] = round(row["paired_delta_sum"] / row["denominator"], 12)
        row["coverage_rate"] = round(row["predicted_pair_count"] / row["denominator"], 12)
        results.append(row)

    return {
        "case_inclusion_manifest_sha256": canonical_sha256(sorted(frozen_case_ids)),
        "primary_denominator_policy": contract["denominator_policy"]["primary_denominator"],
        "contrast_results": results,
        "lane_identity_visible_to_scorer": False,
        "outcome_data_used_in_fixture": False,
        "empirical_credit": "NONE",
    }
