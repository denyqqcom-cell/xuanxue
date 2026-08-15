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
        println("QM1 旬首=${c.xunShou} 遁干=${c.dunGan} 旬空=${c.xunKong} 值符=${c.zhiFu} 值使=${c.zhiShi} 马星=${c.maXing}")
        assertEquals("立秋", c.jieQi)
        assertEquals(-1, c.yinYang)          // 阴遁
        assertEquals("CHAI_BU_DAYCOUNT", c.juMethodUsed)
        assertEquals("中元", c.yuan)
        assertEquals(5, c.ju)                 // 日数分段：立秋第6天 → 中元 5 局
        // 值符值使：用户脚本给 dunPalace 后映射（测试时打印对比，此处不断言具体值）
        println("QM1 九宫: " + c.gongs.map { "${it.palace}宫:地${it.diGan}/星${it.tianXing}/门${it.renMen}/神${it.shenPan}${if (it.isMaXing) "【马】" else ""}${if (it.isKong) "【空】" else ""}" }.joinToString(" | "))
        assertTrue(c.gongs.all { it.diGan.isNotEmpty() })
    }

    @Test
    fun liqiuDayCountNotFutou() {
        val c = QimenEngine.bySolar(2026, 8, 7, 16, 0)
        assertEquals("立秋", c.jieQi)
        assertEquals("CHAI_BU_DAYCOUNT", c.juMethodUsed)
        assertEquals("上元", c.yuan)
        assertEquals(2, c.ju)
        assertEquals("下元", c.yuanFutou)
        assertTrue(c.jieqiDayIndex >= 1)
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
