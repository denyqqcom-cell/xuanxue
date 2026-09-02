#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from k2_qimen_p2_materialize_representation_v02 import (
    ATOMIC_CONTEXT_LAYERS,
    COMPONENT_FIELDS,
    DERIVED_COMPOSITES,
    LANE_IDS,
    materialize_representation_v02,
    validate_materialized_v02,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "knowledge" / "K2_QIMEN_P2_REPRESENTATION_CONTRACT_V02.json"
ONTOLOGY = ROOT / "knowledge" / "K2_QIMEN_P2_ONTOLOGY_DECISION_V01.json"
IMPLEMENTATION = ROOT / "knowledge" / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V13.json"
PROTOCOL = ROOT / "knowledge" / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V17.json"
MATERIALIZER = ROOT / "tools" / "k2_qimen_p2_materialize_representation_v02.py"
TEST = ROOT / "tools" / "test_k2_qimen_p2_representation_v02.py"

EXPECTED_CONTRACT_SHA256 = "ad7b30fb42510132f03dd86dd5d98a0c59653715937a2a43d970b1d58a774180"
EXPECTED_CONTRACT_BLOB = "06a993535fdc992cbcbe9fff6cab4192fe1ef95c"
EXPECTED_MATERIALIZER_BLOB = "2bfa07a926e772e0756959079496db330cce8a14"
EXPECTED_TEST_BLOB = "6480171d0561f85fdc02b993d02cb3c1a7c20b06"
EXPECTED_FAIL_FIRST = "b6fdc18a500ca311220214c59b444238b9c1a8ff"
EXPECTED_FAIL_FIRST_RUN = 33604272961
EXPECTED_FAIL_FIRST_JOB = 100164597265


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical_sha256(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def source_fixture():
    return {
        "representation_id": "QRM-P2-SHARED-SUPERSET-REPRESENTATION-V02-VALIDATOR-FIXTURE",
        "world_variable_manifest": {
            "variables": [
                {"id": "W1", "name": "question_domain", "type": "categorical"},
                {"id": "W2", "name": "asked_object", "type": "categorical"},
                {"id": "W3", "name": "method_layer", "type": "categorical"},
            ]
        },
        "symbol_vocabulary": {
            "atomic_context_layers": list(ATOMIC_CONTEXT_LAYERS),
            "derived_composites": list(DERIVED_COMPOSITES),
            "visibility": "ALL_LANES",
        },
        "feature_extraction_manifest": {
            "features": [
                "symbol_instance",
                "palace_identity",
                "palace_relation",
                "wangshuai",
                "season",
                "configuration_composite",
            ],
            "depth": "SHARED",
            "derived_composite_source": "SHARED_INPUTS_ONLY",
        },
        "eligible_rule_pool": {
            "rule_ids": ["R-SOURCE-ROLE", "R-PRIORITY-POLICY", "R-DERIVED-COMPOSITE"],
            "lane_specific_additions": False,
        },
        "prediction_schema": {
            "type": "object",
            "required": ["prediction", "confidence", "abstain"],
        },
        "priority_policy_schema": {
            "policy_forms": [
                "FIXED_RANKED_SUBSET_WITH_VISIBLE_UNRANKED_CONTEXT",
                "QUESTION_DOMAIN_CONDITIONED_PARTIAL_PRIORITY_OR_PRIMARY_LAYER",
            ],
            "ranked_subset_may_be_partial": True,
            "visible_unranked_context_required_when_not_ranked": True,
            "unsupported_total_order_action": "ABSTAIN_FAIL_CLOSED",
            "plate_value_selected_priority_forbidden": True,
            "outcome_or_feedback_selected_priority_forbidden": True,
        },
    }


def main():
    for path in (CONTRACT, ONTOLOGY, IMPLEMENTATION, PROTOCOL, MATERIALIZER, TEST):
        require(path.exists(), f"missing required V02 closure artifact: {path.relative_to(ROOT)}")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    ontology = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    implementation = json.loads(IMPLEMENTATION.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))

    require(canonical_sha256(contract) == EXPECTED_CONTRACT_SHA256, "Representation V02 contract canonical hash drift")
    require(git_blob_sha(CONTRACT) == EXPECTED_CONTRACT_BLOB, "Representation V02 contract git blob drift")
    require(git_blob_sha(MATERIALIZER) == EXPECTED_MATERIALIZER_BLOB, "Representation V02 materializer git blob drift")
    require(git_blob_sha(TEST) == EXPECTED_TEST_BLOB, "Representation V02 test git blob drift")

    model = contract.get("representation_model", {})
    require(model.get("shared_atomic_context_universe") == list(ATOMIC_CONTEXT_LAYERS), "contract atomic universe drift")
    require(model.get("derived_composites") == list(DERIVED_COMPOSITES), "contract derived composites drift")
    require(model.get("same_feature_universe_all_lanes") is True, "same feature universe guard missing")
    require(model.get("lane_specific_feature_vocabulary_forbidden") is True, "lane-specific vocabulary guard missing")
    require(model.get("derived_composite_promoted_to_atomic_layer_forbidden") is True, "格局 atomic-promotion guard missing")

    boundary = contract.get("materialization_boundary", {})
    require(boundary.get("contract_fixture_materialization_allowed") is True, "contract fixture materialization must be allowed")
    for key in (
        "production_domain_instance_materialization_allowed",
        "production_complexity_profile_materialization_allowed",
        "production_abstention_profile_materialization_allowed",
        "statistical_preregistration_allowed",
        "batch_creation_allowed",
    ):
        require(boundary.get(key) is False, f"{key} must remain false")

    require(ontology.get("pre_batch_gate", {}).get("p2_ontology_002") == "CLOSED_ARCHITECTURE_DECISION", "ontology decision not closed")
    require(ontology.get("architecture_decision", {}).get("shared_atomic_context_universe") == list(ATOMIC_CONTEXT_LAYERS), "ontology/representation atomic universe mismatch")
    require(ontology.get("architecture_decision", {}).get("derived_composites") == list(DERIVED_COMPOSITES), "ontology/representation composite mismatch")

    result = materialize_representation_v02(source_fixture())
    validate_materialized_v02(result)
    require(len(result["lane_bindings"]) == len(LANE_IDS), "lane cardinality drift")
    require(len(result["shared_manifests"]) == len(COMPONENT_FIELDS), "shared component cardinality drift")
    require(all(x["shared_representation_sha256"] == result["shared_representation_sha256"] for x in result["lane_bindings"]), "lane representation digest parity drift")
    require(all(x["shared_atomic_context_universe"] == list(ATOMIC_CONTEXT_LAYERS) for x in result["lane_bindings"]), "lane atomic universe parity drift")

    require(implementation.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V13", "wrong V13 implementation state")
    require(implementation.get("parent_head") == EXPECTED_FAIL_FIRST, "V13 parent head drift")
    evidence = implementation.get("fail_first_evidence", {})
    require(evidence.get("commit_sha") == EXPECTED_FAIL_FIRST, "V13 fail-first commit drift")
    require(evidence.get("workflow_run_id") == EXPECTED_FAIL_FIRST_RUN, "V13 fail-first run drift")
    require(evidence.get("job_id") == EXPECTED_FAIL_FIRST_JOB, "V13 fail-first job drift")
    require(evidence.get("expected_failure") == "ModuleNotFoundError: No module named 'k2_qimen_p2_materialize_representation_v02'", "V13 fail-first failure drift")
    require(implementation.get("representation_v02_contract_git_blob") == EXPECTED_CONTRACT_BLOB, "V13 contract blob binding drift")
    require(implementation.get("representation_v02_contract_canonical_sha256") == EXPECTED_CONTRACT_SHA256, "V13 contract hash binding drift")
    require(implementation.get("representation_v02_materializer_git_blob") == EXPECTED_MATERIALIZER_BLOB, "V13 materializer blob binding drift")
    require(implementation.get("representation_v02_test_git_blob") == EXPECTED_TEST_BLOB, "V13 test blob binding drift")
    require(implementation.get("p2_prebatch_rep_001", {}).get("status") == "CLOSED_MACHINE_CONTRACT_FIXTURE", "V02 machine gate not closed")
    require(implementation.get("p2_prebatch_rep_001", {}).get("production_domain_instance_materialized") is False, "production domain instance must remain false")
    require(implementation.get("domain_source_parity_ready") is False, "domain parity rerun still required")
    require(implementation.get("statistical_preregistration_ready") is False, "statistical prereg must remain false")
    require(implementation.get("batch_creation_allowed") is False, "Batch creation must remain false")
    require(implementation.get("batch") == "NONE" and implementation.get("freeze") == "NONE" and implementation.get("outcome") == "NONE", "Batch/Freeze/Outcome must remain NONE")
    require(implementation.get("empirical_credit") == "NONE", "empirical credit must remain NONE")
    require(implementation.get("claim_extraction") == "BLOCKED", "Claim Extraction must remain blocked")

    require(protocol.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V17", "wrong V17 protocol")
    require(protocol.get("supersedes_protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V16", "V17 predecessor drift")
    rep = protocol.get("representation_v02", {})
    require(rep.get("status") == "CLOSED_MACHINE_CONTRACT_FIXTURE", "V17 Representation V02 status drift")
    require(rep.get("shared_atomic_context_universe") == list(ATOMIC_CONTEXT_LAYERS), "V17 atomic universe drift")
    require(rep.get("derived_composites") == list(DERIVED_COMPOSITES), "V17 composite drift")
    require(rep.get("same_feature_universe_all_lanes") is True, "V17 feature parity guard missing")
    require(protocol.get("domain_source_parity_ready") is False, "V17 must require parity rerun")
    require(protocol.get("batch_creation_allowed") is False, "V17 Batch creation must remain false")
    require(protocol.get("batch") == "NONE" and protocol.get("freeze") == "NONE" and protocol.get("outcome") == "NONE", "V17 Batch/Freeze/Outcome must remain NONE")
    require(protocol.get("empirical_credit") == "NONE", "V17 empirical credit must remain NONE")

    print(
        "k2-qimen-p2-representation-v02: PASS "
        "gate=CLOSED_MACHINE_CONTRACT_FIXTURE atomic_layers=5 derived_composites=1 "
        "lanes=3 shared_components=6 domain_parity_rerun_required=true "
        "production_representation=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
