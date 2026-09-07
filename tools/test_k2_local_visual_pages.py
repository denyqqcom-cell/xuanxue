#!/usr/bin/env python3
import hashlib
import importlib
import json
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
    assert "1 != 2" in reason


def test_renderer_capability_and_page_artifacts():
    with tempfile.TemporaryDirectory(prefix="k2-visual-render-test-") as td:
        root = Path(td)
        source = root / "source.pdf"
        source.write_bytes(b"synthetic")
        out = root / "rendered"

        original_import = v.importlib.import_module
        try:
            def unavailable(name):
                if name == "pymupdf":
                    raise ModuleNotFoundError("No module named 'pymupdf'")
                return original_import(name)

            v.importlib.import_module = unavailable
            rows, renderer, code, reason = v.render_pdf_pymupdf(
                source, out, "BZ-SRC-TEST", "0" * 64, 160
            )
            assert rows is None
            assert renderer is None
            assert code == "PDF_RENDER_SURFACE_UNAVAILABLE"
            assert "pymupdf" in reason.lower()
        finally:
            v.importlib.import_module = original_import

        class FakeMatrix:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        class FakePixmap:
            def __init__(self, page_index):
                self.page_index = page_index
                self.width = 100 + page_index
                self.height = 200 + page_index

            def save(self, path):
                Path(path).write_bytes(f"png-{self.page_index}".encode("ascii"))

        class FakePage:
            def __init__(self, page_index):
                self.page_index = page_index

            def get_pixmap(self, matrix=None, alpha=True):
                assert isinstance(matrix, FakeMatrix)
                assert alpha is False
                return FakePixmap(self.page_index)

        class FakeDocument:
            page_count = 2

            def load_page(self, page_index):
                return FakePage(page_index)

            def close(self):
                pass

        class FakePyMuPDF:
            Matrix = FakeMatrix
            __version__ = "TEST"

            @staticmethod
            def open(path):
                assert path == str(source)
                return FakeDocument()

        try:
            v.importlib.import_module = (
                lambda name: FakePyMuPDF if name == "pymupdf" else original_import(name)
            )
            rows, renderer, code, reason = v.render_pdf_pymupdf(
                source, out, "BZ-SRC-TEST", "0" * 64, 160
            )
        finally:
            v.importlib.import_module = original_import

        assert renderer == "PYMUPDF"
        assert code is None and reason is None
        assert len(rows) == 2
        assert rows[0]["page"] == 1 and rows[1]["page"] == 2
        assert rows[0]["width_px"] == 100 and rows[1]["height_px"] == 201
        assert rows[0]["image_file"] == "page-0001.png"
        assert (out / "page-0001.png").is_file()
        assert rows[0]["image_sha256"] != rows[1]["image_sha256"]
        assert all("text" not in row for row in rows)


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
        original_render = v.render_pdf_pymupdf
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
                        "renderer": "PYMUPDF",
                    })
                return rows, "PYMUPDF", None, None

            v.render_pdf_pymupdf = fake_render
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
            v.render_pdf_pymupdf = original_render
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
        assert row["renderer"] == "PYMUPDF"
        assert row["source_file_sha256"] == digest
        assert row["visual_manifest_file"] == "BZ-SRC-TEST/visual-pages.jsonl"
        assert row["policy_snapshot"]["copyright"] == "FORBIDDEN_TO_PACKAGE"
        assert row["policy_snapshot"]["packaged"] is False
        assert "local_path" not in row
        assert "source_path" not in row
        assert (out / "BZ-SRC-TEST" / "visual-pages.jsonl").is_file()


def main():
    test_plan_and_dpi_contracts()
    test_renderer_capability_and_page_artifacts()
    test_main_emits_execution_only_manifest_without_local_path()
    print("k2-local-visual-pages-tests: PASS")


if __name__ == "__main__":
    main()
