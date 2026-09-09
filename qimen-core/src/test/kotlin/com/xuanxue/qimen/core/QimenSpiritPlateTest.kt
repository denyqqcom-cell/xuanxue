package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.QimenSpirit
import com.xuanxue.qimen.core.plate.SpiritMethod
import com.xuanxue.qimen.core.plate.SpiritPlateBuilder
import com.xuanxue.qimen.core.plate.SpiritPlateError
import com.xuanxue.qimen.core.xun.XunResolver
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNull

class QimenSpiritPlateTest {
    @Test
    fun `2004 yang eight wu-wu reproduces printed spirit board`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val hour = StemBranch(Stem.WU, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YANG)
        val plate = SpiritPlateBuilder.build(duty, Dun.YANG).getOrThrow()

        assertEquals(QimenSpirit.JIU_TIAN, plate.spiritAt(1))
        assertEquals(QimenSpirit.BAI_HU, plate.spiritAt(2))
        assertEquals(QimenSpirit.TENG_SHE, plate.spiritAt(3))
        assertEquals(QimenSpirit.TAI_YIN, plate.spiritAt(4))
        assertNull(plate.spiritAt(5))
        assertEquals(QimenSpirit.JIU_DI, plate.spiritAt(6))
        assertEquals(QimenSpirit.XUAN_WU, plate.spiritAt(7))
        assertEquals(QimenSpirit.VALUE_SYMBOL, plate.spiritAt(8))
        assertEquals(QimenSpirit.LIU_HE, plate.spiritAt(9))
    }

    @Test
    fun `printed yin eight value-star-at-eight reproduces reverse spirit board`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.WU, Branch.XU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)
        val plate = SpiritPlateBuilder.build(duty, Dun.YIN).getOrThrow()

        assertEquals(QimenSpirit.TENG_SHE, plate.spiritAt(1))
        assertEquals(QimenSpirit.BAI_HU, plate.spiritAt(2))
        assertEquals(QimenSpirit.JIU_TIAN, plate.spiritAt(3))
        assertEquals(QimenSpirit.JIU_DI, plate.spiritAt(4))
        assertNull(plate.spiritAt(5))
        assertEquals(QimenSpirit.TAI_YIN, plate.spiritAt(6))
        assertEquals(QimenSpirit.LIU_HE, plate.spiritAt(7))
        assertEquals(QimenSpirit.VALUE_SYMBOL, plate.spiritAt(8))
        assertEquals(QimenSpirit.XUAN_WU, plate.spiritAt(9))
    }

    @Test
    fun `alternative per-xun spirit school remains explicitly unsupported`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val hour = StemBranch(Stem.WU, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YANG)

        val result = SpiritPlateBuilder.build(duty, Dun.YANG, SpiritMethod.PER_XUN_GROUND_SPIRITS)
        assertIs<SpiritPlateError.UnsupportedMethod>(result.exceptionOrNull())
    }

    @Test
    fun `center-current value star does not invent a spirit layout`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.XIN, Branch.YOU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)

        assertEquals(5, duty.valueStarPalace)
        val result = SpiritPlateBuilder.build(duty, Dun.YIN)
        assertIs<SpiritPlateError.CenterValueStarUnverified>(result.exceptionOrNull())
    }
}
