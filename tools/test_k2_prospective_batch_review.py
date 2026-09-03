#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_k2_prospective_validation as fx
import validate_k2_prospective_batch_review as br

ROOT=Path(__file__).resolve().parents[1]


def full_fixture(candidate_wins=True):
    p=fx.plan();b=fx.batch(p);b["planned_case_count"]=2
    f1=fx.freeze(p,b)
    f2=copy.deepcopy(f1)
    f2["freeze_id"]="K2PVF-CASE_002";f2["case_id"]="CASE_002";f2["frozen_at_utc"]="2026-08-22T00:01:00Z"

    def make_outcome(f,idx):
        o=fx.outcome(f)
        o["outcome_id"]=f"K2PVO-CASE_{idx:03d}"
        o["observed_at_utc"]=f"2026-08-23T00:0{idx}:00Z"
        if candidate_wins:
            o["observed_value"]="EVENT_A";o["evaluation"]="SUCCESS"
            o["score_components"]={"CANDIDATE_SCORE":1.0,"COMPARATOR_SCORE":0.0,"PAIRED_SCORE_DELTA":1.0}
        return o

    outcomes=[make_outcome(f1,1),make_outcome(f2,2)]
    return p,b,[f1,f2],outcomes


def review_for(b,freezes,outcomes,verdict="PASS",aggregate=1.0,decision_met=True):
    evaluations=[o["evaluation"] for o in outcomes]
    return {
        "review_id":"K2PVBR-BATCH_001",
        "batch_id":b["batch_id"],
        "batch_sha256":br.canonical_sha256(b),
        "reviewed_at_utc":"2026-08-24T00:00:00Z",
        "planned_case_count":b["planned_case_count"],
        "freeze_count":len(freezes),
        "outcome_count":len(outcomes),
        "evaluable_count":sum(x in {"SUCCESS","PARTIAL","FAIL"} for x in evaluations),
        "abstain_count":sum(x=="ABSTAIN" for x in evaluations),
        "unevaluable_count":sum(x=="UNEVALUABLE" for x in evaluations),
        "outcome_ids":sorted(o["outcome_id"] for o in outcomes),
        "outcome_records_sha256":br.canonical_outcome_records_sha256(outcomes),
        "aggregate_primary_metric":b["primary_metric"],
        "aggregate_value":aggregate,
        "decision_met":decision_met,
        "batch_verdict":verdict,
        "research_only":True,
        "empirical_credit":"NONE",
        "status":"REVIEWED",
    }


def validate(p,b,freezes,outcomes,reviews):
    return br.validate_records(fx.distillates(),[p],[b],freezes,outcomes,reviews)


def must_fail(p,b,freezes,outcomes,reviews,needle):
    issues=validate(p,b,freezes,outcomes,reviews)
    text="; ".join(f"{a}: {msg}" for a,msg in issues)
    assert issues,"expected failure"
    assert needle in text,(needle,text)


def main():
    assert (ROOT/"knowledge/K2_PROSPECTIVE_BATCH_REVIEWS.jsonl").exists()
    assert (ROOT/"knowledge/K2_PROSPECTIVE_BATCH_REVIEW_PROTOCOL.md").exists()
    workflow=(ROOT/".github/workflows/knowledge-engine-ci.yml").read_text(encoding="utf-8")
    assert "python3 tools/test_k2_prospective_batch_review.py" in workflow
    assert "python3 tools/validate_k2_prospective_batch_review.py" in workflow

    p,b,freezes,outcomes=full_fixture(candidate_wins=True)
    r=review_for(b,freezes,outcomes)
    assert not validate(p,b,freezes,outcomes,[r]),validate(p,b,freezes,outcomes,[r])

    under_freezes=freezes[:1];under_outcomes=outcomes[:1]
    bad=review_for(b,under_freezes,under_outcomes)
    must_fail(p,b,under_freezes,under_outcomes,[bad],"incomplete fixed-N coverage")
    good=review_for(b,under_freezes,under_outcomes,verdict="INCOMPLETE",aggregate=None,decision_met=None)
    assert not validate(p,b,under_freezes,under_outcomes,[good]),validate(p,b,under_freezes,under_outcomes,[good])

    bad=review_for(b,freezes,outcomes[:1])
    must_fail(p,b,freezes,outcomes[:1],[bad],"incomplete outcome coverage")

    abst_outcomes=copy.deepcopy(outcomes)
    abst_outcomes[1]["evaluation"]="ABSTAIN";abst_outcomes[1]["observed_value"]=None;abst_outcomes[1]["score_components"]={}
    bad=review_for(b,freezes,abst_outcomes)
    must_fail(p,b,freezes,abst_outcomes,[bad],"non-evaluable cases require INCOMPLETE verdict")
    good=review_for(b,freezes,abst_outcomes,verdict="INCOMPLETE",aggregate=None,decision_met=None)
    assert not validate(p,b,freezes,abst_outcomes,[good]),validate(p,b,freezes,abst_outcomes,[good])

    bad=copy.deepcopy(r);bad["outcome_ids"]=bad["outcome_ids"][:1]
    must_fail(p,b,freezes,outcomes,[bad],"outcome_ids must include every batch outcome exactly once")

    bad=copy.deepcopy(r);bad["outcome_records_sha256"]="a"*64
    must_fail(p,b,freezes,outcomes,[bad],"outcome_records_sha256 does not bind exact retained batch outcomes")

    bad=copy.deepcopy(r);bad["aggregate_value"]=0.5
    must_fail(p,b,freezes,outcomes,[bad],"aggregate_value does not match machine recomputation")

    bad=copy.deepcopy(r);bad["batch_verdict"]="FAIL";bad["decision_met"]=False
    must_fail(p,b,freezes,outcomes,[bad],"batch verdict does not match preregistered decision rule")

    bad=copy.deepcopy(r);bad["reviewed_at_utc"]="2026-08-22T12:00:00Z"
    must_fail(p,b,freezes,outcomes,[bad],"batch review must occur after all retained records")

    bad=copy.deepcopy(r);bad["empirical_credit"]="WEAK"
    must_fail(p,b,freezes,outcomes,[bad],"batch review cannot upgrade empirical credit")

    p2,b2,freezes2,outcomes2=full_fixture(candidate_wins=False)
    r2=review_for(b2,freezes2,outcomes2,verdict="FAIL",aggregate=-1.0,decision_met=False)
    assert not validate(p2,b2,freezes2,outcomes2,[r2]),validate(p2,b2,freezes2,outcomes2,[r2])

    print("k2-prospective-batch-review-tests: PASS")
    print("cases=12")

if __name__=="__main__":main()
