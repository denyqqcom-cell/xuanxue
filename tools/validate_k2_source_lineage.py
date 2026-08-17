#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
EXPECTED = {"ziwei":148,"bazi":168,"qimen":154,"liuyao":7,"liuren":10,"fengshui":28}
RELATIONS = {"PRIMARY_WORK","SAME_WORK_VARIANT","COMMENTARY_DERIVATIVE","SECONDARY_NOTE","IMPLEMENTATION","AUXILIARY_INDEX","OUT_OF_SCOPE","UNKNOWN"}
INDEPENDENCE = {"PRIMARY_CANDIDATE","SAME_WORK_NOT_INDEPENDENT","DERIVATIVE_REVIEW_REQUIRED","IMPLEMENTATION_ONLY","NOT_ELIGIBLE","UNKNOWN"}
BASIS = {"TITLE_MATCH","CONTENT_VERIFIED","MANUAL_VERIFIED","HASH_PROVENANCE","PROJECT_CODE_PATH","UNKNOWN"}
PRIORITY = {"P0","P1","P2","P3","SKIP"}
REVIEW = {"UNREVIEWED","REVIEWED","BLOCKED"}


def fail(msg):
    print(f"k2-source-lineage: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot parse {path}: {e}")


def load_jsonl(path):
    rows=[]
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():
            continue
        try:
            row=json.loads(raw)
        except Exception as e:
            fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row,dict):
            fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows


def source_index(repo):
    out={}
    counts={}
    for d in DOMAINS:
        rows=load_jsonl(repo/"knowledge"/"domains"/d/"sources.jsonl")
        counts[d]=len(rows)
        if counts[d] != EXPECTED[d]:
            fail(f"registry count drift for {d}: {counts[d]} != {EXPECTED[d]}")
        for row in rows:
            sid=row.get("source_id")
            if not isinstance(sid,str) or not sid:
                fail(f"missing source_id in {d}")
            if sid in out:
                fail(f"duplicate canonical source_id across registries: {sid}")
            out[sid]=row
    return out, counts


def inspect(row, source):
    sid=source["source_id"]
    issues=[]
    if row.get("source_id") != sid:
        issues.append("source_id mismatch")
    relation=row.get("relation")
    independence=row.get("independence_class")
    basis=row.get("lineage_basis")
    priority=row.get("read_priority")
    review=row.get("review_status")
    parents=row.get("parent_work_ids")
    evidence=row.get("lineage_evidence")
    work=row.get("work_id")
    eligible=row.get("k2_eligible")
    if relation not in RELATIONS: issues.append("invalid relation")
    if independence not in INDEPENDENCE: issues.append("invalid independence_class")
    if basis not in BASIS: issues.append("invalid lineage_basis")
    if priority not in PRIORITY: issues.append("invalid read_priority")
    if review not in REVIEW: issues.append("invalid review_status")
    if not isinstance(parents,list) or len(parents)!=len(set(parents)): issues.append("parent_work_ids must be unique array")
    if not isinstance(eligible,bool): issues.append("k2_eligible must be boolean")
    if work is not None and (not isinstance(work,str) or not work.strip()): issues.append("work_id must be string or null")
    if isinstance(parents,list) and work and work in parents: issues.append("work_id cannot be its own parent")
    if basis == "UNKNOWN":
        if evidence not in (None,""): issues.append("UNKNOWN basis must not claim lineage evidence")
    else:
        if not isinstance(evidence,str) or not evidence.strip() or len(evidence)>240: issues.append("resolved lineage requires short evidence")
    if relation == "UNKNOWN":
        if independence != "UNKNOWN": issues.append("UNKNOWN relation requires UNKNOWN independence")
        if basis != "UNKNOWN": issues.append("UNKNOWN relation requires UNKNOWN basis")
    if relation == "OUT_OF_SCOPE":
        if eligible is not False or priority != "SKIP" or independence != "NOT_ELIGIBLE": issues.append("OUT_OF_SCOPE must be non-eligible/SKIP/NOT_ELIGIBLE")
    if relation == "AUXILIARY_INDEX":
        if eligible is not False or independence != "NOT_ELIGIBLE": issues.append("AUXILIARY_INDEX must be non-eligible/NOT_ELIGIBLE")
    if relation == "SAME_WORK_VARIANT" and independence != "SAME_WORK_NOT_INDEPENDENT": issues.append("same-work variant cannot count independently")
    role=source.get("evidence_role")
    if role == "SECONDARY_NOTE" and relation != "SECONDARY_NOTE": issues.append("secondary note must remain SECONDARY_NOTE")
    if role == "SECONDARY_NOTE" and independence == "PRIMARY_CANDIDATE": issues.append("secondary note cannot be primary independent evidence")
    if role == "IMPLEMENTATION_EVIDENCE":
        if relation != "IMPLEMENTATION" or independence != "IMPLEMENTATION_ONLY": issues.append("implementation evidence must remain IMPLEMENTATION/IMPLEMENTATION_ONLY")
    if role == "AUXILIARY_INDEX" and relation != "AUXILIARY_INDEX": issues.append("auxiliary index must remain AUXILIARY_INDEX")
    kd=source.get("knowledge_domains")
    if kd == ["OUT_OF_SCOPE"] and relation != "OUT_OF_SCOPE": issues.append("OUT_OF_SCOPE source must remain out of K2 textual lane")
    return [(sid,x) for x in issues]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",type=Path,default=ROOT)
    ap.add_argument("--force",action="store_true")
    args=ap.parse_args()
    repo=args.repo_root.resolve()
    k=repo/"knowledge"
    project=load_json(k/"PROJECT_STATE.json")
    state=load_json(k/"K2_SOURCE_LINEAGE_STATE.json")
    sources, counts=source_index(repo)
    if sum(counts.values()) != 515 or state.get("total_sources") != 515:
        fail("K2 lineage source total must remain 515")
    if project.get("phase") != "K2_SOURCE_LINEAGE":
        fail("validator is only valid during K2_SOURCE_LINEAGE")
    if project.get("k1_acceptance") != "PROJECT_VERIFIED" or project.get("k2_blocked") is not False:
        fail("K2 cannot start before project-verified K1 closure")
    if project.get("claim_extraction_blocked") is not True or state.get("claim_extraction_blocked") is not True:
        fail("claim extraction must remain blocked during source-lineage stage")

    target=k/"K2_SOURCE_LINEAGE.jsonl"
    status=state.get("status")
    if not target.exists():
        if status == "REVIEW_REQUIRED" and not args.force:
            print("k2-source-lineage: REVIEW_REQUIRED")
            print("sources=515 lineage_rows=0 claim_extraction_blocked=true")
            return
        fail("public K2_SOURCE_LINEAGE.jsonl missing")

    rows=load_jsonl(target)
    seen=set(); issues=[]
    for row in rows:
        sid=row.get("source_id")
        if sid in seen: issues.append((sid or "<missing>","duplicate lineage row")); continue
        seen.add(sid)
        src=sources.get(sid)
        if not src: issues.append((sid or "<missing>","unknown source_id")); continue
        issues.extend(inspect(row,src))
    missing=set(sources)-seen
    extra=seen-set(sources)
    if missing: issues.append(("<global>",f"missing {len(missing)} canonical source rows"))
    if extra: issues.append(("<global>",f"extra {len(extra)} lineage source ids"))

    by_work={}
    for row in rows:
        wid=row.get("work_id")
        if wid:
            by_work.setdefault(wid,[]).append(row)
    for wid, members in by_work.items():
        prim=[r for r in members if r.get("independence_class")=="PRIMARY_CANDIDATE"]
        if len(prim)>1:
            issues.append((wid,"more than one PRIMARY_CANDIDATE in same work family"))

    if issues:
        sample="; ".join(f"{sid}: {msg}" for sid,msg in issues[:20])
        if status == "REVIEW_REQUIRED" and not args.force:
            print("k2-source-lineage: REVIEW_REQUIRED")
            print(f"sources=515 lineage_rows={len(rows)} issues={len(issues)}")
            print(sample)
            return
        fail(f"{len(issues)} issue(s); {sample}")

    if len(rows)!=515:
        fail(f"lineage row count {len(rows)} != 515")
    if status == "COMPLETE":
        print("k2-source-lineage: PASS")
        print("sources=515 lineage_rows=515 issues=0")
        return
    if args.force:
        fail("lineage data passes but state is not COMPLETE")
    print("k2-source-lineage: REVIEW_REQUIRED")
    print("sources=515 lineage_rows=515 issues=0; promote state only after project review")

if __name__=="__main__":
    main()
