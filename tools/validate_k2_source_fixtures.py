#!/usr/bin/env python3
import json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
ANCHOR_LOC_RE=re.compile(r"^MAIN_TABLE/甲子/(TOP_STAR_HEADER|BOTTOM_DOOR_FOOTER)$")
ALLOWED_FIELDS={
    "anchor_count","anchors","bureau","canonical_sha256","copyright_class",
    "fixture_family","fixture_id","fixture_status","method_layer",
    "polarity","review_status","source_id","source_location","source_table_state",
    "table_title","time_family","verification_basis","work_id"
}
ANCHOR_FIELDS={"anchor_id","locator","value"}
STATUS={"INDEXED","ANCHORS_VERIFIED","IMPLEMENTATION_CHECKED"}
TABLE_STATES={"TABLE_VISIBLE","TITLE_VISIBLE_TABLE_NOT_PRESENT"}
STARS={"天蓬","天芮","天衝","天輔","天禽","天心","天柱","天任","天英"}
DOORS={"休","生","傷","杜","景","死","驚","開"}
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

def validate_anchor(fid,a):
    issues=[]
    if not isinstance(a,dict):
        return [(fid,"anchor must be object")]
    extra=set(a)-ANCHOR_FIELDS
    missing=ANCHOR_FIELDS-set(a)
    if extra: issues.append((fid,f"anchor unexpected fields: {sorted(extra)}"))
    if missing: issues.append((fid,f"anchor missing fields: {sorted(missing)}"))
    aid=a.get("anchor_id")
    loc=a.get("locator")
    val=a.get("value")
    if not isinstance(aid,str) or not aid.strip():
        issues.append((fid,"anchor_id must be non-empty"))
    m=ANCHOR_LOC_RE.match(loc or "")
    if not m:
        issues.append((fid,"anchor locator invalid"))
    if not isinstance(val,str) or not val.strip():
        issues.append((fid,"anchor value must be non-empty"))
    elif m:
        if m.group(1)=="TOP_STAR_HEADER" and val not in STARS:
            issues.append((fid,f"unexpected star anchor value: {val}"))
        if m.group(1)=="BOTTOM_DOOR_FOOTER" and val not in DOORS:
            issues.append((fid,f"unexpected door anchor value: {val}"))
    if PATH_RE.search(json.dumps(a,ensure_ascii=False)):
        issues.append((fid,"local filesystem path leaked through anchor"))
    return issues

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
        if r.get("source_table_state") not in TABLE_STATES: issues.append((fid,"invalid source_table_state"))

        anchors=r.get("anchors")
        if not isinstance(anchors,list):
            issues.append((fid,"anchors must be list"));anchors=[]
        if len(anchors)>4: issues.append((fid,"anchors must contain at most 4 sparse anchors"))
        anchor_ids=set();anchor_locs=set()
        for a in anchors:
            issues.extend(validate_anchor(fid,a))
            if isinstance(a,dict):
                aid=a.get("anchor_id");loc=a.get("locator")
                if aid in anchor_ids: issues.append((fid,"duplicate anchor_id"))
                if loc in anchor_locs: issues.append((fid,"duplicate anchor locator"))
                anchor_ids.add(aid);anchor_locs.add(loc)

        ac=r.get("anchor_count")
        if not isinstance(ac,int) or isinstance(ac,bool) or ac<0 or ac>4:
            issues.append((fid,"anchor_count must be integer 0..4"))
        elif ac!=len(anchors):
            issues.append((fid,"anchor_count must equal len(anchors)"))
        elif r.get("fixture_status")=="INDEXED" and ac!=0:
            issues.append((fid,"INDEXED fixture must have anchor_count=0"))
        elif r.get("fixture_status") in {"ANCHORS_VERIFIED","IMPLEMENTATION_CHECKED"} and ac==0:
            issues.append((fid,"verified/checked fixture requires at least one sparse anchor"))

        if r.get("source_table_state")=="TITLE_VISIBLE_TABLE_NOT_PRESENT":
            if r.get("fixture_status")!="INDEXED" or ac!=0:
                issues.append((fid,"title-only fixture must remain INDEXED with zero anchors"))
        elif r.get("fixture_status") in {"ANCHORS_VERIFIED","IMPLEMENTATION_CHECKED"} and r.get("source_table_state")!="TABLE_VISIBLE":
            issues.append((fid,"verified/checked fixture requires TABLE_VISIBLE"))

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
                if p=="YIN" and n==1:
                    if page!=49 or r.get("source_table_state")!="TITLE_VISIBLE_TABLE_NOT_PRESENT":
                        issues.append((fid,"YIN-01 must preserve p49 title-visible/table-not-present anomaly"))
                elif r.get("source_table_state")!="TABLE_VISIBLE":
                    issues.append((fid,"expected TABLE_VISIBLE for this bureau page"))
    return issues

def main():
    rows=load_fixture_rows(ROOT)
    issues=validate_rows(source_index(),lineage_index(),aggregate_ledger(),rows)
    if issues:
        first=issues[0];fail(f"issues={len(issues)} first={first[0]}: {first[1]}")
    print("k2-source-fixtures: PASS")
    print(f"rows={len(rows)} issues=0")

if __name__=="__main__": main()
