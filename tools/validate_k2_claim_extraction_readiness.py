#!/usr/bin/env python3
import json,sys
from generate_k2_claim_extraction_readiness import ROOT,OUT,SCHEMA_VERSION,actual_readiness,render

TOP_KEYS={"schema_version","status","claim_extraction_authorized","transition_policy","generated_from","checks","blockers","observed_state","empirical_credit_path_separate"}
CHECK_KEYS={"evidence_state_complete","unknown_textual_backlog_cleared","unknown_textual_backlog_materialization_current","unknown_textual_backlog_accounting_current","evidence_state_unblocks_claim_extraction","project_k2_not_blocked","project_evidence_extraction_open","required_domains_consistent","qcic_materialization_current"}
OBS_KEYS={"project_phase","project_next_phase","evidence_status","evidence_state_unknown_textual_resolution_backlog","raw_unknown_textual_source_count","resolved_by_k2_discovery_count","unknown_textual_resolution_backlog","qcic_stance_topic_count","qcic_enumeration_unit_count","qcic_claim_eligible_unit_count"}
STATUSES={"CLOSED","READY_FOR_PROJECT_REVIEW"}


def fail(msg):
    print(f"k2-claim-extraction-readiness: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)


def shape_issues(v):
    issues=[]
    if not isinstance(v,dict):return ["readiness must be object"]
    if set(v)!=TOP_KEYS:issues.append(f"top-level keys mismatch: {sorted(set(v)^TOP_KEYS)}")
    if v.get("schema_version")!=SCHEMA_VERSION:issues.append("schema_version mismatch")
    if v.get("status") not in STATUSES:issues.append("invalid status")
    if v.get("claim_extraction_authorized") is not False:issues.append("v1 gate must never authorize Claim Extraction")
    if v.get("transition_policy")!="PROJECT_REVIEW_REQUIRED_V1_NEVER_AUTO_OPENS":issues.append("invalid transition_policy")
    if v.get("empirical_credit_path_separate") is not True:issues.append("empirical credit path must remain separate")
    checks=v.get("checks")
    if not isinstance(checks,dict) or set(checks)!=CHECK_KEYS or any(not isinstance(x,bool) for x in checks.values()):issues.append("checks must be exact boolean contract")
    blockers=v.get("blockers")
    if not isinstance(blockers,list) or len(blockers)!=len(set(blockers)) or any(not isinstance(x,str) or not x for x in blockers):issues.append("blockers must be unique non-empty strings")
    obs=v.get("observed_state")
    if not isinstance(obs,dict) or set(obs)!=OBS_KEYS:issues.append("observed_state keys mismatch")
    if isinstance(obs,dict):
        for k in ("evidence_state_unknown_textual_resolution_backlog","raw_unknown_textual_source_count","resolved_by_k2_discovery_count","unknown_textual_resolution_backlog","qcic_stance_topic_count","qcic_enumeration_unit_count","qcic_claim_eligible_unit_count"):
            x=obs.get(k)
            if not isinstance(x,int) or isinstance(x,bool) or x<0:issues.append(f"{k} must be non-negative integer")
        raw=obs.get("raw_unknown_textual_source_count");resolved=obs.get("resolved_by_k2_discovery_count");remaining=obs.get("unknown_textual_resolution_backlog")
        if all(isinstance(x,int) and not isinstance(x,bool) for x in (raw,resolved,remaining)) and raw-resolved!=remaining:
            issues.append("raw unknown - resolved discovery must equal remaining backlog")
    if isinstance(checks,dict) and set(checks)==CHECK_KEYS:
        expected_status="READY_FOR_PROJECT_REVIEW" if all(checks.values()) else "CLOSED"
        if v.get("status")!=expected_status:issues.append("status does not match automated prerequisite checks")
        if expected_status=="READY_FOR_PROJECT_REVIEW" and blockers:issues.append("ready state cannot have blockers")
        if expected_status=="CLOSED" and not blockers:issues.append("closed state requires blockers")
    gf=v.get("generated_from")
    if not isinstance(gf,list) or len(gf)<4 or len(gf)!=len(set(gf)) or any(not isinstance(x,str) or not x for x in gf):issues.append("generated_from must be unique non-empty list")
    return issues


def main():
    if not OUT.exists():fail(f"missing generated readiness: {OUT.relative_to(ROOT)}")
    try:stored=json.loads(OUT.read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid readiness JSON: {e}")
    issues=shape_issues(stored)
    if issues:fail("; ".join(issues[:20]))
    expected=render(actual_readiness(ROOT));actual=OUT.read_text(encoding="utf-8")
    if actual!=expected:fail("readiness snapshot is stale; run tools/generate_k2_claim_extraction_readiness.py --write")
    print("k2-claim-extraction-readiness: PASS")
    print(f"status={stored['status']} authorized=false blockers={len(stored['blockers'])} backlog={stored['observed_state']['unknown_textual_resolution_backlog']}")


if __name__=="__main__":main()
