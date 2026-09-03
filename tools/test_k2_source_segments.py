#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_source_segments as v


def source():
    return {
        "QM-SRC-9000":{"source_id":"QM-SRC-9000","pages":6,"file_sha256":"a"*64},
        "QM-SRC-9001":{"source_id":"QM-SRC-9001","pages":2,"file_sha256":"b"*64},
    }


def valid_rows():
    return [
        {"author":"甲","author_basis":"CONTENT_VERIFIED","author_evidence":"内页署名","canonical_sha256":"a"*64,"domain_routes":["qimen"],"evidence_locators":["pdf:p1","pdf:p2"],"independence_class":"SAME_WORK_NOT_INDEPENDENT","paired_source_ids":["QM-SRC-9001"],"page_end":2,"page_start":1,"part_label":"下册","relation":"WORK_PART","review_status":"REVIEWED","segment_id":"QM-SRC-9000#SEG-001","source_credit_scope":"SEGMENT_ONLY","source_id":"QM-SRC-9000","title":"甲书下册","title_variants":[],"verification_mode":"VISUAL_PAGE"},
        {"author":None,"author_basis":"UNKNOWN","author_evidence":None,"canonical_sha256":"a"*64,"domain_routes":["OUT_OF_SCOPE"],"evidence_locators":["pdf:p3","pdf:p5"],"independence_class":"PRIMARY_CANDIDATE","paired_source_ids":[],"page_end":5,"page_start":3,"part_label":None,"relation":"PRIMARY_WORK_IN_COMPOSITE","review_status":"REVIEWED","segment_id":"QM-SRC-9000#SEG-002","source_credit_scope":"SEGMENT_ONLY","source_id":"QM-SRC-9000","title":"乙书","title_variants":[],"verification_mode":"VISUAL_PAGE"},
        {"author":None,"author_basis":"UNKNOWN","author_evidence":None,"canonical_sha256":"a"*64,"domain_routes":["CARRIER_MATTER"],"evidence_locators":["pdf:p6"],"independence_class":"NOT_ELIGIBLE","paired_source_ids":[],"page_end":6,"page_start":6,"part_label":None,"relation":"NON_WORK","review_status":"REVIEWED","segment_id":"QM-SRC-9000#SEG-003","source_credit_scope":"SEGMENT_ONLY","source_id":"QM-SRC-9000","title":"出版资料","title_variants":[],"verification_mode":"VISUAL_PAGE"},
    ]


def must_pass(rows):
    issues=v.validate_rows(source(),rows)
    assert not issues,issues


def must_fail(rows,needle):
    issues=v.validate_rows(source(),rows)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=valid_rows();must_pass(base)

    # A carrier-internal colophon/editorial attribution is real provenance
    # evidence, but it is weaker than external authorship verification and must
    # have its own basis instead of being laundered into CONTENT_VERIFIED.
    rows=copy.deepcopy(base)
    rows[1]["author"]="乙"
    rows[1]["author_basis"]="SOURCE_INTERNAL_ATTRIBUTION"
    rows[1]["author_evidence"]="载本内部编后语归属；未做外部作者学验证。"
    must_pass(rows)

    rows=copy.deepcopy(base);rows[1]["page_start"]=2
    must_fail(rows,"overlap")

    rows=copy.deepcopy(base);rows[1]["page_start"]=4
    must_fail(rows,"gap")

    rows=copy.deepcopy(base);rows[0]["paired_source_ids"]=[]
    must_fail(rows,"WORK_PART requires paired_source_ids")

    rows=copy.deepcopy(base);rows[1]["author"]="误继承作者";rows[1]["author_basis"]="UNKNOWN";rows[1]["author_evidence"]=None
    must_fail(rows,"known author requires verified author_basis")

    rows=copy.deepcopy(base);rows[2]["domain_routes"]=["qimen"]
    must_fail(rows,"NON_WORK must route only to CARRIER_MATTER")

    rows=copy.deepcopy(base);rows[1]["evidence_locators"]=["pdf:p6"]
    must_fail(rows,"outside segment")

    rows=copy.deepcopy(base);rows[0]["source_credit_scope"]="CARRIER_WIDE"
    must_fail(rows,"source_credit_scope must be SEGMENT_ONLY")

    print("k2-source-segments-tests: PASS")
    print("cases=9")

if __name__=="__main__":main()
