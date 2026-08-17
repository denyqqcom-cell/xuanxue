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
      "source_id":"BZ-SRC-0001","work_id":"WORK-000001","relation":"PRIMARY_WORK",
      "part_label":None,"variant_of_source_id":None,"parent_work_ids":[],
      "independence_class":"PRIMARY_CANDIDATE","lineage_basis":"TITLE_MATCH","lineage_evidence":"same canonical work title",
      "k2_eligible":True,"read_priority":"P0","review_status":"REVIEWED"
    }
    r.update(overrides); return r

def main():
    assert not v.inspect(row(),source())

    issues=v.inspect(row(relation="SAME_WORK_VARIANT",independence_class="SAME_WORK_NOT_INDEPENDENT"),source())
    assert any("variant_of_source_id" in msg for _,msg in issues),issues

    part=row(
        relation="WORK_PART",part_label="卷二",independence_class="SAME_WORK_NOT_INDEPENDENT",
        lineage_evidence="same titled work; this carrier contains only volume two",read_priority="P1")
    assert not v.inspect(part,source()),v.inspect(part,source())
    issues=v.inspect(dict(part,part_label=None),source())
    assert any("part_label" in msg for _,msg in issues),issues

    issues=v.inspect(row(),source(evidence_role="SECONDARY_NOTE"))
    assert any("secondary note" in msg.lower() for _,msg in issues),issues
    issues=v.inspect(row(),source(evidence_role="IMPLEMENTATION_EVIDENCE"))
    assert any("implementation" in msg.lower() for _,msg in issues),issues

    oos_text=row(
        relation="OUT_OF_SCOPE",independence_class="NOT_ELIGIBLE",k2_eligible=False,
        read_priority="SKIP",lineage_evidence="content belongs to another divination system")
    assert not v.inspect(oos_text,source(knowledge_domains=["OUT_OF_SCOPE"])),v.inspect(oos_text,source(knowledge_domains=["OUT_OF_SCOPE"]))

    oos_code=row(
        relation="IMPLEMENTATION",independence_class="IMPLEMENTATION_ONLY",k2_eligible=False,
        read_priority="SKIP",lineage_basis="PROJECT_CODE_PATH",lineage_evidence="project accessory implementation")
    assert not v.inspect(oos_code,source(evidence_role="IMPLEMENTATION_EVIDENCE",knowledge_domains=["OUT_OF_SCOPE"])),v.inspect(oos_code,source(evidence_role="IMPLEMENTATION_EVIDENCE",knowledge_domains=["OUT_OF_SCOPE"]))

    unknown=row(
        relation="UNKNOWN",work_id=None,independence_class="UNKNOWN",lineage_basis="UNKNOWN",
        lineage_evidence=None,k2_eligible=False,read_priority="P3")
    assert not v.inspect(unknown,source()),v.inspect(unknown,source())

    print("k2-source-lineage-tests: PASS")

if __name__=="__main__": main()
