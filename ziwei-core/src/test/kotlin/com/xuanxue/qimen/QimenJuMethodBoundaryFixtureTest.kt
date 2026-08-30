package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/**
 * Method-boundary fixtures kept separate from general Engine regressions.
 *
 * These tests combine source-specific JuMethod expectations with independent
 * astronomical timing. They validate method identity/implementation only and
 * grant no weather or metaphysical empirical credit.
 */
class QimenJuMethodBoundaryFixtureTest {

    @Test
    fun qm0021ChaibuExampleSwitchesAtFirstWholeMinuteAfterIndependent2004LichunInstant() {
        // Source method expectation:
        // QM-SRC-0021, pdf:p67-p68 / K2E-W1-QM-0021-0019 uses
        // 2004-02-04 癸丑日 to explain拆补: retain the nearest five-day head
        // 己酉 for上元 classification, but once actual立春交节 occurs use the
        // NEW solar term's ju system, hence 立春上元 -> 阳遁八局.
        //
        // Independent astronomy:
        // National Astronomical Observatory of Japan's 2004 almanac places
        // 立春 in the 20:56 JST minute = 19:56 HKT minute. Public second-level
        // ephemeris/calendar data place the instant at about 19:56:13 HKT.
        // QimenEngine.bySolar currently accepts whole minutes only, so
        // 19:56:00 is still pre-transition and 19:57:00 is the first
        // representable post-transition sample. Do not collapse an almanac
        // minute label into an artificial :00-second boundary.
        fun chartAt(totalMinutes: Int) = QimenEngine.bySolar(
            2004,
            2,
            4,
            totalMinutes / 60,
            totalMinutes % 60,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )

        val firstRepresentableLichunMinute = (1 until 24 * 60).firstOrNull { minute ->
            chartAt(minute).jieQi == "立春"
        }
        assertTrue(firstRepresentableLichunMinute != null)
        assertEquals(
            19 * 60 + 57,
            firstRepresentableLichunMinute,
            "minute-resolution Engine must switch at first whole-minute sample after the 19:56:xx HKT Lichun instant",
        )

        val before = chartAt(19 * 60 + 56)
        val after = chartAt(19 * 60 + 57)

        assertEquals("癸丑", before.dayGZ)
        assertEquals(before.dayGZ, after.dayGZ)
        assertEquals("上元", before.yuan)
        assertEquals(before.yuan, after.yuan)
        assertEquals("上元", after.yuanFutou)

        assertEquals("大寒", before.jieQi)
        assertEquals("立春", after.jieQi)
        assertEquals(1, before.yinYang)
        assertEquals(1, after.yinYang)
        assertEquals(3, before.ju, "19:56:00 HKT is still before the 19:56:xx transition: 大寒上元阳3")
        assertEquals(8, after.ju, "first representable post-transition minute must match QM-SRC-0021 立春上元阳8")
    }
}
