package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.PlateState
import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.FullPlateLockReason
import com.xuanxue.qimen.core.plate.FullPlateResolution
import com.xuanxue.qimen.core.plate.FullPlateResolver
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.plate.QimenSpirit
import com.xuanxue.qimen.core.plate.QimenStar
import com.xuanxue.qimen.core.xun.XunResolver
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs

class QimenFullBoardGoldenTest {
    @Test
    fun `1995 june 11 source case reproduces calendar and resolved four-layer board end to end`() {
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
        assertEquals(PlateState.FULL_PLATE_RESOLVED_SUPPORTED_METHOD, chart.plateState)

        val resolved = assertIs<FullPlateResolution.Resolved>(chart.fullPlate)
        val sky = resolved.plate.sky
        assertEquals(listOf(QimenStar.TIAN_REN), sky.starsAt(9))
        assertEquals(listOf(QimenStar.TIAN_CHONG), sky.starsAt(2))
        assertEquals(listOf(QimenStar.TIAN_FU), sky.starsAt(7))
        assertEquals(listOf(QimenStar.TIAN_YING), sky.starsAt(6))
        assertEquals(setOf(QimenStar.TIAN_RUI, QimenStar.TIAN_QIN), sky.starsAt(1).toSet())
        assertEquals(listOf(QimenStar.TIAN_ZHU), sky.starsAt(8))
        assertEquals(listOf(QimenStar.TIAN_XIN), sky.starsAt(3))
        assertEquals(listOf(QimenStar.TIAN_PENG), sky.starsAt(4))

        val human = resolved.plate.human
        assertEquals(QimenGate.SHENG, human.gateAt(2))
        assertEquals(QimenGate.SHANG, human.gateAt(7))
        assertEquals(QimenGate.DU, human.gateAt(6))
        assertEquals(QimenGate.JING_SCENERY, human.gateAt(1))

        val spirit = resolved.plate.spirit
        assertEquals(QimenSpirit.VALUE_SYMBOL, spirit.spiritAt(9))
        assertEquals(QimenSpirit.TENG_SHE, spirit.spiritAt(2))
        assertEquals(QimenSpirit.TAI_YIN, spirit.spiritAt(7))
        assertEquals(QimenSpirit.LIU_HE, spirit.spiritAt(6))
        assertEquals(QimenSpirit.BAI_HU, spirit.spiritAt(1))
    }

    @Test
    fun `center target returns explicit full-plate lock instead of fabricated board`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.JIA, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)

        val locked = assertIs<FullPlateResolution.Locked>(FullPlateResolver.resolve(earth, duty, Dun.YIN))
        assertEquals(
            setOf(FullPlateLockReason.VALUE_STAR_IN_CENTER, FullPlateLockReason.VALUE_GATE_IN_CENTER),
            locked.reasons,
        )
    }
}
