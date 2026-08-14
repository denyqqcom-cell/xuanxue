package com.xuanxue.ai

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class EvidenceContractTest {

    @Test
    fun `qimen full board must remain experimental until golden boards exist`() {
        val audit = MethodAuditRegistry.qimen
        assertEquals(MethodMaturity.EXPERIMENTAL, audit.maturity)
        assertTrue(audit.sourceIds.contains("handoff/qimen/HANDOFF_SUMMARY.md"))
        assertTrue(audit.limitations.any { it.contains("完整九宫黄金盘数量为 0") })
        assertTrue(audit.limitations.any { it.contains("实验实现") })
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
