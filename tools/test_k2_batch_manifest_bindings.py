#!/usr/bin/env python3
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_k2_batch_manifest_bindings as v

ROOT = Path(__file__).resolve().parents[1]


def batch(batch_id="K2PVB-BATCH_001", plan_id="K2PV-TEST-001", model_sha="a" * 40):
    return {
        "batch_id": batch_id,
        "plan_id": plan_id,
        "model_commit_sha": model_sha,
    }


def binding(manifest_ref, manifest, batch_id="K2PVB-BATCH_001"):
    return {
        "batch_id": batch_id,
        "manifest_ref": manifest_ref,
        "manifest_sha256": v.canonical_sha256(manifest),
        "status": "BOUND",
    }


def must_pass(batches, bindings, repo, allowed_prefixes):
    issues = v.validate_bindings(
        batches,
        bindings,
        repo=repo,
        allowed_prefixes=allowed_prefixes,
    )
    assert not issues, issues


def must_fail(batches, bindings, repo, allowed_prefixes, needle):
    issues = v.validate_bindings(
        batches,
        bindings,
        repo=repo,
        allowed_prefixes=allowed_prefixes,
    )
    assert issues, "expected failure"
    text = "; ".join(f"{item_id}: {issue}" for item_id, issue in issues)
    assert needle in text, (needle, text)


def write_manifest(repo, manifest, name="manifest.json"):
    directory = repo / "manifests"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"manifests/{name}"


def base_manifest():
    return {
        "manifest_version": "TEST_V1",
        "batch_id": "K2PVB-BATCH_001",
        "plan_id": "K2PV-TEST-001",
        "model_commit_sha": "a" * 40,
        "research_only": True,
        "outcome_data_used": False,
        "contract": {"scope": "test-only"},
    }


def main():
    # Repository fixture proves a real checked-in file can be canonical-hash bound.
    fixture_path = ROOT / "tools/testdata/prospective_batch_manifest_test.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    fixture_binding = binding("tools/testdata/prospective_batch_manifest_test.json", fixture)
    must_pass(
        [batch()],
        [fixture_binding],
        repo=ROOT,
        allowed_prefixes=("tools/testdata/",),
    )

    # Empty production state remains valid until the first preregistered Batch exists.
    must_pass([], [], repo=ROOT, allowed_prefixes=(v.PRODUCTION_MANIFEST_PREFIX,))

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        manifest = base_manifest()
        ref = write_manifest(repo, manifest)
        good = binding(ref, manifest)
        allowed = ("manifests/",)
        must_pass([batch()], [good], repo, allowed)

        must_fail([batch()], [], repo, allowed, "missing canonical manifest binding")

        dangling = copy.deepcopy(good)
        dangling["batch_id"] = "K2PVB-NOT_FOUND"
        must_fail([batch()], [dangling], repo, allowed, "unknown batch_id")

        must_fail(
            [batch()],
            [good, copy.deepcopy(good)],
            repo,
            allowed,
            "exactly one manifest binding",
        )

        bad_hash = copy.deepcopy(good)
        bad_hash["manifest_sha256"] = "b" * 64
        must_fail([batch()], [bad_hash], repo, allowed, "does not bind exact canonical manifest")

        wrong_batch_manifest = copy.deepcopy(manifest)
        wrong_batch_manifest["batch_id"] = "K2PVB-OTHER"
        wrong_batch_ref = write_manifest(repo, wrong_batch_manifest, "wrong-batch.json")
        must_fail(
            [batch()],
            [binding(wrong_batch_ref, wrong_batch_manifest)],
            repo,
            allowed,
            "manifest batch_id does not match",
        )

        wrong_plan_manifest = copy.deepcopy(manifest)
        wrong_plan_manifest["plan_id"] = "K2PV-OTHER"
        wrong_plan_ref = write_manifest(repo, wrong_plan_manifest, "wrong-plan.json")
        must_fail(
            [batch()],
            [binding(wrong_plan_ref, wrong_plan_manifest)],
            repo,
            allowed,
            "manifest plan_id does not match",
        )

        wrong_model_manifest = copy.deepcopy(manifest)
        wrong_model_manifest["model_commit_sha"] = "c" * 40
        wrong_model_ref = write_manifest(repo, wrong_model_manifest, "wrong-model.json")
        must_fail(
            [batch()],
            [binding(wrong_model_ref, wrong_model_manifest)],
            repo,
            allowed,
            "manifest model_commit_sha does not match",
        )

        outcome_manifest = copy.deepcopy(manifest)
        outcome_manifest["outcome_data_used"] = True
        outcome_ref = write_manifest(repo, outcome_manifest, "outcome-used.json")
        must_fail(
            [batch()],
            [binding(outcome_ref, outcome_manifest)],
            repo,
            allowed,
            "outcome_data_used=false",
        )

        empty_contract_manifest = copy.deepcopy(manifest)
        empty_contract_manifest["contract"] = {}
        empty_contract_ref = write_manifest(repo, empty_contract_manifest, "empty-contract.json")
        must_fail(
            [batch()],
            [binding(empty_contract_ref, empty_contract_manifest)],
            repo,
            allowed,
            "contract must be a non-empty object",
        )

        traversal = copy.deepcopy(good)
        traversal["manifest_ref"] = "manifests/../outside.json"
        must_fail([batch()], [traversal], repo, allowed, "traversal components")

    print("k2-batch-manifest-binding-tests: PASS")
    print("cases=12 exact_hash_binding=PASS one_binding_per_batch=PASS outcome_blind=PASS")


if __name__ == "__main__":
    main()
