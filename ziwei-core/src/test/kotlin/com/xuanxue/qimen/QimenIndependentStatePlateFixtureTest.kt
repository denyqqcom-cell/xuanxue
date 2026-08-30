package com.xuanxue.qimen

import java.time.LocalDate
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

/**
 * Independent state-defined plate fixture from QM-SRC-0017 费秉勋《奇门遁甲新述》.
 *
 * Credit boundary:
 * - this is NOT a dated source fixture; the book defines the Qimen state directly;
 * - the civil date searched below is only an Engine harness that instantiates the same state;
 * - expected palace/star/heaven-stem pairs were frozen from the source before Engine comparison;
 * - no source event result, divination verdict, or empirical claim is used.
 */
class QimenIndependentStatePlateFixtureTest {

    @Test
    fun qm0017_yang1_bingyin_state_matches_source_derived_star_heaven_stem_pairs() {
        // QM-SRC-0017 printed p18: 阳遁一局活盘图 binds the movable heaven-plate
        // star layer to its 甲/六仪/三奇 carrier in each sector.
        // printed p24: for 阳遁一局丙寅时, 丙寅 belongs to 甲子旬, 值符天蓬/值使休门;
        // 时干丙 is at 艮8 on the earth plate, therefore the heaven plate rotates so
        // 天蓬 moves from 坎1 to 艮8. The remaining star+carrier pairs rotate rigidly
        // with that same source-local plate movement.
        //
        // This expected map is source-derived and intentionally written before locating
        // any civil-date Engine harness. If Engine output differs, preserve the conflict;
        // do not edit this map merely to make the test green.
        val expectedOuterPairs = mapOf(
            1 to ("天心" to "癸"),
            2 to ("天英" to "乙"),
            3 to ("天任" to "丙"),
            4 to ("天冲" to "庚"),
            6 to ("天柱" to "丁"),
            7 to ("天芮天禽" to "己"),
            8 to ("天蓬" to "戊"),
            9 to ("天辅" to "辛"),
        )

        // Gate A2 tests state -> plate, not calendar -> state. Search a bounded civil
        // interval only to instantiate the exact source state through the public Engine API.
        // The discovered date is test harness metadata and MUST NOT be promoted to source provenance.
        var date = LocalDate.of(2000, 1, 1)
        val end = LocalDate.of(2029, 12, 31)
        var harness: QimenEngine.QimenChart? = null

        while (!date.isAfter(end) && harness == null) {
            val c = QimenEngine.bySolar(
                date.year,
                date.monthValue,
                date.dayOfMonth,
                4,
                0,
                QimenEngine.JuMethod.CHAI_BU_FUTOU,
            )
            if (
                c.yinYang == 1 &&
                c.ju == 1 &&
                c.hourGZ == "丙寅" &&
                c.xunShou == "甲子" &&
                c.zhiFu == "天蓬"
            ) {
                harness = c
            }
            date = date.plusDays(1)
        }

        val c = assertNotNull(harness, "no Engine harness found for source state 阳遁一局/甲子旬/丙寅时")
        assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)
        assertEquals(1, c.yinYang)
        assertEquals(1, c.ju)
        assertEquals("丙寅", c.hourGZ)
        assertEquals("甲子", c.xunShou)
        assertEquals("天蓬", c.zhiFu)

        val actualOuterPairs = c.gongs
            .filter { it.palace != 5 }
            .associate { it.palace to (it.tianXing to it.tianGan) }

        assertEquals(expectedOuterPairs, actualOuterPairs)
    }
}
