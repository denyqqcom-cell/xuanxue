package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.api.PlateState
import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationError
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import com.xuanxue.qimen.core.plate.FullPlateLockReason
import com.xuanxue.qimen.core.plate.FullPlateResolution
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class AiInterpretationContractTest {
    private fun chartAt(year: Int, month: Int, day: Int, hour: Int, minute: Int) = QimenEngine.cast(
        QimenRequest(
            instantEpochMs = LocalDateTime.of(year, month, day, hour, minute)
                .atZone(ZoneId.of("Asia/Shanghai"))
                .toInstant()
                .toEpochMilli(),
        ),
    ).getOrThrow()

    private fun chart() = chartAt(2022, 8, 8, 10, 0)

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
    fun remoteModeRequiresExplicitConsentAndPreviewFingerprint() {
        val currentChart = chart()
        val question = "帮我分析"
        val preview = AiInterpretationGate.preview(
            chart = currentChart,
            question = question,
            scope = AiInterpretationScope.EARTH_PLATE,
        ).getOrThrow()

        val noConsent = AiInterpretationGate.prepare(
            chart = currentChart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.EARTH_PLATE,
                explicitRemoteConsent = false,
                remoteConsentFingerprint = preview.payloadFingerprint,
            ),
        )
        assertIs<AiInterpretationError.RemoteConsentRequired>(noConsent.exceptionOrNull())

        val noFingerprint = AiInterpretationGate.prepare(
            chart = currentChart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.EARTH_PLATE,
                explicitRemoteConsent = true,
            ),
        )
        assertIs<AiInterpretationError.RemoteConsentFingerprintRequired>(noFingerprint.exceptionOrNull())
    }

    @Test
    fun consentFingerprintIsBoundToExactQuestionAndEvidence() {
        val currentChart = chart()
        val previewA = AiInterpretationGate.preview(
            currentChart,
            "这次合作是否继续？",
            AiInterpretationScope.EARTH_PLATE,
        ).getOrThrow()
        val previewB = AiInterpretationGate.preview(
            currentChart,
            "这次合作是否立即停止？",
            AiInterpretationScope.EARTH_PLATE,
        ).getOrThrow()

        assertNotEquals(previewA.payloadFingerprint, previewB.payloadFingerprint)
        assertTrue(previewA.payloadFingerprint.matches(Regex("[0-9a-f]{64}")))
        assertTrue(previewA.fieldIds.contains("earth_plate"))

        val staleConsent = AiInterpretationGate.prepare(
            chart = currentChart,
            question = previewB.question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.EARTH_PLATE,
                explicitRemoteConsent = true,
                remoteConsentFingerprint = previewA.payloadFingerprint,
            ),
        )
        assertIs<AiInterpretationError.RemoteConsentMismatch>(staleConsent.exceptionOrNull())
    }

    @Test
    fun realCenterTargetChartLocksFullPlateAndAiCannotBypassIt() {
        val lockedChart = chartAt(1995, 8, 13, 12, 0)
        assertEquals("丙子", lockedChart.dayPillar.zh)
        assertEquals("甲午", lockedChart.hourPillar.zh)
        assertEquals(PlateState.FULL_PLATE_LOCKED_CENTER_TARGET, lockedChart.plateState)
        val locked = assertIs<FullPlateResolution.Locked>(lockedChart.fullPlate)
        assertEquals(
            setOf(FullPlateLockReason.VALUE_STAR_IN_CENTER, FullPlateLockReason.VALUE_GATE_IN_CENTER),
            locked.reasons,
        )

        val preview = AiInterpretationGate.preview(
            chart = lockedChart,
            question = "完整解盘",
            scope = AiInterpretationScope.FULL_PLATE,
        )
        assertIs<AiInterpretationError.ScopeLocked>(preview.exceptionOrNull())

        val result = AiInterpretationGate.prepare(
            chart = lockedChart,
            question = "完整解盘",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.LOCAL_MODEL,
                scope = AiInterpretationScope.FULL_PLATE,
            ),
        )
        assertIs<AiInterpretationError.ScopeLocked>(result.exceptionOrNull())
    }

    @Test
    fun resolvedSourceChartCanProduceFullPlateEvidenceWithoutAiRecalculating() {
        val sourceChart = chartAt(1995, 6, 11, 9, 30)
        assertEquals(PlateState.FULL_PLATE_RESOLVED_SUPPORTED_METHOD, sourceChart.plateState)
        assertIs<FullPlateResolution.Resolved>(sourceChart.fullPlate)

        val request = AiInterpretationGate.prepare(
            chart = sourceChart,
            question = "只依据完整盘面事实分析当前结构",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.LOCAL_MODEL,
                scope = AiInterpretationScope.FULL_PLATE,
            ),
        ).getOrThrow()

        val facts = request.evidence.facts.associateBy { it.id }
        assertEquals(AiInterpretationScope.FULL_PLATE, request.evidence.verifiedScope)
        assertTrue("earth_plate" in facts)
        assertTrue("value_star" in facts)
        assertTrue("value_gate" in facts)
        assertTrue("sky_plate" in facts)
        assertTrue("human_plate" in facts)
        assertTrue("spirit_plate" in facts)
        assertTrue(facts.getValue("sky_plate").value.contains("9宫=天任/癸"))
        assertTrue(facts.getValue("human_plate").value.contains("2宫=生门"))
        assertTrue(facts.getValue("spirit_plate").value.contains("9宫=值符"))
        assertTrue(facts.values.all { it.provenance == "ENGINE_VERIFIED" })
        assertTrue(request.evidence.caveats.any { it.contains("不得重新排盘") })
        assertTrue(request.payloadFingerprint.matches(Regex("[0-9a-f]{64}")))
    }

    @Test
    fun remoteFullPlateConsentMustMatchTheExactPreview() {
        val sourceChart = chartAt(1995, 6, 11, 9, 30)
        assertIs<FullPlateResolution.Resolved>(sourceChart.fullPlate)
        val question = "完整解盘"
        val preview = AiInterpretationGate.preview(
            sourceChart,
            question,
            AiInterpretationScope.FULL_PLATE,
        ).getOrThrow()

        val allowed = AiInterpretationGate.prepare(
            chart = sourceChart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.FULL_PLATE,
                explicitRemoteConsent = true,
                remoteConsentFingerprint = preview.payloadFingerprint,
            ),
        ).getOrThrow()
        assertEquals(AiInterpretationScope.FULL_PLATE, allowed.evidence.verifiedScope)
        assertEquals(preview.payloadFingerprint, allowed.payloadFingerprint)
    }

    @Test
    fun earthPlateEvidenceUsesCoreFactsInsteadOfAskingAiToRecalculate() {
        val currentChart = chart()
        val question = "从已验证信息看当前局面"
        val preview = AiInterpretationGate.preview(
            currentChart,
            question,
            AiInterpretationScope.EARTH_PLATE,
        ).getOrThrow()
        val request = AiInterpretationGate.prepare(
            chart = currentChart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = AiInterpretationScope.EARTH_PLATE,
                explicitRemoteConsent = true,
                remoteConsentFingerprint = preview.payloadFingerprint,
            ),
        ).getOrThrow()

        assertEquals(AiInterpretationScope.EARTH_PLATE, request.evidence.verifiedScope)
        assertTrue(request.evidence.facts.any { it.id == "earth_plate" })
        assertFalse(request.evidence.facts.any { it.id == "value_star" })
        assertTrue(request.evidence.facts.all { it.provenance == "ENGINE_VERIFIED" })
        assertTrue(request.evidence.caveats.any { it.contains("补算未提供的层") })
    }

    @Test
    fun dutyRuntimeScopeAddsOnlyEngineResolvedDutyFacts() {
        val request = AiInterpretationGate.prepare(
            chart = chart(),
            question = "只依据当前已验证的值符值使信息分析",
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.LOCAL_MODEL,
                scope = AiInterpretationScope.DUTY_RUNTIME,
            ),
        ).getOrThrow()

        val facts = request.evidence.facts.associateBy { it.id }
        assertEquals(AiInterpretationScope.DUTY_RUNTIME, request.evidence.verifiedScope)
        assertTrue("earth_plate" in facts)
        assertTrue("value_star" in facts)
        assertTrue("value_star_palace" in facts)
        assertTrue("value_gate" in facts)
        assertTrue("value_gate_home_palace" in facts)
        assertTrue("value_gate_anchor_state" in facts)
        assertTrue("value_gate_palace" in facts)
        assertTrue("duty_branch_steps" in facts)
        assertTrue(facts.values.all { it.provenance == "ENGINE_VERIFIED" })
        assertFalse("sky_plate" in facts)
        assertFalse("human_plate" in facts)
        assertFalse("spirit_plate" in facts)
        assertTrue(request.evidence.caveats.any { it.contains("没有包含完整四层盘") })
    }
}
