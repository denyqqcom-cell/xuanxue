package com.xuanxue.ai

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class EvidenceContractTest {

    @Test
    fun `qimen remains experimental despite weather method identity closure`() {
        val audit = MethodAuditRegistry.qimen
        assertEquals(MethodMaturity.EXPERIMENTAL, audit.maturity)
        assertTrue(audit.sourceIds.contains("handoff/qimen/HANDOFF_SUMMARY.md"))
        assertTrue(audit.sourceIds.contains("knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md"))
        assertTrue(audit.sourceIds.contains("knowledge/K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md"))
        assertTrue(audit.summary.contains("weather-v0.1"))
        assertTrue(audit.summary.contains("CHAI_BU_FUTOU"))
        assertTrue(audit.limitations.any { it.contains("不能当作完整九宫全局黄金盘") })
        assertTrue(audit.limitations.any { it.contains("DAYCOUNT") && it.contains("ZHI_RUN") && it.contains("不能迁移") })
        assertTrue(audit.limitations.any { it.contains("静态星门神") && it.contains("候选特征") && it.contains("竞争解释") })
        assertTrue(audit.limitations.any { it.contains("完整九宫仍属于实验实现") })
        assertTrue(audit.limitations.any { it.contains("现实预测有效性") })
    }

    @Test
    fun `every module exposes provenance and limitations`() {
        assertEquals(6, MethodAuditRegistry.all.size)
        MethodAuditRegistry.all.forEach { audit ->
            assertTrue(audit.sourceIds.isNotEmpty(), "${audit.id} must have source ids")
            assertTrue(audit.limitations.isNotEmpty(), "${audit.id} must have explicit limitations")
            assertTrue(audit.summary.isNotBlank(), "${audit.id} must have an audit summary")
        }
    }

    @Test
    fun `verified fixture label does not imply metaphysical truth`() {
        val ziwei = MethodAuditRegistry.ziwei
        assertEquals(MethodMaturity.IMPLEMENTATION_PARITY, ziwei.maturity)
        assertTrue(ziwei.summary.contains("不等于"))
        assertTrue(ziwei.limitations.any { it.contains("不是独立第三方真值") })
    }

    @Test
    fun `bazi audit explicitly rejects single-factor strength judgement`() {
        val bazi = MethodAuditRegistry.bazi
        assertTrue(bazi.limitations.any { it.contains("十二运") && it.contains("简化") })
    }
}
