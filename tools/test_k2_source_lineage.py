#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_source_lineage as v


def source(**overrides):
    s={"source_id":"BZ-SRC-0001","evidence_role":"TEXTUAL_SOURCE","knowledge_domains":["bazi"]}
    s.update(overrides); return s

def row(**overrides):
    r={
      "source_id":"BZ-SRC-0001","work_id":"WORK-000001","relation":"PRIMARY_WORK","parent_work_ids":[],
      "independence_class":"PRIMARY_CANDIDATE","lineage_basis":"TITLE_MATCH","lineage_evidence":"same canonical work title",
      "k2_eligible":True,"read_priority":"P0","review_status":"REVIEWED"
    }
    r.update(overrides); return r

def main():
    assert not v.inspect(row(),source())
    issues=v.inspect(row(relation="SAME_WORK_VARIANT"),source())
    assert any("same-work" in msg for _,msg in issues),issues
    issues=v.inspect(row(),source(evidence_role="SECONDARY_NOTE"))
    assert any("secondary note" in msg for _,msg in issues),issues
    issues=v.inspect(row(),source(evidence_role="IMPLEMENTATION_EVIDENCE"))
    assert any("implementation" in msg for _,msg in issues),issues
    issues=v.inspect(row(relation="OUT_OF_SCOPE",independence_class="NOT_ELIGIBLE",k2_eligible=False,read_priority="SKIP"),source(knowledge_domains=["OUT_OF_SCOPE"]))
    assert not issues,issues
    issues=v.inspect(row(relation="UNKNOWN",work_id=None,independence_class="UNKNOWN",lineage_basis="UNKNOWN",lineage_evidence=None,read_priority="P3"),source())
    assert not issues,issues
    print("k2-source-lineage-tests: PASS")

if __name__=="__main__": main()
