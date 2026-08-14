package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiPromptBuilder

/**
 * App 层的 provider-neutral 准备器：把已经通过 core gate 的请求转为可审阅/可复制 prompt。
 * 这里仍不联网，也不保存任何 provider credential。
 */
data class QimenPreparedPrompt(
    val systemInstruction: String,
    val userContent: String,
)

object QimenAiUiPreparation {
    fun preparePrompt(
        chart: QimenChart,
        question: String,
        policy: AiInterpretationPolicy,
    ): Result<QimenPreparedPrompt> = AiInterpretationGate.prepare(chart, question, policy).map { request ->
        val envelope = AiPromptBuilder.build(request)
        QimenPreparedPrompt(
            systemInstruction = envelope.systemInstruction,
            userContent = envelope.userContent,
        )
    }
}
