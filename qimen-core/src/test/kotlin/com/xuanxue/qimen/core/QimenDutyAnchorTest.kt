package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyAnchorResolver
import com.xuanxue.qimen.core.plate.DutyGateAnchorState
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.plate.QimenStar
import com.xuanxue.qimen.core.xun.XunResolver
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class QimenDutyAnchorTest {
    @Test
    fun `source example yang eight jia-yin anchors tian-fu and du at palace four`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val xun = XunResolver.resolve(StemBranch.fromSexagenaryIndex(50)) // 甲寅

        val duty = DutyAnchorResolver.resolve(earth, xun)

        assertEquals(4, duty.dunYiPalace)
        assertEquals(QimenStar.TIAN_FU, duty.valueStar)
        assertEquals(QimenGate.DU, duty.valueGate)
        assertEquals(DutyGateAnchorState.RESOLVED, duty.gateState)
    }

    @Test
    fun `center palace never invents a gate host rule`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 1)
        val xun = XunResolver.resolve(StemBranch.fromSexagenaryIndex(40)) // 甲辰 -> 壬

        val duty = DutyAnchorResolver.resolve(earth, xun)

        assertEquals(5, duty.dunYiPalace)
        assertEquals(QimenStar.TIAN_QIN, duty.valueStar)
        assertNull(duty.valueGate)
        assertEquals(DutyGateAnchorState.CENTER_PALACE_REQUIRES_HOST_RULE, duty.gateState)
    }
}
