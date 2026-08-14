package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.QimenStar
import com.xuanxue.qimen.core.plate.SkyPlateBuilder
import com.xuanxue.qimen.core.plate.SkyPlateError
import com.xuanxue.qimen.core.xun.XunResolver
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertTrue

class QimenSkyPlateTest {
    @Test
    fun `2004 yang eight wu-wu reproduces printed sky-star board`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val hour = StemBranch(Stem.WU, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YANG)
        val plate = SkyPlateBuilder.build(duty).getOrThrow()

        assertEquals(listOf(QimenStar.TIAN_CHONG), plate.starsAt(1))
        assertEquals(listOf(QimenStar.TIAN_XIN), plate.starsAt(2))
        assertEquals(listOf(QimenStar.TIAN_YING), plate.starsAt(3))
        assertEquals(setOf(QimenStar.TIAN_RUI, QimenStar.TIAN_QIN), plate.starsAt(4).toSet())
        assertTrue(plate.starsAt(5).isEmpty())
        assertEquals(listOf(QimenStar.TIAN_REN), plate.starsAt(6))
        assertEquals(listOf(QimenStar.TIAN_PENG), plate.starsAt(7))
        assertEquals(listOf(QimenStar.TIAN_FU), plate.starsAt(8))
        assertEquals(listOf(QimenStar.TIAN_ZHU), plate.starsAt(9))
    }

    @Test
    fun `printed yin eight wu-xu reproduces tian-qin hosted sky board`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.WU, Branch.XU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)
        val plate = SkyPlateBuilder.build(duty).getOrThrow()

        assertEquals(listOf(QimenStar.TIAN_YING), plate.starsAt(1))
        assertEquals(listOf(QimenStar.TIAN_REN), plate.starsAt(2))
        assertEquals(listOf(QimenStar.TIAN_ZHU), plate.starsAt(3))
        assertEquals(listOf(QimenStar.TIAN_XIN), plate.starsAt(4))
        assertTrue(plate.starsAt(5).isEmpty())
        assertEquals(listOf(QimenStar.TIAN_FU), plate.starsAt(6))
        assertEquals(listOf(QimenStar.TIAN_CHONG), plate.starsAt(7))
        assertEquals(setOf(QimenStar.TIAN_RUI, QimenStar.TIAN_QIN), plate.starsAt(8).toSet())
        assertEquals(listOf(QimenStar.TIAN_PENG), plate.starsAt(9))
    }

    @Test
    fun `center-current value star stays locked until a complete center target board is sourced`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.XIN, Branch.YOU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)

        assertEquals(5, duty.valueStarPalace)
        val result = SkyPlateBuilder.build(duty)
        assertIs<SkyPlateError.CenterValueStarUnverified>(result.exceptionOrNull())
    }
}
