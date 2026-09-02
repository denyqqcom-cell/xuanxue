#!/usr/bin/env python3
import json
from pathlib import Path

from k2_qimen_p2_materialize_production_profile import materialize_production_bundle

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

PATHS = {
    "contract": K / "K2_QIMEN_P2_PRODUCTION_PROFILE_CONTRACT_V01.json",
    "source": K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_SOURCE_V01.json",
    "representation": K / "K2_QIMEN_P2_PRODUCTION_REPRESENTATION_V01.json",
    "profiles": K / "K2_QIMEN_P2_SHARED_PROFILES_V01.json",
    "rep_v02_contract": K / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json",
    "parity_v02": K / "K2_QIMEN_P2_DOMAIN_SOURCE_PARITY_V02.json",
    "complexity_contract": K / "K2_QIMEN_P2_COMPLEXITY_BUDGET_CONTRACT_V01.json",
    "abstain_contract": K / "K2_QIMEN_P2_ABSTAIN_DENOMINATOR_CONTRACT_V01.json",
    "implementation": K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V15.json",
    "protocol": K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V19.json",
}

EXPECTED_BLOBS = {
    "production_profile_contract_git_blob": "c77c600d1f34820450eac367942afd68760e691d",
    "production_representation_source_git_blob": "9a8393f31ac553aaab82960267a987fd542fe84f",
    "production_representation_git_blob": "5459936c725726c834879e5c22f5ef77cf37c35d",
    "shared_profiles_git_blob": "e859a56f393782f923935ddc358c7dc767ff1048",
    "production_profile_materializer_git_blob": "f8cb8a7f57337e190f72deaf7b9dff56b3c58023",
    "production_profile_test_git_blob": "febecbe43962d134cf8fc397e6ed4d5283b4b455",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    values = {name: load(path) for name, path in PATHS.items()}
    bundle = materialize_production_bundle(
        values["contract"],
        values["source"],
        values["profiles"],
        values["rep_v02_contract"],
        values["parity_v02"],
        values["complexity_contract"],
        values["abstain_contract"],
    )
    require(bundle["representation"] == values["representation"], "committed production representation differs from deterministic materialization")
    require(bundle["representation"]["shared_representation_sha256"] == "a440ef84f42b5798ab6bf8b8e5d802b554b2ba05a35810f67eb9f69eebd48fbb", "production representation digest drift")
    require(bundle["profile_hashes"]["complexity_profile_sha256"] == "d84f0b441b03563d7e98f00725a15dc2d1df568d00a8510677fb1a0f7acdcf6c", "complexity profile digest drift")
    require(bundle["profile_hashes"]["abstention_profile_sha256"] == "846672693d242593f370d21e1ed956e322f9b3b35e9d87d0f6be55aa7aff46c3", "abstention profile digest drift")
    require(bundle["profile_hashes"]["shared_profiles_sha256"] == "0f904b1d84b101dea21e1b852d4dda6dcc5422c0ababf39765e114b3f2409e85", "shared profiles digest drift")

    impl = values["implementation"]
    proto = values["protocol"]
    require(impl.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V15", "implementation V15 missing")
    require(proto.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V19", "protocol V19 missing")
    require(impl.get("state_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V19.json", "implementation/protocol binding drift")
    require(proto.get("execution_implementation_ref") == "knowledge/K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V15.json", "protocol/implementation binding drift")
    require(impl.get("production_profile_test_ref") == "tools/test_k2_qimen_p2_production_profile_v02.py", "successor production-profile test ref drift")
    require(impl.get("production_profile_validator_ref") == "tools/validate_k2_qimen_p2_production_profile_v02.py", "successor production-profile validator ref drift")

    for field, expected in EXPECTED_BLOBS.items():
        require(impl.get(field) == expected, f"implementation exact blob binding drift: {field}")

    fail = impl.get("fail_first_evidence", {})
    require(fail.get("commit_sha") == "4795009b17bef3a667615b3aabb987d914bc11eb", "fail-first commit drift")
    require(fail.get("workflow_run_id") == 33605949544, "fail-first workflow run drift")
    require(fail.get("job_id") == 100169833619, "fail-first job drift")
    require(fail.get("expected_failure") == "ModuleNotFoundError: No module named 'k2_qimen_p2_materialize_production_profile'", "fail-first failure mode drift")
    require(fail.get("all_predecessor_p2_steps_passed_before_failure") is True, "fail-first predecessor pass evidence missing")

    repair = impl.get("closure_repair_evidence", {})
    require(repair.get("commit_sha") == "ea3c97eb84ec882811bf3e030e6f08106beafc39", "closure repair commit drift")
    require(repair.get("workflow_run_id") == 33606809624, "closure repair workflow run drift")
    require(repair.get("job_id") == 100172562150, "closure repair job drift")
    require(repair.get("failure") == "AssertionError: negative_cases == 16", "closure repair failure marker drift")
    require(repair.get("repair") == "SUCCESSOR_TEST_RECOUNTS_17_NEGATIVE_CASES_WITHOUT_WEAKENING_GUARDS", "closure repair description drift")

    profile_state = impl.get("p2_prebatch_profile_003", {})
    require(profile_state.get("status") == "CLOSED_RESTRICTED_PRODUCTION_REPRESENTATION_AND_SHARED_PROFILES", "P2-PREBATCH-PROFILE-003 not closed")
    require(profile_state.get("candidate_domain") == "WORKPLACE_ORGANIZATIONAL_RELATIONSHIP_CHANGE", "production domain drift")
    require(profile_state.get("shared_role_ids") == ["asker", "organization", "superior", "peer", "subordinate"], "production role universe drift")
    require(profile_state.get("shared_atomic_context_universe") == ["奇仪", "八门", "八神", "九星", "九宫"], "production atomic context drift")
    require(profile_state.get("derived_composites") == ["格局"], "production composite drift")
    require(profile_state.get("complexity_profile", {}).get("max_total_units_per_lane") == 15, "production complexity total drift")
    require(profile_state.get("abstention_profile", {}).get("abstain_metric_value") == 0.0, "production abstention metric drift")
    require(profile_state.get("statistical_metric_binding") == "PENDING_STATISTICAL_PREREGISTRATION", "statistical binding prematurely closed")
    require(profile_state.get("negative_test_count") == 17, "production-profile negative test count drift")

    for value in (impl, proto):
        require(value.get("production_representation_materialized") is True, "production representation must be materialized")
        require(value.get("production_complexity_budget_profile_materialized") is True, "production complexity profile must be materialized")
        require(value.get("production_abstention_scoring_profile_materialized") is True, "production abstention profile must be materialized")
        require(value.get("statistical_preregistration_ready") is False, "statistical preregistration cannot be claimed")
        require(value.get("batch_ready") is False, "Batch cannot be ready")
        require(value.get("batch_creation_allowed") is False, "Batch creation cannot be allowed")
        require(value.get("batch") == value.get("freeze") == value.get("outcome") == "NONE", "research state mutation detected")
        require(value.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
        require(value.get("claim_extraction") == "BLOCKED", "claim extraction must remain blocked")

    require(proto.get("production_scope", {}).get("workplace_total_order_status") == "NOT_SOURCE_ESTABLISHED", "protocol invented workplace total order")
    require(proto.get("production_scope", {}).get("unsupported_topology_action") == "ABSTAIN_OR_OUT_OF_SCOPE_FAIL_CLOSED", "protocol unsupported topology guard drift")
    require(proto.get("shared_profiles", {}).get("abstain_metric_value") == 0.0, "protocol abstention profile drift")
    require(proto.get("shared_profiles", {}).get("metric_scale_binding") == "PENDING_STATISTICAL_PREREGISTRATION", "protocol metric binding drift")

    print(
        "k2-qimen-p2-production-profile-validator-v02: PASS "
        "gate=CLOSED_RESTRICTED_PRODUCTION_REPRESENTATION_AND_SHARED_PROFILES "
        "representation_sha256=a440ef84f42b5798ab6bf8b8e5d802b554b2ba05a35810f67eb9f69eebd48fbb "
        "negative_cases=17 complexity_total=15 abstain_metric=0.0 "
        "statistical_preregistration=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
