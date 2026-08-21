#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_deep_reading as v


def sources():
    return {
        "QM-SRC-9000":{"source_id":"QM-SRC-9000","pages":4,"file_sha256":"a"*64},
        "QM-SRC-9001":{"source_id":"QM-SRC-9001","pages":5,"file_sha256":"b"*64},
    }


def segs():
    return {
        "QM-SRC-9001":[
            {"segment_id":"QM-SRC-9001#SEG-001","source_id":"QM-SRC-9001","page_start":1,"page_end":2},
            {"segment_id":"QM-SRC-9001#SEG-002","source_id":"QM-SRC-9001","page_start":3,"page_end":5},
        ]
    }


def rows():
    return [
        {"binding_mode":"SOURCE","canonical_sha256":"a"*64,"page_end":4,"page_start":1,"pages_reviewed_count":4,"read_status":"COMPLETE","reading_basis":"PROJECT_MAIN_AGENT_VISUAL_REVIEW","reading_id":"K2DEEP-QM-SRC-9000","review_status":"REVIEWED","segment_ids":[],"source_id":"QM-SRC-9000","verification_mode":"VISUAL_PAGE"},
        {"binding_mode":"SEGMENTED_CARRIER","canonical_sha256":"b"*64,"page_end":5,"page_start":1,"pages_reviewed_count":5,"read_status":"COMPLETE","reading_basis":"PROJECT_MAIN_AGENT_VISUAL_REVIEW","reading_id":"K2DEEP-QM-SRC-9001","review_status":"REVIEWED","segment_ids":["QM-SRC-9001#SEG-001","QM-SRC-9001#SEG-002"],"source_id":"QM-SRC-9001","verification_mode":"VISUAL_PAGE"},
    ]


def must_pass(rs):
    issues=v.validate_rows(sources(),segs(),rs)
    assert not issues,issues


def must_fail(rs,needle):
    issues=v.validate_rows(sources(),segs(),rs)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=rows();must_pass(base)

    rs=copy.deepcopy(base);rs[0]["page_end"]=3;must_fail(rs,"cover canonical")
    rs=copy.deepcopy(base);rs[0]["verification_mode"]="TEXT_LAYER_FULL";must_fail(rs,"requires VISUAL_PAGE")
    rs=copy.deepcopy(base);rs[1]["binding_mode"]="SOURCE";must_fail(rs,"requires SEGMENTED_CARRIER")
    rs=copy.deepcopy(base);rs[1]["segment_ids"]=["QM-SRC-9001#SEG-001"];must_fail(rs,"exactly match")
    rs=copy.deepcopy(base);rs[0]["segment_ids"]=["x"];must_fail(rs,"must not list segment_ids")
    rs=copy.deepcopy(base);rs[0]["canonical_sha256"]="c"*64;must_fail(rs,"canonical_sha256 mismatch")
    rs=copy.deepcopy(base);rs[0]["reading_basis"]="PACKET_READY";must_fail(rs,"unsupported reading_basis")
    rs=copy.deepcopy(base);rs.append(copy.deepcopy(base[0]));rs[-1]["reading_id"]="K2DEEP-QM-SRC-9999";must_fail(rs,"duplicate deep reading source")

    print("k2-deep-reading-tests: PASS")
    print("cases=9")

if __name__=="__main__":main()
