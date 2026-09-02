#!/usr/bin/env python3
"""Source-grounded chart-only plate-pairing mirror fixture for QM-SRC-0021.

No weather forecast/outcome data are read. The source expected values are also
asserted directly against the Kotlin QimenEngine in QimenSourcePlateFixtureTest;
this Python test remains a pinned cross-language mirror/structure guard and must
not be used to create extra source provenance.
"""

from __future__ import annotations

from test_k2_qimen_weather_structure_audit import (
    ENGINE_PATH,
    EXPECTED_ENGINE_GIT_BLOB_SHA,
    git_blob_sha,
    implementation_state,
    seq_of,
)


def futou_yuan(day_gz: str) -> str:
    # Five-day 拆补符头: each yuan begins on a 甲 or 己 day.
    # Do not replace this with the ten-unit 六甲旬首 boundary.
    s = seq_of(day_gz[0], day_gz[1])
    base = s - (s % 5)
    gan = "甲乙丙丁戊己庚辛壬癸"
    zhi = "子丑寅卯辰巳午未申酉戌亥"
    ft = gan[base % 10] + zhi[base % 12]
    if ft in {"甲子", "甲午", "己卯", "己酉"}:
        return "上元"
    if ft in {"甲寅", "甲申", "己巳", "己亥"}:
        return "中元"
    return "下元"


def main() -> None:
    actual_blob = git_blob_sha(ENGINE_PATH)
    assert actual_blob == EXPECTED_ENGINE_GIT_BLOB_SHA, (
        "QimenEngine blob changed; source plate-pairing fixture must be reviewed: "
        f"expected={EXPECTED_ENGINE_GIT_BLOB_SHA} actual={actual_blob}"
    )

    # QM-SRC-0021 algorithm chapter: 2004-05-29 戊申日戊午时,
    # 小满, 符头法下元 -> 阳遁八局, 甲寅旬, 值符天辅.
    assert futou_yuan("戊申") == "下元"

    # Do not restore the old 2002-08-01 date/hour assertion here. That metadata
    # was withdrawn from golden-fixture credit and remains SOURCE_PAGE_REVERIFICATION_REQUIRED.
    state = implementation_state(1, 8, "戊午")

    expected_stars = {
        1: "天冲",
        2: "天心",
        3: "天英",
        4: "天芮天禽",
        6: "天任",
        7: "天蓬",
        8: "天辅",
        9: "天柱",
    }
    expected_heaven_stems = {
        1: "壬",
        2: "丙",
        3: "己",
        4: "辛",
        6: "戊",
        7: "庚",
        8: "癸",
        9: "乙",
    }

    assert state["tian"] == expected_stars
    assert state["tian_yi"] == expected_heaven_stems

    expected_pairs = {
        palace: (expected_stars[palace], expected_heaven_stems[palace])
        for palace in expected_stars
    }
    actual_pairs = {
        palace: (state["tian"][palace], state["tian_yi"][palace])
        for palace in state["tian"]
    }
    assert actual_pairs == expected_pairs

    print(
        "K2_QIMEN_PLATE_PAIRING_FIXTURE=PASS "
        "source=QM-SRC-0021 printed_pages=68-70 "
        "datetime=2004-05-29T12:00 method=CHAI_BU_FUTOU ju=YANG8 "
        f"engine_blob={actual_blob} empirical_credit=NONE"
    )


if __name__ == "__main__":
    main()
