#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from validate_k2_qimen_role_map_comparative import (
    ValidationError,
    required_v02_freeze_fields,
    validate_audit_object,
    validate_history_row,
    validate_repin_object,
    validate_v02_protocol,
    validate_v03_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"


def expect_fail(name, fn):
    try:
        fn()
    except ValidationError:
        return
    raise AssertionError(f"negative case did not fail closed: {name}")


def main():
    v02 = json.loads((K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json").read_text(encoding="utf-8"))
    v03 = json.loads((K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V03.json").read_text(encoding="utf-8"))
    audit = json.loads((K / "K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01.json").read_text(encoding="utf-8"))
    repin = json.loads((K / "K2_QIMEN_P2_ROLE_MAP_PLAN_REPIN_V01.json").read_text(encoding="utf-8"))
    history = json.loads((K / "K2_QIMEN_P2_ROLE_MAP_PLAN_HISTORY.jsonl").read_text(encoding="utf-8").strip())
    required = validate_v02_protocol(v02)
    validate_audit_object(audit)
    validate_repin_object(repin, required)
    validate_v03_protocol(v03, required)
    validate_history_row(history)

    cases = []

    def add_v02(name, mutate):
        def run():
            obj = copy.deepcopy(v02); mutate(obj); validate_v02_protocol(obj)
        cases.append((name, run))

    def add_v03(name, mutate):
        def run():
            obj = copy.deepcopy(v03); mutate(obj); validate_v03_protocol(obj, required)
        cases.append((name, run))

    def add_audit(name, mutate):
        def run():
            obj = copy.deepcopy(audit); mutate(obj); validate_audit_object(obj)
        cases.append((name, run))

    def add_repin(name, mutate):
        def run():
            obj = copy.deepcopy(repin); mutate(obj); validate_repin_object(obj, required)
        cases.append((name, run))

    def add_history(name, mutate):
        def run():
            obj = copy.deepcopy(history); mutate(obj); validate_history_row(obj)
        cases.append((name, run))

    add_v02("v02-empirical-credit", lambda x: x.__setitem__("empirical_credit", "PROVISIONAL"))
    add_v02("v02-batch-ready", lambda x: x.__setitem__("batch_ready", True))
    add_v02("v02-map-after-plate", lambda x: x["mapping_input_boundary"].__setitem__("mapping_before_plate_value_access", False))
    add_v02("v02-plate-before-map", lambda x: x["mapping_input_boundary"].__setitem__("plate_value_access_before_mapping", True))
    add_v02("v02-world-manifest-unshared", lambda x: x["representation_parity"].__setitem__("world_variable_manifest_shared", False))
    add_v02("v02-symbol-vocabulary-unshared", lambda x: x["representation_parity"].__setitem__("symbol_vocabulary_shared", False))
    add_v02("v02-lane-variable-expansion", lambda x: x["representation_parity"].__setitem__("lane_specific_world_variable_addition_forbidden", False))
    add_v02("v02-priority-changes-eligibility", lambda x: x["layer_priority_semantics"].__setitem__("priority_may_not_change_rule_eligibility", False))
    add_v02("v02-priority-early-stop", lambda x: x["layer_priority_semantics"].__setitem__("priority_may_not_enable_early_stop", False))
    add_v02("v02-branch-budget-asymmetry", lambda x: x["complexity_budget"].__setitem__("reasoning_branch_budget_equal", False))
    add_v02("v02-tool-budget-asymmetry", lambda x: x["complexity_budget"].__setitem__("tool_access_budget_equal", False))
    add_v02("v02-cross-lane-leak", lambda x: x["blinding_and_isolation"].__setitem__("no_cross_lane_intermediate_output", False))
    add_v02("v02-unblind-before-freeze", lambda x: x["blinding_and_isolation"].__setitem__("all_predictions_frozen_before_unblinding", False))
    add_v02("v02-abstain-drops-case", lambda x: x["denominator_and_abstention"].__setitem__("abstain_never_silently_drops_case", False))
    add_v02("v02-lane-exclusion", lambda x: x["denominator_and_abstention"].__setitem__("lane_specific_case_exclusion_forbidden", False))
    add_v02("v02-repro-fixture-removed", lambda x: x["determinism_controls"].__setitem__("pre_batch_reproducibility_fixture_required", False))
    add_v02("v02-c1-not-single-difference", lambda x: x["estimand_lock"]["P2-C1"].__setitem__("only_allowed_difference", "ROLE_PLUS_RULES"))
    add_v02("v02-c2-other-dimensions-change", lambda x: x["estimand_lock"]["P2-C2"].__setitem__("all_other_dimensions_equal", False))
    add_v02("v02-future-symbol-hash-missing", lambda x: x["future_batch_freeze_required"].remove("symbol_vocabulary_hash"))
    add_v02("v02-future-denominator-missing", lambda x: x["future_batch_freeze_required"].remove("primary_denominator_policy"))

    add_audit("audit-unsafe-verdict-erased", lambda x: x.__setitem__("audit_result", "V01_BATCH_SAFE"))
    add_audit("audit-self-correction-erased", lambda x: x.__setitem__("prior_status_reassessment", "DESIGN_READY_WAS_CORRECT"))
    add_audit("audit-plan-blocker-erased", lambda x: next(y for y in x["findings"] if y["finding_id"] == "P2-AUD-012").__setitem__("status", "CLOSED_IN_V02"))

    add_repin("repin-wrong-target", lambda x: x.__setitem__("to_plan_id", "K2PV-QRM-999"))
    add_repin("repin-batch-ready", lambda x: x.__setitem__("batch_ready", True))
    add_repin("repin-self-approves-audit", lambda x: x.__setitem__("post_repin_audit_status", "PASSED"))
    add_repin("repin-missing-v02-field", lambda x: x["required_freeze_fields"].remove("reproducibility_fixture_hash"))
    add_repin("repin-old-plan-not-preserved", lambda x: x.__setitem__("old_plan_preserved", False))

    add_v03("v03-batch-ready", lambda x: x.__setitem__("batch_ready", True))
    add_v03("v03-batch-gate-open", lambda x: x.__setitem__("batch_gate", "OPEN"))
    add_v03("v03-batch-created", lambda x: x.__setitem__("batch", "B1"))
    add_v03("v03-empirical-credit", lambda x: x.__setitem__("empirical_credit", "PROVISIONAL"))
    add_v03("v03-active-plan-drift", lambda x: x.__setitem__("active_plan_id", "K2PV-QRM-001"))
    add_v03("v03-origin-drift", lambda x: x.__setitem__("hypothesis_origin_key", "P2-ROLE-MAP-v0.1"))
    add_v03("v03-plan-binding-false", lambda x: x["plan_alignment"].__setitem__("all_v02_future_freeze_fields_bound", False))
    add_v03("v03-old-plan-active", lambda x: x["plan_alignment"].__setitem__("old_plan_absent_from_active_registry", False))
    add_v03("v03-post-audit-self-passed", lambda x: x["post_repin_audit"].__setitem__("status", "PASSED"))
    add_v03("v03-required-field-missing", lambda x: x["required_plan_freeze_fields"].remove("tool_access_budget"))

    add_history("history-wrong-old-plan", lambda x: x.__setitem__("plan_id", "K2PV-QRM-002"))
    add_history("history-wrong-blob", lambda x: x.__setitem__("retired_registry_blob_sha", "0" * 40))
    add_history("history-had-batch", lambda x: x.__setitem__("batch_count_at_retirement", 1))
    add_history("history-had-outcome", lambda x: x.__setitem__("outcome_count_at_retirement", 1))
    add_history("history-credit-laundering", lambda x: x.__setitem__("empirical_credit_at_retirement", "PROVISIONAL"))

    for name, fn in cases:
        expect_fail(name, fn)

    print(f"k2-qimen-role-map-comparative-negative-tests: PASS ({len(cases)} cases)")


if __name__ == "__main__":
    main()
