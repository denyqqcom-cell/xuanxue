#!/usr/bin/env python3
import copy,sys
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_work_family_distillates as v

FAM="WF-QM-TEST-001"


def indexes():
    families=defaultdict(list)
    families[FAM]=[
        {"member_ref":"QM-SRC-9000","member_kind":"SOURCE","source_id":"QM-SRC-9000","segment_id":None,"work_title":"甲书","domain_routes":["qimen"]},
        {"member_ref":"QM-SRC-9001#SEG-001","member_kind":"SEGMENT","source_id":"QM-SRC-9001","segment_id":"QM-SRC-9001#SEG-001","work_title":"甲书","domain_routes":["qimen"]},
    ]
    readings={
        "K2DEEP-QM-SRC-9000":{"reading_id":"K2DEEP-QM-SRC-9000","source_id":"QM-SRC-9000","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"},
        "K2DEEP-QM-SRC-9001":{"reading_id":"K2DEEP-QM-SRC-9001","source_id":"QM-SRC-9001","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"},
    }
    ev={
        "K2SEG-QM9001-001":{"evidence_id":"K2SEG-QM9001-001","work_family_key":FAM}
    }
    segs={"QM-SRC-9001#SEG-001":{"segment_id":"QM-SRC-9001#SEG-001","page_start":1,"page_end":3}}
    sources={
        "QM-SRC-9000":{"source_id":"QM-SRC-9000","pages":5},
        "QM-SRC-9001":{"source_id":"QM-SRC-9001","pages":6},
    }
    return families,readings,ev,segs,sources


def row():
    return {
        "anti_patterns":["不能压成静态词典"],
        "applicability_constraints":["规则绑定具体上下文"],
        "claim_extraction_blocked":True,
        "conflicts_and_tensions":["先拆上下文再判冲突"],
        "copyright_class":"DERIVED_SYNTHESIS_SAFE",
        "credit_decisions":[{"anchors":["QM-SRC-9000@pdf:p2","K2SEG-QM9001-001"],"decision":"RETAIN","empirical_credit":"NONE","source_credit":"FULL","summary":"来源支持方法结构，不支持现实有效性。","topic":"method"}],
        "direct_source_locators":["QM-SRC-9000@pdf:p2"],
        "distillate_id":"K2WF-QM-TEST-001",
        "distillation_status":"REVIEWED",
        "domain":"qimen",
        "empirical_credit":"NONE",
        "essence":["保留关系结构"],
        "excluded_from_operational_use":["高风险现实决策"],
        "member_refs":["QM-SRC-9000","QM-SRC-9001#SEG-001"],
        "method_map":["对象进入关系网络后判断"],
        "model_updates":["从静态字典转关系模型"],
        "reading_refs":["K2DEEP-QM-SRC-9000","K2DEEP-QM-SRC-9001"],
        "review_status":"REVIEWED",
        "segment_evidence_refs":["K2SEG-QM9001-001"],
        "source_credit":"FULL_WORK_FAMILY_REVIEWED",
        "source_limitations":["没有前瞻验证"],
        "testable_hypotheses":[{"failure_condition":"盲测不改善则失败","freeze_requirements":"反馈前冻结规则集","hypothesis_id":"H-001","statement":"关系模型优于静态词典","status":"UNTESTED"}],
        "work_family_key":FAM,
        "work_title":"甲书",
    }


def must_pass(rows):
    issues=v.validate_rows(*indexes(),rows)
    assert not issues,issues


def must_fail(rows,needle):
    issues=v.validate_rows(*indexes(),rows)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def main():
    base=row();must_pass([base])

    r=copy.deepcopy(base);r["member_refs"]=["QM-SRC-9000"];must_fail([r],"exactly match")
    r=copy.deepcopy(base);r["reading_refs"]=["K2DEEP-QM-SRC-9000"];must_fail([r],"cover exactly")
    r=copy.deepcopy(base);r["segment_evidence_refs"]=[];must_fail([r],"exactly match current family")
    r=copy.deepcopy(base);r["direct_source_locators"]=["QM-SRC-9001#SEG-001@pdf:p2"];must_fail([r],"reserved for SOURCE members")
    r=copy.deepcopy(base);r["empirical_credit"]="VALIDATED";must_fail([r],"cannot grant empirical credit")
    r=copy.deepcopy(base);r["testable_hypotheses"][0]["status"]="CONFIRMED";must_fail([r],"must remain UNTESTED")
    r=copy.deepcopy(base);r["credit_decisions"][0]["empirical_credit"]="VALIDATED";must_fail([r],"cannot grant empirical credit")
    r=copy.deepcopy(base);r["claim_extraction_blocked"]=False;must_fail([r],"must remain true")

    print("k2-work-family-distillates-tests: PASS")
    print("cases=9")

if __name__=="__main__":main()
