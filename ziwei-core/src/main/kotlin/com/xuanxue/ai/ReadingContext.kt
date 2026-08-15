package com.xuanxue.ai

/**
 * 求测/咨询上下文。
 *
 * 排盘结构本身不能替代现实问题。对奇门、六爻、大六壬这类事占模块，解释层必须知道
 * “问什么”和“已知现实条件”，否则只展示结构，不自动选择用神、类神，也不输出成败/应期。
 */
enum class QueryDomain(val label: String) {
    GENERAL("泛问"),
    CAREER("事业 / 工作"),
    WEALTH("财务 / 交易"),
    RELATIONSHIP("感情 / 人际"),
    STUDY("学业 / 考试"),
    HEALTH("健康"),
    TRAVEL("出行 / 迁移"),
    CONTRACT("合同 / 诉讼"),
    OTHER("其他"),
}

data class ReadingContext(
    val domain: QueryDomain = QueryDomain.GENERAL,
    val question: String = "",
    val knownFacts: String = "",
) {
    val normalizedQuestion: String get() = question.trim()
    val normalizedKnownFacts: String get() = knownFacts.trim()

    /**
     * 仅用于判断“是否给了足够具体的事体描述”，不是内容质量评分。
     */
    val isSpecific: Boolean get() = normalizedQuestion.length >= 4

    fun summary(): String = buildString {
        append("领域【${domain.label}】")
        if (normalizedQuestion.isNotEmpty()) append("；问题【$normalizedQuestion】")
        if (normalizedKnownFacts.isNotEmpty()) append("；已知条件【$normalizedKnownFacts】")
    }
}
