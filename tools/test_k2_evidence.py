#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_evidence as v
import build_k2_local_page_packets as packets


def main():
    sources={
      "A":{"source_id":"A","knowledge_domains":["ziwei"],"pages":10,"readability":"TEXT_OK"},
      "B":{"source_id":"B","knowledge_domains":["ziwei"],"pages":20,"readability":"SCAN"},
      "C":{"source_id":"C","knowledge_domains":["liuyao"],"pages":30,"readability":"OCR_WEAK"},
      "D":{"source_id":"D","knowledge_domains":["UNKNOWN"],"pages":40,"readability":"TEXT_OK"},
    }
    lineage={
      "A":{"source_id":"A","work_id":"W1","relation":"WORK_PART","k2_eligible":True,"read_priority":"P0"},
      "B":{"source_id":"B","work_id":"W1","relation":"WORK_PART","k2_eligible":True,"read_priority":"P2"},
      "C":{"source_id":"C","work_id":"W2","relation":"PRIMARY_WORK","k2_eligible":True,"read_priority":"P1"},
      "D":{"source_id":"D","work_id":None,"relation":"UNKNOWN","k2_eligible":False,"read_priority":"P3"},
    }
    expected=v.wave1_expected(sources,lineage)
    assert expected=={"A","B","C"},expected
    assert v.expected_execution_lane(sources["A"])=="TEXT_DIRECT"
    assert v.expected_execution_lane(sources["B"])=="VISUAL_REQUIRED"
    assert v.expected_execution_lane(sources["C"])=="VISUAL_REQUIRED"
    issues=[]
    cov=v.range_union([{"start":1,"end":5},{"start":6,"end":10}],10,issues,"A")
    assert len(cov)==10 and not issues,(cov,issues)
    issues=[]
    v.range_union([{"start":1,"end":11}],10,issues,"A")
    assert any("exceeds" in m for _,m in issues),issues
    assert v.PATH_RE.search("/home/user/book.pdf")
    assert v.PDF_LOC_RE.search("printed:p5|pdf:p8-p9")
    assert "VISION_UNAVAILABLE" in v.BLOCKER_CODES

    assert str(packets.normalize_local_path(r"E:\\books\\a.pdf"))=="/mnt/e/books/a.pdf"
    assert packets.sha_text("abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    try:
        packets.ensure_local_only(packets.ROOT / "knowledge-intake-test")
    except SystemExit:
        pass
    else:
        raise AssertionError("local page-packet helper must reject repository-contained output")

    print("k2-evidence-tests: PASS")

if __name__=="__main__":main()
