#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as v


def distillates():
    return [{"work_family_key":"WF-TEST-001","testable_hypotheses":[{"hypothesis_id":"H-TEST-001","status":"UNTESTED"}]}]


def project_hypotheses():
    return [{
        "hypothesis_id":"CDAF-H2",
        "origin_type":"PROJECT_GENERATED",
        "origin_key":"CDAF-v0.1",
        "origin_ref":"knowledge/K2_QIMEN_CONTEXTUAL_DIFFERENTIAL_ABLATION_V01.md#CDAF-H2",
        "statement":"frozen symbolic mapping should add measurable value beyond the same context-structured baseline",
        "status":"UNTESTED",
        "empirical_credit":"NONE",
        "baseline_required":True,
        "falsification_summary":"no preregistered incremental value beyond the same context baseline falsifies the proposed increment",
    }]


def plan():
    return {
        "plan_id":"K2PV-TEST-001",
        "hypothesis_id":"H-TEST-001",
        "hypothesis_origin_type":"SOURCE_DERIVED",
        "hypothesis_origin_key":"WF-TEST-001",
        "hypothesis_origin_ref":"knowledge/K2_WORK_FAMILY_DISTILLATES.jsonl#H-TEST-001",
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


def project_plan():
    p=plan()
    p.update({
        "plan_id":"K2PV-CDAF-H2",
        "hypothesis_id":"CDAF-H2",
        "hypothesis_origin_type":"PROJECT_GENERATED",
        "hypothesis_origin_key":"CDAF-v0.1",
        "hypothesis_origin_ref":"knowledge/K2_QIMEN_CONTEXTUAL_DIFFERENTIAL_ABLATION_V01.md#CDAF-H2",
        "model_name":"FROZEN_SYMBOLIC_MAPPING",
        "comparator_name":"CONTEXT_STRUCTURED_BASELINE",
    })
    return p


def batch(p=None):
    p=p or plan()
    return {
        "batch_id":"K2PVB-BATCH_001",
        "plan_id":p["plan_id"],
        "plan_sha256":v.canonical_sha256(p),
        "preregistered_at_utc":"2026-08-21T23:00:00Z",
        "model_commit_sha":"a"*40,
        "comparator_ref":"STATIC_BASELINE_V1",
        "planned_case_count":20,
        "sampling_rule":"accept consecutive eligible cases under frozen scope",
        "primary_metric":"predeclared binary score",
        "decision_rule":"candidate must exceed baseline by frozen threshold T",
        "secondary_metrics":["calibration","abstention_rate"],
        "stopping_rule":"stop only at planned_case_count unless documented external impossibility",
        "exclusion_rule":"exclude only cases ineligible before outcome is known",
        "duplicate_case_policy":"same underlying event may appear only once",
        "research_only":True,
        "status":"PREREGISTERED",
        "empirical_credit":"NONE",
    }


def freeze(p=None,b=None):
    p=p or plan();b=b or batch(p)
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
        "batch_id":b["batch_id"],
        "batch_sha256":v.canonical_sha256(b),
        "case_id":"CASE_001",
        "frozen_at_utc":"2026-08-22T00:00:00Z",
        "model_commit_sha":b["model_commit_sha"],
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
        "freeze_record_sha256":v.canonical_sha256(f),
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


def must_pass(plans,batches=None,freezes=None,outcomes=None,projects=None):
    issues=v.validate_records(distillates(),plans,batches or [],freezes or [],outcomes or [],project_hypotheses=project_hypotheses() if projects is None else projects)
    assert not issues,issues


def must_fail(plans,batches=None,freezes=None,outcomes=None,needle="",projects=None):
    issues=v.validate_records(distillates(),plans,batches or [],freezes or [],outcomes or [],project_hypotheses=project_hypotheses() if projects is None else projects)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    p=plan();must_pass([p])
    pp=project_plan();must_pass([pp])
    must_pass([p,pp])

    bad=copy.deepcopy(p);bad["hypothesis_id"]="H-NOT-FOUND"
    must_fail([bad],needle="unknown hypothesis_id")

    bad=copy.deepcopy(p);bad["hypothesis_origin_type"]="PROJECT_GENERATED"
    must_fail([bad],needle="hypothesis_origin_type does not match")

    bad=copy.deepcopy(pp);bad["hypothesis_origin_key"]="WF-FAKE-SOURCE"
    must_fail([bad],needle="hypothesis_origin_key does not match")

    bad_projects=copy.deepcopy(project_hypotheses());bad_projects[0]["origin_type"]="SOURCE_DERIVED"
    must_fail([],projects=bad_projects,needle="origin_type must be PROJECT_GENERATED")

    bad_projects=copy.deepcopy(project_hypotheses());bad_projects[0]["baseline_required"]=False
    must_fail([],projects=bad_projects,needle="must require baseline")

    bad_projects=copy.deepcopy(project_hypotheses());bad_projects[0]["empirical_credit"]="WEAK"
    must_fail([],projects=bad_projects,needle="cannot carry empirical credit")

    bad=copy.deepcopy(p);bad["freeze_required_fields"].remove("role_map")
    must_fail([bad],needle="missing mandatory fields")

    bad=copy.deepcopy(p);bad["empirical_credit"]="STRONG"
    must_fail([bad],needle="cannot carry empirical credit")

    b=batch(p);must_pass([p],[b])

    badb=copy.deepcopy(b);badb["plan_sha256"]="b"*64
    must_fail([p],[badb],needle="bind exact test plan")

    badb=copy.deepcopy(b);badb["primary_metric"]=""
    must_fail([p],[badb],needle="primary_metric must be non-empty text")

    badb=copy.deepcopy(b);badb["empirical_credit"]="WEAK"
    must_fail([p],[badb],needle="preregistered batch cannot carry empirical credit")

    f=freeze(p,b)
    must_fail([p],[],[f],needle="requires preregistered batch")
    must_pass([p],[b],[f])

    badf=copy.deepcopy(f);badf["batch_sha256"]="c"*64
    must_fail([p],[b],[badf],needle="bind exact preregistered batch")

    badf=copy.deepcopy(f);badf["frozen_at_utc"]="2026-08-21T22:00:00Z"
    must_fail([p],[b],[badf],needle="after batch preregistration")

    badf=copy.deepcopy(f);badf["frozen_payload"]["prediction"]="CHANGED_AFTER_FREEZE"
    must_fail([p],[b],[badf],needle="frozen_payload_sha256 mismatch")

    o=outcome(f);must_pass([p],[b],[f],[o])

    bado=copy.deepcopy(o);bado["freeze_record_sha256"]="d"*64
    must_fail([p],[b],[f],[bado],needle="bind exact freeze record")

    bado=copy.deepcopy(o);bado["freeze_payload_sha256"]="b"*64
    must_fail([p],[b],[f],[bado],needle="exact frozen payload hash")

    bado=copy.deepcopy(o);bado["observed_at_utc"]="2026-08-21T00:00:00Z"
    must_fail([p],[b],[f],[bado],needle="observed after freeze")

    bado=copy.deepcopy(o);bado["empirical_credit"]="WEAK"
    must_fail([p],[b],[f],[bado],needle="single-case outcome cannot upgrade empirical credit")

    bado=copy.deepcopy(o);bado["prediction_override"]="post-hoc"
    must_fail([p],[b],[f],[bado],needle="outcome fields mismatch")

    print("k2-prospective-validation-tests: PASS")
    print("cases=26 project_generated_origin=PASS source_derived_origin=PASS")

if __name__=="__main__":main()
