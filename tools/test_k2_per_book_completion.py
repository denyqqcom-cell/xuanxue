#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_k2_per_book_completion as v


def dump(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows),
        encoding="utf-8",
    )


def expect_block(fn, label):
    try:
        fn()
    except SystemExit as exc:
        assert exc.code == 1, (label, exc.code)
        return
    raise AssertionError(f"expected fail-closed block: {label}")


def base_files(root):
    k = root / "knowledge"
    k.mkdir(parents=True, exist_ok=True)
    dump(k / v.BASE_LEDGER, [])
    dump(k / v.BASE_EVIDENCE, [])
    dump(k / v.BASE_DISTILLATES, [])
    return k


def main():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / v.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "A"}],
        )
        dump(
            k / v.SHARD_DIRS["evidence"] / "A.jsonl",
            [{"evidence_id": "E-A-1", "source_id": "A"}],
        )
        dump(
            k / v.SHARD_DIRS["distillate"] / "A.jsonl",
            [{"distillate_id": "D-A", "source_id": "A"}],
        )
        ledger, evidence, distillates = v.aggregate(root)
        assert [r["reading_id"] for r in ledger] == ["R-A"]
        assert [r["evidence_id"] for r in evidence] == ["E-A-1"]
        assert [r["distillate_id"] for r in distillates] == ["D-A"]

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / v.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "B"}],
        )
        expect_block(lambda: v.aggregate(root), "shard/source mismatch")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(k / v.BASE_LEDGER, [{"reading_id": "R-A-BASE", "source_id": "A"}])
        dump(
            k / v.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A-SHARD", "source_id": "A"}],
        )
        expect_block(lambda: v.aggregate(root), "duplicate Reading source base+shard")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / v.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "A"}],
        )
        dump(
            k / v.SHARD_DIRS["evidence"] / "A.jsonl",
            [
                {"evidence_id": "E-DUP", "source_id": "A"},
                {"evidence_id": "E-DUP", "source_id": "A"},
            ],
        )
        expect_block(lambda: v.aggregate(root), "duplicate Evidence id")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / v.SHARD_DIRS["evidence"] / "A.jsonl",
            [{"evidence_id": "E-A-1", "source_id": "A"}],
        )
        expect_block(lambda: v.aggregate(root), "Evidence shard without Reading row")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / v.SHARD_DIRS["ledger"] / "A.jsonl",
            [
                {"reading_id": "R-A-1", "source_id": "A"},
                {"reading_id": "R-A-2", "source_id": "A"},
            ],
        )
        expect_block(lambda: v.aggregate(root), "Reading shard cardinality")

    rows = [{"evidence_id": "X", "source_id": "A"}, {"evidence_id": "X", "source_id": "B"}]
    expect_block(lambda: v.ensure_unique(rows, "evidence_id", "evidence"), "global duplicate id")

    print("k2-per-book-completion-tests: PASS")


if __name__ == "__main__":
    main()
