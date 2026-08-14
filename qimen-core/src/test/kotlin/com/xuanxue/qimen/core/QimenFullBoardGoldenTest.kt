package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.plate.HumanPlateBuilder
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.plate.QimenSpirit
import com.xuanxue.qimen.core.plate.QimenStar
import com.xuanxue.qimen.core.plate.SkyPlateBuilder
import com.xuanxue.qimen.core.plate.SpiritPlateBuilder
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals

class QimenFullBoardGoldenTest {
    @Test
    fun `1995 june 11 source case reproduces calendar duty sky human and spirit layers`() {
        val instant = LocalDateTime.of(1995, 6, 11, 9, 30)
            .atZone(ZoneId.of("Asia/Shanghai"))
            .toInstant()
            .toEpochMilli()
        val chart = QimenEngine.cast(QimenRequest(instantEpochMs = instant)).getOrThrow()

        assertEquals("癸酉", chart.dayPillar.zh)
        assertEquals("丁巳", chart.hourPillar.zh)
        assertEquals("甲寅", chart.xun.xunShou.zh)
        assertEquals(3, chart.ju)
        assertEquals(QimenStar.TIAN_REN, chart.duty.anchor.valueStar)
        assertEquals(9, chart.duty.valueStarPalace)
        assertEquals(QimenGate.SHENG, chart.duty.anchor.valueGate)
        assertEquals(2, chart.duty.valueGatePalace)

        val sky = SkyPlateBuilder.build(chart.earthPlate, chart.duty).getOrThrow()
        assertEquals(listOf(QimenStar.TIAN_REN), sky.starsAt(9))
        assertEquals(listOf(QimenStar.TIAN_CHONG), sky.starsAt(2))
        assertEquals(listOf(QimenStar.TIAN_FU), sky.starsAt(7))
        assertEquals(listOf(QimenStar.TIAN_YING), sky.starsAt(6))
        assertEquals(setOf(QimenStar.TIAN_RUI, QimenStar.TIAN_QIN), sky.starsAt(1).toSet())
        assertEquals(listOf(QimenStar.TIAN_ZHU), sky.starsAt(8))
        assertEquals(listOf(QimenStar.TIAN_XIN), sky.starsAt(3))
        assertEquals(listOf(QimenStar.TIAN_PENG), sky.starsAt(4))

        val human = HumanPlateBuilder.build(chart.duty).getOrThrow()
        assertEquals(QimenGate.SHENG, human.gateAt(2))
        assertEquals(QimenGate.SHANG, human.gateAt(7))
        assertEquals(QimenGate.DU, human.gateAt(6))
        assertEquals(QimenGate.JING_SCENERY, human.gateAt(1))

        val spirit = SpiritPlateBuilder.build(chart.duty, chart.jieqi.dun).getOrThrow()
        assertEquals(QimenSpirit.VALUE_SYMBOL, spirit.spiritAt(9))
        assertEquals(QimenSpirit.TENG_SHE, spirit.spiritAt(2))
        assertEquals(QimenSpirit.TAI_YIN, spirit.spiritAt(7))
        assertEquals(QimenSpirit.LIU_HE, spirit.spiritAt(6))
        assertEquals(QimenSpirit.BAI_HU, spirit.spiritAt(1))
    }
}
