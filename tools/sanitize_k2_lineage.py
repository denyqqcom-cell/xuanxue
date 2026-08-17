#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
FIELDS=[
    "source_id","work_id","relation","part_label","variant_of_source_id",
    "parent_work_ids","independence_class","lineage_basis","lineage_evidence",
    "k2_eligible","read_priority","review_status"
]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")

def fail(msg):
    print(f"k2-lineage-sanitize: FAIL: {msg}",file=sys.stderr); raise SystemExit(1)

def load_jsonl(path):
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip(): continue
        try: row=json.loads(raw)
        except Exception as e: fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row,dict): fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows

def canonical_ids(repo):
    ids=[]
    for d in DOMAINS:
        for row in load_jsonl(repo/"knowledge"/"domains"/d/"sources.jsonl"):
            ids.append(row["source_id"])
    if len(ids)!=515 or len(set(ids))!=515: fail("canonical source registry must contain 515 unique IDs")
    return set(ids)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input",type=Path)
    ap.add_argument("--repo-root",type=Path,default=ROOT)
    ap.add_argument("--output",type=Path,default=None)
    args=ap.parse_args()
    repo=args.repo_root.resolve(); target=args.output or repo/"knowledge"/"K2_SOURCE_LINEAGE.jsonl"
    rows=load_jsonl(args.input)
    expected=canonical_ids(repo)
    seen=set(); clean=[]
    for row in rows:
        sid=row.get("source_id")
        if sid not in expected: fail(f"unknown source_id: {sid}")
        if sid in seen: fail(f"duplicate source_id: {sid}")
        seen.add(sid)
        extra=set(row)-set(FIELDS)
        if extra: fail(f"{sid}: non-whitelisted fields present: {sorted(extra)}")
        out={k:row.get(k) for k in FIELDS}
        for k,v in out.items():
            if isinstance(v,str) and PATH_RE.search(v): fail(f"{sid}: local path leaked through {k}")
            if isinstance(v,list):
                for x in v:
                    if isinstance(x,str) and PATH_RE.search(x): fail(f"{sid}: local path leaked through {k}")
        clean.append(out)
    if seen != expected:
        fail(f"lineage draft must cover exactly all 515 canonical sources; missing={len(expected-seen)} extra={len(seen-expected)}")
    clean.sort(key=lambda x:x["source_id"])
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in clean),encoding="utf-8")
    print("k2-lineage-sanitize: PASS")
    print(f"sources={len(clean)} output={target}")

if __name__=="__main__": main()
