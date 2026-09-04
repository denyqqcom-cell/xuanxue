#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as pv
import k2_sample_fingerprint as sf

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"

POLICY_FIELDS={
    "policy_version","fingerprint_method","fingerprint_scope","fingerprint_key_id",
    "require_preoutcome_binding","require_fingerprint_on_every_freeze",
    "require_unique_within_batch","require_unique_within_replication_cohort",
    "raw_identity_repository_storage_forbidden","secret_repository_storage_forbidden","research_only",
}
BINDING_FIELDS={
    "binding_id","batch_id","batch_sha256","bound_at_utc",
    "sample_provenance_policy_version","sample_provenance_policy_sha256",
    "sample_identity_schema_version","sample_identity_schema_sha256",
    "research_only","status",
}
KNOWN_METHODS={"HMAC_SHA256_V1"}
KNOWN_SCOPES={"PROJECT_WIDE"}
BINDING_ID_RE=re.compile(r"^K2PVSPB-[A-Z0-9_-]+$")
POLICY_VERSION_RE=re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
KEY_ID_RE=re.compile(r"^[A-Z][A-Z0-9_-]{2,127}$")
SHA64_RE=re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_RAW_IDENTITY_KEYS={
    "sample_identity","sample_identity_material","raw_sample_identity","raw_identity",
    "fingerprint_secret","sample_fingerprint_secret","sample_fingerprint_key",
}


def fail(msg):
    print(f"k2-sample-provenance: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


def load_policies(root=ROOT):
    return pv.load_jsonl(root/"knowledge"/"K2_PROSPECTIVE_SAMPLE_PROVENANCE_POLICIES.jsonl")


def load_bindings(root=ROOT):
    return pv.load_jsonl(root/"knowledge"/"K2_PROSPECTIVE_SAMPLE_PROVENANCE_BINDINGS.jsonl")


def load_identity_schemas(root=ROOT):
    return sf.load_identity_schemas(root)


def policy_index(rows):
    issues=[];out={}
    if not rows:return out,[("<sample-provenance-policy>","sample provenance policy registry must contain at least one version")]
    for row in rows:
        version=row.get("policy_version") or "<missing>"
        if set(row)!=POLICY_FIELDS:issues.append((version,f"sample provenance policy fields mismatch missing={sorted(POLICY_FIELDS-set(row))} extra={sorted(set(row)-POLICY_FIELDS)}"))
        if not isinstance(version,str) or not POLICY_VERSION_RE.match(version):issues.append((version,"invalid sample provenance policy_version"))
        if version in out:issues.append((version,"duplicate sample provenance policy_version"))
        out[version]=row
        if row.get("fingerprint_method") not in KNOWN_METHODS:issues.append((version,f"fingerprint_method must be one of {sorted(KNOWN_METHODS)}"))
        if row.get("fingerprint_scope") not in KNOWN_SCOPES:issues.append((version,f"fingerprint_scope must be one of {sorted(KNOWN_SCOPES)}"))
        key_id=row.get("fingerprint_key_id")
        if not isinstance(key_id,str) or not KEY_ID_RE.match(key_id):issues.append((version,"fingerprint_key_id must be stable uppercase key identifier"))
        for field in ["require_preoutcome_binding","require_fingerprint_on_every_freeze","require_unique_within_batch","require_unique_within_replication_cohort","raw_identity_repository_storage_forbidden","secret_repository_storage_forbidden","research_only"]:
            if row.get(field) is not True:issues.append((version,f"{field} must be true in current governed sample provenance schema"))
        if pv.PATH_RE.search(json.dumps(row,ensure_ascii=False)):issues.append((version,"sample provenance policy leaks local filesystem path"))
    return out,issues


def recursive_keys(value):
    keys=[]
    if isinstance(value,dict):
        for key,item in value.items():
            keys.append(str(key));keys.extend(recursive_keys(item))
    elif isinstance(value,list):
        for item in value:keys.extend(recursive_keys(item))
    return keys


def validate_records(batches,freezes,bindings,policies,identity_schemas=None):
    issues=[]
    policy_by_version,policy_issues=policy_index(policies);issues.extend(policy_issues)
    schema_rows=load_identity_schemas(ROOT) if identity_schemas is None else identity_schemas
    schema_by_version,schema_issues=sf.identity_schema_index(schema_rows);issues.extend(schema_issues)
    batch_by_id={b.get("batch_id"):b for b in batches}
    freezes_by_batch={}
    for f in freezes:freezes_by_batch.setdefault(f.get("batch_id"),[]).append(f)

    binding_by_batch={};seen_binding_ids=set()
    for row in bindings:
        rid=row.get("binding_id") or "<missing>";bid=row.get("batch_id")
        if set(row)!=BINDING_FIELDS:issues.append((rid,f"sample provenance binding fields mismatch missing={sorted(BINDING_FIELDS-set(row))} extra={sorted(set(row)-BINDING_FIELDS)}"))
        if not isinstance(rid,str) or not BINDING_ID_RE.match(rid):issues.append((rid,"invalid sample provenance binding_id"))
        if rid in seen_binding_ids:issues.append((rid,"duplicate sample provenance binding_id"))
        seen_binding_ids.add(rid)
        if bid in binding_by_batch:issues.append((rid,"a batch may have only one sample provenance binding"))
        binding_by_batch[bid]=row
        batch=batch_by_id.get(bid)
        if not batch:
            issues.append((rid,f"sample provenance binding references unknown batch_id: {bid}"));continue
        if row.get("batch_sha256")!=pv.canonical_sha256(batch):issues.append((rid,"sample provenance binding batch_sha256 does not bind exact preregistered batch"))
        if not isinstance(row.get("batch_sha256"),str) or not SHA64_RE.match(row.get("batch_sha256","")):issues.append((rid,"sample provenance binding batch_sha256 must be lowercase sha256"))
        version=row.get("sample_provenance_policy_version");policy=policy_by_version.get(version)
        if not pv.nonempty_text(version):issues.append((rid,"sample_provenance_policy_version must be non-empty text"))
        elif policy is None:issues.append((rid,f"unknown sample_provenance_policy_version: {version}"))
        policy_sha=row.get("sample_provenance_policy_sha256")
        if not isinstance(policy_sha,str) or not SHA64_RE.match(policy_sha):issues.append((rid,"sample_provenance_policy_sha256 must be lowercase sha256"))
        elif policy is not None and policy_sha!=pv.canonical_sha256(policy):issues.append((rid,"sample_provenance_policy_sha256 does not bind exact registered sample provenance policy"))
        schema_version=row.get("sample_identity_schema_version");schema=schema_by_version.get(schema_version)
        if not pv.nonempty_text(schema_version):issues.append((rid,"sample_identity_schema_version must be non-empty text"))
        elif schema is None:issues.append((rid,f"unknown sample_identity_schema_version: {schema_version}"))
        schema_sha=row.get("sample_identity_schema_sha256")
        if not isinstance(schema_sha,str) or not SHA64_RE.match(schema_sha):issues.append((rid,"sample_identity_schema_sha256 must be lowercase sha256"))
        elif schema is not None and schema_sha!=sf.canonical_sha256(schema):issues.append((rid,"sample_identity_schema_sha256 does not bind exact registered sample identity schema"))
        bound_dt=pv.utc_value(row.get("bound_at_utc"));batch_dt=pv.utc_value(batch.get("preregistered_at_utc"))
        if bound_dt is None:issues.append((rid,"bound_at_utc must be UTC second timestamp ending Z"))
        elif batch_dt and bound_dt<=batch_dt:issues.append((rid,"sample provenance binding must occur after batch preregistration"))
        freeze_times=[pv.utc_value(f.get("frozen_at_utc")) for f in freezes_by_batch.get(bid,[])];freeze_times=[x for x in freeze_times if x]
        if bound_dt and freeze_times and bound_dt>=min(freeze_times):issues.append((rid,"sample provenance binding must occur before first case freeze"))
        if row.get("research_only") is not True:issues.append((rid,"sample provenance binding must be research_only=true"))
        if row.get("status")!="BOUND":issues.append((rid,"sample provenance binding status must be BOUND"))
        if pv.PATH_RE.search(json.dumps(row,ensure_ascii=False)):issues.append((rid,"sample provenance binding leaks local filesystem path"))

    for batch in batches:
        bid=batch.get("batch_id") or "<missing>"
        if bid not in binding_by_batch:issues.append((bid,"preregistered batch requires pre-outcome sample provenance binding"))

    fingerprints_by_batch={}
    for f in freezes:
        fid=f.get("freeze_id") or "<missing>";bid=f.get("batch_id");binding=binding_by_batch.get(bid)
        policy=policy_by_version.get(binding.get("sample_provenance_policy_version")) if isinstance(binding,dict) else None
        schema=schema_by_version.get(binding.get("sample_identity_schema_version")) if isinstance(binding,dict) else None
        payload=f.get("frozen_payload")
        if not isinstance(payload,dict):issues.append((fid,"sample provenance requires frozen_payload object"));continue
        forbidden=sorted(set(recursive_keys(payload)) & FORBIDDEN_RAW_IDENTITY_KEYS)
        if forbidden:issues.append((fid,f"raw identity/secret material forbidden in repository payload: {forbidden}"))
        fingerprint=payload.get("sample_fingerprint")
        if policy is not None and policy.get("require_fingerprint_on_every_freeze"):
            if not isinstance(fingerprint,str) or not SHA64_RE.match(fingerprint):issues.append((fid,"sample_fingerprint must be lowercase 64-char HMAC digest"))
        elif fingerprint is not None and (not isinstance(fingerprint,str) or not SHA64_RE.match(fingerprint)):issues.append((fid,"sample_fingerprint must be lowercase 64-char digest when present"))
        if policy is not None:
            if payload.get("sample_provenance_policy_version")!=policy.get("policy_version"):issues.append((fid,"freeze sample_provenance_policy_version must match preregistered binding"))
            if payload.get("sample_provenance_policy_sha256")!=pv.canonical_sha256(policy):issues.append((fid,"freeze sample_provenance_policy_sha256 must match preregistered binding"))
            if payload.get("sample_fingerprint_key_id")!=policy.get("fingerprint_key_id"):issues.append((fid,"freeze sample_fingerprint_key_id must match registered policy key id"))
        if schema is not None:
            if payload.get("sample_identity_schema_version")!=schema.get("schema_version"):issues.append((fid,"freeze sample_identity_schema_version must match preregistered binding"))
            if payload.get("sample_identity_schema_sha256")!=sf.canonical_sha256(schema):issues.append((fid,"freeze sample_identity_schema_sha256 must match preregistered binding"))
        if isinstance(fingerprint,str) and SHA64_RE.match(fingerprint):fingerprints_by_batch.setdefault(bid,[]).append((fid,fingerprint))

    for bid,pairs in fingerprints_by_batch.items():
        binding=binding_by_batch.get(bid);policy=policy_by_version.get(binding.get("sample_provenance_policy_version")) if isinstance(binding,dict) else None
        if policy and policy.get("require_unique_within_batch"):
            seen={}
            for fid,fingerprint in pairs:
                if fingerprint in seen:issues.append((fid,f"sample_fingerprint duplicates another case inside batch: {seen[fingerprint]}"))
                else:seen[fingerprint]=fid
    return issues


def main():
    project=pv.load_json(K/"PROJECT_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked")
    batches=pv.load_jsonl(K/"K2_PROSPECTIVE_BATCHES.jsonl");freezes=pv.load_jsonl(K/"K2_PROSPECTIVE_FREEZES.jsonl")
    policies=load_policies(ROOT);bindings=load_bindings(ROOT);identity_schemas=load_identity_schemas(ROOT)
    issues=validate_records(batches,freezes,bindings,policies,identity_schemas)
    if issues:fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")
    print("k2-sample-provenance: PASS")
    print(f"policies={len(policies)} identity_schemas={len(identity_schemas)} bindings={len(bindings)} batches={len(batches)} freezes={len(freezes)} issues=0")
    print("real_world_sample_independence_proven=false")


if __name__=="__main__":main()
