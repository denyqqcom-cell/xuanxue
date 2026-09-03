#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS={"ziwei","bazi","qimen","liuyao","liuren","fengshui"}
ALLOWED={
    "closure_id","source_id","canonical_sha256","deep_reading_id","segment_ids",
    "work_segment_ids","non_work_segment_ids","work_family_keys","completion_scope",
    "queue_resolution","legacy_wave1_credit","source_credit","carrier_independent_vote_credit",
    "empirical_credit","claim_extraction_blocked","closure_status","review_status"
}
CID_RE=re.compile(r"^K2CC-[A-Z]+-SRC-\d{4}$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(msg):
    print(f"k2-composite-source-closures: FAIL: {msg}",file=sys.stderr)
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


def load_work_family_distillates(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_WORK_FAMILY_DISTILLATES.jsonl")
    d=root/"knowledge"/"K2_WORK_FAMILY_DISTILLATES.d"
    if d.exists():
        for p in sorted(d.glob("*.jsonl")):
            rows.extend(load_jsonl(p))
    return rows


def source_index(root=ROOT):
    out={}
    for d in sorted(DOMAINS):
        p=root/"knowledge"/"domains"/d/"sources.jsonl"
        if not p.exists():continue
        for r in load_jsonl(p):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out


def validate_rows(sources,segments,deep_rows,lineage_rows,evidence_rows,distillates,
                  wave1_ledger,wave1_evidence,wave1_distillates,rows):
    issues=[];seen_id=set();seen_source=set()

    deep={r.get("reading_id"):r for r in deep_rows}
    if len(deep)!=len(deep_rows):
        issues.append(("<global>","duplicate deep reading_id"))

    seg_by_source=defaultdict(list)
    for s in segments.values():
        seg_by_source[s.get("source_id")].append(s)

    bindings_by_seg=defaultdict(list)
    family_members=defaultdict(list)
    for r in lineage_rows:
        family_members[r.get("work_family_key")].append(r)
        if r.get("member_kind")=="SEGMENT" and r.get("segment_id"):
            bindings_by_seg[r.get("segment_id")].append(r)

    ev_by_seg=defaultdict(list);ev_by_family=defaultdict(list)
    for e in evidence_rows:
        ev_by_seg[e.get("segment_id")].append(e)
        ev_by_family[e.get("work_family_key")].append(e)

    dist_by_family=defaultdict(list)
    for d in distillates:
        dist_by_family[d.get("work_family_key")].append(d)

    legacy_terminal={r.get("source_id") for r in wave1_ledger if r.get("read_status") in {"COMPLETE","BLOCKED"}}
    legacy_ev_sources={r.get("source_id") for r in wave1_evidence if r.get("source_id")}
    legacy_dist_sources={r.get("source_id") for r in wave1_distillates if r.get("source_id")}

    for c in rows:
        cid=c.get("closure_id") or "<missing>";sid=c.get("source_id") or "<missing>"
        if cid in seen_id:issues.append((cid,"duplicate closure_id"))
        seen_id.add(cid)
        if sid in seen_source:issues.append((sid,"duplicate composite closure source"))
        seen_source.add(sid)

        extra=set(c)-ALLOWED
        if extra:issues.append((cid,f"unexpected fields: {sorted(extra)}"))
        if not isinstance(cid,str) or not CID_RE.match(cid):issues.append((cid,"invalid closure_id"))
        src=sources.get(sid)
        if not src:issues.append((cid,"unknown source_id"));continue
        if c.get("canonical_sha256")!=src.get("file_sha256"):issues.append((cid,"canonical_sha256 mismatch"))

        if c.get("completion_scope")!="COMPOSITE_CARRIER_EXECUTION":issues.append((cid,"invalid completion_scope"))
        if c.get("queue_resolution")!="RESOLVED":issues.append((cid,"queue_resolution must be RESOLVED"))
        if c.get("legacy_wave1_credit")!="NONE":issues.append((cid,"legacy_wave1_credit must remain NONE"))
        if c.get("source_credit")!="FULL_CARRIER_VISUAL_REVIEWED_AND_EMBEDDED_WORKS_DISTILLED":
            issues.append((cid,"invalid source_credit"))
        if c.get("carrier_independent_vote_credit")!="NONE":issues.append((cid,"carrier cannot receive an independent vote"))
        if c.get("empirical_credit")!="NONE":issues.append((cid,"composite closure cannot grant empirical credit"))
        if c.get("claim_extraction_blocked") is not True:issues.append((cid,"claim_extraction_blocked must remain true"))
        if c.get("closure_status")!="C2_COMPOSITE_NORMALIZED":issues.append((cid,"invalid closure_status"))
        if c.get("review_status")!="REVIEWED":issues.append((cid,"review_status must be REVIEWED"))

        if sid in legacy_terminal:issues.append((cid,"source already has terminal legacy Wave1 Reading; composite closure would double-resolve it"))
        if sid in legacy_ev_sources:issues.append((cid,"composite source must not also carry legacy Wave1 Evidence"))
        if sid in legacy_dist_sources:issues.append((cid,"composite source must not also carry legacy Wave1 Book Distillate"))

        srows=sorted(seg_by_source.get(sid,[]),key=lambda x:x.get("page_start",10**9))
        actual_seg_ids=[r.get("segment_id") for r in srows]
        if not srows:issues.append((cid,"composite closure requires reviewed source segments"));continue

        seg_ids=c.get("segment_ids")
        if not isinstance(seg_ids,list) or len(seg_ids)!=len(set(seg_ids)):issues.append((cid,"segment_ids must be unique array"));seg_ids=[]
        if seg_ids!=actual_seg_ids:issues.append((cid,"segment_ids must exactly match reviewed carrier segmentation"))

        work_segments=[
            r for r in srows
            if r.get("relation")!="NON_WORK"
            and any(d in DOMAINS for d in (r.get("domain_routes") or []))
        ]
        non_work=[r for r in srows if r.get("relation")=="NON_WORK"]
        expected_work_ids=[r.get("segment_id") for r in work_segments]
        expected_non_work_ids=[r.get("segment_id") for r in non_work]
        if c.get("work_segment_ids")!=expected_work_ids:issues.append((cid,"work_segment_ids must exactly match governed work-bearing segments"))
        if c.get("non_work_segment_ids")!=expected_non_work_ids:issues.append((cid,"non_work_segment_ids must exactly match NON_WORK segments"))

        rid=c.get("deep_reading_id");dr=deep.get(rid)
        if not dr:issues.append((cid,"deep_reading_id not found"))
        else:
            if dr.get("source_id")!=sid:issues.append((cid,"deep reading/source mismatch"))
            if dr.get("canonical_sha256")!=src.get("file_sha256"):issues.append((cid,"deep reading SHA mismatch"))
            if dr.get("read_status")!="COMPLETE" or dr.get("review_status")!="REVIEWED" or dr.get("verification_mode")!="VISUAL_PAGE":
                issues.append((cid,"deep reading must be COMPLETE REVIEWED VISUAL_PAGE"))
            if dr.get("binding_mode")!="SEGMENTED_CARRIER":issues.append((cid,"deep reading must use SEGMENTED_CARRIER"))
            if dr.get("segment_ids")!=actual_seg_ids:issues.append((cid,"deep reading segment_ids mismatch"))
            pages=src.get("pages")
            if isinstance(pages,int):
                if dr.get("page_start")!=1 or dr.get("page_end")!=pages or dr.get("pages_reviewed_count")!=pages:
                    issues.append((cid,"deep reading does not cover full canonical carrier"))

        derived_families=[]
        for s in work_segments:
            seg_id=s.get("segment_id")
            binds=bindings_by_seg.get(seg_id,[])
            if len(binds)!=1:
                issues.append((cid,f"work segment must have exactly one segment-work binding: {seg_id}"))
                continue
            b=binds[0]
            if b.get("credit_scope")!="SEGMENT_ONLY":issues.append((cid,f"binding must be SEGMENT_ONLY: {seg_id}"))
            if b.get("relation") not in {"PRIMARY_WORK_IN_COMPOSITE","WORK_PART"}:
                issues.append((cid,f"unsupported work-bearing segment relation: {seg_id}"))
            derived_families.append(b.get("work_family_key"))

            seg_ev=ev_by_seg.get(seg_id,[])
            if not seg_ev:issues.append((cid,f"work segment has no normalized Segment Evidence: {seg_id}"))
            routed={d for d in (s.get("domain_routes") or []) if d in DOMAINS}
            evidenced={e.get("domain") for e in seg_ev}
            if not routed.issubset(evidenced):
                issues.append((cid,f"segment Evidence does not cover all governed routes: {seg_id} missing={sorted(routed-evidenced)}"))

        for seg_id in expected_non_work_ids:
            if ev_by_seg.get(seg_id):
                issues.append((cid,f"NON_WORK segment must not carry Segment Evidence: {seg_id}"))

        if len(derived_families)!=len(set(derived_families)):
            issues.append((cid,"multiple work segments collapse into duplicate family without explicit multipart review"))
        if c.get("work_family_keys")!=derived_families:
            issues.append((cid,"work_family_keys must exactly follow work-segment order"))

        for family in derived_families:
            ds=dist_by_family.get(family,[])
            if len(ds)!=1:
                issues.append((cid,f"work family must have exactly one reviewed distillate: {family}"))
                continue
            d=ds[0]
            if d.get("distillation_status")!="REVIEWED" or d.get("review_status")!="REVIEWED":
                issues.append((cid,f"work-family distillate not REVIEWED: {family}"))
            if d.get("empirical_credit")!="NONE" or d.get("claim_extraction_blocked") is not True:
                issues.append((cid,f"work-family distillate credit boundary violated: {family}"))
            if rid not in (d.get("reading_refs") or []):
                issues.append((cid,f"work-family distillate does not cite carrier deep reading: {family}"))
            expected_ev={e.get("evidence_id") for e in ev_by_family.get(family,[])}
            if set(d.get("segment_evidence_refs") or [])!=expected_ev:
                issues.append((cid,f"work-family distillate evidence refs not exact: {family}"))

        blob=json.dumps(c,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((cid,"local filesystem path leaked"))

    return issues


def repository_state(root=ROOT):
    root=Path(root).resolve()
    sys.path.insert(0,str(root/"tools"))
    import k2_wave1_aggregate as wave1
    import validate_k2_work_family_distillates as wf

    sources=source_index(root)
    seg_rows=load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl")
    segments={r.get("segment_id"):r for r in seg_rows}
    deep_rows=load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")
    lineage_rows=load_jsonl(root/"knowledge"/"K2_SEGMENT_LINEAGE.jsonl")
    evidence_rows=load_jsonl(root/"knowledge"/"K2_SEGMENT_EVIDENCE.jsonl")
    distillates=wf.load_distillates(root)
    ledger,legacy_evidence,legacy_distillates=wave1.aggregate_wave1(root)
    return sources,segments,deep_rows,lineage_rows,evidence_rows,distillates,ledger,legacy_evidence,legacy_distillates


def valid_closure_source_ids(root=ROOT):
    root=Path(root).resolve()
    rows=load_jsonl(root/"knowledge"/"K2_COMPOSITE_SOURCE_CLOSURES.jsonl")
    if not rows:return set()
    state=repository_state(root)
    issues=validate_rows(*state,rows)
    if issues:
        raise ValueError("invalid composite closure registry: "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    return {r.get("source_id") for r in rows if r.get("queue_resolution")=="RESOLVED"}


def main():
    path=K/"K2_COMPOSITE_SOURCE_CLOSURES.jsonl"
    rows=load_jsonl(path)
    if not rows:
        print("k2-composite-source-closures: PASS")
        print("closures=0 resolved=0 issues=0")
        return
    state=repository_state(ROOT)
    issues=validate_rows(*state,rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-composite-source-closures: PASS")
    print(f"closures={len(rows)} resolved={len(valid_closure_source_ids(ROOT))} issues=0")
    print("legacy_wave1_credit=unchanged")
    print("claim_extraction_blocked=true")


if __name__=="__main__":main()
