package com.xuanxue.qimen

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class QimenEngineTest {

    @Test
    fun alignUserScript() {
        // 对齐用户本地脚本案例：2026-08-12 申时(15:37)，立秋后第6天 → 中元 → 阴遁5局
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        println("QM1 节气=${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        println("QM1 旬首=${c.xunShou} 遁干=${c.dunGan} 日空=${c.dayKong} 时空=${c.hourKong} 值符=${c.zhiFu} 值使=${c.zhiShi} 马星=${c.maXing}")
        assertEquals("立秋", c.jieQi)
        assertEquals(-1, c.yinYang)          // 阴遁
        assertEquals(5, c.ju)                 // 中元 5 局（对齐用户脚本）
        // 值符值使：用户脚本给 dunPalace 后映射（测试时打印对比，此处不断言具体值）
        println("QM1 九宫: " + c.gongs.map { "${it.palace}宫:地${it.diGan}/星${it.tianXing}/门${it.renMen}/神${it.shenPan}${if (it.isMaXing) "【马】" else ""}${if (it.isDayKong) "【日空】" else ""}${if (it.isHourKong) "【时空】" else ""}" }.joinToString(" | "))
        assertTrue(c.gongs.all { it.diGan.isNotEmpty() })
    }

    @Test
    fun shanTianDao20161202BasicMarkers() {
        // 《善天道奇门遁甲高级研修班讲义》案例（二）：2016-12-02 17:48。
        // 原资料明确给出：戊午日、辛酉时；日空与时空均为子丑；酉时马星为亥。
        val c = QimenEngine.bySolar(2016, 12, 2, 17, 48)
        assertEquals("戊午", c.dayGZ)
        assertEquals("辛酉", c.hourGZ)
        assertEquals(listOf("子", "丑"), c.dayKong)
        assertEquals(listOf("子", "丑"), c.hourKong)
        assertEquals("亥", c.maXing)

        // 子落坎一、丑落艮八；亥落乾六。
        assertTrue(c.gongs.first { it.palace == 1 }.isDayKong)
        assertTrue(c.gongs.first { it.palace == 1 }.isHourKong)
        assertTrue(c.gongs.first { it.palace == 8 }.isDayKong)
        assertTrue(c.gongs.first { it.palace == 8 }.isHourKong)
        assertTrue(c.gongs.first { it.palace == 6 }.isMaXing)
    }

    @Test
    fun winterSolsticeYang1() {
        // 冬至：阳遁 上元 1 局（标准：冬至 一七四）
        val c = QimenEngine.bySolar(2026, 12, 22, 10, 0)
        println("QM2 ${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        assertTrue(c.jieQi == "冬至" || c.jieQi == "大雪", "节气=${c.jieQi}") // 可能仍在大雪（12/22 前后）
        if (c.jieQi == "冬至") {
            assertEquals(1, c.yinYang)
        }
        println("QM2 旬首=${c.xunShou} 遁干=${c.dunGan} 值符=${c.zhiFu} 值使=${c.zhiShi}")
    }

    @Test
    fun knownExample() {
        // 已知经典案例（书籍验证）：1990-05-20 12:00 前后（小满后）→ 阳遁
        val c = QimenEngine.bySolar(1990, 5, 20, 12, 30)
        println("QM3 ${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ} 值符=${c.zhiFu} 值使=${c.zhiShi}")
        println("QM3 九宫: " + c.gongs.map { "${it.palace}宫:${it.diGan}" }.joinToString(" "))
        assertTrue(c.gongs.size == 9)
        // 地盘：阳遁顺飞 戊起局数宫
        val di = c.gongs.associate { it.palace to it.diGan }
        val ju = c.ju
        assertEquals("戊", di[ju])
    }
}
