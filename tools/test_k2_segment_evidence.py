#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_segment_evidence as v


def segments():
    return {
        "QM-SRC-9000#SEG-001":{
            "segment_id":"QM-SRC-9000#SEG-001","source_id":"QM-SRC-9000",
            "page_start":1,"page_end":4,"domain_routes":["qimen"]
        }
    }


def bindings():
    return {
        ("WF-QM-TEST-001","QM-SRC-9000#SEG-001"):{
            "work_family_key":"WF-QM-TEST-001","segment_id":"QM-SRC-9000#SEG-001",
            "independent_vote_key":"WF-QM-TEST-001","domain_routes":["qimen"]
        }
    }


def row():
    return {"claim_readiness":"CONTEXT_REQUIRED","domain":"qimen","empirical_credit":"NONE","evidence_id":"K2SEG-QM9000-001","evidence_type":"EXPLICIT_RULE","extraction_basis":"VISUAL_PAGE","independent_vote_key":"WF-QM-TEST-001","locator":"pdf:p2","normalized_fact":"在特定组合关系下作判断。","review_status":"REVIEWED","segment_id":"QM-SRC-9000#SEG-001","source_credit":"SUPPORTED","source_id":"QM-SRC-9000","scope":"INTERPRETATION","verbatim_quote":None,"work_family_key":"WF-QM-TEST-001"}


def must_pass(rows):
    issues=v.validate_rows(segments(),bindings(),rows)
    assert not issues,issues


def must_fail(rows,needle):
    issues=v.validate_rows(segments(),bindings(),rows)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=row();must_pass([base])

    r=copy.deepcopy(base);r["locator"]="pdf:p5";must_fail([r],"outside reviewed segment")
    r=copy.deepcopy(base);r["work_family_key"]="WF-QM-OTHER";must_fail([r],"not bound")
    r=copy.deepcopy(base);r["independent_vote_key"]="WF-QM-OTHER";must_fail([r],"independent_vote_key mismatch")
    r=copy.deepcopy(base);r["domain"]="bazi";must_fail([r],"domain not supported")
    r=copy.deepcopy(base);r["empirical_credit"]="VALIDATED";must_fail([r],"cannot grant empirical credit")
    r=copy.deepcopy(base);r["verbatim_quote"]="原文";must_fail([r],"must not store verbatim quote")
    r=copy.deepcopy(base);r["evidence_type"]="CASE_RECORD";r["claim_readiness"]="READY";must_fail([r],"CASE_RECORD must remain NOT_CLAIM")
    r=copy.deepcopy(base);r["extraction_basis"]="TEXT_LAYER";must_fail([r],"requires VISUAL_PAGE")

    print("k2-segment-evidence-tests: PASS")
    print("cases=9")

if __name__=="__main__":main()
