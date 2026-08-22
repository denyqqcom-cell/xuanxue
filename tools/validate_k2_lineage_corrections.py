#!/usr/bin/env python3
import json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ALLOWED={"correction_id","source_id","previous_relation","previous_work_id","corrected_relation","corrected_work_id","part_label","parent_work_title","correction_basis","evidence_locators","reason","review_status"}
LOC_RE=re.compile(r"^pdf:p([1-9][0-9]*)$")
CORR_RE=re.compile(r"^K2LC-[A-Z]{2}-\d{4}-\d{3}$")
RELATIONS={"PRIMARY_WORK","WORK_PART","SAME_WORK_VARIANT","COMMENTARY_DERIVATIVE","UNKNOWN"}


def fail(msg):
    print(f"k2-lineage-corrections: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)


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


def raw_lineage_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_SOURCE_LINEAGE.jsonl")}


def reading_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")}


def apply_correction(raw,c):
    out=dict(raw)
    out["relation"]=c.get("corrected_relation")
    out["work_id"]=c.get("corrected_work_id")
    out["part_label"]=c.get("part_label")
    if c.get("corrected_relation")=="WORK_PART":
        out["independence_class"]="SAME_WORK_NOT_INDEPENDENT"
        out["k2_eligible"]=True
        out["variant_of_source_id"]=None
    return out


def effective_lineage_index(raw_index,corrections):
    out={k:dict(v) for k,v in raw_index.items()}
    for c in corrections:
        sid=c.get("source_id")
        if sid in out:out[sid]=apply_correction(out[sid],c)
    return out


def inspect(c,sources,raw,readings):
    cid=c.get("correction_id") or "<missing>";sid=c.get("source_id") or "<missing>";issues=[]
    extra=set(c)-ALLOWED
    if extra:issues.append((cid,f"unexpected fields: {sorted(extra)}"))
    if not isinstance(cid,str) or not CORR_RE.match(cid):issues.append((cid,"invalid correction_id"))
    src=sources.get(sid);old=raw.get(sid);reading=readings.get(sid)
    if not src:issues.append((cid,"unknown source_id"));return issues
    if not old:issues.append((cid,"missing raw lineage row"));return issues
    if c.get("previous_relation")!=old.get("relation"):issues.append((cid,"previous_relation does not match accepted raw lineage"))
    if c.get("previous_work_id")!=old.get("work_id"):issues.append((cid,"previous_work_id does not match accepted raw lineage"))
    rel=c.get("corrected_relation")
    if rel not in RELATIONS:issues.append((cid,"invalid corrected_relation"))
    if c.get("correction_basis")!="VISUAL_PAGE":issues.append((cid,"correction_basis must be VISUAL_PAGE"))
    if c.get("review_status")!="REVIEWED":issues.append((cid,"review_status must be REVIEWED"))
    if not isinstance(c.get("reason"),str) or not c.get("reason").strip():issues.append((cid,"reason required"))
    if not reading or reading.get("read_status")!="COMPLETE" or reading.get("verification_mode")!="VISUAL_PAGE":
        issues.append((cid,"lineage correction requires COMPLETE VISUAL_PAGE deep reading"))
    elif reading.get("canonical_sha256")!=src.get("file_sha256"):
        issues.append((cid,"deep reading SHA mismatch"))
    locs=c.get("evidence_locators")
    if not isinstance(locs,list) or not locs or len(locs)!=len(set(locs)):issues.append((cid,"evidence_locators must be non-empty unique array"))
    else:
        pages=src.get("pages")
        for loc in locs:
            m=LOC_RE.match(loc) if isinstance(loc,str) else None
            if not m:issues.append((cid,f"invalid evidence locator: {loc}"));continue
            p=int(m.group(1))
            if not isinstance(pages,int) or not (1<=p<=pages):issues.append((cid,f"evidence locator outside canonical pages: {loc}"))
            if reading and not (reading.get("page_start",1)<=p<=reading.get("page_end",0)):issues.append((cid,f"evidence locator outside deep reading coverage: {loc}"))
    if rel=="WORK_PART":
        if not isinstance(c.get("corrected_work_id"),str) or not c.get("corrected_work_id").strip():issues.append((cid,"WORK_PART requires corrected_work_id"))
        if not isinstance(c.get("part_label"),str) or not c.get("part_label").strip():issues.append((cid,"WORK_PART requires part_label"))
        if not isinstance(c.get("parent_work_title"),str) or not c.get("parent_work_title").strip():issues.append((cid,"WORK_PART requires parent_work_title"))
    return issues


def validate_rows(rows,sources,raw,readings):
    issues=[];seen_c=set();seen_s=set()
    for c in rows:
        cid=c.get("correction_id");sid=c.get("source_id")
        if cid in seen_c:issues.append((cid or "<missing>","duplicate correction_id"))
        if sid in seen_s:issues.append((sid or "<missing>","multiple active corrections for source; versioning not implemented"))
        seen_c.add(cid);seen_s.add(sid)
        issues.extend(inspect(c,sources,raw,readings))
    return issues


def main():
    rows=load_jsonl(K/"K2_LINEAGE_CORRECTIONS.jsonl")
    sources=source_index();raw=raw_lineage_index();readings=reading_index()
    issues=validate_rows(rows,sources,raw,readings)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    effective=effective_lineage_index(raw,rows)
    changed=sum(1 for sid in effective if effective[sid]!=raw[sid])
    print("k2-lineage-corrections: PASS")
    print(f"corrections={len(rows)} effective_changed={changed} issues=0")

if __name__=="__main__":main()
