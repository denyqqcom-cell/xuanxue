#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS={"ziwei","bazi","qimen","liuyao","liuren","fengshui"}
MEMBER_KINDS={"SOURCE","SEGMENT"}
RELATIONS={"WORK_PART","PRIMARY_WORK_IN_COMPOSITE"}
INDEPENDENCE={"SAME_WORK_NOT_INDEPENDENT","PRIMARY_CANDIDATE"}
AUTHOR_BASES={"CONTENT_VERIFIED","MANUAL_VERIFIED","TITLE_PAGE","SOURCE_INTERNAL_ATTRIBUTION","UNKNOWN"}
CREDIT_SCOPES={"SOURCE_ONLY","SEGMENT_ONLY"}
ALLOWED={
    "binding_id","work_family_key","work_title","member_kind","member_ref",
    "source_id","segment_id","page_start","page_end","relation","part_label",
    "independence_class","domain_routes","author","author_basis","author_evidence",
    "evidence_locators","credit_scope","independent_vote_key","review_status"
}
FAMILY_RE=re.compile(r"^WF-[A-Z0-9-]+$")
BINDING_RE=re.compile(r"^(WF-[A-Z0-9-]+)#MEM-(\d{3})$")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")


def fail(msg):
    print(f"k2-segment-lineage: FAIL: {msg}",file=sys.stderr)
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
    for d in sorted(DOMAINS):
        p=root/"knowledge"/"domains"/d/"sources.jsonl"
        if not p.exists():continue
        for r in load_jsonl(p):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out


def segment_index(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl")
    out={}
    for r in rows:
        seg=r.get("segment_id")
        if seg in out:fail(f"duplicate segment_id {seg}")
        out[seg]=r
    return out


def validate_rows(sources,segments,rows):
    issues=[];seen=set();by_family=defaultdict(list)
    segmented_sources={r.get("source_id") for r in segments.values()}

    for r in rows:
        bid=r.get("binding_id") or "<missing>"
        family=r.get("work_family_key") or "<missing>"
        sid=r.get("source_id") or "<missing>"
        if bid in seen:issues.append((bid,"duplicate binding_id"))
        seen.add(bid)
        extra=set(r)-ALLOWED
        if extra:issues.append((bid,f"unexpected fields: {sorted(extra)}"))

        fm=FAMILY_RE.match(family) if isinstance(family,str) else None
        bm=BINDING_RE.match(bid) if isinstance(bid,str) else None
        if not fm:issues.append((bid,"invalid work_family_key"))
        if not bm:issues.append((bid,"binding_id must be FAMILY#MEM-NNN"))
        elif bm.group(1)!=family:issues.append((bid,"binding_id/work_family_key mismatch"))
        by_family[family].append(r)

        src=sources.get(sid)
        if not src:issues.append((bid,"unknown source_id"));continue

        kind=r.get("member_kind")
        if kind not in MEMBER_KINDS:issues.append((bid,"invalid member_kind"))

        relation=r.get("relation")
        independence=r.get("independence_class")
        part=r.get("part_label")
        if relation not in RELATIONS:
            issues.append((bid,"invalid segment-aware relation"))
        elif relation=="WORK_PART":
            if independence!="SAME_WORK_NOT_INDEPENDENT":
                issues.append((bid,"WORK_PART must be SAME_WORK_NOT_INDEPENDENT"))
            if not isinstance(part,str) or not part.strip():
                issues.append((bid,"WORK_PART requires part_label"))
        elif relation=="PRIMARY_WORK_IN_COMPOSITE":
            if independence!="PRIMARY_CANDIDATE":
                issues.append((bid,"PRIMARY_WORK_IN_COMPOSITE must be PRIMARY_CANDIDATE"))
            if part not in (None,""):
                issues.append((bid,"PRIMARY_WORK_IN_COMPOSITE must not use part_label"))
            if kind!="SEGMENT":
                issues.append((bid,"PRIMARY_WORK_IN_COMPOSITE must use SEGMENT member"))

        if independence not in INDEPENDENCE:
            issues.append((bid,"invalid independence_class"))
        if r.get("independent_vote_key")!=family:issues.append((bid,"independent_vote_key must equal work_family_key"))
        if r.get("review_status")!="REVIEWED":issues.append((bid,"review_status must be REVIEWED"))
        title=r.get("work_title")
        if not isinstance(title,str) or not title.strip():issues.append((bid,"work_title must be non-empty"))

        routes=r.get("domain_routes")
        if not isinstance(routes,list) or not routes or len(routes)!=len(set(routes)) or any(x not in DOMAINS for x in routes):
            issues.append((bid,"domain_routes must contain governed domains only"))

        a=r.get("page_start");b=r.get("page_end");pages=src.get("pages")
        if not isinstance(a,int) or not isinstance(b,int) or a<1 or b<a:issues.append((bid,"invalid page range"))
        elif isinstance(pages,int) and b>pages:issues.append((bid,"page range exceeds canonical source"))

        locs=r.get("evidence_locators")
        if not isinstance(locs,list) or not locs:issues.append((bid,"evidence_locators must be non-empty"))
        else:
            for loc in locs:
                lm=LOC_RE.match(loc) if isinstance(loc,str) else None
                if not lm:issues.append((bid,"locator must be pdf:pN"));continue
                p=int(lm.group(1))
                if isinstance(a,int) and isinstance(b,int) and not (a<=p<=b):issues.append((bid,f"locator {loc} outside member range"))

        author=r.get("author");basis=r.get("author_basis");ae=r.get("author_evidence")
        if author is None:
            if basis!="UNKNOWN" or ae not in (None,""):
                issues.append((bid,"unknown author must use author_basis=UNKNOWN with null evidence"))
        else:
            if not isinstance(author,str) or not author.strip():issues.append((bid,"author must be non-empty or null"))
            if basis not in AUTHOR_BASES-{"UNKNOWN"}:issues.append((bid,"known author requires governed attribution basis"))
            if not isinstance(ae,str) or not ae.strip():issues.append((bid,"known author requires non-empty author_evidence"))

        member_ref=r.get("member_ref");seg_id=r.get("segment_id");scope=r.get("credit_scope")
        if kind=="SOURCE":
            if sid in segmented_sources:issues.append((bid,"composite source cannot be bound carrier-wide; use SEGMENT member"))
            if member_ref!=sid:issues.append((bid,"SOURCE member_ref must equal source_id"))
            if seg_id is not None:issues.append((bid,"SOURCE member must have segment_id=null"))
            if scope!="SOURCE_ONLY":issues.append((bid,"SOURCE member requires SOURCE_ONLY credit_scope"))
            if isinstance(pages,int) and (a!=1 or b!=pages):issues.append((bid,"SOURCE member must cover the complete canonical source"))
        elif kind=="SEGMENT":
            if not isinstance(seg_id,str) or member_ref!=seg_id:issues.append((bid,"SEGMENT member_ref must equal segment_id"))
            seg=segments.get(seg_id)
            if not seg:issues.append((bid,"segment_id not found in K2_SOURCE_SEGMENTS"))
            else:
                if seg.get("source_id")!=sid:issues.append((bid,"segment/source mismatch"))
                if a!=seg.get("page_start") or b!=seg.get("page_end"):issues.append((bid,"binding range must exactly match reviewed segment"))
                seg_routes=set(seg.get("domain_routes") or [])
                if isinstance(routes,list) and not set(routes).issubset(seg_routes):issues.append((bid,"binding domain_routes exceed segment routing"))
                if seg.get("author") is not None and author!=seg.get("author"):issues.append((bid,"binding author conflicts with reviewed segment author"))
                if seg.get("author") is None and author is not None:
                    issues.append((bid,"binding cannot invent an author absent from reviewed segment"))
                if relation=="PRIMARY_WORK_IN_COMPOSITE" and seg.get("relation")!="PRIMARY_WORK_IN_COMPOSITE":
                    issues.append((bid,"PRIMARY_WORK_IN_COMPOSITE binding requires matching reviewed segment relation"))
            if scope!="SEGMENT_ONLY":issues.append((bid,"SEGMENT member requires SEGMENT_ONLY credit_scope"))

        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((bid,"local filesystem path leaked"))

    for family,group in by_family.items():
        if family=="<missing>":continue
        titles={r.get("work_title") for r in group}
        if len(titles)!=1:issues.append((family,"work family members must share one work_title"))

        relations={r.get("relation") for r in group}
        if len(relations)!=1:
            issues.append((family,"work family cannot mix relation classes"))
            continue

        relation=next(iter(relations))
        if relation=="WORK_PART":
            if len(group)<2:issues.append((family,"WORK_PART family requires at least two members"))
            parts=[r.get("part_label") for r in group]
            if len(parts)!=len(set(parts)):issues.append((family,"duplicate part_label in work family"))
            routes={tuple(r.get("domain_routes") or []) for r in group}
            if len(routes)!=1:issues.append((family,"work family members must share domain routing"))
            authors={(r.get("author"),r.get("author_basis")) for r in group}
            known={a for a,b in authors if a is not None}
            if len(known)>1:issues.append((family,"work family has conflicting reviewed authors"))
            if known and any(r.get("author") is None for r in group):
                issues.append((family,"work family mixes known and unknown author attribution"))
        elif relation=="PRIMARY_WORK_IN_COMPOSITE":
            if len(group)!=1:
                issues.append((family,"PRIMARY_WORK_IN_COMPOSITE family must be a singleton segment family"))
            else:
                member=group[0]
                if member.get("member_kind")!="SEGMENT":
                    issues.append((family,"PRIMARY_WORK_IN_COMPOSITE singleton must be a SEGMENT member"))
                if member.get("independence_class")!="PRIMARY_CANDIDATE":
                    issues.append((family,"PRIMARY_WORK_IN_COMPOSITE singleton must remain PRIMARY_CANDIDATE"))

    return issues


def main():
    path=K/"K2_SEGMENT_LINEAGE.jsonl"
    if not path.exists():
        print("k2-segment-lineage: PASS")
        print("families=0 bindings=0 issues=0")
        return
    rows=load_jsonl(path);sources=source_index(ROOT);segments=segment_index(ROOT)
    issues=validate_rows(sources,segments,rows)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-segment-lineage: PASS")
    print(f"families={len({r['work_family_key'] for r in rows})} bindings={len(rows)} issues=0")

if __name__=="__main__":main()
