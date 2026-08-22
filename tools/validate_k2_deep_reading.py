#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ALLOWED={"reading_id","source_id","canonical_sha256","page_start","page_end","pages_reviewed_count","verification_mode","read_status","binding_mode","segment_ids","reading_basis","review_status"}
READING_ID_RE=re.compile(r"^K2DEEP-[A-Z]+-SRC-\d{4}$")
BINDING_MODES={"SOURCE","SEGMENTED_CARRIER"}


def fail(msg):
    print(f"k2-deep-reading: FAIL: {msg}",file=sys.stderr)
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
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out


def segments_by_source(root=ROOT):
    out=defaultdict(list)
    for r in load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl"):
        out[r.get("source_id")].append(r)
    return out


def validate_rows(sources,seg_by_source,rows):
    issues=[];seen_ids=set();seen_sources=set()
    for r in rows:
        rid=r.get("reading_id") or "<missing>";sid=r.get("source_id") or "<missing>"
        if rid in seen_ids:issues.append((rid,"duplicate reading_id"))
        seen_ids.add(rid)
        if sid in seen_sources:issues.append((sid,"duplicate deep reading source"))
        seen_sources.add(sid)
        if not isinstance(rid,str) or not READING_ID_RE.match(rid):issues.append((rid,"invalid reading_id"))
        if set(r)-ALLOWED:issues.append((rid,f"unexpected fields: {sorted(set(r)-ALLOWED)}"))
        src=sources.get(sid)
        if not src:issues.append((rid,"unknown source_id"));continue
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((rid,"canonical_sha256 mismatch"))
        pages=src.get("pages");a=r.get("page_start");b=r.get("page_end");count=r.get("pages_reviewed_count")
        if not isinstance(pages,int):issues.append((rid,"deep reading currently requires canonical PDF page count"))
        else:
            if a!=1 or b!=pages:issues.append((rid,"COMPLETE deep reading must cover canonical p1-pN"))
            if count!=pages:issues.append((rid,"pages_reviewed_count mismatch"))
        if r.get("verification_mode")!="VISUAL_PAGE":issues.append((rid,"deep reading COMPLETE requires VISUAL_PAGE"))
        if r.get("read_status")!="COMPLETE":issues.append((rid,"deep reading row must be COMPLETE"))
        if r.get("review_status")!="REVIEWED":issues.append((rid,"review_status must be REVIEWED"))
        if r.get("reading_basis")!="PROJECT_MAIN_AGENT_VISUAL_REVIEW":issues.append((rid,"unsupported reading_basis"))
        mode=r.get("binding_mode")
        if mode not in BINDING_MODES:issues.append((rid,"invalid binding_mode"))
        segs=r.get("segment_ids")
        if not isinstance(segs,list) or len(segs)!=len(set(segs)):issues.append((rid,"segment_ids must be unique array"));segs=[]
        actual=seg_by_source.get(sid,[])
        actual_ids=[x.get("segment_id") for x in sorted(actual,key=lambda x:x.get("page_start",10**9))]
        if actual:
            if mode!="SEGMENTED_CARRIER":issues.append((rid,"segmented source requires SEGMENTED_CARRIER binding_mode"))
            if segs!=actual_ids:issues.append((rid,"segment_ids must exactly match reviewed carrier segmentation"))
            cursor=1
            for x in sorted(actual,key=lambda x:x.get("page_start",10**9)):
                if x.get("page_start")!=cursor:issues.append((rid,"segment coverage has gap/overlap"));break
                cursor=x.get("page_end",cursor-1)+1
            if isinstance(pages,int) and cursor!=pages+1:issues.append((rid,"segment coverage does not close canonical pages"))
        else:
            if mode!="SOURCE":issues.append((rid,"unsegmented source requires SOURCE binding_mode"))
            if segs:issues.append((rid,"unsegmented source must not list segment_ids"))
    return issues


def main():
    path=K/"K2_DEEP_READING_LEDGER.jsonl"
    if not path.exists():
        print("k2-deep-reading: PASS")
        print("complete_sources=0 issues=0")
        return
    rows=load_jsonl(path);issues=validate_rows(source_index(ROOT),segments_by_source(ROOT),rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-deep-reading: PASS")
    print(f"complete_sources={len(rows)} issues=0")

if __name__=="__main__":main()
