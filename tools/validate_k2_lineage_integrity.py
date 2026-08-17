#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_source_lineage as v

ROOT=Path(__file__).resolve().parents[1]

def fail(msg):
    print(f"k2-lineage-integrity: FAIL: {msg}",file=sys.stderr); raise SystemExit(1)

def main():
    repo=ROOT; k=repo/"knowledge"
    project=v.load_json(k/"PROJECT_STATE.json")
    state=v.load_json(k/"K2_SOURCE_LINEAGE_STATE.json")
    if state.get("status")!="COMPLETE": fail("post-K2A phases require COMPLETE lineage state")
    if not str(project.get("phase","")).startswith("K2_"): fail("lineage integrity only applies in K2")
    sources,counts=v.source_index(repo)
    if sum(counts.values())!=515: fail("canonical source total drift")
    rows=v.load_jsonl(k/"K2_SOURCE_LINEAGE.jsonl")
    if len(rows)!=515: fail(f"lineage row count {len(rows)} != 515")
    by_sid={};issues=[]
    for r in rows:
        sid=r.get("source_id")
        if sid in by_sid: issues.append((sid or "<missing>","duplicate lineage row"));continue
        by_sid[sid]=r
        src=sources.get(sid)
        if not src: issues.append((sid or "<missing>","unknown source_id"));continue
        issues.extend(v.inspect(r,src))
    if set(by_sid)!=set(sources): issues.append(("<global>","lineage/source id set mismatch"))
    by_work={}
    for r in rows:
        if r.get("work_id"): by_work.setdefault(r["work_id"],[]).append(r)
    for wid,members in by_work.items():
        if sum(1 for r in members if r.get("independence_class")=="PRIMARY_CANDIDATE")>1:
            issues.append((wid,"more than one PRIMARY_CANDIDATE"))
        labels=set()
        for r in members:
            if r.get("relation")=="WORK_PART":
                label=r.get("part_label")
                if label in labels: issues.append((r.get("source_id") or wid,"duplicate WORK_PART part_label"))
                labels.add(label)
    for r in rows:
        if r.get("relation")!="SAME_WORK_VARIANT": continue
        sid=r.get("source_id");target=by_sid.get(r.get("variant_of_source_id"))
        if not target: issues.append((sid,"variant target missing"));continue
        if target.get("work_id")!=r.get("work_id"): issues.append((sid,"variant target work_id mismatch"))
        if target.get("relation") not in {"PRIMARY_WORK","WORK_PART"}: issues.append((sid,"variant target must be PRIMARY_WORK/WORK_PART"))
        if target.get("relation")=="WORK_PART" and r.get("part_label")!=target.get("part_label"):
            issues.append((sid,"variant part_label mismatch"))
    if issues:
        fail(f"{len(issues)} issue(s); "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-lineage-integrity: PASS")
    print("sources=515 lineage_rows=515 issues=0")

if __name__=="__main__": main()
