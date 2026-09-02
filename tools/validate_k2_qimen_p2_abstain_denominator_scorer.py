#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

import validate_k2_qimen_p2_blinded_lane_runner as blinded_validator
from k2_qimen_p2_abstain_denominator_scorer import (
    score_cases,
    validate_contrast_bindings,
    validate_scorer_contract,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json"
FIXTURE_PATH = ROOT / "tools/testdata/qimen_p2_abstain_denominator_fixture.json"
SCORER_PATH = ROOT / "tools/k2_qimen_p2_abstain_denominator_scorer.py"
TEST_PATH = ROOT / "tools/test_k2_qimen_p2_abstain_denominator_scorer.py"
EXECUTION_PATH = K / "K2_QIMEN_P2_EXECUTION_CONTRACT_V01.json"
PLAN_PATH = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
V05_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V05.json"
V06_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V06.json"
V09_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V09.json"
V10_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V10.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "1bf117aff2ab7a54570382292b7c75d6e00fe5e28bbef595f3dcb41c7b288c25"
EXPECTED_CONTRACT_BLOB = "15a4aa5beeeed2622f26be1c27cb1c63b103353e"
EXPECTED_FIXTURE_BLOB = "d79f27d71e2ef7759d40a7a6b4ff8f349c938e5b"
EXPECTED_SCORER_BLOB = "b3cdd066fe57950ad3037a8a27083c560326e260"
EXPECTED_TEST_BLOB = "324057b4f2bd6a61b3ac4167bf60fbbc66aadd4d"
EXPECTED_V05_BLOB = "2ff2fb1b5a27c35f8f00ac6d0cfd0caa97e179c1"
EXPECTED_V06_BLOB = "e0d00b5c15f5ff659186212f8f1fb578c4722868"
EXPECTED_V09_BLOB = "aa0b9b4494ce64b098a8b8e20e6acae4e60cbd21"
EXPECTED_V10_BLOB = "002ef0782e15cb78caf83cb6e3db274f26ea63a9"
FAIL_FIRST_COMMIT = "f7e3f30adc1cfa916c177a809cc453b72fd88ac1"
FAIL_FIRST_RUN = 33590793237
FAIL_FIRST_JOB = 100124199490


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be object: {path}")
    return value


def load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            value = json.loads(raw)
            require(isinstance(value, dict), f"JSONL row must be object: {path}")
            rows.append(value)
    return rows


def canonical_sha256(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def git_blob_sha1(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate_plan_alignment(plan):
    require(plan.get("plan_id") == "K2PV-QRM-002", "active plan drift")
    freeze_fields = set(plan.get("freeze_required_fields", []))
    for field in (
        "paired_abstention_policy",
        "primary_denominator_policy",
        "abstention_scoring_policy",
        "technical_unevaluable_policy",
        "attribution_contrasts",
    ):
        require(field in freeze_fields, f"plan missing scorer freeze field: {field}")
    metrics = "\n".join(plan.get("evaluation_metrics", []))
    require("coverage-penalized paired score" in metrics, "plan coverage-penalized metric missing")
    require("P2-C1" in metrics and "P2-C2" in metrics and "P2-C3" in metrics, "plan contrast metric set drift")
    leakage = "\n".join(plan.get("leakage_controls", []))
    require("ABSTAIN 不得静默缩小 denominator" in leakage, "plan ABSTAIN denominator guard missing")
    abstention_rule = plan.get("abstention_rule", "")
    require("ABSTAIN" in abstention_rule and "denominator" in abstention_rule, "plan abstention rule drift")
    require(plan.get("empirical_credit") == "NONE", "plan empirical credit drift")


def validate_repository():
    # Live successor chain: 007 -> 006 -> 005 -> 004 -> Distillate/TBV source-grounding audit.
    blinded_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    execution = load_json(EXECUTION_PATH)
    v05 = load_json(V05_PATH)
    v06 = load_json(V06_PATH)
    v09 = load_json(V09_PATH)
    v10 = load_json(V10_PATH)
    plans = load_jsonl(PLAN_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "ABSTAIN/denominator contract blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "ABSTAIN/denominator fixture blob drift")
    require(git_blob_sha1(SCORER_PATH) == EXPECTED_SCORER_BLOB, "ABSTAIN/denominator scorer blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "ABSTAIN/denominator test blob drift")
    require(git_blob_sha1(V05_PATH) == EXPECTED_V05_BLOB, "V05 historical blob drift")
    require(git_blob_sha1(V06_PATH) == EXPECTED_V06_BLOB, "V06 blob drift")
    require(git_blob_sha1(V09_PATH) == EXPECTED_V09_BLOB, "V09 historical blob drift")
    require(git_blob_sha1(V10_PATH) == EXPECTED_V10_BLOB, "V10 blob drift")
    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "ABSTAIN/denominator contract canonical hash drift")

    validate_scorer_contract(contract, execution)
    validate_contrast_bindings(
        fixture["contrast_bindings"],
        fixture["contrast_binding_frozen_before_outcome_scoring"],
        fixture["validator_only_identity_map"],
        execution,
    )
    result = score_cases(
        fixture["cases"],
        fixture["frozen_case_ids"],
        fixture["contrast_bindings"],
        fixture["abstention_scoring_profile"],
        contract,
    )
    rows = {row["contrast_id"]: row for row in result["contrast_results"]}
    require({row["denominator"] for row in rows.values()} == {len(fixture["frozen_case_ids"])}, "primary denominator asymmetry")
    for cid in ("P2-C1", "P2-C2", "P2-C3"):
        expected = fixture["expected"][cid]
        actual = rows[cid]
        require(actual["paired_primary_delta"] == expected["paired_primary_delta"], f"{cid} fixture paired delta drift")
        require(actual["predicted_pair_count"] == expected["predicted_pair_count"], f"{cid} predicted pair count drift")
        require(actual["abstain_case_count"] == expected["abstain_case_count"], f"{cid} ABSTAIN count drift")
        require(actual["technical_unevaluable_case_count"] == expected["technical_unevaluable_case_count"], f"{cid} technical UNEVALUABLE count drift")
    require(rows["P2-C3"]["component_credit_eligible"] is False, "C3 component credit guard drift")
    require(result.get("lane_identity_visible_to_scorer") is False, "scorer lane identity leak")
    require(result.get("empirical_credit") == "NONE", "fixture must carry no empirical credit")

    plan_matches = [row for row in plans if row.get("plan_id") == "K2PV-QRM-002"]
    require(len(plan_matches) == 1, f"expected one active K2PV-QRM-002 plan, found {len(plan_matches)}")
    validate_plan_alignment(plan_matches[0])

    require(v05.get("open_blockers") == ["P2-EXEC-007", "P2-EXEC-008", "P2-EXEC-009"], "V05 historical open blockers drift")
    require(v06.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V06", "V06 id drift")
    require(v06.get("prior_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V05.json", "V06 must append V05")
    require(v06.get("closed_blockers", [])[-1].get("blocker_id") == "P2-EXEC-007", "V06 blocker closure drift")
    require(v06.get("open_blockers") == ["P2-EXEC-008", "P2-EXEC-009"], "V06 open blocker drift")
    require(v06.get("negative_test_count") == 16, "V06 negative test count drift")
    require(v06.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V06 source-local audit marker drift")
    require(v06.get("execution_substrate_ready") is False, "P2 substrate cannot be ready before 008..009")

    require(v09.get("open_execution_blockers") == ["P2-EXEC-007", "P2-EXEC-008", "P2-EXEC-009"], "V09 historical open blockers drift")
    require(v10.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V10", "V10 id drift")
    require(v10.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V09", "V10 must append V09")
    require(v10.get("closed_execution_blockers") == ["P2-EXEC-001", "P2-EXEC-002", "P2-EXEC-003", "P2-EXEC-004", "P2-EXEC-005", "P2-EXEC-006", "P2-EXEC-007"], "V10 closed blockers drift")
    require(v10.get("open_execution_blockers") == ["P2-EXEC-008", "P2-EXEC-009"], "V10 open blockers drift")
    require(v10.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V10 source-local audit marker drift")

    for obj, label in ((contract, "contract"), (v06, "V06"), (v10, "V10")):
        require(obj.get("batch") == "NONE", f"{label} batch must remain NONE")
        require(obj.get("freeze") == "NONE", f"{label} freeze must remain NONE")
        require(obj.get("outcome") == "NONE", f"{label} outcome must remain NONE")
        require(obj.get("empirical_credit") == "NONE", f"{label} empirical credit must remain NONE")
        require(obj.get("claim_extraction") == "BLOCKED", f"{label} claim extraction must remain BLOCKED")

    require(not [x for x in batches if x.get("plan_id") == "K2PV-QRM-002" or x.get("hypothesis_id") == "QRM-H1"], "P2 Batch exists before substrate closure")
    require(not [x for x in freezes if x.get("plan_id") == "K2PV-QRM-002"], "P2 Freeze exists before substrate closure")

    evidence = v06.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit evidence drift")
    require(evidence.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run evidence drift")
    require(evidence.get("job_id") == FAIL_FIRST_JOB, "fail-first job evidence drift")
    require(evidence.get("run_number") == 11, "fail-first run number drift")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-abstain-denominator: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-abstain-denominator: PASS")
    print("closed=P2-EXEC-001..007 open=P2-EXEC-008..009 negative_cases=16 source_local_overgeneralization=PASS execution_substrate_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE")


if __name__ == "__main__":
    main()
