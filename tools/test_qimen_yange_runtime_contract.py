#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "奇门" / "qclaw" / "qimen-yange" / "SKILL.md"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-yange-runtime-contract: FAIL: {msg}")


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    required = (
        "Provenance Registry",
        "PRIMARY_TEXT",
        "MODERN_PARAPHRASE",
        "TEACHING_MNEMONIC",
        "PAGE_VERIFIED",
        "LEGACY_ATTRIBUTION",
        "ATTRIBUTION_UNRESOLVED",
        "SOURCE_INCONSISTENCY",
        "CROSS_SOURCE_VARIANT",
        "CROSS_SOURCE_PATTERN_LINEAGE_REQUIRED",
        "qimen-qiju",
        "qimen-gexia",
        "Empirical Support",
    )
    for needle in required:
        if needle not in text:
            fail(f"missing {needle!r}")

    forbidden = (
        "吉凶 | 主要含义",
        "★★★★★",
        "灾祸必至",
        "百事大吉",
        "核心经典歌诀",
    )
    for needle in forbidden:
        if needle in text:
            fail(f"legacy provenance/determinism remains active: {needle!r}")

    print("qimen-yange-runtime-contract: PASS")


if __name__ == "__main__":
    main()
