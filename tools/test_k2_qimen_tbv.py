#!/usr/bin/env python3
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_k2_qimen_tbv as gate


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")


def assert_issue(issues, needle):
    if not any(needle in issue for issue in issues):
        raise AssertionError(f"expected issue containing {needle!r}; got {issues[:8]}")


def with_repo(mutator):
    with tempfile.TemporaryDirectory(prefix="qimen-tbv-") as tmp:
        repo = Path(tmp)
        shutil.copytree(ROOT / "knowledge", repo / "knowledge")
        mutator(repo)
        return gate.validate(repo)


def main():
    baseline = gate.validate(ROOT)
    if baseline:
        raise AssertionError(f"current TBV state must pass: {baseline[:8]}")

    def empirical_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl"
        rows = load_jsonl(path)
        rows[0]["empirical_credit"] = "VALIDATED"
        write_jsonl(path, rows)
    assert_issue(with_repo(empirical_mut), "empirical_credit must remain NONE")

    def universal_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl"
        rows = load_jsonl(path)
        rows[0]["universalization_status"] = "ALLOWED"
        write_jsonl(path, rows)
    assert_issue(with_repo(universal_mut), "universalization must remain BLOCKED")

    def false_complete_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_STATE.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["full_reviewed_material_tbv_coverage"] = True
        state["status"] = "COMPLETE"
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    issues = with_repo(false_complete_mut)
    assert_issue(issues, "full_reviewed_material_tbv_coverage must be false")
    assert_issue(issues, "TBV state status must be PARTIAL")

    def ref_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl"
        rows = load_jsonl(path)
        rows[0]["source_refs"] = ["knowledge/DOES_NOT_EXIST.jsonl"]
        write_jsonl(path, rows)
    assert_issue(with_repo(ref_mut), "missing source_ref path")

    def family_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl"
        rows = load_jsonl(path)
        rows[-1]["unit_id"] = "WF-QM-FAKE-001"
        write_jsonl(path, rows)
    issues = with_repo(family_mut)
    assert_issue(issues, "unknown reviewed work family")
    assert_issue(issues, "Wave B seed coverage missing")

    def backlog_mut(repo):
        path = repo / "knowledge" / "K2_UNKNOWN_TEXTUAL_BACKLOG.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["remaining_unknown_textual_source_count"] = 92
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert_issue(with_repo(backlog_mut), "TBV state/backlog count drift")

    def protocol_mut(repo):
        path = repo / "knowledge" / "K2_QIMEN_TBV_PROTOCOL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("KNOWN_OUTCOME_TRAINING != PROSPECTIVE_EVALUATION", "KNOWN_OUTCOME_TRAINING == PROSPECTIVE_EVALUATION")
        path.write_text(text, encoding="utf-8")
    assert_issue(with_repo(protocol_mut), "TBV protocol missing invariant")

    print("k2-qimen-tbv-tests: PASS")


if __name__ == "__main__":
    main()
