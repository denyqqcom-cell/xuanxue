#!/usr/bin/env python3
import json
from pathlib import Path

import audit_qm0017_day_tianyi_consistency as audit

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"knowledge"/"K2_SOURCE_INTERNAL_CONSISTENCY_FIXTURES"/"QM0017_DAY_TIANYI_RULE_EXAMPLES_V1.json"

def main():
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["source_id"]=="QM-SRC-0017"
    assert data["scope"]=="SOURCE_INTERNAL_RULE_VS_EXAMPLE_ONLY"
    assert data["interpretation_status"]=="SOURCE_INTERNAL_TENSION"
    assert data["resolution_status"]=="CONTEXT_REQUIRED"
    assert data["empirical_credit"]=="NONE"
    assert data["claim_extraction_blocked"] is True
    assert len(data["examples"])==13

    report=audit.audit_fixture(data)
    assert report["cases_checked"]==13
    assert report["matching_cases"]==8
    assert report["mismatch_cases"]==5
    assert report["mismatches"]==data["expected_mismatches"], f"source tension drifted: {report['mismatches']}"
    assert report["resolution_status"]=="CONTEXT_REQUIRED"
    assert report["empirical_credit"]=="NONE"
    assert report["claim_extraction_blocked"] is True

    print("qm0017-day-tianyi-consistency: PASS")
    print("cases=13 matching=8 mismatches=5 status=SOURCE_INTERNAL_TENSION resolution=CONTEXT_REQUIRED empirical_credit=NONE")

if __name__=="__main__":main()
