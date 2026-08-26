#!/usr/bin/env python3
from copy import deepcopy
import validate_k2_book_distillates as v


def baseline():
    ledger=[{
        "source_id":"S1","work_id":"W1","read_status":"COMPLETE","evidence_count":2
    }]
    evidence=[
        {"evidence_id":"E1","source_id":"S1","domain":"qimen"},
        {"evidence_id":"E2","source_id":"S1","domain":"qimen"},
    ]
    distillates=[{
        "distillate_id":"D1","source_id":"S1","work_id":"W1","domain":"qimen",
        "distillation_scope":"SOURCE_BOOK","source_read_status":"COMPLETE","evidence_count":2,
        "evidence_anchor_refs":["E1"],
        "essence":["core"],"method_map":["method"],"applicability_constraints":[],
        "source_limitations":["limit"],"conflicts_and_tensions":[],"anti_patterns":[],
        "model_updates":["update"],"testable_hypotheses":[],"excluded_from_operational_use":[],
        "distillation_status":"REVIEWED","review_status":"REVIEWED",
        "copyright_class":"DERIVED_SYNTHESIS_SAFE"
    }]
    return ledger,evidence,distillates


def has(issues,text):
    return any(text in msg for _,msg in issues)


def main():
    ledger,evidence,distillates=baseline()
    assert v.validate_rows(ledger,evidence,distillates)==[]

    assert has(v.validate_rows(ledger,evidence,[]),"missing mandatory book distillate")

    d=deepcopy(distillates);d.append(deepcopy(d[0]));d[1]["distillate_id"]="D2"
    assert has(v.validate_rows(ledger,evidence,d),"duplicate distillate source_id")

    l=deepcopy(ledger);l[0]["read_status"]="PARTIAL"
    assert has(v.validate_rows(l,evidence,distillates),"final distillate requires COMPLETE")

    d=deepcopy(distillates);d[0]["evidence_count"]=1
    issues=v.validate_rows(ledger,evidence,d)
    assert has(issues,"does not match ledger") and has(issues,"does not match actual Evidence")

    d=deepcopy(distillates);d[0]["evidence_anchor_refs"]=["OTHER"]
    assert has(v.validate_rows(ledger,evidence,d),"anchor does not belong")

    d=deepcopy(distillates);d[0]["essence"]=[]
    assert has(v.validate_rows(ledger,evidence,d),"essence must not be empty")

    d=deepcopy(distillates);d[0]["model_updates"]=[]
    assert has(v.validate_rows(ledger,evidence,d),"model_updates must not be empty")

    d=deepcopy(distillates);d[0]["source_limitations"]=["see /home/user/private/book.pdf"]
    assert has(v.validate_rows(ledger,evidence,d),"local filesystem path")

    d=deepcopy(distillates);d[0]["distillation_status"]="DRAFT"
    assert has(v.validate_rows(ledger,evidence,d),"distillate must be REVIEWED")

    d=deepcopy(distillates);d[0]["extra_field"]="x"
    assert has(v.validate_rows(ledger,evidence,d),"unexpected distillate fields")

    print("k2-book-distillate-tests: PASS")


if __name__=="__main__":main()
