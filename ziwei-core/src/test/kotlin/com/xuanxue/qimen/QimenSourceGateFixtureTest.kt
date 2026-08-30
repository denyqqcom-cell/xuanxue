package com.xuanxue.qimen

import java.time.LocalDate
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

/**
 * Source-defined 值使门 rotation fixtures from QM-SRC-0017
 * 费秉勋《奇门遁甲新述》, canonical carrier SHA-256:
 * f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1.
 *
 * Visual source review:
 * - printed p24 (PDF p33): "直符随时干，直使随时宫"; 阳遁一局丙寅时，
 *   值使休门从甲子旬所在坎1顺推到震3。
 * - printed p25 (PDF p34): 阴遁九局戊戌时，值使开门从甲午辛所在乾6
 *   逆推第五个时辰，source explicitly counts "六、五、四、三、二"，落坤2。
 *
 * Credit boundary:
 * - these are source/implementation fixtures, not empirical validation;
 * - the searched civil dates are Engine harnesses only, not source provenance;
 * - this file tests only 值使门 target-palace counting/hosting, not global gate-board validity.
 */
class QimenSourceGateFixtureTest {

    @Test
    fun qm0017_yang1_bingyin_zhiShi_xiu_gate_lands_on_zhen3() {
        val c = findHarness(hour = 4) {
            it.yinYang == 1 &&
                it.ju == 1 &&
                it.hourGZ == "丙寅" &&
                it.xunShou == "甲子" &&
                it.zhiShi == "休门"
        }

        assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)
        assertEquals("休门", c.gongs.first { it.palace == 3 }.renMen)
    }

    @Test
    fun qm0017_yin9_wuxu_zhiShi_kai_gate_counts_center5_and_lands_on_kun2() {
        val c = findHarness(hour = 20) {
            it.yinYang == -1 &&
                it.ju == 9 &&
                it.hourGZ == "戊戌" &&
                it.xunShou == "甲午" &&
                it.zhiShi == "开门"
        }

        assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)
        // QM-SRC-0017 printed p25 explicitly counts 6 -> 5 -> 4 -> 3 -> 2.
        // Center 5 participates in the count; only a FINAL center target is hosted to 坤2.
        assertEquals("开门", c.gongs.first { it.palace == 2 }.renMen)
    }

    private fun findHarness(
        hour: Int,
        predicate: (QimenEngine.QimenChart) -> Boolean,
    ): QimenEngine.QimenChart {
        var date = LocalDate.of(2000, 1, 1)
        val end = LocalDate.of(2029, 12, 31)
        var harness: QimenEngine.QimenChart? = null

        while (!date.isAfter(end) && harness == null) {
            val candidate = QimenEngine.bySolar(
                date.year,
                date.monthValue,
                date.dayOfMonth,
                hour,
                0,
                QimenEngine.JuMethod.CHAI_BU_FUTOU,
            )
            if (predicate(candidate)) harness = candidate
            date = date.plusDays(1)
        }

        return assertNotNull(harness, "no Engine harness found for QM-SRC-0017 source-defined gate state")
    }
}
