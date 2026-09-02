#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge" / "K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V02.json"
TEST = ROOT / "tools" / "test_k2_qimen_p2_domain_source_parity_v02.py"
IMPLEMENTATION = ROOT / "knowledge" / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V14.json"
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V18.json"

EXPECTED_AUDIT_BLOB = "d3c7814f96451db2f33a60f15ef938869a5b2a98"
EXPECTED_TEST_BLOB = "45c41cb9c1b8330947412804b4b5aa97e668d9d7"
EXPECTED_FAIL_FIRST = "f26f08327f24397774854b318190571caced6d5f"
EXPECTED_RUN = 33604974949
EXPECTED_JOB = 100166786641
ATOMIC = ["奇仪", "八门", "八神", "九星", "九宫"]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def main():
    for path in (AUDIT, TEST, IMPLEMENTATION, PROTOCOL):
        require(path.exists(), f"missing parity V02 closure artifact: {path.relative_to(ROOT)}")
    require(git_blob_sha(AUDIT) == EXPECTED_AUDIT_BLOB, "parity V02 audit blob drift")
    require(git_blob_sha(TEST) == EXPECTED_TEST_BLOB, "parity V02 test blob drift")

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    impl = json.loads(IMPLEMENTATION.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))

    require(audit.get("audit_id") == "K2-QIMEN-P2-DOMAIN-SOURCE-PARITY-V02", "audit identity drift")
    require(audit.get("historical_v01_audit_preserved") is True, "historical V01 audit must be preserved")
    require(audit.get("role_parity", {}).get("status") == "PASS_SHARED_ROLE_INTERSECTION", "role parity not closed")
    require(audit.get("atomic_context_parity", {}).get("status") == "PASS_SHARED_SUPERSET_SOURCE_COVERAGE", "atomic parity not closed")
    require(audit.get("atomic_context_parity", {}).get("shared_atomic_context_universe") == ATOMIC, "atomic universe drift")
    require(audit.get("priority_policy_parity", {}).get("status") == "PASS_SOURCE_FAITHFUL_PARTIAL_POLICY_FOR_RESTRICTED_SCOPE", "priority parity not closed")
    b = audit.get("priority_policy_parity", {}).get("P2-B", {})
    require(b.get("primary_atomic_context_set") == ["奇仪", "八门"], "P2-B primary set drift")
    require(b.get("primary_set_internal_order") == "UNORDERED", "P2-B internal order must remain unestablished")
    require(b.get("workplace_total_order_status") == "NOT_SOURCE_ESTABLISHED", "workplace total order must remain unestablished")
    require(audit.get("production_decision", {}).get("domain_source_parity_ready") is True, "domain parity not ready")
    require(audit.get("production_decision", {}).get("production_representation_materialization_allowed") is True, "production representation next-step authorization missing")
    require(audit.get("production_decision", {}).get("production_complexity_profile_materialization_allowed") is False, "complexity profile must not be pre-authorized")
    require(audit.get("production_decision", {}).get("statistical_preregistration_allowed") is False, "statistical prereg must remain blocked")
    require(audit.get("production_decision", {}).get("batch_creation_allowed") is False, "Batch creation must remain blocked")
    require(audit.get("batch") == "NONE" and audit.get("freeze") == "NONE" and audit.get("outcome") == "NONE", "audit cannot create Batch/Freeze/Outcome")
    require(audit.get("empirical_credit") == "NONE", "audit cannot create empirical credit")

    require(impl.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V14", "wrong V14 state")
    require(impl.get("parent_head") == EXPECTED_FAIL_FIRST, "V14 parent drift")
    evidence = impl.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == EXPECTED_FAIL_FIRST, "fail-first commit drift")
    require(evidence.get("workflow_run_id") == EXPECTED_RUN, "fail-first run drift")
    require(evidence.get("job_id") == EXPECTED_JOB, "fail-first job drift")
    require(evidence.get("expected_failure") == "AssertionError: missing Representation V02 domain/source parity audit", "fail-first failure drift")
    require(impl.get("domain_source_parity_v02_git_blob") == EXPECTED_AUDIT_BLOB, "V14 audit blob binding drift")
    require(impl.get("domain_source_parity_v02_test_git_blob") == EXPECTED_TEST_BLOB, "V14 test blob binding drift")
    require(impl.get("domain_source_parity_ready") is True, "V14 parity ready drift")
    require(impl.get("production_representation_materialized") is False, "V14 production representation must remain false")
    require(impl.get("production_representation_materialization_allowed") is True, "V14 production materialization authorization missing")
    require(impl.get("statistical_preregistration_ready") is False, "V14 prereg must remain false")
    require(impl.get("batch_creation_allowed") is False, "V14 Batch creation must remain false")
    require(impl.get("empirical_credit") == "NONE", "V14 empirical credit must remain NONE")

    require(protocol.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V18", "wrong V18 protocol")
    require(protocol.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V17", "V18 predecessor drift")
    require(protocol.get("domain_source_parity_v02", {}).get("status") == "CLOSED_SOURCE_STRUCTURAL_PARITY_RESTRICTED_SCOPE", "V18 parity status drift")
    require(protocol.get("shared_representation", {}).get("atomic_context_universe") == ATOMIC, "V18 shared universe drift")
    require(protocol.get("production_binding_gate", {}).get("production_representation_materialized") is False, "V18 production representation must remain false")
    require(protocol.get("production_binding_gate", {}).get("batch_creation_allowed") is False, "V18 Batch creation must remain false")
    require(protocol.get("batch") == "NONE" and protocol.get("freeze") == "NONE" and protocol.get("outcome") == "NONE", "V18 cannot create Batch/Freeze/Outcome")
    require(protocol.get("empirical_credit") == "NONE", "V18 empirical credit must remain NONE")

    print(
        "k2-qimen-p2-domain-source-parity-v02-validator: PASS "
        "role_parity=PASS atomic_context_parity=PASS priority_policy=PASS_RESTRICTED_SCOPE "
        "production_representation_allowed=true production_representation=false "
        "prereg=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
