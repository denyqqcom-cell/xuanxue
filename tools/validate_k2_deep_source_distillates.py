#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_lineage_corrections as lc

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ALLOWED={"distillate_id","source_id","work_id","domain","distillation_scope","reading_ref","canonical_sha256","source_anchors","course_family_id","course_role","independence_policy","prior_distillate_refs","evidence_reaudit_coverage","source_credit","empirical_credit","essence","method_map","applicability_constraints","source_limitations","conflicts_and_tensions","anti_patterns","model_updates","testable_hypotheses","excluded_from_operational_use","claim_extraction_blocked","acceptance_status","distillation_status","review_status","copyright_class"}
LIST_FIELDS={"source_anchors","prior_distillate_refs","essence","method_map","applicability_constraints","source_limitations","conflicts_and_tensions","anti_patterns","model_updates","excluded_from_operational_use"}
NONEMPTY={"source_anchors","essence","method_map","source_limitations","model_updates"}
HYP_FIELDS={"hypothesis_id","statement","freeze_requirements","failure_condition","status"}
ANCHOR_RE=re.compile(r"^([A-Z]{2}-SRC-\d{4})@pdf:p(\d+)$")
DIST_RE=re.compile(r"^K2DS-[A-Z]{2}-SRC-\d{4}$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
COURSE_ROLES={"FOUNDATION","ADVANCED_EXTENSION","SYNOPSIS_COMPENDIUM","SIBLING_WORK","UNKNOWN"}


def fail(msg):
    print(f"k2-deep-source-distillates: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

def load_json(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:fail(f"cannot parse {path}: {e}")

def load_jsonl(path):
    rows=[]
    if not path.exists():return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows

def load_distillates(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_DEEP_SOURCE_DISTILLATES.jsonl")
    shard=root/"knowledge"/"K2_DEEP_SOURCE_DISTILLATES.d"
    if shard.exists():
        for p in sorted(shard.glob("*.jsonl")):rows.extend(load_jsonl(p))
    return rows

def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out

def prior_distillate_index(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_BOOK_DISTILLATES_WAVE1.jsonl")
    shard=root/"knowledge"/"K2_BOOK_DISTILLATES_WAVE1.d"
    if shard.exists():
        for p in sorted(shard.glob("*.jsonl")):rows.extend(load_jsonl(p))
    return {r.get("distillate_id"):r for r in rows}

def indexes(root=ROOT):
    k=root/"knowledge";sources=source_index(root)
    raw={r.get("source_id"):r for r in load_jsonl(k/"K2_SOURCE_LINEAGE.jsonl")}
    corrections=load_jsonl(k/"K2_LINEAGE_CORRECTIONS.jsonl")
    lineage=lc.effective_lineage_index(raw,corrections)
    readings={r.get("reading_id"):r for r in load_jsonl(k/"K2_DEEP_READING_LEDGER.jsonl")}
    courses={r.get("source_id"):r for r in load_jsonl(k/"K2_COURSE_LINEAGE.jsonl")}
    family_sources={r.get("source_id") for r in load_jsonl(k/"K2_SEGMENT_LINEAGE.jsonl")}
    prior=prior_distillate_index(root);reaudit={}
    state_path=k/"K2_EVIDENCE_REAUDIT_STATE.json"
    if state_path.exists():
        state=load_json(state_path);reaudit={t.get("source_id"):t.get("coverage") for t in state.get("targets") or []}
    return sources,lineage,readings,courses,family_sources,prior,reaudit

def inspect(row,idx):
    sources,lineage,readings,courses,family_sources,prior,reaudit=idx
    did=row.get("distillate_id") or "<missing>";sid=row.get("source_id") or "<missing>";issues=[]
    if not isinstance(did,str) or not DIST_RE.match(did):issues.append((did,"invalid distillate_id"))
    extra=set(row)-ALLOWED
    if extra:issues.append((did,f"unexpected fields: {sorted(extra)}"))
    src=sources.get(sid);lin=lineage.get(sid);reading=readings.get(row.get("reading_ref"))
    if not src:issues.append((did,"unknown source_id"));return issues
    if sid in family_sources:issues.append((did,"source is already governed by work-family distillation; deep-source lane would duplicate credit"))
    if not lin or row.get("work_id")!=lin.get("work_id"):issues.append((did,"work_id mismatch with effective source lineage"))
    if row.get("domain")!=src.get("domain"):issues.append((did,"domain mismatch"))
    if row.get("canonical_sha256")!=src.get("file_sha256"):issues.append((did,"canonical_sha256 mismatch"))
    if not reading:issues.append((did,"unknown reading_ref"))
    else:
        if reading.get("source_id")!=sid:issues.append((did,"reading_ref source mismatch"))
        if reading.get("canonical_sha256")!=row.get("canonical_sha256"):issues.append((did,"reading/source SHA mismatch"))
        if reading.get("read_status")!="COMPLETE" or reading.get("verification_mode")!="VISUAL_PAGE":issues.append((did,"deep source requires COMPLETE VISUAL_PAGE reading"))
        pages=src.get("pages")
        if isinstance(pages,int) and (reading.get("page_start")!=1 or reading.get("page_end")!=pages or reading.get("pages_reviewed_count")!=pages):issues.append((did,"reading_ref does not cover complete canonical source"))
    for field in LIST_FIELDS:
        val=row.get(field)
        if not isinstance(val,list):issues.append((did,f"{field} must be array"));continue
        if len(val)!=len(set(val)):issues.append((did,f"{field} must be unique"))
        if field in NONEMPTY and not val:issues.append((did,f"{field} must not be empty"))
        for x in val:
            if not isinstance(x,str) or not x.strip():issues.append((did,f"{field} items must be non-empty strings"))
    pages=src.get("pages")
    for anchor in row.get("source_anchors") or []:
        m=ANCHOR_RE.match(anchor)
        if not m:issues.append((did,f"invalid source anchor: {anchor}"));continue
        if m.group(1)!=sid:issues.append((did,f"source anchor belongs to another source: {anchor}"));continue
        p=int(m.group(2))
        if not isinstance(pages,int) or not (1<=p<=pages):issues.append((did,f"source anchor outside canonical pages: {anchor}"))
    course=courses.get(sid);ind=row.get("independence_policy")
    if course:
        if row.get("course_family_id")!=course.get("course_family_id"):issues.append((did,"course_family_id mismatch"))
        if row.get("course_role")!=course.get("course_role"):issues.append((did,"course_role mismatch"))
        if course.get("independent_vote_allowed") is False and ind!="COURSE_FAMILY_SINGLE_VOTE":issues.append((did,"same-course source must use COURSE_FAMILY_SINGLE_VOTE"))
    else:
        if row.get("course_family_id") is not None or row.get("course_role") is not None:issues.append((did,"non-course source must keep course fields null"))
        expected_ind="WORK_FAMILY_SINGLE_VOTE" if lin and lin.get("independence_class")=="SAME_WORK_NOT_INDEPENDENT" else "DEFAULT"
        if ind!=expected_ind:issues.append((did,f"independence_policy must be {expected_ind} for effective lineage"))
    if row.get("course_role") is not None and row.get("course_role") not in COURSE_ROLES:issues.append((did,"invalid course_role"))
    for ref in row.get("prior_distillate_refs") or []:
        d=prior.get(ref)
        if not d:issues.append((did,f"unknown prior_distillate_ref: {ref}"))
        elif d.get("source_id")!=sid:issues.append((did,f"prior distillate belongs to another source: {ref}"))
    expected_reaudit=reaudit.get(sid);actual=row.get("evidence_reaudit_coverage")
    if expected_reaudit is None:
        if actual!="NOT_APPLICABLE":issues.append((did,"source without reaudit target must use NOT_APPLICABLE"))
    elif actual!=expected_reaudit:issues.append((did,f"evidence_reaudit_coverage {actual} != current target coverage {expected_reaudit}"))
    expected_scope="DEEP_SOURCE_PART" if lin and lin.get("relation")=="WORK_PART" else "DEEP_SOURCE_BOOK"
    if row.get("distillation_scope")!=expected_scope:issues.append((did,f"distillation_scope must be {expected_scope} for effective lineage"))
    if row.get("source_credit")!="FULL_SOURCE_VISUAL_REVIEWED":issues.append((did,"source_credit must be FULL_SOURCE_VISUAL_REVIEWED"))
    if row.get("empirical_credit")!="NONE":issues.append((did,"deep reading cannot grant empirical credit"))
    if row.get("claim_extraction_blocked") is not True:issues.append((did,"claim_extraction_blocked must remain true"))
    if row.get("acceptance_status")!="K2B_SOURCE_REVIEW_ACCEPTED":issues.append((did,"invalid acceptance_status"))
    if row.get("distillation_status")!="REVIEWED" or row.get("review_status")!="REVIEWED":issues.append((did,"distillate must be REVIEWED"))
    if row.get("copyright_class")!="DERIVED_SYNTHESIS_SAFE":issues.append((did,"copyright_class must be DERIVED_SYNTHESIS_SAFE"))
    hyps=row.get("testable_hypotheses")
    if not isinstance(hyps,list):issues.append((did,"testable_hypotheses must be array"))
    else:
        seen=set()
        for h in hyps:
            if not isinstance(h,dict) or set(h)!=HYP_FIELDS:issues.append((did,"invalid hypothesis object"));continue
            hid=h.get("hypothesis_id")
            if not isinstance(hid,str) or not hid.strip() or hid in seen:issues.append((did,"hypothesis_id missing/duplicate"))
            seen.add(hid)
            for f in ("statement","freeze_requirements","failure_condition"):
                if not isinstance(h.get(f),str) or not h.get(f).strip():issues.append((did,f"hypothesis {f} must be non-empty"))
            if h.get("status")!="UNTESTED":issues.append((did,"new hypotheses must remain UNTESTED"))
    if PATH_RE.search(json.dumps(row,ensure_ascii=False)):issues.append((did,"local filesystem path leaked"))
    return issues

def validate_rows(rows,state,idx):
    issues=[];seen_d=set();seen_s=set()
    for row in rows:
        did=row.get("distillate_id");sid=row.get("source_id")
        if did in seen_d:issues.append((did or "<missing>","duplicate distillate_id"))
        if sid in seen_s:issues.append((sid or "<missing>","duplicate deep-source distillate"))
        seen_d.add(did);seen_s.add(sid);issues.extend(inspect(row,idx))
    targets=state.get("targets") or []
    if len({t.get('source_id') for t in targets})!=len(targets):issues.append(("<state>","duplicate target source_id"))
    for t in targets:
        sid=t.get("source_id")
        if t.get("required") is True and sid not in seen_s:issues.append((sid or "<missing>","required deep-source distillate missing"))
    if state.get("status")=="COMPLETE" and any(t.get("required") is True and t.get("source_id") not in seen_s for t in targets):issues.append(("<state>","status COMPLETE with missing required target"))
    return issues

def main():
    project=load_json(K/"PROJECT_STATE.json");state=load_json(K/"K2_DEEP_SOURCE_DISTILLATION_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True or state.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked")
    rows=load_distillates(ROOT);issues=validate_rows(rows,state,indexes(ROOT))
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-deep-source-distillates: PASS")
    print(f"targets={len(state.get('targets') or [])} distillates={len(rows)} issues=0 status={state.get('status')}")
    print("claim_extraction_blocked=true empirical_credit=NONE")

if __name__=="__main__":main()
