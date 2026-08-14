package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class QimenAiUiPreparationTest {
    private fun sourceChart() = QimenEngine.cast(
        QimenCastInput.toRequest("1995-06-11", "09:30").getOrThrow(),
    ).getOrThrow()

    @Test
    fun `remote prepared prompt is built only from the exact consented preview`() {
        val chart = sourceChart()
        val question = "这件工作的主要矛盾和可反证条件是什么？"
        val preview = AiInterpretationGate.preview(chart, question, AiInterpretationScope.FULL_PLATE).getOrThrow()

        val prompt = QimenAiUiPreparation.preparePrompt(
            chart = chart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.FULL_PLATE,
                explicitRemoteConsent = true,
                remoteConsentFingerprint = preview.payloadFingerprint,
            ),
        ).getOrThrow()

        assertTrue(prompt.systemInstruction.contains("盘面事实"))
        assertTrue(prompt.systemInstruction.contains("反证条件"))
        assertTrue(prompt.systemInstruction.contains("不得重新计算"))
        assertTrue(prompt.userContent.contains(question))
        assertTrue(prompt.userContent.contains("FACT\tsky_plate"))
        assertTrue(prompt.userContent.contains("FACT\thuman_plate"))
        assertTrue(prompt.userContent.contains("FACT\tspirit_plate"))
        assertFalse(prompt.userContent.contains("api_key", ignoreCase = true))
        assertFalse(prompt.userContent.contains("Authorization", ignoreCase = true))
    }

    @Test
    fun `local mode can prepare the same evidence without remote consent`() {
        val prompt = QimenAiUiPreparation.preparePrompt(
            chart = sourceChart(),
            question = "只按盘面事实分析",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.LOCAL_MODEL,
                scope = AiInterpretationScope.FULL_PLATE,
            ),
        ).getOrThrow()

        assertTrue(prompt.userContent.contains("VERIFIED_SCOPE FULL_PLATE"))
        assertTrue(prompt.userContent.contains("ENGINE_VERIFIED"))
    }
}
