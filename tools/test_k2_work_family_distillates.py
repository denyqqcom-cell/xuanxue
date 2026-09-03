#!/usr/bin/env python3
import copy,json,sys,tempfile
from pathlib import Path
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_work_family_distillates as v

FAM="WF-QM-TEST-001"
MFAM="WF-ZW-TEST-MULTI-001"


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


def multi_domain_indexes():
    families=defaultdict(list)
    families[MFAM]=[
        {"member_ref":"ZW-SRC-9000#SEG-001","member_kind":"SEGMENT","source_id":"ZW-SRC-9000","segment_id":"ZW-SRC-9000#SEG-001","work_title":"跨域甲书","domain_routes":["ziwei","fengshui"]},
    ]
    readings={
        "K2DEEP-ZW-SRC-9000":{"reading_id":"K2DEEP-ZW-SRC-9000","source_id":"ZW-SRC-9000","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE"},
    }
    ev={
        "K2SEG-ZW9000-001":{"evidence_id":"K2SEG-ZW9000-001","work_family_key":MFAM},
        "K2SEG-ZW9000-002":{"evidence_id":"K2SEG-ZW9000-002","work_family_key":MFAM},
    }
    segs={"ZW-SRC-9000#SEG-001":{"segment_id":"ZW-SRC-9000#SEG-001","page_start":1,"page_end":8}}
    sources={"ZW-SRC-9000":{"source_id":"ZW-SRC-9000","pages":8}}
    return families,readings,ev,segs,sources


def multi_domain_row():
    return {
        "anti_patterns":["不能把跨域路由压成单一 domain 标签"],
        "applicability_constraints":["跨域解释必须反馈前冻结"],
        "claim_extraction_blocked":True,
        "conflicts_and_tensions":["跨域覆盖增加结果后路线切换风险"],
        "copyright_class":"DERIVED_SYNTHESIS_SAFE",
        "credit_decisions":[{"anchors":["K2SEG-ZW9000-001"],"decision":"RETAIN_WITH_ROUTE_FREEZE","empirical_credit":"NONE","source_credit":"FULL","summary":"来源支持多域方法路由，不支持现实有效性。","topic":"multi_domain_route"}],
        "direct_source_locators":[],
        "distillate_id":"K2WF-ZW-TEST-MULTI-001",
        "distillation_status":"REVIEWED",
        "domain":"ziwei",
        "domain_routes":["ziwei","fengshui"],
        "empirical_credit":"NONE",
        "essence":["保留跨域路由而不压平"],
        "excluded_from_operational_use":["未经验证的高影响现实决策"],
        "member_refs":["ZW-SRC-9000#SEG-001"],
        "method_map":["先冻结 route 再解释"],
        "model_updates":["work-family distillate 显式记录全部 governed routes"],
        "reading_refs":["K2DEEP-ZW-SRC-9000"],
        "review_status":"REVIEWED",
        "segment_evidence_refs":["K2SEG-ZW9000-001","K2SEG-ZW9000-002"],
        "source_credit":"FULL_WORK_FAMILY_REVIEWED",
        "source_limitations":["没有前瞻验证"],
        "testable_hypotheses":[{"failure_condition":"冻结路由不改善复核一致性则失败","freeze_requirements":"反馈前冻结允许的 domain route","hypothesis_id":"H-MULTI-001","statement":"显式多域路由能降低结果后 route shopping","status":"UNTESTED"}],
        "work_family_key":MFAM,
        "work_title":"跨域甲书",
    }


def must_pass(rows):
    issues=v.validate_rows(*indexes(),rows)
    assert not issues,issues


def must_fail(rows,needle):
    issues=v.validate_rows(*indexes(),rows)
    assert issues,"expected failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert needle in text,(needle,text)


def test_shard_loader():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);k=root/"knowledge";k.mkdir()
        base=copy.deepcopy(row());base["distillate_id"]="K2WF-QM-BASE-001"
        shard=copy.deepcopy(row());shard["distillate_id"]="K2WF-QM-SHARD-001"
        (k/"K2_WORK_FAMILY_DISTILLATES.jsonl").write_text(json.dumps(base,ensure_ascii=False)+"\n",encoding="utf-8")
        d=k/"K2_WORK_FAMILY_DISTILLATES.d";d.mkdir()
        (d/"one.jsonl").write_text(json.dumps(shard,ensure_ascii=False)+"\n",encoding="utf-8")
        rows=v.load_distillates(root)
        assert [r["distillate_id"] for r in rows]==["K2WF-QM-BASE-001","K2WF-QM-SHARD-001"],rows


def test_multi_domain_routes():
    base=multi_domain_row()
    issues=v.validate_rows(*multi_domain_indexes(),[base])
    assert not issues,issues
    r=copy.deepcopy(base);r["domain_routes"]=["ziwei"]
    issues=v.validate_rows(*multi_domain_indexes(),[r])
    assert issues,"expected multi-domain route coverage failure"
    text="; ".join(f"{a}: {b}" for a,b in issues)
    assert "domain_routes must exactly cover work-family routes" in text,text


def main():
    base=row();must_pass([base])
    test_shard_loader()
    test_multi_domain_routes()

    r=copy.deepcopy(base);r["member_refs"]=["QM-SRC-9000"];must_fail([r],"exactly match")
    r=copy.deepcopy(base);r["reading_refs"]=["K2DEEP-QM-SRC-9000"];must_fail([r],"cover exactly")
    r=copy.deepcopy(base);r["segment_evidence_refs"]=[];must_fail([r],"exactly match current family")
    r=copy.deepcopy(base);r["direct_source_locators"]=["QM-SRC-9001#SEG-001@pdf:p2"];must_fail([r],"reserved for SOURCE members")
    r=copy.deepcopy(base);r["empirical_credit"]="VALIDATED";must_fail([r],"cannot grant empirical credit")
    r=copy.deepcopy(base);r["testable_hypotheses"][0]["status"]="CONFIRMED";must_fail([r],"must remain UNTESTED")
    r=copy.deepcopy(base);r["credit_decisions"][0]["empirical_credit"]="VALIDATED";must_fail([r],"cannot grant empirical credit")
    r=copy.deepcopy(base);r["claim_extraction_blocked"]=False;must_fail([r],"must remain true")

    print("k2-work-family-distillates-tests: PASS")
    print("cases=12")

if __name__=="__main__":main()
