#!/usr/bin/env python3
import copy
import json
import tempfile
from pathlib import Path

from validate_k2_qimen_p2_post_repin_audit import (
    AUDIT_PATH,
    BATCHES_PATH,
    PLANS_PATH,
    ROOT,
    V03_PATH,
    V04_PATH,
    ValidationError,
    load_json,
    load_jsonl,
    validate_objects,
    validate_repository,
)


def must_fail(v03, v04, audit, plans, batches, root):
    try:
        validate_objects(v03, v04, audit, plans, batches, root=root)
    except ValidationError:
        return
    raise AssertionError("negative mutation unexpectedly passed")


def main():
    validate_repository(ROOT)

    v03 = load_json(V03_PATH)
    v04 = load_json(V04_PATH)
    audit = load_json(AUDIT_PATH)
    plans = load_jsonl(PLANS_PATH)
    batches = load_jsonl(BATCHES_PATH)

    negative_cases = 0
    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)

        x = copy.deepcopy(v04)
        x["batch_ready"] = True
        must_fail(v03, x, audit, plans, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(v04)
        x["open_execution_blockers"] = x["open_execution_blockers"][:-1]
        must_fail(v03, x, audit, plans, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(audit)
        x["blockers"][0]["status"] = "CLOSED"
        must_fail(v03, v04, x, plans, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(audit)
        x["post_repin_checks"][1]["status"] = "PASS"
        must_fail(v03, v04, x, plans, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(plans)
        qrm = next(p for p in x if p.get("hypothesis_id") == "QRM-H1")
        qrm["hypothesis_origin_key"] = "P2-ROLE-MAP-v0.1"
        must_fail(v03, v04, audit, x, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(plans)
        qrm = next(p for p in x if p.get("hypothesis_id") == "QRM-H1")
        qrm["estimand_lock"] = {"P2-C1": {}}
        must_fail(v03, v04, audit, x, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(batches)
        x.append({"batch_id": "ILLEGAL-P2", "plan_id": "K2PV-QRM-002", "hypothesis_id": "QRM-H1"})
        must_fail(v03, v04, audit, plans, x, temp_root)
        negative_cases += 1

        x = copy.deepcopy(v03)
        x["post_repin_audit"]["status"] = "COMPLETE"
        must_fail(x, v04, audit, plans, batches, temp_root)
        negative_cases += 1

        x = copy.deepcopy(audit)
        x["generic_infrastructure_reuse"][0]["status"] = "FULL_P2_EXECUTION_EVIDENCE"
        must_fail(v03, v04, x, plans, batches, temp_root)
        negative_cases += 1

        rel = audit["blockers"][2]["expected_artifact_paths"][0]
        artifact = temp_root / rel
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# implementation appeared without audit closure\n", encoding="utf-8")
        must_fail(v03, v04, audit, plans, batches, temp_root)
        negative_cases += 1

    print(f"k2-qimen-p2-post-repin-audit-tests: PASS negative_cases={negative_cases}")


if __name__ == "__main__":
    main()
