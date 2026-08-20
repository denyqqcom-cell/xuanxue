#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "奇门" / "qclaw" / "qimen-qiju" / "SKILL.md"
REG = ROOT / "奇门" / "qclaw" / "qimen-qiju" / "SETUP_METHOD_REGISTRY.md"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-qiju-runtime-contract: FAIL: {msg}")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"missing {needle!r} in {where}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        fail(f"legacy active rule remains: {needle!r} in {where}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    reg = REG.read_text(encoding="utf-8")

    for needle in (
        "Setup Method Registry",
        "setup_method",
        "setup_calibration",
        "seasonal_alignment",
        "time_boundary_system",
        "TERMINOLOGY_DIRECTION_CONFLICT",
        "ALGORITHM_VARIANT_REQUIRED",
        "DEFINITION_OVERLAP_UNRESOLVED",
        "IMPLEMENTATION_AMBIGUITY",
        "SEMANTIC_LAYER_AMBIGUITY",
        "王云鹏",
        "LEGACY_WEB_NOTE",
    ):
        require(skill, needle, "SKILL.md")

    for needle in (
        "节气先到、旬首未到",
        "上元符头在节气前",
        "20点~23点为晚子时",
        "23-24点为晚子时算次日",
        "PALACE_NUMBER_ORDER",
        "chief_door_position_rule",
        "DEFINITION_OVERLAP_UNRESOLVED",
    ):
        require(reg, needle, "SETUP_METHOD_REGISTRY.md")

    for needle in (
        "### 2.4 拆补法（推荐使用）",
        "简单直观，应用最广",
        "严格遵古，但复杂",
        "（顺时针依次排列）",
        "（逆时针依次排列）",
        "**文献来源**：《奇门遁甲应用学》佚名·第三章",
    ):
        forbid(skill, needle, "SKILL.md")

    print("qimen-qiju-runtime-contract: PASS")


if __name__ == "__main__":
    main()
