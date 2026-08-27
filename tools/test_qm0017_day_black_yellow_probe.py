#!/usr/bin/env python3
import json
from pathlib import Path

from reconstruct_qm0017_day_black_yellow import reconstruct_black_yellow

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"knowledge"/"K2_ENUMERATION_RECONSTRUCTION_FIXTURES"/"QM0017_DAY_BLACK_YELLOW_V1.json"
BRANCHES=list("子丑寅卯辰巳午未申酉戌亥")

def main():
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"]=="k2-enumeration-component-fixture-v1"
    assert data["source_id"]=="QM-SRC-0017"
    assert data["generative_rule_id"]=="QM0017-DAY-QIMEN-120-ENUM"
    assert data["component_id"]=="TWELVE_BLACK_YELLOW_ROAD"
    assert data["scope"]=="COMPONENT_ONLY_NOT_FULL_GENERATOR"
    assert data["review_status"]=="REVIEWED"
    assert data["source_rule_checkpoint"]=="pdf:p281"
    assert len(data["cases"])==4

    checked=0
    for case in data["cases"]:
        expected=case["expected"]
        assert list(expected)==BRANCHES, f"fixture branch order drifted: {case['case_id']}"
        actual=reconstruct_black_yellow(case["day_branch"])
        assert actual==expected, f"source fixture mismatch: {case['case_id']} expected={expected} actual={actual}"
        checked+=len(expected)

    assert checked==48, f"expected 48 source-backed hour states, got {checked}"
    assert any("UNTESTED" in x for x in data["limitations"]),"probe must preserve full-generator UNTESTED boundary"
    assert any("empirical credit" in x for x in data["limitations"]),"probe must preserve empirical-credit boundary"
    print("qm0017-day-black-yellow-probe: PASS")
    print(f"cases={len(data['cases'])} checked_hour_states={checked} matched_hour_states={checked} formal_generator_status=UNTESTED")

if __name__=="__main__":main()
