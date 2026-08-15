package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class ReadingContextTest {

    @Test
    fun `short question is not treated as a specific case`() {
        assertFalse(ReadingContext(question = "工作").isSpecific)
        assertTrue(ReadingContext(question = "未来三个月是否适合换工作").isSpecific)
    }

    @Test
    fun `qimen without question stays at structure layer`() {
        val chart = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val reading = XuanxueAI.qimen(chart)
        assertTrue(reading.caveats.any { it.contains("尚未提供具体事体") })
        assertTrue(reading.items.none { it.evidenceGrade == EvidenceGrade.USER_CONTEXT })
    }

    @Test
    fun `user context is visible but does not upgrade method evidence`() {
        val chart = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val reading = XuanxueAI.qimen(
            chart,
            ReadingContext(
                domain = QueryDomain.CAREER,
                question = "未来三个月是否适合换工作",
                knownFacts = "已有新 offer，但需要异地",
            ),
        )

        assertEquals(EvidenceGrade.USER_CONTEXT, reading.items.first().evidenceGrade)
        assertTrue(reading.items.first().summary.contains("事业 / 工作"))
        assertTrue(reading.items.drop(1).all { it.evidenceGrade != EvidenceGrade.USER_CONTEXT })
        assertTrue(reading.caveats.any { it.contains("实验实现") })
    }
}
