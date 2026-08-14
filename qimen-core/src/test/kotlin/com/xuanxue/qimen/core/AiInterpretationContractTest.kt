package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationError
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertTrue

class AiInterpretationContractTest {
    private fun chart() = QimenEngine.cast(
        QimenRequest(
            instantEpochMs = LocalDateTime.of(2022, 8, 8, 10, 0)
                .atZone(ZoneId.of("Asia/Shanghai"))
                .toInstant()
                .toEpochMilli(),
        ),
    ).getOrThrow()

    @Test
    fun disabledModeCannotPrepareRequest() {
        val result = AiInterpretationGate.prepare(
            chart = chart(),
            question = "这件事目前的主要矛盾是什么？",
            policy = AiInterpretationPolicy(),
        )
        assertIs<AiInterpretationError.Disabled>(result.exceptionOrNull())
    }

    @Test
    fun remoteModeRequiresExplicitConsentPerRequest() {
        val result = AiInterpretationGate.prepare(
            chart = chart(),
            question = "帮我分析",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                explicitRemoteConsent = false,
            ),
        )
        assertIs<AiInterpretationError.RemoteConsentRequired>(result.exceptionOrNull())
    }

    @Test
    fun fullPlateInterpretationStaysLockedUntilAllLayersAreVerified() {
        val result = AiInterpretationGate.prepare(
            chart = chart(),
            question = "完整解盘",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.LOCAL_MODEL,
                scope = AiInterpretationScope.FULL_PLATE,
            ),
        )
        assertIs<AiInterpretationError.ScopeLocked>(result.exceptionOrNull())
    }

    @Test
    fun earthPlateEvidenceUsesCoreFactsInsteadOfAskingAiToRecalculate() {
        val request = AiInterpretationGate.prepare(
            chart = chart(),
            question = "从已验证信息看当前局面",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.EARTH_PLATE,
                explicitRemoteConsent = true,
            ),
        ).getOrThrow()

        assertEquals(AiInterpretationScope.EARTH_PLATE, request.evidence.verifiedScope)
        assertTrue(request.evidence.facts.any { it.id == "earth_plate" })
        assertTrue(request.evidence.facts.all { it.provenance == "ENGINE_VERIFIED" })
        assertTrue(request.evidence.caveats.any { it.contains("AI不得自行补算") })
    }
}
