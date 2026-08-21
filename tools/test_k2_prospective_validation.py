#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as v


def distillates():
    return [{"work_family_key":"WF-TEST-001","testable_hypotheses":[{"hypothesis_id":"H-TEST-001","status":"UNTESTED"}]}]


def plan():
    return {
        "plan_id":"K2PV-TEST-001",
        "hypothesis_id":"H-TEST-001",
        "work_family_key":"WF-TEST-001",
        "model_name":"RELATIONAL_MODEL",
        "comparator_name":"STATIC_BASELINE",
        "question_scope":"low-risk prospective research",
        "unit_of_analysis":"ONE_PREREGISTERED_CASE",
        "freeze_required_fields":sorted(v.MANDATORY_FREEZE_FIELDS),
        "evaluation_metrics":["primary_metric","calibration"],
        "success_condition":"predeclared threshold is met without post-hoc rule changes",
        "failure_condition":"candidate does not outperform baseline under frozen rules",
        "abstention_rule":"abstain when role map cannot be frozen before outcome",
        "leakage_controls":["outcome unknown at freeze","retain failures"],
        "high_risk_policy":"RESEARCH_ONLY; no operational advice",
        "update_policy":"new model version requires new freezes",
        "status":"DESIGN_READY",
        "empirical_credit":"NONE",
    }


def freeze(p=None):
    p=p or plan()
    payload={
        "question_definition":"Will normalized event A occur within frozen window?",
        "asked_object":"OBJECT_A",
        "object_graph":{"subject":"A","target":"B"},
        "role_map":{"primary":"A","secondary":"B"},
        "eligible_rule_set":["R1","R2"],
        "primary_layers":["L1"],
        "boundary_conditions":["B1"],
        "interpretation_path":["R1","R2"],
        "prediction":"EVENT_A",
        "confidence":0.6,
        "abstention_condition":"required object mapping becomes ambiguous before freeze",
    }
    return {
        "freeze_id":"K2PVF-CASE_001",
        "plan_id":p["plan_id"],
        "case_id":"CASE_001",
        "frozen_at_utc":"2026-08-22T00:00:00Z",
        "model_commit_sha":"a"*40,
        "frozen_payload":payload,
        "frozen_payload_sha256":v.canonical_sha256(payload),
        "outcome_known_at_freeze":False,
        "research_only":True,
        "status":"FROZEN",
    }


def outcome(f=None):
    f=f or freeze()
    return {
        "outcome_id":"K2PVO-CASE_001",
        "freeze_id":f["freeze_id"],
        "observed_at_utc":"2026-08-23T00:00:00Z",
        "freeze_payload_sha256":f["frozen_payload_sha256"],
        "outcome_summary":"normalized observed result",
        "evaluation":"FAIL",
        "score_components":{"primary_metric":0},
        "post_hoc_notes":[],
        "research_only":True,
        "empirical_credit":"NONE",
        "status":"REVIEWED",
    }


def must_pass(plans,freezes=None,outcomes=None):
    issues=v.validate_records(distillates(),plans,freezes or [],outcomes or [])
    assert not issues,issues


def must_fail(plans,freezes=None,outcomes=None,needle=""):
    issues=v.validate_records(distillates(),plans,freezes or [],outcomes or [])
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    p=plan();must_pass([p])

    bad=copy.deepcopy(p);bad["hypothesis_id"]="H-NOT-FOUND"
    must_fail([bad],needle="unknown hypothesis_id")

    bad=copy.deepcopy(p);bad["freeze_required_fields"].remove("role_map")
    must_fail([bad],needle="missing mandatory fields")

    bad=copy.deepcopy(p);bad["empirical_credit"]="STRONG"
    must_fail([bad],needle="cannot carry empirical credit")

    f=freeze(p);must_pass([p],[f])

    badf=copy.deepcopy(f);badf["frozen_payload"]["prediction"]="CHANGED_AFTER_FREEZE"
    must_fail([p],[badf],needle="frozen_payload_sha256 mismatch")

    o=outcome(f);must_pass([p],[f],[o])

    bado=copy.deepcopy(o);bado["freeze_payload_sha256"]="b"*64
    must_fail([p],[f],[bado],needle="exact frozen payload hash")

    bado=copy.deepcopy(o);bado["observed_at_utc"]="2026-08-21T00:00:00Z"
    must_fail([p],[f],[bado],needle="observed after freeze")

    bado=copy.deepcopy(o);bado["empirical_credit"]="WEAK"
    must_fail([p],[f],[bado],needle="single-case outcome cannot upgrade empirical credit")

    bado=copy.deepcopy(o);bado["prediction_override"]="post-hoc"
    must_fail([p],[f],[bado],needle="outcome fields mismatch")

    print("k2-prospective-validation-tests: PASS")
    print("cases=11")

if __name__=="__main__":main()
