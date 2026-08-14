package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyGateAnchorState
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.plate.QimenStar
import com.xuanxue.qimen.core.xun.XunResolver
import kotlin.test.Test
import kotlin.test.assertEquals

class QimenDutyMovementTest {
    @Test
    fun `2004 yang eight wu-wu moves tian-fu and du to palace eight`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val hour = StemBranch(Stem.WU, Branch.WU)
        val xun = XunResolver.resolve(hour)

        val duty = DutyMovementResolver.resolve(earth, xun, hour, Dun.YANG)

        assertEquals(4, duty.anchor.dunYiPalace)
        assertEquals(QimenStar.TIAN_FU, duty.anchor.valueStar)
        assertEquals(QimenGate.DU, duty.anchor.valueGate)
        assertEquals(4, duty.branchStepsFromXunHead)
        assertEquals(8, duty.valueStarPalace)
        assertEquals(8, duty.valueGatePalace)
    }

    @Test
    fun `printed yin seven ji-you fixture resolves tian-chong to six and shang gate to seven`() {
        // Source case: 辛巳年 丙申月 壬戌日 己酉时，甲辰旬，阴遁七局；天冲值符落6，伤门值使落7。
        val earth = EarthPlateBuilder.build(Dun.YIN, 7)
        val hour = StemBranch(Stem.JI, Branch.YOU)
        val xun = XunResolver.resolve(hour)

        val duty = DutyMovementResolver.resolve(earth, xun, hour, Dun.YIN)

        assertEquals("甲辰", xun.xunShou.zh)
        assertEquals(3, duty.anchor.dunYiPalace)
        assertEquals(QimenStar.TIAN_CHONG, duty.anchor.valueStar)
        assertEquals(QimenGate.SHANG, duty.anchor.valueGate)
        assertEquals(5, duty.branchStepsFromXunHead)
        assertEquals(6, duty.valueStarPalace)
        assertEquals(7, duty.valueGatePalace)
    }

    @Test
    fun `printed yin eight center-hosted case resolves tian-qin to eight and death gate to one`() {
        // Source case: 乙亥年 甲申月 丙子日 戊戌时，甲午旬，阴遁八局；天禽值符落8，死门值使落1。
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.WU, Branch.XU)
        val xun = XunResolver.resolve(hour)

        val duty = DutyMovementResolver.resolve(earth, xun, hour, Dun.YIN)

        assertEquals("甲午", xun.xunShou.zh)
        assertEquals(5, duty.anchor.dunYiPalace)
        assertEquals(2, duty.anchor.gateHomePalace)
        assertEquals(DutyGateAnchorState.CENTER_PALACE_HOSTED_KUN2, duty.anchor.gateState)
        assertEquals(QimenStar.TIAN_QIN, duty.anchor.valueStar)
        assertEquals(QimenGate.SI, duty.anchor.valueGate)
        assertEquals(4, duty.branchStepsFromXunHead)
        assertEquals(8, duty.valueStarPalace)
        assertEquals(1, duty.valueGatePalace)
    }

    @Test
    fun `jia hour uses hidden dun-yi and leaves duty at anchor`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 7)
        val hour = StemBranch(Stem.JIA, Branch.CHEN)
        val xun = XunResolver.resolve(hour)

        val duty = DutyMovementResolver.resolve(earth, xun, hour, Dun.YIN)

        assertEquals(0, duty.branchStepsFromXunHead)
        assertEquals(duty.anchor.dunYiPalace, duty.valueStarPalace)
        assertEquals(duty.anchor.dunYiPalace, duty.valueGatePalace)
    }
}
