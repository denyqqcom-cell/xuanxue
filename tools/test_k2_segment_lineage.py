#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_segment_lineage as v


def sources():
    return {
        "QM-SRC-9000":{"source_id":"QM-SRC-9000","pages":8,"file_sha256":"a"*64},
        "QM-SRC-9001":{"source_id":"QM-SRC-9001","pages":6,"file_sha256":"b"*64},
        "QM-SRC-9002":{"source_id":"QM-SRC-9002","pages":5,"file_sha256":"c"*64},
        "QM-SRC-9003":{"source_id":"QM-SRC-9003","pages":7,"file_sha256":"d"*64},
    }


def segments():
    return {
        "QM-SRC-9001#SEG-001":{
            "segment_id":"QM-SRC-9001#SEG-001","source_id":"QM-SRC-9001",
            "page_start":1,"page_end":3,"domain_routes":["qimen"],"author":"甲"
        },
        "QM-SRC-9001#SEG-002":{
            "segment_id":"QM-SRC-9001#SEG-002","source_id":"QM-SRC-9001",
            "page_start":4,"page_end":6,"domain_routes":["OUT_OF_SCOPE"],"author":None
        },
        "QM-SRC-9002#SEG-001":{
            "segment_id":"QM-SRC-9002#SEG-001","source_id":"QM-SRC-9002",
            "page_start":1,"page_end":4,"domain_routes":["qimen"],"author":None
        },
        "QM-SRC-9002#SEG-002":{
            "segment_id":"QM-SRC-9002#SEG-002","source_id":"QM-SRC-9002",
            "page_start":5,"page_end":5,"domain_routes":["CARRIER_MATTER"],"author":None
        },
    }


def valid_rows():
    fam="WF-QM-TEST-001"
    return [
        {"author":"甲","author_basis":"CONTENT_VERIFIED","author_evidence":"内页署名","binding_id":fam+"#MEM-001","credit_scope":"SOURCE_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p8"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SOURCE","member_ref":"QM-SRC-9000","page_end":8,"page_start":1,"part_label":"上册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":None,"source_id":"QM-SRC-9000","work_family_key":fam,"work_title":"甲书"},
        {"author":"甲","author_basis":"CONTENT_VERIFIED","author_evidence":"segment 内页署名","binding_id":fam+"#MEM-002","credit_scope":"SEGMENT_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p3"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SEGMENT","member_ref":"QM-SRC-9001#SEG-001","page_end":3,"page_start":1,"part_label":"下册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":"QM-SRC-9001#SEG-001","source_id":"QM-SRC-9001","work_family_key":fam,"work_title":"甲书"},
    ]


def all_source_rows():
    fam="WF-QM-TEST-SOURCE-ONLY-001"
    return [
        {"author":"甲","author_basis":"CONTENT_VERIFIED","author_evidence":"上册内页署名","binding_id":fam+"#MEM-001","credit_scope":"SOURCE_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p8"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SOURCE","member_ref":"QM-SRC-9000","page_end":8,"page_start":1,"part_label":"上册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":None,"source_id":"QM-SRC-9000","work_family_key":fam,"work_title":"丙书"},
        {"author":"甲","author_basis":"CONTENT_VERIFIED","author_evidence":"下册内页署名","binding_id":fam+"#MEM-002","credit_scope":"SOURCE_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p7"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SOURCE","member_ref":"QM-SRC-9003","page_end":7,"page_start":1,"part_label":"下册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":None,"source_id":"QM-SRC-9003","work_family_key":fam,"work_title":"丙书"},
    ]


def unknown_rows():
    fam="WF-QM-TEST-UNKNOWN-001"
    return [
        {"author":None,"author_basis":"UNKNOWN","author_evidence":None,"binding_id":fam+"#MEM-001","credit_scope":"SOURCE_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p8"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SOURCE","member_ref":"QM-SRC-9000","page_end":8,"page_start":1,"part_label":"上册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":None,"source_id":"QM-SRC-9000","work_family_key":fam,"work_title":"乙书"},
        {"author":None,"author_basis":"UNKNOWN","author_evidence":None,"binding_id":fam+"#MEM-002","credit_scope":"SEGMENT_ONLY","domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p4"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","independent_vote_key":fam,"member_kind":"SEGMENT","member_ref":"QM-SRC-9002#SEG-001","page_end":4,"page_start":1,"part_label":"下册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":"QM-SRC-9002#SEG-001","source_id":"QM-SRC-9002","work_family_key":fam,"work_title":"乙书"},
    ]


def must_pass(rows):
    issues=v.validate_rows(sources(),segments(),rows)
    assert not issues,issues


def must_fail(rows,needle):
    issues=v.validate_rows(sources(),segments(),rows)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=valid_rows();must_pass(base)
    source_only=all_source_rows();must_pass(source_only)
    unknown=unknown_rows();must_pass(unknown)

    rows=copy.deepcopy(base);rows[1]["member_kind"]="SOURCE";rows[1]["member_ref"]="QM-SRC-9001";rows[1]["segment_id"]=None;rows[1]["credit_scope"]="SOURCE_ONLY";rows[1]["page_end"]=6
    must_fail(rows,"composite source cannot be bound carrier-wide")

    rows=copy.deepcopy(base);rows[1]["page_end"]=2
    must_fail(rows,"binding range must exactly match reviewed segment")

    rows=copy.deepcopy(base);rows[1]["part_label"]="上册"
    must_fail(rows,"duplicate part_label")

    rows=copy.deepcopy(base);rows[1]["independent_vote_key"]="WF-QM-OTHER"
    must_fail(rows,"independent_vote_key must equal work_family_key")

    rows=copy.deepcopy(base);rows[1]["author"]="乙"
    must_fail(rows,"binding author conflicts")

    rows=copy.deepcopy(base);rows[1]["evidence_locators"]=["pdf:p4"]
    must_fail(rows,"outside member range")

    rows=copy.deepcopy(base);rows[1]["credit_scope"]="SOURCE_ONLY"
    must_fail(rows,"SEGMENT member requires SEGMENT_ONLY")

    rows=[copy.deepcopy(base[0])]
    must_fail(rows,"requires at least two members")

    rows=copy.deepcopy(unknown);rows[0]["author_evidence"]="猜测"
    must_fail(rows,"unknown author must use author_basis=UNKNOWN with null evidence")

    rows=copy.deepcopy(unknown);rows[1]["author"]="乙";rows[1]["author_basis"]="TITLE_PAGE";rows[1]["author_evidence"]="题名页"
    must_fail(rows,"binding cannot invent an author absent from reviewed segment")

    rows=copy.deepcopy(unknown);rows[0]["author"]="甲";rows[0]["author_basis"]="TITLE_PAGE";rows[0]["author_evidence"]="题名页"
    must_fail(rows,"work family mixes known and unknown author attribution")

    print("k2-segment-lineage-tests: PASS")
    print("cases=14")

if __name__=="__main__":main()
