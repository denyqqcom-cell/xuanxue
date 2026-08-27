#!/usr/bin/env python3
import copy,json,re,sys
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS={"ziwei","bazi","qimen","liuyao","liuren","fengshui"}
SPECIAL_ROUTES={"OUT_OF_SCOPE","CARRIER_MATTER","UNKNOWN"}
RELATIONS={"WORK_PART","PRIMARY_WORK_IN_COMPOSITE","NON_WORK"}
INDEPENDENCE={"PRIMARY_CANDIDATE","SAME_WORK_NOT_INDEPENDENT","NOT_ELIGIBLE"}
AUTHOR_BASES={"CONTENT_VERIFIED","MANUAL_VERIFIED","TITLE_PAGE","UNKNOWN"}
AUTHOR_CLAIM_STATUSES={"SOURCE_INTERNAL_ATTRIBUTION","EXTERNALLY_VERIFIED","UNKNOWN"}
AUTHORSHIP_SCHEMA_VERSION="k2-segment-authorship-status-v1"
AUTHORSHIP_FIELDS={"schema_version","segment_id","author_claim_status","review_status","reason","external_evidence_refs"}
ALLOWED={"segment_id","source_id","canonical_sha256","page_start","page_end","relation","independence_class","part_label","paired_source_ids","title","title_variants","domain_routes","author","author_basis","author_claim_status","author_evidence","evidence_locators","source_credit_scope","verification_mode","review_status"}
SEG_ID_RE=re.compile(r"^([A-Z]+-SRC-\d{4})#SEG-(\d{3})$")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(msg):
    print(f"k2-source-segments: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)


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
    for d in sorted(DOMAINS):
        p=root/"knowledge"/"domains"/d/"sources.jsonl"
        if not p.exists():continue
        for r in load_jsonl(p):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate canonical source_id {sid}")
            out[sid]=r
    return out


def apply_author_claim_status(rows,status_rows):
    effective=copy.deepcopy(rows);issues=[]
    by_segment={r.get("segment_id"):r for r in effective if isinstance(r.get("segment_id"),str)}
    seen=set()
    for s in status_rows:
        seg=s.get("segment_id") or "<missing>"
        if seg in seen:issues.append((seg,"duplicate authorship status row"))
        seen.add(seg)
        extra=set(s)-AUTHORSHIP_FIELDS
        if extra:issues.append((seg,f"unexpected authorship status fields: {sorted(extra)}"))
        if s.get("schema_version")!=AUTHORSHIP_SCHEMA_VERSION:issues.append((seg,"invalid authorship status schema_version"))
        target=by_segment.get(seg)
        if target is None:
            issues.append((seg,"authorship status references unknown segment_id"));continue
        if s.get("review_status")!="REVIEWED":issues.append((seg,"authorship status review_status must be REVIEWED"))
        status=s.get("author_claim_status")
        if status not in AUTHOR_CLAIM_STATUSES:issues.append((seg,"invalid author_claim_status"))
        reason=s.get("reason")
        if not isinstance(reason,str) or not reason.strip():issues.append((seg,"authorship status reason must be non-empty"))
        refs=s.get("external_evidence_refs")
        if not isinstance(refs,list) or any(not isinstance(x,str) or not x.strip() for x in refs):
            issues.append((seg,"external_evidence_refs must be string array"));refs=[]
        if status=="EXTERNALLY_VERIFIED" and not refs:
            issues.append((seg,"EXTERNALLY_VERIFIED requires external_evidence_refs"))
        if status in {"SOURCE_INTERNAL_ATTRIBUTION","UNKNOWN"} and refs:
            issues.append((seg,f"{status} must not carry external_evidence_refs"))
        target["author_claim_status"]=status
    return effective,issues


def validate_rows(sources,rows):
    issues=[];seen=set();by_source=defaultdict(list)
    for r in rows:
        seg=r.get("segment_id") or "<missing>";sid=r.get("source_id") or "<missing>"
        if seg in seen:issues.append((seg,"duplicate segment_id"))
        seen.add(seg)
        extra=set(r)-ALLOWED
        if extra:issues.append((seg,f"unexpected fields: {sorted(extra)}"))
        m=SEG_ID_RE.match(seg) if isinstance(seg,str) else None
        if not m:issues.append((seg,"segment_id must be SOURCE#SEG-NNN"))
        elif m.group(1)!=sid:issues.append((seg,"segment_id/source_id mismatch"))
        src=sources.get(sid)
        if not src:issues.append((seg,"unknown source_id"));continue
        by_source[sid].append(r)
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((seg,"canonical_sha256 mismatch"))
        a=r.get("page_start");b=r.get("page_end");pages=src.get("pages")
        if not isinstance(a,int) or not isinstance(b,int) or a<1 or b<a:issues.append((seg,"invalid page range"))
        elif isinstance(pages,int) and b>pages:issues.append((seg,"segment exceeds canonical page count"))
        relation=r.get("relation");ind=r.get("independence_class")
        if relation not in RELATIONS:issues.append((seg,"invalid relation"))
        if ind not in INDEPENDENCE:issues.append((seg,"invalid independence_class"))
        if r.get("source_credit_scope")!="SEGMENT_ONLY":issues.append((seg,"source_credit_scope must be SEGMENT_ONLY"))
        if r.get("verification_mode")!="VISUAL_PAGE":issues.append((seg,"composite segmentation requires VISUAL_PAGE verification"))
        if r.get("review_status")!="REVIEWED":issues.append((seg,"review_status must be REVIEWED"))
        title=r.get("title")
        if not isinstance(title,str) or not title.strip():issues.append((seg,"title must be non-empty"))
        variants=r.get("title_variants")
        if not isinstance(variants,list) or any(not isinstance(x,str) or not x.strip() for x in variants):issues.append((seg,"title_variants must be string array"))
        routes=r.get("domain_routes")
        if not isinstance(routes,list) or not routes or len(routes)!=len(set(routes)) or any(x not in DOMAINS|SPECIAL_ROUTES for x in routes):
            issues.append((seg,"invalid domain_routes"))
        author=r.get("author");basis=r.get("author_basis");claim=r.get("author_claim_status");ae=r.get("author_evidence")
        if basis not in AUTHOR_BASES:issues.append((seg,"invalid author_basis"))
        if author is None:
            if basis!="UNKNOWN" or ae not in (None,""):issues.append((seg,"unknown author must remain UNKNOWN with null evidence"))
            if claim not in (None,"UNKNOWN"):issues.append((seg,"UNKNOWN author_basis requires UNKNOWN author_claim_status"))
        else:
            if not isinstance(author,str) or not author.strip():issues.append((seg,"author must be non-empty or null"))
            if basis in {None,"","UNKNOWN"}:issues.append((seg,"known author requires verified author_basis"))
            if not isinstance(ae,str) or not ae.strip():issues.append((seg,"known author requires author_evidence"))
            if claim not in AUTHOR_CLAIM_STATUSES:issues.append((seg,"known author requires author_claim_status"))
            if basis=="CONTENT_VERIFIED" and claim!="SOURCE_INTERNAL_ATTRIBUTION":issues.append((seg,"CONTENT_VERIFIED may only establish SOURCE_INTERNAL_ATTRIBUTION"))
            if basis=="TITLE_PAGE" and claim!="SOURCE_INTERNAL_ATTRIBUTION":issues.append((seg,"TITLE_PAGE may only establish SOURCE_INTERNAL_ATTRIBUTION"))
            if claim=="UNKNOWN":issues.append((seg,"known author cannot have UNKNOWN author_claim_status"))
            if claim=="EXTERNALLY_VERIFIED" and basis!="MANUAL_VERIFIED":issues.append((seg,"EXTERNALLY_VERIFIED requires MANUAL_VERIFIED author_basis"))
        locs=r.get("evidence_locators")
        if not isinstance(locs,list) or not locs:issues.append((seg,"evidence_locators must be non-empty array"))
        else:
            for loc in locs:
                lm=LOC_RE.match(loc) if isinstance(loc,str) else None
                if not lm:issues.append((seg,"locator must be pdf:pN"));continue
                p=int(lm.group(1))
                if isinstance(a,int) and isinstance(b,int) and not (a<=p<=b):issues.append((seg,f"locator {loc} outside segment"))
        pairs=r.get("paired_source_ids")
        if not isinstance(pairs,list) or len(pairs)!=len(set(pairs)):issues.append((seg,"paired_source_ids must be unique array"))
        else:
            for x in pairs:
                if x==sid:issues.append((seg,"segment cannot pair to its own carrier source"))
                if x not in sources:issues.append((seg,f"paired source missing: {x}"))
        part=r.get("part_label")
        if relation=="WORK_PART":
            if ind!="SAME_WORK_NOT_INDEPENDENT":issues.append((seg,"WORK_PART requires SAME_WORK_NOT_INDEPENDENT"))
            if not isinstance(part,str) or not part.strip():issues.append((seg,"WORK_PART requires part_label"))
            if not isinstance(pairs,list) or not pairs:issues.append((seg,"WORK_PART requires paired_source_ids"))
            if routes==["OUT_OF_SCOPE"] or routes==["CARRIER_MATTER"]:issues.append((seg,"WORK_PART must carry a governed/unknown work route"))
        elif part is not None:issues.append((seg,"only WORK_PART may carry part_label"))
        if relation=="PRIMARY_WORK_IN_COMPOSITE" and ind!="PRIMARY_CANDIDATE":issues.append((seg,"embedded primary work requires PRIMARY_CANDIDATE"))
        if relation=="NON_WORK":
            if ind!="NOT_ELIGIBLE":issues.append((seg,"NON_WORK requires NOT_ELIGIBLE"))
            if routes!=["CARRIER_MATTER"]:issues.append((seg,"NON_WORK must route only to CARRIER_MATTER"))
            if author is not None:issues.append((seg,"carrier matter must not inherit an author"))
        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((seg,"local filesystem path leaked"))

    for sid,group in by_source.items():
        src=sources[sid];pages=src.get("pages")
        if len(group)<2:issues.append((sid,"segmented source must contain at least two segments"))
        if sum(1 for r in group if r.get("relation")!="NON_WORK")<2:issues.append((sid,"composite carrier requires at least two work-bearing segments"))
        ordered=sorted(group,key=lambda r:(r.get("page_start") if isinstance(r.get("page_start"),int) else 10**9,r.get("page_end") if isinstance(r.get("page_end"),int) else 10**9))
        cursor=1
        for r in ordered:
            a=r.get("page_start");b=r.get("page_end")
            if not isinstance(a,int) or not isinstance(b,int):continue
            if a!=cursor:
                if a<cursor:issues.append((sid,f"overlap before {r.get('segment_id')}"))
                else:issues.append((sid,f"gap before {r.get('segment_id')}: expected p{cursor}"))
            cursor=max(cursor,b+1)
        if isinstance(pages,int) and cursor!=pages+1:issues.append((sid,f"segmentation does not close canonical p1-p{pages}"))
    return issues


def main():
    path=K/"K2_SOURCE_SEGMENTS.jsonl"
    if not path.exists():
        print("k2-source-segments: PASS")
        print("segmented_sources=0 segments=0 authorship_statuses=0 issues=0")
        return
    rows=load_jsonl(path);sources=source_index(ROOT)
    status_rows=load_jsonl(K/"K2_SEGMENT_AUTHORSHIP_STATUS.jsonl")
    effective,overlay_issues=apply_author_claim_status(rows,status_rows)
    issues=overlay_issues+validate_rows(sources,effective)
    if issues:
        fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-source-segments: PASS")
    print(f"segmented_sources={len({r['source_id'] for r in rows})} segments={len(rows)} authorship_statuses={len(status_rows)} issues=0")

if __name__=="__main__":main()
