#!/usr/bin/env python3
import copy,json,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_mixed_voice_holds as v


def sources():
    return {"QM-SRC-9000":{"source_id":"QM-SRC-9000","pages":50}}


def hold():
    return {"source_id":"QM-SRC-9000","status":"PARTIAL_READING_CONFIRMED","reviewed_page_start":1,"reviewed_page_end":25,"verification_mode":"VISUAL_PAGE","hold_policy":"BLOCK_FORMAL_EVIDENCE_UNTIL_VOICE_SCHEMA","reason":"mixed voice observed","allowed_voice_layers":sorted(v.LAYERS),"review_status":"REVIEWED"}


def qualified_hold():
    h=hold();h["hold_policy"]="VOICE_QUALIFIED_EVIDENCE_ONLY";return h


def qualified_evidence():
    return {
        "source_id":"QM-SRC-9000",
        "evidence_id":"E-Q-1",
        "claim_readiness":"CONTEXT_REQUIRED",
        "review_status":"REVIEWED",
        "voice_qualification":{
            "voice_layer":"BASE_TEXT",
            "attribution_subject":"TEST-AUTHOR",
            "attribution_basis":"EXPLICIT_AUTHORIAL_CONTEXT",
            "source_stance":"ASSERTS",
            "method_layer":"DIVINATION_INTERPRETATION",
            "operational_scope":"GENERAL_DIVINATION_CANDIDATE",
            "independence_credit_scope":"SOURCE_LOCAL_ONLY",
        },
    }


def must_pass(holds,evidence):
    issues=v.validate_rows(sources(),holds,evidence)
    assert not issues,issues


def must_fail(holds,evidence,needle):
    issues=v.validate_rows(sources(),holds,evidence)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def write_jsonl(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows),encoding="utf-8")


def main():
    base=hold();must_pass([base],[])

    complete=copy.deepcopy(base);complete["status"]="COMPLETE_READING_CONFIRMED";complete["reviewed_page_end"]=50
    must_pass([complete],[])

    bad=copy.deepcopy(base);bad["reviewed_page_end"]=0
    must_fail([bad],[],"invalid reviewed page range")

    bad=copy.deepcopy(base);bad["hold_policy"]="ALLOW"
    must_fail([bad],[],"invalid hold_policy")

    bad=copy.deepcopy(base);bad["allowed_voice_layers"]=["BASE_TEXT"]
    must_fail([bad],[],"allowed_voice_layers")

    must_fail([base,copy.deepcopy(base)],[],"duplicate hold row")
    must_fail([base],[{"source_id":"QM-SRC-9000","evidence_id":"E-1"}],"formal evidence E-1 is forbidden")

    unknown=copy.deepcopy(base);unknown["source_id"]="QM-SRC-9999"
    must_fail([unknown],[],"unknown source_id")

    incomplete=copy.deepcopy(base);incomplete["status"]="COMPLETE_READING_CONFIRMED"
    must_fail([incomplete],[],"must cover canonical p1-pN")

    bad=copy.deepcopy(base);bad["status"]="COMPLETE"
    must_fail([bad],[],"invalid hold status")

    # New contract: a mixed-voice source may leave the absolute block only when
    # every formal Evidence row carries explicit voice/method qualification.
    qh=qualified_hold();qe=qualified_evidence();must_pass([qh],[qe])

    must_fail([qh],[{"source_id":"QM-SRC-9000","evidence_id":"E-Q-2","claim_readiness":"NOT_CLAIM","review_status":"REVIEWED"}],"voice_qualification required")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["voice_layer"]="UNKNOWN_VOICE"
    must_fail([qh],[bad],"resolved voice_layer required")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["attribution_subject"]=""
    must_fail([qh],[bad],"attribution_subject required")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["attribution_basis"]="UNKNOWN"
    must_fail([qh],[bad],"resolved attribution_basis required")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["method_layer"]="RITUAL_ESOTERIC"
    bad["voice_qualification"]["operational_scope"]="GENERAL_DIVINATION_CANDIDATE"
    must_fail([qh],[bad],"ritual/esoteric evidence cannot enter general divination pool")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["method_layer"]="MILITARY_OPERATIONAL"
    bad["voice_qualification"]["operational_scope"]="EXCLUDED_MILITARY_OPERATIONAL"
    bad["claim_readiness"]="READY"
    must_fail([qh],[bad],"ritual/military evidence must be NOT_CLAIM")

    bad=copy.deepcopy(qe);bad["voice_qualification"]["independence_credit_scope"]="UNRESOLVED"
    must_fail([qh],[bad],"resolved independence_credit_scope required")

    # Per-book Evidence shards are formal Evidence too. A hold gate that reads
    # only the aggregate files can be bypassed accidentally by adding a shard.
    with tempfile.TemporaryDirectory(prefix="mixed-voice-evidence-") as tmp:
        k=Path(tmp)
        write_jsonl(k/"K2_EVIDENCE_WAVE1.jsonl",[{"evidence_id":"E-BASE"}])
        write_jsonl(k/"K2_SEGMENT_EVIDENCE.jsonl",[{"evidence_id":"E-SEG"}])
        write_jsonl(k/"K2_EVIDENCE_WAVE1.d"/"QM-SRC-9000.jsonl",[{"evidence_id":"E-SHARD"}])
        ids={r.get("evidence_id") for r in v.load_formal_evidence(k)}
        assert ids=={"E-BASE","E-SEG","E-SHARD"},ids

    print("k2-mixed-voice-hold-tests: PASS")
    print("cases=19")

if __name__=="__main__":main()
