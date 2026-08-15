#!/usr/bin/env python3
"""Validate structured metaphysics handoff packs before they can influence code.

This validator checks engineering provenance contracts only. It does not certify
that a traditional rule is true or that a prediction method is scientifically valid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_ROOT = ROOT / "handoff"

REQUIRED_FILES = (
    "00_CORPUS_MANIFEST.md",
    "01_SYSTEM_MAP.md",
    "02_ALGORITHM_SPEC.md",
    "03_RULES.jsonl",
    "04_CONFLICTS.md",
    "05_FIXTURES.jsonl",
    "06_CASES.md",
    "07_COPYRIGHT_GATE.md",
    "08_IMPLEMENTATION_HANDOFF.md",
    "09_OPEN_QUESTIONS.md",
    "HANDOFF_SUMMARY.md",
)

RULE_FIELDS = {
    "rule_id",
    "category",
    "statement",
    "conditions",
    "inputs",
    "outputs",
    "school",
    "source_ids",
    "source_location",
    "confidence",
    "conflicts_with",
    "implementation_ready",
    "notes",
}

FIXTURE_FIELDS = {
    "fixture_id",
    "kind",
    "input",
    "expected",
    "compare_fields",
    "source_ids",
    "source_location",
    "known_outcome_case",
    "notes",
}

FORBIDDEN_BINARY_SUFFIXES = {
    ".pdf", ".epub", ".mobi", ".doc", ".docx", ".rtf",
    ".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff",
    ".ttf", ".otf",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_jsonl(path: Path, errors: list[str]) -> list[tuple[int, dict]]:
    rows: list[tuple[int, dict]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: row must be a JSON object")
            continue
        rows.append((line_no, value))
    if not rows:
        fail(errors, f"{path.relative_to(ROOT)}: must contain at least one JSON object")
    return rows


def contains_model_only(value: object) -> bool:
    return "MODEL_KNOWLEDGE_ONLY" in json.dumps(value, ensure_ascii=False)


def validate_rules(module: Path, errors: list[str]) -> None:
    path = module / "03_RULES.jsonl"
    rows = load_jsonl(path, errors)
    seen: set[str] = set()
    for line_no, row in rows:
        missing = RULE_FIELDS - row.keys()
        if missing:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: missing fields {sorted(missing)}")
        rule_id = row.get("rule_id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: rule_id must be non-empty string")
        elif rule_id in seen:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: duplicate rule_id {rule_id}")
        else:
            seen.add(rule_id)

        confidence = row.get("confidence")
        if confidence not in {"A", "B", "C", "D"}:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: confidence must be A/B/C/D")

        source_ids = row.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids or not all(isinstance(x, str) and x.strip() for x in source_ids):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: source_ids must be a non-empty string list")

        ready = row.get("implementation_ready")
        if not isinstance(ready, bool):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: implementation_ready must be boolean")
        if ready is True and contains_model_only(row):
            fail(
                errors,
                f"{path.relative_to(ROOT)}:{line_no}: MODEL_KNOWLEDGE_ONLY rule cannot be implementation_ready=true",
            )


def validate_fixtures(module: Path, errors: list[str]) -> None:
    path = module / "05_FIXTURES.jsonl"
    rows = load_jsonl(path, errors)
    seen: set[str] = set()
    for line_no, row in rows:
        missing = FIXTURE_FIELDS - row.keys()
        if missing:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: missing fields {sorted(missing)}")
        fixture_id = row.get("fixture_id")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: fixture_id must be non-empty string")
        elif fixture_id in seen:
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: duplicate fixture_id {fixture_id}")
        else:
            seen.add(fixture_id)

        source_ids = row.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids or not all(isinstance(x, str) and x.strip() for x in source_ids):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: source_ids must be a non-empty string list")

        if not isinstance(row.get("known_outcome_case"), bool):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: known_outcome_case must be boolean")

        if contains_model_only(row):
            fail(errors, f"{path.relative_to(ROOT)}:{line_no}: MODEL_KNOWLEDGE_ONLY content cannot enter golden fixtures")


def validate_module(module: Path, errors: list[str]) -> None:
    rel = module.relative_to(ROOT)
    for name in REQUIRED_FILES:
        path = module / name
        if not path.is_file() or path.stat().st_size == 0:
            fail(errors, f"{rel}: missing or empty required file {name}")

    for path in module.rglob("*"):
        if path.is_file() and path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            fail(errors, f"{path.relative_to(ROOT)}: binary/source-book asset is forbidden inside public handoff")

    if (module / "03_RULES.jsonl").is_file():
        validate_rules(module, errors)
    if (module / "05_FIXTURES.jsonl").is_file():
        validate_fixtures(module, errors)

    copyright_gate = module / "07_COPYRIGHT_GATE.md"
    if copyright_gate.is_file():
        gate_text = copyright_gate.read_text(encoding="utf-8")
        if "App" not in gate_text and "APP" not in gate_text:
            fail(errors, f"{copyright_gate.relative_to(ROOT)}: copyright gate must explicitly discuss App distribution")


def main() -> int:
    errors: list[str] = []
    if not HANDOFF_ROOT.is_dir():
        print("handoff directory does not exist", file=sys.stderr)
        return 1

    modules = sorted(
        path for path in HANDOFF_ROOT.iterdir()
        if path.is_dir() and (path / "HANDOFF_SUMMARY.md").exists()
    )
    if not modules:
        print("No completed handoff modules found; nothing to validate.")
        return 0

    for module in modules:
        validate_module(module, errors)

    if errors:
        print("HANDOFF VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"HANDOFF VALIDATION PASS: {', '.join(path.name for path in modules)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
