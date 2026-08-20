#!/usr/bin/env python3
import copy,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import validate_k2_prospective_cases as v

H="0"*64
BASE={
    "case_id":"K2PC-QM-000001",
    "domain":"qimen",
    "question_fingerprint_sha256":H,
    "question_domain":"TEST_DOMAIN",
    "method_family":"TEST_FAMILY",
    "method_layer":"STANDARD_PLATE",
    "setup_method":"CHAIBU_SOLAR_TERM",
    "setup_calibration":"PINGQI",
    "seasonal_alignment":"JIEQI",
    "time_boundary_system":"ZI_START_23",
    "time_family":"HOUR",
    "layout_method":"ROTATING_PLATE",
    "deity_system":"GOUCHEN_ZHUQUE",
    "star_state_system":"NOT_APPLICABLE",
    "door_state_system":"NOT_APPLICABLE",
    "hour_omen_family":"NONE",
    "ritual_layer":"EXCLUDED_BY_DEFAULT",
    "bureau_table_source":"LIANG_18_BUREAU",
    "role_map_sha256":H,
    "eligible_features_sha256":H,
    "competing_branches_sha256":H,
    "timing_protocol_sha256":H,
    "auxiliary_information_policy":"NONE",
    "outcome_unknown_at_freeze":True,
    "eligible_for_scoring":True,
    "freeze_timestamp":"2026-08-21T03:10:00+08:00",
    "status":"FROZEN",
    "outcome_class":None,
    "contamination_flags":[],
    "review_status":"REVIEWED"
}


def expect_ok(rows):
    issues=v.validate_rows(rows)
    if issues:raise AssertionError(issues)


def expect_fail(rows,needle):
    issues=v.validate_rows(rows)
    if not any(needle in msg for _,msg in issues):raise AssertionError((needle,issues))


def main():
    expect_ok([copy.deepcopy(BASE)])
    r=copy.deepcopy(BASE);r["question_fingerprint_sha256"]="ABC";expect_fail([r],"question_fingerprint_sha256")
    r=copy.deepcopy(BASE);r["freeze_timestamp"]="2026-08-21T03:10:00";expect_fail([r],"offset-aware")
    r=copy.deepcopy(BASE);r["status"]="RESOLVED";r["outcome_class"]="MISS";expect_ok([r])
    r=copy.deepcopy(BASE);r["status"]="RESOLVED";r["outcome_class"]=None;expect_fail([r],"RESOLVED requires")
    r=copy.deepcopy(BASE);r["outcome_unknown_at_freeze"]=False;expect_fail([r],"requires outcome_unknown_at_freeze=true")
    r=copy.deepcopy(BASE);r["method_layer"]="RITUAL_AUXILIARY";r["eligible_for_scoring"]=True;expect_fail([r],"RITUAL_AUXILIARY")
    r=copy.deepcopy(BASE);r["status"]="RESOLVED";r["outcome_class"]="CONTAMINATED";expect_fail([r],"requires contamination flag")
    r=copy.deepcopy(BASE);r["status"]="RESOLVED";r["outcome_class"]="HIT";r["contamination_flags"]=["AUXILIARY_CONTAMINATION"];expect_fail([r],"cannot remain eligible_for_scoring")
    r=copy.deepcopy(BASE);r["layout_method"]="/home/user/private";expect_fail([r],"local filesystem path leaked")
    for f in ("setup_method","time_boundary_system","star_state_system","door_state_system"):
        r=copy.deepcopy(BASE);del r[f];expect_fail([r],"missing fields")
        r=copy.deepcopy(BASE);r[f]="";expect_fail([r],f"{f} must be non-empty")
        r=copy.deepcopy(BASE);r[f]="CONTEXT_REQUIRED";expect_fail([r],f"cannot leave {f}=CONTEXT_REQUIRED")
    expect_fail([copy.deepcopy(BASE),copy.deepcopy(BASE)],"duplicate case_id")
    r=copy.deepcopy(BASE);r["unexpected"]=1;expect_fail([r],"unexpected fields")
    print("k2-prospective-case-tests: PASS")

if __name__=="__main__":main()
