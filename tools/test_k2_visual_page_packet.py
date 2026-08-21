#!/usr/bin/env python3
"""Portable fail-closed tests for the K2 VISUAL_REQUIRED page renderer."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "tools" / "build_k2_visual_page_packet.py"


def sha_file(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(cmd, expect_success=True):
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if expect_success and proc.returncode != 0:
        raise AssertionError(
            f"command failed rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        )
    if not expect_success and proc.returncode == 0:
        raise AssertionError(
            f"command unexpectedly succeeded\nstdout={proc.stdout}\nstderr={proc.stderr}"
        )
    return proc


def write_plan(path: Path, digest: str, pages=2, lane="VISUAL_REQUIRED"):
    row = {
        "source_id": "QM-SRC-TEST",
        "file_sha256": digest,
        "pages": pages,
        "execution_lane": lane,
    }
    path.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python-deps-dir", type=Path)
    args = ap.parse_args()

    deps = args.python_deps_dir
    if deps is None:
        raw = os.environ.get("K2_PYTHON_DEPS")
        deps = Path(raw) if raw else None
    if deps is None or not deps.is_dir():
        raise AssertionError("K2 isolated dependency directory is required")

    deps_value = str(deps.resolve())
    if deps_value not in sys.path:
        sys.path.insert(0, deps_value)

    import pypdf

    with tempfile.TemporaryDirectory() as td:
        temp = Path(td).resolve()
        source_dir = temp / "source"
        source_dir.mkdir()
        pdf_path = source_dir / "scan.pdf"

        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=400, height=500)
        with pdf_path.open("wb") as fh:
            writer.write(fh)

        digest = sha_file(pdf_path)
        plan = temp / "plan.jsonl"
        write_plan(plan, digest)
        output_dir = temp / "visual-packet"

        base_cmd = [
            sys.executable,
            str(HELPER),
            "--plan",
            str(plan),
            "--source-id",
            "QM-SRC-TEST",
            "--search-root",
            str(source_dir),
            "--python-deps-dir",
            str(deps),
            "--output-dir",
            str(output_dir),
            "--dpi",
            "96",
        ]
        proc = run(base_cmd)
        assert "READY_FOR_VISUAL_REVIEW" in proc.stdout
        assert "review_credit_granted=false" in proc.stdout

        manifest_path = output_dir / "QM-SRC-TEST.visual_manifest.json"
        assert manifest_path.is_file()
        raw_manifest = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(raw_manifest)
        assert manifest["schema_version"] == "k2-visual-page-packet-v1"
        assert manifest["source_file_sha256"] == digest
        assert manifest["packet_status"] == "READY_FOR_VISUAL_REVIEW"
        assert manifest["review_credit_granted"] is False
        assert manifest["ocr_performed"] is False
        assert manifest["semantic_extraction_performed"] is False
        assert manifest["registered_page_count"] == 2
        assert manifest["rendered_page_count"] == 2
        assert len(manifest["pages"]) == 2
        assert str(pdf_path) not in raw_manifest
        assert "local_path" not in raw_manifest

        for expected_page, row in enumerate(manifest["pages"], 1):
            assert row["page"] == expected_page
            image_path = output_dir / row["image_file"]
            assert image_path.is_file()
            assert sha_file(image_path) == row["image_sha256"]
            assert row["width_px"] > 0
            assert row["height_px"] > 0
            with image_path.open("rb") as fh:
                assert fh.read(8) == b"\x89PNG\r\n\x1a\n"

        # Page-count mismatch must fail closed even though canonical bytes resolve.
        bad_pages_plan = temp / "bad-pages.jsonl"
        write_plan(bad_pages_plan, digest, pages=3)
        bad_pages_cmd = list(base_cmd)
        bad_pages_cmd[bad_pages_cmd.index(str(plan))] = str(bad_pages_plan)
        bad_pages_output = temp / "bad-pages-output"
        bad_pages_cmd[bad_pages_cmd.index(str(output_dir))] = str(bad_pages_output)
        run(bad_pages_cmd, expect_success=False)

        # A TEXT_DIRECT source must not be silently rendered through this path.
        wrong_lane_plan = temp / "wrong-lane.jsonl"
        write_plan(wrong_lane_plan, digest, lane="TEXT_DIRECT")
        wrong_lane_cmd = list(base_cmd)
        wrong_lane_cmd[wrong_lane_cmd.index(str(plan))] = str(wrong_lane_plan)
        wrong_lane_output = temp / "wrong-lane-output"
        wrong_lane_cmd[wrong_lane_cmd.index(str(output_dir))] = str(wrong_lane_output)
        run(wrong_lane_cmd, expect_success=False)

        # Rendered research pages must never be written inside the repository.
        forbidden_output = ROOT / "should-not-exist-k2-visual-output"
        forbidden_cmd = list(base_cmd)
        forbidden_cmd[forbidden_cmd.index(str(output_dir))] = str(forbidden_output)
        run(forbidden_cmd, expect_success=False)
        assert not forbidden_output.exists()

    print("k2-visual-page-packet-tests: PASS")


if __name__ == "__main__":
    main()
