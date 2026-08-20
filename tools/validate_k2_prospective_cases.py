#!/usr/bin/env python3
import json,re,sys
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"knowledge"/"K2_PROSPECTIVE_CASE_REGISTRY.jsonl"
HEX64=re.compile(r"^[0-9a-f]{64}$")
PATH_RE=re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")

ALLOWED_TOP={
    "case_id","domain","question_fingerprint_sha256","question_domain","method_family",
    "method_layer","setup_method","setup_calibration","seasonal_alignment","time_boundary_system",
    "time_family","layout_method","deity_system","star_state_system","door_state_system",
    "hour_omen_family","ritual_layer","bureau_table_source","role_map_sha256",
    "eligible_features_sha256","competing_branches_sha256","timing_protocol_sha256",
    "auxiliary_information_policy","outcome_unknown_at_freeze","eligible_for_scoring",
    "freeze_timestamp","status","outcome_class","contamination_flags","review_status"
}
METHOD_LAYERS={"STANDARD_PLATE","TIME_FAMILY_VARIANT","HOUR_OMEN","RITUAL_AUXILIARY"}
SETUP={"PINGQI","DINGQI","SOURCE_DEFINED_OTHER","NOT_APPLICABLE"}
ALIGN={"ZHENGSHOU","CHAOSHEN","ZHIRUN","JIEQI","SOURCE_DEFINED_OTHER","NOT_APPLICABLE"}
TIME_FAMILIES={"YEAR","MONTH","DAY","HOUR","NOT_APPLICABLE"}
DEITY={"GOUCHEN_ZHUQUE","BAIHU_XUANWU","SOURCE_DEFINED_OTHER","NOT_APPLICABLE"}
RITUAL={"EXCLUDED_BY_DEFAULT","RESEARCH_ONLY"}
AUX={"NONE","ALLOWED_AFTER_FREEZE","PRE_EXPOSED"}
STATUS={"PREREGISTERED","FROZEN","RESOLVED","VOID"}
OUTCOMES={"HIT","PARTIAL","MISS","UNRESOLVED","CONTAMINATED"}
CONTAM={
    "AUXILIARY_CONTAMINATION","PRIOR_SOCIAL_INFORMATION","EXTERNAL_OMEN",
    "CROSS_METHOD_CONFIRMATION","POST_FEEDBACK_ROLE_SWITCH","POST_FEEDBACK_FACTOR_SWITCH",
    "POST_FEEDBACK_METHOD_SWITCH","POST_FEEDBACK_TIMING_SWITCH",
    "INVALID_INPUT_ACCEPTED_POST_HOC","OTHER"
}
HASH_FIELDS={
    "question_fingerprint_sha256","role_map_sha256","eligible_features_sha256",
    "competing_branches_sha256","timing_protocol_sha256"
}
FREE_TEXT_REQUIRED={
    "question_domain","method_family","setup_method","time_boundary_system","layout_method",
    "star_state_system","door_state_system","hour_omen_family","bureau_table_source"
}


def load_rows(path=REG):
    rows=[]
    if not path.exists():return rows
    for n,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        try:r=json.loads(raw)
        except Exception as e:raise ValueError(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(r,dict):raise ValueError(f"row must be object {path}:{n}")
        rows.append(r)
    return rows


def valid_iso8601_offset(value):
    if not isinstance(value,str) or not value.strip():return False
    try:dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    except Exception:return False
    return dt.tzinfo is not None


def validate_rows(rows):
    issues=[];seen=set()
    for i,r in enumerate(rows,1):
        cid=r.get("case_id") or f"<row:{i}>"
        if cid in seen:issues.append((cid,"duplicate case_id"))
        seen.add(cid)
        extra=set(r)-ALLOWED_TOP;missing=ALLOWED_TOP-set(r)
        if extra:issues.append((cid,f"unexpected fields: {sorted(extra)}"))
        if missing:issues.append((cid,f"missing fields: {sorted(missing)}"))
        blob=json.dumps(r,ensure_ascii=False)
        if PATH_RE.search(blob):issues.append((cid,"local filesystem path leaked"))
        if r.get("domain")!="qimen":issues.append((cid,"domain must be qimen"))
        if not isinstance(r.get("case_id"),str) or not r.get("case_id","").strip():issues.append((cid,"case_id must be non-empty string"))
        for f in HASH_FIELDS:
            if not HEX64.match(r.get(f) or ""):issues.append((cid,f"{f} must be lowercase sha256"))
        for f in FREE_TEXT_REQUIRED:
            if not isinstance(r.get(f),str) or not r.get(f,"").strip():issues.append((cid,f"{f} must be non-empty string"))
        if r.get("method_layer") not in METHOD_LAYERS:issues.append((cid,"invalid method_layer"))
        if r.get("setup_calibration") not in SETUP:issues.append((cid,"invalid setup_calibration"))
        if r.get("seasonal_alignment") not in ALIGN:issues.append((cid,"invalid seasonal_alignment"))
        if r.get("time_family") not in TIME_FAMILIES:issues.append((cid,"invalid time_family"))
        if r.get("deity_system") not in DEITY:issues.append((cid,"invalid deity_system"))
        if r.get("ritual_layer") not in RITUAL:issues.append((cid,"invalid ritual_layer"))
        if r.get("auxiliary_information_policy") not in AUX:issues.append((cid,"invalid auxiliary_information_policy"))
        if r.get("status") not in STATUS:issues.append((cid,"invalid status"))
        if r.get("review_status")!="REVIEWED":issues.append((cid,"review_status must be REVIEWED"))
        if not isinstance(r.get("outcome_unknown_at_freeze"),bool):issues.append((cid,"outcome_unknown_at_freeze must be boolean"))
        if not isinstance(r.get("eligible_for_scoring"),bool):issues.append((cid,"eligible_for_scoring must be boolean"))
        if not valid_iso8601_offset(r.get("freeze_timestamp")):issues.append((cid,"freeze_timestamp must be offset-aware ISO8601"))
        flags=r.get("contamination_flags")
        if not isinstance(flags,list) or len(flags)!=len(set(flags)) or any(x not in CONTAM for x in flags):issues.append((cid,"invalid contamination_flags"))
        st=r.get("status");out=r.get("outcome_class")
        if st=="RESOLVED":
            if out not in OUTCOMES:issues.append((cid,"RESOLVED requires valid outcome_class"))
        elif out is not None:issues.append((cid,"non-RESOLVED row must have outcome_class=null"))
        if st in {"FROZEN","RESOLVED"} and r.get("eligible_for_scoring") and r.get("outcome_unknown_at_freeze") is not True:
            issues.append((cid,"scored FROZEN/RESOLVED row requires outcome_unknown_at_freeze=true"))
        if r.get("method_layer")=="RITUAL_AUXILIARY" and r.get("eligible_for_scoring") is not False:
            issues.append((cid,"RITUAL_AUXILIARY must be ineligible for scoring"))
        if st in {"FROZEN","RESOLVED"} and r.get("eligible_for_scoring"):
            for f in ("setup_method","time_boundary_system","star_state_system","door_state_system"):
                if r.get(f)=="CONTEXT_REQUIRED":issues.append((cid,f"scored frozen model cannot leave {f}=CONTEXT_REQUIRED; resolve it, use NOT_APPLICABLE, or preregister A/B cases"))
        if out=="CONTAMINATED" and not flags:issues.append((cid,"CONTAMINATED outcome requires contamination flag"))
        if flags and st=="RESOLVED" and out=="HIT" and r.get("eligible_for_scoring"):
            issues.append((cid,"contaminated resolved HIT cannot remain eligible_for_scoring"))
    return issues


def main():
    try:rows=load_rows()
    except Exception as e:
        print(f"k2-prospective-cases: FAIL: {e}",file=sys.stderr);raise SystemExit(1)
    issues=validate_rows(rows)
    if issues:
        cid,msg=issues[0];print(f"k2-prospective-cases: FAIL: issues={len(issues)} first={cid}: {msg}",file=sys.stderr);raise SystemExit(1)
    print("k2-prospective-cases: PASS")
    print(f"rows={len(rows)} issues=0")

if __name__=="__main__":main()
