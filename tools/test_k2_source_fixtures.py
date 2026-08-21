#!/usr/bin/env python3
import copy,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import validate_k2_source_fixtures as v

SHA="0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf"
SRC={"QM-SRC-0001":{"source_id":"QM-SRC-0001","file_sha256":SHA}}
LIN={"QM-SRC-0001":{"source_id":"QM-SRC-0001","work_id":"WORK-000217"}}
LED={"QM-SRC-0001":{"source_id":"QM-SRC-0001","work_id":"WORK-000217","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_ranges":[{"start":1,"end":57}]}}
CN={1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九"}

def row(pol,n,page):
    star,door=v.LIANG_JIAZI[n]
    return {
        "anchor_count":2,
        "anchors":[
            {"anchor_id":"A1","locator":"MAIN_TABLE/甲子/TOP_STAR_HEADER","value":star},
            {"anchor_id":"A2","locator":"MAIN_TABLE/甲子/BOTTOM_DOOR_FOOTER","value":door},
        ],
        "bureau":n,
        "canonical_sha256":SHA,
        "copyright_class":"DERIVED_FACT_SAFE",
        "fixture_family":"LIANG_18_BUREAU",
        "fixture_id":f"K2F-QM-0001-{pol}-{n:02d}",
        "fixture_status":"ANCHORS_VERIFIED",
        "method_layer":"STANDARD_PLATE",
        "polarity":pol,
        "review_status":"REVIEWED",
        "source_id":"QM-SRC-0001",
        "source_location":f"pdf:p{page}",
        "source_table_state":"TABLE_VISIBLE",
        "table_title":("陽遁" if pol=="YANG" else "陰遁")+CN[n]+"局圖",
        "time_family":"HOUR",
        "verification_basis":"VISUAL_PAGE",
        "work_id":"WORK-000217",
    }

def rows():
    out=[row("YANG",n,v.LIANG_YANG_PAGE[n]) for n in range(1,10)]
    out.extend(row("YIN",n,v.LIANG_YIN_PAGE[n]) for n in range(9,0,-1))
    return out

def expect_ok(rs):
    issues=v.validate_rows(SRC,LIN,LED,rs)
    if issues: raise AssertionError(issues)

def expect_fail(rs,needle,led=None):
    issues=v.validate_rows(SRC,LIN,LED if led is None else led,rs)
    if not any(needle in msg for _,msg in issues): raise AssertionError((needle,issues))

def main():
    base=rows();expect_ok(copy.deepcopy(base))

    r=copy.deepcopy(base);r[0]["source_location"]="pdf:p32";expect_fail(r,"bureau/table-body page mapping mismatch")
    r=copy.deepcopy(base);r[4]["source_location"]="pdf:p35";r[5]["source_location"]="pdf:p36";expect_fail(r,"bureau/table-body page mapping mismatch")
    r=copy.deepcopy(base);r[-1]["source_location"]="pdf:p49";expect_fail(r,"bureau/table-body page mapping mismatch")

    r=copy.deepcopy(base);r[0]["canonical_sha256"]="0"*64;expect_fail(r,"canonical_sha256 mismatch")
    r=copy.deepcopy(base);r[0]["fixture_id"]=r[1]["fixture_id"];expect_fail(r,"duplicate fixture_id")
    r=copy.deepcopy(base);r[0]["anchor_count"]=1;expect_fail(r,"anchor_count must equal len(anchors)")
    r=copy.deepcopy(base);r[0]["table_title"]="陽遁九局圖";expect_fail(r,"table_title mismatch")
    r=copy.deepcopy(base[:-1]);expect_fail(r,"expected 18 rows")
    r=copy.deepcopy(base);r[0]["unexpected"]=1;expect_fail(r,"unexpected fields")

    r=copy.deepcopy(base);r[0]["anchors"][0]["value"]="天芮";expect_fail(r,"bureau-specific Jiazi star anchor mismatch")
    r=copy.deepcopy(base);r[0]["anchors"][1]["value"]="死";expect_fail(r,"bureau-specific Jiazi door anchor mismatch")
    r=copy.deepcopy(base);r[0]["anchors"][0]["value"]="天芮";r[0]["anchors"][1]["value"]="死";expect_fail(r,"bureau-specific Jiazi")

    assert base[-1]["fixture_id"]=="K2F-QM-0001-YIN-01"
    assert base[-1]["source_location"]=="pdf:p48"
    expect_ok(copy.deepcopy(base))

    bad_led=copy.deepcopy(LED);bad_led["QM-SRC-0001"]["read_status"]="PARTIAL";expect_fail(copy.deepcopy(base),"requires COMPLETE reading row",bad_led)
    bad_led=copy.deepcopy(LED);bad_led["QM-SRC-0001"]["verification_mode"]="TEXT_LAYER_FULL";expect_fail(copy.deepcopy(base),"requires VISUAL_PAGE reading",bad_led)
    print("k2-source-fixture-tests: PASS")

if __name__=="__main__": main()
