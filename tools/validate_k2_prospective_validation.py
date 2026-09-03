#!/usr/bin/env python3
import hashlib,json,re,sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"

PLAN_FIELDS={
    "plan_id","hypothesis_id","hypothesis_sha256","hypothesis_context_sha256","work_family_key","model_name","comparator_name",
    "question_scope","unit_of_analysis","freeze_required_fields","evaluation_metrics",
    "success_condition","failure_condition","abstention_rule","leakage_controls",
    "high_risk_policy","update_policy","status","empirical_credit",
}
BATCH_FIELDS={
    "batch_id","plan_id","plan_sha256","preregistered_at_utc","model_commit_sha","comparator_ref",
    "planned_case_count","sampling_rule","primary_metric","decision_rule",
    "secondary_metrics","stopping_rule","exclusion_rule","duplicate_case_policy",
    "research_only","status","empirical_credit",
}
FREEZE_FIELDS={
    "freeze_id","plan_id","batch_id","batch_sha256","case_id","frozen_at_utc","model_commit_sha",
    "frozen_payload","frozen_payload_sha256","outcome_known_at_freeze",
    "research_only","status",
}
OUTCOME_FIELDS={
    "outcome_id","freeze_id","freeze_record_sha256","observed_at_utc","freeze_payload_sha256",
    "outcome_summary","evaluation","score_components","post_hoc_notes",
    "research_only","empirical_credit","status",
}
MANDATORY_FREEZE_FIELDS={
    "question_definition","asked_object","object_graph","role_map","eligible_rule_set",
    "primary_layers","boundary_conditions","interpretation_path","prediction",
    "confidence","abstention_condition",
}
EVALUATIONS={"SUCCESS","PARTIAL","FAIL","ABSTAIN","UNEVALUABLE"}
PLAN_ID_RE=re.compile(r"^K2PV-[A-Z0-9-]+$")
BATCH_ID_RE=re.compile(r"^K2PVB-[A-Z0-9_-]+$")
FREEZE_ID_RE=re.compile(r"^K2PVF-[A-Z0-9_-]+$")
OUTCOME_ID_RE=re.compile(r"^K2PVO-[A-Z0-9_-]+$")
CASE_ID_RE=re.compile(r"^[A-Z0-9_-]+$")
SHA40_RE=re.compile(r"^[0-9a-f]{40}$")
SHA64_RE=re.compile(r"^[0-9a-f]{64}$")
UTC_RE=re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(msg):
    print(f"k2-prospective-validation: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    if not path.exists():return []
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows


def load_work_family_distillates(root=ROOT):
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    import validate_k2_work_family_distillates as wf
    return wf.load_distillates(root)


def canonical_sha256(value):
    blob=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def nonempty_text(v):
    return isinstance(v,str) and bool(v.strip())


def string_list(v,allow_empty=False):
    return isinstance(v,list) and (allow_empty or bool(v)) and all(nonempty_text(x) for x in v)


def utc_value(v):
    if not isinstance(v,str) or not UTC_RE.match(v):return None
    return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def effective_domain_routes(distillate):
    declared=distillate.get("domain_routes")
    if isinstance(declared,list) and declared:
        return list(declared)
    domain=distillate.get("domain")
    return [domain] if nonempty_text(domain) else []


def hypothesis_context_sha256(work_family_key,domain_routes,hypothesis):
    return canonical_sha256({
        "work_family_key":work_family_key,
        "domain_routes":list(domain_routes),
        "hypothesis":hypothesis,
    })


def hypothesis_index(distillates):
    out={}
    for d in distillates:
        wf=d.get("work_family_key");routes=effective_domain_routes(d)
        for h in d.get("testable_hypotheses") or []:
            if not isinstance(h,dict):continue
            hid=h.get("hypothesis_id")
            if not nonempty_text(hid):continue
            if hid in out:
                fail(f"duplicate hypothesis_id in work-family distillates: {hid}")
            out[hid]={
                "work_family_key":wf,
                "status":h.get("status"),
                "domain_routes":routes,
                "hypothesis_sha256":canonical_sha256(h),
                "hypothesis_context_sha256":hypothesis_context_sha256(wf,routes,h),
            }
    return out


def validate_records(distillates,plans,batches,freezes,outcomes):
    issues=[];hyps=hypothesis_index(distillates)
    plan_by_id={};plan_routes_by_id={};seen_hyp=set()
    for p in plans:
        pid=p.get("plan_id") or "<missing>";hid=p.get("hypothesis_id")
        if set(p)!=PLAN_FIELDS:issues.append((pid,f"plan fields mismatch missing={sorted(PLAN_FIELDS-set(p))} extra={sorted(set(p)-PLAN_FIELDS)}"))
        if not isinstance(pid,str) or not PLAN_ID_RE.match(pid):issues.append((pid,"invalid plan_id"))
        if pid in plan_by_id:issues.append((pid,"duplicate plan_id"))
        plan_by_id[pid]=p
        if hid in seen_hyp:issues.append((pid,"one hypothesis may have only one active design plan"))
        seen_hyp.add(hid)
        h=hyps.get(hid);routes=[]
        hsha=p.get("hypothesis_sha256")
        hcsha=p.get("hypothesis_context_sha256")
        if not isinstance(hsha,str) or not SHA64_RE.match(hsha):
            issues.append((pid,"hypothesis_sha256 must be lowercase sha256"))
        if not isinstance(hcsha,str) or not SHA64_RE.match(hcsha):
            issues.append((pid,"hypothesis_context_sha256 must be lowercase sha256"))
        if not h:issues.append((pid,f"unknown hypothesis_id: {hid}"))
        else:
            routes=h.get("domain_routes") or []
            if p.get("work_family_key")!=h.get("work_family_key"):issues.append((pid,"work_family_key does not match hypothesis source"))
            if h.get("status")!="UNTESTED":issues.append((pid,"prospective design currently requires UNTESTED hypothesis"))
            if hsha!=h.get("hypothesis_sha256"):issues.append((pid,"hypothesis_sha256 does not bind exact hypothesis content"))
            if hcsha!=h.get("hypothesis_context_sha256"):issues.append((pid,"hypothesis_context_sha256 does not bind exact governed hypothesis context"))
        plan_routes_by_id[pid]=routes
        for field in ["model_name","comparator_name","question_scope","unit_of_analysis","success_condition","failure_condition","abstention_rule","high_risk_policy","update_policy"]:
            if not nonempty_text(p.get(field)):issues.append((pid,f"{field} must be non-empty text"))
        if p.get("model_name")==p.get("comparator_name"):issues.append((pid,"candidate model and comparator must differ"))
        req=p.get("freeze_required_fields")
        if not string_list(req):issues.append((pid,"freeze_required_fields must be non-empty string array"))
        else:
            missing=MANDATORY_FREEZE_FIELDS-set(req)
            if missing:issues.append((pid,f"freeze_required_fields missing mandatory fields: {sorted(missing)}"))
            if len(routes)>1 and "active_domain_routes" not in req:
                issues.append((pid,"multi-domain hypothesis requires active_domain_routes in freeze_required_fields"))
            if len(req)!=len(set(req)):issues.append((pid,"duplicate freeze_required_fields"))
        if not string_list(p.get("evaluation_metrics")):issues.append((pid,"evaluation_metrics must be non-empty string array"))
        if not string_list(p.get("leakage_controls")):issues.append((pid,"leakage_controls must be non-empty string array"))
        if p.get("status")!="DESIGN_READY":issues.append((pid,"plan status must be DESIGN_READY"))
        if p.get("empirical_credit")!="NONE":issues.append((pid,"design plan cannot carry empirical credit"))
        if not str(p.get("high_risk_policy","")).startswith("RESEARCH_ONLY"):issues.append((pid,"high_risk_policy must be RESEARCH_ONLY"))
        if PATH_RE.search(json.dumps(p,ensure_ascii=False)):issues.append((pid,"plan leaks local filesystem path"))

    batch_by_id={}
    for b in batches:
        bid=b.get("batch_id") or "<missing>";pid=b.get("plan_id")
        if set(b)!=BATCH_FIELDS:issues.append((bid,f"batch fields mismatch missing={sorted(BATCH_FIELDS-set(b))} extra={sorted(set(b)-BATCH_FIELDS)}"))
        if not isinstance(bid,str) or not BATCH_ID_RE.match(bid):issues.append((bid,"invalid batch_id"))
        if bid in batch_by_id:issues.append((bid,"duplicate batch_id"))
        batch_by_id[bid]=b
        plan=plan_by_id.get(pid)
        if not plan:issues.append((bid,f"unknown plan_id: {pid}"))
        else:
            if b.get("plan_sha256")!=canonical_sha256(plan):issues.append((bid,"plan_sha256 does not bind exact test plan"))
        if not isinstance(b.get("plan_sha256"),str) or not SHA64_RE.match(b.get("plan_sha256","")):issues.append((bid,"plan_sha256 must be lowercase sha256"))
        if utc_value(b.get("preregistered_at_utc")) is None:issues.append((bid,"preregistered_at_utc must be UTC second timestamp ending Z"))
        if not isinstance(b.get("model_commit_sha"),str) or not SHA40_RE.match(b.get("model_commit_sha","")):issues.append((bid,"model_commit_sha must be lowercase 40-char git SHA"))
        for field in ["comparator_ref","sampling_rule","primary_metric","decision_rule","stopping_rule","exclusion_rule","duplicate_case_policy"]:
            if not nonempty_text(b.get(field)):issues.append((bid,f"{field} must be non-empty text"))
        count=b.get("planned_case_count")
        if not isinstance(count,int) or isinstance(count,bool) or count<1:issues.append((bid,"planned_case_count must be positive integer"))
        if not string_list(b.get("secondary_metrics"),allow_empty=True):issues.append((bid,"secondary_metrics must be string array"))
        if b.get("research_only") is not True:issues.append((bid,"batch must be research_only=true"))
        if b.get("status")!="PREREGISTERED":issues.append((bid,"batch status must be PREREGISTERED"))
        if b.get("empirical_credit")!="NONE":issues.append((bid,"preregistered batch cannot carry empirical credit"))
        if PATH_RE.search(json.dumps(b,ensure_ascii=False)):issues.append((bid,"batch leaks local filesystem path"))

    freeze_by_id={};case_keys=set()
    for f in freezes:
        fid=f.get("freeze_id") or "<missing>";pid=f.get("plan_id");bid=f.get("batch_id")
        if set(f)!=FREEZE_FIELDS:issues.append((fid,f"freeze fields mismatch missing={sorted(FREEZE_FIELDS-set(f))} extra={sorted(set(f)-FREEZE_FIELDS)}"))
        if not isinstance(fid,str) or not FREEZE_ID_RE.match(fid):issues.append((fid,"invalid freeze_id"))
        if fid in freeze_by_id:issues.append((fid,"duplicate freeze_id"))
        freeze_by_id[fid]=f
        plan=plan_by_id.get(pid)
        if not plan:issues.append((fid,f"unknown plan_id: {pid}"))
        batch=batch_by_id.get(bid)
        if not batch:issues.append((fid,f"freeze requires preregistered batch: {bid}"))
        else:
            if batch.get("plan_id")!=pid:issues.append((fid,"freeze plan_id does not match batch plan_id"))
            if f.get("batch_sha256")!=canonical_sha256(batch):issues.append((fid,"batch_sha256 does not bind exact preregistered batch"))
        if not isinstance(f.get("batch_sha256"),str) or not SHA64_RE.match(f.get("batch_sha256","")):issues.append((fid,"batch_sha256 must be lowercase sha256"))
        case_id=f.get("case_id")
        if not isinstance(case_id,str) or not CASE_ID_RE.match(case_id):issues.append((fid,"case_id must be anonymous uppercase token"))
        key=(bid,case_id)
        if key in case_keys:issues.append((fid,"duplicate case_id inside batch"))
        case_keys.add(key)
        fdt=utc_value(f.get("frozen_at_utc"))
        if fdt is None:issues.append((fid,"frozen_at_utc must be UTC second timestamp ending Z"))
        if batch:
            bdt=utc_value(batch.get("preregistered_at_utc"))
            if fdt and bdt and fdt<=bdt:issues.append((fid,"case freeze must occur after batch preregistration"))
            if f.get("model_commit_sha")!=batch.get("model_commit_sha"):issues.append((fid,"freeze model_commit_sha must equal batch preregistered model_commit_sha"))
        if not isinstance(f.get("model_commit_sha"),str) or not SHA40_RE.match(f.get("model_commit_sha","")):issues.append((fid,"model_commit_sha must be lowercase 40-char git SHA"))
        payload=f.get("frozen_payload")
        if not isinstance(payload,dict):issues.append((fid,"frozen_payload must be object"))
        else:
            if plan:
                missing=set(plan.get("freeze_required_fields") or [])-set(payload)
                if missing:issues.append((fid,f"frozen_payload missing plan fields: {sorted(missing)}"))
            routes=plan_routes_by_id.get(pid,[])
            active=payload.get("active_domain_routes")
            if len(routes)>1 or active is not None:
                if not string_list(active):
                    issues.append((fid,"active_domain_routes must be non-empty string array"))
                else:
                    if len(active)!=len(set(active)):issues.append((fid,"active_domain_routes must not contain duplicates"))
                    outside=[route for route in active if route not in routes]
                    if outside:issues.append((fid,f"active_domain_routes outside governed routes: {outside}"))
                    expected=[route for route in routes if route in active]
                    if not outside and active!=expected:
                        issues.append((fid,"active_domain_routes must preserve governed route order"))
            conf=payload.get("confidence")
            if not isinstance(conf,(int,float)) or isinstance(conf,bool) or not 0<=conf<=1:issues.append((fid,"confidence must be numeric in [0,1]"))
            if not nonempty_text(payload.get("prediction")):issues.append((fid,"prediction must be explicit non-empty text"))
            if not nonempty_text(payload.get("abstention_condition")):issues.append((fid,"abstention_condition must be explicit"))
            actual=canonical_sha256(payload)
            if f.get("frozen_payload_sha256")!=actual:issues.append((fid,"frozen_payload_sha256 mismatch"))
        if not isinstance(f.get("frozen_payload_sha256"),str) or not SHA64_RE.match(f.get("frozen_payload_sha256","")):issues.append((fid,"frozen_payload_sha256 must be lowercase sha256"))
        if f.get("outcome_known_at_freeze") is not False:issues.append((fid,"outcome_known_at_freeze must be false"))
        if f.get("research_only") is not True:issues.append((fid,"freeze must be research_only=true"))
        if f.get("status")!="FROZEN":issues.append((fid,"freeze status must be FROZEN"))
        if PATH_RE.search(json.dumps(f,ensure_ascii=False)):issues.append((fid,"freeze leaks local filesystem path"))

    seen_outcome=set();seen_freeze_outcome=set()
    for o in outcomes:
        oid=o.get("outcome_id") or "<missing>";fid=o.get("freeze_id")
        if set(o)!=OUTCOME_FIELDS:issues.append((oid,f"outcome fields mismatch missing={sorted(OUTCOME_FIELDS-set(o))} extra={sorted(set(o)-OUTCOME_FIELDS)}"))
        if not isinstance(oid,str) or not OUTCOME_ID_RE.match(oid):issues.append((oid,"invalid outcome_id"))
        if oid in seen_outcome:issues.append((oid,"duplicate outcome_id"))
        seen_outcome.add(oid)
        if fid in seen_freeze_outcome:issues.append((oid,"a freeze may have only one scored outcome row"))
        seen_freeze_outcome.add(fid)
        fr=freeze_by_id.get(fid)
        if not fr:issues.append((oid,f"unknown freeze_id: {fid}"))
        else:
            if o.get("freeze_record_sha256")!=canonical_sha256(fr):issues.append((oid,"freeze_record_sha256 does not bind exact freeze record"))
            if o.get("freeze_payload_sha256")!=fr.get("frozen_payload_sha256"):issues.append((oid,"outcome does not reference exact frozen payload hash"))
            fdt=utc_value(fr.get("frozen_at_utc"));odt=utc_value(o.get("observed_at_utc"))
            if fdt and odt and odt<=fdt:issues.append((oid,"outcome must be observed after freeze"))
        if not isinstance(o.get("freeze_record_sha256"),str) or not SHA64_RE.match(o.get("freeze_record_sha256","")):issues.append((oid,"freeze_record_sha256 must be lowercase sha256"))
        if utc_value(o.get("observed_at_utc")) is None:issues.append((oid,"observed_at_utc must be UTC second timestamp ending Z"))
        if not nonempty_text(o.get("outcome_summary")):issues.append((oid,"outcome_summary must be non-empty derived text"))
        if o.get("evaluation") not in EVALUATIONS:issues.append((oid,"invalid evaluation"))
        if not isinstance(o.get("score_components"),dict):issues.append((oid,"score_components must be object"))
        notes=o.get("post_hoc_notes")
        if not isinstance(notes,list) or any(not nonempty_text(x) for x in notes):issues.append((oid,"post_hoc_notes must be string array"))
        if o.get("research_only") is not True:issues.append((oid,"outcome must be research_only=true"))
        if o.get("empirical_credit")!="NONE":issues.append((oid,"single-case outcome cannot upgrade empirical credit"))
        if o.get("status")!="REVIEWED":issues.append((oid,"outcome status must be REVIEWED"))
        if PATH_RE.search(json.dumps(o,ensure_ascii=False)):issues.append((oid,"outcome leaks local filesystem path"))
    return issues


def main():
    project=load_json(K/"PROJECT_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked")
    distillates=load_work_family_distillates(ROOT)
    plans=load_jsonl(K/"K2_PROSPECTIVE_TEST_PLANS.jsonl")
    batches=load_jsonl(K/"K2_PROSPECTIVE_BATCHES.jsonl")
    freezes=load_jsonl(K/"K2_PROSPECTIVE_FREEZES.jsonl")
    outcomes=load_jsonl(K/"K2_PROSPECTIVE_OUTCOMES.jsonl")
    issues=validate_records(distillates,plans,batches,freezes,outcomes)
    if issues:
        fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")
    print("k2-prospective-validation: PASS")
    print(f"plans={len(plans)} batches={len(batches)} freezes={len(freezes)} outcomes={len(outcomes)} issues=0")
    print("empirical_credit_upgrade_blocked=true")

if __name__=="__main__":main()
