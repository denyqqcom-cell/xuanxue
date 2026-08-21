#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ALLOWED={
    "distillate_id","work_family_key","work_title","domain","member_refs","reading_refs",
    "segment_evidence_refs","direct_source_locators","source_credit","empirical_credit",
    "essence","method_map","applicability_constraints","source_limitations","conflicts_and_tensions",
    "anti_patterns","model_updates","testable_hypotheses","credit_decisions",
    "excluded_from_operational_use","claim_extraction_blocked","distillation_status","review_status",
    "copyright_class"
}
LIST_FIELDS=["member_refs","reading_refs","segment_evidence_refs","direct_source_locators","essence","method_map","applicability_constraints","source_limitations","conflicts_and_tensions","anti_patterns","model_updates","excluded_from_operational_use"]
NONEMPTY_STRING_LISTS={"member_refs","reading_refs","essence","method_map","source_limitations","model_updates"}
DIST_ID_RE=re.compile(r"^K2WF-[A-Z0-9-]+$")
ANCHOR_RE=re.compile(r"^(.+)@pdf:p(\d+)$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
HYP_FIELDS={"hypothesis_id","statement","freeze_requirements","failure_condition","status"}
CREDIT_FIELDS={"topic","source_credit","empirical_credit","decision","summary","anchors"}


def fail(msg):
    print(f"k2-work-family-distillates: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


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
            out[r.get("source_id")]=r
    return out


def indexes(root=ROOT):
    family=defaultdict(list)
    for r in load_jsonl(root/"knowledge"/"K2_SEGMENT_LINEAGE.jsonl"):
        family[r.get("work_family_key")].append(r)
    readings={r.get("reading_id"):r for r in load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")}
    ev={r.get("evidence_id"):r for r in load_jsonl(root/"knowledge"/"K2_SEGMENT_EVIDENCE.jsonl")}
    segs={r.get("segment_id"):r for r in load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl")}
    return family,readings,ev,segs,source_index(root)


def validate_anchor(anchor,family_members,ev,segs,sources,issues,owner):
    if anchor in ev:
        if ev[anchor].get("work_family_key")!=owner:issues.append((owner,f"evidence anchor outside family: {anchor}"))
        return
    m=ANCHOR_RE.match(anchor) if isinstance(anchor,str) else None
    if not m:
        issues.append((owner,f"invalid anchor: {anchor}"));return
    ref=m.group(1);page=int(m.group(2))
    by_ref={r.get("member_ref"):r for r in family_members}
    member=by_ref.get(ref)
    if not member:
        issues.append((owner,f"anchor ref is not a family member: {ref}"));return
    if member.get("member_kind")=="SOURCE":
        src=sources.get(member.get("source_id"));pages=src.get("pages") if src else None
        if not isinstance(pages,int) or not (1<=page<=pages):issues.append((owner,f"source anchor outside canonical pages: {anchor}"))
    else:
        seg=segs.get(member.get("segment_id"));a=seg.get("page_start") if seg else None;b=seg.get("page_end") if seg else None
        if not isinstance(a,int) or not isinstance(b,int) or not (a<=page<=b):issues.append((owner,f"segment anchor outside member range: {anchor}"))


def validate_rows(families,readings,ev,segs,sources,rows):
    issues=[];seen=set()
    ev_by_family=defaultdict(set)
    for eid,e in ev.items():ev_by_family[e.get("work_family_key")].add(eid)

    for d in rows:
        did=d.get("distillate_id") or "<missing>";family=d.get("work_family_key") or "<missing>"
        if did in seen:issues.append((did,"duplicate distillate_id"))
        seen.add(did)
        if not isinstance(did,str) or not DIST_ID_RE.match(did):issues.append((did,"invalid distillate_id"))
        extra=set(d)-ALLOWED
        if extra:issues.append((did,f"unexpected fields: {sorted(extra)}"))
        members=families.get(family,[])
        if not members:issues.append((did,"unknown work_family_key"));continue
        titles={r.get("work_title") for r in members}
        if d.get("work_title") not in titles or len(titles)!=1:issues.append((did,"work_title mismatch"))
        routes={x for r in members for x in (r.get("domain_routes") or [])}
        if d.get("domain") not in routes:issues.append((did,"domain not supported by family members"))

        for field in LIST_FIELDS:
            val=d.get(field)
            if not isinstance(val,list):issues.append((did,f"{field} must be array"));continue
            if len(val)!=len(set(val)):issues.append((did,f"{field} must not contain duplicates"))
            if field in NONEMPTY_STRING_LISTS and not val:issues.append((did,f"{field} must not be empty"))
            for x in val:
                if not isinstance(x,str) or not x.strip():issues.append((did,f"{field} items must be non-empty strings"))

        expected_members={r.get("member_ref") for r in members}
        if set(d.get("member_refs") or [])!=expected_members:issues.append((did,"member_refs must exactly match work-family bindings"))

        expected_source_ids={r.get("source_id") for r in members}
        rr=d.get("reading_refs") or []
        actual_read_sources=set()
        for ref in rr:
            row=readings.get(ref)
            if not row:issues.append((did,f"unknown reading_ref: {ref}"));continue
            if row.get("read_status")!="COMPLETE" or row.get("verification_mode")!="VISUAL_PAGE":issues.append((did,f"reading_ref is not COMPLETE VISUAL_PAGE: {ref}"))
            actual_read_sources.add(row.get("source_id"))
        if actual_read_sources!=expected_source_ids:issues.append((did,"reading_refs must cover exactly the family carrier sources"))

        expected_ev=ev_by_family.get(family,set())
        if set(d.get("segment_evidence_refs") or [])!=expected_ev:issues.append((did,"segment_evidence_refs must exactly match current family segment evidence"))

        for anchor in d.get("direct_source_locators") or []:
            validate_anchor(anchor,members,ev,segs,sources,issues,family)
            m=ANCHOR_RE.match(anchor)
            if m:
                member={r.get("member_ref"):r for r in members}.get(m.group(1))
                if member and member.get("member_kind")!="SOURCE":issues.append((did,"direct_source_locators are reserved for SOURCE members"))

        if d.get("source_credit")!="FULL_WORK_FAMILY_REVIEWED":issues.append((did,"source_credit must be FULL_WORK_FAMILY_REVIEWED"))
        if d.get("empirical_credit")!="NONE":issues.append((did,"work-family reading cannot grant empirical credit"))
        if d.get("claim_extraction_blocked") is not True:issues.append((did,"claim_extraction_blocked must remain true"))
        if d.get("distillation_status")!="REVIEWED" or d.get("review_status")!="REVIEWED":issues.append((did,"distillate must be REVIEWED"))
        if d.get("copyright_class")!="DERIVED_SYNTHESIS_SAFE":issues.append((did,"copyright_class must be DERIVED_SYNTHESIS_SAFE"))

        hypotheses=d.get("testable_hypotheses")
        if not isinstance(hypotheses,list) or not hypotheses:issues.append((did,"testable_hypotheses must be non-empty array"))
        else:
            hseen=set()
            for h in hypotheses:
                if not isinstance(h,dict) or set(h)!=HYP_FIELDS:issues.append((did,"invalid hypothesis object"));continue
                hid=h.get("hypothesis_id")
                if not isinstance(hid,str) or not hid.strip() or hid in hseen:issues.append((did,"hypothesis_id missing/duplicate"))
                hseen.add(hid)
                for f in ("statement","freeze_requirements","failure_condition"):
                    if not isinstance(h.get(f),str) or not h.get(f).strip():issues.append((did,f"hypothesis {f} must be non-empty"))
                if h.get("status")!="UNTESTED":issues.append((did,"new work-family hypotheses must remain UNTESTED"))

        credits=d.get("credit_decisions")
        if not isinstance(credits,list) or not credits:issues.append((did,"credit_decisions must be non-empty array"))
        else:
            topics=set()
            for c in credits:
                if not isinstance(c,dict) or set(c)!=CREDIT_FIELDS:issues.append((did,"invalid credit_decision object"));continue
                topic=c.get("topic")
                if not isinstance(topic,str) or not topic.strip() or topic in topics:issues.append((did,"credit_decision topic missing/duplicate"))
                topics.add(topic)
                if c.get("empirical_credit")!="NONE":issues.append((did,f"credit_decision {topic} cannot grant empirical credit"))
                for f in ("source_credit","decision","summary"):
                    if not isinstance(c.get(f),str) or not c.get(f).strip():issues.append((did,f"credit_decision {f} must be non-empty"))
                anchors=c.get("anchors")
                if not isinstance(anchors,list) or not anchors:issues.append((did,f"credit_decision {topic} requires anchors"))
                else:
                    for a in anchors:validate_anchor(a,members,ev,segs,sources,issues,family)

        serialized=json.dumps(d,ensure_ascii=False)
        if PATH_RE.search(serialized):issues.append((did,"distillate leaks local filesystem path"))
    return issues


def main():
    path=K/"K2_WORK_FAMILY_DISTILLATES.jsonl"
    if not path.exists():
        print("k2-work-family-distillates: PASS")
        print("families=0 distillates=0 issues=0")
        return
    rows=load_jsonl(path);idx=indexes(ROOT);issues=validate_rows(*idx,rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-work-family-distillates: PASS")
    print(f"families={len({r['work_family_key'] for r in rows})} distillates={len(rows)} issues=0")

if __name__=="__main__":main()
