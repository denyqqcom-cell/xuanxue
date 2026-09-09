package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.plate.QimenStar
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals

class QimenEngineDutyIntegrationTest {
    @Test
    fun `2004 source case reproduces day hour ju duty star and duty gate end to end`() {
        val instant = LocalDateTime.of(2004, 5, 29, 11, 30)
            .atZone(ZoneId.of("Asia/Shanghai"))
            .toInstant()
            .toEpochMilli()

        val chart = QimenEngine.cast(QimenRequest(instantEpochMs = instant)).getOrThrow()

        assertEquals("戊申", chart.dayPillar.zh)
        assertEquals("戊午", chart.hourPillar.zh)
        assertEquals("甲寅", chart.xun.xunShou.zh)
        assertEquals(8, chart.ju)
        assertEquals(4, chart.duty.anchor.dunYiPalace)
        assertEquals(QimenStar.TIAN_FU, chart.duty.anchor.valueStar)
        assertEquals(QimenGate.DU, chart.duty.anchor.valueGate)
        assertEquals(8, chart.duty.valueStarPalace)
        assertEquals(8, chart.duty.valueGatePalace)
    }
}
