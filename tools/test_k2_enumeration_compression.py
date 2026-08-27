#!/usr/bin/env python3
from copy import deepcopy
from validate_k2_enumeration_compression import validate_rows,coverage_issues

SRC={"QM-SRC-0017":{"file_sha256":"a"*64}}
LIN={"QM-SRC-0017":{"work_id":"WORK-000224"}}
DEEP={"QM-SRC-0017":{"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_end":419}}
STATE={"schema_version":"k2-qcic-v06-machine-gates-v1","status":"ACTIVE","claim_extraction_blocked":True,"targets":[{"source_id":"QM-SRC-0017","source_stance":{"required":True,"minimum_rows":0},"enumeration_compression":{"required":True,"minimum_rows":1,"required_generative_rule_ids":["QM0017-TIME-ENUM"],"required_generator_entry_counts":{"QM0017-TIME-ENUM":1080},"required_generator_method_layers":{"QM0017-TIME-ENUM":"CALCULATION"}}}]}
BASE={
 "compression_id":"K2EC-QM0017-001","source_id":"QM-SRC-0017","work_id":"WORK-000224","canonical_sha256":"a"*64,
 "enumeration_label":"时家阴阳遁1080定局","method_layer":"CALCULATION","input_domain":"阳遁540+阴遁540",
 "generative_rule_id":"QM0017-TIME-ENUM","evidence_locators":["pdf:p151","pdf:p209"],"enumerated_entries_count":1080,
 "collapsed_structure_units":1,"empirical_evidence_units":0,"compression_policy":"DERIVED_ENUMERATION_COLLAPSE",
 "reconstruction_test_status":"UNTESTED","source_credit":"SOURCE_STRUCTURE_ONLY","empirical_credit":"NONE",
 "claim_extraction_blocked":True,"review_status":"REVIEWED"
}

def assert_bad(mut,msg):
    r=deepcopy(BASE);mut(r)
    assert validate_rows(SRC,LIN,DEEP,[r]),msg

def main():
    assert not validate_rows(SRC,LIN,DEEP,[deepcopy(BASE)])
    assert not coverage_issues([deepcopy(BASE)],deepcopy(STATE))
    assert coverage_issues([],deepcopy(STATE)),"required compression rows may not disappear"
    assert_bad(lambda r:r.__setitem__("collapsed_structure_units",1080),"enumeration inflated structure units")
    assert_bad(lambda r:r.__setitem__("empirical_evidence_units",1080),"enumeration inflated empirical evidence")
    assert_bad(lambda r:r.__setitem__("empirical_credit","VALIDATED"),"empirical credit escaped")
    assert_bad(lambda r:r.__setitem__("evidence_locators",["pdf:p500"]),"out-of-range locator accepted")
    assert_bad(lambda r:r.__setitem__("enumerated_entries_count",1),"single row accepted as enumeration")

    # One generator split across two labels would double-count one structural
    # mechanism if both rows were summed downstream. It must be one registry row.
    a=deepcopy(BASE);a["compression_id"]="A";a["enumeration_label"]="part-a"
    b=deepcopy(BASE);b["compression_id"]="B";b["enumeration_label"]="part-b";b["evidence_locators"]=["pdf:p210"]
    assert validate_rows(SRC,LIN,DEEP,[a,b]),"duplicate generative_rule_id accepted"

    # A minimum row count is not semantic generator coverage. Replacing an
    # accepted generator with an unrelated one must not keep the gate green.
    unrelated=deepcopy(BASE);unrelated["generative_rule_id"]="QM0017-UNRELATED-ENUM"
    assert coverage_issues([unrelated],deepcopy(STATE)),"count-only row substituted required generator"

    changed_count=deepcopy(BASE);changed_count["enumerated_entries_count"]=1079
    assert coverage_issues([changed_count],deepcopy(STATE)),"required generator structure size silently changed"
    changed_layer=deepcopy(BASE);changed_layer["method_layer"]="DIVINATION"
    assert coverage_issues([changed_layer],deepcopy(STATE)),"required generator method layer silently changed"

    malformed=deepcopy(STATE);malformed["targets"][0]["enumeration_compression"]["required_generative_rule_ids"]=["QM0017-TIME-ENUM","QM0017-TIME-ENUM"]
    assert coverage_issues([deepcopy(BASE)],malformed),"duplicate required generator ids accepted"
    malformed=deepcopy(STATE);malformed["targets"][0]["enumeration_compression"]["required_generator_entry_counts"]={}
    assert coverage_issues([deepcopy(BASE)],malformed),"generator/count semantic contract mismatch accepted"
    malformed=deepcopy(STATE);malformed["targets"][0]["enumeration_compression"]["required_generator_method_layers"]={}
    assert coverage_issues([deepcopy(BASE)],malformed),"generator/layer semantic contract mismatch accepted"

    print("k2-enumeration-compression-tests: PASS")
if __name__=="__main__":main()
