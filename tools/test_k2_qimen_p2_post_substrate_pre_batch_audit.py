#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

LEGACY_BUDGET_FIELDS = {
    "role_multiplicity_budget",
    "reasoning_branch_budget",
    "rule_trace_budget",
    "interpreter_information_budget",
    "tool_access_budget",
}
REQUIRED_BUDGET_FIELDS = {
    "max_roles_per_question",
    "max_layers_per_question",
    "max_symbol_instances_per_question",
    "max_total_units_per_lane",
    "max_role_bindings_per_symbol_instance",
}
REQUIRED_SUCCESSOR_FREEZE_FIELDS = {
    "execution_substrate_manifest_sha256",
    "representation_combined_sha256",
    "complexity_budget_profile_sha256",
    "abstention_scoring_profile_sha256",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            rows.append(json.loads(raw))
    return rows


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    plans = load_jsonl(K / "K2_PROSPECTIVE_TEST_PLANS.jsonl")
    qrm_plans = [p for p in plans if p.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm_plans) == 1, "QRM-H1 must have exactly one active plan")
    plan = qrm_plans[0]

    schema = load_json(K / "schema" / "qimen_p2_execution_freeze.schema.json")
    budget_contract = load_json(K / "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json")
    blinding_contract = load_json(K / "K2_QIMEN_P2_BLINDED_LANE_RUNNER_CONTRACT_V01.json")
    denominator_contract = load_json(K / "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json")
    representation_contract = load_json(K / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json")

    drift = []
    freeze_budget_required = set(schema["properties"]["complexity_budget"]["required"])
    if freeze_budget_required == LEGACY_BUDGET_FIELDS:
        drift.append("FREEZE_COMPLEXITY_BUDGET_BINDING_DRIFT")
    if not REQUIRED_BUDGET_FIELDS.issubset(set(budget_contract["budget_profile_requirements"]["required_limits"])):
        drift.append("P2_EXEC_005_REQUIRED_LIMITS_DRIFT")

    plan_fields = set(plan.get("freeze_required_fields", []))
    if LEGACY_BUDGET_FIELDS.issubset(plan_fields) and not REQUIRED_SUCCESSOR_FREEZE_FIELDS.issubset(plan_fields):
        drift.append("ACTIVE_PLAN_FREEZE_BINDING_DRIFT")

    shared_required = set(schema["properties"]["shared_representation"]["required"])
    if "combined_representation_sha256" not in shared_required:
        drift.append("REPRESENTATION_COMBINED_IDENTITY_NOT_FROZEN")
    require(representation_contract["materialization_contract"]["combined_representation_hash_scope"] == "REPRESENTATION_ID_PLUS_COMPONENT_HASH_MAP", "representation combined-hash semantics drift")

    blinding_props = schema["properties"]["blinding"]["properties"]
    if "contract_sha256" not in blinding_props:
        drift.append("BLINDING_CONTRACT_IDENTITY_NOT_FROZEN")
    require(blinding_contract["failure_policy"] == "FAIL_CLOSED", "blinding contract fail-closed drift")

    denominator_props = schema["properties"]["denominator_policy"]["properties"]
    if "contract_sha256" not in denominator_props or "abstention_scoring_profile_sha256" not in denominator_props:
        drift.append("DENOMINATOR_SCORING_CONTRACT_NOT_FROZEN")
    require(denominator_contract["failure_policy"] == "FAIL_CLOSED", "denominator contract fail-closed drift")

    successor = K / "K2_QIMEN_P2_PRE_BATCH_BINDING_CONTRACT_V01.json"
    if successor.exists():
        binding = load_json(successor)
        require(binding.get("status") == "ACTIVE_PRE_BATCH_BINDING", "pre-batch binding contract status drift")
        require(binding.get("batch_creation_allowed") is False, "binding contract must not itself authorize Batch")
        require(binding.get("outcome_data_used") is False, "pre-batch binding cannot use Outcome")
        require(binding.get("empirical_credit") == "NONE", "pre-batch binding cannot grant empirical credit")
        drift = []

    require(not drift, "post-substrate pre-Batch binding drift: " + ",".join(drift))
    print("k2-qimen-p2-post-substrate-pre-batch-audit: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"k2-qimen-p2-post-substrate-pre-batch-audit: FAIL: {exc}", file=sys.stderr)
        raise
