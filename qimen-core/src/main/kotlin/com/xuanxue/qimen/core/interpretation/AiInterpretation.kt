package com.xuanxue.qimen.core.interpretation

import com.xuanxue.qimen.core.api.QimenChart

/**
 * AI 只作为解释层，不承担历法、定局或排盘计算。
 * 具体本地模型/远程 API 由 App 层实现；qimen-core 不保存密钥、不发网络请求。
 */
enum class AiExecutionMode {
    DISABLED,
    LOCAL_MODEL,
    REMOTE_USER_CONFIGURED,
}

enum class AiInterpretationScope {
    PRE_PLATE,
    EARTH_PLATE,
    FULL_PLATE,
}

data class AiInterpretationPolicy(
    val executionMode: AiExecutionMode = AiExecutionMode.DISABLED,
    val scope: AiInterpretationScope = AiInterpretationScope.EARTH_PLATE,
    /** 远程模型必须由用户在本次操作中明确同意发送数据。 */
    val explicitRemoteConsent: Boolean = false,
)

data class AiFact(
    val id: String,
    val label: String,
    val value: String,
    /** ENGINE_VERIFIED 表示来自已通过核心测试的结构化计算，不等于术数结论已被科学证实。 */
    val provenance: String = "ENGINE_VERIFIED",
)

data class AiEvidencePacket(
    val schemaVersion: String = "qimen-ai-evidence-v1",
    val verifiedScope: AiInterpretationScope,
    val facts: List<AiFact>,
    val caveats: List<String>,
)

data class AiInterpretationRequest(
    val question: String,
    val evidence: AiEvidencePacket,
    val executionMode: AiExecutionMode,
)

data class AiInterpretationResult(
    val text: String,
    val warnings: List<String> = emptyList(),
)

interface AiInterpreter {
    suspend fun interpret(request: AiInterpretationRequest): AiInterpretationResult
}

sealed class AiInterpretationError(message: String) : IllegalStateException(message) {
    class Disabled : AiInterpretationError("AI interpretation is disabled")
    class RemoteConsentRequired : AiInterpretationError("Remote AI requires explicit user consent for this request")
    class ScopeLocked(scope: AiInterpretationScope) :
        AiInterpretationError("AI interpretation scope is not verified yet: $scope")
}

object AiEvidenceBuilder {
    fun build(chart: QimenChart, scope: AiInterpretationScope): AiEvidencePacket {
        if (scope == AiInterpretationScope.FULL_PLATE) {
            throw AiInterpretationError.ScopeLocked(scope)
        }

        val facts = mutableListOf(
            AiFact("qimen_datetime", "起局时间", chart.localDateTime.toString()),
            AiFact("zone", "时区", chart.zoneId),
            AiFact("qimen_date", "奇门换日日期", chart.qimenDate.toString()),
            AiFact("day_pillar", "日柱", chart.dayPillar.zh),
            AiFact("hour_pillar", "时柱", chart.hourPillar.zh),
            AiFact("xun_shou", "旬首", chart.xun.xunShou.zh),
            AiFact("dun_yi", "遁仪", chart.xun.dunYi.zh),
            AiFact("xun_kong", "旬空", chart.xun.xunKong.joinToString("") { it.zh }),
            AiFact("jieqi", "节气", chart.jieqi.jieqi.zh),
            AiFact("dun", "阴阳遁", if (chart.jieqi.dun.name == "YANG") "阳遁" else "阴遁"),
            AiFact("futou", "符头", chart.futou.zh),
            AiFact("yuan", "元", chart.yuan.zh),
            AiFact("ju", "局数", chart.ju.toString()),
            AiFact("wubuyu", "五不遇时", if (chart.isWuBuYu) "是" else "否"),
        )

        if (scope == AiInterpretationScope.EARTH_PLATE) {
            val earth = (1..9).joinToString("；") { palace ->
                "${palace}宫=${chart.earthPlate.stemAt(palace).zh}"
            }
            facts += AiFact("earth_plate", "地盘九仪", earth)
        }

        return AiEvidencePacket(
            verifiedScope = scope,
            facts = facts,
            caveats = listOf(
                "当前核心尚未验证天盘九星、人盘八门、神盘八神，AI不得自行补算这些层。",
                "AI只能解释核心提供的结构化事实，不得覆盖或改写排盘结果。",
                "术数解释属于传统模型的情境推演，不应表述为确定事实或保证性预测。",
            ),
        )
    }
}

object AiInterpretationGate {
    fun prepare(
        chart: QimenChart,
        question: String,
        policy: AiInterpretationPolicy,
    ): Result<AiInterpretationRequest> = runCatching {
        when (policy.executionMode) {
            AiExecutionMode.DISABLED -> throw AiInterpretationError.Disabled()
            AiExecutionMode.REMOTE_USER_CONFIGURED -> {
                if (!policy.explicitRemoteConsent) {
                    throw AiInterpretationError.RemoteConsentRequired()
                }
            }
            AiExecutionMode.LOCAL_MODEL -> Unit
        }

        val normalizedQuestion = question.trim()
        require(normalizedQuestion.isNotEmpty()) { "question must not be blank" }

        AiInterpretationRequest(
            question = normalizedQuestion,
            evidence = AiEvidenceBuilder.build(chart, policy.scope),
            executionMode = policy.executionMode,
        )
    }
}
