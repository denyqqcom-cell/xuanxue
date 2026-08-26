package com.xuanxue.ai

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class LocalModelInferenceTest {
    @Test
    fun promptKeepsChartImmutableAndPreservesEvidenceBoundary() {
        val context = ReadingContext(
            domain = QueryDomain.CAREER,
            question = "这次岗位调整应如何判断？",
            knownFacts = "已经收到两个岗位方案",
        )
        val reading = Reading(
            toolName = "qimen",
            overall = "当前只允许受控情境推演。",
            caveats = listOf("完整九宫仍按实验实现管理。"),
            items = listOf(
                ReadingItem(
                    title = "事体上下文",
                    summary = context.summary(),
                    evidenceGrade = EvidenceGrade.USER_CONTEXT,
                ),
                ReadingItem(
                    title = "奇门",
                    summary = "旬法信息属于当前可工程化层。",
                    evidenceGrade = EvidenceGrade.SOURCE_DERIVED,
                    sourceIds = listOf("QM-SRC-0013"),
                ),
            ),
        )

        val request = LocalModelPromptCompiler.forReading(reading, context)

        assertEquals("xuanxue-local-inference-v1", request.packet.schemaVersion)
        assertEquals(context, request.packet.context)
        assertEquals(reading, request.packet.reading)
        assertTrue(request.prompt.contains("不得重新计算、纠正或改写排盘"))
        assertTrue(request.prompt.contains("USER_CONTEXT"))
        assertTrue(request.prompt.contains("用户输入"))
        assertTrue(request.prompt.contains("QM-SRC-0013"))
        assertTrue(request.prompt.contains("竞争解释与反证/敏感点"))
        assertTrue(request.prompt.contains("不要伪造来源 ID"))
    }

    @Test
    fun providerContractDoesNotRequireAndroidOrNetworkTypes() {
        val descriptor = LocalModelDescriptor(
            modelId = "local-test-model",
            displayName = "Local Test Model",
            backend = "fake",
        )
        val provider = object : LocalModelProvider {
            override val descriptor = descriptor
            override fun availability() = LocalModelAvailability.READY
            override fun generate(request: LocalModelRequest): LocalModelResult =
                LocalModelResult.Success("ok", descriptor)
        }

        assertEquals(LocalModelAvailability.READY, provider.availability())
        val result = provider.generate(
            LocalModelPromptCompiler.forReading(
                Reading(toolName = "qimen", items = emptyList()),
            ),
        )
        assertTrue(result is LocalModelResult.Success)
        val success = result as LocalModelResult.Success
        assertEquals("ok", success.text)
    }
}
