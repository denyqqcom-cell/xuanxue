package com.xuanxue.qimen.core.interpretation

import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.plate.FullPlateResolution
import java.security.MessageDigest

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
    /** 地盘 + 已验证的值符/值使初始锚点与当前落宫。 */
    DUTY_RUNTIME,
    /** 仅当 QimenEngine 已经返回 Resolved 四层盘时允许。 */
    FULL_PLATE,
}

data class AiInterpretationPolicy(
    val executionMode: AiExecutionMode = AiExecutionMode.DISABLED,
    val scope: AiInterpretationScope = AiInterpretationScope.EARTH_PLATE,
    /** 远程模型必须由用户在本次操作中明确同意发送数据。 */
    val explicitRemoteConsent: Boolean = false,
    /** 必须来自本次 AiInterpretationGate.preview()；把用户同意绑定到其实际看到的 question + evidence。 */
    val remoteConsentFingerprint: String? = null,
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

data class AiOutboundPreview(
    val question: String,
    val evidence: AiEvidencePacket,
    /** SHA-256 of the exact canonical payload represented by this preview. */
    val payloadFingerprint: String,
) {
    val fieldIds: List<String> get() = evidence.facts.map { it.id }
}

data class AiInterpretationRequest(
    val question: String,
    val evidence: AiEvidencePacket,
    val executionMode: AiExecutionMode,
    /** Remote adapters can log/compare this value without receiving any secret. */
    val payloadFingerprint: String,
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
    class RemoteConsentFingerprintRequired : AiInterpretationError(
        "Remote AI consent must be bound to the exact outbound preview",
    )
    class RemoteConsentMismatch : AiInterpretationError(
        "Remote AI consent fingerprint does not match the current question/evidence payload",
    )
    class ScopeLocked(scope: AiInterpretationScope) :
        AiInterpretationError("AI interpretation scope is not verified for this chart: $scope")
}

object AiEvidenceBuilder {
    fun build(chart: QimenChart, scope: AiInterpretationScope): AiEvidencePacket {
        val resolvedFullPlate = if (scope == AiInterpretationScope.FULL_PLATE) {
            when (val resolution = chart.fullPlate) {
                is FullPlateResolution.Resolved -> resolution.plate
                is FullPlateResolution.Locked -> throw AiInterpretationError.ScopeLocked(scope)
            }
        } else {
            null
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

        if (scope == AiInterpretationScope.EARTH_PLATE ||
            scope == AiInterpretationScope.DUTY_RUNTIME ||
            scope == AiInterpretationScope.FULL_PLATE
        ) {
            val earth = (1..9).joinToString("；") { palace ->
                "${palace}宫=${chart.earthPlate.stemAt(palace).zh}"
            }
            facts += AiFact("earth_plate", "地盘九仪", earth)
        }

        if (scope == AiInterpretationScope.DUTY_RUNTIME || scope == AiInterpretationScope.FULL_PLATE) {
            facts += AiFact("duty_anchor_palace", "旬首遁仪初始宫", chart.duty.anchor.dunYiPalace.toString())
            facts += AiFact("value_star", "值符星", chart.duty.anchor.valueStar.zh)
            facts += AiFact("value_star_palace", "值符星当前落宫", chart.duty.valueStarPalace.toString())
            facts += AiFact("value_gate", "值使门", chart.duty.anchor.valueGate.zh)
            facts += AiFact("value_gate_home_palace", "值使门原驻来源宫", chart.duty.anchor.gateHomePalace.toString())
            facts += AiFact("value_gate_anchor_state", "值使门锚点规则", chart.duty.anchor.gateState.name)
            facts += AiFact("value_gate_palace", "值使门当前落宫", chart.duty.valueGatePalace.toString())
            facts += AiFact("duty_branch_steps", "值使自旬首推进时辰数", chart.duty.branchStepsFromXunHead.toString())
        }

        if (resolvedFullPlate != null) {
            val sky = (1..9).mapNotNull { palace ->
                val placements = resolvedFullPlate.sky.placementsAt(palace)
                if (placements.isEmpty()) null else {
                    val value = placements.joinToString("+") { "${it.star.zh}/${it.carriedStem.zh}" }
                    "${palace}宫=$value"
                }
            }.joinToString("；")
            val human = resolvedFullPlate.human.asMap().entries.joinToString("；") { (palace, gate) ->
                "${palace}宫=${gate.zh}"
            }
            val spirit = resolvedFullPlate.spirit.asMap().entries.joinToString("；") { (palace, spiritValue) ->
                "${palace}宫=${spiritValue.zh}"
            }
            facts += AiFact("sky_plate", "天盘九星与所携奇仪", sky)
            facts += AiFact("human_plate", "人盘八门", human)
            facts += AiFact("spirit_plate", "神盘八神", spirit)
        }

        val caveats = if (scope == AiInterpretationScope.FULL_PLATE) {
            listOf(
                "本次命盘满足当前已验证转盘方法的完整四层构造条件；其他命盘若值符或值使落中五仍会被硬锁。",
                "AI只能解释本 evidence packet 中的结构化事实，不得重新排盘、改写核心结果或混入未选择的流派规则。",
                "ENGINE_VERIFIED只表示来自当前测试过的确定性引擎；术数解释属于传统模型的情境推演，不应表述为科学事实或保证性预测。",
            )
        } else {
            listOf(
                "当前 evidence scope 没有包含完整四层盘；AI不得依据自身记忆补算未提供的层。",
                "AI只能解释核心提供的结构化事实，不得覆盖或改写排盘结果。",
                "ENGINE_VERIFIED只表示来自当前测试过的确定性引擎；术数解释属于传统模型的情境推演，不应表述为科学事实或保证性预测。",
            )
        }

        return AiEvidencePacket(
            verifiedScope = scope,
            facts = facts,
            caveats = caveats,
        )
    }
}

object AiInterpretationGate {
    /**
     * Builds the exact outbound payload before any remote consent is accepted.
     * UI should render this preview, then bind the user's confirmation to payloadFingerprint.
     */
    fun preview(
        chart: QimenChart,
        question: String,
        scope: AiInterpretationScope,
    ): Result<AiOutboundPreview> = runCatching {
        val normalizedQuestion = question.trim()
        require(normalizedQuestion.isNotEmpty()) { "question must not be blank" }
        val evidence = AiEvidenceBuilder.build(chart, scope)
        AiOutboundPreview(
            question = normalizedQuestion,
            evidence = evidence,
            payloadFingerprint = fingerprint(normalizedQuestion, evidence),
        )
    }

    fun prepare(
        chart: QimenChart,
        question: String,
        policy: AiInterpretationPolicy,
    ): Result<AiInterpretationRequest> = runCatching {
        if (policy.executionMode == AiExecutionMode.DISABLED) {
            throw AiInterpretationError.Disabled()
        }

        val preview = preview(chart, question, policy.scope).getOrThrow()

        if (policy.executionMode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
            if (!policy.explicitRemoteConsent) {
                throw AiInterpretationError.RemoteConsentRequired()
            }
            val consentFingerprint = policy.remoteConsentFingerprint
                ?: throw AiInterpretationError.RemoteConsentFingerprintRequired()
            if (consentFingerprint != preview.payloadFingerprint) {
                throw AiInterpretationError.RemoteConsentMismatch()
            }
        }

        AiInterpretationRequest(
            question = preview.question,
            evidence = preview.evidence,
            executionMode = policy.executionMode,
            payloadFingerprint = preview.payloadFingerprint,
        )
    }

    private fun fingerprint(question: String, evidence: AiEvidencePacket): String {
        val canonical = buildString {
            appendLine("schema=${evidence.schemaVersion}")
            appendLine("scope=${evidence.verifiedScope.name}")
            appendLine("question=$question")
            evidence.facts.forEachIndexed { index, fact ->
                appendLine("fact[$index].id=${fact.id}")
                appendLine("fact[$index].label=${fact.label}")
                appendLine("fact[$index].value=${fact.value}")
                appendLine("fact[$index].provenance=${fact.provenance}")
            }
            evidence.caveats.forEachIndexed { index, caveat ->
                appendLine("caveat[$index]=$caveat")
            }
        }
        return MessageDigest.getInstance("SHA-256")
            .digest(canonical.toByteArray(Charsets.UTF_8))
            .joinToString("") { byte -> "%02x".format(byte) }
    }
}
