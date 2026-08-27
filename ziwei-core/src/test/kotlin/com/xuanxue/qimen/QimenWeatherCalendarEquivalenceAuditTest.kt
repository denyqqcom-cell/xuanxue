package com.xuanxue.qimen

import java.io.File
import java.security.MessageDigest
import java.time.LocalDate
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * Structure-only audit for the CDAF-H2 calendar-equivalence negative controls.
 *
 * This test deliberately uses no HKO forecast data and no weather outcome data.
 * It verifies only that the preregistered solar-term-segment +/-1 day shams are
 * deterministic calendar controls that preserve each segment's trigger count
 * while breaking exact civil-date alignment.
 *
 * The 2000-01-01..2099-12-31 window is an audit window only. The generated
 * schedule hash is NOT a future Batch Freeze and grants no empirical credit.
 */
class QimenWeatherCalendarEquivalenceAuditTest {

    private data class SignalHit(val palace: Int, val star: String, val heavenStem: String)
    private data class DayState(val date: LocalDate, val jieQi: String, val signal: Boolean)

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

    private fun sha256Hex(value: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))
            .joinToString("") { byte -> "%02x".format(byte) }

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

    @Test
    fun solarTermSegmentPhaseShamsPreservePropensityAndBreakExactAlignment() {
        val coreStart = LocalDate.of(2000, 1, 1)
        val coreEnd = LocalDate.of(2099, 12, 31)

        // The extension exists only to identify the full solar-term segments
        // that touch the audit-window boundaries. No weather data is consulted.
        val scanStart = coreStart.minusDays(40)
        val scanEnd = coreEnd.plusDays(40)

        val states = mutableListOf<DayState>()
        var date = scanStart
        while (!date.isAfter(scanEnd)) {
            val chart = QimenEngine.bySolar(
                date.year,
                date.monthValue,
                date.dayOfMonth,
                17,
                0,
                QimenEngine.JuMethod.CHAI_BU_FUTOU,
            )
            assertEquals("CHAI_BU_FUTOU", chart.juMethodUsed)
            assertEquals('酉', chart.hourGZ[1], "17:00 HKT civil time must remain 酉时 at $date")
            states += DayState(date, chart.jieQi, coreRainSignal(chart).isNotEmpty())
            date = date.plusDays(1)
        }

        val segments = mutableListOf<List<DayState>>()
        var current = mutableListOf<DayState>()
        for (state in states) {
            if (current.isNotEmpty() && current.last().jieQi != state.jieQi) {
                segments += current.toList()
                current = mutableListOf()
            }
            current += state
        }
        if (current.isNotEmpty()) segments += current.toList()

        val completeSegments = segments.filter { segment ->
            !segment.first().date.isBefore(coreStart) && !segment.last().date.isAfter(coreEnd)
        }

        assertTrue(completeSegments.size > 2_300, "100 years should contain thousands of complete solar-term segments")
        assertTrue(completeSegments.all { it.size > 1 }, "phase shams require multi-day segments")
        assertTrue(completeSegments.all { segment -> segment.all { it.jieQi == segment.first().jieQi } })

        var totalSegmentDays = 0
        var originalTriggers = 0
        var plusTriggers = 0
        var minusTriggers = 0
        var mixedSegments = 0
        var allZeroSegments = 0
        var allOneSegments = 0
        var plusHamming = 0
        var minusHamming = 0
        var minSegmentDays = Int.MAX_VALUE
        var maxSegmentDays = 0

        val segmentCountsByJieqi = linkedMapOf<String, Int>()
        val originalTriggersByJieqi = linkedMapOf<String, Int>()
        val plusTriggersByJieqi = linkedMapOf<String, Int>()
        val minusTriggersByJieqi = linkedMapOf<String, Int>()
        val schedule = StringBuilder()

        completeSegments.forEachIndexed { segmentIndex, segment ->
            val n = segment.size
            val original = segment.map { it.signal }
            val plus = List(n) { i -> original[(i + 1) % n] }
            val minus = List(n) { i -> original[(i - 1 + n) % n] }

            val originalCount = original.count { it }
            val plusCount = plus.count { it }
            val minusCount = minus.count { it }

            assertEquals(originalCount, plusCount, "+1 sham must preserve trigger count within ${segment.first().jieQi} ${segment.first().date}")
            assertEquals(originalCount, minusCount, "-1 sham must preserve trigger count within ${segment.first().jieQi} ${segment.first().date}")

            val jieQi = segment.first().jieQi
            val segmentId = "%04d:%s:%s:%s".format(
                segmentIndex + 1,
                jieQi,
                segment.first().date,
                segment.last().date,
            )

            segmentCountsByJieqi[jieQi] = segmentCountsByJieqi.getOrDefault(jieQi, 0) + 1
            originalTriggersByJieqi[jieQi] = originalTriggersByJieqi.getOrDefault(jieQi, 0) + originalCount
            plusTriggersByJieqi[jieQi] = plusTriggersByJieqi.getOrDefault(jieQi, 0) + plusCount
            minusTriggersByJieqi[jieQi] = minusTriggersByJieqi.getOrDefault(jieQi, 0) + minusCount

            when (originalCount) {
                0 -> allZeroSegments += 1
                n -> allOneSegments += 1
                else -> mixedSegments += 1
            }

            for (i in 0 until n) {
                if (original[i] != plus[i]) plusHamming += 1
                if (original[i] != minus[i]) minusHamming += 1
                schedule.append(segmentId)
                    .append('|').append(segment[i].date)
                    .append('|').append(if (original[i]) '1' else '0')
                    .append('|').append(if (plus[i]) '1' else '0')
                    .append('|').append(if (minus[i]) '1' else '0')
                    .append('\n')
            }

            totalSegmentDays += n
            originalTriggers += originalCount
            plusTriggers += plusCount
            minusTriggers += minusCount
            minSegmentDays = minOf(minSegmentDays, n)
            maxSegmentDays = maxOf(maxSegmentDays, n)
        }

        assertEquals(originalTriggers, plusTriggers)
        assertEquals(originalTriggers, minusTriggers)
        assertEquals(originalTriggersByJieqi, plusTriggersByJieqi)
        assertEquals(originalTriggersByJieqi, minusTriggersByJieqi)
        assertEquals(24, segmentCountsByJieqi.size, "all 24 solar terms must have complete segments in the audit")
        assertTrue(mixedSegments > 0, "at least some segments must contain both trigger and non-trigger days")
        assertTrue(plusHamming > 0, "+1 sham must break exact-date alignment somewhere")
        assertTrue(minusHamming > 0, "-1 sham must break exact-date alignment somewhere")
        assertFalse(schedule.isEmpty())

        val scheduleHash = sha256Hex(schedule.toString())
        assertEquals(64, scheduleHash.length)

        val reportDir = File("build/reports")
        reportDir.mkdirs()
        val report = File(reportDir, "qimen-weather-calendar-equivalence-audit-v01.json")
        report.writeText(
            buildString {
                append("{\n")
                append("  \"audit_scope\": \"SOLAR_TERM_SEGMENT_PHASE_SHAM_STRUCTURE_ONLY\",\n")
                append("  \"calendar_window\": \"2000-01-01/2099-12-31\",\n")
                append("  \"boundary_scan_padding_days\": 40,\n")
                append("  \"civil_time_hkt\": \"17:00\",\n")
                append("  \"qimen_ju_method\": \"CHAI_BU_FUTOU\",\n")
                append("  \"qimen_engine_blob_sha\": \"1912760ccd10cb4a58eb8faec06669c0d690657b\",\n")
                append("  \"sham_policy\": \"WITHIN_COMPLETE_SOLAR_TERM_SEGMENT_CYCLIC_PLUS_MINUS_1_DAY\",\n")
                append("  \"weather_forecast_data_used\": false,\n")
                append("  \"weather_outcome_data_used\": false,\n")
                append("  \"complete_segment_count\": ${completeSegments.size},\n")
                append("  \"complete_segment_days\": $totalSegmentDays,\n")
                append("  \"min_segment_days\": $minSegmentDays,\n")
                append("  \"max_segment_days\": $maxSegmentDays,\n")
                append("  \"mixed_segments\": $mixedSegments,\n")
                append("  \"all_zero_segments\": $allZeroSegments,\n")
                append("  \"all_one_segments\": $allOneSegments,\n")
                append("  \"original_triggers\": $originalTriggers,\n")
                append("  \"plus_1_triggers\": $plusTriggers,\n")
                append("  \"minus_1_triggers\": $minusTriggers,\n")
                append("  \"plus_1_hamming_days\": $plusHamming,\n")
                append("  \"minus_1_hamming_days\": $minusHamming,\n")
                append("  \"segments_by_jieqi\": ${stringIntMapJson(segmentCountsByJieqi)},\n")
                append("  \"original_triggers_by_jieqi\": ${stringIntMapJson(originalTriggersByJieqi)},\n")
                append("  \"plus_1_triggers_by_jieqi\": ${stringIntMapJson(plusTriggersByJieqi)},\n")
                append("  \"minus_1_triggers_by_jieqi\": ${stringIntMapJson(minusTriggersByJieqi)},\n")
                append("  \"audit_schedule_sha256\": \"$scheduleHash\",\n")
                append("  \"future_batch_schedule_frozen\": false,\n")
                append("  \"sample_duration_usable\": false,\n")
                append("  \"empirical_credit\": \"NONE\"\n")
                append("}\n")
            },
            Charsets.UTF_8,
        )

        assertTrue(report.isFile && report.length() > 0L)
    }
}
