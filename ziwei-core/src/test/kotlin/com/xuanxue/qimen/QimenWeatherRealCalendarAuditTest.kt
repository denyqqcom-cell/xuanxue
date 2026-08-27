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
 * - the fixed 2000-01-01..2099-12-31 window is a calendar-structure coverage
 *   window, NOT a weather sample and NOT a stopping rule for a future Batch.
 */
class QimenWeatherRealCalendarAuditTest {

    private data class SignalHit(val palace: Int, val star: String, val heavenStem: String)

    private fun carriedHeavenStems(c: QimenEngine.QimenChart): Map<Int, String> {
        val ring = QimenEngine.RING.toList()
        val di = c.gongs.associate { it.palace to it.diGan }

        val rawDunPalace = di.entries.first { it.value == c.dunGan }.key
        val effectiveDunPalace = if (rawDunPalace == 5) 2 else rawDunPalace

        val effectiveHourGan = if (c.hourGZ[0] == '甲') c.dunGan else c.hourGZ[0].toString()
        val rawHourGanPalace = di.entries.first { it.value == effectiveHourGan }.key
        val zhiFuPalace = if (rawHourGanPalace == 5) 2 else rawHourGanPalace

        val baseIdx = ring.indexOf(effectiveDunPalace)
        require(baseIdx >= 0) { "effective dun palace must be on outer ring: $effectiveDunPalace" }

        val sourceOrder = (0 until 8).map { k ->
            if (c.yinYang > 0) ring[(baseIdx + k) % 8]
            else ring[((baseIdx - k) % 8 + 8) % 8]
        }

        val shift = (ring.indexOf(zhiFuPalace) - ring.indexOf(effectiveDunPalace) + 8) % 8
        val result = mutableMapOf<Int, String>()
        for (sourcePalace in sourceOrder) {
            val yi = di[sourcePalace].orEmpty()
            val srcIdx = ring.indexOf(sourcePalace)
            val targetPalace = if (c.yinYang > 0) {
                ring[(srcIdx + shift) % 8]
            } else {
                ring[((srcIdx - shift) % 8 + 8) % 8]
            }
            result[targetPalace] = yi
        }
        return result
    }

    private fun coreRainSignal(c: QimenEngine.QimenChart): List<SignalHit> {
        val heavenStems = carriedHeavenStems(c)
        val targetPalaces = setOf(1, 3, 6, 7)
        return c.gongs.mapNotNull { gong ->
            val stem = heavenStems[gong.palace].orEmpty()
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

        val reportDir = File("build/reports")
        reportDir.mkdirs()
        val report = File(reportDir, "qimen-weather-real-calendar-audit-v01.json")
        val triggerRate = triggerDays.toDouble() / totalDays.toDouble()

        report.writeText(
            buildString {
                append("{\n")
                append("  \"audit_scope\": \"REAL_CIVIL_CALENDAR_STRUCTURE_ONLY\",\n")
                append("  \"calendar_window\": \"2000-01-01/2099-12-31\",\n")
                append("  \"civil_time_hkt\": \"17:00\",\n")
                append("  \"qimen_ju_method\": \"CHAI_BU_FUTOU\",\n")
                append("  \"qimen_engine_blob_sha\": \"1912760ccd10cb4a58eb8faec06669c0d690657b\",\n")
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
