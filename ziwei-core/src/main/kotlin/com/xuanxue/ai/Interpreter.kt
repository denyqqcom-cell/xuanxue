package com.xuanxue.ai

/**
 * 玄学解读引擎 — 离线规则解读（确定性，无网络）。
 *
 * 这里的“确定性”只表示同一输入会得到同一输出，不表示术数判断已经被科学验证。
 * 所有用户可见解读必须区分：用户输入、实现核验、来源可追溯、传统启发式、实验性能力。
 */
interface Interpreter<T> {
    val toolName: String
    val toolDesc: String
    fun interpret(chart: T): List<String>
}

/**
 * 证据等级只描述“这条信息在当前仓库里来自哪里/被核验到什么程度”，不是吉凶强弱。
 */
enum class EvidenceGrade(val label: String) {
    USER_CONTEXT("用户输入"),
    VERIFIED_FIXTURE("夹具核验"),
    SOURCE_DERIVED("来源可追溯"),
    TRADITIONAL_HEURISTIC("传统启发式"),
    EXPERIMENTAL("实验"),
}

/** 解读条目：标题 + 结论 + 依据 + 当前证据等级。 */
data class ReadingItem(
    val title: String,
    val summary: String,
    val detail: String = "",
    val evidenceGrade: EvidenceGrade = EvidenceGrade.TRADITIONAL_HEURISTIC,
    val sourceIds: List<String> = emptyList(),
    val caveat: String = "",
)

/** 统一解读结果。 */
data class Reading(
    val toolName: String,
    val items: List<ReadingItem>,
    val overall: String = "",
    val caveats: List<String> = emptyList(),
) {
    val text: String get() = buildString {
        if (overall.isNotEmpty()) appendLine("【总评】$overall")
        caveats.forEach { appendLine("【边界】$it") }
        items.forEach { item ->
            appendLine("【${item.title}·${item.evidenceGrade.label}】${item.summary}")
            if (item.detail.isNotEmpty()) appendLine(item.detail)
            if (item.sourceIds.isNotEmpty()) appendLine("来源：${item.sourceIds.joinToString("、")}")
            if (item.caveat.isNotEmpty()) appendLine("注意：${item.caveat}")
        }
    }
}
