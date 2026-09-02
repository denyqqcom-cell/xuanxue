#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
V04_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V04.json"
V05_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V05.json"
AUDIT_PATH = K / "K2_QIMEN_P2_ROLE_MAP_POST_REPIN_AUDIT_V01.json"
IMPL_PATH = K / "K2_QIMEN_P2_EXECUTION_IMPLEMENTATION_V01.json"
CONTRACT_PATH = K / "K2_QIMEN_P2_EXECUTION_CONTRACT_V01.json"
GEN_SCHEMA_PATH = K / "schema" / "qimen_p2_generator_descriptor.schema.json"
FREEZE_SCHEMA_PATH = K / "schema" / "qimen_p2_execution_freeze.schema.json"
FIXTURE_PATH = ROOT / "tools" / "testdata" / "qimen_p2_generator_descriptor_fixture.json"
PLANS_PATH = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
FREEZES_PATH = K / "K2_PROSPECTIVE_FREEZES.jsonl"
SUCCESSOR_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V06.json"

CLOSED = {"P2-EXEC-001", "P2-EXEC-002"}
OPEN = {f"P2-EXEC-{i:03d}" for i in range(3, 10)}
SHA64_RE = re.compile(r"^[0-9a-f]{64}$")
GENERATOR_FIELDS = {
    "generator_id", "lane_id", "version", "implementation_ref",
    "implementation_sha256", "canonical_input_schema_sha256",
    "canonical_output_schema_sha256", "nondeterminism_policy", "seed",
}
GENERIC_PLAN_FIELDS = {
    "plan_id","hypothesis_id","hypothesis_origin_type","hypothesis_origin_key","hypothesis_origin_ref",
    "model_name","comparator_name","question_scope","unit_of_analysis","freeze_required_fields","evaluation_metrics",
    "success_condition","failure_condition","abstention_rule","leakage_controls",
    "high_risk_policy","update_policy","status","empirical_credit",
}

EXPECTED_ESTIMANDS = {
    "P2-C1": {
        "candidate": "P2-A_PRIME",
        "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_POLICY",
        "all_other_dimensions_equal": True,
        "credit_scope": "TOPOLOGY_ROLE_BINDING_ONLY",
    },
    "P2-C2": {
        "candidate": "P2-B",
        "comparator": "P2-A_PRIME",
        "only_allowed_difference": "LAYER_PRIORITY_POLICY",
        "all_other_dimensions_equal": True,
        "credit_scope": "TOPOLOGY_CONDITIONED_LAYER_PRIORITY_ONLY",
    },
    "P2-C3": {
        "candidate": "P2-B",
        "comparator": "P2-A",
        "only_allowed_difference": "ROLE_BINDING_PLUS_LAYER_PRIORITY",
        "component_credit_forbidden": True,
        "credit_scope": "FULL_BUNDLE_ONLY_NOT_COMPONENT_ATTRIBUTION",
    },
}
EXPECTED_LANES = [
    {
        "lane_id": "P2-A",
        "neutral_execution_label": "LANE-1",
        "model_name": "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01",
        "role_binding_policy": "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY",
        "layer_priority_policy": "FIXED_GLOBAL",
        "fixed_layer_priority": ["奇仪", "八门", "八神", "九星"],
    },
    {
        "lane_id": "P2-A_PRIME",
        "neutral_execution_label": "LANE-2",
        "model_name": "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01",
        "role_binding_policy": "QUESTION_TOPOLOGY_CONDITIONED",
        "layer_priority_policy": "FIXED_GLOBAL",
        "fixed_layer_priority": ["奇仪", "八门", "八神", "九星"],
    },
    {
        "lane_id": "P2-B",
        "neutral_execution_label": "LANE-3",
        "model_name": "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01",
        "role_binding_policy": "QUESTION_TOPOLOGY_CONDITIONED",
        "layer_priority_policy": "QUESTION_TOPOLOGY_CONDITIONED",
        "fixed_layer_priority": None,
    },
]


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


def validate_generator_descriptor(descriptor):
    require(isinstance(descriptor, dict), "generator descriptor must be object")
    require(set(descriptor) == GENERATOR_FIELDS, "generator descriptor fields drift")
    require(isinstance(descriptor.get("generator_id"), str) and descriptor["generator_id"], "generator_id missing")
    require(descriptor.get("lane_id") in {"P2-A", "P2-A_PRIME", "P2-B"}, "generator lane_id invalid")
    require(isinstance(descriptor.get("version"), str) and descriptor["version"], "generator version missing")
    ref = descriptor.get("implementation_ref")
    require(isinstance(ref, str) and ref.startswith("tools/") and ref.endswith(".py"), "generator implementation_ref invalid")
    require(".." not in Path(ref).parts and not ref.startswith("/"), "generator implementation_ref unsafe")
    for key in ("implementation_sha256", "canonical_input_schema_sha256", "canonical_output_schema_sha256"):
        require(isinstance(descriptor.get(key), str) and SHA64_RE.match(descriptor[key]), f"{key} invalid")
    policy = descriptor.get("nondeterminism_policy")
    require(policy in {"DETERMINISTIC", "SEEDED"}, "nondeterminism_policy invalid")
    if policy == "DETERMINISTIC":
        require(descriptor.get("seed") is None, "deterministic generator seed must be null")
    else:
        require(isinstance(descriptor.get("seed"), int) and not isinstance(descriptor.get("seed"), bool), "seeded generator requires integer seed")


def validate_core(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes):
    require(v04.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V04", "V04 identity drift")
    require(v04.get("status") == "POST_REPIN_AUDITED_EXECUTION_BLOCKED", "V04 historical verdict drift")
    require(set(v04.get("open_execution_blockers", [])) == CLOSED | OPEN, "V04 historical blocker set drift")
    require(v04.get("batch_ready") is False and v04.get("execution_substrate_ready") is False, "V04 historical readiness drift")

    require(v05.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V05", "V05 identity drift")
    require(v05.get("version") == "0.5", "V05 version drift")
    require(v05.get("status") == "PARTIAL_EXECUTION_SUBSTRATE_CONTRACT_BOUND", "V05 status drift")
    require(v05.get("supersedes_protocol_id") == v04.get("protocol_id"), "V05 lineage drift")
    require(v05.get("active_plan_id") == "K2PV-QRM-002", "V05 active plan drift")
    require(v05.get("hypothesis_id") == "QRM-H1", "V05 hypothesis drift")
    require(set(v05.get("closed_execution_blockers", [])) == CLOSED, "V05 closed blocker set drift")
    require(set(v05.get("open_execution_blockers", [])) == OPEN, "V05 open blocker set drift")
    require(v05.get("execution_substrate_ready") is False, "V05 cannot claim full execution readiness")
    require(v05.get("batch_ready") is False, "V05 cannot be Batch-ready")
    require(v05.get("batch_creation_allowed") is False, "V05 must forbid Batch creation")
    require(v05.get("batch_gate") == "BLOCKED_REMAINING_EXECUTION_SUBSTRATE_P2_EXEC_003_TO_009", "V05 gate drift")
    for key in ("batch", "freeze", "outcome"):
        require(v05.get(key) == "NONE", f"V05 {key} must remain NONE")
    require(v05.get("empirical_credit") == "NONE", "V05 empirical credit must remain NONE")
    require(v05.get("claim_extraction") == "BLOCKED", "V05 claim extraction must remain blocked")
    generic_policy = v05.get("generic_plan_registry_policy", {})
    require(generic_policy.get("K2PV_QRM_002_must_remain_generic_schema_compatible") is True, "generic plan compatibility guard missing")
    require(generic_policy.get("p2_specific_machine_contract_must_be_external_to_generic_plan_row") is True, "P2 external contract guard missing")

    require(audit.get("audit_id") == "K2-QIMEN-P2-ROLE-MAP-POST-REPIN-AUDIT-V01", "audit identity drift")
    require(audit.get("audit_result") == "POST_REPIN_COMPLETE_EXECUTION_BLOCKED", "audit historical result drift")
    require(audit.get("batch") == "NONE" and audit.get("freeze") == "NONE" and audit.get("outcome") == "NONE", "audit historical no-data state drift")

    require(impl.get("implementation_state_id") == "K2-QIMEN-P2-EXECUTION-IMPLEMENTATION-V01", "implementation state id drift")
    require(impl.get("stage") == "PRE_BATCH_PRE_FREEZE_PRE_OUTCOME", "implementation stage drift")
    require(impl.get("parent_head") == "a0464e5831a4f0a33c985b268ea098631909febf", "implementation parent head drift")
    require(impl.get("active_plan_id") == "K2PV-QRM-002" and impl.get("hypothesis_id") == "QRM-H1", "implementation identity drift")
    require(impl.get("execution_substrate_ready") is False and impl.get("batch_ready") is False, "implementation overclaims readiness")
    require(impl.get("batch_creation_allowed") is False, "implementation must forbid Batch")
    for key in ("batch", "freeze", "outcome"):
        require(impl.get(key) == "NONE", f"implementation {key} must remain NONE")
    require(impl.get("empirical_credit") == "NONE", "implementation empirical credit must remain NONE")
    closed_rows = {x.get("blocker_id"): x for x in impl.get("closed_blockers", [])}
    require(set(closed_rows) == CLOSED, "implementation closure set drift")
    require(all(x.get("status") == "CLOSED_MACHINE_CONTRACT" for x in closed_rows.values()), "closure must be machine-contract only")
    require(set(impl.get("open_blockers", [])) == OPEN, "implementation open blocker set drift")
    require("production mapping generators do not yet exist" in closed_rows["P2-EXEC-002"].get("does_not_claim", ""), "P2-EXEC-002 scope guard missing")

    require(contract.get("contract_id") == "K2-QIMEN-P2-EXECUTION-CONTRACT-V01", "execution contract id drift")
    require(contract.get("version") == "0.1", "execution contract version drift")
    require(contract.get("plan_id") == "K2PV-QRM-002" and contract.get("hypothesis_id") == "QRM-H1", "execution contract plan/hypothesis drift")
    require(contract.get("semantic_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V02.json", "semantic protocol binding drift")
    require(contract.get("state_protocol_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V05.json", "state protocol binding drift")
    require(contract.get("research_only") is True and contract.get("outcome_data_used") is False, "execution contract research/outcome guard drift")
    boundary = contract.get("mapping_boundary", {})
    require(boundary == {"mapping_before_plate_value_access": True, "plate_value_access_before_mapping": False}, "mapping boundary drift")
    require(contract.get("lanes") == EXPECTED_LANES, "machine lane graph drift")
    require(contract.get("estimand_lock") == EXPECTED_ESTIMANDS, "machine estimand lock drift")
    guard = contract.get("component_credit_guard", {})
    require(guard == {
        "P2-C1_requires_exact_single_difference": True,
        "P2-C2_requires_exact_single_difference": True,
        "P2-C3_cannot_award_component_credit": True,
    }, "component-credit guard drift")
    desc_contract = contract.get("generator_descriptor_contract", {})
    require(desc_contract == {
        "schema_ref": "knowledge/schema/qimen_p2_generator_descriptor.schema.json",
        "canonical_serialization": "UTF8_JSON_SORT_KEYS_COMPACT",
        "hash_algorithm": "SHA256",
        "descriptor_hash_scope": "FULL_DESCRIPTOR_OBJECT",
    }, "generator descriptor canonicalization contract drift")
    require(contract.get("future_freeze_schema_ref") == "knowledge/schema/qimen_p2_execution_freeze.schema.json", "future freeze schema ref drift")

    contract_hash = canonical_sha256(contract)
    require(contract_hash == "218bf3dbc8e83421db34d3d8678a17b93c7e1ed981d28ba70ede02c1c145264b", "execution contract canonical hash drift")
    require(v05.get("execution_contract_canonical_sha256") == contract_hash, "V05 contract hash binding drift")
    require(impl.get("execution_contract_canonical_sha256") == contract_hash, "implementation contract hash binding drift")

    require(gen_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "generator schema draft drift")
    require(gen_schema.get("type") == "object" and gen_schema.get("additionalProperties") is False, "generator schema root drift")
    require(set(gen_schema.get("required", [])) == GENERATOR_FIELDS, "generator schema required fields drift")
    props = gen_schema.get("properties", {})
    require(set(props) == GENERATOR_FIELDS, "generator schema properties drift")
    require(set(props.get("lane_id", {}).get("enum", [])) == {"P2-A", "P2-A_PRIME", "P2-B"}, "generator schema lane enum drift")
    require(set(props.get("nondeterminism_policy", {}).get("enum", [])) == {"DETERMINISTIC", "SEEDED"}, "generator schema nondeterminism policy drift")
    require(len(gen_schema.get("allOf", [])) == 2, "generator schema seed conditional contract drift")

    require(freeze_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "freeze schema draft drift")
    require(freeze_schema.get("type") == "object" and freeze_schema.get("additionalProperties") is False, "freeze schema root drift")
    fp = freeze_schema.get("properties", {})
    require(fp.get("artifact_kind", {}).get("const") == "P2_EXECUTION_FREEZE", "future Freeze artifact kind drift")
    require(fp.get("plan_id", {}).get("const") == "K2PV-QRM-002", "future Freeze plan binding drift")
    require(fp.get("hypothesis_id", {}).get("const") == "QRM-H1", "future Freeze hypothesis binding drift")
    mb = fp.get("mapping_boundary", {}).get("properties", {})
    require(mb.get("mapping_before_plate_value_access", {}).get("const") is True, "future Freeze mapping-before-value guard missing")
    require(mb.get("plate_value_access_before_mapping", {}).get("const") is False, "future Freeze value-before-mapping guard drift")
    require(fp.get("estimand_lock", {}).get("const") == EXPECTED_ESTIMANDS, "future Freeze estimand lock drift")
    defs = freeze_schema.get("$defs", {})
    require(defs.get("generator", {}).get("$ref") == "qimen_p2_generator_descriptor.schema.json", "future Freeze generator schema binding drift")
    expected_defs = {
        "laneA": ("P2-A", "GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01", "SOURCE_CATALOG_DOMAIN_SELECTION_ONLY", "FIXED_GLOBAL"),
        "laneAPrime": ("P2-A_PRIME", "GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01", "QUESTION_TOPOLOGY_CONDITIONED", "FIXED_GLOBAL"),
        "laneB": ("P2-B", "TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01", "QUESTION_TOPOLOGY_CONDITIONED", "QUESTION_TOPOLOGY_CONDITIONED"),
    }
    for key, values in expected_defs.items():
        dp = defs.get(key, {}).get("properties", {})
        require(dp.get("lane_id", {}).get("const") == values[0], f"{key} lane id drift")
        require(dp.get("model_name", {}).get("const") == values[1], f"{key} model drift")
        require(dp.get("role_binding_policy", {}).get("const") == values[2], f"{key} role policy drift")
        require(dp.get("layer_priority_policy", {}).get("const") == values[3], f"{key} layer policy drift")
    require(fp.get("research_only", {}).get("const") is True and fp.get("outcome_data_used", {}).get("const") is False, "future Freeze no-outcome guard drift")

    require(fixture.get("fixture_only") is True, "canonicalization fixture must remain fixture_only")
    require("not a production generator or Freeze" in fixture.get("purpose", ""), "fixture non-production guard missing")
    rows = fixture.get("descriptors", [])
    require(isinstance(rows, list) and len(rows) == 3, "canonicalization fixture must contain three descriptors")
    by_lane = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"descriptor", "canonical_sha256"}, "fixture row shape drift")
        descriptor = row.get("descriptor")
        validate_generator_descriptor(descriptor)
        lane = descriptor["lane_id"]
        require(lane not in by_lane, "duplicate fixture lane")
        actual_hash = canonical_sha256(descriptor)
        require(row.get("canonical_sha256") == actual_hash, f"fixture canonical hash drift for {lane}")
        by_lane[lane] = actual_hash
    require(set(by_lane) == {"P2-A", "P2-A_PRIME", "P2-B"}, "fixture lane coverage drift")
    impl_hashes = impl.get("canonicalization_contract", {}).get("fixture_hashes", {})
    require(impl_hashes == by_lane, "implementation fixture hash registry drift")
    require(impl.get("canonicalization_contract", {}).get("serialization") == "UTF8_JSON_SORT_KEYS_COMPACT", "implementation serialization drift")
    require(impl.get("canonicalization_contract", {}).get("hash_algorithm") == "SHA256", "implementation hash algorithm drift")
    require(impl.get("canonicalization_contract", {}).get("scope") == "FULL_DESCRIPTOR_OBJECT", "implementation descriptor hash scope drift")

    qrm_plans = [p for p in plans if p.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm_plans) == 1, "exactly one active QRM-H1 plan required")
    plan = qrm_plans[0]
    require(set(plan) == GENERIC_PLAN_FIELDS, "K2PV-QRM-002 must remain generic PLAN_FIELDS-compatible")
    require(plan.get("plan_id") == "K2PV-QRM-002", "active QRM plan drift")
    require("estimand_lock" not in plan and "bridge_model_name" not in plan, "P2-specific keys leaked into generic plan row")
    require(plan.get("status") == "DESIGN_READY" and plan.get("empirical_credit") == "NONE", "active QRM plan status/credit drift")

    qrm_batches = [b for b in batches if b.get("plan_id") == "K2PV-QRM-002" or b.get("hypothesis_id") == "QRM-H1"]
    require(not qrm_batches, "P2 Batch exists before execution substrate is ready")
    qrm_freezes = [f for f in freezes if f.get("plan_id") == "K2PV-QRM-002"]
    require(not qrm_freezes, "P2 Freeze exists before execution substrate is ready")


def validate_repository(root=ROOT):
    k = root / "knowledge"
    v04 = load_json(k / V04_PATH.name)
    v05 = load_json(k / V05_PATH.name)
    audit = load_json(k / AUDIT_PATH.name)
    impl = load_json(k / IMPL_PATH.name)
    contract = load_json(k / CONTRACT_PATH.name)
    gen_schema = load_json(k / "schema" / GEN_SCHEMA_PATH.name)
    freeze_schema = load_json(k / "schema" / FREEZE_SCHEMA_PATH.name)
    fixture = load_json(root / "tools" / "testdata" / FIXTURE_PATH.name)
    plans = load_jsonl(k / PLANS_PATH.name)
    batches = load_jsonl(k / BATCHES_PATH.name)
    freezes = load_jsonl(k / FREEZES_PATH.name)
    validate_core(v04, v05, audit, impl, contract, gen_schema, freeze_schema, fixture, plans, batches, freezes)

    blob_bindings = {
        CONTRACT_PATH: impl.get("execution_contract_git_blob"),
        GEN_SCHEMA_PATH: impl.get("generator_descriptor_schema_git_blob"),
        FREEZE_SCHEMA_PATH: impl.get("future_freeze_schema_git_blob"),
        FIXTURE_PATH: impl.get("canonicalization_fixture_git_blob"),
    }
    for path, expected_blob in blob_bindings.items():
        require(isinstance(expected_blob, str) and re.match(r"^[0-9a-f]{40}$", expected_blob), f"invalid git blob registry for {path}")
        require(git_blob_sha1(path) == expected_blob, f"exact git blob binding drift: {path.relative_to(root)}")

    if not (root / SUCCESSOR_PATH.relative_to(ROOT)).exists():
        audit_blockers = {x.get("blocker_id"): x for x in audit.get("blockers", [])}
        for blocker_id in sorted(OPEN):
            blocker = audit_blockers.get(blocker_id, {})
            for rel in blocker.get("expected_artifact_paths", []):
                require(not (root / rel).exists(), f"{blocker_id} implementation appeared without successor protocol: {rel}")

    for row in fixture.get("descriptors", []):
        ref = row["descriptor"]["implementation_ref"]
        require(not (root / ref).exists(), f"fixture implementation_ref became a real file and could be mistaken for production evidence: {ref}")


def main():
    try:
        validate_repository()
    except ValidationError as exc:
        print(f"k2-qimen-p2-execution-contract: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-execution-contract: PASS")
    print("closed=P2-EXEC-001,P2-EXEC-002 open=P2-EXEC-003..009 execution_substrate_ready=false batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE")


if __name__ == "__main__":
    main()
