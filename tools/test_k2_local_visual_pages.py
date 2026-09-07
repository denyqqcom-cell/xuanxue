#!/usr/bin/env python3
import hashlib
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_k2_local_visual_pages as v


def expect_system_exit(fn):
    try:
        fn()
    except SystemExit:
        return
    raise AssertionError("expected SystemExit")


def valid_plan_row(file_sha256="0" * 64):
    return {
        "source_id": "BZ-SRC-TEST",
        "file_sha256": file_sha256,
        "pages": 2,
        "execution_lane": "VISUAL_REQUIRED",
        "readability": "SCAN",
        "source_type": "BOOK",
        "copyright": "FORBIDDEN_TO_PACKAGE",
        "local_only": True,
        "packaged": False,
        "record_scope": "SANITIZED_METADATA_ONLY",
        "author_basis": "FILENAME",
    }


def test_plan_and_dpi_contracts():
    row = valid_plan_row()
    v.validate_visual_plan([row])

    bad = dict(row)
    bad["execution_lane"] = "TEXT_DIRECT"
    expect_system_exit(lambda: v.validate_visual_plan([bad]))

    bad = dict(row)
    bad.pop("record_scope")
    expect_system_exit(lambda: v.validate_visual_plan([bad]))

    bad = dict(row)
    bad["readability"] = "TEXT_OK"
    expect_system_exit(lambda: v.validate_visual_plan([bad]))

    assert v.validate_dpi(160) == 160
    expect_system_exit(lambda: v.validate_dpi(40))
    expect_system_exit(lambda: v.validate_dpi(401))

    assert v.classify_rendered_page_count(2, 2) == (None, None)
    code, reason = v.classify_rendered_page_count(1, 2)
    assert code == "PDF_RENDER_PAGE_COUNT_MISMATCH"
    assert "rendered PDF page count 1" in reason
    assert "physical PDF pages 2" in reason


def test_renderer_capability_and_page_artifacts():
    with tempfile.TemporaryDirectory(prefix="k2-visual-render-test-") as td:
        root = Path(td)
        source = root / "source.pdf"
        source.write_bytes(b"synthetic")
        out = root / "rendered"

        original_import = v.importlib.import_module
        try:
            def unavailable(name):
                if name == "pypdfium2":
                    raise ModuleNotFoundError("No module named 'pypdfium2'")
                return original_import(name)

            v.importlib.import_module = unavailable
            rows, renderer, code, reason = v.render_pdf_pdfium(
                source, out, "BZ-SRC-TEST", "0" * 64, 160
            )
            assert rows is None
            assert renderer is None
            assert code == "PDF_RENDER_SURFACE_UNAVAILABLE"
            assert "pypdfium2" in reason.lower()
        finally:
            v.importlib.import_module = original_import

        class FakeImage:
            def __init__(self, page_index):
                self.page_index = page_index
                self.size = (100 + page_index, 200 + page_index)

            def save(self, path, format=None):
                assert format == "PNG"
                Path(path).write_bytes(f"png-{self.page_index}".encode("ascii"))

            def close(self):
                pass

        class FakeBitmap:
            def __init__(self, page_index):
                self.page_index = page_index

            def to_pil(self):
                return FakeImage(self.page_index)

            def close(self):
                pass

        class FakePage:
            def __init__(self, page_index):
                self.page_index = page_index

            def render(self, scale=1):
                assert scale == 160 / 72.0
                return FakeBitmap(self.page_index)

            def close(self):
                pass

        class FakeDocument:
            def __init__(self, path):
                assert path == str(source)

            def __len__(self):
                return 2

            def __getitem__(self, page_index):
                return FakePage(page_index)

            def close(self):
                pass

        class FakePdfium:
            PdfDocument = FakeDocument
            __version__ = "TEST"

        class FakePIL:
            __version__ = "TEST"

        try:
            def fake_import(name):
                if name == "pypdfium2":
                    return FakePdfium
                if name == "PIL.Image":
                    return FakePIL
                return original_import(name)

            v.importlib.import_module = fake_import
            rows, renderer, code, reason = v.render_pdf_pdfium(
                source, out, "BZ-SRC-TEST", "0" * 64, 160
            )
        finally:
            v.importlib.import_module = original_import

        assert renderer == "PYPDFIUM2"
        assert code is None and reason is None
        assert len(rows) == 2
        assert rows[0]["page"] == 1 and rows[1]["page"] == 2
        assert rows[0]["width_px"] == 100 and rows[1]["height_px"] == 201
        assert rows[0]["image_file"] == "page-0001.png"
        assert (out / "page-0001.png").is_file()
        assert rows[0]["image_sha256"] != rows[1]["image_sha256"]
        assert all("text" not in row for row in rows)


def test_real_renderer_smoke_from_isolated_target():
    """Windows portability CI supplies K2_PYTHON_DEPS; use it for a real render."""
    raw_target = os.environ.get("K2_PYTHON_DEPS")
    if not raw_target:
        return
    target = Path(raw_target)
    if not target.is_dir():
        raise AssertionError(f"K2_PYTHON_DEPS does not exist: {target}")
    v.base.configure_python_deps(target)
    pypdf = importlib.import_module("pypdf")

    with tempfile.TemporaryDirectory(prefix="k2-visual-real-render-") as td:
        root = Path(td)
        source = root / "one-page.pdf"
        writer = pypdf.PdfWriter()
        try:
            writer.add_blank_page(width=72, height=72)
            with source.open("wb") as fh:
                writer.write(fh)
        finally:
            close = getattr(writer, "close", None)
            if callable(close):
                close()

        out = root / "rendered"
        digest = v.base.sha_file(source)
        rows, renderer, code, reason = v.render_pdf_pdfium(
            source, out, "BZ-SRC-REAL", digest, 144
        )
        assert code is None, reason
        assert renderer == "PYPDFIUM2"
        assert len(rows) == 1
        assert rows[0]["page"] == 1
        assert rows[0]["source_file_sha256"] == digest
        assert rows[0]["width_px"] > 0 and rows[0]["height_px"] > 0
        assert (out / "page-0001.png").is_file()
        assert (out / "page-0001.png").stat().st_size > 0


def test_renderer_failure_redacts_local_carrier_path():
    with tempfile.TemporaryDirectory(prefix="k2-visual-redaction-test-") as td:
        root = Path(td)
        source = root / "secret-carrier.pdf"
        source.write_bytes(b"synthetic")
        out = root / "rendered"
        original_import = v.importlib.import_module

        class BrokenPdfium:
            class PdfDocument:
                def __init__(self, path):
                    raise RuntimeError(f"cannot open {path}")

        try:
            v.importlib.import_module = (
                lambda name: BrokenPdfium
                if name == "pypdfium2"
                else object()
                if name == "PIL.Image"
                else original_import(name)
            )
            rows, renderer, code, reason = v.render_pdf_pdfium(
                source, out, "BZ-SRC-TEST", "0" * 64, 160
            )
        finally:
            v.importlib.import_module = original_import

        assert rows is None
        assert renderer == "PYPDFIUM2"
        assert code == "PDF_RENDER_FAILED"
        assert str(source) not in reason
        assert "<LOCAL_CARRIER>" in reason


def test_main_emits_execution_only_manifest_without_local_path():
    with tempfile.TemporaryDirectory(prefix="k2-visual-main-test-") as td:
        root = Path(td)
        search = root / "search"
        search.mkdir()
        source = search / "carrier.pdf"
        source.write_bytes(b"visual-carrier-test")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        plan_path = root / "plan.jsonl"
        plan_path.write_text(
            json.dumps(valid_plan_row(digest), ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        out = root / "out"

        original_inspect = v.base.inspect_pdf_material_page_count
        original_render = v.render_pdf_pdfium
        original_argv = sys.argv[:]
        try:
            v.base.inspect_pdf_material_page_count = (
                lambda path: (2, "TEST_PAGE_TREE", None, None)
            )

            def fake_render(path, source_out, source_id, source_hash, dpi):
                source_out.mkdir(parents=True, exist_ok=True)
                rows = []
                for page in (1, 2):
                    image = source_out / f"page-{page:04d}.png"
                    image.write_bytes(f"page-{page}".encode("ascii"))
                    rows.append({
                        "source_id": source_id,
                        "source_file_sha256": source_hash,
                        "page": page,
                        "image_file": image.name,
                        "image_sha256": v.base.sha_file(image),
                        "width_px": 100,
                        "height_px": 200,
                        "dpi": dpi,
                        "renderer": "PYPDFIUM2",
                    })
                return rows, "PYPDFIUM2", None, None

            v.render_pdf_pdfium = fake_render
            sys.argv = [
                "build_k2_local_visual_pages.py",
                "--plan", str(plan_path),
                "--search-root", str(search),
                "--output-dir", str(out),
                "--dpi", "160",
            ]
            v.main()
        finally:
            v.base.inspect_pdf_material_page_count = original_inspect
            v.render_pdf_pdfium = original_render
            sys.argv = original_argv

        manifest_rows = [
            json.loads(line)
            for line in (out / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert len(manifest_rows) == 1
        row = manifest_rows[0]
        assert row["execution_status"] == "VISUAL_PAGES_READY"
        assert row["rendered_page_count"] == 2
        assert row["renderer"] == "PYPDFIUM2"
        assert row["source_file_sha256"] == digest
        assert row["visual_manifest_file"] == "BZ-SRC-TEST/visual-pages.jsonl"
        assert row["policy_snapshot"]["copyright"] == "FORBIDDEN_TO_PACKAGE"
        assert row["policy_snapshot"]["packaged"] is False
        assert row["reading_credit"] == "NONE"
        assert "local_path" not in row
        assert "source_path" not in row
        assert str(source) not in json.dumps(row, ensure_ascii=False)
        assert (out / "BZ-SRC-TEST" / "visual-pages.jsonl").is_file()


def main():
    test_plan_and_dpi_contracts()
    test_renderer_capability_and_page_artifacts()
    test_real_renderer_smoke_from_isolated_target()
    test_renderer_failure_redacts_local_carrier_path()
    test_main_emits_execution_only_manifest_without_local_path()
    print("k2-local-visual-pages-tests: PASS")


if __name__ == "__main__":
    main()
