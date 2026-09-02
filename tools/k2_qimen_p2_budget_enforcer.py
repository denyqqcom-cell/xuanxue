#!/usr/bin/env python3
import copy
import hashlib
import json

LANE_IDS = ("P2-A", "P2-A_PRIME", "P2-B")
FORMULA_ID = "P2_SHARED_COMPLEXITY_FORMULA_V01"
ALLOWED_SOURCE_FIELDS = {
    "question_id",
    "question_domain",
    "asked_object",
    "method_layer",
    "role_candidates",
    "layer_ids",
    "symbol_instances",
}
REQUIRED_SOURCE_FIELDS = set(ALLOWED_SOURCE_FIELDS)
FORBIDDEN_SOURCE_FIELDS = {
    "current_plate_symbol_values",
    "current_plate_strength_or_auspiciousness",
    "prediction",
    "outcome",
    "feedback",
    "lane_output",
    "lane_peer_intermediate_output",
    "unregistered_external_omen",
}
REQUIRED_LIMITS = (
    "max_roles_per_question",
    "max_layers_per_question",
    "max_symbol_instances_per_question",
    "max_total_units_per_lane",
    "max_role_bindings_per_symbol_instance",
)
ALLOWED_PROFILE_FIELDS = {
    "profile_id",
    "fixture_synthetic_limits",
    "research_design_choice",
    *REQUIRED_LIMITS,
}
EXPECTED_FORMULA = {
    "role_count": "COUNT_UNIQUE(role_candidates.role_id)",
    "layer_count": "COUNT_UNIQUE(layer_ids)",
    "symbol_instance_count": "COUNT_UNIQUE_CANONICAL(symbol_instances)",
    "total_units_per_lane": "role_count + layer_count + symbol_instance_count",
    "role_bindings_per_symbol_instance": "COUNT(role_candidates grouped by canonical symbol_instance_selector)",
    "same_formula_all_lanes": True,
}


class BudgetError(RuntimeError):
    pass


def _require(condition, message):
    if not condition:
        raise BudgetError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _contains_forbidden_token(value):
    text = canonical_json(value).lower()
    return any(
        token in text
        for token in (
            "current_plate_symbol_values",
            "current_plate_strength_or_auspiciousness",
            "outcome",
            "feedback",
            "prediction",
            "lane_output",
            "lane_peer_intermediate_output",
        )
    )


def validate_contract(contract):
    _require(isinstance(contract, dict), "budget contract must be an object")
    _require(contract.get("contract_id") == "K2-QIMEN-P2-COMPLEXITY-BUDGET-CONTRACT-V01", "contract id drift")
    _require(contract.get("capability") == "P2-EXEC-005", "contract capability drift")
    _require(contract.get("plan_id") == "K2PV-QRM-002", "plan id drift")
    _require(contract.get("hypothesis_id") == "QRM-H1", "hypothesis id drift")

    domain = contract.get("budget_domain", {})
    _require(domain.get("levels") == ["PER_QUESTION", "PER_LANE", "PER_SYMBOL_INSTANCE"], "budget levels drift")
    _require(domain.get("lane_ids") == list(LANE_IDS), "lane ids drift")
    _require(domain.get("shared_formula_id") == FORMULA_ID, "shared formula id drift")
    _require(domain.get("lane_formula_overrides_forbidden") is True, "lane formula overrides must be forbidden")
    _require("lane_formula_overrides" not in domain, "lane-specific budget formula override detected")

    formula = contract.get("shared_formula", {})
    _require(formula == EXPECTED_FORMULA, "shared complexity formula drift")
    _require(not _contains_forbidden_token(formula), "budget formula references forbidden post-freeze data")

    profile_req = contract.get("budget_profile_requirements", {})
    _require(profile_req.get("required_limits") == list(REQUIRED_LIMITS), "required budget limits drift")
    _require(profile_req.get("limits_must_be_positive_integers") is True, "positive integer limit guard missing")
    _require(profile_req.get("profile_must_be_frozen_before_mapping_freeze") is True, "budget pre-mapping freeze guard missing")
    _require(profile_req.get("profile_immutable_after_freeze") is True, "budget immutability guard missing")
    _require(profile_req.get("no_universal_numeric_limits_claimed_by_this_contract") is True, "numeric-limit non-claim missing")

    boundary = contract.get("budget_input_boundary", {})
    _require(set(boundary.get("allowed_pre_freeze_fields", [])) == ALLOWED_SOURCE_FIELDS, "allowed pre-freeze field set drift")
    _require(FORBIDDEN_SOURCE_FIELDS.issubset(set(boundary.get("forbidden_fields", []))), "forbidden field set drift")
    _require(boundary.get("plate_value_access_forbidden") is True, "plate-value access guard missing")
    _require(boundary.get("outcome_access_forbidden") is True, "outcome access guard missing")

    policy = contract.get("enforcement_policy", {})
    _require(policy.get("over_budget_action") == "REJECT_QUESTION_FAIL_CLOSED", "over-budget action must fail closed")
    _require(policy.get("degrade_or_truncate_forbidden") is True, "degrade/truncate must be forbidden")
    _require(policy.get("execute_over_budget_question_forbidden") is True, "over-budget execution must be forbidden")
    _require(policy.get("budget_edit_after_freeze") == "FAIL", "post-freeze budget edit must fail")

    scope = contract.get("source_scope_policy", {})
    _require(scope.get("budget_is_methodological_not_source_semantic") is True, "budget must remain methodological")
    _require(scope.get("source_local_role_layer_rules_may_not_be_promoted_by_budget") is True, "source-local globalization guard missing")
    _require(scope.get("source_derived_role_layer_scope_must_be_preserved") is True, "source scope preservation guard missing")
    _require(scope.get("source_local_overgeneralization_check_required") is True, "source-local audit requirement missing")

    _require(contract.get("research_only") is True, "budget contract must remain research-only")
    _require(contract.get("outcome_data_used") is False, "budget contract cannot use outcome data")
    _require(contract.get("batch_creation_allowed") is False, "budget contract cannot create Batch")
    for field in ("batch", "freeze", "outcome"):
        _require(contract.get(field) == "NONE", f"{field} must remain NONE")
    _require(contract.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    _require(contract.get("claim_extraction") == "BLOCKED", "claim extraction must remain BLOCKED")


def _validate_selector(selector):
    _require(isinstance(selector, dict) and selector, "symbol instance selector must be a non-empty object")
    for key in ("symbol_type", "plate_layer", "instance_role", "relation_direction"):
        _require(isinstance(selector.get(key), str) and selector.get(key), f"symbol instance selector missing {key}")


def _validate_source(source):
    _require(isinstance(source, dict), "budget source must be an object")
    keys = set(source)
    _require(not (keys & FORBIDDEN_SOURCE_FIELDS), "budget source contains forbidden post-freeze fields")
    _require(keys == REQUIRED_SOURCE_FIELDS, "budget source field set drift")
    for key in ("question_id", "question_domain", "asked_object", "method_layer"):
        _require(isinstance(source.get(key), str) and source.get(key), f"budget source missing {key}")

    roles = source.get("role_candidates")
    layers = source.get("layer_ids")
    instances = source.get("symbol_instances")
    _require(isinstance(roles, list), "role_candidates must be a list")
    _require(isinstance(layers, list), "layer_ids must be a list")
    _require(isinstance(instances, list), "symbol_instances must be a list")

    role_ids = []
    selectors = []
    for role in roles:
        _require(isinstance(role, dict), "role candidate must be an object")
        role_id = role.get("role_id")
        _require(isinstance(role_id, str) and role_id, "role candidate missing role_id")
        selector = role.get("symbol_instance_selector")
        _validate_selector(selector)
        role_ids.append(role_id)
        selectors.append(selector)
    _require(len(role_ids) == len(set(role_ids)), "role ids must be unique before budget freeze")

    _require(all(isinstance(x, str) and x for x in layers), "layer ids must be non-empty strings")
    _require(len(layers) == len(set(layers)), "layer ids must be unique before budget freeze")

    instance_keys = []
    for selector in instances:
        _validate_selector(selector)
        instance_keys.append(canonical_json(selector))
    _require(len(instance_keys) == len(set(instance_keys)), "symbol instances must be unique before budget freeze")
    known_instances = set(instance_keys)
    _require(
        all(canonical_json(selector) in known_instances for selector in selectors),
        "role candidate references symbol instance outside frozen symbol-instance set",
    )


def _validate_profile(profile):
    _require(isinstance(profile, dict), "budget profile must be an object")
    _require(set(profile).issubset(ALLOWED_PROFILE_FIELDS), "budget profile contains lane override or unknown field")
    _require(isinstance(profile.get("profile_id"), str) and profile.get("profile_id"), "budget profile id missing")
    for key in REQUIRED_LIMITS:
        value = profile.get(key)
        _require(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{key} must be a positive integer")


def _count(source):
    role_ids = sorted({role["role_id"] for role in source["role_candidates"]})
    layer_ids = sorted(set(source["layer_ids"]))
    instance_map = {canonical_json(x): copy.deepcopy(x) for x in source["symbol_instances"]}
    binding_counts = {key: 0 for key in instance_map}
    for role in source["role_candidates"]:
        key = canonical_json(role["symbol_instance_selector"])
        binding_counts[key] += 1

    role_count = len(role_ids)
    layer_count = len(layer_ids)
    symbol_instance_count = len(instance_map)
    total_units = role_count + layer_count + symbol_instance_count
    per_lane = [
        {
            "lane_id": lane_id,
            "formula_id": FORMULA_ID,
            "role_count": role_count,
            "layer_count": layer_count,
            "symbol_instance_count": symbol_instance_count,
            "total_units": total_units,
        }
        for lane_id in LANE_IDS
    ]
    per_symbol_instance = [
        {
            "symbol_instance_selector": instance_map[key],
            "role_binding_count": binding_counts[key],
        }
        for key in sorted(instance_map)
    ]
    return {
        "per_question": {
            "role_count": role_count,
            "layer_count": layer_count,
            "symbol_instance_count": symbol_instance_count,
        },
        "per_lane": per_lane,
        "per_symbol_instance": per_symbol_instance,
    }


def _assert_within_budget(counts, profile):
    q = counts["per_question"]
    _require(q["role_count"] <= profile["max_roles_per_question"], "role count exceeds per-question budget")
    _require(q["layer_count"] <= profile["max_layers_per_question"], "layer count exceeds per-question budget")
    _require(q["symbol_instance_count"] <= profile["max_symbol_instances_per_question"], "symbol instance count exceeds per-question budget")
    for lane in counts["per_lane"]:
        _require(
            lane["total_units"] <= profile["max_total_units_per_lane"],
            f"{lane['lane_id']} exceeds shared per-lane complexity budget",
        )
    for row in counts["per_symbol_instance"]:
        _require(
            row["role_binding_count"] <= profile["max_role_bindings_per_symbol_instance"],
            "symbol instance exceeds role-binding budget",
        )


def _frozen_payload_hash(value):
    payload = copy.deepcopy(value)
    payload.pop("frozen_payload_sha256", None)
    return canonical_sha256(payload)


def freeze_budget(source, profile, contract):
    validate_contract(contract)
    _validate_source(source)
    _validate_profile(profile)
    counts = _count(source)
    _assert_within_budget(counts, profile)

    frozen = {
        "artifact_kind": "P2_FROZEN_COMPLEXITY_BUDGET",
        "formula_id": FORMULA_ID,
        "lane_ids": list(LANE_IDS),
        "question_id": source["question_id"],
        "budget_frozen_before_mapping": True,
        "budget_immutable_after_freeze": True,
        "budget_source_sha256": canonical_sha256(source),
        "budget_profile_sha256": canonical_sha256(profile),
        "budget_contract_sha256": canonical_sha256(contract),
        "budget_profile": copy.deepcopy(profile),
        "counts": copy.deepcopy(counts),
        "outcome_data_used": False,
        "decision": "ALLOW",
        "over_budget": False,
    }
    frozen["frozen_payload_sha256"] = _frozen_payload_hash(frozen)
    return frozen


def enforce_budget(frozen, source, contract):
    validate_contract(contract)
    _require(isinstance(frozen, dict), "frozen budget must be an object")
    _require(frozen.get("artifact_kind") == "P2_FROZEN_COMPLEXITY_BUDGET", "frozen budget artifact kind drift")
    _require(frozen.get("budget_frozen_before_mapping") is True, "budget was not frozen before mapping")
    _require(frozen.get("budget_immutable_after_freeze") is True, "budget immutability marker missing")
    _require(frozen.get("frozen_payload_sha256") == _frozen_payload_hash(frozen), "frozen budget mutated after freeze")
    _require(frozen.get("budget_contract_sha256") == canonical_sha256(contract), "budget contract changed after freeze")
    _require(frozen.get("budget_source_sha256") == canonical_sha256(source), "budget source changed after freeze")
    _validate_source(source)
    _validate_profile(frozen.get("budget_profile"))
    _require(
        frozen.get("budget_profile_sha256") == canonical_sha256(frozen["budget_profile"]),
        "budget profile changed after freeze",
    )
    counts = _count(source)
    _require(counts == frozen.get("counts"), "frozen complexity counts changed")
    _assert_within_budget(counts, frozen["budget_profile"])
    _require(frozen.get("outcome_data_used") is False, "outcome data use detected")
    result = copy.deepcopy(frozen)
    result["decision"] = "ALLOW"
    result["over_budget"] = False
    result["per_lane"] = copy.deepcopy(counts["per_lane"])
    result["per_symbol_instance"] = copy.deepcopy(counts["per_symbol_instance"])
    return result
