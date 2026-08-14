package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenEngine
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertTrue

class QimenCastInputTest {
    @Test
    fun `strict Beijing input reproduces existing 1995 core golden entry`() {
        val request = QimenCastInput.toRequest("1995-06-11", "09:30").getOrThrow()
        val expectedEpoch = LocalDateTime.of(1995, 6, 11, 9, 30)
            .atZone(ZoneId.of(QimenCastInput.ZONE_ID))
            .toInstant()
            .toEpochMilli()

        assertEquals(expectedEpoch, request.instantEpochMs)
        assertEquals("Asia/Shanghai", request.zoneId)

        val chart = QimenEngine.cast(request).getOrThrow()
        assertEquals("癸酉", chart.dayPillar.zh)
        assertEquals("丁巳", chart.hourPillar.zh)
        assertEquals(3, chart.ju)
    }

    @Test
    fun `invalid calendar date is rejected before core cast`() {
        val result = QimenCastInput.toRequest("2026-02-30", "10:30")
        assertTrue(result.isFailure)
        assertIs<QimenCastInput.InputError.InvalidDate>(result.exceptionOrNull())
    }

    @Test
    fun `invalid clock time is rejected before core cast`() {
        val result = QimenCastInput.toRequest("2026-08-15", "24:00")
        assertTrue(result.isFailure)
        assertIs<QimenCastInput.InputError.InvalidTime>(result.exceptionOrNull())
    }

    @Test
    fun `display and parse roundtrip keeps the same Beijing minute`() {
        val original = LocalDateTime.of(2026, 8, 15, 0, 21)
            .atZone(ZoneId.of(QimenCastInput.ZONE_ID))
            .toInstant()
            .toEpochMilli()

        val display = QimenCastInput.displayForEpochMs(original)
        assertEquals("2026-08-15", display.dateText)
        assertEquals("00:21", display.timeText)

        val parsed = QimenCastInput.toRequest(display.dateText, display.timeText).getOrThrow()
        assertEquals(original, parsed.instantEpochMs)
    }
}
