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
    fun liqiuDayCountKeepsFutouMetadataSeparate() {
        // HKO 2026 almanac gives Liqiu at 2026-08-07 19:43 HKT; use 20:00 so
        // this regression is safely after the actual transition.
        val c = QimenEngine.bySolar(2026, 8, 7, 20, 0)
        assertEquals("立秋", c.jieQi)
        assertEquals("CHAI_BU_DAYCOUNT", c.juMethodUsed)
        assertEquals("上元", c.yuan)
        assertEquals(2, c.ju)

        // 2026-08-07 is 癸丑. Under the five-day拆补符头 rule the nearest
        // preceding 甲/己 head is 己酉, which belongs to上元. This metadata is
        // computed independently from the selected DAYCOUNT execution method.
        assertEquals("上元", c.yuanFutou)
        assertTrue(c.jieqiDayIndex in 1..15)
    }

    @Test
    fun futouPreservesIndependentAstronomicalLiqiuBoundaryInsteadOfSwitchingAtMidnight() {
        // Source-method policy:
        // - QM-SRC-0021 K2E-W1-QM-0021-0019 and QM-SRC-0028
        //   K2E-W1-QM-0028-0018 both state that拆补 switches to the new
        //   solar-term ju system at the actual交节时辰 while retaining the
        //   applicable five-day甲/己 head for yuan classification.
        // Independent astronomy fixture:
        // - Hong Kong Observatory, 2026 August almanac / Date and Time of the
        //   24 Solar Terms: Liqiu (Autumn Commences) = 2026-08-07 19:43 HKT.
        //   HKO states its solar-term astronomical information is based on data
        //   from HM Nautical Almanac Office and the US Naval Observatory.
        //
        // This closes the previous circularity where the regression discovered
        // the boundary only from the same lunar-java dependency used by Engine.
        fun chartAt(totalMinutes: Int) = QimenEngine.bySolar(
            2026,
            8,
            7,
            totalMinutes / 60,
            totalMinutes % 60,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )

        val boundaryMinute = (1 until 24 * 60).firstOrNull { minute ->
            chartAt(minute).jieQi == "立秋"
        }
        assertTrue(boundaryMinute != null && boundaryMinute > 0)
        assertEquals(19 * 60 + 43, boundaryMinute, "Engine solar-term minute must match HKO 2026 almanac")

        val before = chartAt(boundaryMinute!! - 1)
        val after = chartAt(boundaryMinute)

        assertEquals("大暑", before.jieQi)
        assertEquals("立秋", after.jieQi)
        assertEquals("癸丑", before.dayGZ)
        assertEquals(before.dayGZ, after.dayGZ)
        assertEquals("上元", before.yuan)
        assertEquals(before.yuan, after.yuan)

        // Same civil date and same five-day head; only the verified solar-term side changed.
        // 大暑上元=阴7, 立秋上元=阴2.
        assertEquals(-1, before.yinYang)
        assertEquals(-1, after.yinYang)
        assertEquals(7, before.ju)
        assertEquals(2, after.ju)
    }

    @Test
    fun qm0021ChaibuExampleSwitchesAtIndependent2004LichunBoundary() {
        // Source fixture: QM-SRC-0021, pdf:p67-p68 / K2E-W1-QM-0021-0019.
        // The source explicitly uses 2004-02-04 癸丑日 as its拆补 example:
        // after entering the Liqiu/Lichun-style actual transition boundary, retain the
        // nearest five-day head 己酉 for上元 classification, but use the NEW solar
        // term's ju system; for 立春 this produces 阳遁八局.
        //
        // Independent astronomical boundary: National Astronomical Observatory
        // of Japan, 2004 calendar almanac, gives 立春 at 2004-02-04 20:56 JST.
        // JST is UTC+9, so the same instant is 19:56 HKT/UTC+8.
        // This combines a source-specific post-transition expected ju with an
        // astronomy authority outside lunar-java, rather than letting Engine
        // choose both the boundary and the expected result.
        val before = QimenEngine.bySolar(
            2004, 2, 4, 19, 55,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )
        val after = QimenEngine.bySolar(
            2004, 2, 4, 19, 56,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )

        assertEquals("癸丑", before.dayGZ)
        assertEquals(before.dayGZ, after.dayGZ)
        assertEquals("上元", before.yuan)
        assertEquals(before.yuan, after.yuan)
        assertEquals("上元", after.yuanFutou)

        assertEquals("大寒", before.jieQi)
        assertEquals("立春", after.jieQi)
        assertEquals(1, before.yinYang)
        assertEquals(1, after.yinYang)
        assertEquals(3, before.ju, "one minute before independent Lichun boundary must remain 大寒上元阳3")
        assertEquals(8, after.ju, "QM-SRC-0021 post-transition example requires 立春上元阳8")
    }

    @Test
    fun futouSharedFiveDayHeadMatchesIndependent1990DahanFixture() {
        // Independent source cross-check: QM-SRC-0017 费秉勋《奇门遁甲新述》,
        // canonical SHA-256 f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1.
        // PDF p15-p17 (printed p6-p8), in the chapter on 超神接气和置闰, states that
        // each局 spans five days and its first day stem must be甲/己, then gives
        // 1990-01-27 壬辰 as belonging to the 己丑→癸巳 five-day group: 己丑 is
        // 大寒下元, hence 阳遁六局.
        //
        // Credit boundary: this corroborates the shared five-day甲/己 head substructure
        // and this dated 元/局 result. It does NOT identify the source's full置闰 method
        // with CHAI_BU_FUTOU, and does not validate either method globally.
        // The source gives a civil date, not a clock time; 12:00 below is only a safe
        // engine sampling time well inside the 大寒 segment, not a source-claimed时柱.
        val c = QimenEngine.bySolar(
            1990, 1, 27, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )

        assertEquals("壬辰", c.dayGZ)
        assertEquals("大寒", c.jieQi)
        assertEquals("下元", c.yuanFutou)
        assertEquals("下元", c.yuan)
        assertEquals(1, c.yinYang)
        assertEquals(6, c.ju)
        assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)

        // Negative comparator: the project's DAYCOUNT approximation must not be treated
        // as source-equivalent merely because it is the app default. On this dated source
        // example it must not reproduce the source's 阳遁六局 result by accident.
        val dayCount = QimenEngine.bySolar(
            1990, 1, 27, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_DAYCOUNT,
        )
        assertEquals("CHAI_BU_DAYCOUNT", dayCount.juMethodUsed)
        assertNotEquals(6, dayCount.ju)
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
