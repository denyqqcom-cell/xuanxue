package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import java.nio.charset.StandardCharsets
import java.security.MessageDigest

/**
 * World Model Before Symbols 的确定性阶段边界。
 *
 * 这是推理/provenance 基础设施，不是新的奇门预测器。M1 只由现实输入构建；
 * 奇门盘只能从 M2 起进入。M4 只引用已经冻结的 M3 指纹，不能产生第二份机器预测。
 */
object QimenReasoningStages {
    const val WORLD_MODEL_PROVENANCE = "REALITY_ONLY"
    const val EMPIRICAL_CREDIT = "NONE"

    enum class PredictionStatus {
        PREDICTION,
        ABSTAIN,
        UNEVALUABLE,
    }

    data class M0Input internal constructor(
        val domain: QueryDomain,
        val question: String,
        val knownFacts: String,
        val inputSha256: String,
    )

    data class M1WorldModel internal constructor(
        val domain: QueryDomain,
        val question: String,
        val knownFacts: String,
        val inputSha256: String,
        val worldModelSha256: String,
        val provenance: String = WORLD_MODEL_PROVENANCE,
    )

    data class M2SymbolMapping internal constructor(
        val worldModelSha256: String,
        val chartSha256: String,
        val mappingSha256: String,
    )

    data class M3FrozenPrediction internal constructor(
        val mappingSha256: String,
        val status: PredictionStatus,
        val predictionPayload: String?,
        val predictionSha256: String,
        val empiricalCredit: String = EMPIRICAL_CREDIT,
    )

    /**
     * M4 intentionally does not contain a mutable/copy of predictionPayload.
     * User-facing prose must be rendered beside the separately retained M3 record.
     */
    data class M4Narrative internal constructor(
        val predictionSha256: String,
        val predictionStatus: PredictionStatus,
        val narrative: String,
        val empiricalCredit: String = EMPIRICAL_CREDIT,
    )

    fun freezeInput(context: ReadingContext): M0Input {
        val question = context.normalizedQuestion
        val knownFacts = context.normalizedKnownFacts
        val inputSha = sha256(
            "M0_INPUT_FREEZE",
            context.domain.name,
            question,
            knownFacts,
        )
        return M0Input(
            domain = context.domain,
            question = question,
            knownFacts = knownFacts,
            inputSha256 = inputSha,
        )
    }

    /**
     * M1 has no chart/symbol argument by design. It cannot inspect a QimenChart.
     */
    fun buildWorldModel(input: M0Input): M1WorldModel {
        val worldSha = sha256(
            "M1_REALITY_ONLY",
            input.inputSha256,
            input.domain.name,
            input.question,
            input.knownFacts,
        )
        return M1WorldModel(
            domain = input.domain,
            question = input.question,
            knownFacts = input.knownFacts,
            inputSha256 = input.inputSha256,
            worldModelSha256 = worldSha,
        )
    }

    /**
     * 奇门盘第一次进入流水线的位置。这里只绑定盘面状态，不授予预测或实证信用。
     */
    fun mapSymbols(world: M1WorldModel, chart: QimenEngine.QimenChart): M2SymbolMapping {
        require(world.provenance == WORLD_MODEL_PROVENANCE) { "M1 must be REALITY_ONLY" }
        val chartSha = chartSha256(chart)
        return M2SymbolMapping(
            worldModelSha256 = world.worldModelSha256,
            chartSha256 = chartSha,
            mappingSha256 = sha256("M2_SYMBOL_MAPPING", world.worldModelSha256, chartSha),
        )
    }

    /**
     * 只冻结上游已经形成的机器结果；本函数本身不生成预测。
     */
    fun freezePrediction(
        mapping: M2SymbolMapping,
        status: PredictionStatus,
        predictionPayload: String? = null,
    ): M3FrozenPrediction {
        val normalizedPayload = predictionPayload?.trim()?.takeIf { it.isNotEmpty() }
        when (status) {
            PredictionStatus.PREDICTION -> require(normalizedPayload != null) {
                "PREDICTION requires a non-empty pre-outcome payload"
            }
            PredictionStatus.ABSTAIN,
            PredictionStatus.UNEVALUABLE,
            -> require(normalizedPayload == null) {
                "$status cannot carry a prediction payload"
            }
        }
        return M3FrozenPrediction(
            mappingSha256 = mapping.mappingSha256,
            status = status,
            predictionPayload = normalizedPayload,
            predictionSha256 = sha256(
                "M3_FROZEN_PREDICTION",
                mapping.mappingSha256,
                status.name,
                normalizedPayload.orEmpty(),
            ),
        )
    }

    /**
     * M4 can add prose only. It receives M3 and returns the same prediction identity.
     */
    fun narrate(prediction: M3FrozenPrediction, narrative: String): M4Narrative = M4Narrative(
        predictionSha256 = prediction.predictionSha256,
        predictionStatus = prediction.status,
        narrative = narrative.trim(),
    )

    private fun chartSha256(chart: QimenEngine.QimenChart): String {
        val gongState = chart.gongs
            .sortedBy { it.palace }
            .joinToString("|") { gong ->
                listOf(
                    gong.palace.toString(),
                    gong.diGan,
                    gong.tianXing,
                    gong.renMen,
                    gong.shenPan,
                    gong.isMaXing.toString(),
                    gong.isDayKong.toString(),
                    gong.isHourKong.toString(),
                    gong.isJiXing.toString(),
                ).joinToString(":")
            }
        return sha256(
            "QIMEN_CHART_FACTS",
            chart.solarDate,
            chart.lunarDateStr,
            chart.yearGZ,
            chart.monthGZ,
            chart.dayGZ,
            chart.hourGZ,
            chart.jieQi,
            chart.yinYang.toString(),
            chart.yuan,
            chart.ju.toString(),
            chart.juMethodUsed,
            chart.xunShou,
            chart.dunGan,
            chart.dayKong.joinToString(","),
            chart.hourKong.joinToString(","),
            chart.zhiFu,
            chart.zhiShi,
            chart.maXing,
            chart.isWuBuYu.toString(),
            chart.patterns.joinToString("|"),
            gongState,
        )
    }

    private fun sha256(vararg parts: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
            .digest(parts.joinToString("\u001f").toByteArray(StandardCharsets.UTF_8))
        return digest.joinToString("") { byte -> "%02x".format(byte.toInt() and 0xff) }
    }
}
