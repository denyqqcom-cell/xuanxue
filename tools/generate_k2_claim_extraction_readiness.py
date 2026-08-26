#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path

from generate_k2_qcic_eligibility_view import ROOT,actual_view,render_view
from generate_k2_unknown_textual_backlog import build_state as build_unknown_state,render as render_unknown_state

K=ROOT/"knowledge"
OUT=K/"K2_CLAIM_EXTRACTION_READINESS.json"
SCHEMA_VERSION="k2-claim-extraction-readiness-v1"
GENERATED_FROM=[
    "knowledge/PROJECT_STATE.json",
    "knowledge/K2_EVIDENCE_STATE.json",
    "knowledge/K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json",
    "knowledge/K2_UNKNOWN_TEXTUAL_BACKLOG.json",
]
BLOCKER_CODES={
    "evidence_state_complete":"K2_EVIDENCE_STATE_NOT_COMPLETE",
    "unknown_textual_backlog_cleared":"UNKNOWN_TEXTUAL_BACKLOG_REMAINS",
    "unknown_textual_backlog_materialization_current":"UNKNOWN_TEXTUAL_BACKLOG_MATERIALIZATION_STALE",
    "unknown_textual_backlog_accounting_current":"UNKNOWN_TEXTUAL_BACKLOG_ACCOUNTING_DRIFT",
    "evidence_state_unblocks_claim_extraction":"EVIDENCE_STATE_BLOCKS_CLAIM_EXTRACTION",
    "project_k2_not_blocked":"PROJECT_K2_BLOCKED",
    "project_evidence_extraction_open":"PROJECT_EVIDENCE_EXTRACTION_BLOCKED",
    "required_domains_consistent":"PROJECT_EVIDENCE_DOMAIN_SET_MISMATCH",
    "qcic_materialization_current":"QCIC_ELIGIBILITY_MATERIALIZATION_STALE",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def qcic_current(root=ROOT):
    path=root/"knowledge"/"K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json"
    if not path.exists():return False,None
    try:stored=path.read_text(encoding="utf-8");view=json.loads(stored)
    except Exception:return False,None
    try:expected=render_view(actual_view(root))
    except Exception:return False,view
    return stored==expected,view


def unknown_backlog_current(root=ROOT):
    path=root/"knowledge"/"K2_UNKNOWN_TEXTUAL_BACKLOG.json"
    if not path.exists():return False,None
    try:stored=path.read_text(encoding="utf-8");view=json.loads(stored)
    except Exception:return False,None
    try:expected=render_unknown_state(build_unknown_state(root))
    except Exception:return False,view
    return stored==expected,view


def build_readiness(project,evidence,qcic_view,qcic_is_current,unknown_state,unknown_is_current):
    project_domains=project.get("required_domains") or []
    evidence_domains=evidence.get("required_domains") or []
    remaining=unknown_state.get("remaining_unknown_textual_source_count")
    raw_unknown=unknown_state.get("raw_unknown_textual_source_count")
    resolved=unknown_state.get("resolved_by_k2_discovery_count")
    for name,value in (("remaining",remaining),("raw_unknown",raw_unknown),("resolved",resolved)):
        if not isinstance(value,int) or isinstance(value,bool) or value<0:
            raise ValueError(f"{name} unknown-textual count must be a non-negative integer")
    stance_topics=qcic_view.get("stance_topics") or []
    enum_units=qcic_view.get("enumeration_units") or []
    claim_eligible=sum(1 for r in stance_topics+enum_units if isinstance(r,dict) and r.get("claim_eligible") is True)
    checks={
        "evidence_state_complete":evidence.get("status")=="COMPLETE",
        "unknown_textual_backlog_cleared":remaining==0,
        "unknown_textual_backlog_materialization_current":unknown_is_current is True,
        "unknown_textual_backlog_accounting_current":evidence.get("unknown_textual_resolution_backlog")==remaining,
        "evidence_state_unblocks_claim_extraction":evidence.get("claim_extraction_blocked") is False,
        "project_k2_not_blocked":project.get("k2_blocked") is False,
        "project_evidence_extraction_open":project.get("evidence_extraction_blocked") is False,
        "required_domains_consistent":bool(project_domains) and set(project_domains)==set(evidence_domains) and len(project_domains)==len(set(project_domains)) and len(evidence_domains)==len(set(evidence_domains)),
        "qcic_materialization_current":qcic_is_current is True,
    }
    blockers=[BLOCKER_CODES[k] for k,v in checks.items() if not v]
    ready=not blockers
    return {
        "blockers":blockers,
        "checks":checks,
        "claim_extraction_authorized":False,
        "empirical_credit_path_separate":True,
        "generated_from":list(GENERATED_FROM),
        "observed_state":{
            "evidence_state_unknown_textual_resolution_backlog":evidence.get("unknown_textual_resolution_backlog"),
            "evidence_status":evidence.get("status") or "UNKNOWN",
            "project_next_phase":project.get("next_phase") or "UNKNOWN",
            "project_phase":project.get("phase") or "UNKNOWN",
            "qcic_claim_eligible_unit_count":claim_eligible,
            "qcic_enumeration_unit_count":len(enum_units),
            "qcic_stance_topic_count":len(stance_topics),
            "raw_unknown_textual_source_count":raw_unknown,
            "resolved_by_k2_discovery_count":resolved,
            "unknown_textual_resolution_backlog":remaining,
        },
        "schema_version":SCHEMA_VERSION,
        "status":"READY_FOR_PROJECT_REVIEW" if ready else "CLOSED",
        "transition_policy":"PROJECT_REVIEW_REQUIRED_V1_NEVER_AUTO_OPENS",
    }


def actual_readiness(root=ROOT):
    project=load_json(root/"knowledge"/"PROJECT_STATE.json")
    evidence=load_json(root/"knowledge"/"K2_EVIDENCE_STATE.json")
    qcurrent,qview=qcic_current(root)
    ucurrent,uview=unknown_backlog_current(root)
    if qview is None:raise ValueError("missing/invalid QCIC eligibility view")
    if uview is None:raise ValueError("missing/invalid unknown textual backlog view")
    return build_readiness(project,evidence,qview,qcurrent,uview,ucurrent)


def render(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n"


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write",action="store_true");g.add_argument("--stdout",action="store_true")
    args=p.parse_args();text=render(actual_readiness(ROOT))
    if args.write:
        OUT.write_text(text,encoding="utf-8");print(f"wrote {OUT.relative_to(ROOT)}")
    else:sys.stdout.write(text)


if __name__=="__main__":main()
