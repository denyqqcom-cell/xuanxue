#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_composite_source_closures as v

SID="ZW-SRC-0004"
S1=SID+"#SEG-001";S2=SID+"#SEG-002";S3=SID+"#SEG-003"
F1="WF-ZW-DOUSHU-XUANWEI-001";F2="WF-ZW-DOUSHU-SIHUA-DUANJUE-001"
RID="K2DEEP-ZW-SRC-0004"


def fixtures():
    sources={SID:{"source_id":SID,"pages":404,"file_sha256":"a"*64}}
    segments={
      S1:{"segment_id":S1,"source_id":SID,"page_start":1,"page_end":6,"relation":"NON_WORK","domain_routes":["CARRIER_MATTER"]},
      S2:{"segment_id":S2,"source_id":SID,"page_start":7,"page_end":205,"relation":"PRIMARY_WORK_IN_COMPOSITE","domain_routes":["ziwei","fengshui"]},
      S3:{"segment_id":S3,"source_id":SID,"page_start":206,"page_end":404,"relation":"PRIMARY_WORK_IN_COMPOSITE","domain_routes":["ziwei"]},
    }
    deep=[{"binding_mode":"SEGMENTED_CARRIER","canonical_sha256":"a"*64,"page_end":404,"page_start":1,
           "pages_reviewed_count":404,"read_status":"COMPLETE","reading_basis":"PROJECT_MAIN_AGENT_VISUAL_REVIEW",
           "reading_id":RID,"review_status":"REVIEWED","segment_ids":[S1,S2,S3],"source_id":SID,
           "verification_mode":"VISUAL_PAGE"}]
    lineage=[
      {"work_family_key":F1,"member_kind":"SEGMENT","segment_id":S2,"source_id":SID,
       "credit_scope":"SEGMENT_ONLY","relation":"PRIMARY_WORK_IN_COMPOSITE","member_ref":S2,"domain_routes":["ziwei","fengshui"]},
      {"work_family_key":F2,"member_kind":"SEGMENT","segment_id":S3,"source_id":SID,
       "credit_scope":"SEGMENT_ONLY","relation":"PRIMARY_WORK_IN_COMPOSITE","member_ref":S3,"domain_routes":["ziwei"]},
    ]
    ev=[
      {"evidence_id":"E1","segment_id":S2,"source_id":SID,"work_family_key":F1,"domain":"fengshui"},
      {"evidence_id":"E2","segment_id":S2,"source_id":SID,"work_family_key":F1,"domain":"ziwei"},
      {"evidence_id":"E3","segment_id":S2,"source_id":SID,"work_family_key":F1,"domain":"ziwei"},
      {"evidence_id":"E4","segment_id":S3,"source_id":SID,"work_family_key":F2,"domain":"ziwei"},
    ]
    dist=[
      {"work_family_key":F1,"domain":"ziwei","domain_routes":["ziwei","fengshui"],"distillation_status":"REVIEWED","review_status":"REVIEWED","empirical_credit":"NONE",
       "claim_extraction_blocked":True,"reading_refs":[RID],"segment_evidence_refs":["E1","E2","E3"]},
      {"work_family_key":F2,"domain":"ziwei","domain_routes":["ziwei"],"distillation_status":"REVIEWED","review_status":"REVIEWED","empirical_credit":"NONE",
       "claim_extraction_blocked":True,"reading_refs":[RID],"segment_evidence_refs":["E4"]},
    ]
    closure={
      "carrier_independent_vote_credit":"NONE","canonical_sha256":"a"*64,"claim_extraction_blocked":True,
      "closure_id":"K2CC-ZW-SRC-0004","closure_status":"C2_COMPOSITE_NORMALIZED",
      "completion_scope":"COMPOSITE_CARRIER_EXECUTION","deep_reading_id":RID,"empirical_credit":"NONE",
      "legacy_wave1_credit":"NONE","non_work_segment_ids":[S1],"queue_resolution":"RESOLVED",
      "review_status":"REVIEWED","segment_ids":[S1,S2,S3],
      "source_credit":"FULL_CARRIER_VISUAL_REVIEWED_AND_EMBEDDED_WORKS_DISTILLED",
      "source_id":SID,"work_family_keys":[F1,F2],"work_segment_ids":[S2,S3]
    }
    return sources,segments,deep,lineage,ev,dist,[],[],[],closure


def issues(f=None):
    data=list(fixtures())
    c=data.pop()
    if f:f(data,c)
    return v.validate_rows(*data,[c])


def must_fail(mutator,needle):
    xs=issues(mutator)
    assert xs,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in xs)
    assert needle in text,(needle,text)


def main():
    assert not issues(),issues()

    must_fail(lambda d,c:d[2].__setitem__(0,dict(d[2][0],page_end=403)),"does not cover full canonical")
    must_fail(lambda d,c:d[2].__setitem__(0,dict(d[2][0],segment_ids=[S1,S2])),"deep reading segment_ids mismatch")
    must_fail(lambda d,c:d[3].pop(),"exactly one segment-work binding")
    must_fail(lambda d,c:d[4].__setitem__(slice(None),[e for e in d[4] if e["segment_id"]!=S3]),"no normalized Segment Evidence")
    must_fail(lambda d,c:d[4].append({"evidence_id":"ENW","segment_id":S1,"source_id":SID,"work_family_key":"X","domain":"ziwei"}),"NON_WORK segment")
    must_fail(lambda d,c:d[5].pop(),"exactly one reviewed distillate")
    must_fail(lambda d,c:d[6].append({"source_id":SID,"read_status":"COMPLETE"}),"double-resolve")
    must_fail(lambda d,c:c.__setitem__("empirical_credit","VALIDATED"),"cannot grant empirical credit")
    must_fail(lambda d,c:c.__setitem__("work_family_keys",[F2,F1]),"work_family_keys must exactly follow")
    def missing_route(d,c):
        d[4][:]=[e for e in d[4] if not (e["segment_id"]==S2 and e["domain"]=="fengshui")]
    must_fail(missing_route,"does not cover all governed routes")
    def bad_refs(d,c):
        d[5][0]=dict(d[5][0],segment_evidence_refs=["E2","E3"])
    must_fail(bad_refs,"evidence refs not exact")
    def bad_distillate_routes(d,c):
        d[5][0]=dict(d[5][0],domain_routes=["ziwei"])
    must_fail(bad_distillate_routes,"distillate routes do not cover work-family routes")
    def bad_primary_domain(d,c):
        d[5][0]=dict(d[5][0],domain="fengshui")
    must_fail(bad_primary_domain,"distillate primary domain does not match first governed route")

    print("k2-composite-source-closure-tests: PASS")
    print("cases=14")


if __name__=="__main__":main()
