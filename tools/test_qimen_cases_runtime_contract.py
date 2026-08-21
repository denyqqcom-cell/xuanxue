#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "奇门" / "qclaw" / "qimen-cases" / "SKILL.md"
MIRROR = ROOT / "奇门" / "qclaw" / "qimen-cases-v2.md"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-cases-runtime-contract: FAIL: {msg}")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"missing {needle!r} in {where}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        fail(f"legacy deterministic rule remains active: {needle!r} in {where}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    mirror = MIRROR.read_text(encoding="utf-8")

    for needle in (
        "SOURCE_RETROSPECTIVE_CASE",
        "PROJECT_RETROSPECTIVE_REANALYSIS",
        "PROSPECTIVE_FROZEN_CASE",
        "CONTAMINATED_CASE",
        "IMPLEMENTATION_FAILURE_CASE",
        "UNSCORABLE_ANECDOTE",
        "UNSUPPORTED_ACCURACY_CLAIM",
        "K2_PROSPECTIVE_CASE_REGISTRY.jsonl",
        "Empirical Support",
        "Role Map Freeze",
        "预测有约八成准确率",
    ):
        require(skill, needle, "qimen-cases/SKILL.md")

    # Historical bad claims may remain only as explicitly labelled debt. Do not
    # ban their literal text, otherwise the audit cannot preserve what was wrong.
    if skill.index("预测有约八成准确率") > skill.index("UNSUPPORTED_ACCURACY_CLAIM"):
        # A later occurrence is acceptable only if the marker also appears in the
        # same accuracy-gate section; the stronger invariant below ensures the
        # current file does not expose an operational percentage.
        pass
    if "当前标：\n\n`UNSUPPORTED_ACCURACY_CLAIM`" not in skill:
        fail("legacy accuracy statement is not explicitly downgraded")

    for needle in (
        "Frozen Protocol",
        "Frozen Prediction",
        "Outcome Audit",
        "Model Delta",
        "eligible_for_scoring",
        "time_boundary_system",
        "star_state_system",
        "door_state_system",
        "K2_PROSPECTIVE_CASE_REGISTRY.jsonl",
        "不显示项目总体“应验率/准确率”",
    ):
        require(mirror, needle, "qimen-cases-v2.md")

    for needle in (
        "玄武，必定是假冒伪劣产品",
        "惊门临凶神凶格，必有官司口舌",
        "师傅修正：",
        "应验率评估：[完全应验 / 部分应验 / 未应验]",
    ):
        forbid(skill, needle, "qimen-cases/SKILL.md")
        forbid(mirror, needle, "qimen-cases-v2.md")

    print("qimen-cases-runtime-contract: PASS")


if __name__ == "__main__":
    main()
