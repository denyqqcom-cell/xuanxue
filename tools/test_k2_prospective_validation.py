#!/usr/bin/env python3
import copy,json,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as v


def hypothesis():
    return {
        "hypothesis_id":"H-TEST-001",
        "statement":"relational model should outperform a static baseline under frozen rules",
        "freeze_requirements":"freeze object mapping, eligible rules and scoring before outcome",
        "failure_condition":"candidate fails to outperform baseline under the preregistered metric",
        "status":"UNTESTED",
    }


def distillates():
    return [{"work_family_key":"WF-TEST-001","domain":"qimen","testable_hypotheses":[hypothesis()]}]


def multi_domain_hypothesis():
    h=hypothesis()
    h["hypothesis_id"]="H-MULTI-001"
    return h


def multi_domain_distillates():
    return [{
        "work_family_key":"WF-MULTI-001",
        "domain":"ziwei",
        "domain_routes":["ziwei","fengshui"],
        "testable_hypotheses":[multi_domain_hypothesis()],
    }]


def plan():
    h=hypothesis()
    return {
        "plan_id":"K2PV-TEST-001",
        "hypothesis_id":"H-TEST-001",
        "hypothesis_sha256":v.canonical_sha256(h),
        "hypothesis_context_sha256":v.hypothesis_context_sha256("WF-TEST-001",["qimen"],h),
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


def multi_domain_plan(include_route_freeze=False):
    p=plan();h=multi_domain_hypothesis()
    p["plan_id"]="K2PV-MULTI-001"
    p["hypothesis_id"]="H-MULTI-001"
    p["hypothesis_sha256"]=v.canonical_sha256(h)
    p["hypothesis_context_sha256"]=v.hypothesis_context_sha256("WF-MULTI-001",["ziwei","fengshui"],h)
    p["work_family_key"]="WF-MULTI-001"
    if include_route_freeze:
        p["freeze_required_fields"]=sorted(set(p["freeze_required_fields"])|{"active_domain_routes"})
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
        "primary_metric":"PAIRED_SCORE_DELTA",
        "primary_metric_spec":{"scoring_rule":"PAIRED_EXACT_MATCH_DELTA_V1"},
        "decision_rule":{"aggregation":"MEAN","operator":">","threshold":0.0},
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
        "comparator_prediction":"EVENT_B",
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
        "observed_value":"EVENT_B",
        "outcome_summary":"normalized observed result",
        "evaluation":"FAIL",
        "score_components":{"CANDIDATE_SCORE":0.0,"COMPARATOR_SCORE":1.0,"PAIRED_SCORE_DELTA":-1.0},
        "post_hoc_notes":[],
        "research_only":True,
        "empirical_credit":"NONE",
        "status":"REVIEWED",
    }


def validation_text(ds,plans,batches=None,freezes=None,outcomes=None):
    issues=v.validate_records(ds,plans,batches or [],freezes or [],outcomes or [])
    return issues,"; ".join(f"{a}: {b}" for a,b in issues)


def must_pass(plans,batches=None,freezes=None,outcomes=None):
    issues,_=validation_text(distillates(),plans,batches,freezes,outcomes)
    assert not issues,issues


def must_fail(plans,batches=None,freezes=None,outcomes=None,needle=""):
    issues,text=validation_text(distillates(),plans,batches,freezes,outcomes)
    assert issues,"expected failure"
    assert needle in text,(needle,text)


def test_sharded_work_family_loader():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);k=root/"knowledge";k.mkdir()
        base={"work_family_key":"WF-BASE-001","testable_hypotheses":[{"hypothesis_id":"H-BASE-001","status":"UNTESTED"}]}
        shard={"work_family_key":"WF-SHARD-001","testable_hypotheses":[{"hypothesis_id":"H-SHARD-001","status":"UNTESTED"}]}
        (k/"K2_WORK_FAMILY_DISTILLATES.jsonl").write_text(json.dumps(base)+"\n",encoding="utf-8")
        d=k/"K2_WORK_FAMILY_DISTILLATES.d";d.mkdir()
        (d/"one.jsonl").write_text(json.dumps(shard)+"\n",encoding="utf-8")
        rows=v.load_work_family_distillates(root)
        assert [r["work_family_key"] for r in rows]==["WF-BASE-001","WF-SHARD-001"],rows


def test_multi_domain_route_freeze():
    p=multi_domain_plan(include_route_freeze=False)
    issues,text=validation_text(multi_domain_distillates(),[p])
    assert issues,"expected multi-domain plan without route freeze to fail"
    assert "active_domain_routes" in text,text

    p=multi_domain_plan(include_route_freeze=True)
    issues,text=validation_text(multi_domain_distillates(),[p])
    assert not issues,text
    b=batch(p)
    f=freeze(p,b)
    issues,text=validation_text(multi_domain_distillates(),[p],[b],[f])
    assert issues and "active_domain_routes" in text,text

    f=freeze(p,b);f["frozen_payload"]["active_domain_routes"]=["ziwei","fengshui"]
    f["frozen_payload_sha256"]=v.canonical_sha256(f["frozen_payload"])
    issues,text=validation_text(multi_domain_distillates(),[p],[b],[f])
    assert not issues,text

    bad=copy.deepcopy(f);bad["frozen_payload"]["active_domain_routes"]=["fengshui","ziwei"]
    bad["frozen_payload_sha256"]=v.canonical_sha256(bad["frozen_payload"])
    issues,text=validation_text(multi_domain_distillates(),[p],[b],[bad])
    assert issues and "preserve governed route order" in text,text

    bad=copy.deepcopy(f);bad["frozen_payload"]["active_domain_routes"]=["bazi"]
    bad["frozen_payload_sha256"]=v.canonical_sha256(bad["frozen_payload"])
    issues,text=validation_text(multi_domain_distillates(),[p],[b],[bad])
    assert issues and "outside governed routes" in text,text


def test_hypothesis_content_binding():
    p=plan()
    changed=distillates()
    changed[0]["testable_hypotheses"][0]["statement"]="changed after the plan was designed"
    issues,text=validation_text(changed,[p])
    assert issues,"expected changed hypothesis content under the same hypothesis_id to invalidate the plan"
    assert "hypothesis_sha256 does not bind exact hypothesis content" in text,text


def test_hypothesis_context_binding():
    p=multi_domain_plan(include_route_freeze=True)
    changed=multi_domain_distillates()
    changed[0]["domain_routes"]=["ziwei","fengshui","bazi"]
    issues,text=validation_text(changed,[p])
    assert issues,"expected governed domain route drift under unchanged hypothesis content to invalidate the plan"
    assert "hypothesis_context_sha256 does not bind exact governed hypothesis context" in text,text


def main():
    test_sharded_work_family_loader()
    test_multi_domain_route_freeze()
    test_hypothesis_content_binding()
    test_hypothesis_context_binding()
    p=plan();must_pass([p])

    bad=copy.deepcopy(p);bad["hypothesis_id"]="H-NOT-FOUND"
    must_fail([bad],needle="unknown hypothesis_id")

    bad=copy.deepcopy(p);bad["hypothesis_sha256"]="b"*64
    must_fail([bad],needle="does not bind exact hypothesis content")

    bad=copy.deepcopy(p);bad["hypothesis_sha256"]="B"*64
    must_fail([bad],needle="hypothesis_sha256 must be lowercase sha256")

    bad=copy.deepcopy(p);bad["hypothesis_context_sha256"]="c"*64
    must_fail([bad],needle="does not bind exact governed hypothesis context")

    bad=copy.deepcopy(p);bad["hypothesis_context_sha256"]="C"*64
    must_fail([bad],needle="hypothesis_context_sha256 must be lowercase sha256")

    bad=copy.deepcopy(p);bad["freeze_required_fields"].remove("role_map")
    must_fail([bad],needle="missing mandatory fields")

    bad=copy.deepcopy(p);bad["empirical_credit"]="STRONG"
    must_fail([bad],needle="cannot carry empirical credit")

    b=batch(p);must_pass([p],[b])

    legacy=copy.deepcopy(b);legacy.pop("primary_metric_spec",None)
    must_fail([p],[legacy],needle="primary_metric_spec")

    badb=copy.deepcopy(b);badb["primary_metric_spec"]="score it later"
    must_fail([p],[badb],needle="primary_metric_spec must be machine-evaluable object")

    badb=copy.deepcopy(b);badb["primary_metric_spec"]["scoring_rule"]="POST_HOC_V1"
    must_fail([p],[badb],needle="primary_metric_spec scoring_rule must be one of")

    badb=copy.deepcopy(b);badb["primary_metric_spec"]["extra"]="free_degree"
    must_fail([p],[badb],needle="primary_metric_spec fields mismatch")

    badb=copy.deepcopy(b);badb["primary_metric"]="PRIMARY_SCORE"
    must_fail([p],[badb],needle="paired scoring rule requires primary_metric=PAIRED_SCORE_DELTA")

    badb=copy.deepcopy(b);badb["plan_sha256"]="b"*64
    must_fail([p],[badb],needle="bind exact test plan")

    badb=copy.deepcopy(b);badb["primary_metric"]="predeclared binary score"
    must_fail([p],[badb],needle="primary_metric must be uppercase machine key")

    badb=copy.deepcopy(b);badb["decision_rule"]="candidate must exceed baseline by frozen threshold T"
    must_fail([p],[badb],needle="decision_rule must be machine-evaluable object")

    badb=copy.deepcopy(b);badb["decision_rule"]["threshold"]="T"
    must_fail([p],[badb],needle="decision_rule threshold must be finite numeric")

    badb=copy.deepcopy(b);badb["decision_rule"]["aggregation"]="BEST_CASE"
    must_fail([p],[badb],needle="decision_rule aggregation must be one of")

    badb=copy.deepcopy(b);badb["decision_rule"]["operator"]="APPROX"
    must_fail([p],[badb],needle="decision_rule operator must be one of")

    badb=copy.deepcopy(b);badb["planned_case_count"]=None
    must_fail([p],[badb],needle="planned_case_count must be positive integer")

    badb=copy.deepcopy(b);badb["empirical_credit"]="WEAK"
    must_fail([p],[badb],needle="preregistered batch cannot carry empirical credit")

    f=freeze(p,b)
    must_fail([p],[],[f],needle="requires preregistered batch")

    legacyf=copy.deepcopy(f);legacyf["frozen_payload"].pop("comparator_prediction")
    legacyf["frozen_payload_sha256"]=v.canonical_sha256(legacyf["frozen_payload"])
    must_fail([p],[b],[legacyf],needle="comparator_prediction")

    badf=copy.deepcopy(f);badf["frozen_payload"]["comparator_prediction"]=""
    badf["frozen_payload_sha256"]=v.canonical_sha256(badf["frozen_payload"])
    must_fail([p],[b],[badf],needle="comparator_prediction")

    must_pass([p],[b],[f])

    capped=copy.deepcopy(b);capped["planned_case_count"]=1
    f1=freeze(p,capped)
    f2=copy.deepcopy(f1);f2["freeze_id"]="K2PVF-CASE_002";f2["case_id"]="CASE_002"
    must_fail([p],[capped],[f1,f2],needle="freeze count exceeds planned_case_count")

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

    bado=copy.deepcopy(o);bado["observed_value"]=""
    must_fail([p],[b],[f],[bado],needle="observed_value must be non-empty text for evaluable outcome")

    bado=copy.deepcopy(o);bado["score_components"]={}
    must_fail([p],[b],[f],[bado],needle="missing required paired score")

    bado=copy.deepcopy(o);bado["score_components"].pop("COMPARATOR_SCORE")
    must_fail([p],[b],[f],[bado],needle="COMPARATOR_SCORE")

    bado=copy.deepcopy(o);bado["score_components"]["CANDIDATE_SCORE"]="later"
    must_fail([p],[b],[f],[bado],needle="paired score must be finite numeric: CANDIDATE_SCORE")

    bado=copy.deepcopy(o);bado["score_components"]["CANDIDATE_SCORE"]=1.0
    must_fail([p],[b],[f],[bado],needle="paired score does not match preregistered scoring function: CANDIDATE_SCORE")

    bado=copy.deepcopy(o);bado["score_components"]["COMPARATOR_SCORE"]=0.0
    must_fail([p],[b],[f],[bado],needle="paired score does not match preregistered scoring function: COMPARATOR_SCORE")

    bado=copy.deepcopy(o);bado["score_components"]["PAIRED_SCORE_DELTA"]=0.0
    must_fail([p],[b],[f],[bado],needle="paired score does not match preregistered scoring function: PAIRED_SCORE_DELTA")

    hit=copy.deepcopy(o);hit["observed_value"]="EVENT_A";hit["score_components"]={"CANDIDATE_SCORE":1.0,"COMPARATOR_SCORE":0.0,"PAIRED_SCORE_DELTA":1.0};hit["evaluation"]="SUCCESS"
    must_pass([p],[b],[f],[hit])

    abst=copy.deepcopy(o);abst["evaluation"]="ABSTAIN";abst["observed_value"]=None;abst["score_components"]={}
    must_pass([p],[b],[f],[abst])

    bado=copy.deepcopy(o);bado["empirical_credit"]="WEAK"
    must_fail([p],[b],[f],[bado],needle="single-case outcome cannot upgrade empirical credit")

    bado=copy.deepcopy(o);bado["prediction_override"]="post-hoc"
    must_fail([p],[b],[f],[bado],needle="outcome fields mismatch")

    print("k2-prospective-validation-tests: PASS")
    print("cases=55")

if __name__=="__main__":main()
