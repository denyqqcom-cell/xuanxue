#!/usr/bin/env python3
import json, sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ROLES={"FOUNDATION","ADVANCED_EXTENSION","SYNOPSIS_COMPENDIUM","SIBLING_WORK","UNKNOWN"}
DEPENDENCE={"SAME_TEACHING_PROVENANCE","DERIVATIVE_TEACHING_PROVENANCE","UNKNOWN"}
BASIS={"CONTENT_VERIFIED","MANUAL_VERIFIED","UNKNOWN"}
ALLOWED={
    "course_family_id","domain","source_id","work_id","relation_scope","course_role",
    "dependence_class","independent_vote_allowed","related_source_ids","lineage_basis",
    "lineage_evidence","review_status","notes"
}

def fail(msg):
    print(f"k2-course-lineage: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)

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

def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out

def work_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_SOURCE_LINEAGE.jsonl")}

def inspect(row, source, work):
    sid=row.get("source_id") or "<missing>"; issues=[]
    extra=set(row)-ALLOWED
    if extra:issues.append(f"unexpected fields: {sorted(extra)}")
    if row.get("relation_scope")!="COURSE_PROVENANCE":issues.append("relation_scope must be COURSE_PROVENANCE")
    if row.get("domain")!=source.get("domain"):issues.append("domain mismatch")
    if row.get("work_id")!=work.get("work_id"):issues.append("work_id mismatch with K2 source lineage")
    if row.get("course_role") not in ROLES:issues.append("invalid course_role")
    dep=row.get("dependence_class")
    if dep not in DEPENDENCE:issues.append("invalid dependence_class")
    basis=row.get("lineage_basis")
    if basis not in BASIS:issues.append("invalid lineage_basis")
    rel=row.get("related_source_ids")
    if not isinstance(rel,list) or len(rel)!=len(set(rel)):issues.append("related_source_ids must be unique array")
    elif sid in rel:issues.append("related_source_ids cannot contain self")
    if row.get("review_status") not in {"REVIEWED","BLOCKED"}:issues.append("invalid review_status")
    if not isinstance(row.get("independent_vote_allowed"),bool):issues.append("independent_vote_allowed must be boolean")
    evidence=row.get("lineage_evidence")
    if basis=="UNKNOWN":
        if evidence not in (None,""):issues.append("UNKNOWN basis cannot claim lineage evidence")
    elif not isinstance(evidence,str) or not evidence.strip():
        issues.append("resolved lineage requires lineage_evidence")
    if dep in {"SAME_TEACHING_PROVENANCE","DERIVATIVE_TEACHING_PROVENANCE"} and row.get("independent_vote_allowed") is not False:
        issues.append("resolved same-course/derivative member cannot count as independent vote")
    if row.get("course_role")=="SYNOPSIS_COMPENDIUM":
        if dep!="DERIVATIVE_TEACHING_PROVENANCE":issues.append("SYNOPSIS_COMPENDIUM requires DERIVATIVE_TEACHING_PROVENANCE")
        if not isinstance(rel,list) or not rel:issues.append("SYNOPSIS_COMPENDIUM requires related_source_ids")
    if dep=="DERIVATIVE_TEACHING_PROVENANCE" and (not isinstance(rel,list) or not rel):
        issues.append("derivative teaching provenance requires related_source_ids")
    return [(sid,x) for x in issues]

def validate_rows(sources, works, rows):
    issues=[]; seen_sources=set(); by_family=defaultdict(list)
    for r in rows:
        sid=r.get("source_id")
        if sid in seen_sources:issues.append((sid or "<missing>","source appears in multiple course-lineage rows"))
        seen_sources.add(sid)
        src=sources.get(sid); work=works.get(sid)
        if not src:issues.append((sid or "<missing>","unknown source_id"));continue
        if not work or not work.get("work_id"):issues.append((sid,"missing resolved K2 work lineage"));continue
        issues.extend(inspect(r,src,work))
        by_family[r.get("course_family_id")].append(r)
    for fid,members in by_family.items():
        if not isinstance(fid,str) or not fid.strip():
            issues.append(("<global>","course_family_id must be non-empty"));continue
        if len(members)<2:issues.append((fid,"resolved course family must contain at least two sources"))
        work_ids=[r.get("work_id") for r in members]
        if len(work_ids)!=len(set(work_ids)):issues.append((fid,"course lineage may only relate distinct work_ids; same-work variants belong in K2_SOURCE_LINEAGE"))
        member_ids={r.get("source_id") for r in members}
        for r in members:
            for target in r.get("related_source_ids") or []:
                if target not in member_ids:issues.append((r.get("source_id"),f"related source {target} is outside course family"))
    return issues

def main():
    project=load_json(K/"PROJECT_STATE.json")
    if project.get("claim_extraction_blocked") is not True:
        fail("claim extraction must remain blocked during K2B course lineage review")
    rows=load_jsonl(K/"K2_COURSE_LINEAGE.jsonl")
    if not rows:
        print("k2-course-lineage: PASS")
        print("families=0 rows=0 issues=0")
        return
    issues=validate_rows(source_index(),work_index(),rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-course-lineage: PASS")
    print(f"families={len({r['course_family_id'] for r in rows})} rows={len(rows)} issues=0")

if __name__=="__main__":main()
