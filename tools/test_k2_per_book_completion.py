#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import k2_wave1_aggregate as agg
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
    dump(k / agg.BASE_LEDGER, [])
    dump(k / agg.BASE_EVIDENCE, [])
    dump(k / agg.BASE_DISTILLATES, [])
    return k


def main():
    # Authoritative progress must include both base rows and per-book shards.
    # This is the regression that Issue #19 is fixing: a base-only validator
    # must never report itself as the global Wave1 progress view.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.BASE_LEDGER,
            [{"reading_id": "R-A", "source_id": "A"}],
        )
        dump(
            k / agg.BASE_EVIDENCE,
            [{"evidence_id": "E-A-1", "source_id": "A"}],
        )
        dump(
            k / agg.SHARD_DIRS["ledger"] / "B.jsonl",
            [{"reading_id": "R-B", "source_id": "B"}],
        )
        dump(
            k / agg.SHARD_DIRS["evidence"] / "B.jsonl",
            [
                {"evidence_id": "E-B-1", "source_id": "B"},
                {"evidence_id": "E-B-2", "source_id": "B"},
            ],
        )
        ledger, evidence, distillates = agg.aggregate_wave1(root)
        assert [r["reading_id"] for r in ledger] == ["R-A", "R-B"], ledger
        assert [r["evidence_id"] for r in evidence] == ["E-A-1", "E-B-1", "E-B-2"], evidence
        assert distillates == [], distillates

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "A"}],
        )
        dump(
            k / agg.SHARD_DIRS["evidence"] / "A.jsonl",
            [{"evidence_id": "E-A-1", "source_id": "A"}],
        )
        dump(
            k / agg.SHARD_DIRS["distillate"] / "A.jsonl",
            [{"distillate_id": "D-A", "source_id": "A"}],
        )
        ledger, evidence, distillates = agg.aggregate_wave1(root)
        assert [r["reading_id"] for r in ledger] == ["R-A"]
        assert [r["evidence_id"] for r in evidence] == ["E-A-1"]
        assert [r["distillate_id"] for r in distillates] == ["D-A"]

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "B"}],
        )
        expect_block(lambda: agg.aggregate_wave1(root), "shard/source mismatch")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(k / agg.BASE_LEDGER, [{"reading_id": "R-A-BASE", "source_id": "A"}])
        dump(
            k / agg.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A-SHARD", "source_id": "A"}],
        )
        expect_block(lambda: agg.aggregate_wave1(root), "duplicate Reading source base+shard")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.SHARD_DIRS["ledger"] / "A.jsonl",
            [{"reading_id": "R-A", "source_id": "A"}],
        )
        dump(
            k / agg.SHARD_DIRS["evidence"] / "A.jsonl",
            [
                {"evidence_id": "E-DUP", "source_id": "A"},
                {"evidence_id": "E-DUP", "source_id": "A"},
            ],
        )
        expect_block(lambda: agg.aggregate_wave1(root), "duplicate Evidence id")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.SHARD_DIRS["evidence"] / "A.jsonl",
            [{"evidence_id": "E-A-1", "source_id": "A"}],
        )
        expect_block(lambda: agg.aggregate_wave1(root), "Evidence shard without Reading row")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        k = base_files(root)
        dump(
            k / agg.SHARD_DIRS["ledger"] / "A.jsonl",
            [
                {"reading_id": "R-A-1", "source_id": "A"},
                {"reading_id": "R-A-2", "source_id": "A"},
            ],
        )
        expect_block(lambda: agg.aggregate_wave1(root), "Reading shard cardinality")

    rows = [{"evidence_id": "X", "source_id": "A"}, {"evidence_id": "X", "source_id": "B"}]
    expect_block(lambda: agg.ensure_unique(rows, "evidence_id", "evidence"), "global duplicate id")

    # Per-book completion must consume the same authoritative aggregation
    # contract rather than maintaining a second loader with different semantics.
    assert v.aggregate is agg.aggregate_wave1

    print("k2-per-book-completion-tests: PASS")


if __name__ == "__main__":
    main()
