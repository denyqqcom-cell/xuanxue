package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/**
 * Cross-source visual implementation witnesses.
 *
 * QM-SRC-0021 was independently re-opened at the canonical PDF hash and visually
 * inspected at PDF p54, p57 and p69-p72 before these anchors were written.
 * The test measures implementation/source agreement only; it gives no prediction credit.
 */
class QimenCrossSourceVisualTest {

    @Test
    fun qm0021Yang8WuWuWorkedPlateMatchesSelectedVisualAnchors() {
        val c = QimenEngine.bySolar(
            2004, 5, 29, 12, 0,
            QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22,
        )
        val g = c.gongs.associateBy { it.palace }

        // Source setup witness: QM-SRC-0021 PDF p70-p72.
        assertEquals("甲申", c.yearGZ)
        assertEquals("己巳", c.monthGZ)
        assertEquals("戊申", c.dayGZ)
        assertEquals("戊午", c.hourGZ)
        assertEquals(1, c.yinYang)
        assertEquals(8, c.ju)
        assertEquals("甲寅", c.xunShou)
        assertEquals("癸", c.dunGan)
        assertEquals("天辅", c.zhiFu)
        assertEquals("杜门", c.zhiShi)
        assertTrue(c.implementationWarnings.isEmpty())

        // Sparse non-substantial anchors selected from the visually reviewed worked plate.
        assertEquals("天辅", g.getValue(8).tianXing)
        assertEquals("天芮/天禽", g.getValue(4).tianXing)
        assertEquals("杜门", g.getValue(8).renMen)
        assertEquals("死门", g.getValue(4).renMen)
        assertEquals("值符", g.getValue(8).shenPan)
        assertEquals("腾蛇", g.getValue(3).shenPan)
        assertEquals("九天", g.getValue(1).shenPan)
    }
}
