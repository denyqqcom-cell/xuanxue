#!/usr/bin/env python3
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_k2_prospective_validation as fx
import validate_k2_prospective_validation as pv
import validate_k2_prospective_batch_review as br
import validate_k2_empirical_credit_review as er
import validate_k2_sample_provenance as sp
import k2_sample_fingerprint as sf

SYNTHETIC_SECRET=b"S"*32


def sample_policy():
    rows=sp.load_policies()
    return next(row for row in rows if row.get("policy_version")=="SAMPLE_PROVENANCE_V1")


def identity_schema():
    return sf.get_identity_schema("SAMPLE_IDENTITY_V1")


def make_batch_review(batch,freezes,outcomes,index):
    deltas=[o["score_components"]["PAIRED_SCORE_DELTA"] for o in outcomes]
    aggregate=sum(deltas)/len(deltas)
    rule=batch["decision_rule"]
    decision=br.apply_operator(aggregate,rule["operator"],rule["threshold"])
    return {
        "review_id":f"K2PVBR-BATCH_{index:03d}","batch_id":batch["batch_id"],"batch_sha256":br.canonical_sha256(batch),
        "reviewed_at_utc":f"2026-09-{3*index+1:02d}T00:00:00Z","planned_case_count":batch["planned_case_count"],
        "freeze_count":len(freezes),"outcome_count":len(outcomes),"evaluable_count":len(outcomes),"abstain_count":0,"unevaluable_count":0,
        "outcome_ids":sorted(o["outcome_id"] for o in outcomes),"outcome_records_sha256":br.canonical_outcome_records_sha256(outcomes),
        "aggregate_primary_metric":batch["primary_metric"],"aggregate_value":aggregate,"decision_met":decision,
        "batch_verdict":"PASS" if decision else "FAIL","research_only":True,"empirical_credit":"NONE","status":"REVIEWED",
    }


def synthetic_identity(batch_index,case_index,duplicate_across_batches=False):
    identity_batch=1 if duplicate_across_batches and batch_index>1 else batch_index
    return {
        "identity_namespace":"SYNTHETIC",
        "source_system":"FIXTURE",
        "source_record_id":f"REC-B{identity_batch:02d}-C{case_index:03d}",
        "sample_anchor":f"2026-09-{identity_batch:02d}T00:{case_index:02d}:00Z",
    }


def synthetic_sample_fingerprint(batch_index,case_index,duplicate_across_batches=False):
    policy=sample_policy();schema=identity_schema()
    return sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],synthetic_identity(batch_index,case_index,duplicate_across_batches),schema)


def make_batch(plan,index,n=12,candidate_wins=True,duplicate_case_tokens=False,duplicate_sample_fingerprints=False):
    batch=fx.batch(plan);batch["batch_id"]=f"K2PVB-BATCH_{index:03d}"
    prereg_day=1+(index-1)*3;batch["preregistered_at_utc"]=f"2026-09-{prereg_day:02d}T00:00:00Z";batch["planned_case_count"]=n
    sample=sample_policy();sample_sha=pv.canonical_sha256(sample);schema=identity_schema();schema_sha=sf.canonical_sha256(schema)
    freezes=[];outcomes=[];freeze_day=prereg_day+1;outcome_day=prereg_day+2
    for case_index in range(1,n+1):
        freeze=fx.freeze(plan,batch);freeze["freeze_id"]=f"K2PVF-B{index:02d}_CASE_{case_index:03d}"
        token_batch=1 if duplicate_case_tokens and index>1 else index;freeze["case_id"]=f"CASE_B{token_batch:02d}_{case_index:03d}"
        freeze["frozen_at_utc"]=f"2026-09-{freeze_day:02d}T00:{case_index:02d}:00Z";freeze["batch_sha256"]=pv.canonical_sha256(batch);freeze["model_commit_sha"]=batch["model_commit_sha"]
        payload=freeze["frozen_payload"]
        payload["sample_provenance_policy_version"]=sample["policy_version"];payload["sample_provenance_policy_sha256"]=sample_sha
        payload["sample_identity_schema_version"]=schema["schema_version"];payload["sample_identity_schema_sha256"]=schema_sha
        payload["sample_fingerprint_key_id"]=sample["fingerprint_key_id"];payload["sample_fingerprint"]=synthetic_sample_fingerprint(index,case_index,duplicate_sample_fingerprints)
        freeze["frozen_payload_sha256"]=pv.canonical_sha256(payload);freezes.append(freeze)
        outcome=fx.outcome(freeze);outcome["outcome_id"]=f"K2PVO-B{index:02d}_CASE_{case_index:03d}";outcome["observed_at_utc"]=f"2026-09-{outcome_day:02d}T00:{case_index:02d}:00Z"
        if candidate_wins:
            outcome["observed_value"]="EVENT_A";outcome["evaluation"]="SUCCESS";outcome["score_components"]={"CANDIDATE_SCORE":1.0,"COMPARATOR_SCORE":0.0,"PAIRED_SCORE_DELTA":1.0}
        else:
            outcome["observed_value"]="EVENT_B";outcome["evaluation"]="FAIL";outcome["score_components"]={"CANDIDATE_SCORE":0.0,"COMPARATOR_SCORE":1.0,"PAIRED_SCORE_DELTA":-1.0}
        outcomes.append(outcome)
    return batch,freezes,outcomes,make_batch_review(batch,freezes,outcomes,index)


def fixture(second_batch_wins=True,n=12,duplicate_case_tokens=False,duplicate_sample_fingerprints=False):
    plan=fx.plan();b1,f1,o1,r1=make_batch(plan,1,n=n,candidate_wins=True)
    b2,f2,o2,r2=make_batch(plan,2,n=n,candidate_wins=second_batch_wins,duplicate_case_tokens=duplicate_case_tokens,duplicate_sample_fingerprints=duplicate_sample_fingerprints)
    return plan,[b1,b2],f1+f2,o1+o2,[r1,r2]


def sample_binding(batch,index):
    sample=sample_policy();schema=identity_schema();prereg_day=1+(index-1)*3
    return {
        "binding_id":f"K2PVSPB-BATCH_{index:03d}","batch_id":batch["batch_id"],"batch_sha256":pv.canonical_sha256(batch),
        "bound_at_utc":f"2026-09-{prereg_day:02d}T12:00:00Z",
        "sample_provenance_policy_version":sample["policy_version"],"sample_provenance_policy_sha256":pv.canonical_sha256(sample),
        "sample_identity_schema_version":schema["schema_version"],"sample_identity_schema_sha256":sf.canonical_sha256(schema),
        "research_only":True,"status":"BOUND",
    }


def credit_review(plan,batches,freezes,outcomes,batch_reviews,readiness=None):
    policy=er.policy_for_batch(batches[0]);summary=er.compute_credit_summary(plan,batches,freezes,outcomes,batch_reviews,policy)
    return {
        "credit_review_id":"K2PVECR-H_TEST_001","policy_version":batches[0]["empirical_credit_policy_version"],"policy_sha256":batches[0]["empirical_credit_policy_sha256"],
        "sample_provenance_policy_version":summary["sample_provenance_policy_version"],"sample_provenance_policy_sha256":summary["sample_provenance_policy_sha256"],
        "sample_identity_schema_version":summary["sample_identity_schema_version"],"sample_identity_schema_sha256":summary["sample_identity_schema_sha256"],
        "sample_fingerprint_key_id":summary["sample_fingerprint_key_id"],"plan_id":plan["plan_id"],"hypothesis_id":plan["hypothesis_id"],
        "hypothesis_sha256":plan["hypothesis_sha256"],"hypothesis_context_sha256":plan["hypothesis_context_sha256"],"model_commit_sha":batches[0]["model_commit_sha"],
        "comparator_ref":batches[0]["comparator_ref"],"replication_contract_sha256":er.replication_contract_sha256(batches[0]),"reviewed_at_utc":"2026-09-10T00:00:00Z",
        "batch_review_ids":summary["batch_review_ids"],"batch_review_records_sha256":summary["batch_review_records_sha256"],"batch_count":summary["batch_count"],
        "total_case_count":summary["total_case_count"],"discordant_count":summary["discordant_count"],"candidate_win_count":summary["candidate_win_count"],
        "comparator_win_count":summary["comparator_win_count"],"tie_count":summary["tie_count"],"pooled_paired_delta":summary["pooled_paired_delta"],
        "one_sided_exact_pvalue":summary["one_sided_exact_pvalue"],"replication_consistent":summary["replication_consistent"],"case_token_unique":summary["case_token_unique"],
        "sample_provenance_consistent":summary["sample_provenance_consistent"],"sample_fingerprint_unique":summary["sample_fingerprint_unique"],
        "minimum_batch_count":policy["minimum_batch_count"],"minimum_discordant_count":policy["minimum_discordant_count"],"alpha":policy["alpha"],
        "credit_readiness":readiness or summary["credit_readiness"],"research_only":True,"empirical_credit":"NONE","status":"REVIEWED",
    }


def validate(plan,batches,freezes,outcomes,batch_reviews,credit_reviews):
    return er.validate_records(fx.distillates(),[plan],batches,freezes,outcomes,batch_reviews,credit_reviews)


def must_fail(plan,batches,freezes,outcomes,batch_reviews,credit_reviews,needle):
    issues=validate(plan,batches,freezes,outcomes,batch_reviews,credit_reviews);text="; ".join(f"{a}: {msg}" for a,msg in issues)
    assert issues,"expected failure";assert needle in text,(needle,text)


def test_identity_material_contract():
    policy=sample_policy();schema=identity_schema()
    left={"identity_namespace":"SYNTHETIC","source_system":"FIXTURE","source_record_id":" REC-001 ","sample_anchor":" 2026-09-01T00:00:00Z "}
    right={"identity_namespace":"SYNTHETIC","source_system":"FIXTURE","source_record_id":"REC-001","sample_anchor":"2026-09-01T00:00:00Z"}
    assert sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],left,schema)==sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],right,schema)
    extra=dict(right);extra["post_hoc_identity_field"]="FREE_DEGREE"
    try:sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],extra,schema)
    except ValueError:pass
    else:raise AssertionError("expected arbitrary sample identity fields to be rejected")
    missing=dict(right);missing.pop("sample_anchor")
    try:sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],missing,schema)
    except ValueError:pass
    else:raise AssertionError("expected missing sample identity field to be rejected")


def test_sample_provenance_contract(plan,batches,freezes):
    policy=sample_policy();schema=identity_schema();bindings=[sample_binding(batches[0],1),sample_binding(batches[1],2)]
    issues=sp.validate_records(batches,freezes,bindings,[policy],[schema]);assert not issues,issues
    bad=copy.deepcopy(bindings);bad[0]["sample_provenance_policy_sha256"]="0"*64
    text="; ".join(msg for _,msg in sp.validate_records(batches,freezes,bad,[policy],[schema]));assert "does not bind exact registered sample provenance policy" in text,text
    bad=copy.deepcopy(bindings);bad[0]["sample_identity_schema_sha256"]="0"*64
    text="; ".join(msg for _,msg in sp.validate_records(batches,freezes,bad,[policy],[schema]));assert "does not bind exact registered sample identity schema" in text,text
    bad=copy.deepcopy(bindings);bad[0]["bound_at_utc"]=freezes[0]["frozen_at_utc"]
    text="; ".join(msg for _,msg in sp.validate_records(batches,freezes,bad,[policy],[schema]));assert "before first case freeze" in text,text
    bad_freezes=copy.deepcopy(freezes);bad_freezes[0]["frozen_payload"].pop("sample_fingerprint");bad_freezes[0]["frozen_payload_sha256"]=pv.canonical_sha256(bad_freezes[0]["frozen_payload"])
    text="; ".join(msg for _,msg in sp.validate_records(batches,bad_freezes,bindings,[policy],[schema]));assert "sample_fingerprint must be lowercase 64-char HMAC digest" in text,text
    bad_freezes=copy.deepcopy(freezes);bad_freezes[0]["frozen_payload"]["sample_identity_schema_version"]="SAMPLE_IDENTITY_V999";bad_freezes[0]["frozen_payload_sha256"]=pv.canonical_sha256(bad_freezes[0]["frozen_payload"])
    text="; ".join(msg for _,msg in sp.validate_records(batches,bad_freezes,bindings,[policy],[schema]));assert "sample_identity_schema_version must match preregistered binding" in text,text
    bad_freezes=copy.deepcopy(freezes);bad_freezes[0]["frozen_payload"]["sample_identity_material"]={"name":"DO_NOT_STORE"};bad_freezes[0]["frozen_payload_sha256"]=pv.canonical_sha256(bad_freezes[0]["frozen_payload"])
    text="; ".join(msg for _,msg in sp.validate_records(batches,bad_freezes,bindings,[policy],[schema]));assert "raw identity/secret material forbidden" in text,text
    same=synthetic_identity(1,1);fp1=sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],same,schema);fp2=sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],copy.deepcopy(same),schema)
    fp3=sf.compute_fingerprint(SYNTHETIC_SECRET,policy["fingerprint_key_id"],synthetic_identity(1,2),schema);assert fp1==fp2 and fp1!=fp3 and len(fp1)==64


def main():
    test_identity_material_contract()
    p0=fx.plan();b0=fx.batch(p0);b0.pop("empirical_credit_policy_version");b0.pop("empirical_credit_policy_sha256")
    issues0=pv.validate_records(fx.distillates(),[p0],[b0],[],[]);text0="; ".join(f"{a}: {msg}" for a,msg in issues0)
    assert issues0 and "empirical_credit_policy" in text0,text0

    plan,batches,freezes,outcomes,batch_reviews=fixture(second_batch_wins=True,n=12);test_sample_provenance_contract(plan,batches,freezes)
    row=credit_review(plan,batches,freezes,outcomes,batch_reviews);assert row["credit_readiness"]=="READY_FOR_MANUAL_EMPIRICAL_REVIEW",row
    assert row["sample_provenance_consistent"] is True and row["sample_fingerprint_unique"] is True,row
    assert not validate(plan,batches,freezes,outcomes,batch_reviews,[row]),validate(plan,batches,freezes,outcomes,batch_reviews,[row])

    dupfp_plan,dupfp_batches,dupfp_freezes,dupfp_outcomes,dupfp_reviews=fixture(second_batch_wins=True,n=12,duplicate_sample_fingerprints=True)
    dupfp_row=credit_review(dupfp_plan,dupfp_batches,dupfp_freezes,dupfp_outcomes,dupfp_reviews)
    assert dupfp_row["case_token_unique"] is True and dupfp_row["sample_fingerprint_unique"] is False,dupfp_row
    assert dupfp_row["credit_readiness"]=="NOT_ELIGIBLE";assert not validate(dupfp_plan,dupfp_batches,dupfp_freezes,dupfp_outcomes,dupfp_reviews,[dupfp_row])
    bad=copy.deepcopy(dupfp_row);bad["credit_readiness"]="READY_FOR_MANUAL_EMPIRICAL_REVIEW";must_fail(dupfp_plan,dupfp_batches,dupfp_freezes,dupfp_outcomes,dupfp_reviews,[bad],"credit_readiness does not match machine policy")

    losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews=fixture(second_batch_wins=False,n=12);losing_row=credit_review(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews)
    assert losing_row["credit_readiness"]=="NOT_ELIGIBLE";assert not validate(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews,[losing_row])
    bad=copy.deepcopy(losing_row);bad["credit_readiness"]="READY_FOR_MANUAL_EMPIRICAL_REVIEW";must_fail(losing_plan,losing_batches,losing_freezes,losing_outcomes,losing_reviews,[bad],"credit_readiness does not match machine policy")

    bad=copy.deepcopy(row);bad["policy_sha256"]="0"*64;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"policy_sha256 does not bind exact registered empirical-credit policy")
    bad=copy.deepcopy(row);bad["sample_provenance_policy_sha256"]="0"*64;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"sample_provenance_policy_sha256")
    bad=copy.deepcopy(row);bad["sample_identity_schema_sha256"]="0"*64;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"sample_identity_schema_sha256")
    bad=copy.deepcopy(row);bad["batch_review_ids"]=bad["batch_review_ids"][:1];must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"batch_review_ids must bind the complete replication cohort")
    bad=copy.deepcopy(row);bad["batch_review_records_sha256"]="0"*64;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"batch_review_records_sha256 does not bind exact cohort reviews")
    bad=copy.deepcopy(row);bad["one_sided_exact_pvalue"]=0.5;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"one_sided_exact_pvalue does not match machine recomputation")

    small_plan,small_batches,small_freezes,small_outcomes,small_reviews=fixture(second_batch_wins=True,n=5);small_row=credit_review(small_plan,small_batches,small_freezes,small_outcomes,small_reviews)
    assert small_row["credit_readiness"]=="NOT_ELIGIBLE";assert not validate(small_plan,small_batches,small_freezes,small_outcomes,small_reviews,[small_row])
    dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews=fixture(second_batch_wins=True,n=12,duplicate_case_tokens=True);dup_row=credit_review(dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews)
    assert dup_row["credit_readiness"]=="NOT_ELIGIBLE";assert not validate(dup_plan,dup_batches,dup_freezes,dup_outcomes,dup_reviews,[dup_row])

    bad=copy.deepcopy(row);bad["empirical_credit"]="WEAK";must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"empirical credit review cannot upgrade empirical_credit")
    bad=copy.deepcopy(row);bad["reviewed_at_utc"]="2026-09-03T00:00:00Z";must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"empirical credit review must occur after all cohort batch reviews")
    bad=copy.deepcopy(row);bad["replication_contract_sha256"]="f"*64;must_fail(plan,batches,freezes,outcomes,batch_reviews,[bad],"replication_contract_sha256 does not identify a governed cohort")

    print("k2-empirical-credit-review-tests: PASS");print("cases=25")


if __name__=="__main__":main()
