#!/usr/bin/env python3
import json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
LOC_RE=re.compile(r"^pdf:p(\d+)$")
ALLOWED_TOP={"source_id","work_id","canonical_sha256","evidence_locator","verification_basis","verified_fields","review_status"}
ALLOWED_FIELDS={"title","author","author_basis","author_evidence","edition","era","school_ids","school_basis","school_evidence"}
BASES={"TEXT_LAYER","VISUAL_PAGE"}


def fail(msg):
    print(f"k2-verified-source-metadata: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)


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
        for p in sorted(shard.glob("*.jsonl")):rows.extend(load_jsonl(p))
    return {r.get("source_id"):r for r in rows}


def validate_rows(sources,lineage,ledger,rows):
    issues=[];seen=set()
    for r in rows:
        sid=r.get("source_id") or "<missing>"
        if sid in seen:issues.append((sid,"duplicate verified metadata source"))
        seen.add(sid)
        extra=set(r)-ALLOWED_TOP
        if extra:issues.append((sid,f"unexpected fields: {sorted(extra)}"))
        src=sources.get(sid);lin=lineage.get(sid);led=ledger.get(sid)
        if not src:issues.append((sid,"unknown source_id"));continue
        if not lin:issues.append((sid,"missing lineage row"));continue
        if r.get("work_id")!=lin.get("work_id"):issues.append((sid,"work_id mismatch"))
        if r.get("canonical_sha256")!=src.get("file_sha256"):issues.append((sid,"canonical_sha256 mismatch"))
        if r.get("review_status")!="REVIEWED":issues.append((sid,"review_status must be REVIEWED"))
        basis=r.get("verification_basis")
        if basis not in BASES:issues.append((sid,"unsupported verification_basis"))
        fields=r.get("verified_fields")
        if not isinstance(fields,dict) or not fields:issues.append((sid,"verified_fields must be non-empty object"));continue
        unknown=set(fields)-ALLOWED_FIELDS
        if unknown:issues.append((sid,f"unexpected verified_fields: {sorted(unknown)}"))
        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((sid,"local filesystem path leaked"))
        if "author" in fields:
            if not isinstance(fields.get("author"),str) or not fields.get("author").strip():issues.append((sid,"verified author must be non-empty"))
            if fields.get("author_basis") in (None,"","UNKNOWN"):issues.append((sid,"verified author requires non-UNKNOWN author_basis"))
            if not isinstance(fields.get("author_evidence"),str) or not fields.get("author_evidence").strip():issues.append((sid,"verified author requires author_evidence"))
        if "title" in fields and (not isinstance(fields.get("title"),str) or not fields.get("title").strip()):issues.append((sid,"verified title must be non-empty"))
        m=LOC_RE.match(r.get("evidence_locator") or "")
        if not m:issues.append((sid,"evidence_locator must be pdf:pN"));continue
        page=int(m.group(1))
        if not led or led.get("read_status")!="COMPLETE":issues.append((sid,"verified metadata requires COMPLETE reading row"));continue
        covered=set()
        for x in led.get("page_ranges") or []:
            if isinstance(x,dict) and isinstance(x.get("start"),int) and isinstance(x.get("end"),int):covered.update(range(x["start"],x["end"]+1))
        if page not in covered:issues.append((sid,"evidence locator outside reviewed coverage"))
        verification=led.get("verification_mode")
        if basis=="TEXT_LAYER" and verification not in {"TEXT_LAYER_FULL","VISUAL_PAGE"}:issues.append((sid,"TEXT_LAYER metadata requires text/visual reviewed source"))
        if basis=="VISUAL_PAGE" and verification!="VISUAL_PAGE":issues.append((sid,"VISUAL_PAGE metadata requires VISUAL_PAGE reading"))
    return issues


def main():
    rows=load_jsonl(K/"K2_VERIFIED_SOURCE_METADATA.jsonl")
    issues=validate_rows(source_index(),lineage_index(),aggregate_ledger(),rows)
    if issues:
        first=issues[0];fail(f"issues={len(issues)} first={first[0]}: {first[1]}")
    print("k2-verified-source-metadata: PASS")
    print(f"rows={len(rows)} issues=0")

if __name__=="__main__":main()
