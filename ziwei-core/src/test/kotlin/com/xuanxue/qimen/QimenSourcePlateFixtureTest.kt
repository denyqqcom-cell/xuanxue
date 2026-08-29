package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals

/**
 * Source-grounded structural fixtures from QM-SRC-0021 / corroborating Wave1 source rules.
 *
 * They validate calendar/plate construction only. No weather outcome or case
 * verdict is imported, so these tests grant no predictive/empirical credit.
 */
class QimenSourcePlateFixtureTest {

    @Test
    fun five_day_futou_heads_map_to_source_yuan_classes() {
        val expected = mapOf(
            "甲子" to "上元", "甲午" to "上元", "己卯" to "上元", "己酉" to "上元",
            "甲寅" to "中元", "甲申" to "中元", "己巳" to "中元", "己亥" to "中元",
            "甲辰" to "下元", "甲戌" to "下元", "己丑" to "下元", "己未" to "下元",
        )
        expected.forEach { (futou, yuan) ->
            assertEquals(yuan, QimenEngine.yuanOfFutou(futou), "source futou class mismatch for $futou")
        }

        // 辛丑 is not a符头 day. The nearest preceding 甲/己 five-day head is 己亥,
        // therefore it belongs to中元. A ten-unit旬首 implementation would misclassify it.
        assertEquals("中元", QimenEngine.yuanOfFutou("辛丑"))
    }

    @Test
    fun qm0021_20040529_wuwu_futou_reproduces_source_star_and_heaven_stem_pairs() {
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

        // QM-SRC-0021 printed pp68-70: lock the weather-relevant pairing itself,
        // not merely the star positions. Gong.tianGan is the actual Kotlin Engine
        // output, so a mirror implementation can no longer substitute for this fixture.
        val expectedOuterPairs = mapOf(
            1 to ("天冲" to "壬"),
            2 to ("天心" to "丙"),
            3 to ("天英" to "己"),
            4 to ("天芮天禽" to "辛"),
            6 to ("天任" to "戊"),
            7 to ("天蓬" to "庚"),
            8 to ("天辅" to "癸"),
            9 to ("天柱" to "乙"),
        )
        val actualOuterPairs = c.gongs
            .filter { it.palace != 5 }
            .associate { it.palace to (it.tianXing to it.tianGan) }
        assertEquals(expectedOuterPairs, actualOuterPairs)
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
        assertNotEquals(
            sourceMethod.gongs.filter { it.palace != 5 }.associate { it.palace to (it.tianXing to it.tianGan) },
            dayCount.gongs.filter { it.palace != 5 }.associate { it.palace to (it.tianXing to it.tianGan) },
            "DAYCOUNT unexpectedly reproduced the source FUTOU star/heaven-stem pair map",
        )
    }
}
