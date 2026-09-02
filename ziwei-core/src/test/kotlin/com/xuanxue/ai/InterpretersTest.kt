package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.ziwei.core.ZiweiAstro
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class InterpretersTest {

    @Test
    fun baziReading() {
        val c = BaziEngine.bySolar(1990, 5, 20, 12, 30, "男")
        val r = XuanxueAI.bazi(c)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("日主"))
        assertTrue(r.text.contains("五行显示权重"))
        assertTrue(r.text.contains("不能直接等同于旺衰"))
        assertFalse(r.text.contains("喜财官食伤"))
        assertFalse(r.text.contains("喜印比"))
    }

    @Test
    fun ziweiReading() {
        val a = ZiweiAstro.bySolar("1990-05-20", 6, "male")
        val r = XuanxueAI.ziwei(a)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("实现一致"))
        assertTrue(r.text.contains("不代表"))
    }

    @Test
    fun qimenReadingKeepsDayCountMethodIdentityAndBoundaries() {
        val c = QimenEngine.bySolar(
            2026, 8, 12, 15, 37,
            QimenEngine.JuMethod.CHAI_BU_DAYCOUNT,
        )
        val r = XuanxueAI.qimen(c)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("CHAI_BU_DAYCOUNT"))
        assertTrue(r.text.contains("工程为兼容既有行为保留的日数分段近似"))
        assertTrue(r.text.contains("不能借其他 JuMethod 的来源信用"))
        assertTrue(r.text.contains("九宫实验边界"))
        assertTrue(r.text.contains("全局黄金盘"))
        assertFalse(r.text.contains("八门吉凶"))
        assertFalse(r.text.contains("利出行变动"))
        assertFalse(r.text.contains("暂缓待填实"))
    }

    @Test
    fun qimenReadingKeepsFutouMethodCreditBoundedAndContextFirst() {
        val c = QimenEngine.bySolar(
            1990, 1, 27, 12, 0,
            QimenEngine.JuMethod.CHAI_BU_FUTOU,
        )
        val r = XuanxueAI.qimen(c)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("CHAI_BU_FUTOU"))
        assertTrue(r.text.contains("甲/己五日符头"))
        assertTrue(r.text.contains("独立天文边界回归"))
        assertTrue(r.text.contains("只关闭该候选方法身份"))
        assertTrue(r.text.contains("不等于 DAYCOUNT、ZHI_RUN"))
        assertTrue(r.text.contains("更不等于现实预测有效"))
        assertTrue(r.text.contains("书本象意、星门神标签与格局命中只属于候选语义"))
        assertTrue(r.text.contains("具体事体、角色/取用、时间尺度与现实约束"))
        assertTrue(r.text.contains("竞争解释或弃权路径"))
        assertFalse(r.text.contains("已经验证的传统唯一拆补法"))
        assertFalse(r.text.contains("必然"))
    }

    @Test
    fun liuyaoReading() {
        val c = LiuYaoEngine.byNumbers(1, 1, 3, 2026, 8, 15, 10)
        val r = XuanxueAI.liuyao(c)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("世爻"))
        assertTrue(r.text.contains("不能只见六亲就自动下结论"))
    }

    @Test
    fun liurenReading() {
        val c = LiuRenEngine.bySolar(1949, 10, 1, 0, 0)
        val r = XuanxueAI.liuren(c)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("三传"))
        assertTrue(r.text.contains("不单独承担现实吉凶结论"))
    }

    @Test
    fun huangliReading() {
        val l = com.nlf.calendar.Solar.fromYmd(2026, 8, 15).lunar
        val r = XuanxueAI.huangli(l)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("传统历法/民俗"))
    }

    @Test
    fun toolsRegistered() {
        assertEquals(6, XuanxueAI.tools.size)
        assertTrue(XuanxueAI.tools.all { it["name"] != null && it["description"] != null })
    }
}
