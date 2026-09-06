#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_k2_local_page_packets as packets


def main():
    original_pypdf = packets.count_pdf_pages_pypdf
    original_pdfminer = packets.count_pdf_pages_pdfminer
    try:
        # A page-tree counter can verify material cardinality independently of
        # whether any text can be extracted from those pages.
        packets.count_pdf_pages_pypdf = lambda path: (113, None)
        packets.count_pdf_pages_pdfminer = lambda path: (None, "pdfminer unavailable: synthetic")
        count, counter, code, reason = packets.inspect_pdf_material_page_count(Path("synthetic.pdf"))
        assert count == 113
        assert counter == "PYPDF_PAGE_TREE"
        assert code is None and reason is None

        # A later accepted page-tree reader may recover after an unavailable
        # earlier dependency; this must still verify the material page count.
        packets.count_pdf_pages_pypdf = lambda path: (None, "pypdf unavailable: synthetic")
        packets.count_pdf_pages_pdfminer = lambda path: (113, None)
        count, counter, code, reason = packets.inspect_pdf_material_page_count(Path("synthetic.pdf"))
        assert count == 113
        assert counter == "PDFMINER_PAGE_TREE"
        assert code is None and reason is None

        # Zero executable page counters is a runner-capability condition, not a
        # statement that the exact canonical carrier has the wrong page count.
        packets.count_pdf_pages_pdfminer = lambda path: (None, "pdfminer unavailable: synthetic")
        count, counter, code, reason = packets.inspect_pdf_material_page_count(Path("synthetic.pdf"))
        assert count is None and counter is None
        assert code == "PDF_PAGE_COUNTER_UNAVAILABLE"

        # If a page counter actually attempts the PDF but cannot read the page
        # tree, keep that distinct from dependency absence and from mismatch.
        packets.count_pdf_pages_pypdf = lambda path: (None, "pypdf page count failed: ValueError: bad tree")
        count, counter, code, reason = packets.inspect_pdf_material_page_count(Path("synthetic.pdf"))
        assert count is None and counter is None
        assert code == "PDF_PAGE_COUNT_FAILED"
        assert "bad tree" in reason
    finally:
        packets.count_pdf_pages_pypdf = original_pypdf
        packets.count_pdf_pages_pdfminer = original_pdfminer

    code, reason = packets.classify_pdf_material_page_count(113, 113)
    assert code is None and reason is None

    code, reason = packets.classify_pdf_material_page_count(112, 113)
    assert code == "PDF_PAGE_COUNT_MISMATCH"
    assert "physical PDF page count 112" in reason
    assert "registered PDF pages 113" in reason

    # Unknown registered cardinality does not invent a mismatch claim.
    code, reason = packets.classify_pdf_material_page_count(113, None)
    assert code is None and reason is None

    print("k2-pdf-material-page-count-tests: PASS")


if __name__ == "__main__":
    main()
