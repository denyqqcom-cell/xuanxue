package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ProductProvenanceContractTest {

    @Test
    fun `analysis provenance is exactly four non-overlapping product classes`() {
        assertEquals(
            listOf("盘面事实", "来源规则", "项目推论", "未经验证假设"),
            ProductProvenance.entries.map { it.label },
        )
    }

    @Test
    fun `qimen keeps user reality outside provenance and exposes all four classes`() {
        val chart = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val reading = XuanxueAI.qimen(
            chart,
            ReadingContext(
                domain = QueryDomain.CAREER,
                question = "未来三个月是否适合换工作",
                knownFacts = "已有新 offer，需要异地；当前岗位稳定",
            ),
        )

        assertTrue(reading.contextSummary.isNotBlank())
        assertTrue(reading.items.none { it.evidenceGrade == EvidenceGrade.USER_CONTEXT })

        val classes = reading.items.map { it.provenance }.toSet()
        assertTrue(ProductProvenance.CHART_FACT in classes)
        assertTrue(ProductProvenance.SOURCE_RULE in classes)
        assertTrue(ProductProvenance.PROJECT_INFERENCE in classes)
        assertTrue(ProductProvenance.UNVERIFIED_HYPOTHESIS in classes)
    }
}
