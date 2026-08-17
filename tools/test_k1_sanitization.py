#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sanitize_k1_sources as s


def sample(**overrides):
    row = {
        "source_id": "ZW-SRC-0001",
        "domain": "ziwei",
        "title": "示例书",
        "author": "UNKNOWN",
        "source_type": "BOOK",
        "era": "UNKNOWN",
        "edition": None,
        "local_path": "/home/private/books/a.pdf",
        "file_sha256": "a" * 64,
        "pages": 100,
        "size_bytes": 123456,
        "readability": "SCAN",
        "school_ids": [],
        "copyright": "RESEARCH_ONLY",
        "local_only": True,
        "status": "INDEXED",
        "duplicate_of": None,
        "sampled_locations": ["p.1"],
        "notes": "local audit only",
    }
    row.update(overrides)
    return row


def main():
    out = s.sanitize_row(sample(), "ziwei")
    for forbidden in ["local_path", "size_bytes", "sampled_locations", "notes"]:
        assert forbidden not in out, forbidden
    assert out["record_scope"] == "SANITIZED_METADATA_ONLY"
    assert out["packaged"] is False
    assert out["local_only"] is True

    failed = False
    try:
        s.sanitize_row(sample(title="/home/private/leak"), "ziwei")
    except SystemExit:
        failed = True
    assert failed, "path-like title must fail closed"

    print("k1-sanitization-tests: PASS")


if __name__ == "__main__":
    main()
