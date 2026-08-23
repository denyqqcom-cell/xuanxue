#!/usr/bin/env python3
from copy import deepcopy
from generate_k2_qcic_eligibility_view import build_view

STATE={"schema_version":"k2-qcic-v06-machine-gates-v1","status":"ACTIVE","claim_extraction_blocked":True,"targets":[{"source_id":"S1","source_stance":{"required":True,"minimum_rows":1},"enumeration_compression":{"required":True,"minimum_rows":1}}]}
BASE_STANCE={
 "stance_id":"A","source_id":"S1","work_id":"W1","canonical_sha256":"a"*64,"topic_key":"topic",
 "stance":"SOURCE_ENDORSES","evidence_locators":["pdf:p1"],"stance_basis":"VISUAL_PAGE","stance_precedence":10,
 "supersedes_stance_ids":[],"author_method_pool_eligible":True,"empirical_credit":"NONE","claim_extraction_blocked":True,"review_status":"REVIEWED"
}
BASE_ENUM={
 "compression_id":"E1","source_id":"S1","work_id":"W1","canonical_sha256":"a"*64,"enumeration_label":"100 states",
 "method_layer":"CALCULATION","input_domain":"x","generative_rule_id":"G1","evidence_locators":["pdf:p2"],
 "enumerated_entries_count":100,"collapsed_structure_units":1,"empirical_evidence_units":0,
 "compression_policy":"DERIVED_ENUMERATION_COLLAPSE","reconstruction_test_status":"UNTESTED","source_credit":"SOURCE_STRUCTURE_ONLY",
 "empirical_credit":"NONE","claim_extraction_blocked":True,"review_status":"REVIEWED"
}

def main():
    view=build_view(deepcopy(STATE),[deepcopy(BASE_STANCE)],[deepcopy(BASE_ENUM)])
    t=view["stance_topics"][0];e=view["enumeration_units"][0];s=view["source_summaries"][0]
    assert t["inference_eligibility"]=="ALLOW_SOURCE_LOCAL_CANDIDATE"
    assert t["claim_eligible"] is False
    assert e["effective_structure_units"]==1 and e["empirical_evidence_units"]==0
    assert e["inference_eligibility"]=="STRUCTURE_ONLY_RECONSTRUCTION_UNTESTED"
    assert s["author_method_candidate_count"]==1
    assert s["collapsed_enumerated_entries"]==100 and s["effective_structure_units"]==1 and s["empirical_evidence_units"]==0
    assert view["claim_extraction_blocked"] is True and view["empirical_credit"]=="NONE"

    rejected=deepcopy(BASE_STANCE);rejected["stance"]="SOURCE_REJECTS";rejected["author_method_pool_eligible"]=False
    view2=build_view(deepcopy(STATE),[rejected],[])
    assert view2["stance_topics"][0]["inference_eligibility"]=="EXCLUDE_SOURCE_REJECTED"
    assert view2["source_summaries"][0]["excluded_stance_topic_count"]==1

    old=deepcopy(BASE_STANCE);old["stance_id"]="OLD";old["stance"]="SOURCE_REPORTS";old["author_method_pool_eligible"]=False;old["stance_precedence"]=10
    new=deepcopy(BASE_STANCE);new["stance_id"]="NEW";new["supersedes_stance_ids"]=["OLD"];new["stance_precedence"]=20
    view3=build_view(deepcopy(STATE),[old,new],[])
    assert len(view3["stance_topics"])==1 and view3["stance_topics"][0]["effective_stance_id"]=="NEW"

    ambiguous=deepcopy(BASE_STANCE);ambiguous["stance_id"]="B";ambiguous["stance"]="SOURCE_UNCERTAIN";ambiguous["author_method_pool_eligible"]=False
    try:
        build_view(deepcopy(STATE),[deepcopy(BASE_STANCE),ambiguous],[])
        raise AssertionError("ambiguous effective stance was materialized")
    except ValueError:
        pass
    print("k2-qcic-eligibility-view-tests: PASS")
if __name__=="__main__":main()
