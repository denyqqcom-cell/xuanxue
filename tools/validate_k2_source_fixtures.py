#!/usr/bin/env python3
import json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
ALLOWED_FIELDS={
    "anchor_count","bureau","canonical_sha256","copyright_class",
    "fixture_family","fixture_id","fixture_status","method_layer",
    "polarity","review_status","source_id","source_location",
    "table_title","time_family","verification_basis","work_id"
}
STATUS={"INDEXED","ANCHORS_VERIFIED","IMPLEMENTATION_CHECKED"}
CN={1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九"}

def fail(msg):
    print(f"k2-source-fixtures: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

def load_jsonl(path):
    rows=[]
    if not path.exists(): return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip(): continue
        try:r=json.loads(raw)
        except Exception as e: fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict): fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows

def source_index(root=ROOT):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(root/"knowledge"/"domains"/d/"sources.jsonl"):
            out[r["source_id"]]=r
    return out

def lineage_index(root=ROOT):
    return {r["source_id"]:r for r in load_jsonl(root/"knowledge"/"K2_SOURCE_LINEAGE.jsonl")}

def aggregate_ledger(root=ROOT):
    rows=load_jsonl(root/"knowledge"/"K2_READING_LEDGER_WAVE1.jsonl")
    shard=root/"knowledge"/"K2_READING_LEDGER_WAVE1.d"
    if shard.exists():
        for p in sorted(shard.glob("*.jsonl")): rows.extend(load_jsonl(p))
    return {r.get("source_id"):r for r in rows}

def load_fixture_rows(root=ROOT):
    out=[]
    d=root/"knowledge"/"K2_SOURCE_FIXTURES"
    if d.exists():
        for p in sorted(d.glob("*.jsonl")): out.extend(load_jsonl(p))
    return out

def validate_rows(sources,lineage,ledger,rows):
    issues=[];seen=set();liang=[]
    for r in rows:
        fid=r.get("fixture_id") or "<missing>"
        if fid in seen: issues.append((fid,"duplicate fixture_id"))
        seen.add(fid)
        extra=set(r)-ALLOWED_FIELDS
        if extra: issues.append((fid,f"unexpected fields: {sorted(extra)}"))
        missing=ALLOWED_FIELDS-set(r)
        if missing: issues.append((fid,f"missing fields: {sorted(missing)}"))
        sid=r.get("source_id");src=sources.get(sid);lin=lineage.get(sid);led=ledger.get(sid)
        if not src: issues.append((fid,"unknown source_id"));continue
        if not lin: issues.append((fid,"missing lineage row"));continue
        if r.get("work_id")!=lin.get("work_id"): issues.append((fid,"work_id mismatch"))
        if r.get("canonical_sha256")!=src.get("file_sha256"): issues.append((fid,"canonical_sha256 mismatch"))
        if r.get("review_status")!="REVIEWED": issues.append((fid,"review_status must be REVIEWED"))
        if r.get("verification_basis")!="VISUAL_PAGE": issues.append((fid,"verification_basis must be VISUAL_PAGE"))
        if r.get("copyright_class")!="DERIVED_FACT_SAFE": issues.append((fid,"copyright_class must be DERIVED_FACT_SAFE"))
        if r.get("fixture_status") not in STATUS: issues.append((fid,"invalid fixture_status"))
        ac=r.get("anchor_count")
        if not isinstance(ac,int) or isinstance(ac,bool) or ac<0 or ac>4:
            issues.append((fid,"anchor_count must be integer 0..4"))
        elif r.get("fixture_status")=="INDEXED" and ac!=0:
            issues.append((fid,"INDEXED fixture must have anchor_count=0"))
        elif r.get("fixture_status") in {"ANCHORS_VERIFIED","IMPLEMENTATION_CHECKED"} and ac==0:
            issues.append((fid,"verified/checked fixture requires at least one sparse anchor"))
        if r.get("method_layer")!="STANDARD_PLATE": issues.append((fid,"method_layer must be STANDARD_PLATE"))
        if r.get("time_family")!="HOUR": issues.append((fid,"time_family must be HOUR"))
        if r.get("polarity") not in {"YANG","YIN"}: issues.append((fid,"polarity must be YANG or YIN"))
        if not isinstance(r.get("bureau"),int) or isinstance(r.get("bureau"),bool) or not 1<=r.get("bureau",0)<=9:
            issues.append((fid,"bureau must be integer 1..9"))
        if not isinstance(r.get("table_title"),str) or not r.get("table_title").strip():
            issues.append((fid,"table_title must be non-empty"))
        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob): issues.append((fid,"local filesystem path leaked"))
        m=LOC_RE.match(r.get("source_location") or "")
        if not m:
            issues.append((fid,"source_location must be pdf:pN"));continue
        page=int(m.group(1))
        if not led or led.get("read_status")!="COMPLETE":
            issues.append((fid,"fixture requires COMPLETE reading row"));continue
        if led.get("verification_mode")!="VISUAL_PAGE":
            issues.append((fid,"fixture requires VISUAL_PAGE reading"))
        covered=set()
        for x in led.get("page_ranges") or []:
            if isinstance(x,dict) and isinstance(x.get("start"),int) and isinstance(x.get("end"),int):
                covered.update(range(x["start"],x["end"]+1))
        if page not in covered: issues.append((fid,"source_location outside reviewed coverage"))
        if r.get("fixture_family")=="LIANG_18_BUREAU": liang.append((r,page))

    if liang:
        if len(liang)!=18: issues.append(("LIANG_18_BUREAU",f"expected 18 rows, found {len(liang)}"))
        expected={("YANG",n,31+n) for n in range(1,10)}|{("YIN",n,50-n) for n in range(1,10)}
        actual={(r.get("polarity"),r.get("bureau"),page) for r,page in liang}
        if actual!=expected: issues.append(("LIANG_18_BUREAU","bureau/page mapping mismatch"))
        for r,page in liang:
            p=r.get("polarity");n=r.get("bureau");fid=r.get("fixture_id") or "<missing>"
            if p in {"YANG","YIN"} and isinstance(n,int) and 1<=n<=9:
                expected_title=("陽遁" if p=="YANG" else "陰遁")+CN[n]+"局圖"
                if r.get("table_title")!=expected_title:
                    issues.append((fid,f"table_title mismatch; expected {expected_title}"))
    return issues

def main():
    rows=load_fixture_rows(ROOT)
    issues=validate_rows(source_index(),lineage_index(),aggregate_ledger(),rows)
    if issues:
        first=issues[0];fail(f"issues={len(issues)} first={first[0]}: {first[1]}")
    print("k2-source-fixtures: PASS")
    print(f"rows={len(rows)} issues=0")

if __name__=="__main__": main()
