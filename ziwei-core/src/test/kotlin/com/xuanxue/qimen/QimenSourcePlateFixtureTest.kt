package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals

/**
 * Chart-only fixture from QM-SRC-0021, algorithm chapter around printed pp.68-70.
 *
 * Source states for 2004-05-29 戊午时:
 * - 甲申年 / 己巳月 / 戊申日 / 戊午时
 * - 阳遁八局
 * - 甲寅旬, 值符天辅
 * - 天辅随旬首甲寅癸移到艮8，其余九星按固定相对次序同步移动
 *
 * This fixture validates plate construction only. It imports no weather outcome
 * and grants no predictive/empirical credit.
 */
class QimenSourcePlateFixtureTest {

    @Test
    fun qm0021_20040529_wuwu_futou_reproduces_source_star_plate() {
        val c = QimenEngine.bySolar(
            2004, 5, 29, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )

        assertEquals("甲申", c.yearGZ)
        assertEquals("己巳", c.monthGZ)
        assertEquals("戊申", c.dayGZ)
        assertEquals("戊午", c.hourGZ)
        assertEquals("小满", c.jieQi)
        assertEquals(1, c.yinYang)
        assertEquals("下元", c.yuan)
        assertEquals(8, c.ju)
        assertEquals("CHAI_BU_FUTOU", c.juMethodUsed)
        assertEquals("甲寅", c.xunShou)
        assertEquals("癸", c.dunGan)
        assertEquals("天辅", c.zhiFu)

        val stars = c.gongs.associate { it.palace to it.tianXing }
        val expectedOuterStars = mapOf(
            1 to "天冲",
            2 to "天心",
            3 to "天英",
            4 to "天芮天禽",
            6 to "天任",
            7 to "天蓬",
            8 to "天辅",
            9 to "天柱",
        )
        expectedOuterStars.forEach { (palace, expected) ->
            assertEquals(expected, stars[palace], "source plate star mismatch at palace $palace")
        }
    }

    @Test
    fun daycount_is_not_silently_substituted_for_this_source_futou_fixture() {
        val sourceMethod = QimenEngine.bySolar(
            2004, 5, 29, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )
        val dayCount = QimenEngine.bySolar(
            2004, 5, 29, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_DAYCOUNT,
        )

        assertEquals(8, sourceMethod.ju)
        assertNotEquals(
            sourceMethod.ju,
            dayCount.ju,
            "DAYCOUNT unexpectedly became interchangeable with the source's FUTOU method; review method identity",
        )
    }
}
