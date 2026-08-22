#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_evidence_reaudit as v

def ev(readiness="READY",eid="E1",sid="QM-SRC-1"):
    return {"evidence_id":eid,"source_id":sid,"claim_readiness":readiness}

def row(**o):
    r={
      "audit_id":"A1","evidence_id":"E1","source_id":"QM-SRC-1","disposition":"KEEP",
      "effective_claim_readiness":"READY","independence_policy":"COURSE_FAMILY_SINGLE_VOTE",
      "risk_domain":"NONE","rationale":"full-source re-audit preserves source-local record","review_status":"REVIEWED"
    }
    r.update(o);return r

def main():
    course={"independent_vote_allowed":False}
    assert not v.inspect(row(),ev(),course)
    issues=v.inspect(row(effective_claim_readiness="READY",risk_domain="MEDICAL"),ev(),course)
    assert any("high-risk" in msg for _,msg in issues),issues
    issues=v.inspect(row(independence_policy="DEFAULT"),ev(),course)
    assert any("COURSE_FAMILY_SINGLE_VOTE" in msg for _,msg in issues),issues
    issues=v.inspect(row(disposition="KEEP",effective_claim_readiness="NOT_CLAIM"),ev(),course)
    assert any("KEEP" in msg for _,msg in issues),issues
    good=row(disposition="DOWNGRADE_NOT_CLAIM",effective_claim_readiness="NOT_CLAIM",risk_domain="MEDICAL")
    assert not v.inspect(good,ev("CONTEXT_REQUIRED"),course),v.inspect(good,ev("CONTEXT_REQUIRED"),course)
    issues=v.inspect(row(disposition="KEEP",effective_claim_readiness="READY"),ev("NOT_CLAIM"),course)
    assert any("transition" in msg or "KEEP" in msg for _,msg in issues),issues

    evidence={"E1":ev(),"E2":ev("CONTEXT_REQUIRED","E2")}
    audits=[row()]
    state={"targets":[{"source_id":"QM-SRC-1","coverage":"COMPLETE","expected_evidence_count":2}]}
    issues=v.validate_coverage(evidence,audits,state)
    assert any("missing 1" in msg for _,msg in issues),issues
    print("k2-evidence-reaudit-tests: PASS")

if __name__=="__main__":main()
