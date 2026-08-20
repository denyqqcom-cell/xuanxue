#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "奇门" / "qclaw" / "qimen-gexia" / "SKILL.md"
REGISTRY = ROOT / "奇门" / "qclaw" / "qimen-gexia" / "PATTERN_REGISTRY.md"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-gexia-runtime-contract: FAIL: {msg}")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"missing {needle!r} in {where}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        fail(f"legacy deterministic rule still active: {needle!r} in {where}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")

    for needle in (
        "Pattern Registry",
        "PATTERN_TYPE",
        "STRUCTURE",
        "SOURCE_PROVENANCE",
        "APPLICABILITY",
        "EMPIRICAL_SUPPORT",
        "OPERATIONAL_STATUS",
        "ORDERED_PAIR = (HEAVEN_STEM, EARTH_STEM)",
        "Source Fidelity",
        "CONFLICT_CANDIDATE",
        "DEFINITION_UNRESOLVED",
        "POST_FEEDBACK_FACTOR_SWITCH",
    ):
        require(skill, needle, "SKILL.md")

    for needle in (
        "朱雀投江",
        "丁+丙临坤、离",
        "丁+癸",
        "小格",
        "庚+壬 = 小格",
        "庚+己 = 小格",
        "三奇会聚",
        "三吉门会聚",
        "STRUCTURAL_CONFLICT",
        "王云鹏",
        "LEGACY_SOURCE_NOTE",
    ):
        require(registry, needle, "PATTERN_REGISTRY.md")

    for needle in (
        "核心原则**：格局是判断吉凶程度的精细化工具",
        "≥3分即不可轻视",
        "凶格叠加是相乘不是相加",
        "**≥3分** | **直接大凶**",
        "**≥5分** | **极凶**",
        "《奇门遁甲应用学》佚名·第四章·第五节",
    ):
        forbid(skill, needle, "SKILL.md")

    # Guard against collapsing ordered pairs back into directionless semantics.
    require(skill, "`戊加丙` 与 `丙加戊` 不是同一结构", "SKILL.md")

    # Guard the structural impossibility / unresolved-definition findings.
    require(skill, "三吉门会聚同宫", "SKILL.md")
    require(skill, "DEFINITION_UNRESOLVED / STRUCTURAL_CONFLICT", "SKILL.md")

    print("qimen-gexia-runtime-contract: PASS")


if __name__ == "__main__":
    main()
