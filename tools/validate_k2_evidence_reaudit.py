#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
ALLOWED={
  "audit_id","evidence_id","source_id","disposition","effective_claim_readiness",
  "independence_policy","risk_domain","rationale","review_status"
}
READINESS={"READY","CONTEXT_REQUIRED","CONFLICT_CANDIDATE","NOT_CLAIM"}
TRANSITIONS={
  "READY":{"READY","CONTEXT_REQUIRED","NOT_CLAIM"},
  "CONTEXT_REQUIRED":{"CONTEXT_REQUIRED","NOT_CLAIM"},
  "CONFLICT_CANDIDATE":{"CONFLICT_CANDIDATE","NOT_CLAIM"},
  "NOT_CLAIM":{"NOT_CLAIM"},
}

def fail(msg):
    print(f"k2-evidence-reaudit: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

def load_json(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:fail(f"cannot parse {path}: {e}")

def load_jsonl(path):
    rows=[]
    if not path.exists():return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows

def aggregate_evidence(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_EVIDENCE_WAVE1.jsonl")
    shard=root/"knowledge"/"K2_EVIDENCE_WAVE1.d"
    if shard.exists():
        for p in sorted(shard.glob("*.jsonl")):rows.extend(load_jsonl(p))
    out={}
    for r in rows:
        eid=r.get("evidence_id")
        if eid in out:fail(f"duplicate aggregate evidence_id {eid}")
        out[eid]=r
    return out

def course_by_source(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_COURSE_LINEAGE.jsonl")}

def inspect(row,evidence,course=None):
    aid=row.get("audit_id") or "<missing>";issues=[]
    extra=set(row)-ALLOWED
    if extra:issues.append(f"unexpected fields: {sorted(extra)}")
    if row.get("source_id")!=evidence.get("source_id"):issues.append("source_id mismatch")
    base=evidence.get("claim_readiness");eff=row.get("effective_claim_readiness")
    if base not in READINESS or eff not in READINESS:issues.append("invalid readiness")
    elif eff not in TRANSITIONS[base]:issues.append(f"readiness promotion/invalid transition {base}->{eff}")
    disp=row.get("disposition")
    if disp=="KEEP" and eff!=base:issues.append("KEEP must preserve base readiness")
    elif disp=="HOLD_CONFLICT" and not (base=="CONFLICT_CANDIDATE" and eff=="CONFLICT_CANDIDATE"):
        issues.append("HOLD_CONFLICT requires unchanged CONFLICT_CANDIDATE")
    elif disp=="DOWNGRADE_NOT_CLAIM" and not (base!="NOT_CLAIM" and eff=="NOT_CLAIM"):
        issues.append("DOWNGRADE_NOT_CLAIM must lower a non-NOT_CLAIM record to NOT_CLAIM")
    elif disp=="REJECT" and not (eff=="NOT_CLAIM" and row.get("independence_policy")=="EXCLUDED"):
        issues.append("REJECT requires NOT_CLAIM and EXCLUDED")
    elif disp not in {"KEEP","HOLD_CONFLICT","DOWNGRADE_NOT_CLAIM","REJECT"}:
        issues.append("invalid disposition")
    risk=row.get("risk_domain")
    if risk not in {"NONE","FINANCIAL","MEDICAL","LEGAL_CRIMINAL"}:issues.append("invalid risk_domain")
    elif risk!="NONE" and eff!="NOT_CLAIM":issues.append("high-risk reaudit must be NOT_CLAIM")
    policy=row.get("independence_policy")
    if policy not in {"DEFAULT","COURSE_FAMILY_SINGLE_VOTE","EXCLUDED"}:issues.append("invalid independence_policy")
    if course and course.get("independent_vote_allowed") is False and policy!="COURSE_FAMILY_SINGLE_VOTE" and disp!="REJECT":
        issues.append("course-family member must use COURSE_FAMILY_SINGLE_VOTE")
    if row.get("review_status")!="REVIEWED":issues.append("review_status must be REVIEWED")
    if not isinstance(row.get("rationale"),str) or not row.get("rationale").strip():issues.append("rationale required")
    return [(aid,x) for x in issues]

def validate_coverage(evidence,audits,state):
    issues=[]
    audit_by_eid={r.get("evidence_id"):r for r in audits}
    for target in state.get("targets") or []:
        sid=target.get("source_id")
        source_eids={eid for eid,e in evidence.items() if e.get("source_id")==sid}
        audited={eid for eid,r in audit_by_eid.items() if r.get("source_id")==sid}
        expected=target.get("expected_evidence_count")
        if expected!=len(source_eids):issues.append((sid,f"expected_evidence_count {expected} != aggregate evidence {len(source_eids)}"))
        if target.get("coverage")=="COMPLETE":
            missing=source_eids-audited;extra=audited-source_eids
            if missing:issues.append((sid,f"COMPLETE reaudit missing {len(missing)} evidence rows"))
            if extra:issues.append((sid,f"reaudit includes {len(extra)} non-source evidence rows"))
    return issues

def main():
    project=load_json(K/"PROJECT_STATE.json")
    state=load_json(K/"K2_EVIDENCE_REAUDIT_STATE.json")
    if project.get("claim_extraction_blocked") is not True or state.get("claim_extraction_blocked") is not True:
        fail("claim extraction must remain blocked")
    evidence=aggregate_evidence()
    courses=course_by_source()
    rows=load_jsonl(K/"K2_EVIDENCE_REAUDIT.jsonl")
    seen_aid=set();seen_eid=set();issues=[]
    for r in rows:
        aid=r.get("audit_id");eid=r.get("evidence_id")
        if aid in seen_aid:issues.append((aid or "<missing>","duplicate audit_id"))
        if eid in seen_eid:issues.append((eid or "<missing>","duplicate evidence reaudit"))
        seen_aid.add(aid);seen_eid.add(eid)
        e=evidence.get(eid)
        if not e:issues.append((eid or "<missing>","unknown evidence_id"));continue
        issues.extend(inspect(r,e,courses.get(r.get("source_id"))))
    issues.extend(validate_coverage(evidence,rows,state))
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-evidence-reaudit: PASS")
    print(f"audits={len(rows)} complete_targets={sum(1 for t in state.get('targets',[]) if t.get('coverage')=='COMPLETE')} issues=0")

if __name__=="__main__":main()
