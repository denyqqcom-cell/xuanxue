package com.xuanxue.liuyao

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class LiuYaoEngineTest {

    @Test
    fun all64GuaPresent() {
        // 64 卦完整性：8 宫 × 8 卦，卦名全部解析，无重复
        val names = LiuYaoEngine.EIGHT_PALACES.flatMap { (p, list) ->
            list.map { (up, down) -> LiuYaoEngine.guaNameOf(p, up, down) }
        }
        println("LY1 64卦名: " + names.joinToString(" "))
        assertEquals(64, names.size)
        assertEquals(64, names.toSet().size, "卦名有重复")
        assertTrue(names.none { it.length < 2 })
        // 上下卦组合应覆盖全部 8×8 = 64 种组合（无重复=表正确）
        val combos = LiuYaoEngine.EIGHT_PALACES.flatMap { it.value }.toSet()
        assertEquals(64, combos.size, "上下卦组合应有 64 种且无重复")
        println("LY1 组合数=${combos.size} ✓ 八宫表覆盖完整")
    }

    @Test
    fun byNumbersKnown() {
        // 数字起卦：1,1,3 → 乾上乾下(乾为天)/动爻3（第3爻动）→ 变卦 天泽履
        val c = LiuYaoEngine.byNumbers(1, 1, 3, 2026, 8, 15, 10)
        println("LY2 数字起卦: 本卦=${c.benGua.name}(${c.benGua.up}上${c.benGua.down}下) 宫=${c.benGua.palace} 动爻=${c.dongYaoIndexes}")
        println("LY2 本卦六爻: " + c.benGua.yao.map { "${it.index}:${it.liuShen}${it.liuQin}${it.zhi}${if (it.isYang) "—" else "--"}${if (it.isShi) "[世]" else ""}${if (it.isYing) "[应]" else ""}${if (it.isDong) "[动]" else ""}" }.joinToString(" | "))
        assertEquals("乾为天", c.benGua.name)
        assertEquals(listOf(3), c.dongYaoIndexes)
        assertTrue(c.bianGua != null, "动爻应有变卦")
        println("LY2 变卦: ${c.bianGua?.name} (${c.bianGua?.up}上${c.bianGua?.down}下)")
        // 乾为天第三爻动 → 天泽履
        assertEquals("天泽履", c.bianGua?.name)
        // 世应在第六爻（乾为天本宫卦世6应3）
        assertEquals(6, c.benGua.yao.first { it.isShi }.index)
        assertEquals(3, c.benGua.yao.first { it.isYing }.index)
        // 乾为天三爻皆为阳
        assertTrue(c.benGua.yao.all { it.isYang })
        // 动爻3 为阴（变后）
        assertTrue(c.benGua.yao[2].isDong)
    }

    @Test
    fun bySolarKnown() {
        // 时间起卦验证：2026-08-15（农历丙午年七月初三?）任意结果仅验证结构
        val c = LiuYaoEngine.bySolar(2026, 8, 15, 10)
        println("LY3 时间起卦: ${c.benGua.name}(${c.benGua.up}上${c.benGua.down}下) ${c.benGua.palace}${c.benGua.palaceIndex} 动爻=${c.dongYaoIndexes} 日=${c.dayGZ} 时=${c.hourGZ}")
        assertTrue(c.benGua.yao.size == 6)
        assertTrue(c.benGua.yao.all { it.zhi.isNotEmpty() && it.liuQin.isNotEmpty() && it.liuShen.isNotEmpty() })
        // 六神按日干
        val ls = c.benGua.yao.map { it.liuShen }
        assertEquals(6, ls.toSet().size, "六神应六神齐全")
        println("LY3 六亲: " + c.benGua.yao.map { it.liuQin }.joinToString(","))
        println("LY3 纳甲: " + c.benGua.yao.map { it.gan + it.zhi }.joinToString(","))
    }

    @Test
    fun zhiWuXingKnown() {
        assertEquals("金", LiuYaoEngine.ZHI_WUXING["申"])
        assertEquals("水", LiuYaoEngine.ZHI_WUXING["子"])
        assertEquals("火", LiuYaoEngine.ZHI_WUXING["午"])
    }
}
