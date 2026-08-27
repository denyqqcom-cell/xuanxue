#!/usr/bin/env python3
from copy import deepcopy
from validate_k2_source_stance import validate_rows,coverage_issues,effective_stance_rows

SRC={"QM-SRC-0017":{"file_sha256":"a"*64}}
LIN={"QM-SRC-0017":{"work_id":"WORK-000224"}}
DEEP={"QM-SRC-0017":{"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_end":419}}
STATE={"schema_version":"k2-qcic-v06-machine-gates-v1","status":"ACTIVE","claim_extraction_blocked":True,"targets":[{"source_id":"QM-SRC-0017","source_stance":{"required":True,"minimum_rows":1},"enumeration_compression":{"required":True,"minimum_rows":0}}]}
BASE={
 "stance_id":"K2SS-QM0017-001","source_id":"QM-SRC-0017","work_id":"WORK-000224","canonical_sha256":"a"*64,
 "topic_key":"chance-omen","stance":"SOURCE_REJECTS","evidence_locators":["pdf:p416"],"stance_basis":"VISUAL_PAGE",
 "stance_precedence":100,"supersedes_stance_ids":[],"author_method_pool_eligible":False,"empirical_credit":"NONE",
 "claim_extraction_blocked":True,"review_status":"REVIEWED"
}

def assert_bad(mut,msg):
    r=deepcopy(BASE);mut(r)
    assert validate_rows(SRC,LIN,DEEP,[r]),msg

def main():
    assert not validate_rows(SRC,LIN,DEEP,[deepcopy(BASE)])
    assert not coverage_issues([deepcopy(BASE)],deepcopy(STATE))
    assert coverage_issues([],deepcopy(STATE)),"required registry rows may not disappear"
    assert_bad(lambda r:r.__setitem__("author_method_pool_eligible",True),"rejected stance entered method pool")
    assert_bad(lambda r:r.__setitem__("empirical_credit","VALIDATED"),"empirical credit escaped")
    assert_bad(lambda r:r.__setitem__("evidence_locators",["pdf:p999"]),"out-of-range locator accepted")
    def reports_eligible(r):
        r["stance"]="SOURCE_REPORTS";r["author_method_pool_eligible"]=True
    assert_bad(reports_eligible,"reported-only stance entered method pool")

    old=deepcopy(BASE);old["stance_id"]="OLD";old["stance"]="SOURCE_REPORTS";old["stance_precedence"]=10
    new=deepcopy(BASE);new["stance_id"]="NEW";new["supersedes_stance_ids"]=["OLD"];new["stance_precedence"]=20
    assert not validate_rows(SRC,LIN,DEEP,[old,new])
    assert [r["stance_id"] for r in effective_stance_rows([old,new])]==["NEW"]
    new["stance_precedence"]=5
    assert validate_rows(SRC,LIN,DEEP,[old,new]),"lower-precedence supersession accepted"

    # Two unsuperseded rows for one topic create an ambiguous downstream stance
    # even when every row is individually well-formed. This must fail closed.
    a=deepcopy(BASE);a["stance_id"]="A";a["stance"]="SOURCE_REPORTS";a["stance_precedence"]=10
    b=deepcopy(BASE);b["stance_id"]="B";b["stance"]="SOURCE_REJECTS";b["stance_precedence"]=20
    assert validate_rows(SRC,LIN,DEEP,[a,b]),"ambiguous effective stance leaves accepted"
    try:
        effective_stance_rows([a,b])
        raise AssertionError("ambiguous effective stance materialized")
    except ValueError:
        pass

    # A count threshold is not semantic coverage. Once a reviewed source has
    # mandatory stance topics, unrelated replacement rows must not satisfy the
    # gate merely because the row count is unchanged.
    semantic_state=deepcopy(STATE)
    semantic_state["targets"][0]["source_stance"]["required_topic_keys"]=["chance-omen"]
    unrelated=deepcopy(BASE);unrelated["topic_key"]="unrelated-topic"
    assert coverage_issues([unrelated],semantic_state),"count-only rows substituted a required stance topic"
    assert not coverage_issues([deepcopy(BASE)],semantic_state),"required stance topic was not recognized"

    print("k2-source-stance-tests: PASS")
if __name__=="__main__":main()
