package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import com.xuanxue.qimen.core.interpretation.AiPromptBuilder
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class AiPromptBuilderTest {
    private fun resolvedRequest() = AiInterpretationGate.prepare(
        chart = QimenEngine.cast(
            QimenRequest(
                instantEpochMs = LocalDateTime.of(1995, 6, 11, 9, 30)
                    .atZone(ZoneId.of("Asia/Shanghai"))
                    .toInstant()
                    .toEpochMilli(),
            ),
        ).getOrThrow(),
        question = "这次合作是否适合继续推进？",
        policy = AiInterpretationPolicy(
            executionMode = AiExecutionMode.LOCAL_MODEL,
            scope = AiInterpretationScope.FULL_PLATE,
        ),
    ).getOrThrow()

    @Test
    fun promptRequiresSeparatedFactsReasoningCounterevidenceAndBoundaries() {
        val prompt = AiPromptBuilder.build(resolvedRequest())

        listOf("盘面事实", "取用依据", "情境推演", "反证条件", "置信边界").forEach { section ->
            assertTrue(prompt.systemInstruction.contains(section), "missing required section: $section")
        }
        assertTrue(prompt.systemInstruction.contains("不是排盘器"))
        assertTrue(prompt.systemInstruction.contains("不得重新计算、补算、改写命盘"))
        assertTrue(prompt.systemInstruction.contains("不得虚构现实反馈"))
        assertTrue(prompt.systemInstruction.contains("多种用神选择或流派差异"))
    }

    @Test
    fun promptCarriesOnlyPreparedEvidenceAndQuestionInProviderNeutralFormat() {
        val request = resolvedRequest()
        val prompt = AiPromptBuilder.build(request)

        assertTrue(prompt.userContent.contains("QUESTION"))
        assertTrue(prompt.userContent.contains(request.question))
        assertTrue(prompt.userContent.contains("VERIFIED_SCOPE FULL_PLATE"))
        assertTrue(prompt.userContent.contains("FACT\tday_pillar"))
        assertTrue(prompt.userContent.contains("FACT\tsky_plate"))
        assertTrue(prompt.userContent.contains("FACT\thuman_plate"))
        assertTrue(prompt.userContent.contains("FACT\tspirit_plate"))
        assertTrue(prompt.userContent.contains("ENGINE_VERIFIED"))

        assertFalse(prompt.systemInstruction.contains("OpenAI"))
        assertFalse(prompt.systemInstruction.contains("Claude"))
        assertFalse(prompt.systemInstruction.contains("DeepSeek"))
        assertFalse(prompt.userContent.contains("api_key", ignoreCase = true))
        assertFalse(prompt.userContent.contains("authorization", ignoreCase = true))
    }
}
