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

    print("k2-local-page-packet-tests: PASS")


if __name__ == "__main__":
    main()
