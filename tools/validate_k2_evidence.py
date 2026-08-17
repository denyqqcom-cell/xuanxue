#!/usr/bin/env python3
import argparse,json,re,sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
DOMAINS=["ziwei","bazi","qimen","liuyao","liuren","fengshui"]
UNIQUE_REL={"PRIMARY_WORK","WORK_PART","COMMENTARY_DERIVATIVE"}
EVIDENCE_TYPES={"EXPLICIT_RULE","WORKED_EXAMPLE","TABLE","DIAGRAM","COMMENTARY","HISTORICAL_CLAIM","CASE_RECORD","META_METHOD"}
SCOPES={"STRUCTURE","ALGORITHM","SYMBOLISM","SELECTION","INTERPRETATION","TIMING","CASE","HISTORY","META_METHOD"}
BASES={"TEXT_LAYER","VISUAL_PAGE","TABLE_READ","DIAGRAM_READ","MANUAL_TRANSCRIPTION"}
CLAIM_READY={"READY","CONTEXT_REQUIRED","CONFLICT_CANDIDATE","NOT_CLAIM"}
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
PDF_LOC_RE=re.compile(r"(?:^|\|)pdf:p(\d+)(?:-p?(\d+))?(?:$|\|)")

def fail(msg):
    print(f"k2-evidence: FAIL: {msg}",file=sys.stderr); raise SystemExit(1)

def load_json(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e: fail(f"cannot parse {path}: {e}")

def load_jsonl(path):
    rows=[]
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):fail(f"row must be object {path}:{n}")
        rows.append(r)
    return rows

def source_index(repo):
    out={}
    for d in DOMAINS:
        for r in load_jsonl(repo/"knowledge"/"domains"/d/"sources.jsonl"):
            out[r["source_id"]]=r
    if len(out)!=515: fail(f"canonical source count drift: {len(out)}")
    return out

def lineage_index(repo):
    rows=load_jsonl(repo/"knowledge"/"K2_SOURCE_LINEAGE.jsonl")
    out={r["source_id"]:r for r in rows}
    if len(rows)!=515 or len(out)!=515:fail("lineage must contain 515 unique rows")
    return out

def governed(src):
    kd=src.get("knowledge_domains")
    return isinstance(kd,list) and any(x in DOMAINS for x in kd)

def wave1_expected(sources,lineage):
    p0_work=set(); direct=set()
    for sid,l in lineage.items():
        src=sources[sid]
        if l.get("relation") in UNIQUE_REL and l.get("k2_eligible") is True and governed(src) and l.get("read_priority")=="P0":
            if l.get("relation")=="COMMENTARY_DERIVATIVE": direct.add(sid)
            elif l.get("work_id"): p0_work.add(l["work_id"])
    expected=set(direct)
    for sid,l in lineage.items():
        src=sources[sid]
        if l.get("relation") in {"PRIMARY_WORK","WORK_PART"} and l.get("k2_eligible") is True and governed(src) and l.get("work_id") in p0_work:
            expected.add(sid)
        kd=src.get("knowledge_domains") or []
        if ("liuyao" in kd or "liuren" in kd) and l.get("relation") in UNIQUE_REL and l.get("k2_eligible") is True:
            expected.add(sid)
    return expected

def range_union(ranges,pages,issues,sid):
    covered=set()
    if not isinstance(ranges,list):issues.append((sid,"page_ranges must be array"));return covered
    for x in ranges:
        if not isinstance(x,dict) or not isinstance(x.get("start"),int) or not isinstance(x.get("end"),int):
            issues.append((sid,"invalid page range"));continue
        a,b=x["start"],x["end"]
        if a<1 or b<a:issues.append((sid,"invalid page range bounds"));continue
        if isinstance(pages,int) and b>pages:issues.append((sid,"page range exceeds source pages"))
        covered.update(range(a,b+1))
    return covered

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo-root",type=Path,default=ROOT);ap.add_argument("--force",action="store_true");args=ap.parse_args()
    repo=args.repo_root.resolve();k=repo/"knowledge"
    project=load_json(k/"PROJECT_STATE.json");state=load_json(k/"K2_EVIDENCE_STATE.json")
    if project.get("phase")!="K2_EVIDENCE_EXTRACTION":fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("source_lineage")!="COMPLETE" or project.get("evidence_extraction_blocked") is not False:fail("K2B requires completed lineage and open evidence lane")
    if project.get("claim_extraction_blocked") is not True or state.get("claim_extraction_blocked") is not True:fail("Claim Extraction must remain blocked during K2B")
    sources=source_index(repo);lineage=lineage_index(repo);expected=wave1_expected(sources,lineage)
    lp=k/"K2_READING_LEDGER_WAVE1.jsonl";ep=k/"K2_EVIDENCE_WAVE1.jsonl"
    if not lp.exists() or not ep.exists():
        if state.get("status")=="WAVE1_OPEN" and not args.force:
            print("k2-evidence: WAVE1_OPEN")
            print(f"expected_reading_units={len(expected)} evidence_rows=0 claim_extraction_blocked=true")
            return
        fail("Wave1 ledger/evidence files missing")
    ledger=load_jsonl(lp);evidence=load_jsonl(ep);issues=[]
    lseen={};
    for r in ledger:
        sid=r.get("source_id")
        if sid in lseen:issues.append((sid or "<missing>","duplicate ledger source_id"));continue
        lseen[sid]=r
        if sid not in expected:issues.append((sid or "<missing>","source not selected for Wave1"));continue
        lin=lineage[sid];src=sources[sid]
        if r.get("work_id")!=lin.get("work_id"):issues.append((sid,"ledger work_id mismatch"))
        if r.get("relation")!=lin.get("relation"):issues.append((sid,"ledger relation mismatch"))
        status=r.get("read_status");mode=r.get("coverage_mode");pages=src.get("pages")
        covered=range_union(r.get("page_ranges"),pages,issues,sid)
        if status=="COMPLETE":
            if isinstance(pages,int):
                if mode not in {"PDF_PAGES","DOCUMENT_PAGES"}:issues.append((sid,"paged COMPLETE source requires page coverage mode"))
                if len(covered)!=pages or (covered and (min(covered)!=1 or max(covered)!=pages)):issues.append((sid,f"COMPLETE coverage does not span all {pages} pages"))
                if r.get("pages_reviewed_count")!=pages:issues.append((sid,"pages_reviewed_count mismatch"))
            else:
                if mode!="WHOLE_TEXT_DOCUMENT":issues.append((sid,"unpaged COMPLETE source requires WHOLE_TEXT_DOCUMENT"))
        elif status=="BLOCKED":
            if not isinstance(r.get("blocker_reason"),str) or not r.get("blocker_reason").strip():issues.append((sid,"BLOCKED requires blocker_reason"))
        else:
            issues.append((sid,"Wave1 submission must be COMPLETE or BLOCKED"))
        if r.get("review_status")!="REVIEWED":issues.append((sid,"ledger row must be REVIEWED"))
    missing=expected-set(lseen);extra=set(lseen)-expected
    if missing:issues.append(("<global>",f"missing {len(missing)} Wave1 reading units"))
    if extra:issues.append(("<global>",f"extra {len(extra)} Wave1 reading units"))
    ev_seen=set();ev_count=Counter()
    for e in evidence:
        eid=e.get("evidence_id");sid=e.get("source_id")
        if not isinstance(eid,str) or not eid:issues.append((sid or "<missing>","missing evidence_id"));continue
        if eid in ev_seen:issues.append((eid,"duplicate evidence_id"));continue
        ev_seen.add(eid)
        if sid not in expected:issues.append((eid,"evidence source not selected for Wave1"));continue
        lin=lineage[sid];src=sources[sid];ev_count[sid]+=1
        if e.get("work_id")!=lin.get("work_id"):issues.append((eid,"evidence work_id mismatch"))
        kd=src.get("knowledge_domains") or []
        if e.get("domain") not in kd and e.get("domain")!="common":issues.append((eid,"evidence domain not supported by K1 semantic routing"))
        if e.get("evidence_type") not in EVIDENCE_TYPES:issues.append((eid,"invalid evidence_type"))
        if e.get("scope") not in SCOPES:issues.append((eid,"invalid scope"))
        if e.get("extraction_basis") not in BASES:issues.append((eid,"invalid extraction_basis"))
        if e.get("claim_readiness") not in CLAIM_READY:issues.append((eid,"invalid claim_readiness"))
        fact=e.get("normalized_fact")
        if not isinstance(fact,str) or not fact.strip() or len(fact)>800:issues.append((eid,"normalized_fact invalid"))
        loc=e.get("source_location")
        if not isinstance(loc,str) or not loc.strip() or len(loc)>120 or PATH_RE.search(loc):issues.append((eid,"source_location invalid or leaks local path"))
        quote=e.get("verbatim_quote")
        if src.get("copyright")!="PUBLIC_DOMAIN_TEXT_ONLY" and quote not in (None,""):issues.append((eid,"non-public-domain source must not export verbatim_quote"))
        if isinstance(quote,str) and len(quote)>120:issues.append((eid,"quote too long"))
        if e.get("review_status") not in {"REVIEWED","CONFLICTED"}:issues.append((eid,"evidence must be REVIEWED or CONFLICTED"))
        if quote in (None,"") and e.get("copyright_class")!="DERIVED_FACT_SAFE":issues.append((eid,"paraphrased public evidence must use DERIVED_FACT_SAFE"))
        m=PDF_LOC_RE.search(loc or "")
        if m and sid in lseen and lseen[sid].get("read_status")=="COMPLETE":
            a=int(m.group(1));b=int(m.group(2) or a);cov=range_union(lseen[sid].get("page_ranges"),sources[sid].get("pages"),[],sid)
            if any(p not in cov for p in range(a,b+1)):issues.append((eid,"evidence locator outside reviewed coverage"))
    for sid,r in lseen.items():
        if r.get("evidence_count")!=ev_count[sid]:issues.append((sid,"ledger evidence_count does not match evidence rows"))
    blocked=sum(1 for r in ledger if r.get("read_status")=="BLOCKED")
    if issues:
        sample="; ".join(f"{sid}: {msg}" for sid,msg in issues[:25])
        if not args.force:
            print("k2-evidence: REVIEW_REQUIRED")
            print(f"expected_reading_units={len(expected)} ledger_rows={len(ledger)} evidence_rows={len(evidence)} blocked={blocked} issues={len(issues)}")
            print(sample);return
        fail(f"{len(issues)} issue(s); {sample}")
    print("k2-evidence: REVIEW_REQUIRED")
    print(f"expected_reading_units={len(expected)} ledger_rows={len(ledger)} evidence_rows={len(evidence)} blocked={blocked} issues=0")
    print("claim_extraction_blocked=true; project review required")

if __name__=="__main__":main()
