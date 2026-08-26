#!/usr/bin/env python3
import argparse,json,re,sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
ROUTES=set(DOMAINS+["OUT_OF_SCOPE","CARRIER_MATTER"])
ROW_FIELDS={"routing_id","source_id","canonical_sha256","routing_mode","raw_knowledge_domains","resolved_routes","routing_basis","evidence_locators","segment_ids","review_status","empirical_credit","claim_extraction_blocked"}
MODES={"SOURCE_WIDE","SEGMENTED"}
BASES={"DEEP_VISUAL_REVIEW","SEGMENT_REGISTRY_VISUAL_REVIEW"}
LOC_RE=re.compile(r"^pdf:p(\d+)$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
STATE_VERSION="k2-unknown-textual-backlog-v1"
OUT=K/"K2_UNKNOWN_TEXTUAL_BACKLOG.json"
REGISTRY=K/"K2_SEMANTIC_DISCOVERY_ROUTING.jsonl"


def load_jsonl(path):
    rows=[]
    if not path.exists():return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:raise ValueError(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):raise ValueError(f"row must be object {path}:{n}")
        rows.append(r)
    return rows


def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):
            sid=r.get("source_id")
            if not isinstance(sid,str) or not sid:raise ValueError(f"missing source_id in {d}")
            if sid in out:raise ValueError(f"duplicate source_id {sid}")
            out[sid]=r
    if len(out)!=515:raise ValueError(f"canonical source count drift: {len(out)}")
    return out


def deep_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")}


def segments_by_source(root=ROOT):
    out=defaultdict(list)
    for r in load_jsonl(root/"knowledge"/"K2_SOURCE_SEGMENTS.jsonl"):
        out[r.get("source_id")].append(r)
    return out


def raw_unknown_ids(sources):
    return {
        sid for sid,src in sources.items()
        if src.get("evidence_role")=="TEXTUAL_SOURCE" and src.get("knowledge_domains")==["UNKNOWN"]
    }


def validate_corrections(root,sources,rows):
    issues=[];seen_ids=set();seen_sources=set();deep=deep_index(root);segments=segments_by_source(root)
    unknown=raw_unknown_ids(sources)
    for r in rows:
        rid=r.get("routing_id") or "<missing>";sid=r.get("source_id") or "<missing>"
        if set(r)!=ROW_FIELDS:issues.append((rid,f"fields mismatch missing={sorted(ROW_FIELDS-set(r))} extra={sorted(set(r)-ROW_FIELDS)}"))
        if rid in seen_ids:issues.append((rid,"duplicate routing_id"))
        seen_ids.add(rid)
        if sid in seen_sources:issues.append((rid,"one correction row allowed per source"))
        seen_sources.add(sid)
        src=sources.get(sid)
        if not src:issues.append((rid,"unknown source_id"));continue
        if sid not in unknown:issues.append((rid,"correction requires raw TEXTUAL_SOURCE knowledge_domains=[UNKNOWN]"))
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((rid,"canonical_sha256 mismatch"))
        if r.get("raw_knowledge_domains")!=["UNKNOWN"]:issues.append((rid,"raw_knowledge_domains must preserve [UNKNOWN]"))
        mode=r.get("routing_mode")
        if mode not in MODES:issues.append((rid,"invalid routing_mode"))
        basis=r.get("routing_basis")
        if basis not in BASES:issues.append((rid,"invalid routing_basis"))
        if mode=="SOURCE_WIDE" and basis!="DEEP_VISUAL_REVIEW":issues.append((rid,"SOURCE_WIDE requires DEEP_VISUAL_REVIEW"))
        if mode=="SEGMENTED" and basis!="SEGMENT_REGISTRY_VISUAL_REVIEW":issues.append((rid,"SEGMENTED requires SEGMENT_REGISTRY_VISUAL_REVIEW"))
        routes=r.get("resolved_routes")
        if not isinstance(routes,list) or not routes or len(routes)!=len(set(routes)) or any(x not in ROUTES for x in routes):
            issues.append((rid,"resolved_routes must be unique non-empty canonical routes"));routes=[]
        if "CARRIER_MATTER" in routes and mode!="SEGMENTED":issues.append((rid,"CARRIER_MATTER is only valid for SEGMENTED routing"))
        locs=r.get("evidence_locators")
        if not isinstance(locs,list) or not locs or len(locs)!=len(set(locs)):
            issues.append((rid,"evidence_locators must be unique non-empty array"));locs=[]
        read=deep.get(sid)
        if not read or read.get("read_status")!="COMPLETE" or read.get("verification_mode")!="VISUAL_PAGE":
            issues.append((rid,"discovery routing requires COMPLETE VISUAL_PAGE deep reading"))
        else:
            page_end=read.get("page_end")
            for loc in locs:
                m=LOC_RE.match(loc) if isinstance(loc,str) else None
                if not m:issues.append((rid,f"invalid evidence locator {loc!r}"));continue
                p=int(m.group(1))
                if not isinstance(page_end,int) or p<1 or p>page_end:issues.append((rid,f"evidence locator outside deep review: {loc}"))
        seg_ids=r.get("segment_ids")
        if not isinstance(seg_ids,list) or len(seg_ids)!=len(set(seg_ids)):
            issues.append((rid,"segment_ids must be unique array"));seg_ids=[]
        registered=segments.get(sid,[])
        if mode=="SOURCE_WIDE":
            if seg_ids:issues.append((rid,"SOURCE_WIDE must not carry segment_ids"))
            if registered:issues.append((rid,"SOURCE_WIDE cannot bypass an existing segment registry"))
            if any(x=="CARRIER_MATTER" for x in routes):issues.append((rid,"SOURCE_WIDE route cannot be carrier matter"))
        elif mode=="SEGMENTED":
            reg_ids={x.get("segment_id") for x in registered}
            if not registered:issues.append((rid,"SEGMENTED routing requires registered segments"))
            if set(seg_ids)!=reg_ids:issues.append((rid,"segment_ids must equal the full registered segment set"))
            route_union=set()
            for seg in registered:
                if seg.get("review_status")!="REVIEWED" or seg.get("verification_mode")!="VISUAL_PAGE":
                    issues.append((rid,f"segment not visually reviewed: {seg.get('segment_id')}"))
                srouters=seg.get("domain_routes")
                if not isinstance(srouters,list) or not srouters or any(x not in ROUTES for x in srouters):
                    issues.append((rid,f"segment has unresolved/invalid routes: {seg.get('segment_id')}"));continue
                route_union.update(srouters)
            if set(routes)!=route_union:issues.append((rid,f"resolved_routes must equal segment route union {sorted(route_union)}"))
        if r.get("review_status")!="REVIEWED":issues.append((rid,"review_status must be REVIEWED"))
        if r.get("empirical_credit")!="NONE":issues.append((rid,"empirical_credit must remain NONE"))
        if r.get("claim_extraction_blocked") is not True:issues.append((rid,"claim_extraction_blocked must remain true"))
        if PATH_RE.search(json.dumps(r,ensure_ascii=False)):issues.append((rid,"local filesystem path leaked"))
    return issues


def build_state(root=ROOT):
    sources=source_index(root);rows=load_jsonl(root/"knowledge"/"K2_SEMANTIC_DISCOVERY_ROUTING.jsonl")
    issues=validate_corrections(root,sources,rows)
    if issues:raise ValueError("; ".join(f"{a}: {b}" for a,b in issues[:20]))
    raw=raw_unknown_ids(sources);resolved={r["source_id"] for r in rows};remaining=raw-resolved
    return {
        "schema_version":STATE_VERSION,
        "raw_unknown_textual_source_count":len(raw),
        "resolved_by_k2_discovery_count":len(resolved),
        "remaining_unknown_textual_source_count":len(remaining),
        "resolved_source_ids":sorted(resolved),
        "claim_extraction_blocked":True,
        "generated_from":[
            "knowledge/domains/*/sources.jsonl",
            "knowledge/K2_SEMANTIC_DISCOVERY_ROUTING.jsonl",
            "knowledge/K2_DEEP_READING_LEDGER.jsonl",
            "knowledge/K2_SOURCE_SEGMENTS.jsonl",
        ],
    }


def render(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n"


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write",action="store_true");g.add_argument("--stdout",action="store_true")
    args=p.parse_args()
    try:text=render(build_state(ROOT))
    except ValueError as e:
        print(f"k2-semantic-discovery-routing: FAIL: {e}",file=sys.stderr);raise SystemExit(1)
    if args.write:
        OUT.write_text(text,encoding="utf-8");print(f"wrote {OUT.relative_to(ROOT)}")
    else:sys.stdout.write(text)


if __name__=="__main__":main()
