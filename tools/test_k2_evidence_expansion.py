#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_k2_evidence_expansion as ex


def assert_issue(issues, needle):
    assert any(needle in msg for _, msg in issues), (needle, issues)


def main():
    # Real repository must satisfy the expansion contract.
    issues, source_ids, complete, evidence_count = ex.validate_repo(ex.ROOT)
    assert not issues, issues
    assert source_ids == ["QM-SRC-0017"], source_ids
    assert complete == 1, complete
    assert evidence_count == 18, evidence_count

    # Fail closed on duplicate expansion sources.
    sources = {
        "X": {"source_id": "X", "knowledge_domains": ["qimen"], "evidence_role": "TEXTUAL_SOURCE", "readability": "SCAN"},
    }
    lineage = {
        "X": {"source_id": "X", "work_id": "WX", "relation": "PRIMARY_WORK", "k2_eligible": True, "read_priority": "P2"},
    }
    manifest = {
        "schema_version": "k2-evidence-expansion-v1",
        "status": "ACTIVE",
        "source_ids": ["X", "X"],
        "selection_rule": "test",
        "review_status": "REVIEWED",
    }
    issues, _ = ex.validate_manifest(manifest, sources, lineage)
    assert_issue(issues, "duplicate source_ids")

    # Fail closed on non-eligible textual source.
    lineage_bad = {
        "X": {"source_id": "X", "work_id": "WX", "relation": "PRIMARY_WORK", "k2_eligible": False, "read_priority": "P2"},
    }
    manifest["source_ids"] = ["X"]
    issues, _ = ex.validate_manifest(manifest, sources, lineage_bad)
    assert_issue(issues, "k2_eligible=true")

    # Fail closed when a source already belongs to base Wave1.
    sources_wave = {
        "A": {"source_id": "A", "knowledge_domains": ["qimen"], "evidence_role": "TEXTUAL_SOURCE", "readability": "TEXT_OK"},
    }
    lineage_wave = {
        "A": {"source_id": "A", "work_id": "WA", "relation": "PRIMARY_WORK", "k2_eligible": True, "read_priority": "P0"},
    }
    manifest_wave = {
        "schema_version": "k2-evidence-expansion-v1",
        "status": "ACTIVE",
        "source_ids": ["A"],
        "selection_rule": "test",
        "review_status": "REVIEWED",
    }
    issues, _ = ex.validate_manifest(manifest_wave, sources_wave, lineage_wave)
    assert_issue(issues, "already belongs to base Wave1")

    print("k2-evidence-expansion-tests: PASS")


if __name__ == "__main__":
    main()
