package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.plate.HumanPlateBuilder
import com.xuanxue.qimen.core.plate.HumanPlateError
import com.xuanxue.qimen.core.plate.QimenGate
import com.xuanxue.qimen.core.xun.XunResolver
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNull

class QimenHumanPlateTest {
    @Test
    fun `2004 yang eight wu-wu reproduces printed eight-gate board`() {
        val earth = EarthPlateBuilder.build(Dun.YANG, 8)
        val hour = StemBranch(Stem.WU, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YANG)
        val plate = HumanPlateBuilder.build(duty).getOrThrow()

        assertEquals(QimenGate.SHANG, plate.gateAt(1))
        assertEquals(QimenGate.KAI, plate.gateAt(2))
        assertEquals(QimenGate.JING_SCENERY, plate.gateAt(3))
        assertEquals(QimenGate.SI, plate.gateAt(4))
        assertNull(plate.gateAt(5))
        assertEquals(QimenGate.SHENG, plate.gateAt(6))
        assertEquals(QimenGate.XIU, plate.gateAt(7))
        assertEquals(QimenGate.DU, plate.gateAt(8))
        assertEquals(QimenGate.JING, plate.gateAt(9))
    }

    @Test
    fun `printed yin eight wu-xu reproduces complete eight-gate board`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.WU, Branch.XU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)
        val plate = HumanPlateBuilder.build(duty).getOrThrow()

        assertEquals(QimenGate.SI, plate.gateAt(1))
        assertEquals(QimenGate.SHANG, plate.gateAt(2))
        assertEquals(QimenGate.KAI, plate.gateAt(3))
        assertEquals(QimenGate.XIU, plate.gateAt(4))
        assertNull(plate.gateAt(5))
        assertEquals(QimenGate.JING_SCENERY, plate.gateAt(6))
        assertEquals(QimenGate.DU, plate.gateAt(7))
        assertEquals(QimenGate.JING, plate.gateAt(8))
        assertEquals(QimenGate.SHENG, plate.gateAt(9))
    }

    @Test
    fun `center-current value gate stays locked until a complete center board is sourced`() {
        val earth = EarthPlateBuilder.build(Dun.YIN, 8)
        val hour = StemBranch(Stem.JIA, Branch.WU)
        val duty = DutyMovementResolver.resolve(earth, XunResolver.resolve(hour), hour, Dun.YIN)

        assertEquals(5, duty.valueGatePalace)
        val result = HumanPlateBuilder.build(duty)
        assertIs<HumanPlateError.CenterValueGateUnverified>(result.exceptionOrNull())
    }
}
