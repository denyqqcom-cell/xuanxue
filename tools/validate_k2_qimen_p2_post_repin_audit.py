#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
V03_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V03.json"
V04_PATH = K / "K2_QIMEN_P2_ROLE_MAP_COMPARATIVE_PROTOCOL_V04.json"
AUDIT_PATH = K / "K2_QIMEN_P2_ROLE_MAP_POST_REPIN_AUDIT_V01.json"
PLANS_PATH = K / "K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"

EXPECTED_BLOCKERS = {f"P2-EXEC-{i:03d}" for i in range(1, 10)}


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


def validate_objects(v03, v04, audit, plans, batches, root=ROOT):
    require(v03.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V03", "V03 identity drift")
    require(v03.get("status") == "PLAN_REPINNED_REAUDIT_REQUIRED", "V03 historical status drift")
    require(v03.get("batch_gate") == "BLOCKED_PENDING_POST_REPIN_AUDIT", "V03 historical gate drift")
    require(v03.get("batch_ready") is False, "V03 historical state must remain not Batch-ready")
    require(v03.get("post_repin_audit", {}).get("status") == "PENDING", "V03 historical pending audit must remain immutable")

    require(v04.get("protocol_id") == "K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V04", "V04 protocol_id drift")
    require(v04.get("version") == "0.4", "V04 version drift")
    require(v04.get("status") == "POST_REPIN_AUDITED_EXECUTION_BLOCKED", "V04 status drift")
    require(v04.get("supersedes_protocol_id") == v03.get("protocol_id"), "V04 must supersede V03")
    require(v04.get("active_plan_id") == "K2PV-QRM-002", "V04 active plan drift")
    require(v04.get("hypothesis_id") == "QRM-H1", "V04 hypothesis drift")
    require(v04.get("post_repin_audit_ref") == "knowledge/K2_QIMEN_P2_ROLE_MAP_POST_REPIN_AUDIT_V01.json", "V04 audit ref drift")
    require(v04.get("post_repin_audit_status") == "COMPLETE_BLOCKED_EXECUTION_SUBSTRATE", "V04 audit state drift")
    require(v04.get("execution_substrate_ready") is False, "V04 cannot claim execution readiness")
    require(v04.get("batch_ready") is False, "V04 cannot be Batch-ready")
    require(v04.get("batch_gate") == "BLOCKED_MISSING_EXECUTION_SUBSTRATE", "V04 gate drift")
    require(v04.get("batch_creation_allowed") is False, "V04 must forbid Batch creation")
    for key in ("batch", "freeze", "outcome"):
        require(v04.get(key) == "NONE", f"V04 {key} must remain NONE")
    require(v04.get("empirical_credit") == "NONE", "V04 empirical credit must remain NONE")
    require(v04.get("claim_extraction") == "BLOCKED", "V04 claim extraction must remain blocked")
    require(set(v04.get("open_execution_blockers", [])) == EXPECTED_BLOCKERS, "V04 blocker set drift")

    require(audit.get("audit_id") == "K2-QIMEN-P2-ROLE-MAP-POST-REPIN-AUDIT-V01", "audit identity drift")
    require(audit.get("audit_stage") == "PRE_BATCH_PRE_FREEZE_PRE_OUTCOME", "audit stage drift")
    require(audit.get("audited_parent_head") == "e4aed3c5cb2d40ee89f9a5e314234cafec62fef7", "audited parent head drift")
    require(audit.get("audited_protocol_id") == v03.get("protocol_id"), "audit target drift")
    require(audit.get("active_plan_id") == "K2PV-QRM-002", "audit plan drift")
    require(audit.get("hypothesis_id") == "QRM-H1", "audit hypothesis drift")
    require(audit.get("audit_result") == "POST_REPIN_COMPLETE_EXECUTION_BLOCKED", "audit verdict drift")
    require(audit.get("execution_substrate_ready") is False, "audit cannot claim execution readiness")
    require(audit.get("batch_ready") is False, "audit cannot be Batch-ready")
    require(audit.get("batch_gate") == "BLOCKED_MISSING_EXECUTION_SUBSTRATE", "audit gate drift")
    for key in ("batch", "freeze", "outcome"):
        require(audit.get(key) == "NONE", f"audit {key} must remain NONE")
    require(audit.get("empirical_credit") == "NONE", "audit empirical credit must remain NONE")
    require(audit.get("claim_extraction") == "BLOCKED", "audit claim extraction must remain blocked")

    checks = {x.get("check_id"): x for x in audit.get("post_repin_checks", [])}
    require(set(checks) == {f"P2-POST-C{i:02d}" for i in range(1, 6)}, "post-repin check set drift")
    require(checks["P2-POST-C01"].get("status") == "PASS", "plan field/provenance check must pass")
    require(checks["P2-POST-C02"].get("status") == "PARTIAL_BLOCKED", "estimand serialization must remain partial-blocked")
    for cid in ("P2-POST-C03", "P2-POST-C04", "P2-POST-C05"):
        require(checks[cid].get("status") == "BLOCKED", f"{cid} must remain blocked")

    blockers = {x.get("blocker_id"): x for x in audit.get("blockers", [])}
    require(set(blockers) == EXPECTED_BLOCKERS, "audit blocker family drift")
    for blocker_id, blocker in blockers.items():
        require(blocker.get("status") == "OPEN_BLOCKER", f"{blocker_id} closed without replacement protocol")
        require(isinstance(blocker.get("reason"), str) and blocker["reason"].strip(), f"{blocker_id} reason missing")
        closure = blocker.get("closure_requires")
        require(isinstance(closure, list) and closure, f"{blocker_id} closure contract missing")
        paths = blocker.get("expected_artifact_paths")
        require(isinstance(paths, list) and paths, f"{blocker_id} expected artifact paths missing")
        for rel in paths:
            require(isinstance(rel, str) and rel and not rel.startswith("/"), f"{blocker_id} invalid expected artifact path")
            require(not (root / rel).exists(), f"{blocker_id} is stale: implementation artifact now exists: {rel}")

    closure = audit.get("closure_policy", {})
    for field in ("all_blockers_must_close", "machine_evidence_required", "new_protocol_version_required_after_closure",
                  "batch_creation_forbidden_until_new_protocol", "outcome_access_forbidden_during_closure"):
        require(closure.get(field) is True, f"closure policy {field} must remain true")

    qrm_plans = [p for p in plans if p.get("hypothesis_id") == "QRM-H1"]
    require(len(qrm_plans) == 1, "exactly one active QRM-H1 plan required")
    plan = qrm_plans[0]
    require(plan.get("plan_id") == "K2PV-QRM-002", "active QRM plan identity drift")
    require(plan.get("hypothesis_origin_key") == "P2-ROLE-MAP-v0.2", "active QRM plan origin drift")
    require(plan.get("status") == "DESIGN_READY", "active QRM plan design status drift")
    require(plan.get("empirical_credit") == "NONE", "active QRM plan cannot gain empirical credit")
    required = set(v03.get("required_plan_freeze_fields", []))
    actual = set(plan.get("freeze_required_fields", []))
    require(required and required.issubset(actual), "active plan lost V02/V03 required freeze fields")

    # The post-repin audit intentionally records a real serialization gap:
    # prose preserves the contrasts, but the active plan does not machine-bind
    # the exact A/A'/B graph as structured data.
    require("estimand_lock" not in plan, "P2-EXEC-001 audit is stale: estimand_lock now exists")
    require("bridge_model_name" not in plan, "P2-EXEC-001 audit is stale: bridge_model_name now exists")

    qrm_batches = [b for b in batches if b.get("plan_id") == "K2PV-QRM-002" or b.get("hypothesis_id") == "QRM-H1"]
    require(not qrm_batches, "P2 Batch exists while execution substrate is blocked")

    generic = audit.get("generic_infrastructure_reuse", [])
    require(len(generic) == 1, "generic infrastructure reuse record drift")
    require(generic[0].get("ref") == "tools/validate_k2_batch_manifest_bindings.py", "generic binder evidence ref drift")
    require(generic[0].get("status") == "PARTIAL_REUSE_ONLY", "generic binder must not be promoted to P2 execution evidence")


def validate_repository(root=ROOT):
    k = root / "knowledge"
    v03 = load_json(k / V03_PATH.name)
    v04 = load_json(k / V04_PATH.name)
    audit = load_json(k / AUDIT_PATH.name)
    plans = load_jsonl(k / PLANS_PATH.name)
    batches = load_jsonl(k / BATCHES_PATH.name)
    validate_objects(v03, v04, audit, plans, batches, root=root)


def main():
    try:
        validate_repository()
    except ValidationError as exc:
        print(f"k2-qimen-p2-post-repin-audit: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("k2-qimen-p2-post-repin-audit: PASS")
    print("result=POST_REPIN_COMPLETE_EXECUTION_BLOCKED blockers=9 batch=NONE freeze=NONE outcome=NONE empirical_credit=NONE")


if __name__ == "__main__":
    main()
