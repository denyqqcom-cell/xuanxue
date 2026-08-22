#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
REQUIRED_LIST_FIELDS=[
    "essence","method_map","applicability_constraints","source_limitations",
    "conflicts_and_tensions","anti_patterns","model_updates","testable_hypotheses",
    "excluded_from_operational_use",
]
NONEMPTY_LIST_FIELDS={"essence","method_map","source_limitations","model_updates"}
ALLOWED_FIELDS={
    "distillate_id","source_id","work_id","domain","distillation_scope",
    "source_read_status","evidence_count","evidence_anchor_refs","essence",
    "method_map","applicability_constraints","source_limitations",
    "conflicts_and_tensions","anti_patterns","model_updates","testable_hypotheses",
    "excluded_from_operational_use","distillation_status","review_status",
    "copyright_class",
}


def fail(msg):
    print(f"k2-book-distillates: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:fail(f"cannot parse {path}: {e}")


def load_jsonl(path):
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows


def validate_rows(ledger,evidence,distillates):
    issues=[]
    complete={}
    for r in ledger:
        sid=r.get("source_id")
        if r.get("read_status")=="COMPLETE":
            if sid in complete:issues.append((sid or "<missing>","duplicate COMPLETE ledger source"))
            complete[sid]=r

    ev_by_source=Counter()
    ev_ids={}
    ev_domains={}
    for e in evidence:
        eid=e.get("evidence_id");sid=e.get("source_id")
        if isinstance(eid,str) and eid:
            ev_ids[eid]=sid
        if sid:
            ev_by_source[sid]+=1
            if e.get("domain") and e.get("domain")!="common":ev_domains.setdefault(sid,set()).add(e.get("domain"))

    source_rows={}
    distillate_ids=set()
    for d in distillates:
        sid=d.get("source_id");did=d.get("distillate_id")
        if not isinstance(did,str) or not did.strip():issues.append((sid or "<missing>","missing distillate_id"))
        elif did in distillate_ids:issues.append((did,"duplicate distillate_id"))
        else:distillate_ids.add(did)
        if sid in source_rows:issues.append((sid or "<missing>","duplicate distillate source_id"))
        source_rows[sid]=d

        unknown=set(d)-ALLOWED_FIELDS
        if unknown:issues.append((sid or "<missing>",f"unexpected distillate fields: {sorted(unknown)}"))
        if sid not in complete:
            issues.append((sid or "<missing>","final distillate requires COMPLETE reading source"))
            continue
        l=complete[sid]
        if d.get("work_id")!=l.get("work_id"):issues.append((sid,"distillate work_id mismatch"))
        if d.get("distillation_scope")!="SOURCE_BOOK":issues.append((sid,"distillation_scope must be SOURCE_BOOK"))
        if d.get("source_read_status")!="COMPLETE":issues.append((sid,"source_read_status must be COMPLETE"))
        if d.get("distillation_status")!="REVIEWED" or d.get("review_status")!="REVIEWED":issues.append((sid,"distillate must be REVIEWED"))
        if d.get("copyright_class")!="DERIVED_SYNTHESIS_SAFE":issues.append((sid,"copyright_class must be DERIVED_SYNTHESIS_SAFE"))

        actual_count=ev_by_source.get(sid,0)
        if d.get("evidence_count")!=l.get("evidence_count"):issues.append((sid,"distillate evidence_count does not match ledger"))
        if d.get("evidence_count")!=actual_count:issues.append((sid,"distillate evidence_count does not match actual Evidence rows"))

        domains=ev_domains.get(sid,set())
        if len(domains)==1 and d.get("domain") not in domains:issues.append((sid,"distillate domain does not match source Evidence domain"))

        refs=d.get("evidence_anchor_refs")
        if not isinstance(refs,list) or not refs:issues.append((sid,"evidence_anchor_refs must be non-empty array"))
        else:
            if len(refs)!=len(set(refs)):issues.append((sid,"duplicate evidence_anchor_refs"))
            for ref in refs:
                if ev_ids.get(ref)!=sid:issues.append((sid,f"evidence anchor does not belong to source: {ref}"))

        for field in REQUIRED_LIST_FIELDS:
            value=d.get(field)
            if not isinstance(value,list):issues.append((sid,f"{field} must be array"));continue
            if field in NONEMPTY_LIST_FIELDS and not value:issues.append((sid,f"{field} must not be empty"))
            for item in value:
                if not isinstance(item,str) or not item.strip():issues.append((sid,f"{field} items must be non-empty strings"))

        serialized=json.dumps(d,ensure_ascii=False)
        if PATH_RE.search(serialized):issues.append((sid,"distillate leaks local filesystem path"))

    for sid in complete:
        if sid not in source_rows:issues.append((sid,"COMPLETE reading missing mandatory book distillate"))

    return issues


def main():
    k=ROOT/"knowledge"
    project=load_json(k/"PROJECT_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked during K2B distillation")

    lp=k/"K2_READING_LEDGER_WAVE1.jsonl"
    ep=k/"K2_EVIDENCE_WAVE1.jsonl"
    dp=k/"K2_BOOK_DISTILLATES_WAVE1.jsonl"
    if not lp.exists() or not ep.exists():fail("Reading Ledger and Evidence are required before distillation validation")
    ledger=load_jsonl(lp);evidence=load_jsonl(ep)
    complete_count=sum(1 for r in ledger if r.get("read_status")=="COMPLETE")
    if not dp.exists():
        if complete_count:fail(f"{complete_count} COMPLETE reading sources require book distillates")
        print("k2-book-distillates: PASS")
        print("complete_sources=0 distillates=0 issues=0")
        print("claim_extraction_blocked=true")
        return

    distillates=load_jsonl(dp)
    issues=validate_rows(ledger,evidence,distillates)
    if issues:
        first=issues[0]
        fail(f"issues={len(issues)} first={first[0]}: {first[1]}")

    print("k2-book-distillates: PASS")
    print(f"complete_sources={complete_count} distillates={len(distillates)} issues=0")
    print("claim_extraction_blocked=true")


if __name__=="__main__":main()
