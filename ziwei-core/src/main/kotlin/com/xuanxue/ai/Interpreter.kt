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

/**
 * 产品层 provenance 与 EvidenceGrade 正交。
 *
 * EvidenceGrade 回答“这条内容在仓库里被核验到什么程度”；ProductProvenance 回答
 * “用户看到的这段内容是什么性质”。四类不得互相升格：计算字段不是来源规则，
 * 来源规则不是项目推论，项目推论也不能伪装成已经验证的现实结论。
 */
enum class ProductProvenance(val label: String, val description: String) {
    CHART_FACT(
        "盘面事实",
        "当前输入与引擎计算得到的可观察字段；只说明系统现在算出了什么，不等于术理或现实预测已经验证。",
    ),
    SOURCE_RULE(
        "来源规则",
        "可追溯到当前资料/规则登记的说法；只证明来源这样规定或项目按该规则实现，不自动等于现实真理。",
    ),
    PROJECT_INFERENCE(
        "项目推论",
        "项目基于现实条件、工程边界与规则关系作出的推演或方法判断；必须与来源原文分开。",
    ),
    UNVERIFIED_HYPOTHESIS(
        "未经验证假设",
        "仍有冲突、缺少黄金夹具或尚无前瞻结果支持的候选解释；不得包装成确定结论。",
    ),
}

/** 解读条目：标题 + 结论 + 依据 + 当前证据等级 + 产品 provenance。 */
data class ReadingItem(
    val title: String,
    val summary: String,
    val detail: String = "",
    val evidenceGrade: EvidenceGrade = EvidenceGrade.TRADITIONAL_HEURISTIC,
    val provenance: ProductProvenance = ProductProvenance.PROJECT_INFERENCE,
    val sourceIds: List<String> = emptyList(),
    val caveat: String = "",
)

/** 统一解读结果。 */
data class Reading(
    val toolName: String,
    val items: List<ReadingItem>,
    val overall: String = "",
    val caveats: List<String> = emptyList(),
    val contextSummary: String = "",
    val contextCaveat: String = "",
) {
    val text: String get() = buildString {
        if (overall.isNotEmpty()) appendLine("【总评】$overall")
        if (contextSummary.isNotEmpty()) {
            appendLine("【现实输入】$contextSummary")
            if (contextCaveat.isNotEmpty()) appendLine("注意：$contextCaveat")
        }
        caveats.forEach { appendLine("【边界】$it") }
        items.forEach { item ->
            appendLine("【${item.provenance.label}·${item.title}·${item.evidenceGrade.label}】${item.summary}")
            if (item.detail.isNotEmpty()) appendLine(item.detail)
            if (item.sourceIds.isNotEmpty()) appendLine("来源：${item.sourceIds.joinToString("、")}")
            if (item.caveat.isNotEmpty()) appendLine("注意：${item.caveat}")
        }
    }
}
