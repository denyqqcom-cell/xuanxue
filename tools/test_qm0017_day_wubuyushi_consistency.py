#!/usr/bin/env python3
import json
from pathlib import Path

import audit_qm0017_day_wubuyushi_consistency as audit

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"knowledge"/"K2_SOURCE_INTERNAL_CONSISTENCY_FIXTURES"/"QM0017_DAY_WUBUYUSHI_RULE_EXAMPLES_V1.json"

def main():
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["source_id"]=="QM-SRC-0017"
    assert data["scope"]=="SOURCE_INTERNAL_RULE_VS_EXAMPLE_ONLY"
    assert data["interpretation_status"]=="SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE"
    assert data["resolution_status"]=="NO_TENSION_IN_FIXTURE"
    assert data["empirical_credit"]=="NONE"
    assert data["claim_extraction_blocked"] is True
    assert len(data["examples"])==13

    report=audit.audit_fixture(data)
    assert report["cases_checked"]==13
    assert report["matching_cases"]==13
    assert report["mismatch_cases"]==0
    assert report["mismatches"]=={}
    assert report["interpretation_status"]=="SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE"
    assert report["resolution_status"]=="NO_TENSION_IN_FIXTURE"
    assert report["empirical_credit"]=="NONE"
    assert report["claim_extraction_blocked"] is True

    print("qm0017-day-wubuyushi-consistency: PASS")
    print("cases=13 matching=13 mismatches=0 status=SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE empirical_credit=NONE")

if __name__=="__main__":main()
