#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "奇门" / "qclaw" / "qimen-gongpan" / "SKILL.md"
AUDIT = ROOT / "奇门" / "qclaw" / "qimen-gongpan" / "SOURCE_LAYER_AUDIT.md"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-gongpan-runtime-contract: FAIL: {msg}")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"missing {needle!r} in {where}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        fail(f"legacy deterministic rule still active: {needle!r} in {where}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    for needle in (
        "STRUCTURAL_METADATA",
        "SOURCE_SYMBOLISM",
        "STATE_FEATURE",
        "ROLE_BINDING",
        "RELATION",
        "CONTEXTUAL_INFERENCE",
        "STAR_STATE_SYSTEM_REQUIRED",
        "deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER",
        "METHOD-FAMILY-SPECIFIC FEATURE ORDER",
        "HIGH_RISK_SOURCE_SYMBOLISM",
        "POST_FEEDBACK_FACTOR_SWITCH",
        "王云鹏",
    ):
        require(skill, needle, "SKILL.md")

    for needle in (
        "旺于亥子， 相于寅卯",
        "旺于寅卯， 相于亥子",
        "SOURCE_INCONSISTENCY / STAR_STATE_SYSTEM_REQUIRED",
        "CONTEXT_SPLIT_REQUIRED",
        "DEPRECATED_AS_GLOBAL_RULE",
        "DEPRECATED_AS_GLOBAL_PRIORITY",
        "SOURCE_ONLY / NON_MEDICAL_EVIDENCE",
        "METHOD_SPECIFIC_SOURCE",
        "PROVENANCE_CORRECTED",
    ):
        require(audit, needle, "SOURCE_LAYER_AUDIT.md")

    # Forbid old rules only in their former active forms. Historical migration notes are allowed to name them.
    for needle in (
        "**核心原则**：星+门+神+卦+格局五位一体",
        "| 吉星+吉门+吉神 | 大吉 |",
        "| 凶星+凶门 | 大凶 |",
        "| 旺 | 最强 | 吉星旺则大吉，凶星旺则大凶 |",
        "1. 时干生日干→风水无害，即使星门神格局不好",
        "2. 时干克日干→风水不利，即使星门神格局再好",
        "> **文献来源**：《奇门遁甲应用学》佚名",
    ):
        forbid(skill, needle, "SKILL.md")

    # The runtime must explicitly refuse a universal star-state algorithm while the legacy source is inconsistent.
    require(skill, "star_state_system = SOURCE_DEFINED / CONTEXT_REQUIRED", "SKILL.md")

    print("qimen-gongpan-runtime-contract: PASS")


if __name__ == "__main__":
    main()
