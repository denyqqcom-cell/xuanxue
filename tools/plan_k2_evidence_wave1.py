#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import validate_k2_evidence as v

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",type=Path,default=ROOT)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args();repo=args.repo_root.resolve()
    sources=v.source_index(repo);lineage=v.lineage_index(repo)
    selected=v.wave1_expected(sources,lineage)
    rows=[]
    for sid in sorted(selected):
        s=sources[sid];l=lineage[sid]
        rows.append({
          "source_id":sid,
          "work_id":l.get("work_id"),
          "relation":l.get("relation"),
          "read_priority":l.get("read_priority"),
          "knowledge_domains":s.get("knowledge_domains"),
          "title":s.get("title"),
          "pages":s.get("pages"),
          "readability":s.get("readability"),
          "copyright":s.get("copyright"),
        })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
    print("k2-wave1-plan: PASS")
    print(f"selected_reading_units={len(rows)} output={args.output}")

if __name__=="__main__":main()
