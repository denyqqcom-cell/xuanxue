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
        "PAGE_VERIFIED_WITNESS_ATTRIBUTION",
        "LEGACY_ATTRIBUTION",
        "ATTRIBUTION_UNRESOLVED",
        "HISTORICAL_AUTHORSHIP_UNRESOLVED",
        "EDITION_UNRESOLVED",
        "SOURCE_INCONSISTENCY",
        "CROSS_SOURCE_VARIANT",
        "CROSS_SOURCE_PATTERN_LINEAGE_REQUIRED",
        "QM-SRC-0024",
        "qimen-qiju",
        "qimen-gexia",
        "Empirical Support",
        "星级 `★★★★★`：`PROJECT_GLOSS / NOT_OPERATIONAL`",
    )
    for needle in required:
        if needle not in text:
            fail(f"missing {needle!r}")

    # The p5 witness may upgrade the witness-level Zhao Pu attribution, but
    # must not silently turn the filename's bundled claim into verified
    # historical authorship or edition truth.
    if "赵普历史作者身份" not in text or "仍不可由这一页单独证明" not in text:
        fail("QM-SRC-0024 witness attribution must remain separate from historical authorship")
    if "“明刊本”版本判断" not in text or "EDITION_UNRESOLVED" not in text:
        fail("QM-SRC-0024 edition claim must remain unresolved until edition witness review")
    if "不等于 `QM-SRC-0024` 全书 Reading COMPLETE" not in text:
        fail("targeted provenance review must not be mistaken for full-book reading credit")

    # Historical debt must remain auditable. Literal legacy tokens may appear
    # only when explicitly downgraded; do not forbid the evidence of the bug.
    forbidden = (
        "| 歌诀 | 星名 | 五行 | 吉凶 | 主要含义 |",
        "灾祸必至",
        "百事大吉",
    )
    for needle in forbidden:
        if needle in text:
            fail(f"legacy provenance/determinism remains active: {needle!r}")

    print("qimen-yange-runtime-contract: PASS")


if __name__ == "__main__":
    main()
