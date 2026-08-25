package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertFailsWith
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class QimenEngineTest {

    @Test
    fun alignUserScript() {
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        assertEquals("立秋", c.jieQi)
        assertEquals(-1, c.yinYang)
        assertEquals(5, c.ju)
        assertEquals("中元", c.yuan)
        assertEquals("CHAI_BU_DAYCOUNT", c.juMethodUsed)
        assertTrue(c.gongs.all { it.diGan.isNotEmpty() })

        val f = QimenEngine.bySolar(
            2026, 8, 12, 15, 37,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )
        assertEquals(5, f.ju)
        assertEquals("中元", f.yuan)
        assertEquals("CHAI_BU_FUTOU", f.juMethodUsed)
        assertTrue(f.juMethod.contains("实验"))
    }

    @Test
    fun liqiuDayCountNotFutou() {
        val c = QimenEngine.bySolar(2026, 8, 7, 16, 0)
        assertEquals("立秋", c.jieQi)
        assertEquals("CHAI_BU_DAYCOUNT", c.juMethodUsed)
        assertEquals("上元", c.yuan)
        assertEquals(2, c.ju)
        assertEquals("下元", c.yuanFutou)
        assertTrue(c.jieqiDayIndex in 1..15)
    }

    @Test
    fun dayCountFailsClosedOutsideDocumentedWindow() {
        assertFailsWith<IllegalArgumentException> { QimenEngine.yuanByDayCount(0) }
        assertFailsWith<IllegalArgumentException> { QimenEngine.yuanByDayCount(16) }
    }

    @Test
    fun zhiRunFailsClosedInsteadOfUsingFutouApproximation() {
        assertFailsWith<UnsupportedOperationException> {
            QimenEngine.bySolar(
                2026, 8, 12, 15, 37,
                QimenEngine.JuMethod.ZHI_RUN,
            )
        }
    }

    @Test
    fun winterSolsticeYang() {
        // 12/22 10:00 may still be before the actual solstice instant; use the next civil day
        // so the jieqi clock is unambiguously inside 冬至 and still inside R-JU-001's 1..15 window.
        val c = QimenEngine.bySolar(2026, 12, 23, 10, 0)
        assertEquals("冬至", c.jieQi)
        assertEquals(1, c.yinYang)
        assertTrue(c.jieqiDayIndex in 1..15)
    }

    @Test
    fun earthPlateKeepsWuOnJuPalace() {
        val c = QimenEngine.bySolar(1990, 5, 20, 12, 30)
        assertEquals(9, c.gongs.size)
        val di = c.gongs.associate { it.palace to it.diGan }
        assertEquals("戊", di[c.ju])
    }

    @Test
    fun jiaHourDoesNotCrash() {
        val c = QimenEngine.bySolar(2026, 8, 12, 4, 30)
        assertEquals("甲寅", c.hourGZ)
        assertTrue(
            c.gongs.filter { it.palace != 5 }
                .all { it.diGan.isNotEmpty() && it.tianXing.isNotEmpty() },
        )
    }

    @Test
    fun zhiFuStarLandsOnHourStemTargetPalace() {
        // Structural invariant from R-SKY-001 only. This does not upgrade the experimental
        // full-board implementation to a golden-board-verified plate.
        for (h in listOf(0, 4, 9, 15, 21)) {
            val c = QimenEngine.bySolar(2026, 8, 12, h, 30)
            val effectiveHourGan = if (c.hourGZ[0] == '甲') c.dunGan else c.hourGZ[0].toString()
            val rawTarget = c.gongs.first { it.diGan == effectiveHourGan }.palace
            val expectedTarget = if (rawTarget == 5) 2 else rawTarget
            val targetStar = c.gongs.first { it.palace == expectedTarget }.tianXing
            assertTrue(
                targetStar.contains(c.zhiFu),
                "h=$h hour=${c.hourGZ} zhiFu=${c.zhiFu} expected=$expectedTarget actualStar=$targetStar",
            )
        }
    }

    @Test
    fun ringRotationPreservesGateAdjacency() {
        for (h in listOf(9, 11, 15, 21)) {
            val c = QimenEngine.bySolar(2026, 8, 12, h, 0)
            val xiu = c.gongs.first { it.renMen == "休门" }.palace
            val sheng = c.gongs.first { it.renMen == "生门" }.palace
            val ring = QimenEngine.RING
            val d = (ring.indexOf(xiu) - ring.indexOf(sheng) + 8) % 8
            assertTrue(d == 1 || d == 7, "h=$h 休${xiu} 生${sheng} 环距=$d")
        }
    }

    @Test
    fun twelveDoubleHoursKeepEightOuterPlateSlotsPopulated() {
        for (h in listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22)) {
            val c = QimenEngine.bySolar(2026, 8, 12, h, 30)
            val outer = c.gongs.filter { it.palace != 5 }
            assertEquals(8, outer.count { it.tianXing.isNotBlank() }, "star h=$h")
            assertEquals(8, outer.count { it.renMen.isNotBlank() }, "gate h=$h")
            assertEquals(8, outer.count { it.shenPan.isNotBlank() }, "spirit h=$h")
        }
    }

    @Test
    fun wuBuYuGeneratorMatchesGoldenFixturesAndRejectsNearMisses() {
        // handoff/qimen/05_FIXTURES.jsonl: 甲日庚午、己日乙亥 are true.
        assertTrue(QimenEngine.isWuBuYuStemPair('甲', '庚'))
        assertTrue(QimenEngine.isWuBuYuStemPair('己', '乙'))

        // Near misses must not pass merely because the test executes.
        assertFalse(QimenEngine.isWuBuYuStemPair('甲', '己'))
        assertFalse(QimenEngine.isWuBuYuStemPair('甲', '辛'))
        assertFalse(QimenEngine.isWuBuYuStemPair('己', '甲'))
    }

    @Test
    fun dayHourKongAndTimeMaAreSeparated() {
        // 2026-08-12 00:30 uses a 子时; this fixture intentionally makes day/hour旬 different.
        val c = QimenEngine.bySolar(2026, 8, 12, 0, 30)
        assertEquals('子', c.hourGZ[1])

        // 马星 must follow the占时支, not silently reuse day branch.
        assertEquals(QimenEngine.maXingOf(c.hourGZ[1].toString()), c.maXing)
        assertEquals("寅", c.maXing)
        assertNotEquals(QimenEngine.maXingOf(c.dayGZ[1].toString()), c.maXing)

        // Day and hour voids are separate model facts and separate palace flags.
        assertNotEquals(c.dayKong, c.hourKong)
        val expectedDay = c.dayKong.map { QimenEngine.zhiPalace(it) }.toSet()
        val expectedHour = c.hourKong.map { QimenEngine.zhiPalace(it) }.toSet()
        val actualDay = c.gongs.filter { it.isDayKong }.map { it.palace }.toSet()
        val actualHour = c.gongs.filter { it.isHourKong }.map { it.palace }.toSet()
        assertEquals(expectedDay, actualDay)
        assertEquals(expectedHour, actualHour)
    }
}
