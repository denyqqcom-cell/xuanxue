#!/usr/bin/env python3
from copy import deepcopy
from validate_k2_enumeration_compression import validate_rows

SRC={"QM-SRC-0017":{"file_sha256":"a"*64}}
LIN={"QM-SRC-0017":{"work_id":"WORK-000224"}}
DEEP={"QM-SRC-0017":{"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_end":419}}
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
    assert_bad(lambda r:r.__setitem__("collapsed_structure_units",1080),"enumeration inflated structure units")
    assert_bad(lambda r:r.__setitem__("empirical_evidence_units",1080),"enumeration inflated empirical evidence")
    assert_bad(lambda r:r.__setitem__("empirical_credit","VALIDATED"),"empirical credit escaped")
    assert_bad(lambda r:r.__setitem__("evidence_locators",["pdf:p500"]),"out-of-range locator accepted")
    assert_bad(lambda r:r.__setitem__("enumerated_entries_count",1),"single row accepted as enumeration")
    print("k2-enumeration-compression-tests: PASS")
if __name__=="__main__":main()
