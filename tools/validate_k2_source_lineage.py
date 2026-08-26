#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
EXPECTED = {"ziwei":148,"bazi":168,"qimen":154,"liuyao":7,"liuren":10,"fengshui":28}
RELATIONS = {"PRIMARY_WORK","WORK_PART","SAME_WORK_VARIANT","COMMENTARY_DERIVATIVE","SECONDARY_NOTE","IMPLEMENTATION","AUXILIARY_INDEX","OUT_OF_SCOPE","UNKNOWN"}
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
    part_label=row.get("part_label")
    variant_of=row.get("variant_of_source_id")

    if relation not in RELATIONS: issues.append("invalid relation")
    if independence not in INDEPENDENCE: issues.append("invalid independence_class")
    if basis not in BASIS: issues.append("invalid lineage_basis")
    if priority not in PRIORITY: issues.append("invalid read_priority")
    if review not in REVIEW: issues.append("invalid review_status")
    if not isinstance(parents,list) or len(parents)!=len(set(parents)): issues.append("parent_work_ids must be unique array")
    if not isinstance(eligible,bool): issues.append("k2_eligible must be boolean")
    if work is not None and (not isinstance(work,str) or not work.strip()): issues.append("work_id must be string or null")
    if part_label is not None and (not isinstance(part_label,str) or not part_label.strip() or len(part_label)>120): issues.append("part_label must be null or short non-empty string")
    if variant_of is not None and (not isinstance(variant_of,str) or not variant_of.strip()): issues.append("variant_of_source_id must be null or source id")
    if variant_of == sid: issues.append("variant cannot point to itself")
    if isinstance(parents,list) and work and work in parents: issues.append("work_id cannot be its own parent")

    if basis == "UNKNOWN":
        if evidence not in (None,""): issues.append("UNKNOWN basis must not claim lineage evidence")
    else:
        if not isinstance(evidence,str) or not evidence.strip() or len(evidence)>240: issues.append("resolved lineage requires short evidence")

    if relation == "PRIMARY_WORK":
        if work is None: issues.append("PRIMARY_WORK requires work_id")
        if independence != "PRIMARY_CANDIDATE": issues.append("PRIMARY_WORK requires PRIMARY_CANDIDATE")
        if eligible is not True: issues.append("PRIMARY_WORK must be K2 eligible")
        if part_label is not None: issues.append("PRIMARY_WORK cannot carry part_label")
        if variant_of is not None: issues.append("PRIMARY_WORK cannot be a variant")

    if relation == "WORK_PART":
        if work is None: issues.append("WORK_PART requires work_id")
        if independence != "SAME_WORK_NOT_INDEPENDENT": issues.append("WORK_PART is not an independent work vote")
        if eligible is not True: issues.append("WORK_PART must remain K2 eligible so unique part content is not dropped")
        if not isinstance(part_label,str) or not part_label.strip(): issues.append("WORK_PART requires part_label")
        if variant_of is not None: issues.append("WORK_PART cannot itself be a variant")

    if relation == "SAME_WORK_VARIANT":
        if work is None: issues.append("SAME_WORK_VARIANT requires work_id")
        if independence != "SAME_WORK_NOT_INDEPENDENT": issues.append("same-work variant cannot count independently")
        if not isinstance(variant_of,str) or not variant_of.strip(): issues.append("SAME_WORK_VARIANT requires variant_of_source_id")

    if relation == "COMMENTARY_DERIVATIVE":
        if independence != "DERIVATIVE_REVIEW_REQUIRED": issues.append("commentary derivative requires DERIVATIVE_REVIEW_REQUIRED")
        if not isinstance(parents,list) or not parents: issues.append("commentary derivative requires parent_work_ids")

    if relation == "SECONDARY_NOTE":
        if independence != "NOT_ELIGIBLE" or eligible is not False: issues.append("SECONDARY_NOTE must be non-eligible/NOT_ELIGIBLE")
        if priority != "SKIP": issues.append("SECONDARY_NOTE must be SKIP in textual reading lane")

    if relation == "IMPLEMENTATION":
        if independence != "IMPLEMENTATION_ONLY" or eligible is not False: issues.append("IMPLEMENTATION must be non-eligible/IMPLEMENTATION_ONLY")
        if priority != "SKIP": issues.append("IMPLEMENTATION must be SKIP in textual reading lane")

    if relation == "AUXILIARY_INDEX":
        if eligible is not False or independence != "NOT_ELIGIBLE" or priority != "SKIP": issues.append("AUXILIARY_INDEX must be non-eligible/SKIP/NOT_ELIGIBLE")

    if relation == "OUT_OF_SCOPE":
        if eligible is not False or priority != "SKIP" or independence != "NOT_ELIGIBLE": issues.append("OUT_OF_SCOPE must be non-eligible/SKIP/NOT_ELIGIBLE")

    if relation == "UNKNOWN":
        if independence != "UNKNOWN": issues.append("UNKNOWN relation requires UNKNOWN independence")
        if basis != "UNKNOWN": issues.append("UNKNOWN relation requires UNKNOWN basis")
        if eligible is not False: issues.append("UNKNOWN relation must remain non-eligible until resolved")
        if variant_of is not None or part_label is not None: issues.append("UNKNOWN relation cannot claim part/variant structure")

    role=source.get("evidence_role")
    if role == "SECONDARY_NOTE":
        if relation != "SECONDARY_NOTE": issues.append("secondary note must remain SECONDARY_NOTE")
        if independence == "PRIMARY_CANDIDATE": issues.append("secondary note cannot be primary independent evidence")
    if role == "IMPLEMENTATION_EVIDENCE":
        if relation != "IMPLEMENTATION" or independence != "IMPLEMENTATION_ONLY": issues.append("implementation evidence must remain IMPLEMENTATION/IMPLEMENTATION_ONLY")
    if role == "AUXILIARY_INDEX" and relation != "AUXILIARY_INDEX": issues.append("auxiliary index must remain AUXILIARY_INDEX")

    kd=source.get("knowledge_domains")
    if kd == ["OUT_OF_SCOPE"]:
        if eligible is not False or priority != "SKIP": issues.append("OUT_OF_SCOPE semantic source must not enter six-domain reading lane")
        if role == "TEXTUAL_SOURCE" and relation != "OUT_OF_SCOPE": issues.append("OUT_OF_SCOPE textual source must remain OUT_OF_SCOPE")
        if role == "IMPLEMENTATION_EVIDENCE" and relation != "IMPLEMENTATION": issues.append("OUT_OF_SCOPE code remains IMPLEMENTATION, not textual evidence")
        if role == "SECONDARY_NOTE" and relation != "SECONDARY_NOTE": issues.append("OUT_OF_SCOPE note remains SECONDARY_NOTE")
        if role == "AUXILIARY_INDEX" and relation != "AUXILIARY_INDEX": issues.append("OUT_OF_SCOPE index remains AUXILIARY_INDEX")

    if kd == ["UNKNOWN"]:
        if role == "TEXTUAL_SOURCE" and relation != "UNKNOWN": issues.append("UNKNOWN semantic textual source must remain UNKNOWN until routed")
        if role in {"SECONDARY_NOTE","IMPLEMENTATION_EVIDENCE","AUXILIARY_INDEX"} and eligible is not False:
            issues.append("UNKNOWN semantic non-text source cannot enter textual reading lane")

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
    seen=set(); issues=[]; rows_by_sid={}
    for row in rows:
        sid=row.get("source_id")
        if sid in seen:
            issues.append((sid or "<missing>","duplicate lineage row")); continue
        seen.add(sid)
        rows_by_sid[sid]=row
        src=sources.get(sid)
        if not src:
            issues.append((sid or "<missing>","unknown source_id")); continue
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
        part_labels={}
        for r in members:
            if r.get("relation")=="WORK_PART":
                label=r.get("part_label")
                if label in part_labels:
                    issues.append((r.get("source_id") or wid,f"duplicate WORK_PART label {label!r}; use SAME_WORK_VARIANT for alternate carriers of the same part"))
                else:
                    part_labels[label]=r.get("source_id")

    for row in rows:
        if row.get("relation") != "SAME_WORK_VARIANT":
            continue
        sid=row.get("source_id")
        target_id=row.get("variant_of_source_id")
        target=rows_by_sid.get(target_id)
        if not target:
            issues.append((sid,"variant_of_source_id must reference another canonical lineage row")); continue
        if target.get("work_id") != row.get("work_id"):
            issues.append((sid,"variant and target must share work_id"))
        if target.get("relation") not in {"PRIMARY_WORK","WORK_PART"}:
            issues.append((sid,"variant must point directly to PRIMARY_WORK or WORK_PART, not another variant"))
        if target.get("relation")=="PRIMARY_WORK" and row.get("part_label") is not None:
            issues.append((sid,"complete-work variant must not carry part_label"))
        if target.get("relation")=="WORK_PART" and row.get("part_label") != target.get("part_label"):
            issues.append((sid,"part variant must carry the same part_label as its WORK_PART target"))

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
