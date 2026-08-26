#!/usr/bin/env python3
import json,sys
from generate_k2_unknown_textual_backlog import ROOT,OUT,REGISTRY,STATE_VERSION,build_state,render,source_index,load_jsonl,validate_corrections

TOP_KEYS={"schema_version","raw_unknown_textual_source_count","resolved_by_k2_discovery_count","remaining_unknown_textual_source_count","resolved_source_ids","claim_extraction_blocked","generated_from"}


def fail(msg):
    print(f"k2-semantic-discovery-routing: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)


def shape_issues(v):
    issues=[]
    if not isinstance(v,dict):return ["state must be object"]
    if set(v)!=TOP_KEYS:issues.append(f"state keys mismatch: {sorted(set(v)^TOP_KEYS)}")
    if v.get("schema_version")!=STATE_VERSION:issues.append("schema_version mismatch")
    for k in ("raw_unknown_textual_source_count","resolved_by_k2_discovery_count","remaining_unknown_textual_source_count"):
        x=v.get(k)
        if not isinstance(x,int) or isinstance(x,bool) or x<0:issues.append(f"{k} must be non-negative integer")
    ids=v.get("resolved_source_ids")
    if not isinstance(ids,list) or len(ids)!=len(set(ids)) or any(not isinstance(x,str) or not x for x in ids):issues.append("resolved_source_ids must be unique non-empty strings")
    if isinstance(ids,list) and isinstance(v.get("resolved_by_k2_discovery_count"),int) and len(ids)!=v.get("resolved_by_k2_discovery_count"):
        issues.append("resolved source count mismatch")
    if all(isinstance(v.get(k),int) and not isinstance(v.get(k),bool) for k in ("raw_unknown_textual_source_count","resolved_by_k2_discovery_count","remaining_unknown_textual_source_count")):
        if v["raw_unknown_textual_source_count"]-v["resolved_by_k2_discovery_count"]!=v["remaining_unknown_textual_source_count"]:
            issues.append("raw - resolved must equal remaining")
    if v.get("claim_extraction_blocked") is not True:issues.append("Claim Extraction must remain blocked")
    gf=v.get("generated_from")
    if not isinstance(gf,list) or len(gf)<4 or len(gf)!=len(set(gf)) or any(not isinstance(x,str) or not x for x in gf):issues.append("generated_from must be unique non-empty input list")
    return issues


def main():
    if not REGISTRY.exists():fail(f"missing routing registry: {REGISTRY.relative_to(ROOT)}")
    sources=source_index(ROOT);rows=load_jsonl(REGISTRY);issues=validate_corrections(ROOT,sources,rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    if not OUT.exists():fail(f"missing generated backlog state: {OUT.relative_to(ROOT)}")
    try:stored=json.loads(OUT.read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid backlog JSON: {e}")
    issues=shape_issues(stored)
    if issues:fail("; ".join(issues[:20]))
    try:expected=render(build_state(ROOT))
    except ValueError as e:fail(str(e))
    if OUT.read_text(encoding="utf-8")!=expected:fail("backlog state is stale; run tools/generate_k2_unknown_textual_backlog.py --write")
    try:evidence=json.loads((ROOT/"knowledge"/"K2_EVIDENCE_STATE.json").read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid K2_EVIDENCE_STATE.json: {e}")
    if evidence.get("unknown_textual_resolution_backlog")!=stored.get("remaining_unknown_textual_source_count"):
        fail("K2_EVIDENCE_STATE unknown_textual_resolution_backlog does not match generated discovery backlog")
    if evidence.get("claim_extraction_blocked") is not True:fail("Evidence state must keep Claim Extraction blocked during discovery routing")
    print("k2-semantic-discovery-routing: PASS")
    print(f"raw_unknown={stored['raw_unknown_textual_source_count']} resolved={stored['resolved_by_k2_discovery_count']} remaining={stored['remaining_unknown_textual_source_count']} claim_extraction_blocked=true")


if __name__=="__main__":main()
