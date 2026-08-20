#!/usr/bin/env python3
import copy,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import validate_k2_verified_source_metadata as v

SRC={"QM-SRC-0016":{"source_id":"QM-SRC-0016","file_sha256":"f80169f351740a338d5227225e96939fb3a7045a4e4037b4b3b035bf66630fc7"}}
LIN={"QM-SRC-0016":{"source_id":"QM-SRC-0016","work_id":"WORK-000026"}}
LED={"QM-SRC-0016":{"source_id":"QM-SRC-0016","work_id":"WORK-000026","read_status":"COMPLETE","verification_mode":"TEXT_LAYER_FULL","page_ranges":[{"start":1,"end":415}]}}
ROW={"source_id":"QM-SRC-0016","work_id":"WORK-000026","canonical_sha256":"f80169f351740a338d5227225e96939fb3a7045a4e4037b4b3b035bf66630fc7","evidence_locator":"pdf:p415","verification_basis":"TEXT_LAYER","verified_fields":{"title":"奇门遁甲应用学","author":"王云鹏","author_basis":"MANUAL_VERIFIED","author_evidence":"作者通讯处（PDF p415）署名王云鹏"},"review_status":"REVIEWED"}


def expect_ok(rows):
    issues=v.validate_rows(SRC,LIN,LED,rows)
    if issues:raise AssertionError(issues)


def expect_fail(rows,needle):
    issues=v.validate_rows(SRC,LIN,LED,rows)
    if not any(needle in msg for _,msg in issues):raise AssertionError((needle,issues))


def main():
    expect_ok([copy.deepcopy(ROW)])
    r=copy.deepcopy(ROW);r["canonical_sha256"]="0"*64;expect_fail([r],"canonical_sha256 mismatch")
    r=copy.deepcopy(ROW);r["work_id"]="WORK-X";expect_fail([r],"work_id mismatch")
    r=copy.deepcopy(ROW);r["evidence_locator"]="pdf:p416";expect_fail([r],"outside reviewed coverage")
    r=copy.deepcopy(ROW);r["verified_fields"]["author_basis"]="UNKNOWN";expect_fail([r],"non-UNKNOWN author_basis")
    r=copy.deepcopy(ROW);r["verified_fields"]["author_evidence"]="/home/joe/private.pdf";expect_fail([r],"local filesystem path leaked")
    expect_fail([copy.deepcopy(ROW),copy.deepcopy(ROW)],"duplicate verified metadata source")
    r=copy.deepcopy(ROW);r["unexpected"]=1;expect_fail([r],"unexpected fields")
    print("k2-verified-source-metadata-tests: PASS")

if __name__=="__main__":main()
