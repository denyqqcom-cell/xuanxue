#!/usr/bin/env python3
from copy import deepcopy
import json
from pathlib import Path
import tempfile

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


def write_jsonl(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(
        "".join(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n" for row in rows),
        encoding="utf-8",
    )


def assert_standalone_main_aggregates_shards():
    """A shard-resident contract break must fail the standalone validator too."""
    with tempfile.TemporaryDirectory(prefix="k2-book-distillate-shard-test-") as tmp:
        root=Path(tmp)
        k=root/"knowledge"
        k.mkdir(parents=True)
        (k/"PROJECT_STATE.json").write_text(
            json.dumps({"phase":"K2_EVIDENCE_EXTRACTION","claim_extraction_blocked":True}),
            encoding="utf-8",
        )

        ledger,evidence,distillates=baseline()
        ledger[0]["reading_id"]="R1"
        write_jsonl(k/v.agg.BASE_LEDGER,ledger)
        write_jsonl(k/v.agg.BASE_EVIDENCE,evidence)
        write_jsonl(k/v.agg.BASE_DISTILLATES,distillates)

        shard_ledger=[{
            "reading_id":"R2","source_id":"S2","work_id":"W2",
            "read_status":"COMPLETE","evidence_count":1,
        }]
        shard_evidence=[{"evidence_id":"E3","source_id":"S2","domain":"qimen"}]
        shard_distillate=deepcopy(distillates[0])
        shard_distillate.update({
            "distillate_id":"D2","source_id":"S2","work_id":"WRONG",
            "evidence_count":1,"evidence_anchor_refs":["E3"],
        })
        write_jsonl(k/v.agg.SHARD_DIRS["ledger"]/"S2.jsonl",shard_ledger)
        write_jsonl(k/v.agg.SHARD_DIRS["evidence"]/"S2.jsonl",shard_evidence)
        write_jsonl(k/v.agg.SHARD_DIRS["distillate"]/"S2.jsonl",[shard_distillate])

        previous_root=v.ROOT
        try:
            v.ROOT=root
            try:
                v.main()
            except SystemExit as exc:
                assert exc.code==1
            else:
                raise AssertionError("standalone validator ignored invalid shard distillate")
        finally:
            v.ROOT=previous_root


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

    assert_standalone_main_aggregates_shards()

    print("k2-book-distillate-tests: PASS")


if __name__=="__main__":main()