#!/usr/bin/env python3
import json,math,re,sys
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as pv

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"

REVIEW_FIELDS={
    "review_id","batch_id","batch_sha256","reviewed_at_utc","planned_case_count",
    "freeze_count","outcome_count","evaluable_count","abstain_count","unevaluable_count",
    "outcome_ids","outcome_records_sha256","aggregate_primary_metric","aggregate_value",
    "decision_met","batch_verdict","research_only","empirical_credit","status",
}
REVIEW_ID_RE=re.compile(r"^K2PVBR-[A-Z0-9_-]+$")
SHA64_RE=re.compile(r"^[0-9a-f]{64}$")
VERDICTS={"PASS","FAIL","INCOMPLETE"}
EVALUABLE={"SUCCESS","PARTIAL","FAIL"}


def fail(msg):
    print(f"k2-prospective-batch-review: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


def canonical_sha256(value):
    return pv.canonical_sha256(value)


def canonical_outcome_records_sha256(outcomes):
    ordered=sorted(outcomes,key=lambda row:row.get("outcome_id") or "")
    return canonical_sha256(ordered)


def finite_number(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)


def utc_value(v):
    if not isinstance(v,str) or not pv.UTC_RE.match(v):return None
    return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def apply_operator(value,operator,threshold):
    if operator==">":return value>threshold
    if operator==">=":return value>=threshold
    if operator=="<":return value<threshold
    if operator=="<=":return value<=threshold
    return None


def validate_records(distillates,plans,batches,freezes,outcomes,reviews):
    issues=[]
    upstream=pv.validate_records(distillates,plans,batches,freezes,outcomes)
    if upstream:
        issues.extend(("UPSTREAM_PROSPECTIVE",f"upstream prospective contract invalid: {rid}: {msg}") for rid,msg in upstream)
        return issues

    batch_by_id={b.get("batch_id"):b for b in batches}
    freeze_by_id={f.get("freeze_id"):f for f in freezes}
    freezes_by_batch={}
    for f in freezes:freezes_by_batch.setdefault(f.get("batch_id"),[]).append(f)
    outcomes_by_batch={}
    for o in outcomes:
        fr=freeze_by_id.get(o.get("freeze_id"))
        if fr:outcomes_by_batch.setdefault(fr.get("batch_id"),[]).append(o)

    seen_review=set();seen_batch=set()
    for r in reviews:
        rid=r.get("review_id") or "<missing>";bid=r.get("batch_id")
        if set(r)!=REVIEW_FIELDS:
            issues.append((rid,f"review fields mismatch missing={sorted(REVIEW_FIELDS-set(r))} extra={sorted(set(r)-REVIEW_FIELDS)}"))
        if not isinstance(rid,str) or not REVIEW_ID_RE.match(rid):issues.append((rid,"invalid review_id"))
        if rid in seen_review:issues.append((rid,"duplicate review_id"))
        seen_review.add(rid)
        if bid in seen_batch:issues.append((rid,"a batch may have only one active review row"))
        seen_batch.add(bid)

        batch=batch_by_id.get(bid)
        if not batch:
            issues.append((rid,f"unknown batch_id: {bid}"))
            continue
        expected_batch_sha=canonical_sha256(batch)
        if r.get("batch_sha256")!=expected_batch_sha:issues.append((rid,"batch_sha256 does not bind exact preregistered batch"))
        if not isinstance(r.get("batch_sha256"),str) or not SHA64_RE.match(r.get("batch_sha256","")):issues.append((rid,"batch_sha256 must be lowercase sha256"))

        fs=freezes_by_batch.get(bid,[]);os=outcomes_by_batch.get(bid,[])
        planned=batch.get("planned_case_count")
        freeze_count=len(fs);outcome_count=len(os)
        evaluations=[o.get("evaluation") for o in os]
        evaluable_count=sum(x in EVALUABLE for x in evaluations)
        abstain_count=sum(x=="ABSTAIN" for x in evaluations)
        unevaluable_count=sum(x=="UNEVALUABLE" for x in evaluations)

        expected_counts={
            "planned_case_count":planned,"freeze_count":freeze_count,"outcome_count":outcome_count,
            "evaluable_count":evaluable_count,"abstain_count":abstain_count,"unevaluable_count":unevaluable_count,
        }
        for field,value in expected_counts.items():
            if r.get(field)!=value:issues.append((rid,f"{field} does not match retained batch records"))

        expected_outcome_ids=sorted(o.get("outcome_id") for o in os)
        if r.get("outcome_ids")!=expected_outcome_ids:
            issues.append((rid,"outcome_ids must include every batch outcome exactly once"))
        if r.get("outcome_records_sha256")!=canonical_outcome_records_sha256(os):
            issues.append((rid,"outcome_records_sha256 does not bind exact retained batch outcomes"))
        if not isinstance(r.get("outcome_records_sha256"),str) or not SHA64_RE.match(r.get("outcome_records_sha256","")):
            issues.append((rid,"outcome_records_sha256 must be lowercase sha256"))

        review_dt=utc_value(r.get("reviewed_at_utc"))
        if review_dt is None:
            issues.append((rid,"reviewed_at_utc must be UTC second timestamp ending Z"))
        else:
            retained_times=[utc_value(batch.get("preregistered_at_utc"))]
            retained_times.extend(utc_value(f.get("frozen_at_utc")) for f in fs)
            retained_times.extend(utc_value(o.get("observed_at_utc")) for o in os)
            retained_times=[x for x in retained_times if x]
            if retained_times and review_dt<=max(retained_times):
                issues.append((rid,"batch review must occur after all retained records"))

        if r.get("aggregate_primary_metric")!=batch.get("primary_metric"):
            issues.append((rid,"aggregate_primary_metric must equal preregistered primary_metric"))

        fixed_n_complete=freeze_count==planned
        outcome_complete=outcome_count==freeze_count and all(f.get("freeze_id") in {o.get("freeze_id") for o in os} for f in fs)
        has_non_evaluable=(abstain_count+unevaluable_count)>0

        if not fixed_n_complete:
            issues.append((rid,"incomplete fixed-N coverage"))
        if not outcome_complete:
            issues.append((rid,"incomplete outcome coverage"))

        complete_for_decision=fixed_n_complete and outcome_complete and not has_non_evaluable
        expected_aggregate=None;expected_decision=None;expected_verdict="INCOMPLETE"
        if complete_for_decision:
            deltas=[]
            for o in os:
                fr=freeze_by_id.get(o.get("freeze_id"))
                scores=pv.paired_exact_match_scores(batch,fr,o) if fr else None
                if not scores or pv.PAIRED_PRIMARY_METRIC not in scores:
                    issues.append((rid,f"cannot recompute paired delta for outcome {o.get('outcome_id')}"))
                    continue
                deltas.append(scores[pv.PAIRED_PRIMARY_METRIC])
            if len(deltas)==planned:
                expected_aggregate=sum(deltas)/planned
                rule=batch.get("decision_rule") or {}
                expected_decision=apply_operator(expected_aggregate,rule.get("operator"),rule.get("threshold"))
                if expected_decision is None:
                    issues.append((rid,"cannot apply preregistered decision rule"))
                else:
                    expected_verdict="PASS" if expected_decision else "FAIL"

        if has_non_evaluable and r.get("batch_verdict")!="INCOMPLETE":
            issues.append((rid,"non-evaluable cases require INCOMPLETE verdict under current V1 policy"))

        if complete_for_decision:
            if not finite_number(r.get("aggregate_value")) or r.get("aggregate_value")!=expected_aggregate:
                issues.append((rid,"aggregate_value does not match machine recomputation"))
            if r.get("decision_met") is not expected_decision:
                issues.append((rid,"decision_met does not match preregistered decision rule"))
            if r.get("batch_verdict")!=expected_verdict:
                issues.append((rid,"batch verdict does not match preregistered decision rule"))
        else:
            if r.get("aggregate_value") is not None:issues.append((rid,"incomplete review aggregate_value must be null"))
            if r.get("decision_met") is not None:issues.append((rid,"incomplete review decision_met must be null"))
            if r.get("batch_verdict")!="INCOMPLETE":issues.append((rid,"incomplete batch review verdict must be INCOMPLETE"))

        if r.get("batch_verdict") not in VERDICTS:issues.append((rid,"invalid batch_verdict"))
        if r.get("research_only") is not True:issues.append((rid,"batch review must be research_only=true"))
        if r.get("empirical_credit")!="NONE":issues.append((rid,"batch review cannot upgrade empirical credit"))
        if r.get("status")!="REVIEWED":issues.append((rid,"batch review status must be REVIEWED"))
        if pv.PATH_RE.search(json.dumps(r,ensure_ascii=False)):issues.append((rid,"batch review leaks local filesystem path"))
    return issues


def main():
    project=pv.load_json(K/"PROJECT_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked")
    distillates=pv.load_work_family_distillates(ROOT)
    plans=pv.load_jsonl(K/"K2_PROSPECTIVE_TEST_PLANS.jsonl")
    batches=pv.load_jsonl(K/"K2_PROSPECTIVE_BATCHES.jsonl")
    freezes=pv.load_jsonl(K/"K2_PROSPECTIVE_FREEZES.jsonl")
    outcomes=pv.load_jsonl(K/"K2_PROSPECTIVE_OUTCOMES.jsonl")
    reviews=pv.load_jsonl(K/"K2_PROSPECTIVE_BATCH_REVIEWS.jsonl")
    issues=validate_records(distillates,plans,batches,freezes,outcomes,reviews)
    if issues:fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")
    print("k2-prospective-batch-review: PASS")
    print(f"batches={len(batches)} reviews={len(reviews)} issues=0")
    print("empirical_credit_upgrade_blocked=true")

if __name__=="__main__":main()
