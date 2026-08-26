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

    # A packet must be semantically readable, not merely non-empty. Normal
    # Chinese/Latin text and ordinary East-Asian mixed scripts are valid;
    # synthetic font/CMap damage spanning many unrelated scripts must fail closed.
    readable_cjk = ["紫微斗數 命宮 天機 四化 三方四正"] * 2
    readable_latin = ["Ziwei astrolabe method layer and timing model"] * 2
    readable_japanese = ["紫微斗数の命宮をみる テスト カタカナ"] * 2
    readable_cjk_latin = ["紫微斗數 Ziwei method v1 四化 timing layer"] * 2
    garbled = [("ΩЖشമԱሀᐁϞЯعകՖሴᑕ " * 24).strip()] * 2
    assert p.text_layer_is_semantically_readable(readable_cjk)
    assert p.text_layer_is_semantically_readable(readable_latin)
    assert p.text_layer_is_semantically_readable(readable_japanese)
    assert p.text_layer_is_semantically_readable(readable_cjk_latin)
    assert not p.text_layer_is_semantically_readable(garbled)

    # A second false-positive class is a scanned/image-backed book that carries
    # only a small repeated advertisement/watermark text layer. Such a layer is
    # perfectly valid Unicode, but it does not cover the source body and must not
    # be accepted as a TEXT_DIRECT page packet. The contract deliberately uses
    # repeated low-information page signatures rather than source-specific words.
    overlay_a = "获取更多资料 example.invalid 联系方式 123456"
    overlay_b = "更多资料 example.invalid 备用联系方式 654321"
    overlay_only = [overlay_a if i % 2 == 0 else overlay_b for i in range(24)]
    source_body = [
        f"第{i}页 紫微斗數命宮與三方四正的正文分析，這一頁有不同的章節內容與推演關係。"
        for i in range(1, 25)
    ]
    assert not p.text_layer_has_semantic_coverage(overlay_only)
    assert p.text_layer_has_semantic_coverage(source_body)

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

        # Unicode-valid repeated overlay text must also trigger extractor
        # fallback. If every extractor sees only the overlay, fail closed rather
        # than writing a misleading READY packet.
        p.extract_pdf_text_pdftotext = lambda path: (overlay_only, None)
        p.extract_pdf_text_pypdf = lambda path: (overlay_only, None)
        p.extract_pdf_text_pdfminer = lambda path: (source_body, None)
        pages, extractor, code, reason = p.extract_pdf_text(Path("synthetic.pdf"))
        assert pages == source_body
        assert extractor == "PDFMINER_TEXT_LAYER"
        assert code is None and reason is None

        p.extract_pdf_text_pdfminer = lambda path: (overlay_only, None)
        pages, extractor, code, reason = p.extract_pdf_text(Path("synthetic.pdf"))
        assert pages is None
        assert extractor is None
        assert code == "TEXT_EXTRACTION_FAILED"
        assert "semantic coverage" in reason.lower()
    finally:
        p.extract_pdf_text_pdftotext = original_pdftotext
        p.extract_pdf_text_pypdf = original_pypdf
        p.extract_pdf_text_pdfminer = original_pdfminer

    print("k2-local-page-packet-tests: PASS")


if __name__ == "__main__":
    main()
