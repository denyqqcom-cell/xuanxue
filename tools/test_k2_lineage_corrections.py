#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_lineage_corrections as v


def main():
    sources={"QM-SRC-0015":{"source_id":"QM-SRC-0015","file_sha256":"a"*64,"pages":53}}
    raw={"QM-SRC-0015":{"source_id":"QM-SRC-0015","relation":"PRIMARY_WORK","work_id":"WORK-1","independence_class":"PRIMARY_CANDIDATE","k2_eligible":True,"part_label":None,"variant_of_source_id":None}}
    readings={"QM-SRC-0015":{"source_id":"QM-SRC-0015","canonical_sha256":"a"*64,"page_start":1,"page_end":53,"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"}}
    c={"correction_id":"K2LC-QM-0015-001","source_id":"QM-SRC-0015","previous_relation":"PRIMARY_WORK","previous_work_id":"WORK-1","corrected_relation":"WORK_PART","corrected_work_id":"WORK-1","part_label":"第三篇","parent_work_title":"超级神算","correction_basis":"VISUAL_PAGE","evidence_locators":["pdf:p1","pdf:p53"],"reason":"visual pages prove work-part carrier","review_status":"REVIEWED"}
    assert not v.inspect(c,sources,raw,readings),v.inspect(c,sources,raw,readings)
    eff=v.effective_lineage_index(raw,[c])["QM-SRC-0015"]
    assert eff["relation"]=="WORK_PART" and eff["independence_class"]=="SAME_WORK_NOT_INDEPENDENT" and eff["part_label"]=="第三篇"

    bad=dict(c,evidence_locators=["pdf:p54"])
    issues=v.inspect(bad,sources,raw,readings)
    assert any("outside canonical pages" in m for _,m in issues),issues

    bad=dict(c,previous_relation="WORK_PART")
    issues=v.inspect(bad,sources,raw,readings)
    assert any("previous_relation" in m for _,m in issues),issues

    bad_read={"QM-SRC-0015":dict(readings["QM-SRC-0015"],verification_mode="TEXT_LAYER_FULL")}
    issues=v.inspect(c,sources,raw,bad_read)
    assert any("COMPLETE VISUAL_PAGE" in m for _,m in issues),issues

    issues=v.validate_rows([c,dict(c,correction_id="K2LC-QM-0015-002")],sources,raw,readings)
    assert any("multiple active corrections" in m for _,m in issues),issues
    print("k2-lineage-correction-tests: PASS")

if __name__=="__main__":main()
