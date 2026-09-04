#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_k2_prospective_validation as fx
import validate_k2_prospective_validation as pv
import validate_k2_prospective_batch_review as br
import validate_k2_empirical_credit_review as er


def make_batch_review(batch,freezes,outcomes,index):
    deltas=[o["score_components"]["PAIRED_SCORE_DELTA"] for o in outcomes]
    aggregate=sum(deltas)/len(deltas)
    rule=batch["decision_rule"]
    decision=br.apply_operator(aggregate,rule["operator"],rule["threshold"])
    return {
        "review_id":f"K2PVBR-BATCH_{index:03d}",
        "batch_id":batch["batch_id"],
        "batch_sha256":br.canonical_sha256(batch),
        "reviewed_at_utc":f"2026-09-{3*index+1:02d}T00:00:00Z",
        "planned_case_count":batch["planned_case_count"],
        "freeze_count":len(freezes),
        "outcome_count":len(outcomes),
        "evaluable_count":len(outcomes),
        "abstain_count":0,
        "unevaluable_count":0,
        "outcome_ids":sorted(o["outcome_id"] for o in outcomes),
        "outcome_records_sha256":br.canonical_outcome_records_sha256(outcomes),
        "aggregate_primary_metric":batch["primary_metric"],
        "aggregate_value":aggregate,
        "decision_met":decision,
        "batch_verdict":"PASS" if decision else "FAIL",
        "research_only":True,
        "empirical_credit":"NONE",
        "status":"REVIEWED",
    }


def make_batch(plan,index,n=12,candidate_wins=True,duplicate_case_tokens=False):
    batch=fx.batch(plan)
    batch["batch_id"]=f"K2PVB-BATCH_{index:03d}"
    prereg_day=1+(index-1)*3
    batch["preregistered_at_utc"]=f"2026-09-{prereg_day:02d}T00:00:00Z"
    batch["planned_case_count"]=n
    freezes=[];outcomes=[]
    freeze_day=prereg_day+1;outcome_day=prereg_day+2
    for case_index in range(1,n+1):
        freeze=fx.freeze(plan,batch)
        freeze["freeze_id"]=f"K2PVF-B{index:02d}_CASE_{case_index:03d}"
        token_batch=1 if duplicate_case_tokens and index>1 else index
        freeze["case_id"]=f"CASE_B{token_batch:02d}_{case_index:03d}"
        freeze["frozen_at_utc"]=f"2026-09-{freeze_day:02d}T00:{case_index:02d}:00Z"
        freeze["batch_sha256"]=pv.canonical_sha256(batch)
        freeze["model_commit_sha"]=batch["model_commit_sha"]
        freeze["frozen_payload_sha256"]=pv.canonical_sha256(freeze["frozen_payload"])
        freezes.append(freeze)

        outcome=fx.outcome(freeze)
        outcome["outcome_id"]=f"K2PVO-B{index:02d}_CASE_{case_index:03d}"
        outcome["observed_at_utc"]=f"2026-09-{outcome_day:02d}T00:{case_index:02d}:00Z"
        if candidate_wins:
            outcome["observed_value"]="EVENT_A"
            outcome["evaluation"]="SUCCESS"
            outcome["score_components"]={"CANDIDATE_SCORE":1.0,"COMPARATOR_SCORE":0.0,"PAIRED_SCORE_DELTA":1.0}
        else:
            outcome["observed_value"]="EVENT_B"
            outcome["evaluation"]="FAIL"
            outcome["score_components"]={"CANDIDATE_SCORE":0.0,"COMPARATOR_SCORE":1.0,"PAIRED_SCORE_DELTA":-1.0}
        outcomes.append(outcome)
    review=make_batch_review(batch,freezes,outcomes,index)
    return batch,freezes,outcomes,review


def fixture(second_batch_wins=True,n=12,duplicate_case_tokens=False):
    plan=fx.plan()
    b1,f1,o1,r1=make_batch(plan,1,n=n,candidate_wins=True)
    b2,f2,o2,r2=make_batch(plan,2,n=n,candidate_wins=second_batch_wins,duplicate_case_tokens=duplicate_case_tokens)
    return plan,[b1,b2],f1+f2,o1+o2,[r1,r2]


def credit_review(plan,batches,freezes,outcomes,batch_reviews,readiness=None):
    summary=er.compute_credit_summary(plan,batches,freezes,outcomes,batch_reviews)
    return {
        "credit_review_id":"K2PVECR-H_TEST_001",
        "policy_version":er.POLICY_VERSION,
        "plan_id":plan["plan_id"],
        "hypothesis_id":plan["hypothesis_id"],
        "hypothesis_sha256":plan["hypothesis_sha256"],
        "hypothesis_context_sha256":plan["hypothesis_context_sha256"],
        "model_commit_sha":batches[0]["model_commit_sha"],
        "comparator_ref":batches[0]["comparator_ref"],
        "replication_contract_sha256":er.replication_contract_sha256(batches[0]),
        "reviewed_at_utc":"2026-09-10T00:00:00Z",
        "batch_review_ids":summary["batch_review_ids"],
        "batch_review_records_sha256":summary["batch_review_records_sha256"],
        "batch_count":summary["batch_count"],
        "total_case_count":summary["total_case_count"],
        "discordant_count":summary["discordant_count"],
        "candidate_win_count":summary["candidate_win_count"],
        "comparator_win_count":summary["comparator_win_count"],
        "tie_count":summary["tie_count"],
        "pooled_paired_delta":summary["pooled_paired_delta"],
        "one_sided_exact_pvalue":summary["one_sided_exact_pvalue"],
        "replication_consistent":summary["replication_consistent"],
        "case_token_unique":summary["case_token_unique"],
        "minimum_batch_count":er.MIN_BATCH_COUNT,
        "minimum_discordant_count":er.MIN_DISCORDANT_COUNT,
        "alpha":er.ALPHA,
        "credit_readiness":readiness or summary["credit_readiness"],
        "research_only":True,
        "empirical_credit":"NONE",
        "status":"REVIEWED",
    }


def validate(plan,batches,freezes,outcomes,batch_reviews,credit_reviews):
    return er.validate_records(fx.distillates(),[plan],batches,freezes,outcomes,batch_reviews,credit_reviews)


def must_fail(plan,batches,freezes,outcomes,batch_reviews,credit_reviews,needle):
    issues=validate(plan,batches,freezes,outcomes,batch_reviews,credit_reviews)
    text="; ".join(f"{a}: {msg}" for a,msg in issues)
    assert issues,"expected failure"
    assert needle in text,(needle,text)


def main():
    # Fail-first for the next provenance boundary: a preregistered batch must
    # bind the exact empirical-credit policy before any outcome can exist.
    p0=fx.plan();b0=fx.batch(p0)
    issues0=pv.validate_records(fx.distillates(),[p0],[b0],[],[])
    text0="; ".join(f"{a}: {msg}" for a,msg in issues0)
    assert issues0,"expected preregistered batch without empirical_credit_policy binding to fail"
    assert "empirical_credit_policy" in text0,text0

    plan,batches,freezes,outcomes,batch_reviews=fixture(second_batch_wins=True,n=12)
    row=credit_review(plan,batches,freezes,outcomes,batch_reviews)
    assert row["credit_readiness"]=="READY_FOR_MANUAL_EMPIRICAL_REVIEW",row
    assert not validate(plan,batches,freezes,outcomes,batch_reviews,[row]),validate(plan,batches,freezes,outcomes,batch_reviews,[row])

    losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews=fixture(second_batch_wins=False,n=12)
    losing_row=credit_review(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews)
    assert losing_row["credit_readiness"]=="NOT_ELIGIBLE",losing_row
    assert not validate(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews,[losing_row])
    bad=copy.deepcopy(losing_row);bad["credit_readiness"]="READY_FOR_MANUAL_EMPIRICAL_REVIEW"
    must_fail(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews,[bad],"credit_readiness does not match machine policy")

    bad=copy.deepcopy(row);bad["batch_review_ids"]=bad["batch_review_ids"][:1]
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"batch_review_ids must bind the complete replication cohort")

    bad=copy.deepcopy(row);bad["batch_review_records_sha256"]="0"*64
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"batch_review_records_sha256 does not bind exact cohort reviews")

    bad=copy.deepcopy(row);bad["one_sided_exact_pvalue"]=0.5
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"one_sided_exact_pvalue does not match machine recomputation")

    small_plan,small_batches,small_freezes,small_outcomes,small_reviews=fixture(second_batch_wins=True,n=5)
    small_row=credit_review(small_plan,small_batches,small_freezes,small_outcomes,small_reviews)
    assert small_row["credit_readiness"]=="NOT_ELIGIBLE",small_row
    assert not validate(small_plan,small_batches,small_freezes,small_outcomes,small_reviews,[small_row])

    dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews=fixture(second_batch_wins=True,n=12,duplicate_case_tokens=True)
    dup_row=credit_review(dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews)
    assert dup_row["credit_readiness"]=="NOT_ELIGIBLE",dup_row
    assert not validate(dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews,[dup_row])

    bad=copy.deepcopy(row);bad["empirical_credit"]="WEAK"
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"empirical credit review cannot upgrade empirical_credit")

    bad=copy.deepcopy(row);bad["reviewed_at_utc"]="2026-09-03T00:00:00Z"
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"empirical credit review must occur after all cohort batch reviews")

    bad=copy.deepcopy(row);bad["replication_contract_sha256"]="f"*64
    must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"replication_contract_sha256 does not identify a governed cohort")

    print("k2-empirical-credit-review-tests: PASS")
    print("cases=11")

if __name__=="__main__":main()
