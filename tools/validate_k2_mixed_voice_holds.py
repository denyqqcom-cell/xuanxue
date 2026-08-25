#!/usr/bin/env python3
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
POLICIES={"BLOCK_FORMAL_EVIDENCE_UNTIL_VOICE_SCHEMA","VOICE_QUALIFIED_EVIDENCE_ONLY"}
STATUSES={"PARTIAL_READING_CONFIRMED","COMPLETE_READING_CONFIRMED"}
LAYERS={
    "BASE_TEXT","COMMENTARY","TRANSLATION_PARAPHRASE","EDITORIAL_FRONT_MATTER",
    "TITLE_PAGE_ATTRIBUTION","TRADITIONAL_ATTRIBUTION_CLAIM","PUBLISHER_METADATA","UNKNOWN_VOICE"
}
ATTRIBUTION_BASES={
    "EXPLICIT_AUTHORIAL_CONTEXT","EXPLICIT_QUOTATION","TITLE_PAGE","SECTION_HEADING",
    "EDITORIAL_CONTEXT","PUBLISHER_METADATA","TRADITIONAL_ATTRIBUTION","UNKNOWN"
}
SOURCE_STANCES={"SOURCE_REPORTS","SOURCE_ENDORSES","SOURCE_REJECTS","SOURCE_UNCERTAIN"}
METHOD_LAYERS={
    "STRUCTURE_CALCULATION","DIVINATION_INTERPRETATION","TRANSMITTED_REFERENCE",
    "RITUAL_ESOTERIC","MILITARY_OPERATIONAL","HISTORICAL_EDITORIAL","METADATA","UNKNOWN"
}
OPERATIONAL_SCOPES={
    "GENERAL_DIVINATION_CANDIDATE","STRUCTURE_ONLY","REFERENCE_ONLY","NON_OPERATIONAL",
    "EXCLUDED_RITUAL_ESOTERIC","EXCLUDED_MILITARY_OPERATIONAL","UNRESOLVED"
}
INDEPENDENCE_SCOPES={"SOURCE_LOCAL_ONLY","DERIVED_ENUMERATION_COLLAPSED","NO_INDEPENDENT_CREDIT","UNRESOLVED"}
QUALIFICATION_FIELDS={
    "voice_layer","attribution_subject","attribution_basis","source_stance",
    "method_layer","operational_scope","independence_credit_scope"
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


def load_formal_evidence(k=K):
    rows=[]
    for name in ("K2_EVIDENCE_WAVE1.jsonl","K2_SEGMENT_EVIDENCE.jsonl"):
        rows.extend(load_jsonl(k/name))
    shard_dir=k/"K2_EVIDENCE_WAVE1.d"
    if shard_dir.exists():
        for p in sorted(shard_dir.glob("*.jsonl")):
            rows.extend(load_jsonl(p))
    return rows


def validate_voice_qualification(sid,e,issues):
    eid=e.get("evidence_id") or "<missing evidence_id>"
    q=e.get("voice_qualification")
    if not isinstance(q,dict):
        issues.append((sid,f"formal evidence {eid}: voice_qualification required"));return
    if set(q)!=QUALIFICATION_FIELDS:
        issues.append((sid,f"formal evidence {eid}: voice_qualification fields mismatch"));return

    layer=q.get("voice_layer")
    if layer not in LAYERS:issues.append((sid,f"formal evidence {eid}: invalid voice_layer"))
    elif layer=="UNKNOWN_VOICE":issues.append((sid,f"formal evidence {eid}: resolved voice_layer required"))

    subject=q.get("attribution_subject")
    if not isinstance(subject,str) or not subject.strip():
        issues.append((sid,f"formal evidence {eid}: attribution_subject required"))

    basis=q.get("attribution_basis")
    if basis not in ATTRIBUTION_BASES:issues.append((sid,f"formal evidence {eid}: invalid attribution_basis"))
    elif basis=="UNKNOWN":issues.append((sid,f"formal evidence {eid}: resolved attribution_basis required"))

    stance=q.get("source_stance")
    if stance not in SOURCE_STANCES:issues.append((sid,f"formal evidence {eid}: invalid source_stance"))

    method=q.get("method_layer")
    if method not in METHOD_LAYERS:issues.append((sid,f"formal evidence {eid}: invalid method_layer"))
    elif method=="UNKNOWN":issues.append((sid,f"formal evidence {eid}: resolved method_layer required"))

    scope=q.get("operational_scope")
    if scope not in OPERATIONAL_SCOPES:issues.append((sid,f"formal evidence {eid}: invalid operational_scope"))
    elif scope=="UNRESOLVED":issues.append((sid,f"formal evidence {eid}: resolved operational_scope required"))

    credit=q.get("independence_credit_scope")
    if credit not in INDEPENDENCE_SCOPES:issues.append((sid,f"formal evidence {eid}: invalid independence_credit_scope"))
    elif credit=="UNRESOLVED":issues.append((sid,f"formal evidence {eid}: resolved independence_credit_scope required"))

    # Operational eligibility is a relation between method and source stance,
    # not a free label. This prevents non-divination material from silently
    # entering the ordinary divination candidate pool.
    if scope=="GENERAL_DIVINATION_CANDIDATE":
        if stance!="SOURCE_ENDORSES":
            issues.append((sid,f"formal evidence {eid}: GENERAL_DIVINATION_CANDIDATE requires SOURCE_ENDORSES"))
        if method!="DIVINATION_INTERPRETATION":
            issues.append((sid,f"formal evidence {eid}: GENERAL_DIVINATION_CANDIDATE requires DIVINATION_INTERPRETATION"))

    if method=="STRUCTURE_CALCULATION" and scope!="STRUCTURE_ONLY":
        issues.append((sid,f"formal evidence {eid}: STRUCTURE_CALCULATION requires STRUCTURE_ONLY"))
    if method=="TRANSMITTED_REFERENCE" and scope!="REFERENCE_ONLY":
        issues.append((sid,f"formal evidence {eid}: TRANSMITTED_REFERENCE requires REFERENCE_ONLY"))
    if method in {"HISTORICAL_EDITORIAL","METADATA"} and scope!="NON_OPERATIONAL":
        issues.append((sid,f"formal evidence {eid}: HISTORICAL_EDITORIAL/METADATA requires NON_OPERATIONAL"))

    if method=="RITUAL_ESOTERIC":
        if scope!="EXCLUDED_RITUAL_ESOTERIC":
            issues.append((sid,f"formal evidence {eid}: ritual/esoteric evidence cannot enter general divination pool"))
        if e.get("claim_readiness")!="NOT_CLAIM":
            issues.append((sid,f"formal evidence {eid}: ritual/military evidence must be NOT_CLAIM"))
    if method=="MILITARY_OPERATIONAL":
        if scope!="EXCLUDED_MILITARY_OPERATIONAL":
            issues.append((sid,f"formal evidence {eid}: military evidence must stay excluded from general divination pool"))
        if e.get("claim_readiness")!="NOT_CLAIM":
            issues.append((sid,f"formal evidence {eid}: ritual/military evidence must be NOT_CLAIM"))


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
        if h.get("hold_policy") not in POLICIES:issues.append((sid,"invalid hold_policy"))
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
        h=by_source.get(sid)
        if not h:continue
        eid=e.get("evidence_id") or "<missing evidence_id>"
        policy=h.get("hold_policy")
        if policy=="BLOCK_FORMAL_EVIDENCE_UNTIL_VOICE_SCHEMA":
            issues.append((sid,f"formal evidence {eid} is forbidden while mixed-voice hold is active"))
        elif policy=="VOICE_QUALIFIED_EVIDENCE_ONLY":
            validate_voice_qualification(sid,e,issues)
    return issues


def main():
    hp=K/"K2_MIXED_VOICE_HOLDS.jsonl"
    holds=load_jsonl(hp)
    evidence=load_formal_evidence(K)
    issues=validate_rows(source_index(ROOT),holds,evidence)
    if issues:
        fail(f"issues={len(issues)}; "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    print("k2-mixed-voice-holds: PASS")
    print(f"holds={len(holds)} evidence_rows_checked={len(evidence)} issues=0")

if __name__=="__main__":main()
