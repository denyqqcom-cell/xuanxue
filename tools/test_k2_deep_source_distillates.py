#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_deep_source_distillates as v


def indexes():
    sources={"QM-SRC-0001":{"source_id":"QM-SRC-0001","domain":"qimen","file_sha256":"a"*64,"pages":10}}
    lineage={"QM-SRC-0001":{"source_id":"QM-SRC-0001","work_id":"WORK-1"}}
    readings={"K2DEEP-QM-SRC-0001":{"reading_id":"K2DEEP-QM-SRC-0001","source_id":"QM-SRC-0001","canonical_sha256":"a"*64,"page_start":1,"page_end":10,"pages_reviewed_count":10,"read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"}}
    courses={"QM-SRC-0001":{"source_id":"QM-SRC-0001","course_family_id":"COURSE-QM-1","course_role":"FOUNDATION","independent_vote_allowed":False}}
    family_sources=set()
    prior={"OLD-1":{"distillate_id":"OLD-1","source_id":"QM-SRC-0001"}}
    reaudit={"QM-SRC-0001":"COMPLETE"}
    return sources,lineage,readings,courses,family_sources,prior,reaudit


def row(**o):
    r={
      "distillate_id":"K2DS-QM-SRC-0001","source_id":"QM-SRC-0001","work_id":"WORK-1","domain":"qimen",
      "distillation_scope":"DEEP_SOURCE_BOOK","reading_ref":"K2DEEP-QM-SRC-0001","canonical_sha256":"a"*64,
      "source_anchors":["QM-SRC-0001@pdf:p1"],"course_family_id":"COURSE-QM-1","course_role":"FOUNDATION",
      "independence_policy":"COURSE_FAMILY_SINGLE_VOTE","prior_distillate_refs":["OLD-1"],"evidence_reaudit_coverage":"COMPLETE",
      "source_credit":"FULL_SOURCE_VISUAL_REVIEWED","empirical_credit":"NONE","essence":["x"],"method_map":["x"],
      "applicability_constraints":[],"source_limitations":["x"],"conflicts_and_tensions":[],"anti_patterns":[],"model_updates":["x"],
      "testable_hypotheses":[{"hypothesis_id":"H1","statement":"x","freeze_requirements":"x","failure_condition":"x","status":"UNTESTED"}],
      "excluded_from_operational_use":[],"claim_extraction_blocked":True,"acceptance_status":"K2B_SOURCE_REVIEW_ACCEPTED",
      "distillation_status":"REVIEWED","review_status":"REVIEWED","copyright_class":"DERIVED_SYNTHESIS_SAFE"
    }
    r.update(o);return r


def main():
    idx=indexes()
    assert not v.inspect(row(),idx),v.inspect(row(),idx)

    issues=v.inspect(row(independence_policy="DEFAULT"),idx)
    assert any("COURSE_FAMILY_SINGLE_VOTE" in m for _,m in issues),issues

    issues=v.inspect(row(source_anchors=["QM-SRC-0001@pdf:p11"]),idx)
    assert any("outside canonical pages" in m for _,m in issues),issues

    issues=v.inspect(row(empirical_credit="FULL"),idx)
    assert any("empirical credit" in m for _,m in issues),issues

    bad_idx=list(idx);bad_idx[4]={"QM-SRC-0001"};bad_idx=tuple(bad_idx)
    issues=v.inspect(row(),bad_idx)
    assert any("work-family" in m for _,m in issues),issues

    issues=v.inspect(row(evidence_reaudit_coverage="NOT_APPLICABLE"),idx)
    assert any("current target coverage" in m for _,m in issues),issues

    state={"status":"COMPLETE","targets":[{"source_id":"QM-SRC-0001","required":True}]}
    assert not v.validate_rows([row()],state,idx),v.validate_rows([row()],state,idx)
    issues=v.validate_rows([],state,idx)
    assert any("required deep-source distillate missing" in m for _,m in issues),issues
    print("k2-deep-source-distillate-tests: PASS")

if __name__=="__main__":main()
