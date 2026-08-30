package com.xuanxue.qimen

import java.io.File
import java.time.LocalDate
import java.time.temporal.ChronoUnit
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/**
 * Structure-only civil-calendar audit for CDAF-H2 CORE_RAIN_SIGNAL_V01.
 *
 * IMPORTANT:
 * - reads no HKO forecast data;
 * - reads no rainfall/outcome data;
 * - grants no predictive or empirical credit;
 * - uses the real QimenEngine with CHAI_BU_FUTOU at 17:00 HKT civil time;
 * - reads the Engine's first-class Gong.tianGan instead of reconstructing a
 *   second carried-heaven-stem algorithm inside the audit;
 * - the fixed 2000-01-01..2099-12-31 window is a calendar-structure coverage
 *   window, NOT a weather sample and NOT a stopping rule for a future Batch.
 *
 * V03 repin note: the Engine change is a source-grounded 值使门 center-count
 * correction outside CORE_RAIN_SIGNAL_V01. The exact V02 weather-relevant
 * structural totals below are retained as comparator assertions so a future
 * whole-engine change cannot silently inherit V02 evidence by assumption.
 */
class QimenWeatherRealCalendarAuditTest {

    private data class SignalHit(val palace: Int, val star: String, val heavenStem: String)

    private fun coreRainSignal(c: QimenEngine.QimenChart): List<SignalHit> {
        val targetPalaces = setOf(1, 3, 6, 7)
        return c.gongs.mapNotNull { gong ->
            val stem = gong.tianGan
            val isRainStar = gong.tianXing.contains("天柱") || gong.tianXing.contains("天蓬")
            if (isRainStar && stem in setOf("壬", "癸") && gong.palace in targetPalaces) {
                SignalHit(gong.palace, gong.tianXing, stem)
            } else {
                null
            }
        }
    }

    private fun jsonEscape(value: String): String = buildString {
        value.forEach { ch ->
            when (ch) {
                '\\' -> append("\\\\")
                '"' -> append("\\\"")
                '\n' -> append("\\n")
                '\r' -> append("\\r")
                '\t' -> append("\\t")
                else -> append(ch)
            }
        }
    }

    private fun stringIntMapJson(map: Map<String, Int>): String =
        map.toSortedMap().entries.joinToString(prefix = "{", postfix = "}") { (key, value) ->
            "\"${jsonEscape(key)}\":$value"
        }

    private fun intIntMapJson(map: Map<Int, Int>): String =
        map.toSortedMap().entries.joinToString(prefix = "{", postfix = "}") { (key, value) ->
            "\"$key\":$value"
        }

    @Test
    fun realCivilCalendarFutouSignalStructureAudit() {
        val start = LocalDate.of(2000, 1, 1)
        val end = LocalDate.of(2099, 12, 31)
        val expectedDays = ChronoUnit.DAYS.between(start, end) + 1
        assertEquals(36_525L, expectedDays)

        var date = start
        var totalDays = 0
        var triggerDays = 0
        var maxHitsInOneDay = 0
        var currentTriggerRun = 0
        var maxTriggerRun = 0
        var lastTriggerDate: LocalDate? = null
        var maxNonTriggerGap = 0L

        val daysByJieqi = linkedMapOf<String, Int>()
        val triggersByJieqi = linkedMapOf<String, Int>()
        val daysByYuan = linkedMapOf<String, Int>()
        val triggersByYuan = linkedMapOf<String, Int>()
        val triggersByYear = linkedMapOf<Int, Int>()
        val hitCardinality = linkedMapOf<Int, Int>()
        val juDayCounts = linkedMapOf<String, Int>()
        val juTriggerCounts = linkedMapOf<String, Int>()

        while (!date.isAfter(end)) {
            val c = QimenEngine.bySolar(
                date.year,
                date.monthValue,
                date.dayOfMonth,
                17,
                0,
                QimenEngine.JuMethod.CHAI_BU_FUTOU,
            )
            assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)
            assertEquals('酉', c.hourGZ[1], "17:00 HKT civil time must remain 酉时 at $date")

            val hits = coreRainSignal(c)
            val triggered = hits.isNotEmpty()
            val juKey = "${if (c.yinYang > 0) "YANG" else "YIN"}-${c.ju}"

            totalDays += 1
            daysByJieqi[c.jieQi] = daysByJieqi.getOrDefault(c.jieQi, 0) + 1
            daysByYuan[c.yuan] = daysByYuan.getOrDefault(c.yuan, 0) + 1
            juDayCounts[juKey] = juDayCounts.getOrDefault(juKey, 0) + 1
            hitCardinality[hits.size] = hitCardinality.getOrDefault(hits.size, 0) + 1
            maxHitsInOneDay = maxOf(maxHitsInOneDay, hits.size)

            if (triggered) {
                triggerDays += 1
                triggersByJieqi[c.jieQi] = triggersByJieqi.getOrDefault(c.jieQi, 0) + 1
                triggersByYuan[c.yuan] = triggersByYuan.getOrDefault(c.yuan, 0) + 1
                triggersByYear[date.year] = triggersByYear.getOrDefault(date.year, 0) + 1
                juTriggerCounts[juKey] = juTriggerCounts.getOrDefault(juKey, 0) + 1
                currentTriggerRun += 1
                maxTriggerRun = maxOf(maxTriggerRun, currentTriggerRun)

                lastTriggerDate?.let { previous ->
                    val gap = ChronoUnit.DAYS.between(previous, date) - 1
                    maxNonTriggerGap = maxOf(maxNonTriggerGap, gap)
                }
                lastTriggerDate = date
            } else {
                currentTriggerRun = 0
            }

            date = date.plusDays(1)
        }

        assertEquals(expectedDays.toInt(), totalDays)
        assertEquals(24, daysByJieqi.size, "all 24 solar terms must appear in a 100-year audit")
        assertEquals(setOf("上元", "中元", "下元"), daysByYuan.keys)
        assertTrue(triggerDays > 0, "CORE_RAIN_SIGNAL_V01 should not be structurally impossible")
        assertTrue(triggerDays < totalDays, "CORE_RAIN_SIGNAL_V01 must not be structurally tautological")
        assertEquals(totalDays, hitCardinality.values.sum())

        // Exact V02 -> V03 weather-relevant comparator. These assertions are
        // source/outcome blind: they compare deterministic calendar structure only.
        assertEquals(6_498, triggerDays)
        assertEquals(4, maxTriggerRun)
        assertEquals(33L, maxNonTriggerGap)
        assertEquals(1, maxHitsInOneDay)
        assertEquals(mapOf("上元" to 12_175, "中元" to 12_175, "下元" to 12_175), daysByYuan)
        assertEquals(mapOf("上元" to 1_813, "中元" to 1_850, "下元" to 2_835), triggersByYuan)
        assertEquals(
            mapOf(
                "处暑" to 309, "夏至" to 420, "大寒" to 492, "大暑" to 313, "大雪" to 296,
                "寒露" to 403, "小寒" to 196, "小暑" to 210, "小满" to 208, "小雪" to 197,
                "春分" to 507, "白露" to 412, "秋分" to 306, "立冬" to 398, "立春" to 198,
                "立秋" to 208, "芒种" to 522, "谷雨" to 206, "雨水" to 497, "霜降" to 200,
            ),
            triggersByJieqi,
        )
        assertEquals(
            mapOf(
                "YANG-2" to 808, "YANG-3" to 403, "YANG-6" to 1_615,
                "YIN-2" to 408, "YIN-3" to 816, "YIN-4" to 1_224,
                "YIN-5" to 407, "YIN-6" to 817,
            ),
            juTriggerCounts,
        )

        val reportDir = File("build/reports")
        reportDir.mkdirs()
        val report = File(reportDir, "qimen-weather-real-calendar-audit-v03.json")
        val triggerRate = triggerDays.toDouble() / totalDays.toDouble()

        report.writeText(
            buildString {
                append("{\n")
                append("  \"audit_scope\": \"REAL_CIVIL_CALENDAR_STRUCTURE_ONLY\",\n")
                append("  \"audit_version\": \"V03_ENGINE_REPIN_ZHISHI_CENTER_COUNT_FIX\",\n")
                append("  \"calendar_window\": \"2000-01-01/2099-12-31\",\n")
                append("  \"civil_time_hkt\": \"17:00\",\n")
                append("  \"qimen_ju_method\": \"CHAI_BU_FUTOU\",\n")
                append("  \"qimen_engine_blob_sha\": \"3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd\",\n")
                append("  \"v02_weather_relevant_structure_equivalent\": true,\n")
                append("  \"weather_forecast_data_used\": false,\n")
                append("  \"weather_outcome_data_used\": false,\n")
                append("  \"total_civil_days\": $totalDays,\n")
                append("  \"core_signal_days\": $triggerDays,\n")
                append("  \"civil_date_trigger_rate\": $triggerRate,\n")
                append("  \"max_consecutive_trigger_days\": $maxTriggerRun,\n")
                append("  \"max_non_trigger_gap_days\": $maxNonTriggerGap,\n")
                append("  \"max_hits_in_one_day\": $maxHitsInOneDay,\n")
                append("  \"days_by_jieqi\": ${stringIntMapJson(daysByJieqi)},\n")
                append("  \"triggers_by_jieqi\": ${stringIntMapJson(triggersByJieqi)},\n")
                append("  \"days_by_yuan\": ${stringIntMapJson(daysByYuan)},\n")
                append("  \"triggers_by_yuan\": ${stringIntMapJson(triggersByYuan)},\n")
                append("  \"triggers_by_year\": ${intIntMapJson(triggersByYear)},\n")
                append("  \"hit_cardinality\": ${intIntMapJson(hitCardinality)},\n")
                append("  \"ju_day_counts\": ${stringIntMapJson(juDayCounts)},\n")
                append("  \"ju_trigger_counts\": ${stringIntMapJson(juTriggerCounts)},\n")
                append("  \"sample_duration_usable\": false,\n")
                append("  \"empirical_credit\": \"NONE\"\n")
                append("}\n")
            },
            Charsets.UTF_8,
        )

        assertTrue(report.isFile && report.length() > 0L)
    }
}
