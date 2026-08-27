#!/usr/bin/env python3
"""Abstract plate-state audit for CDAF-H2 CORE_RAIN_SIGNAL_V01.

This test deliberately uses no weather forecast and no weather outcome data.
It mirrors only the weather-relevant plate transitions of the exact pinned
QimenEngine blob.

Important: 24 terms × 3 named yuans × 5 fixed-酉 hour states is a Cartesian
state-space audit. It is NOT a civil-date frequency model for拆补符头. The
source method may use 残上→中→下→补上 around solar-term boundaries, so real
calendar weighting must be audited separately before sample-duration design.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt"
EXPECTED_ENGINE_GIT_BLOB_SHA = "1912760ccd10cb4a58eb8faec06669c0d690657b"

RING = [1, 8, 3, 4, 9, 2, 7, 6]
STAR_HOME = {
    1: "天蓬", 2: "天芮", 3: "天冲", 4: "天辅", 5: "天禽",
    6: "天心", 7: "天柱", 8: "天任", 9: "天英",
}
YI = "戊己庚辛壬癸丁丙乙"
GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
XUN_DUN = {
    "甲子": "戊", "甲戌": "己", "甲申": "庚",
    "甲午": "辛", "甲辰": "壬", "甲寅": "癸",
}
JIE_QI_JU = {
    "冬至": (1, 1, 7, 4), "小寒": (1, 2, 8, 5), "大寒": (1, 3, 9, 6),
    "立春": (1, 8, 5, 2), "雨水": (1, 9, 6, 3), "惊蛰": (1, 1, 7, 4),
    "春分": (1, 3, 9, 6), "清明": (1, 4, 1, 7), "谷雨": (1, 5, 2, 8),
    "立夏": (1, 4, 1, 7), "小满": (1, 5, 2, 8), "芒种": (1, 6, 3, 9),
    "夏至": (-1, 9, 3, 6), "小暑": (-1, 8, 2, 5), "大暑": (-1, 7, 1, 4),
    "立秋": (-1, 2, 5, 8), "处暑": (-1, 1, 4, 7), "白露": (-1, 9, 3, 6),
    "秋分": (-1, 7, 1, 4), "寒露": (-1, 6, 9, 3), "霜降": (-1, 5, 8, 2),
    "立冬": (-1, 6, 9, 3), "小雪": (-1, 5, 8, 2), "大雪": (-1, 4, 7, 1),
}

# At a fixed 酉时 there are five possible hour-stem states across day-stem
# classes. These are used as nominal plate inputs, not as a claim that every
# solar term contains each named yuan for exactly five civil days.
HOUR_STATES_17_HKT = ["癸酉", "乙酉", "丁酉", "己酉", "辛酉"]
TARGET_PALACES = {1, 3, 6, 7}

EXPECTED_PER_JIEQI_TRIGGERS = {
    "冬至": 0, "小寒": 2, "大寒": 5, "立春": 2, "雨水": 5, "惊蛰": 0,
    "春分": 5, "清明": 0, "谷雨": 2, "立夏": 0, "小满": 2, "芒种": 5,
    "夏至": 4, "小暑": 2, "大暑": 3, "立秋": 2, "处暑": 3, "白露": 4,
    "秋分": 3, "寒露": 4, "霜降": 2, "立冬": 4, "小雪": 2, "大雪": 3,
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def seq_of(gan: str, zhi: str) -> int:
    g = GAN.index(gan)
    z = ZHI.index(zhi)
    for i in range(60):
        if i % 10 == g and i % 12 == z:
            return i
    raise AssertionError(f"invalid sexagenary pair: {gan}{zhi}")


def xun_info(gz: str) -> tuple[str, str]:
    s = seq_of(gz[0], gz[1])
    base = (s // 10) * 10
    xun_shou = GAN[base % 10] + ZHI[base % 12]
    return xun_shou, XUN_DUN[xun_shou]


def implementation_state(yin_yang: int, ju: int, hour_gz: str) -> dict:
    # Exact weather-relevant mirror of QimenEngine.kt at the pinned blob.
    luo_shu = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    di: dict[int, str] = {}
    idx = luo_shu.index(ju)
    for k, yi in enumerate(YI):
        pos = (
            luo_shu[(idx + k) % 9]
            if yin_yang > 0
            else luo_shu[(idx - k) % 9]
        )
        di[pos] = yi

    _, dun_gan = xun_info(hour_gz)
    dun_palace = next(p for p, value in di.items() if value == dun_gan)
    hour_gan_or_dun = dun_gan if hour_gz[0] == "甲" else hour_gz[0]
    hour_gan_palace = next(p for p, value in di.items() if value == hour_gan_or_dun)
    zhi_fu_palace = 2 if hour_gan_palace == 5 else hour_gan_palace

    stars_on_ring = [STAR_HOME[p] for p in RING]
    tian: dict[int, str] = {}
    if dun_palace == 5:
        rui_idx = RING.index(2)
        fu_idx = RING.index(zhi_fu_palace)
        shift = (fu_idx - rui_idx + 8) % 8
        for source_idx in range(8):
            tian[RING[(source_idx + shift) % 8]] = stars_on_ring[source_idx]
        rui_new = next(p for p, value in tian.items() if value == "天芮")
        tian[rui_new] = "天禽天芮"
    else:
        src_idx = RING.index(dun_palace)
        fu_idx = RING.index(zhi_fu_palace)
        shift = (fu_idx - src_idx + 8) % 8
        for source_idx in range(8):
            tian[RING[(source_idx + shift) % 8]] = stars_on_ring[source_idx]
        rui_new = next(p for p, value in tian.items() if value == "天芮")
        tian[rui_new] = "天芮天禽"

    tian_yi: dict[int, str] = {}
    effective_dun_palace = dun_palace if dun_palace != 5 else 2
    base_idx = RING.index(effective_dun_palace)
    di_yi_order = [
        RING[(base_idx + k) % 8] if yin_yang > 0 else RING[(base_idx - k) % 8]
        for k in range(8)
    ]
    shift_ring = (RING.index(zhi_fu_palace) - RING.index(effective_dun_palace)) % 8
    for src_p in di_yi_order:
        yi = di.get(src_p, "")
        src_idx = RING.index(src_p)
        dst_p = (
            RING[(src_idx + shift_ring) % 8]
            if yin_yang > 0
            else RING[(src_idx - shift_ring) % 8]
        )
        tian_yi[dst_p] = yi

    return {"tian": tian, "tian_yi": tian_yi}


def core_rain_signal_v01(state: dict) -> list[tuple[int, str, str]]:
    hits = []
    for palace, star in state["tian"].items():
        carried_stem = state["tian_yi"].get(palace, "")
        if (
            ("天柱" in star or "天蓬" in star)
            and carried_stem in {"壬", "癸"}
            and palace in TARGET_PALACES
        ):
            hits.append((palace, star, carried_stem))
    return hits


def main() -> None:
    actual_blob = git_blob_sha(ENGINE_PATH)
    assert actual_blob == EXPECTED_ENGINE_GIT_BLOB_SHA, (
        "QimenEngine blob changed; abstract weather plate-state audit must be reviewed: "
        f"expected={EXPECTED_ENGINE_GIT_BLOB_SHA} actual={actual_blob}"
    )

    total_states = 0
    trigger_states = 0
    per_jieqi = Counter()
    hit_cardinality = Counter()

    for jieqi, (yin_yang, shang, zhong, xia) in JIE_QI_JU.items():
        for ju in (shang, zhong, xia):
            for hour_gz in HOUR_STATES_17_HKT:
                total_states += 1
                hits = core_rain_signal_v01(implementation_state(yin_yang, ju, hour_gz))
                if hits:
                    trigger_states += 1
                    per_jieqi[jieqi] += 1
                    hit_cardinality[len(hits)] += 1

    assert total_states == 24 * 3 * 5 == 360
    assert trigger_states == 64
    assert dict(per_jieqi) == {
        k: v for k, v in EXPECTED_PER_JIEQI_TRIGGERS.items() if v > 0
    }
    assert hit_cardinality == Counter({1: 64})

    result = {
        "audit_scope": "ABSTRACT_PLATE_STATE_SPACE_ONLY",
        "civil_date_frequency_claimed": False,
        "weather_forecast_data_used": False,
        "weather_outcome_data_used": False,
        "engine_git_blob_sha": actual_blob,
        "abstract_contract_states": total_states,
        "core_rain_signal_trigger_states": trigger_states,
        "state_space_density": trigger_states / total_states,
        "per_jieqi_triggers_out_of_15_nominal_states": EXPECTED_PER_JIEQI_TRIGGERS,
        "sample_duration_usable": False,
        "empirical_credit": "NONE",
    }
    print("K2_QIMEN_WEATHER_STRUCTURE_AUDIT=" + json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
