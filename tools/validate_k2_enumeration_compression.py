#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import Counter
from validate_k2_lineage_corrections import raw_lineage_index,effective_lineage_index

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
ALLOWED={"compression_id","source_id","work_id","canonical_sha256","enumeration_label","method_layer","input_domain","generative_rule_id","evidence_locators","enumerated_entries_count","collapsed_structure_units","empirical_evidence_units","compression_policy","reconstruction_test_status","source_credit","empirical_credit","claim_extraction_blocked","review_status"}
METHODS={"CALCULATION","DIVINATION","SELECTION_STRATEGY","MILITARY_OPERATIONAL","RITUAL_ESOTERIC","TRANSMITTED_REFERENCE"}
RECON={"UNTESTED","PASS","FAIL"}
STATE_VERSION="k2-qcic-v06-machine-gates-v1"

def fail(msg):
    print(f"k2-enumeration-compression: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

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

def load_state(path):
    if not path.exists():return None
    try:r=json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid state JSON {path}: {e}")
    return r

def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):out[r["source_id"]]=r
    return out

def lineage_index(root=ROOT):
    raw=raw_lineage_index(root)
    corrections=load_jsonl(root/"knowledge"/"K2_LINEAGE_CORRECTIONS.jsonl")
    return effective_lineage_index(raw,corrections)

def deep_reading_index(root=ROOT):
    return {r.get("source_id"):r for r in load_jsonl(root/"knowledge"/"K2_DEEP_READING_LEDGER.jsonl")}

def coverage_issues(rows,state):
    issues=[]
    if not isinstance(state,dict):return [("STATE","missing QCIC v0.6 gate state")]
    if state.get("schema_version")!=STATE_VERSION:issues.append(("STATE","unexpected schema_version"))
    if state.get("status")!="ACTIVE":issues.append(("STATE","status must be ACTIVE"))
    if state.get("claim_extraction_blocked") is not True:issues.append(("STATE","claim_extraction_blocked must be true"))
    targets=state.get("targets")
    if not isinstance(targets,list) or not targets:issues.append(("STATE","targets must be non-empty array"));return issues
    counts=Counter(r.get("source_id") for r in rows)
    seen=set()
    for t in targets:
        sid=t.get("source_id") if isinstance(t,dict) else None
        if not isinstance(sid,str) or not sid:issues.append(("STATE","target source_id required"));continue
        if sid in seen:issues.append((sid,"duplicate target"))
        seen.add(sid)
        cfg=t.get("enumeration_compression")
        if not isinstance(cfg,dict):issues.append((sid,"enumeration_compression target config required"));continue
        required=cfg.get("required")
        minimum=cfg.get("minimum_rows")
        if not isinstance(required,bool):issues.append((sid,"enumeration_compression.required must be bool"))
        if not isinstance(minimum,int) or minimum<0:issues.append((sid,"enumeration_compression.minimum_rows must be non-negative int"));continue
        if required and counts.get(sid,0)<minimum:issues.append((sid,f"required enumeration compression rows missing: have={counts.get(sid,0)} need>={minimum}"))
    return issues

def validate_rows(sources,lineage,deep,rows):
    issues=[];ids=set();keys=set()
    for r in rows:
        rid=r.get("compression_id") or "<missing>";sid=r.get("source_id") or "<missing>"
        if rid in ids:issues.append((rid,"duplicate compression_id"))
        ids.add(rid)
        key=(sid,r.get("enumeration_label"))
        if key in keys:issues.append((rid,"duplicate source/enumeration_label"))
        keys.add(key)
        extra=set(r)-ALLOWED
        if extra:issues.append((rid,f"unexpected fields: {sorted(extra)}"))
        src=sources.get(sid);lin=lineage.get(sid);read=deep.get(sid)
        if not src:issues.append((rid,"unknown source_id"));continue
        if not lin:issues.append((rid,"missing effective lineage row"));continue
        if r.get("work_id")!=lin.get("work_id"):issues.append((rid,"work_id mismatch with effective lineage"))
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((rid,"canonical_sha256 mismatch"))
        for f in ("enumeration_label","input_domain","generative_rule_id"):
            if not isinstance(r.get(f),str) or not r.get(f).strip():issues.append((rid,f"{f} must be non-empty"))
        if r.get("method_layer") not in METHODS:issues.append((rid,"invalid method_layer"))
        n=r.get("enumerated_entries_count")
        if not isinstance(n,int) or n<2:issues.append((rid,"enumerated_entries_count must be >=2"))
        if r.get("collapsed_structure_units")!=1:issues.append((rid,"collapsed_structure_units must be 1"))
        if r.get("empirical_evidence_units")!=0:issues.append((rid,"empirical_evidence_units must be 0"))
        if r.get("compression_policy")!="DERIVED_ENUMERATION_COLLAPSE":issues.append((rid,"compression_policy must be DERIVED_ENUMERATION_COLLAPSE"))
        if r.get("reconstruction_test_status") not in RECON:issues.append((rid,"invalid reconstruction_test_status"))
        if r.get("source_credit")!="SOURCE_STRUCTURE_ONLY":issues.append((rid,"source_credit must be SOURCE_STRUCTURE_ONLY"))
        if r.get("empirical_credit")!="NONE":issues.append((rid,"empirical_credit must be NONE"))
        if r.get("claim_extraction_blocked") is not True:issues.append((rid,"claim_extraction_blocked must be true"))
        if r.get("review_status")!="REVIEWED":issues.append((rid,"review_status must be REVIEWED"))
        locs=r.get("evidence_locators")
        if not isinstance(locs,list) or not locs or len(locs)!=len(set(locs)):
            issues.append((rid,"evidence_locators must be non-empty unique array"));locs=[]
        if not read or read.get("read_status")!="COMPLETE" or read.get("verification_mode")!="VISUAL_PAGE":
            issues.append((rid,"enumeration compression requires COMPLETE VISUAL_PAGE deep reading"))
        else:
            page_end=read.get("page_end")
            for loc in locs:
                m=LOC_RE.match(loc) if isinstance(loc,str) else None
                if not m:issues.append((rid,f"invalid evidence locator {loc!r}"));continue
                p=int(m.group(1))
                if not isinstance(page_end,int) or p<1 or p>page_end:issues.append((rid,f"evidence locator outside reviewed pages: {loc}"))
        if PATH_RE.search(json.dumps(r,ensure_ascii=False)):issues.append((rid,"local filesystem path leaked"))
    return issues

def main():
    rows=load_jsonl(K/"K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl")
    state=load_state(K/"K2_QCIC_V06_GATE_STATE.json")
    issues=validate_rows(source_index(),lineage_index(),deep_reading_index(),rows)+coverage_issues(rows,state)
    if issues:fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-enumeration-compression: PASS")
    print(f"rows={len(rows)} collapsed_entries={sum(r.get('enumerated_entries_count',0) for r in rows)} required_targets={len(state.get('targets',[]))} issues=0")
if __name__=="__main__":main()
