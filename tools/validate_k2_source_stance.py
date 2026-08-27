#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import Counter,defaultdict
from validate_k2_lineage_corrections import raw_lineage_index,effective_lineage_index

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
ALLOWED={"stance_id","source_id","work_id","canonical_sha256","topic_key","stance","evidence_locators","stance_basis","stance_precedence","supersedes_stance_ids","author_method_pool_eligible","empirical_credit","claim_extraction_blocked","review_status"}
STANCES={"SOURCE_REPORTS","SOURCE_ENDORSES","SOURCE_REJECTS","SOURCE_UNCERTAIN"}
BASES={"VISUAL_PAGE","TEXT_LAYER"}
STATE_VERSION="k2-qcic-v06-machine-gates-v1"

def fail(msg):
    print(f"k2-source-stance: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

def load_jsonl(path):
    rows=[]
    if not path.exists(): return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip(): continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows

def load_state(path):
    if not path.exists():return None
    try:r=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid state JSON {path}: {e}")
    return r

def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):
            sid=r.get("source_id")
            if sid in out:fail(f"duplicate source_id {sid}")
            out[sid]=r
    return out

def lineage_index(root=ROOT):
    raw=raw_lineage_index(root)
    corrections=load_jsonl(root/"knowledge"/"K2_LINEAGE_CORRECTIONS.jsonl")
    return effective_lineage_index(raw,corrections)

def deep_reading_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")}

def effective_stance_rows(rows):
    by_topic=defaultdict(list);superseded=set()
    for r in rows:
        by_topic[(r.get("source_id"),r.get("topic_key"))].append(r)
        superseded.update(r.get("supersedes_stance_ids") or [])
    out=[]
    for key,group in by_topic.items():
        leaves=[r for r in group if r.get("stance_id") not in superseded]
        if len(leaves)!=1:
            raise ValueError(f"ambiguous effective stance for {key}: leaves={[r.get('stance_id') for r in leaves]}")
        out.append(leaves[0])
    return sorted(out,key=lambda r:(r.get("source_id") or "",r.get("topic_key") or "",r.get("stance_id") or ""))

def coverage_issues(rows,state):
    issues=[]
    if not isinstance(state,dict):return [("STATE","missing QCIC v0.6 gate state")]
    if state.get("schema_version")!=STATE_VERSION:issues.append(("STATE","unexpected schema_version"))
    if state.get("status")!="ACTIVE":issues.append(("STATE","status must be ACTIVE"))
    if state.get("claim_extraction_blocked") is not True:issues.append(("STATE","claim_extraction_blocked must be true"))
    targets=state.get("targets")
    if not isinstance(targets,list) or not targets:issues.append(("STATE","targets must be non-empty array"));return issues

    try:
        effective=effective_stance_rows(rows)
    except ValueError:
        effective=[]
    counts=Counter(r.get("source_id") for r in effective)
    by_topic={(r.get("source_id"),r.get("topic_key")):r for r in effective}
    seen=set()
    for t in targets:
        sid=t.get("source_id") if isinstance(t,dict) else None
        if not isinstance(sid,str) or not sid:issues.append(("STATE","target source_id required"));continue
        if sid in seen:issues.append((sid,"duplicate target"))
        seen.add(sid)
        cfg=t.get("source_stance")
        if not isinstance(cfg,dict):issues.append((sid,"source_stance target config required"));continue
        required=cfg.get("required");minimum=cfg.get("minimum_rows")
        if not isinstance(required,bool):issues.append((sid,"source_stance.required must be bool"))
        if not isinstance(minimum,int) or minimum<0:issues.append((sid,"source_stance.minimum_rows must be non-negative int"));continue

        topic_keys=cfg.get("required_topic_keys")
        if not isinstance(topic_keys,list) or len(topic_keys)!=len(set(topic_keys)) or any(not isinstance(x,str) or not x.strip() for x in topic_keys):
            issues.append((sid,"source_stance.required_topic_keys must be a unique string array"));topic_keys=[]
        expected=cfg.get("required_topic_stances")
        if not isinstance(expected,dict):
            issues.append((sid,"source_stance.required_topic_stances must be an object"));expected={}
        else:
            if any(not isinstance(k,str) or not k.strip() for k in expected):issues.append((sid,"required_topic_stances keys must be non-empty strings"))
            if any(v not in STANCES for v in expected.values()):issues.append((sid,"required_topic_stances contains invalid stance"))
            if set(expected)!=set(topic_keys):issues.append((sid,"required_topic_stances keys must exactly match required_topic_keys"))

        if required:
            if not topic_keys:issues.append((sid,"required source stance target must freeze required_topic_keys"))
            if counts.get(sid,0)<minimum:issues.append((sid,f"required effective source stance rows missing: have={counts.get(sid,0)} need>={minimum}"))
            for topic in topic_keys:
                leaf=by_topic.get((sid,topic))
                if leaf is None:
                    issues.append((sid,f"required source stance topic missing: {topic}"));continue
                want=expected.get(topic)
                if want in STANCES and leaf.get("stance")!=want:
                    issues.append((sid,f"required source stance topic changed: {topic} expected={want} actual={leaf.get('stance')}"))
    return issues

def validate_rows(sources,lineage,deep,rows):
    issues=[];ids=set();by_id={};by_topic=defaultdict(list);superseded=set()
    for r in rows:
        rid=r.get("stance_id") or "<missing>";sid=r.get("source_id") or "<missing>"
        if rid in ids:issues.append((rid,"duplicate stance_id"))
        ids.add(rid);by_id[rid]=r;by_topic[(sid,r.get("topic_key"))].append(r)
        extra=set(r)-ALLOWED
        if extra:issues.append((rid,f"unexpected fields: {sorted(extra)}"))
        src=sources.get(sid);lin=lineage.get(sid);read=deep.get(sid)
        if not src:issues.append((rid,"unknown source_id"));continue
        if not lin:issues.append((rid,"missing effective lineage row"));continue
        if r.get("work_id")!=lin.get("work_id"):issues.append((rid,"work_id mismatch with effective lineage"))
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((rid,"canonical_sha256 mismatch"))
        stance=r.get("stance")
        if stance not in STANCES:issues.append((rid,"invalid stance"))
        if r.get("stance_basis") not in BASES:issues.append((rid,"invalid stance_basis"))
        if not isinstance(r.get("topic_key"),str) or not r.get("topic_key").strip():issues.append((rid,"topic_key must be non-empty"))
        if not isinstance(r.get("stance_precedence"),int) or r.get("stance_precedence")<0:issues.append((rid,"stance_precedence must be non-negative int"))
        supers=r.get("supersedes_stance_ids")
        if not isinstance(supers,list) or len(supers)!=len(set(supers)):issues.append((rid,"supersedes_stance_ids must be unique array"));supers=[]
        superseded.update(x for x in supers if isinstance(x,str))
        eligible=r.get("author_method_pool_eligible")
        if not isinstance(eligible,bool):issues.append((rid,"author_method_pool_eligible must be bool"))
        if stance in {"SOURCE_REPORTS","SOURCE_REJECTS","SOURCE_UNCERTAIN"} and eligible is not False:
            issues.append((rid,f"{stance} must not enter author method pool"))
        if r.get("empirical_credit")!="NONE":issues.append((rid,"empirical_credit must be NONE"))
        if r.get("claim_extraction_blocked") is not True:issues.append((rid,"claim_extraction_blocked must be true"))
        if r.get("review_status")!="REVIEWED":issues.append((rid,"review_status must be REVIEWED"))
        locs=r.get("evidence_locators")
        if not isinstance(locs,list) or not locs or len(locs)!=len(set(locs)):
            issues.append((rid,"evidence_locators must be non-empty unique array"));locs=[]
        if not read or read.get("read_status")!="COMPLETE" or read.get("verification_mode")!="VISUAL_PAGE":
            issues.append((rid,"source stance requires COMPLETE VISUAL_PAGE deep reading"))
        else:
            page_end=read.get("page_end")
            for loc in locs:
                m=LOC_RE.match(loc) if isinstance(loc,str) else None
                if not m:issues.append((rid,f"invalid evidence locator {loc!r}"));continue
                p=int(m.group(1))
                if not isinstance(page_end,int) or p<1 or p>page_end:issues.append((rid,f"evidence locator outside reviewed pages: {loc}"))
        if PATH_RE.search(json.dumps(r,ensure_ascii=False)):issues.append((rid,"local filesystem path leaked"))

    for r in rows:
        rid=r.get("stance_id") or "<missing>"
        for prev in r.get("supersedes_stance_ids") or []:
            target=by_id.get(prev)
            if not target:issues.append((rid,f"supersedes unknown stance {prev}"));continue
            if target.get("source_id")!=r.get("source_id") or target.get("topic_key")!=r.get("topic_key"):
                issues.append((rid,"superseded stance must share source_id and topic_key"))
            if isinstance(target.get("stance_precedence"),int) and isinstance(r.get("stance_precedence"),int) and r["stance_precedence"]<=target["stance_precedence"]:
                issues.append((rid,"superseding stance must have higher precedence"))

    for key,group in by_topic.items():
        leaves=[r for r in group if r.get("stance_id") not in superseded]
        if len(leaves)!=1:
            issues.append((f"{key[0]}:{key[1]}",f"effective stance must resolve to exactly one leaf, found={len(leaves)}"))
    return issues

def main():
    rows=load_jsonl(K/"K2_SOURCE_STANCE_REGISTRY.jsonl")
    state=load_state(K/"K2_QCIC_V06_GATE_STATE.json")
    issues=validate_rows(source_index(),lineage_index(),deep_reading_index(),rows)+coverage_issues(rows,state)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-source-stance: PASS")
    print(f"rows={len(rows)} effective_topics={len(effective_stance_rows(rows))} required_targets={len(state.get('targets',[]))} issues=0")
if __name__=="__main__":main()
