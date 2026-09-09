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

class QimenDutyAnchorTest {
    @Test
    fun `source example yang eight jia-yin anchors tian-fu and du at palace four`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val xun = XunResolver.resolve(StemBranch.fromSexagenaryIndex(50)) // 甲寅

        val duty = DutyAnchorResolver.resolve(earth, xun)

        assertEquals(4, duty.dunYiPalace)
        assertEquals(4, duty.gateHomePalace)
        assertEquals(QimenStar.TIAN_FU, duty.valueStar)
        assertEquals(QimenGate.DU, duty.valueGate)
        assertEquals(DutyGateAnchorState.RESOLVED, duty.gateState)
    }

    @Test
    fun `printed yin eight center case hosts tian-qin with kun-two death gate`() {
        // 乙亥年甲申月丙子日戊戌时：甲午旬、阴遁八局，原书明确天禽值符、死门值使。
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val xun = XunResolver.resolve(StemBranch.fromSexagenaryIndex(30)) // 甲午 -> 辛

        val duty = DutyAnchorResolver.resolve(earth, xun)

        assertEquals(5, duty.dunYiPalace)
        assertEquals(2, duty.gateHomePalace)
        assertEquals(QimenStar.TIAN_QIN, duty.valueStar)
        assertEquals(QimenGate.SI, duty.valueGate)
        assertEquals(DutyGateAnchorState.CENTER_PALACE_HOSTED_KUN2, duty.gateState)
    }
}
