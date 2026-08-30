#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
BATCHES_PATH = K / "K2_PROSPECTIVE_BATCHES.jsonl"
BINDINGS_PATH = K / "K2_PROSPECTIVE_BATCH_MANIFEST_BINDINGS.jsonl"
PRODUCTION_MANIFEST_PREFIX = "knowledge/preregistration_manifests/"

BINDING_FIELDS = {"batch_id", "manifest_ref", "manifest_sha256", "status"}
MANIFEST_REQUIRED_FIELDS = {
    "manifest_version",
    "batch_id",
    "plan_id",
    "model_commit_sha",
    "research_only",
    "outcome_data_used",
    "contract",
}
SHA64_RE = re.compile(r"^[0-9a-f]{64}$")
PATH_LEAK_RE = re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(message):
    print(f"k2-batch-manifest-bindings: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


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
            fail(f"invalid JSONL {path}:{line_no}: {exc}")
        if not isinstance(value, dict):
            fail(f"row must be object {path}:{line_no}")
        rows.append(value)
    return rows


def canonical_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def safe_manifest_path(repo, manifest_ref, allowed_prefixes):
    if not isinstance(manifest_ref, str) or not manifest_ref.strip():
        return None, "manifest_ref must be non-empty text"
    if "\\" in manifest_ref or manifest_ref.startswith("/"):
        return None, "manifest_ref must be repository-relative POSIX path"
    parts = Path(manifest_ref).parts
    if ".." in parts or "." in parts:
        return None, "manifest_ref must not contain traversal components"
    if not any(manifest_ref.startswith(prefix) for prefix in allowed_prefixes):
        return None, f"manifest_ref outside allowed roots: {manifest_ref}"
    resolved = (repo / manifest_ref).resolve()
    repo_resolved = repo.resolve()
    try:
        resolved.relative_to(repo_resolved)
    except ValueError:
        return None, "manifest_ref resolves outside repository"
    return resolved, None


def validate_bindings(
    batches,
    bindings,
    repo=ROOT,
    allowed_prefixes=(PRODUCTION_MANIFEST_PREFIX,),
):
    issues = []
    batch_by_id = {}
    for batch in batches:
        batch_id = batch.get("batch_id")
        if isinstance(batch_id, str) and batch_id:
            if batch_id in batch_by_id:
                issues.append((batch_id, "duplicate batch_id in prospective batches"))
            batch_by_id[batch_id] = batch

    binding_by_batch = {}
    for index, binding in enumerate(bindings, 1):
        batch_id = binding.get("batch_id") or f"binding-row-{index}"
        if set(binding) != BINDING_FIELDS:
            issues.append(
                (
                    batch_id,
                    "binding fields mismatch "
                    f"missing={sorted(BINDING_FIELDS-set(binding))} "
                    f"extra={sorted(set(binding)-BINDING_FIELDS)}",
                )
            )
        if binding.get("status") != "BOUND":
            issues.append((batch_id, "binding status must be BOUND"))
        if batch_id not in batch_by_id:
            issues.append((batch_id, "binding references unknown batch_id"))
        if batch_id in binding_by_batch:
            issues.append((batch_id, "batch must have exactly one manifest binding"))
        else:
            binding_by_batch[batch_id] = binding

        manifest_hash = binding.get("manifest_sha256")
        if not isinstance(manifest_hash, str) or not SHA64_RE.match(manifest_hash):
            issues.append((batch_id, "manifest_sha256 must be lowercase sha256"))

        manifest_ref = binding.get("manifest_ref")
        path, path_error = safe_manifest_path(repo, manifest_ref, allowed_prefixes)
        if path_error:
            issues.append((batch_id, path_error))
            continue
        if not path.exists() or not path.is_file():
            issues.append((batch_id, f"manifest file missing: {manifest_ref}"))
            continue
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append((batch_id, f"invalid manifest JSON: {exc}"))
            continue
        if not isinstance(manifest, dict):
            issues.append((batch_id, "manifest must be a JSON object"))
            continue

        missing = MANIFEST_REQUIRED_FIELDS - set(manifest)
        if missing:
            issues.append((batch_id, f"manifest missing required fields: {sorted(missing)}"))
        actual_hash = canonical_sha256(manifest)
        if manifest_hash != actual_hash:
            issues.append((batch_id, "manifest_sha256 does not bind exact canonical manifest"))

        batch = batch_by_id.get(batch_id)
        if batch:
            if manifest.get("batch_id") != batch_id:
                issues.append((batch_id, "manifest batch_id does not match bound batch"))
            if manifest.get("plan_id") != batch.get("plan_id"):
                issues.append((batch_id, "manifest plan_id does not match bound batch"))
            if manifest.get("model_commit_sha") != batch.get("model_commit_sha"):
                issues.append((batch_id, "manifest model_commit_sha does not match bound batch"))
        if manifest.get("research_only") is not True:
            issues.append((batch_id, "manifest must remain research_only=true"))
        if manifest.get("outcome_data_used") is not False:
            issues.append((batch_id, "manifest must declare outcome_data_used=false"))
        contract = manifest.get("contract")
        if not isinstance(contract, dict) or not contract:
            issues.append((batch_id, "manifest contract must be a non-empty object"))
        serialized = json.dumps(manifest, ensure_ascii=False)
        if PATH_LEAK_RE.search(serialized):
            issues.append((batch_id, "manifest leaks local filesystem path"))

    for batch_id in batch_by_id:
        if batch_id not in binding_by_batch:
            issues.append((batch_id, "preregistered batch missing canonical manifest binding"))

    return issues


def main():
    batches = load_jsonl(BATCHES_PATH)
    bindings = load_jsonl(BINDINGS_PATH)
    issues = validate_bindings(batches, bindings)
    if issues:
        first_id, first_issue = issues[0]
        fail(f"issues={len(issues)} first={first_id}: {first_issue}")
    print("k2-batch-manifest-bindings: PASS")
    print(
        f"batches={len(batches)} bindings={len(bindings)} "
        "canonical_manifest_binding=ENFORCED outcome_data_used=false issues=0"
    )


if __name__ == "__main__":
    main()
