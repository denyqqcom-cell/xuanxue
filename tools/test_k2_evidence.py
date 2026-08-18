#!/usr/bin/env python3
import os
import tempfile
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_evidence as v
import build_k2_local_page_packets as packets
import show_k2_page_packet as show


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

    # Incremental Wave1 review contract: only actually reviewed rows may emit Evidence,
    # and each lane must use a verification mode that matches its source quality.
    assert v.WAVE_STATES=={"WAVE1_OPEN","WAVE1_REVIEW_REQUIRED","COMPLETE"}
    assert v.READ_STATUSES=={"NOT_STARTED","PARTIAL","COMPLETE","BLOCKED"}
    assert v.EVIDENCE_ALLOWED_READ_STATUSES=={"PARTIAL","COMPLETE"}
    assert v.FINAL_READ_STATUSES=={"COMPLETE","BLOCKED"}

    issues=[]
    v.validate_verification_for_reviewed_source("A","TEXT_DIRECT","TEXT_LAYER_FULL",issues)
    assert not issues,issues
    issues=[]
    v.validate_verification_for_reviewed_source("A","TEXT_DIRECT","NONE",issues)
    assert any("TEXT_DIRECT" in m for _,m in issues),issues
    issues=[]
    v.validate_verification_for_reviewed_source("B","VISUAL_REQUIRED","VISUAL_PAGE",issues)
    assert not issues,issues
    issues=[]
    v.validate_verification_for_reviewed_source("B","VISUAL_REQUIRED","TEXT_LAYER_FULL",issues)
    assert any("VISUAL_REQUIRED" in m for _,m in issues),issues
    issues=[]
    v.validate_verification_for_reviewed_source("C","ACCESS_REVIEW","NONE",issues)
    assert any("ACCESS_REVIEW" in m for _,m in issues),issues

    posix=packets.normalize_local_path(r"E:\books\a.pdf",host_os="posix")
    win=packets.normalize_local_path(r"E:\books\a.pdf",host_os="nt")
    wsl_win=packets.normalize_local_path("/mnt/f/books/a.pdf",host_os="nt")
    assert posix.as_posix()=="/mnt/e/books/a.pdf",posix
    assert win.as_posix().lower()=="e:/books/a.pdf",win
    assert wsl_win.as_posix().lower()=="f:/books/a.pdf",wsl_win

    assert packets.sha_text("abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    packets.validate_plan([{"source_id":"A","file_sha256":"a"*64}])
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        books=root/"books"
        books.mkdir()
        sample=books/"sample.pdf"
        sample.write_bytes(b"abc")
        digest=packets.sha_file(sample)
        assert digest=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

        matches=packets.discover_hash_matches([root],{digest},root/"packets-out")
        assert matches[digest] and matches[digest][0].name=="sample.pdf",matches

        private={"source_id":"A","file_sha256":digest}
        item={"source_id":"A","file_sha256":digest}
        packets.verify_private_registry_hash("A",item,private)
        assert packets.verify_local_file_hash("A",digest,sample)==digest

        # Exercise the pypdf fallback without depending on PDF internals.
        deps=root/"deps"
        pypdf_pkg=deps/"pypdf"
        pypdf_pkg.mkdir(parents=True)
        (pypdf_pkg/"__init__.py").write_text(
            "class _Page:\n"
            "    def __init__(self,t): self.t=t\n"
            "    def extract_text(self, extraction_mode=None): return self.t\n"
            "class PdfReader:\n"
            "    def __init__(self,path,strict=False): self.pages=[_Page('alpha'),_Page('beta')]\n",
            encoding="utf-8",
        )

        # Exercise the pdfminer.six fallback with its page-separator contract.
        pdfminer_pkg=deps/"pdfminer"
        pdfminer_pkg.mkdir(parents=True)
        (pdfminer_pkg/"__init__.py").write_text("",encoding="utf-8")
        (pdfminer_pkg/"high_level.py").write_text(
            "def extract_text(path): return 'gamma\\fdelta\\f'\n",
            encoding="utf-8",
        )

        packets.configure_python_deps(deps)
        sys.modules.pop("pypdf",None)
        pages, reason=packets.extract_pdf_text_pypdf(sample)
        assert pages==["alpha","beta"] and reason is None,(pages,reason)
        sys.modules.pop("pypdf",None)

        sys.modules.pop("pdfminer.high_level",None)
        sys.modules.pop("pdfminer",None)
        pages, reason=packets.extract_pdf_text_pdfminer(sample)
        assert pages==["gamma","delta"] and reason is None,(pages,reason)
        sys.modules.pop("pdfminer.high_level",None)
        sys.modules.pop("pdfminer",None)

        packet=root/"A.pages.jsonl"
        packets.write_packet(packet,"A",digest,["p1","p2","p3"])
        rows=show.load_packet(packet,"A")
        selected=show.select_pages(rows,2,3)
        assert [r["page"] for r in selected]==[2,3]
        assert show.MAX_PAGES_PER_CALL==25
    try:
        packets.ensure_local_only(packets.ROOT / "knowledge-intake-test")
    except SystemExit:
        pass
    else:
        raise AssertionError("local page-packet helper must reject repository-contained output")

    print("k2-evidence-tests: PASS")
    print(f"host_os={os.name}")

if __name__=="__main__":main()
