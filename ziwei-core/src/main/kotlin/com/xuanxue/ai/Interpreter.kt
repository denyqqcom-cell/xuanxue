package com.xuanxue.ai

/**
 * 玄学解读引擎 — 离线规则解读（确定性，无网络）。
 * 内容原则：星曜/格局/课型含义均为公开传统释义（公有领域常识性描述），
 * 不引用任何商业 App 的文案。
 *
 * 架构预留：本接口将来可扩展为"工具注册"（BYOK 云端 AI 解读时，
 * 每个解读器即一个 function-calling 工具）。
 */
interface Interpreter<T> {
    val toolName: String          // 将来注册为工具名
    val toolDesc: String          // 工具描述（JSON schema 用）
    fun interpret(chart: T): List<String>  // 返回解读条目（每条独立成段）
}

fun sourcedItem(
    layer: String,
    ruleId: String,
    summary: String,
    source: String,
    confidence: String,
    detail: String = "",
): ReadingItem = ReadingItem(
    title = "$layer · $ruleId",
    summary = summary,
    detail = detail,
    layer = layer,
    ruleId = ruleId,
    source = source,
    confidence = confidence,
)

const val LAYER_ALG = "算法"
const val LAYER_SCHOOL = "门派"
const val LAYER_EXP = "经验"

/** 解读条目：标题 + 结论 + 依据。layer/ruleId 供带来源的规则用。 */
data class ReadingItem(
    val title: String,
    val summary: String,
    val detail: String = "",
    val layer: String = "",
    val ruleId: String = "",
    val source: String = "",
    val confidence: String = "",
)

/** 统一解读结果 */
data class Reading(
    val toolName: String,
    val items: List<ReadingItem>,
    val overall: String = "",     // 总评
) {
    val text: String get() = buildString {
        if (overall.isNotEmpty()) appendLine("【总评】$overall")
        items.forEach { it ->
            appendLine("【${it.title}】${it.summary}")
            if (it.detail.isNotEmpty()) appendLine(it.detail)
            if (it.source.isNotEmpty()) {
                append("来源 ${it.source}")
                if (it.confidence.isNotEmpty()) append(" 信心 ${it.confidence}")
                appendLine()
            }
        }
    }
}
