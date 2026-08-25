package com.xuanxue.ai

/**
 * 手机本地语言模型的 provider-neutral 合同。
 *
 * 本接口只允许模型消费已经由确定性排盘/受控解释层生成的输入包；模型不得反向修改排盘、
 * Evidence 等级、来源归属或用户输入。Android 侧具体使用哪一种 Gemma/LiteRT/IPC 后端，
 * 由 app 模块的 adapter 决定，core 不绑定任何移动端推理 SDK。
 */
enum class LocalModelAvailability {
    UNAVAILABLE,
    READY,
    BUSY,
    ERROR,
}

data class LocalModelDescriptor(
    val modelId: String,
    val displayName: String,
    val backend: String,
    val localOnly: Boolean = true,
    val metadata: Map<String, String> = emptyMap(),
)

data class LocalInferencePacket(
    val schemaVersion: String = "xuanxue-local-inference-v1",
    val toolName: String,
    val context: ReadingContext,
    val reading: Reading,
    val constraints: List<String>,
)

data class LocalModelRequest(
    val packet: LocalInferencePacket,
    val prompt: String,
)

sealed class LocalModelResult {
    data class Success(
        val text: String,
        val model: LocalModelDescriptor,
    ) : LocalModelResult()

    data class Unavailable(val reason: String) : LocalModelResult()
    data class Failure(val reason: String) : LocalModelResult()
}

interface LocalModelProvider {
    val descriptor: LocalModelDescriptor
    fun availability(): LocalModelAvailability
    fun generate(request: LocalModelRequest): LocalModelResult
}

/**
 * 把确定性 Reading 编译成小而受控的本地模型输入。
 *
 * 2B 级本地模型首先承担“受控语言推演/整理”职责，而不是全知识库自由检索器，也不是排盘器。
 */
object LocalModelPromptCompiler {
    val defaultConstraints: List<String> = listOf(
        "不得重新计算、纠正或改写排盘；盘面输入是不可变输入。",
        "用户提供的现实条件只属于 USER_CONTEXT，不得提升任何术数规则的证据等级。",
        "EvidenceGrade 只表示仓库中的来源/核验层级，不等于真值概率、吉凶强度或科学验证。",
        "只能使用本输入包明确提供的盘面事实、来源 ID、边界和用户上下文；不得补造未提供的古籍规则或来源。",
        "标为实验或受 caveat 限制的字段不得被升级为已核验事实。",
        "必须把盘面事实、来源/传统候选解释、模型自己的情境推演、不确定性分开表达。",
        "具体事体不足、角色映射不清或候选解释无法区分时，允许并优先输出无法判断/需要补充信息。",
        "不得因为模型生成得更流畅，就把推演升级为 Claim、经验验证或确定性预测。",
    )

    fun forReading(
        reading: Reading,
        context: ReadingContext = ReadingContext(),
    ): LocalModelRequest {
        val packet = LocalInferencePacket(
            toolName = reading.toolName,
            context = context,
            reading = reading,
            constraints = defaultConstraints,
        )
        return LocalModelRequest(packet = packet, prompt = compile(packet))
    }

    fun compile(packet: LocalInferencePacket): String = buildString {
        appendLine("你是玄学 App 的手机本地语言模型解释层。")
        appendLine("你的职责是对给定的确定性排盘结果和现实问题做受控整理与情境推演，不是重新排盘，也不是自由补充知识库。")
        appendLine()
        appendLine("【硬约束】")
        packet.constraints.forEachIndexed { index, constraint ->
            appendLine("${index + 1}. $constraint")
        }
        appendLine()
        appendLine("【模块】${packet.toolName}")
        appendLine("【用户事体】${packet.context.summary()}")
        appendLine()
        appendLine("【确定性/受控解释输入】")
        if (packet.reading.overall.isNotBlank()) appendLine("总评边界：${packet.reading.overall}")
        packet.reading.items.forEachIndexed { index, item ->
            appendLine("${index + 1}. [${item.evidenceGrade.label}] ${item.title}：${item.summary}")
            if (item.detail.isNotBlank()) appendLine("   细节：${item.detail}")
            if (item.sourceIds.isNotEmpty()) appendLine("   来源ID：${item.sourceIds.joinToString("、")}")
            if (item.caveat.isNotBlank()) appendLine("   条目边界：${item.caveat}")
        }
        if (packet.reading.caveats.isNotEmpty()) {
            appendLine()
            appendLine("【当前核验边界】")
            packet.reading.caveats.distinct().forEach { appendLine("- $it") }
        }
        appendLine()
        appendLine("【输出要求】")
        appendLine("按以下四段输出：")
        appendLine("1. 盘面与现实问题的关系摘要")
        appendLine("2. 候选推演（明确哪些是来源/传统候选，哪些是模型推演）")
        appendLine("3. 竞争解释与反证/敏感点")
        appendLine("4. 不确定性、无法判断项与需要补充的信息")
        appendLine("不要输出你重新计算出的盘，不要伪造来源 ID，不要把实验字段写成已验证结论。")
    }
}
