#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

import validate_k2_qimen_p2_representation as representation_validator
from k2_qimen_p2_generate_mapping import (
    FIXED_GLOBAL_PRIORITY,
    LANE_IDS,
    generate_all_lane_mappings,
    validate_pre_plate_input,
)

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
CONTRACT_PATH = K / "K2_QIMEN_P2_ROLE_LAYER_GENERATOR_CONTRACT_V01.json"
V06_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V06.json"
V07_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V07.json"
IMPL_V02_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V02.json"
IMPL_V03_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V03.json"
GENERATOR_PATH = ROOT / "tools" / "k2_qimen_p2_generate_mapping.py"
TEST_PATH = ROOT / "tools" / "test_k2_qimen_p2_role_layer_generators.py"
VALIDATOR_PATH = ROOT / "tools" / "validate_k2_qimen_p2_role_layer_generators.py"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_role_layer_generator_fixture.json"
PLANS_PATH = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"
SHANTIADAO_ACCEPTANCE_PATH = K / "K2_SHANTIADAO_PER_BOOK_ACCEPTANCE.md"
TBV_STATE_PATH = K / "K2_QIMEN_TBV_STATE.json"

EXPECTED_CONTRACT_HASH = "5bca2e5544cadf3e1dad2f8e150dffd93b0a12b1d3295d8ab01f56b0ff18bf63"
FAIL_FIRST_COMMIT = "fa3fa045c03511639c78fc02334d5668126cb5f6"
FAIL_FIRST_RUN = 33587987744
FAIL_FIRST_JOB = 100116022003
CLOSED = {f"P2-EXEC-{i:03d}" for i in range(1, 5)}
OPEN = {f"P2-EXEC-{i:03d}" for i in range(5, 10)}
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


def aggregate_jsonl(base_path, shard_dir):
    rows = load_jsonl(base_path)
    if shard_dir.exists():
        for path in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(path))
    return rows


def canonical_sha256(value):
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git_blob_sha1(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def find_one(rows, predicate, label):
    matches = [row for row in rows if predicate(row)]
    require(len(matches) == 1, f"{label}: expected one row, found {len(matches)}")
    return matches[0]


def joined(row, *keys):
    parts = []
    for key in keys:
        value = row.get(key)
        if isinstance(value, list):
            parts.extend(str(x) for x in value)
        elif value is not None:
            parts.append(str(value))
    return "\n".join(parts)


def validate_source_grounding(contract, fixture, mappings):
    source_constraints = {
        row.get("source_key"): row for row in contract.get("source_constraints", [])
    }
    require(
        set(source_constraints)
        == {
            "QM-SRC-0003",
            "QM-SRC-0021",
            "WF-QM-JINHAN-YUJING-001",
            "COURSE-QM-SHANTIADAO-001",
        },
        "source constraint set drift",
    )
    require(
        source_constraints["QM-SRC-0003"].get("globalizable_scope")
        == "LAYER_PRIORITY_ONLY",
        "QM-SRC-0003 may globalize only the frozen layer-priority baseline",
    )
    for key in (
        "QM-SRC-0021",
        "WF-QM-JINHAN-YUJING-001",
        "COURSE-QM-SHANTIADAO-001",
    ):
        require(
            source_constraints[key].get("globalizable_scope") == "NONE",
            f"{key} source-local scope drift",
        )

    wave1 = aggregate_jsonl(
        K / "K2_BOOK_DISTILLATES_WAVE1.jsonl",
        K / "K2_BOOK_DISTILLATES_WAVE1.d",
    )
    d0003 = find_one(wave1, lambda row: row.get("source_id") == "QM-SRC-0003", "QM-SRC-0003 distillate")
    text0003 = joined(d0003, "method_map", "anti_patterns", "model_updates")
    require("Eligible Rule Set Freeze" in text0003, "QM-SRC-0003 Eligible Rule Set Freeze missing")
    require("固定全局优先级" in text0003, "QM-SRC-0003 global-priority limitation missing")

    deep = aggregate_jsonl(
        K / "K2_DEEP_SOURCE_DISTILLATES.jsonl",
        K / "K2_DEEP_SOURCE_DISTILLATES.d",
    )
    d0021 = find_one(deep, lambda row: row.get("source_id") == "QM-SRC-0021", "QM-SRC-0021 deep distillate")
    require(d0021.get("claim_extraction_blocked") is True, "QM-SRC-0021 claim gate drift")
    require(d0021.get("empirical_credit") == "NONE", "QM-SRC-0021 empirical credit drift")
    text0021 = joined(d0021, "essence", "method_map", "anti_patterns", "model_updates")
    require("问题域" in text0021, "QM-SRC-0021 question-domain conditioning missing")
    require("事后" in text0021, "QM-SRC-0021 hindsight-repair warning missing")

    work_families = aggregate_jsonl(
        K / "K2_WORK_FAMILY_DISTILLATES.jsonl",
        K / "K2_WORK_FAMILY_DISTILLATES.d",
    )
    jinhan = find_one(
        work_families,
        lambda row: row.get("work_family_key") == "WF-QM-JINHAN-YUJING-001",
        "Jinhan Yujing work-family distillate",
    )
    require(jinhan.get("claim_extraction_blocked") is True, "Jinhan claim gate drift")
    require(jinhan.get("empirical_credit") == "NONE", "Jinhan empirical credit drift")
    jinhan_text = joined(jinhan, "method_map", "model_updates", "applicability_constraints")
    require("question_domain" in jinhan_text and "asked_object" in jinhan_text, "Jinhan role topology qualifiers missing")
    require(
        ("SymbolType" in jinhan_text and "SymbolInstance" in jinhan_text)
        or "layer-qualified" in jinhan_text,
        "Jinhan layer-qualified symbol-instance constraint missing",
    )

    shantiadao = [
        find_one(deep, lambda row, sid=sid: row.get("source_id") == sid, f"{sid} deep distillate")
        for sid in ("QM-SRC-0027", "QM-SRC-0028", "QM-SRC-0029")
    ]
    for row in shantiadao:
        require(
            row.get("course_family_id") == "COURSE-QM-SHANTIADAO-001",
            f"{row.get('source_id')} course-family drift",
        )
        require(
            row.get("independence_policy") == "COURSE_FAMILY_SINGLE_VOTE",
            f"{row.get('source_id')} provenance-vote drift",
        )
        require(row.get("claim_extraction_blocked") is True, f"{row.get('source_id')} claim gate drift")
        require(row.get("empirical_credit") == "NONE", f"{row.get('source_id')} empirical credit drift")
    require(
        "ROLE_CANDIDATE_LIBRARY" in joined(shantiadao[0], "model_updates"),
        "Shantiadao Role Candidate Library missing",
    )
    acceptance = SHANTIADAO_ACCEPTANCE_PATH.read_text(encoding="utf-8")
    require("Role Candidate Library" in acceptance, "Shantiadao Role Candidate Library acceptance missing")
    require("Correction Rule Registry" in acceptance, "Shantiadao Correction Rule Registry acceptance missing")

    tbv = load_json(TBV_STATE_PATH)
    require(tbv.get("empirical_credit") == "NONE", "Qimen TBV empirical credit drift")
    require(tbv.get("claim_extraction_blocked") is True, "Qimen TBV claim gate drift")

    pre = fixture["pre_plate_input"]
    question_domain = pre["question_domain"]
    catalog_ids = {row["role_id"] for row in pre["source_role_catalog"]}
    topology_ids = {row["role_id"] for row in pre["topology_role_candidates"]}
    require(catalog_ids == topology_ids, "topology generator invented/dropped a role outside shared catalog")
    require(
        all("QM-SRC-0003" in row["source_refs"] for row in pre["source_role_catalog"]),
        "P2-A fixture no longer exercises QM-SRC-0003 source catalog",
    )
    require(
        all("QM-SRC-0021" in row["source_refs"] for row in pre["topology_role_candidates"]),
        "topology fixture no longer exercises QM-SRC-0021 constraints",
    )
    require(
        pre["topology_layer_priority"].get("fixture_synthetic_order") is True,
        "synthetic topology-order fixture must remain explicitly non-source-claim",
    )

    for lane in mappings.values():
        for role in lane["roles"]:
            require(role["source_scope"] == question_domain, "generated role escaped question-domain source scope")
            selector = role["symbol_instance_selector"]
            require(bool(selector.get("plate_layer")), "generated role lost plate-layer identity")
            require(bool(selector.get("relation_direction")), "generated role lost relation direction")
        for correction in lane["correction_registry"]:
            require(correction["source_scope"] == question_domain, "generated correction escaped source scope")
        require(lane.get("outcome_data_used") is False, "generator accessed outcome data")

    require(
        [row["role_id"] for row in mappings["P2-A"]["roles"]]
        == sorted(catalog_ids),
        "P2-A weakened/dropped source catalog roles",
    )
    require(
        mappings["P2-A"]["layer_priority"] == list(FIXED_GLOBAL_PRIORITY),
        "P2-A source-faithful fixed layer priority drift",
    )
    require(
        mappings["P2-A_PRIME"]["layer_priority"] == list(FIXED_GLOBAL_PRIORITY),
        "P2-A_PRIME fixed layer priority drift",
    )
    require(
        mappings["P2-A_PRIME"]["roles"] == mappings["P2-B"]["roles"],
        "P2-C2 changed role binding in addition to layer priority",
    )


def validate_repository():
    representation_validator.EXPECTED_NOT_YET_IMPLEMENTED = {
        blocker_id: path
        for blocker_id, path in representation_validator.EXPECTED_NOT_YET_IMPLEMENTED.items()
        if blocker_id != "P2-EXEC-004"
    }
    representation_validator.validate_repository()

    contract = load_json(CONTRACT_PATH)
    v06 = load_json(V06_PATH)
    v07 = load_json(V07_PATH)
    impl_v02 = load_json(IMPL_V02_PATH)
    impl_v03 = load_json(IMPL_V03_PATH)
    fixture = load_json(FIXTURE_PATH)
    plans = load_jsonl(PLANS_PATH)
    batches = load_jsonl(BATCHES_PATH)
    freezes = load_jsonl(FREEZES_PATH)

    require(contract.get("contract_id") == "K2-QIMEN-P2-ROLE-LAYER-GENERATOR-CONTRACT-V01", "role/layer contract id drift")
    require(contract.get("version") == "0.1" and contract.get("capability") == "P2-EXEC-004", "role/layer contract capability drift")
    require(contract.get("status") == "ACTIVE_FAIL_FIRST_CONTRACT", "role/layer contract status drift")
    require(contract.get("plan_id") == "K2PV-QRM-002" and contract.get("hypothesis_id") == "QRM-H1", "role/layer plan/hypothesis drift")
    require(canonical_sha256(contract) == EXPECTED_CONTRACT_HASH, "role/layer contract canonical hash drift")
    boundary = contract.get("mapping_input_boundary", {})
    require(boundary.get("mapping_before_plate_value_access") is True, "mapping-before-plate boundary missing")
    require(
        {"current_plate_symbol_values", "outcome", "feedback"}.issubset(set(boundary.get("forbidden_input_fields", []))),
        "forbidden post-mapping inputs drift",
    )
    require(contract.get("research_only") is True and contract.get("outcome_data_used") is False, "role/layer research/outcome guard drift")
    for key in ("batch", "freeze", "outcome"):
        require(contract.get(key) == "NONE", f"role/layer contract {key} must remain NONE")
    require(contract.get("empirical_credit") == "NONE" and contract.get("claim_extraction") == "BLOCKED", "role/layer epistemic guard drift")

    expected_lanes = [
        ("P2-A", "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY", "FIXED_GLOBAL"),
        ("P2-A_PRIME", "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "QUESTION_TOPOLOGY_CONDITIONED", "FIXED_GLOBAL"),
        ("P2-B", "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "QUESTION_TOPOLOGY_CONDITIONED", "QUESTION_TOPOLOGY_CONDITIONED"),
    ]
    actual_lanes = [
        (row.get("lane_id"), row.get("model_name"), row.get("role_binding_policy"), row.get("layer_priority_policy"))
        for row in contract.get("lanes", [])
    ]
    require(actual_lanes == expected_lanes, "three-lane contract drift")
    require(contract["lanes"][0].get("fixed_layer_priority") == list(FIXED_GLOBAL_PRIORITY), "P2-A fixed priority drift")
    require(contract["lanes"][1].get("fixed_layer_priority") == list(FIXED_GLOBAL_PRIORITY), "P2-A_PRIME fixed priority drift")
    require(contract["lanes"][2].get("fixed_layer_priority") is None, "P2-B must not inherit fixed priority")

    require(v06.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V06", "V06 historical identity drift")
    require(set(v06.get("closed_execution_blockers", [])) == {f"P2-EXEC-{i:03d}" for i in range(1, 4)}, "V06 historical closure drift")
    require(impl_v02.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V02", "V02 historical implementation drift")

    require(v07.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V07", "V07 identity drift")
    require(v07.get("version") == "0.7", "V07 version drift")
    require(v07.get("supersedes_protocol_id") == v06.get("protocol_id"), "V07 lineage drift")
    require(set(v07.get("closed_execution_blockers", [])) == CLOSED, "V07 closed blocker set drift")
    require(set(v07.get("open_execution_blockers", [])) == OPEN, "V07 open blocker set drift")
    require(v07.get("execution_substrate_ready") is False and v07.get("batch_ready") is False, "V07 overclaims readiness")
    require(v07.get("batch_creation_allowed") is False, "V07 must forbid Batch creation")
    for key in ("batch", "freeze", "outcome"):
        require(v07.get(key) == "NONE", f"V07 {key} must remain NONE")
    require(v07.get("empirical_credit") == "NONE" and v07.get("claim_extraction") == "BLOCKED", "V07 epistemic state drift")
    require(v07.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V07 source-local audit not PASS")

    require(impl_v03.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V03", "V03 implementation identity drift")
    require(impl_v03.get("parent_head") == FAIL_FIRST_COMMIT, "V03 parent/fail-first identity drift")
    require(impl_v03.get("state_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V07.json", "V03 state protocol drift")
    fail_first = impl_v03.get("fail_first_evidence", {})
    require(fail_first.get("commit_sha") == FAIL_FIRST_COMMIT, "P2-004 fail-first commit drift")
    require(fail_first.get("workflow_run_id") == FAIL_FIRST_RUN, "P2-004 fail-first run drift")
    require(fail_first.get("job_id") == FAIL_FIRST_JOB, "P2-004 fail-first job drift")
    require("ModuleNotFoundError" in fail_first.get("expected_failure", ""), "P2-004 fail-first failure class drift")
    require(fail_first.get("predecessor_execution_negative_cases") == 14, "P2-004 predecessor execution negative count drift")
    require(fail_first.get("predecessor_representation_negative_cases") == 5, "P2-004 predecessor representation negative count drift")

    closed_rows = {row.get("blocker_id"): row for row in impl_v03.get("closed_blockers", [])}
    require(set(closed_rows) == CLOSED, "V03 implementation closure set drift")
    require(closed_rows["P2-EXEC-004"].get("status") == "CLOSED_MACHINE_IMPLEMENTATION", "P2-EXEC-004 closure status drift")
    require(impl_v03.get("negative_test_count") == 10, "P2-004 negative test count drift")
    require(set(impl_v03.get("open_blockers", [])) == OPEN, "V03 implementation open blocker drift")
    require(impl_v03.get("execution_substrate_ready") is False and impl_v03.get("batch_ready") is False, "V03 overclaims readiness")
    for key in ("batch", "freeze", "outcome"):
        require(impl_v03.get(key) == "NONE", f"V03 {key} must remain NONE")
    require(impl_v03.get("empirical_credit") == "NONE" and impl_v03.get("claim_extraction") == "BLOCKED", "V03 epistemic state drift")
    require(impl_v03.get("source_local_overgeneralization_check", {}).get("status") == "PASS", "V03 source-local audit not PASS")

    expected_blob_bindings = {
        CONTRACT_PATH: impl_v03.get("role_layer_contract_git_blob"),
        GENERATOR_PATH: impl_v03.get("generator_git_blob"),
        TEST_PATH: impl_v03.get("test_git_blob"),
        VALIDATOR_PATH: impl_v03.get("validator_git_blob"),
        FIXTURE_PATH: impl_v03.get("fixture_git_blob"),
    }
    for path, expected in expected_blob_bindings.items():
        require(isinstance(expected, str) and SHA40_RE.match(expected), f"invalid blob binding for {path.relative_to(ROOT)}")
        require(git_blob_sha1(path) == expected, f"exact blob binding drift: {path.relative_to(ROOT)}")

    require(fixture.get("fixture_only") is True, "role/layer fixture must remain fixture-only")
    require("not a source claim" in fixture.get("purpose", ""), "fixture non-claim guard missing")
    pre = fixture.get("pre_plate_input")
    validate_pre_plate_input(pre)
    first = generate_all_lane_mappings(pre)
    second = generate_all_lane_mappings(json.loads(json.dumps(pre)))
    require(first == second, "role/layer generator is not deterministic")
    require(tuple(first) == LANE_IDS, "role/layer lane set/order drift")

    validate_source_grounding(contract, fixture, first)

    qrm_plans = [row for row in plans if row.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm_plans) == 1 and qrm_plans[0].get("plan_id") == "K2PV-QRM-002", "active QRM plan drift")
    require(qrm_plans[0].get("empirical_credit") == "NONE", "active QRM plan empirical credit drift")
    require(
        not [row for row in batches if row.get("plan_id") == "K2PV-QRM-002" or row.get("hypothesis_id") == "QRM-H1"],
        "P2 Batch exists before full execution substrate closure",
    )
    require(
        not [row for row in freezes if row.get("plan_id") == "K2PV-QRM-002"],
        "P2 Freeze exists before full execution substrate closure",
    )


def main():
    try:
        validate_repository()
    except (ValidationError, representation_validator.ValidationError) as exc:
        print(f"k2-qimen-p2-role-layer-generator: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-role-layer-generator: PASS")
    print(
        "closed=P2-EXEC-001..004 open=P2-EXEC-005..009 "
        "negative_cases=10 source_local_overgeneralization=PASS "
        "execution_substrate_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
