#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

from k2_qimen_p2_materialize_representation import (
    COMPONENT_FIELDS,
    LANE_IDS,
    PARITY_CONTRACT,
    materialize_representation,
    validate_materialized,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
SEMANTIC_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json"
V05_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V05.json"
V06_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V06.json"
IMPL_V01_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V01.json"
IMPL_V02_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V02.json"
REP_CONTRACT_PATH = K / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json"
MATERIALIZER_PATH = ROOT / "tools" / "k2_qimen_p2_materialize_representation.py"
TEST_PATH = ROOT / "tools" / "test_k2_qimen_p2_representation.py"
PLANS_PATH = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"

EXPECTED_CONTRACT_HASH = "1a7128dd4c1ba5846c1d74f78645ff7b1ea87032898bbd83f61859283182393d"
EXPECTED_CONTRACT_BLOB = "c20c0ce08f05a85f4579b31a3b1ff0d996e5e795"
EXPECTED_MATERIALIZER_BLOB = "95937fbc8697ec69e24772241ade648f96611656"
EXPECTED_TEST_BLOB = "b8a3d45ca10ec68251471838b907229854bc8f40"
FAIL_FIRST_COMMIT = "caa9a4ab1863ee8e29cdecfc6c0404b22c8e3572"
FAIL_FIRST_RUN = 33584625223
FAIL_FIRST_JOB = 100106063019
CLOSED = {"P2-EXEC-001", "P2-EXEC-002", "P2-EXEC-003"}
OPEN = {f"P2-EXEC-{i:03d}" for i in range(4, 10)}
EXPECTED_NOT_YET_IMPLEMENTED = {
    "P2-EXEC-004": ROOT / "tools" / "k2_qimen_p2_generate_mapping.py",
    "P2-EXEC-005": ROOT / "tools" / "k2_qimen_p2_enforce_budget.py",
    "P2-EXEC-006": ROOT / "tools" / "k2_qimen_p2_run_blinded_lanes.py",
    "P2-EXEC-007": ROOT / "tools" / "k2_qimen_p2_score.py",
    "P2-EXEC-008": ROOT / "tools" / "k2_qimen_p2_repro_fixture.py",
    "P2-EXEC-009": ROOT / "tools" / "k2_qimen_p2_freeze.py",
}
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class ValidationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load_json(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root must be object: {path}")
    return value


def load_jsonl(path):
    if not path.exists():
        return []
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except Exception as exc:
            raise ValidationError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
        require(isinstance(value, dict), f"JSONL row must be object: {path}:{line_no}")
        rows.append(value)
    return rows


def canonical_sha256(value):
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git_blob_sha1(path):
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_repository():
    semantic = load_json(SEMANTIC_PATH)
    v05 = load_json(V05_PATH)
    v06 = load_json(V06_PATH)
    impl_v01 = load_json(IMPL_V01_PATH)
    impl_v02 = load_json(IMPL_V02_PATH)
    contract = load_json(REP_CONTRACT_PATH)
    plans = load_jsonl(PLANS_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(
        semantic.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V02",
        "semantic protocol identity drift",
    )
    semantic_parity = semantic.get("representation_parity", {})
    for key in (
        "world_variable_manifest_shared",
        "lane_specific_world_variable_addition_forbidden",
        "symbol_vocabulary_shared",
        "feature_extraction_manifest_shared",
        "eligible_rule_pool_shared",
        "prediction_schema_shared",
    ):
        require(semantic_parity.get(key) is True, f"semantic parity guard drift: {key}")

    require(
        v05.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V05",
        "V05 historical identity drift",
    )
    require(
        set(v05.get("closed_execution_blockers", []))
        == {"P2-EXEC-001", "P2-EXEC-002"},
        "V05 historical closure drift",
    )
    require(
        "P2-EXEC-003" in set(v05.get("open_execution_blockers", [])),
        "V05 historical P2-EXEC-003 blocker drift",
    )

    require(
        v06.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V06",
        "V06 identity drift",
    )
    require(v06.get("version") == "0.6", "V06 version drift")
    require(
        v06.get("status") == "PARTIAL_EXECUTION_SUBSTRATE_REPRESENTATION_BOUND",
        "V06 status drift",
    )
    require(
        v06.get("supersedes_protocol_id") == v05.get("protocol_id"),
        "V06 lineage drift",
    )
    require(v06.get("active_plan_id") == "K2PV-QRM-002", "V06 plan drift")
    require(v06.get("hypothesis_id") == "QRM-H1", "V06 hypothesis drift")
    require(
        set(v06.get("closed_execution_blockers", [])) == CLOSED,
        "V06 closed blocker set drift",
    )
    require(
        set(v06.get("open_execution_blockers", [])) == OPEN,
        "V06 open blocker set drift",
    )
    require(
        v06.get("representation_contract_ref")
        == "knowledge/K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json",
        "V06 representation contract ref drift",
    )
    require(
        v06.get("representation_contract_canonical_sha256") == EXPECTED_CONTRACT_HASH,
        "V06 representation contract hash drift",
    )
    require(
        v06.get("representation_parity") == PARITY_CONTRACT,
        "V06 representation parity contract drift",
    )
    require(v06.get("execution_substrate_ready") is False, "V06 overclaims execution readiness")
    require(v06.get("batch_ready") is False, "V06 overclaims Batch readiness")
    require(v06.get("batch_creation_allowed") is False, "V06 must forbid Batch creation")
    require(
        v06.get("batch_gate")
        == "BLOCKED_REMAINING_EXECUTION_SUBSTRATE_P2_EXEC_004_TO_009",
        "V06 batch gate drift",
    )
    for key in ("batch", "freeze", "outcome"):
        require(v06.get(key) == "NONE", f"V06 {key} must remain NONE")
    require(v06.get("empirical_credit") == "NONE", "V06 empirical credit drift")
    require(v06.get("claim_extraction") == "BLOCKED", "V06 claim extraction drift")

    require(
        contract.get("contract_id") == "K2-QIMEN-P2-REPRESENTATION-CONTRACT-V01",
        "representation contract identity drift",
    )
    require(contract.get("version") == "0.1", "representation contract version drift")
    require(contract.get("plan_id") == "K2PV-QRM-002", "representation contract plan drift")
    require(contract.get("hypothesis_id") == "QRM-H1", "representation contract hypothesis drift")
    require(contract.get("capability") == "P2-EXEC-003", "representation capability drift")
    require(
        contract.get("materializer_ref") == "tools/k2_qimen_p2_materialize_representation.py",
        "representation materializer ref drift",
    )
    require(
        contract.get("canonical_serialization") == "UTF8_JSON_SORT_KEYS_COMPACT",
        "representation canonicalization drift",
    )
    require(contract.get("hash_algorithm") == "SHA256", "representation hash algorithm drift")
    require(
        contract.get("representation_source_fields")
        == ["representation_id", *COMPONENT_FIELDS],
        "representation source field contract drift",
    )
    require(
        contract.get("shared_component_fields") == list(COMPONENT_FIELDS),
        "shared component field contract drift",
    )
    require(contract.get("lane_ids") == list(LANE_IDS), "representation lane identity drift")
    require(contract.get("parity_contract") == PARITY_CONTRACT, "representation parity drift")
    materialization_contract = contract.get("materialization_contract", {})
    require(
        materialization_contract
        == {
            "single_shared_source_object": True,
            "component_hash_scope": "FULL_COMPONENT_OBJECT",
            "combined_representation_hash_scope": "REPRESENTATION_ID_PLUS_COMPONENT_HASH_MAP",
            "all_lane_bindings_must_equal_shared_hash_map": True,
            "lane_specific_source_objects_forbidden": True,
        },
        "materialization contract drift",
    )
    require(contract.get("research_only") is True, "representation contract must be research_only")
    require(contract.get("outcome_data_used") is False, "representation contract outcome guard drift")
    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "representation contract canonical hash drift")

    require(
        impl_v01.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V01",
        "V01 implementation history drift",
    )
    require(
        set(impl_v01.get("open_blockers", [])) == {f"P2-EXEC-{i:03d}" for i in range(3, 10)},
        "V01 implementation historical blockers drift",
    )

    require(
        impl_v02.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V02",
        "V02 implementation identity drift",
    )
    require(impl_v02.get("parent_head") == FAIL_FIRST_COMMIT, "V02 implementation parent drift")
    require(impl_v02.get("active_plan_id") == "K2PV-QRM-002", "V02 implementation plan drift")
    require(impl_v02.get("hypothesis_id") == "QRM-H1", "V02 implementation hypothesis drift")
    require(
        impl_v02.get("representation_contract_ref")
        == "knowledge/K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json",
        "V02 implementation representation contract ref drift",
    )
    require(
        impl_v02.get("representation_contract_canonical_sha256") == EXPECTED_CONTRACT_HASH,
        "V02 implementation contract hash drift",
    )
    require(
        impl_v02.get("representation_contract_git_blob") == EXPECTED_CONTRACT_BLOB,
        "V02 implementation contract blob drift",
    )
    require(
        impl_v02.get("representation_materializer_git_blob") == EXPECTED_MATERIALIZER_BLOB,
        "V02 implementation materializer blob drift",
    )
    require(
        impl_v02.get("representation_test_git_blob") == EXPECTED_TEST_BLOB,
        "V02 implementation test blob drift",
    )
    fail_first = impl_v02.get("fail_first_evidence", {})
    require(fail_first.get("commit_sha") == FAIL_FIRST_COMMIT, "fail-first commit drift")
    require(fail_first.get("workflow_run_id") == FAIL_FIRST_RUN, "fail-first run drift")
    require(fail_first.get("job_id") == FAIL_FIRST_JOB, "fail-first job drift")
    require(
        "ModuleNotFoundError" in fail_first.get("expected_failure", ""),
        "fail-first expected failure class drift",
    )
    require(
        fail_first.get("execution_contract_negative_cases_before_failure") == 14,
        "fail-first predecessor negative test count drift",
    )
    closed_rows = {x.get("blocker_id"): x for x in impl_v02.get("closed_blockers", [])}
    require(set(closed_rows) == CLOSED, "V02 implementation closure set drift")
    require(
        closed_rows["P2-EXEC-003"].get("status") == "CLOSED_MACHINE_IMPLEMENTATION",
        "P2-EXEC-003 implementation closure status drift",
    )
    require(
        "production Role/Layer generators do not yet exist"
        in closed_rows["P2-EXEC-003"].get("does_not_claim", ""),
        "P2-EXEC-003 scope guard missing",
    )
    require(set(impl_v02.get("open_blockers", [])) == OPEN, "V02 implementation open blocker drift")
    require(impl_v02.get("execution_substrate_ready") is False, "V02 implementation overclaims readiness")
    require(impl_v02.get("batch_ready") is False, "V02 implementation overclaims Batch readiness")
    require(impl_v02.get("batch_creation_allowed") is False, "V02 implementation must forbid Batch")
    for key in ("batch", "freeze", "outcome"):
        require(impl_v02.get(key) == "NONE", f"V02 implementation {key} must remain NONE")
    require(impl_v02.get("empirical_credit") == "NONE", "V02 implementation empirical credit drift")

    expected_blobs = {
        REP_CONTRACT_PATH: EXPECTED_CONTRACT_BLOB,
        MATERIALIZER_PATH: EXPECTED_MATERIALIZER_BLOB,
        TEST_PATH: EXPECTED_TEST_BLOB,
    }
    for path, expected in expected_blobs.items():
        require(SHA40_RE.match(expected) is not None, f"invalid expected blob sha: {path}")
        require(git_blob_sha1(path) == expected, f"exact git blob binding drift: {path.relative_to(ROOT)}")

    probe = {
        "representation_id": "K2-P2-REPRESENTATION-VALIDATOR-PROBE-V01",
        "world_variable_manifest": {"probe": "world"},
        "symbol_vocabulary": {"probe": "symbol"},
        "feature_extraction_manifest": {"probe": "feature"},
        "eligible_rule_pool": {"probe": "rule"},
        "prediction_schema": {"probe": "prediction"},
    }
    first = materialize_representation(probe)
    second = materialize_representation(json.loads(json.dumps(probe)))
    require(first == second, "representation materializer is not deterministic")
    validate_materialized(first)
    require(
        len({row["shared_representation_sha256"] for row in first["lane_bindings"]}) == 1,
        "shared representation identity differs across lanes",
    )
    require(
        all(
            row["shared_manifest_hashes"] == first["shared_manifest_hashes"]
            for row in first["lane_bindings"]
        ),
        "shared representation component hashes differ across lanes",
    )

    qrm_plans = [p for p in plans if p.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm_plans) == 1 and qrm_plans[0].get("plan_id") == "K2PV-QRM-002", "active QRM plan drift")
    require(qrm_plans[0].get("empirical_credit") == "NONE", "active QRM plan empirical credit drift")
    require(
        not [b for b in batches if b.get("plan_id") == "K2PV-QRM-002" or b.get("hypothesis_id") == "QRM-H1"],
        "P2 Batch exists before full execution substrate closure",
    )
    require(
        not [f for f in freezes if f.get("plan_id") == "K2PV-QRM-002"],
        "P2 Freeze exists before full execution substrate closure",
    )

    for blocker_id, path in EXPECTED_NOT_YET_IMPLEMENTED.items():
        require(not path.exists(), f"{blocker_id} implementation appeared without successor closure: {path.relative_to(ROOT)}")


def main():
    try:
        validate_repository()
    except ValidationError as exc:
        print(f"k2-qimen-p2-representation: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-representation: PASS")
    print(
        "closed=P2-EXEC-001,P2-EXEC-002,P2-EXEC-003 "
        "open=P2-EXEC-004..009 execution_substrate_ready=false "
        "batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
