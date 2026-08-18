package com.xuanxue.qimen.core.interpretation

/**
 * Provider-neutral prompt envelope. qimen-core 只负责把已经过 gate 的 evidence 转成明确的解释契约；
 * 不包含 API key、HTTP、厂商 SDK，也不嵌入现代教材长段落或断语库。
 */
data class AiPromptEnvelope(
    val systemInstruction: String,
    val userContent: String,
)

object AiPromptBuilder {
    private val requiredSections = listOf(
        "盘面事实",
        "取用依据",
        "情境推演",
        "反证条件",
        "置信边界",
    )

    fun build(request: AiInterpretationRequest): AiPromptEnvelope {
        require(request.question.isNotBlank()) { "question must not be blank" }
        require(request.evidence.facts.isNotEmpty()) { "evidence facts must not be empty" }

        val systemInstruction = buildString {
            appendLine("你是奇门遁甲的解释层，不是排盘器。")
            appendLine("只能使用 EVIDENCE 中给出的结构化事实；不得重新计算、补算、改写命盘，也不得把模型记忆当作盘面事实。")
            appendLine("若一个问题存在多种用神选择或流派差异，必须写明本次采用的取用依据，并指出会改变判断的替代选择。")
            appendLine("术数内容只能作为传统模型下的情境推演，不得写成科学事实、确定事件或保证性结果。")
            appendLine("不得虚构现实反馈；缺少现实条件时必须明确说明未知。")
            appendLine("输出必须依次包含以下五个标题：${requiredSections.joinToString(" / ")}。")
            appendLine("“盘面事实”只能复述 evidence；推断必须放在“情境推演”；反例或失效条件必须放在“反证条件”。")
        }.trim()

        val userContent = buildString {
            appendLine("QUESTION")
            appendLine(request.question.trim())
            appendLine()
            appendLine("EVIDENCE_SCHEMA ${request.evidence.schemaVersion}")
            appendLine("VERIFIED_SCOPE ${request.evidence.verifiedScope.name}")
            request.evidence.facts.forEach { fact ->
                appendLine("FACT\t${fact.id}\t${fact.label}\t${fact.value}\t${fact.provenance}")
            }
            appendLine()
            appendLine("CAVEATS")
            request.evidence.caveats.forEach { caveat -> appendLine("- $caveat") }
        }.trim()

        return AiPromptEnvelope(
            systemInstruction = systemInstruction,
            userContent = userContent,
        )
    }
}
