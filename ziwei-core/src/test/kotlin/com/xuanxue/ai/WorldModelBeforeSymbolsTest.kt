package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue
import kotlin.test.assertFailsWith

class WorldModelBeforeSymbolsTest {

    @Test
    fun `M1 is built from reality input before any qimen chart enters`() {
        val context = ReadingContext(
            domain = QueryDomain.CAREER,
            question = "未来三个月是否适合换工作",
            knownFacts = "已有新 offer，需要异地；当前岗位稳定",
        )
        val m0 = QimenReasoningStages.freezeInput(context)
        val m1 = QimenReasoningStages.buildWorldModel(m0)

        assertEquals(QimenReasoningStages.WORLD_MODEL_PROVENANCE, m1.provenance)
        assertEquals(m0.inputSha256, m1.inputSha256)
        assertEquals(context.normalizedQuestion, m1.question)
        assertEquals(context.normalizedKnownFacts, m1.knownFacts)

        val forbiddenFieldFragments = listOf("qimen", "chart", "symbol", "gong", "gate", "star", "shen", "palace")
        val fieldNames = m1.javaClass.declaredFields.map { it.name.lowercase() }
        assertTrue(fieldNames.none { name -> forbiddenFieldFragments.any(name::contains) }, fieldNames.toString())
    }

    @Test
    fun `M2 binds qimen chart only after frozen M1`() {
        val m0 = QimenReasoningStages.freezeInput(
            ReadingContext(
                domain = QueryDomain.CAREER,
                question = "未来三个月是否适合换工作",
                knownFacts = "已有新 offer，需要异地",
            ),
        )
        val m1 = QimenReasoningStages.buildWorldModel(m0)
        val chartA = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val chartB = QimenEngine.bySolar(2026, 8, 12, 17, 37)

        val m2a = QimenReasoningStages.mapSymbols(m1, chartA)
        val m2b = QimenReasoningStages.mapSymbols(m1, chartB)

        assertEquals(m1.worldModelSha256, m2a.worldModelSha256)
        assertEquals(m1.worldModelSha256, m2b.worldModelSha256)
        assertNotEquals(m2a.chartSha256, m2b.chartSha256)
        assertNotEquals(m2a.mappingSha256, m2b.mappingSha256)
    }

    @Test
    fun `M4 narrative cannot mutate frozen M3 prediction identity`() {
        val m0 = QimenReasoningStages.freezeInput(
            ReadingContext(
                domain = QueryDomain.TRAVEL,
                question = "本周是否按原计划出行",
                knownFacts = "机票已购买，可退改",
            ),
        )
        val m1 = QimenReasoningStages.buildWorldModel(m0)
        val m2 = QimenReasoningStages.mapSymbols(m1, QimenEngine.bySolar(2026, 8, 12, 15, 37))
        val m3 = QimenReasoningStages.freezePrediction(
            m2,
            QimenReasoningStages.PredictionStatus.PREDICTION,
            "PROCEED",
        )
        val m4 = QimenReasoningStages.narrate(
            m3,
            "叙事层可以解释来源与边界，但机器预测仍以 M3 为准。",
        )

        assertEquals(m3.predictionSha256, m4.predictionSha256)
        assertEquals(m3.status, m4.predictionStatus)
        assertEquals("NONE", m3.empiricalCredit)
        assertEquals("NONE", m4.empiricalCredit)
        assertFalse(m4.javaClass.declaredFields.any { it.name == "predictionPayload" })
    }

    @Test
    fun `abstain and unevaluable cannot smuggle prediction payload`() {
        val m0 = QimenReasoningStages.freezeInput(ReadingContext(question = "是否行动"))
        val m1 = QimenReasoningStages.buildWorldModel(m0)
        val m2 = QimenReasoningStages.mapSymbols(m1, QimenEngine.bySolar(2026, 8, 12, 15, 37))

        val abstain = QimenReasoningStages.freezePrediction(
            m2,
            QimenReasoningStages.PredictionStatus.ABSTAIN,
        )
        assertEquals(null, abstain.predictionPayload)

        assertFailsWith<IllegalArgumentException> {
            QimenReasoningStages.freezePrediction(
                m2,
                QimenReasoningStages.PredictionStatus.UNEVALUABLE,
                "POST_HOC_OUTPUT",
            )
        }
    }
}
