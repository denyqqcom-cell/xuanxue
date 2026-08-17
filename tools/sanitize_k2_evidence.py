#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LEDGER_FIELDS=["reading_id","source_id","work_id","relation","coverage_mode","page_ranges","pages_reviewed_count","read_status","evidence_count","blocker_reason","review_status"]
EVIDENCE_FIELDS=["evidence_id","domain","source_id","work_id","source_location","evidence_type","scope","topic","normalized_fact","extraction_basis","claim_readiness","school_ids","verbatim_quote","review_status","copyright_class","notes"]

def fail(msg):
    print(f"k2-evidence-sanitize: FAIL: {msg}",file=sys.stderr); raise SystemExit(1)

def load_jsonl(path):
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip(): continue
        try: row=json.loads(raw)
        except Exception as e: fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row,dict): fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows

def contains_path(v):
    if isinstance(v,str): return bool(PATH_RE.search(v))
    if isinstance(v,list): return any(contains_path(x) for x in v)
    if isinstance(v,dict): return any(contains_path(x) for x in v.values())
    return False

def sanitize(rows,fields,kind):
    clean=[]; seen=set()
    id_field="reading_id" if kind=="ledger" else "evidence_id"
    for row in rows:
        rid=row.get(id_field)
        if not isinstance(rid,str) or not rid: fail(f"{kind}: missing {id_field}")
        if rid in seen: fail(f"{kind}: duplicate {id_field}: {rid}")
        seen.add(rid)
        extra=set(row)-set(fields)
        if extra: fail(f"{rid}: non-whitelisted fields: {sorted(extra)}")
        out={k:row.get(k) for k in fields}
        if contains_path(out): fail(f"{rid}: local path leaked")
        if kind=="evidence":
            q=out.get("verbatim_quote")
            if isinstance(q,str) and len(q)>120: fail(f"{rid}: quote too long")
            fact=out.get("normalized_fact")
            if not isinstance(fact,str) or not fact.strip() or len(fact)>800: fail(f"{rid}: normalized_fact invalid")
        clean.append(out)
    return clean

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ledger",type=Path,required=True)
    ap.add_argument("--evidence",type=Path,required=True)
    ap.add_argument("--repo-root",type=Path,default=ROOT)
    args=ap.parse_args(); repo=args.repo_root.resolve()
    led=sanitize(load_jsonl(args.ledger),LEDGER_FIELDS,"ledger")
    ev=sanitize(load_jsonl(args.evidence),EVIDENCE_FIELDS,"evidence")
    k=repo/"knowledge"; k.mkdir(parents=True,exist_ok=True)
    (k/"K2_READING_LEDGER_WAVE1.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in sorted(led,key=lambda x:x["reading_id"])),encoding="utf-8")
    (k/"K2_EVIDENCE_WAVE1.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in sorted(ev,key=lambda x:x["evidence_id"])),encoding="utf-8")
    print("k2-evidence-sanitize: PASS")
    print(f"ledger_rows={len(led)} evidence_rows={len(ev)}")

if __name__=="__main__": main()
