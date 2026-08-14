package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenError
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.ju.JuMethod
import com.xuanxue.qimen.core.school.BoardSchool
import com.xuanxue.qimen.core.school.QimenSchoolConfig
import java.time.Instant
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNull
import kotlin.test.assertTrue

class QimenEngineGateTest {
    private val knownInstant = Instant.parse("2022-08-08T04:00:00Z").toEpochMilli()

    @Test
    fun `default engine returns only verified partial chart and no fake earth plate`() {
        val result = QimenEngine.cast(QimenRequest(knownInstant))
        assertTrue(result.isSuccess)
        val chart = result.getOrThrow()
        assertEquals("立秋", chart.jieqi)
        assertEquals(Dun.YIN, chart.dun)
        assertEquals(2, chart.ju)
        assertNull(chart.earth)
    }

    @Test
    fun `true solar time is explicitly unsupported`() {
        assertUnsupported(QimenSchoolConfig(useTrueSolarTime = true), "useTrueSolarTime")
    }

    @Test
    fun `unverified ju methods are explicitly unsupported`() {
        assertUnsupported(QimenSchoolConfig(juMethod = JuMethod.CHAI_BU_FUTOU), "CHAI_BU_FUTOU")
        assertUnsupported(QimenSchoolConfig(juMethod = JuMethod.ZHI_RUN), "ZHI_RUN")
        assertUnsupported(QimenSchoolConfig(juMethod = JuMethod.MAO_SHAN), "MAO_SHAN")
    }

    @Test
    fun `fei gong is explicitly unsupported`() {
        assertUnsupported(QimenSchoolConfig(boardSchool = BoardSchool.FEI_GONG), "FEI_GONG")
    }

    private fun assertUnsupported(school: QimenSchoolConfig, flag: String) {
        val failure = QimenEngine.cast(QimenRequest(knownInstant, school = school)).exceptionOrNull()
        val error = assertIs<QimenError.UnsupportedSchool>(failure)
        assertEquals(flag, error.flag)
    }
}
