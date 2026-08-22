#!/usr/bin/env python3
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
POLICY="BLOCK_FORMAL_EVIDENCE_UNTIL_VOICE_SCHEMA"
STATUSES={"PARTIAL_READING_CONFIRMED","COMPLETE_READING_CONFIRMED"}
LAYERS={
    "BASE_TEXT","COMMENTARY","TRANSLATION_PARAPHRASE","EDITORIAL_FRONT_MATTER",
    "TITLE_PAGE_ATTRIBUTION","TRADITIONAL_ATTRIBUTION_CLAIM","PUBLISHER_METADATA","UNKNOWN_VOICE"
}


def fail(msg):
    print(f"k2-mixed-voice-holds: FAIL: {msg}",file=sys.stderr)
    raise SystemExit(1)


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
    for p in (root/"knowledge"/"domains").glob("*/sources.jsonl"):
        for r in load_jsonl(p):
            sid=r.get("source_id")
            if sid:out[sid]=r
    return out


def validate_rows(sources,holds,evidence_rows):
    issues=[];seen=set();by_source={}
    for h in holds:
        sid=h.get("source_id") or "<missing>"
        if sid in seen:issues.append((sid,"duplicate hold row"))
        seen.add(sid);by_source[sid]=h
        src=sources.get(sid)
        if not src:issues.append((sid,"unknown source_id"))
        status=h.get("status")
        if status not in STATUSES:issues.append((sid,"invalid hold status"))
        if h.get("hold_policy")!=POLICY:issues.append((sid,"invalid hold_policy"))
        if h.get("verification_mode")!="VISUAL_PAGE":issues.append((sid,"mixed-voice hold requires VISUAL_PAGE verification"))
        a=h.get("reviewed_page_start");b=h.get("reviewed_page_end")
        if not isinstance(a,int) or not isinstance(b,int) or a<1 or b<a:issues.append((sid,"invalid reviewed page range"))
        if status=="COMPLETE_READING_CONFIRMED" and src:
            pages=src.get("pages")
            if not isinstance(pages,int) or a!=1 or b!=pages:
                issues.append((sid,"COMPLETE_READING_CONFIRMED must cover canonical p1-pN"))
        layers=h.get("allowed_voice_layers")
        if not isinstance(layers,list) or set(layers)!=LAYERS:issues.append((sid,"allowed_voice_layers must equal governed layer set"))
        if not isinstance(h.get("reason"),str) or not h.get("reason").strip():issues.append((sid,"reason required"))
        if h.get("review_status")!="REVIEWED":issues.append((sid,"review_status must be REVIEWED"))

    for e in evidence_rows:
        sid=e.get("source_id")
        if sid in by_source:
            eid=e.get("evidence_id") or "<missing evidence_id>"
            issues.append((sid,f"formal evidence {eid} is forbidden while mixed-voice hold is active"))
    return issues


def main():
    hp=K/"K2_MIXED_VOICE_HOLDS.jsonl"
    holds=load_jsonl(hp)
    evidence=[]
    for name in ("K2_EVIDENCE_WAVE1.jsonl","K2_SEGMENT_EVIDENCE.jsonl"):
        evidence.extend(load_jsonl(K/name))
    issues=validate_rows(source_index(ROOT),holds,evidence)
    if issues:
        fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-mixed-voice-holds: PASS")
    print(f"holds={len(holds)} evidence_rows_checked={len(evidence)} issues=0")

if __name__=="__main__":main()
