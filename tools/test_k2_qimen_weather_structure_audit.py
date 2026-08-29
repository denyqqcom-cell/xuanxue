#!/usr/bin/env python3
"""Structure-only audits and batch-contract gate for CDAF-H2 weather v0.1.

This gate deliberately uses no weather forecast and no weather outcome data.
It has two responsibilities only:

1. preserve the abstract weather-relevant plate-state audit against the exact
   pinned QimenEngine blob; and
2. fail closed if the CDAF-H2 sample/serial design, prospective Plan, or any
   future CDAF-H2 Batch drifts away from the preregistered v0.1 contract.

Important: 24 terms × 3 named yuans × 5 fixed-酉 hour states is a Cartesian
state-space audit. It is NOT a civil-date frequency model for拆补符头. Real
calendar weighting and the +/-1 solar-term-segment shams are audited elsewhere.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt"
PLAN_PATH = ROOT / "knowledge/K2_PROSPECTIVE_TEST_PLANS.jsonl"
BATCH_PATH = ROOT / "knowledge/K2_PROSPECTIVE_BATCHES.jsonl"
SAMPLE_PLAN_PATH = ROOT / "knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md"
EXPECTED_ENGINE_GIT_BLOB_SHA = "89ce6d53eb80e195f8fd69071f6c6c02549596da"
CDAF_PLAN_ID = "K2PV-CDAF-H2"

# Machine tokens for a future CDAF-H2 Batch. These live at Batch level because
# they govern acquisition/stopping/inference for the whole series, not an
# individual case frozen_payload.
EXPECTED_COMPARATOR_REF = "K2PV-CDAF-H2:M1+SHAM_PLUS_1+SHAM_MINUS_1:V01"
EXPECTED_SAMPLING_RULE = (
    "CDAF_H2_SAMPLING_V01|START=SOLAR_TERM_SEGMENT_BOUNDARY|MIN_SEGMENTS=48|"
    "EXTEND_IF_ANY_PREOUTCOME_INFO_LT_80=PLUS_24_SEGMENTS|MAX_SEGMENTS=72|"
    "OUTCOME_QUARANTINED=true"
)
EXPECTED_PRIMARY_METRIC = (
    "CDAF_H2_PRIMARY_V01|DELTA_M1=MEAN_D_M1|DELTA_PLUS=MEAN_D_PLUS|"
    "DELTA_MINUS=MEAN_D_MINUS|HAC=BARTLETT|CALENDAR_LAG_DAYS=30"
)
EXPECTED_DECISION_RULE = (
    "CDAF_H2_DECISION_V01|FWER_ALPHA=0.05|PRIMARY_CONTRASTS=3|"
    "BONFERRONI_ONE_SIDED=true|Z_CRITICAL=2.1280452342|"
    "REQUIRE_ALL_HAC_LOWER_BOUNDS_GT_0=true"
)
EXPECTED_STOPPING_RULE = (
    "CDAF_H2_STOP_V01|CHECK_AT_SEGMENT=48|IF_ANY_PREOUTCOME_INFO_LT_80=EXTEND_TO_72|"
    "CLOSE_AT_SEGMENT=72|NO_OUTCOME_PEEKING=true|NO_REOPEN_AFTER_OUTCOME_QC=true"
)
EXPECTED_EXCLUSION_RULE = (
    "CDAF_H2_EXCLUSION_V01|PREOUTCOME_ONLY=true|PSR_MEDIUM=INELIGIBLE|"
    "MISSING_1630_SNAPSHOT=INELIGIBLE|OUTCOME_DATA_QC_FAILURE=UNEVALUABLE_NOT_EXCLUDED"
)
EXPECTED_DUPLICATE_POLICY = "CDAF_H2_DUPLICATE_V01|TARGET_DATE_HKT_UNIQUE_WITHIN_BATCH=true"
EXPECTED_SECONDARY_METRICS = [
    "PREOUTCOME_INFO_COUNTS_V01",
    "EVALUABLE_INFO_COUNTS_V01",
    "UNIQUE_CORRECTION_DEGRADATION_V01",
    "UNEVALUABLE_RATE_V01",
    "PER_JIEQI_PAIRED_DELTA_V01",
]

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
# classes. These are nominal plate inputs, not a civil-calendar weighting model.
HOUR_STATES_17_HKT = ["癸酉", "乙酉", "丁酉", "己酉", "辛酉"]
TARGET_PALACES = {1, 3, 6, 7}

EXPECTED_PER_JIEQI_TRIGGERS = {
    "冬至": 0, "小寒": 2, "大寒": 5, "立春": 2, "雨水": 5, "惊蛰": 0,
    "春分": 5, "清明": 0, "谷雨": 2, "立夏": 0, "小满": 2, "芒种": 5,
    "夏至": 4, "小暑": 2, "大暑": 3, "立秋": 2, "处暑": 3, "白露": 4,
    "秋分": 3, "寒露": 4, "霜降": 2, "立冬": 4, "小雪": 2, "大雪": 3,
}

SAMPLE_PLAN_REQUIRED_MARKERS = [
    "MIN_PREOUTCOME_INFO_PER_CONTRAST = 80",
    "48 个完整连续 solar-term segments",
    "MAX_SEGMENTS = 72",
    "HAC_KERNEL   = Bartlett",
    "HAC_MAX_LAG  = 30 civil days",
    "FWER_ALPHA = 0.05",
    "NUMBER_OF_PRIMARY_CONTRASTS = 3",
    "Z_CRITICAL = 2.1280452342",
    "INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC",
]
PLAN_REQUIRED_MARKERS = [
    "K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md v0.1",
    "48",
    "72",
    "80",
    "HAC_MAX_LAG=30",
    "2.1280452342",
    "Outcome",
]
PER_CASE_REQUIRED_FIELDS = {
    "solar_term_segment_id",
    "calendar_sham_plus_1_signal",
    "calendar_sham_minus_1_signal",
    "calendar_sham_schedule_ref",
    "calendar_sham_schedule_hash",
    "qimen_ju_method",
    "qimen_engine_blob_sha",
}
BATCH_ONLY_FIELDS = {
    "sampling_rule",
    "stopping_rule",
    "planned_case_count",
    "primary_metric",
    "decision_rule",
    "HAC_MAX_LAG",
    "MIN_PREOUTCOME_INFO_PER_CONTRAST",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        assert isinstance(value, dict), f"{path}:{line_no} must be an object"
        rows.append(value)
    return rows


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


def cdaf_h2_batch_contract_issues(batch: dict) -> list[str]:
    issues = []
    expected = {
        "comparator_ref": EXPECTED_COMPARATOR_REF,
        "sampling_rule": EXPECTED_SAMPLING_RULE,
        "primary_metric": EXPECTED_PRIMARY_METRIC,
        "decision_rule": EXPECTED_DECISION_RULE,
        "stopping_rule": EXPECTED_STOPPING_RULE,
        "exclusion_rule": EXPECTED_EXCLUSION_RULE,
        "duplicate_case_policy": EXPECTED_DUPLICATE_POLICY,
    }
    if batch.get("planned_case_count") is not None:
        issues.append("planned_case_count must be null because stopping is segment/information based")
    for field, value in expected.items():
        if batch.get(field) != value:
            issues.append(f"{field} does not match CDAF-H2 v0.1 machine contract")
    if batch.get("secondary_metrics") != EXPECTED_SECONDARY_METRICS:
        issues.append("secondary_metrics do not match CDAF-H2 v0.1 machine contract")
    return issues


def synthetic_valid_cdaf_batch() -> dict:
    return {
        "planned_case_count": None,
        "comparator_ref": EXPECTED_COMPARATOR_REF,
        "sampling_rule": EXPECTED_SAMPLING_RULE,
        "primary_metric": EXPECTED_PRIMARY_METRIC,
        "decision_rule": EXPECTED_DECISION_RULE,
        "secondary_metrics": EXPECTED_SECONDARY_METRICS.copy(),
        "stopping_rule": EXPECTED_STOPPING_RULE,
        "exclusion_rule": EXPECTED_EXCLUSION_RULE,
        "duplicate_case_policy": EXPECTED_DUPLICATE_POLICY,
    }


def exercise_batch_contract_negative_cases() -> None:
    good = synthetic_valid_cdaf_batch()
    assert not cdaf_h2_batch_contract_issues(good)

    mutations = [
        ("planned_case_count", 80),
        ("sampling_rule", "run until enough information"),
        ("primary_metric", "ordinary independent Bernoulli accuracy"),
        ("decision_rule", "pick the best of three contrasts"),
        ("stopping_rule", "stop when p<0.05"),
        ("exclusion_rule", "drop outcome-missing dates before scoring"),
        ("duplicate_case_policy", "allow repeated target dates"),
        ("secondary_metrics", ["ONLY_SUCCESSFUL_DAYS"]),
    ]
    for field, bad_value in mutations:
        bad = copy.deepcopy(good)
        bad[field] = bad_value
        issues = cdaf_h2_batch_contract_issues(bad)
        assert issues, f"mutation must fail closed: {field}"


def validate_sample_and_prospective_contracts() -> int:
    sample_text = SAMPLE_PLAN_PATH.read_text(encoding="utf-8")
    for marker in SAMPLE_PLAN_REQUIRED_MARKERS:
        assert marker in sample_text, f"sample plan missing frozen marker: {marker}"

    plans = load_jsonl(PLAN_PATH)
    matches = [p for p in plans if p.get("plan_id") == CDAF_PLAN_ID]
    assert len(matches) == 1, f"expected exactly one {CDAF_PLAN_ID} plan, got {len(matches)}"
    plan = matches[0]
    plan_text = json.dumps(plan, ensure_ascii=False, sort_keys=True)
    for marker in PLAN_REQUIRED_MARKERS:
        assert marker in plan_text, f"prospective plan missing Gate-D marker: {marker}"

    freeze_fields = set(plan.get("freeze_required_fields") or [])
    missing_case_fields = PER_CASE_REQUIRED_FIELDS - freeze_fields
    assert not missing_case_fields, f"CDAF-H2 case freeze missing fields: {sorted(missing_case_fields)}"
    leaked_batch_fields = BATCH_ONLY_FIELDS & freeze_fields
    assert not leaked_batch_fields, (
        "batch-level sample/statistical rules must not be copied into each case frozen_payload: "
        f"{sorted(leaked_batch_fields)}"
    )

    exercise_batch_contract_negative_cases()

    batches = [b for b in load_jsonl(BATCH_PATH) if b.get("plan_id") == CDAF_PLAN_ID]
    for batch in batches:
        issues = cdaf_h2_batch_contract_issues(batch)
        assert not issues, f"CDAF-H2 Batch contract drift: {issues[0]}"
    return len(batches)


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

    cdaf_batch_count = validate_sample_and_prospective_contracts()

    result = {
        "audit_scope": "ABSTRACT_PLATE_STATE_SPACE_PLUS_PREBATCH_CONTRACT",
        "civil_date_frequency_claimed": False,
        "weather_forecast_data_used": False,
        "weather_outcome_data_used": False,
        "engine_git_blob_sha": actual_blob,
        "abstract_contract_states": total_states,
        "core_rain_signal_trigger_states": trigger_states,
        "state_space_density": trigger_states / total_states,
        "per_jieqi_triggers_out_of_15_nominal_states": EXPECTED_PER_JIEQI_TRIGGERS,
        "sample_duration_usable": False,
        "sample_gate_contract_ready": True,
        "cdaf_h2_batches_present": cdaf_batch_count,
        "batch_created_by_this_gate": False,
        "empirical_credit": "NONE",
    }
    print("K2_QIMEN_WEATHER_STRUCTURE_AUDIT=" + json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
