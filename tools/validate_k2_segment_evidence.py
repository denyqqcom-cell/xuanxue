#!/usr/bin/env python3
import json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
EVIDENCE_TYPES={"EXPLICIT_RULE","WORKED_EXAMPLE","TABLE","DIAGRAM","COMMENTARY","HISTORICAL_CLAIM","CASE_RECORD","META_METHOD"}
SCOPES={"STRUCTURE","ALGORITHM","SYMBOLISM","SELECTION","INTERPRETATION","TIMING","CASE","HISTORY","META_METHOD"}
CLAIM_READY={"READY","CONTEXT_REQUIRED","CONFLICT_CANDIDATE","NOT_CLAIM"}
ALLOWED={
    "evidence_id","source_id","segment_id","work_family_key","independent_vote_key",
    "domain","locator","evidence_type","scope","normalized_fact","extraction_basis",
    "claim_readiness","source_credit","empirical_credit","verbatim_quote","review_status"
}
EID_RE=re.compile(r"^K2SEG-[A-Z0-9-]+$")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(msg):
    print(f"k2-segment-evidence: FAIL: {msg}",file=sys.stderr)
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


def indexes(root=ROOT):
    seg_rows=load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl")
    segments={r.get("segment_id"):r for r in seg_rows}
    if len(segments)!=len(seg_rows):fail("duplicate segment_id in K2_SOURCE_SEGMENTS")
    lin_rows=load_jsonl(root/"knowledge"/"K2_SEGMENT_LINEAGE.jsonl")
    bindings={}
    for r in lin_rows:
        key=(r.get("work_family_key"),r.get("segment_id"))
        if r.get("member_kind")=="SEGMENT":
            if key in bindings:fail(f"duplicate segment family binding {key}")
            bindings[key]=r
    return segments,bindings


def validate_rows(segments,bindings,rows):
    issues=[];seen=set()
    for r in rows:
        eid=r.get("evidence_id") or "<missing>"
        if eid in seen:issues.append((eid,"duplicate evidence_id"))
        seen.add(eid)
        if not isinstance(eid,str) or not EID_RE.match(eid):issues.append((eid,"invalid evidence_id"))
        extra=set(r)-ALLOWED
        if extra:issues.append((eid,f"unexpected fields: {sorted(extra)}"))

        seg_id=r.get("segment_id");seg=segments.get(seg_id)
        if not seg:issues.append((eid,"segment_id not found"));continue
        sid=r.get("source_id")
        if sid!=seg.get("source_id"):issues.append((eid,"source_id/segment mismatch"))
        family=r.get("work_family_key")
        bind=bindings.get((family,seg_id))
        if not bind:issues.append((eid,"segment is not bound to work_family_key"))
        else:
            if r.get("independent_vote_key")!=bind.get("independent_vote_key"):issues.append((eid,"independent_vote_key mismatch"))
            if r.get("domain") not in (bind.get("domain_routes") or []):issues.append((eid,"domain not supported by work-family binding"))

        loc=r.get("locator");lm=LOC_RE.match(loc) if isinstance(loc,str) else None
        if not lm:issues.append((eid,"locator must be pdf:pN"))
        else:
            page=int(lm.group(1));a=seg.get("page_start");b=seg.get("page_end")
            if not isinstance(a,int) or not isinstance(b,int) or not (a<=page<=b):issues.append((eid,"locator outside reviewed segment"))

        domain=r.get("domain")
        if domain not in (seg.get("domain_routes") or []):issues.append((eid,"domain not supported by segment routing"))
        if r.get("evidence_type") not in EVIDENCE_TYPES:issues.append((eid,"invalid evidence_type"))
        if r.get("scope") not in SCOPES:issues.append((eid,"invalid scope"))
        if r.get("extraction_basis")!="VISUAL_PAGE":issues.append((eid,"segment evidence requires VISUAL_PAGE extraction"))
        if r.get("claim_readiness") not in CLAIM_READY:issues.append((eid,"invalid claim_readiness"))
        if r.get("source_credit")!="SUPPORTED":issues.append((eid,"source_credit must be SUPPORTED"))
        if r.get("empirical_credit")!="NONE":issues.append((eid,"K2 reading cannot grant empirical credit"))
        if r.get("review_status")!="REVIEWED":issues.append((eid,"review_status must be REVIEWED"))
        fact=r.get("normalized_fact")
        if not isinstance(fact,str) or not fact.strip():issues.append((eid,"normalized_fact must be non-empty"))
        if r.get("verbatim_quote") is not None:issues.append((eid,"segment evidence must not store verbatim quote"))
        if r.get("evidence_type")=="CASE_RECORD" and r.get("claim_readiness")!="NOT_CLAIM":issues.append((eid,"CASE_RECORD must remain NOT_CLAIM"))
        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((eid,"local filesystem path leaked"))
    return issues


def main():
    path=K/"K2_SEGMENT_EVIDENCE.jsonl"
    if not path.exists():
        print("k2-segment-evidence: PASS")
        print("evidence_rows=0 issues=0")
        return
    rows=load_jsonl(path);segments,bindings=indexes(ROOT);issues=validate_rows(segments,bindings,rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-segment-evidence: PASS")
    print(f"evidence_rows={len(rows)} segments={len({r['segment_id'] for r in rows})} issues=0")

if __name__=="__main__":main()
