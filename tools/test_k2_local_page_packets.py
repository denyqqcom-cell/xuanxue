#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_k2_local_page_packets as p


def main():
    win = p.normalize_local_path(r"E:\\books\\a.pdf")
    assert str(win) == "/mnt/e/books/a.pdf", win

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        intake = root / "intake"
        domain = intake / "ziwei"
        domain.mkdir(parents=True)
        src = domain / "book.txt"
        src.write_text("page text", encoding="utf-8")
        (domain / "sources.jsonl").write_text(
            json.dumps({"source_id": "ZW-SRC-X", "local_path": str(src)}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        index = p.private_source_index(intake)
        assert index["ZW-SRC-X"]["local_path"] == str(src)
        assert p.sha_text("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

    try:
        p.ensure_local_only(p.ROOT / "knowledge-intake-test")
    except SystemExit:
        pass
    else:
        raise AssertionError("repository-contained output must be rejected")

    # A packet must be semantically readable, not merely non-empty.  Normal
    # Chinese and normal Latin text are both valid; synthetic font/CMap damage
    # spanning many unrelated scripts must fail closed.
    readable_cjk = ["紫微斗數 命宮 天機 四化 三方四正"] * 2
    readable_latin = ["Ziwei astrolabe method layer and timing model"] * 2
    garbled = [("ΩЖشമԱሀᐁϞЯعകՖሴᑕ " * 24).strip()] * 2
    assert p.text_layer_is_semantically_readable(readable_cjk)
    assert p.text_layer_is_semantically_readable(readable_latin)
    assert not p.text_layer_is_semantically_readable(garbled)

    # If an earlier extractor returns non-empty but semantically garbled text,
    # the helper must continue to the next text-layer extractor instead of
    # producing a false READY packet.
    original_pdftotext = p.extract_pdf_text_pdftotext
    original_pypdf = p.extract_pdf_text_pypdf
    original_pdfminer = p.extract_pdf_text_pdfminer
    try:
        p.extract_pdf_text_pdftotext = lambda path: (None, "not installed")
        p.extract_pdf_text_pypdf = lambda path: (garbled, None)
        p.extract_pdf_text_pdfminer = lambda path: (readable_cjk, None)
        pages, extractor, code, reason = p.extract_pdf_text(Path("synthetic.pdf"))
        assert pages == readable_cjk
        assert extractor == "PDFMINER_TEXT_LAYER"
        assert code is None and reason is None

        # If every available text-layer path is unreadable, fail closed. OCR is
        # still outside this helper's contract.
        p.extract_pdf_text_pypdf = lambda path: (garbled, None)
        p.extract_pdf_text_pdfminer = lambda path: (garbled, None)
        pages, extractor, code, reason = p.extract_pdf_text(Path("synthetic.pdf"))
        assert pages is None
        assert extractor is None
        assert code == "TEXT_EXTRACTION_FAILED"
        assert "semantic readability" in reason.lower()
    finally:
        p.extract_pdf_text_pdftotext = original_pdftotext
        p.extract_pdf_text_pypdf = original_pypdf
        p.extract_pdf_text_pdfminer = original_pdfminer

    print("k2-local-page-packet-tests: PASS")


if __name__ == "__main__":
    main()
