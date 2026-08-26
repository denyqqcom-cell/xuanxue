#!/usr/bin/env python3
from generate_k2_claim_extraction_readiness import build_readiness
from validate_k2_claim_extraction_readiness import shape_issues


def base_project():
    return {
        "phase": "K2_EVIDENCE_EXTRACTION",
        "next_phase": "K2_CLAIM_EXTRACTION",
        "required_domains": ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"],
        "k2_blocked": False,
        "evidence_extraction_blocked": False,
        "claim_extraction_blocked": True,
    }


def base_evidence():
    return {
        "status": "WAVE1_OPEN",
        "claim_extraction_blocked": True,
        "unknown_textual_resolution_backlog": 93,
        "required_domains": ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"],
    }


def base_qcic():
    return {
        "stance_topics": [{"claim_eligible": False},{"claim_eligible": True}],
        "enumeration_units": [{"claim_eligible": False}],
    }


def base_unknown():
    return {
        "raw_unknown_textual_source_count": 96,
        "resolved_by_k2_discovery_count": 3,
        "remaining_unknown_textual_source_count": 93,
    }


def expect_raises(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("expected ValueError")


def main():
    project=base_project();evidence=base_evidence();qcic=base_qcic();unknown=base_unknown()
    closed=build_readiness(project,evidence,qcic,True,unknown,True)
    assert closed["status"]=="CLOSED"
    assert closed["claim_extraction_authorized"] is False
    assert closed["empirical_credit_path_separate"] is True
    assert closed["blockers"]==[
        "K2_EVIDENCE_STATE_NOT_COMPLETE",
        "UNKNOWN_TEXTUAL_BACKLOG_REMAINS",
        "EVIDENCE_STATE_BLOCKS_CLAIM_EXTRACTION",
    ]
    assert closed["observed_state"]["qcic_claim_eligible_unit_count"]==1
    assert closed["observed_state"]["raw_unknown_textual_source_count"]==96
    assert closed["observed_state"]["resolved_by_k2_discovery_count"]==3
    assert shape_issues(closed)==[]

    ready_evidence=base_evidence();ready_evidence.update({"status":"COMPLETE","claim_extraction_blocked":False,"unknown_textual_resolution_backlog":0})
    ready_unknown={"raw_unknown_textual_source_count":96,"resolved_by_k2_discovery_count":96,"remaining_unknown_textual_source_count":0}
    ready=build_readiness(project,ready_evidence,qcic,True,ready_unknown,True)
    assert ready["status"]=="READY_FOR_PROJECT_REVIEW"
    assert ready["blockers"]==[]
    assert ready["claim_extraction_authorized"] is False
    assert shape_issues(ready)==[]

    stale=build_readiness(project,ready_evidence,qcic,True,ready_unknown,False)
    assert stale["status"]=="CLOSED"
    assert stale["blockers"]==["UNKNOWN_TEXTUAL_BACKLOG_MATERIALIZATION_STALE"]

    accounting=base_evidence();accounting["unknown_textual_resolution_backlog"]=92
    drift=build_readiness(project,accounting,qcic,True,unknown,True)
    assert "UNKNOWN_TEXTUAL_BACKLOG_ACCOUNTING_DRIFT" in drift["blockers"]

    mismatch_project=base_project();mismatch_project["required_domains"]=["qimen"]
    mismatch=build_readiness(mismatch_project,evidence,qcic,True,unknown,True)
    assert "PROJECT_EVIDENCE_DOMAIN_SET_MISMATCH" in mismatch["blockers"]

    invalid=dict(ready);invalid["claim_extraction_authorized"]=True
    assert any("never authorize" in issue for issue in shape_issues(invalid))

    expect_raises(lambda: build_readiness(project,evidence,qcic,True,{**unknown,"remaining_unknown_textual_source_count":-1},True))
    expect_raises(lambda: build_readiness(project,evidence,qcic,True,{**unknown,"remaining_unknown_textual_source_count":True},True))

    print("k2-claim-extraction-readiness-tests: PASS")


if __name__=="__main__":main()
