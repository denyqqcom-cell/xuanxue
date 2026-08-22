#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_deep_source_distillates as v


def base_indexes(part=False):
    sources={"QM-SRC-0001":{"source_id":"QM-SRC-0001","domain":"qimen","file_sha256":"a"*64,"pages":10}}
    lin={"source_id":"QM-SRC-0001","work_id":"WORK-1","relation":"WORK_PART" if part else "PRIMARY_WORK","independence_class":"SAME_WORK_NOT_INDEPENDENT" if part else "PRIMARY_CANDIDATE"}
    lineage={"QM-SRC-0001":lin}
    readings={"K2DEEP-QM-SRC-0001":{"reading_id":"K2DEEP-QM-SRC-0001","source_id":"QM-SRC-0001","canonical_sha256":"a"*64,"page_start":1,"page_end":10,"pages_reviewed_count":10,"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"}}
    return sources,lineage,readings,{},set(),{},{}


def row(part=False,**o):
    r={
      "distillate_id":"K2DS-QM-SRC-0001","source_id":"QM-SRC-0001","work_id":"WORK-1","domain":"qimen",
      "distillation_scope":"DEEP_SOURCE_PART" if part else "DEEP_SOURCE_BOOK","reading_ref":"K2DEEP-QM-SRC-0001","canonical_sha256":"a"*64,
      "source_anchors":["QM-SRC-0001@pdf:p1"],"course_family_id":None,"course_role":None,
      "independence_policy":"WORK_FAMILY_SINGLE_VOTE" if part else "DEFAULT","prior_distillate_refs":[],"evidence_reaudit_coverage":"NOT_APPLICABLE",
      "source_credit":"FULL_SOURCE_VISUAL_REVIEWED","empirical_credit":"NONE","essence":["x"],"method_map":["x"],"applicability_constraints":[],
      "source_limitations":["x"],"conflicts_and_tensions":[],"anti_patterns":[],"model_updates":["x"],
      "testable_hypotheses":[{"hypothesis_id":"H1","statement":"x","freeze_requirements":"x","failure_condition":"x","status":"UNTESTED"}],
      "excluded_from_operational_use":[],"claim_extraction_blocked":True,"acceptance_status":"K2B_SOURCE_REVIEW_ACCEPTED","distillation_status":"REVIEWED","review_status":"REVIEWED","copyright_class":"DERIVED_SYNTHESIS_SAFE"
    }
    r.update(o);return r


def main():
    idx=base_indexes(False);assert not v.inspect(row(False),idx),v.inspect(row(False),idx)
    idxp=base_indexes(True);assert not v.inspect(row(True),idxp),v.inspect(row(True),idxp)

    issues=v.inspect(row(True,distillation_scope="DEEP_SOURCE_BOOK"),idxp)
    assert any("DEEP_SOURCE_PART" in m for _,m in issues),issues
    issues=v.inspect(row(True,independence_policy="DEFAULT"),idxp)
    assert any("WORK_FAMILY_SINGLE_VOTE" in m for _,m in issues),issues
    issues=v.inspect(row(False,source_anchors=["QM-SRC-0001@pdf:p11"]),idx)
    assert any("outside canonical pages" in m for _,m in issues),issues
    issues=v.inspect(row(False,empirical_credit="FULL"),idx)
    assert any("empirical credit" in m for _,m in issues),issues

    bad=list(idx);bad[4]={"QM-SRC-0001"};issues=v.inspect(row(False),tuple(bad))
    assert any("work-family" in m for _,m in issues),issues

    state={"status":"COMPLETE","targets":[{"source_id":"QM-SRC-0001","required":True}]}
    assert not v.validate_rows([row(False)],state,idx),v.validate_rows([row(False)],state,idx)
    issues=v.validate_rows([],state,idx)
    assert any("required deep-source distillate missing" in m for _,m in issues),issues
    print("k2-deep-source-distillate-tests: PASS")

if __name__=="__main__":main()
