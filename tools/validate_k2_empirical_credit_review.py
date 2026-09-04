#!/usr/bin/env python3
import json,math,re,sys
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_prospective_validation as pv
import validate_k2_prospective_batch_review as br

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"

DEFAULT_POLICY_VERSION="EMPIRICAL_CREDIT_REVIEW_V1"
READINESS_VALUES={"NOT_ELIGIBLE",pv.READINESS_CEILING}
REVIEW_FIELDS={
    "credit_review_id","policy_version","policy_sha256","plan_id","hypothesis_id","hypothesis_sha256",
    "hypothesis_context_sha256","model_commit_sha","comparator_ref","replication_contract_sha256",
    "reviewed_at_utc","batch_review_ids","batch_review_records_sha256","batch_count",
    "total_case_count","discordant_count","candidate_win_count","comparator_win_count","tie_count",
    "pooled_paired_delta","one_sided_exact_pvalue","replication_consistent","case_token_unique",
    "minimum_batch_count","minimum_discordant_count","alpha","credit_readiness",
    "research_only","empirical_credit","status",
}
CREDIT_REVIEW_ID_RE=re.compile(r"^K2PVECR-[A-Z0-9_-]+$")
SHA64_RE=re.compile(r"^[0-9a-f]{64}$")
SHA40_RE=re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print(f"k2-empirical-credit-review: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


def canonical_sha256(value):
    return pv.canonical_sha256(value)


def load_policy_index(policies=None):
    rows=pv.load_empirical_credit_policies(ROOT) if policies is None else policies
    index,issues=pv.empirical_credit_policy_index(rows)
    return rows,index,issues


def default_policy():
    _,index,issues=load_policy_index()
    if issues:fail(f"invalid empirical credit policy registry: {issues[0][0]}: {issues[0][1]}")
    policy=index.get(DEFAULT_POLICY_VERSION)
    if not policy:fail(f"missing default empirical credit policy: {DEFAULT_POLICY_VERSION}")
    return policy


_DEFAULT_POLICY=default_policy()
POLICY_VERSION=DEFAULT_POLICY_VERSION
MIN_BATCH_COUNT=_DEFAULT_POLICY["minimum_batch_count"]
MIN_DISCORDANT_COUNT=_DEFAULT_POLICY["minimum_discordant_count"]
ALPHA=_DEFAULT_POLICY["alpha"]


def policy_for_batch(batch,policies=None):
    _,index,issues=load_policy_index(policies)
    if issues:return None
    version=batch.get("empirical_credit_policy_version") if isinstance(batch,dict) else None
    policy=index.get(version)
    if not policy:return None
    if batch.get("empirical_credit_policy_sha256")!=canonical_sha256(policy):return None
    return policy


def replication_contract_sha256(batch):
    governed={
        "plan_id":batch.get("plan_id"),
        "plan_sha256":batch.get("plan_sha256"),
        "model_commit_sha":batch.get("model_commit_sha"),
        "comparator_ref":batch.get("comparator_ref"),
        "empirical_credit_policy_version":batch.get("empirical_credit_policy_version"),
        "empirical_credit_policy_sha256":batch.get("empirical_credit_policy_sha256"),
        "planned_case_count":batch.get("planned_case_count"),
        "sampling_rule":batch.get("sampling_rule"),
        "primary_metric":batch.get("primary_metric"),
        "primary_metric_spec":batch.get("primary_metric_spec"),
        "decision_rule":batch.get("decision_rule"),
        "secondary_metrics":batch.get("secondary_metrics"),
        "stopping_rule":batch.get("stopping_rule"),
        "exclusion_rule":batch.get("exclusion_rule"),
        "duplicate_case_policy":batch.get("duplicate_case_policy"),
        "research_only":batch.get("research_only"),
    }
    return canonical_sha256(governed)


def canonical_batch_review_records_sha256(reviews):
    ordered=sorted(reviews,key=lambda row:row.get("review_id") or "")
    return canonical_sha256(ordered)


def utc_value(v):
    if not isinstance(v,str) or not pv.UTC_RE.match(v):return None
    return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def finite_number(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)


def exact_one_sided_binomial_pvalue(candidate_wins,comparator_wins):
    n=candidate_wins+comparator_wins
    if n<=0:return None
    numerator=sum(math.comb(n,k) for k in range(candidate_wins,n+1))
    return numerator/(2**n)


def compute_credit_summary(plan,batches,freezes,outcomes,batch_reviews,policy=None):
    policy=policy or (policy_for_batch(batches[0]) if batches else None)
    if policy is None:
        return {
            "batch_review_ids":sorted(r.get("review_id") for r in batch_reviews),
            "batch_review_records_sha256":canonical_batch_review_records_sha256(batch_reviews),
            "batch_count":len(batch_reviews),"total_case_count":0,"discordant_count":0,
            "candidate_win_count":0,"comparator_win_count":0,"tie_count":0,
            "pooled_paired_delta":None,"one_sided_exact_pvalue":None,
            "replication_consistent":False,"case_token_unique":False,"credit_readiness":"NOT_ELIGIBLE",
        }
    batch_ids={b.get("batch_id") for b in batches}
    selected_freezes=[f for f in freezes if f.get("batch_id") in batch_ids]
    freeze_by_id={f.get("freeze_id"):f for f in selected_freezes}
    selected_outcomes=[o for o in outcomes if o.get("freeze_id") in freeze_by_id]

    candidate_wins=0;comparator_wins=0;ties=0;deltas=[]
    complete_scores=True
    batch_by_id={b.get("batch_id"):b for b in batches}
    for o in selected_outcomes:
        f=freeze_by_id.get(o.get("freeze_id"))
        b=batch_by_id.get(f.get("batch_id")) if f else None
        scores=pv.paired_exact_match_scores(b,f,o) if b and f else None
        if not scores:
            complete_scores=False
            continue
        delta=scores[pv.PAIRED_PRIMARY_METRIC]
        deltas.append(delta)
        if delta>0:candidate_wins+=1
        elif delta<0:comparator_wins+=1
        else:ties+=1

    total_case_count=len(selected_freezes)
    discordant=candidate_wins+comparator_wins
    pooled=(sum(deltas)/total_case_count) if total_case_count>0 and len(deltas)==total_case_count else None
    pvalue=exact_one_sided_binomial_pvalue(candidate_wins,comparator_wins) if complete_scores and discordant>0 else None
    review_passes=all(r.get("batch_verdict")=="PASS" for r in batch_reviews)
    positive_effects=all(finite_number(r.get("aggregate_value")) and r.get("aggregate_value")>0 for r in batch_reviews)
    replication_consistent=bool(batch_reviews)
    if policy.get("require_all_batch_reviews_pass"):replication_consistent=replication_consistent and review_passes
    if policy.get("require_positive_batch_aggregate"):replication_consistent=replication_consistent and positive_effects
    case_ids=[f.get("case_id") for f in selected_freezes]
    case_token_unique=len(case_ids)==len(set(case_ids)) and all(isinstance(x,str) and bool(x) for x in case_ids)
    ready=(
        len(batch_reviews)>=policy["minimum_batch_count"]
        and len(batch_reviews)==len(batches)
        and complete_scores
        and len(selected_outcomes)==total_case_count
        and replication_consistent
        and (case_token_unique or not policy.get("require_unique_case_tokens"))
        and discordant>=policy["minimum_discordant_count"]
        and (candidate_wins>comparator_wins or not policy.get("require_candidate_wins_gt_comparator_wins"))
        and (pooled is not None and pooled>0 if policy.get("require_positive_pooled_paired_delta") else pooled is not None)
        and pvalue is not None and pvalue<=policy["alpha"]
    )
    return {
        "batch_review_ids":sorted(r.get("review_id") for r in batch_reviews),
        "batch_review_records_sha256":canonical_batch_review_records_sha256(batch_reviews),
        "batch_count":len(batch_reviews),
        "total_case_count":total_case_count,
        "discordant_count":discordant,
        "candidate_win_count":candidate_wins,
        "comparator_win_count":comparator_wins,
        "tie_count":ties,
        "pooled_paired_delta":pooled,
        "one_sided_exact_pvalue":pvalue,
        "replication_consistent":replication_consistent,
        "case_token_unique":case_token_unique,
        "credit_readiness":policy["readiness_ceiling"] if ready else "NOT_ELIGIBLE",
    }


def values_match(actual,expected):
    if expected is None:return actual is None
    if isinstance(expected,float):
        return finite_number(actual) and math.isclose(actual,expected,rel_tol=0.0,abs_tol=1e-15)
    return actual==expected


def validate_records(distillates,plans,batches,freezes,outcomes,batch_reviews,credit_reviews,empirical_credit_policies=None):
    issues=[]
    policies,policy_by_version,policy_issues=load_policy_index(empirical_credit_policies)
    issues.extend(policy_issues)
    upstream=pv.validate_records(distillates,plans,batches,freezes,outcomes,policies)
    if upstream:
        issues.extend(("UPSTREAM_PROSPECTIVE",f"upstream prospective contract invalid: {rid}: {msg}") for rid,msg in upstream)
        return issues
    upstream_batch=br.validate_records(distillates,plans,batches,freezes,outcomes,batch_reviews)
    if upstream_batch:
        issues.extend(("UPSTREAM_BATCH_REVIEW",f"upstream batch review invalid: {rid}: {msg}") for rid,msg in upstream_batch)
        return issues

    plan_by_id={p.get("plan_id"):p for p in plans}
    review_by_batch={r.get("batch_id"):r for r in batch_reviews}
    seen_ids=set();seen_cohorts=set()

    for r in credit_reviews:
        rid=r.get("credit_review_id") or "<missing>"
        if set(r)!=REVIEW_FIELDS:
            issues.append((rid,f"credit review fields mismatch missing={sorted(REVIEW_FIELDS-set(r))} extra={sorted(set(r)-REVIEW_FIELDS)}"))
        if not isinstance(rid,str) or not CREDIT_REVIEW_ID_RE.match(rid):issues.append((rid,"invalid credit_review_id"))
        if rid in seen_ids:issues.append((rid,"duplicate credit_review_id"))
        seen_ids.add(rid)

        policy_version=r.get("policy_version")
        policy_sha=r.get("policy_sha256")
        policy=policy_by_version.get(policy_version)
        if not pv.nonempty_text(policy_version):issues.append((rid,"policy_version must be non-empty text"))
        elif policy is None:issues.append((rid,f"unknown policy_version: {policy_version}"))
        if not isinstance(policy_sha,str) or not SHA64_RE.match(policy_sha):issues.append((rid,"policy_sha256 must be lowercase sha256"))
        elif policy is not None and policy_sha!=canonical_sha256(policy):issues.append((rid,"policy_sha256 does not bind exact registered empirical-credit policy"))

        pid=r.get("plan_id");plan=plan_by_id.get(pid)
        if not plan:
            issues.append((rid,f"unknown plan_id: {pid}"))
            continue
        for field in ["hypothesis_id","hypothesis_sha256","hypothesis_context_sha256"]:
            if r.get(field)!=plan.get(field):issues.append((rid,f"{field} must match exact governed plan"))
        if not isinstance(r.get("hypothesis_sha256"),str) or not SHA64_RE.match(r.get("hypothesis_sha256","")):issues.append((rid,"hypothesis_sha256 must be lowercase sha256"))
        if not isinstance(r.get("hypothesis_context_sha256"),str) or not SHA64_RE.match(r.get("hypothesis_context_sha256","")):issues.append((rid,"hypothesis_context_sha256 must be lowercase sha256"))
        if not isinstance(r.get("model_commit_sha"),str) or not SHA40_RE.match(r.get("model_commit_sha","")):issues.append((rid,"model_commit_sha must be lowercase 40-char git SHA"))
        if not isinstance(r.get("comparator_ref"),str) or not r.get("comparator_ref","").strip():issues.append((rid,"comparator_ref must be non-empty text"))

        contract_sha=r.get("replication_contract_sha256")
        if not isinstance(contract_sha,str) or not SHA64_RE.match(contract_sha):issues.append((rid,"replication_contract_sha256 must be lowercase sha256"))
        cohort=[b for b in batches if b.get("plan_id")==pid and b.get("model_commit_sha")==r.get("model_commit_sha") and b.get("comparator_ref")==r.get("comparator_ref") and b.get("empirical_credit_policy_version")==policy_version and b.get("empirical_credit_policy_sha256")==policy_sha and replication_contract_sha256(b)==contract_sha]
        cohort_key=(pid,r.get("model_commit_sha"),r.get("comparator_ref"),policy_version,policy_sha,contract_sha)
        if cohort_key in seen_cohorts:issues.append((rid,"a governed replication cohort may have only one active credit review"))
        seen_cohorts.add(cohort_key)
        if not cohort:
            issues.append((rid,"replication_contract_sha256 does not identify a governed cohort"))
            continue

        if policy is None:
            issues.append((rid,"credit review cannot evaluate cohort without registered policy"))
            continue
        expected_policy_sha=canonical_sha256(policy)
        if any(b.get("empirical_credit_policy_version")!=policy_version or b.get("empirical_credit_policy_sha256")!=expected_policy_sha for b in cohort):issues.append((rid,"replication cohort policy binding is inconsistent"))

        cohort_batch_ids={b.get("batch_id") for b in cohort}
        cohort_reviews=[review_by_batch.get(bid) for bid in cohort_batch_ids if review_by_batch.get(bid)]
        if len(cohort_reviews)!=len(cohort):issues.append((rid,"replication cohort contains batches without batch review"))
        expected_review_ids=sorted(x.get("review_id") for x in cohort_reviews)
        if r.get("batch_review_ids")!=expected_review_ids:issues.append((rid,"batch_review_ids must bind the complete replication cohort"))
        expected_review_sha=canonical_batch_review_records_sha256(cohort_reviews)
        if r.get("batch_review_records_sha256")!=expected_review_sha:issues.append((rid,"batch_review_records_sha256 does not bind exact cohort reviews"))
        if not isinstance(r.get("batch_review_records_sha256"),str) or not SHA64_RE.match(r.get("batch_review_records_sha256","")):issues.append((rid,"batch_review_records_sha256 must be lowercase sha256"))

        selected_freezes=[f for f in freezes if f.get("batch_id") in cohort_batch_ids]
        selected_freeze_ids={f.get("freeze_id") for f in selected_freezes}
        selected_outcomes=[o for o in outcomes if o.get("freeze_id") in selected_freeze_ids]
        summary=compute_credit_summary(plan,cohort,selected_freezes,selected_outcomes,cohort_reviews,policy)
        for field in ["batch_count","total_case_count","discordant_count","candidate_win_count","comparator_win_count","tie_count","replication_consistent","case_token_unique","credit_readiness"]:
            if r.get(field)!=summary[field]:issues.append((rid,f"{field} does not match machine recomputation" if field!="credit_readiness" else "credit_readiness does not match machine policy"))
        if not values_match(r.get("pooled_paired_delta"),summary["pooled_paired_delta"]):issues.append((rid,"pooled_paired_delta does not match machine recomputation"))
        if not values_match(r.get("one_sided_exact_pvalue"),summary["one_sided_exact_pvalue"]):issues.append((rid,"one_sided_exact_pvalue does not match machine recomputation"))

        if r.get("minimum_batch_count")!=policy["minimum_batch_count"]:issues.append((rid,f"minimum_batch_count must equal preregistered policy value {policy['minimum_batch_count']}"))
        if r.get("minimum_discordant_count")!=policy["minimum_discordant_count"]:issues.append((rid,f"minimum_discordant_count must equal preregistered policy value {policy['minimum_discordant_count']}"))
        if not finite_number(r.get("alpha")) or r.get("alpha")!=policy["alpha"]:issues.append((rid,f"alpha must equal preregistered policy value {policy['alpha']}"))
        if r.get("credit_readiness") not in READINESS_VALUES:issues.append((rid,"invalid credit_readiness"))
        if r.get("credit_readiness")==pv.READINESS_CEILING and policy.get("readiness_ceiling")!=pv.READINESS_CEILING:issues.append((rid,"credit_readiness exceeds preregistered policy ceiling"))

        review_dt=utc_value(r.get("reviewed_at_utc"))
        if review_dt is None:
            issues.append((rid,"reviewed_at_utc must be UTC second timestamp ending Z"))
        else:
            batch_review_times=[utc_value(x.get("reviewed_at_utc")) for x in cohort_reviews]
            batch_review_times=[x for x in batch_review_times if x]
            if batch_review_times and review_dt<=max(batch_review_times):issues.append((rid,"empirical credit review must occur after all cohort batch reviews"))

        if r.get("research_only") is not True:issues.append((rid,"empirical credit review must be research_only=true"))
        if r.get("empirical_credit")!="NONE":issues.append((rid,"empirical credit review cannot upgrade empirical_credit"))
        if r.get("status")!="REVIEWED":issues.append((rid,"empirical credit review status must be REVIEWED"))
        if pv.PATH_RE.search(json.dumps(r,ensure_ascii=False)):issues.append((rid,"empirical credit review leaks local filesystem path"))
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
    batch_reviews=pv.load_jsonl(K/"K2_PROSPECTIVE_BATCH_REVIEWS.jsonl")
    credit_reviews=pv.load_jsonl(K/"K2_PROSPECTIVE_EMPIRICAL_CREDIT_REVIEWS.jsonl")
    policies=pv.load_empirical_credit_policies(ROOT)
    issues=validate_records(distillates,plans,batches,freezes,outcomes,batch_reviews,credit_reviews,policies)
    if issues:fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")
    ready=sum(r.get("credit_readiness")==pv.READINESS_CEILING for r in credit_reviews)
    print("k2-empirical-credit-review: PASS")
    print(f"policies={len(policies)} credit_reviews={len(credit_reviews)} ready_for_manual_review={ready} issues=0")
    print("empirical_credit_upgrade_blocked=true")

if __name__=="__main__":main()
