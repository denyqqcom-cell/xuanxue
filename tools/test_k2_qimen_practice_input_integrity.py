#!/usr/bin/env python3
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_k2_qimen_practice_input_integrity as gate


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_issue(issues, needle):
    if not any(needle in x for x in issues):
        raise AssertionError(f"expected {needle!r}; got {issues}")


def with_repo(mutator):
    with tempfile.TemporaryDirectory(prefix="qimen-input-integrity-") as tmp:
        repo = Path(tmp)
        shutil.copytree(ROOT / "knowledge", repo / "knowledge")
        mutator(repo)
        return gate.validate(repo)


def main():
    baseline = gate.validate(ROOT)
    assert not baseline, baseline

    def remove_layer(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["required"].remove("plate_layer")
        write_json(p, data)
    assert_issue(with_repo(remove_layer), "required-field contract incomplete")

    def remove_dun_mode(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["required"].remove("dun_mode")
        write_json(p, data)
    assert_issue(with_repo(remove_dun_mode), "required-field contract incomplete")

    def corrupt_dun_enum(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["dun_mode"]["enum"] = ["YANG_DUN", "NOT_APPLICABLE", "UNRESOLVED"]
        write_json(p, data)
    assert_issue(with_repo(corrupt_dun_enum), "dun_mode enum drift")

    def allow_collapse(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["instance_collapse_blocked"]["const"] = False
        write_json(p, data)
    assert_issue(with_repo(allow_collapse), "instance collapse")

    def remove_contested(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["readback_status"]["enum"].remove("CONTESTED")
        write_json(p, data)
    assert_issue(with_repo(remove_contested), "readback_status enum drift")

    def universalize_semantics(repo):
        p = repo / "knowledge" / "schema" / "qimen_symbolic_mapping.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["semantics_status"]["enum"] = ["UNIVERSAL"]
        write_json(p, data)
    assert_issue(with_repo(universalize_semantics), "semantics_status enum drift")

    def unlink_scenario(repo):
        p = repo / "knowledge" / "schema" / "qimen_scenario_reasoning.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["symbolic_mapping_hypotheses"]["items"] = {"type": "object"}
        write_json(p, data)
    assert_issue(with_repo(unlink_scenario), "must bind qimen_symbolic_mapping schema")

    def open_tie_break(repo):
        p = repo / "knowledge" / "schema" / "qimen_scenario_reasoning.schema.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["properties"]["decision_tie_break_policy"]["additionalProperties"] = True
        write_json(p, data)
    assert_issue(with_repo(open_tie_break), "tie-break policy must be closed object")

    def weaken_protocol(repo):
        p = repo / "knowledge" / "K2_QIMEN_PRACTICE_INPUT_INTEGRITY_PROTOCOL.md"
        text = p.read_text(encoding="utf-8").replace("SAME STEM != SAME STATE", "SAME STEM == SAME STATE")
        p.write_text(text, encoding="utf-8")
    assert_issue(with_repo(weaken_protocol), "protocol missing invariant")

    print("k2-qimen-practice-input-integrity-tests: PASS")
    print("cases=9")


if __name__ == "__main__":
    main()
