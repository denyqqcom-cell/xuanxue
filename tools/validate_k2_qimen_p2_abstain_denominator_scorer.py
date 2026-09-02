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
V09_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V09.json"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "1bf117aff2ab7a54570382292b7c75d6e00fe5e28bbef595f3dcb41c7b288c25"
EXPECTED_CONTRACT_BLOB = "15a4aa5beeeed2622f26be1c27cb1c63b103353e"
EXPECTED_FIXTURE_BLOB = "d79f27d71e2ef7759d40a7a6b4ff8f349c938e5b"
EXPECTED_TEST_BLOB = "324057b4f2bd6a61b3ac4167bf60fbbc66aadd4d"
EXPECTED_V05_BLOB = "2ff2fb1b5a27c35f8f00ac6d0cfd0caa97e179c1"
EXPECTED_V09_BLOB = "aa0b9b4494ce64b098a8b8e20e6acae4e60cbd21"


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
    leakage = "\n".join(plan.get("leakage_controls", []))
    require("ABSTAIN 不得静默缩小 denominator" in leakage, "plan ABSTAIN denominator guard missing")
    require("P2-C1" in metrics and "P2-C2" in metrics and "P2-C3" in metrics, "plan contrast metric set drift")
    abstention_rule = plan.get("abstention_rule", "")
    require("ABSTAIN" in abstention_rule and "denominator" in abstention_rule, "plan abstention rule drift")
    require(plan.get("empirical_credit") == "NONE", "plan empirical credit drift")


def validate_repository():
    # Live successor chain: 006 -> 005 -> 004 -> Distillate/TBV source-grounding audit.
    blinded_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    fixture = load_json(FIXTURE_PATH)
    execution = load_json(EXECUTION_PATH)
    v05 = load_json(V05_PATH)
    v09 = load_json(V09_PATH)
    plans = load_jsonl(PLAN_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(git_blob_sha1(CONTRACT_PATH) == EXPECTED_CONTRACT_BLOB, "ABSTAIN/denominator contract blob drift")
    require(git_blob_sha1(FIXTURE_PATH) == EXPECTED_FIXTURE_BLOB, "ABSTAIN/denominator fixture blob drift")
    require(git_blob_sha1(TEST_PATH) == EXPECTED_TEST_BLOB, "ABSTAIN/denominator test blob drift")
    require(git_blob_sha1(V05_PATH) == EXPECTED_V05_BLOB, "V05 historical blob drift")
    require(git_blob_sha1(V09_PATH) == EXPECTED_V09_BLOB, "V09 historical blob drift")
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
    require(rows["P2-C3"]["component_credit_eligible"] is False, "C3 component credit guard drift")
    require(result.get("lane_identity_visible_to_scorer") is False, "scorer lane identity leak")
    require(result.get("empirical_credit") == "NONE", "fixture must carry no empirical credit")

    plan_matches = [row for row in plans if row.get("plan_id") == "K2PV-QRM-002"]
    require(len(plan_matches) == 1, f"expected one active K2PV-QRM-002 plan, found {len(plan_matches)}")
    validate_plan_alignment(plan_matches[0])

    require(v05.get("open_blockers") == ["P2-EXEC-007", "P2-EXEC-008", "P2-EXEC-009"], "V05 historical open blockers drift")
    require(v09.get("open_execution_blockers") == ["P2-EXEC-007", "P2-EXEC-008", "P2-EXEC-009"], "V09 historical open blockers drift")
    require(not [x for x in batches if x.get("plan_id") == "K2PV-QRM-002" or x.get("hypothesis_id") == "QRM-H1"], "P2 Batch exists before substrate closure")
    require(not [x for x in freezes if x.get("plan_id") == "K2PV-QRM-002"], "P2 Freeze exists before substrate closure")


def main():
    try:
        validate_repository()
    except Exception as exc:
        print(f"k2-qimen-p2-abstain-denominator: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-abstain-denominator: PASS")
    print("closed=P2-EXEC-001..006 open=P2-EXEC-007..009 fail-first-awaiting-scorer=true batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE")


if __name__ == "__main__":
    main()
