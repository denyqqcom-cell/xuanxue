package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertTrue

class RemoteAiExecutionPlanTest {
    private val chart by lazy {
        QimenEngine.cast(QimenCastInput.toRequest("1995-06-11", "09:30").getOrThrow()).getOrThrow()
    }

    private fun preview(question: String = "分析工作问题") = AiInterpretationGate.preview(
        chart = chart,
        question = question,
        scope = AiInterpretationScope.FULL_PLATE,
    ).getOrThrow()

    @Test
    fun `valid remote execution plan recomputes both payload and destination gates`() {
        val outbound = preview()
        val profile = RemoteAiProfile("https://api.example.com/v1/chat", "model-a")
        val dispatch = RemoteAiDispatchGate.preview(outbound, profile).getOrThrow()

        val plan = RemoteAiExecutionPlanner.prepare(
            chart = chart,
            question = outbound.question,
            scope = AiInterpretationScope.FULL_PLATE,
            profile = profile,
            displayedPayloadFingerprint = outbound.payloadFingerprint,
            dispatchConsentFingerprint = dispatch.dispatchFingerprint,
        ).getOrThrow()

        assertEquals(outbound.payloadFingerprint, plan.payloadFingerprint)
        assertEquals(dispatch.dispatchFingerprint, plan.dispatchFingerprint)
        assertEquals("https://api.example.com/v1/chat", plan.profile.endpoint)
        assertEquals("model-a", plan.profile.model)
        assertTrue(plan.prompt.userContent.contains("VERIFIED_SCOPE FULL_PLATE"))
        assertFalse(plan.transportPolicy.followRedirects)
    }

    @Test
    fun `question change after preview invalidates execution plan`() {
        val outbound = preview("原问题")
        val profile = RemoteAiProfile("https://api.example.com/v1/chat", "model-a")
        val dispatch = RemoteAiDispatchGate.preview(outbound, profile).getOrThrow()

        val result = RemoteAiExecutionPlanner.prepare(
            chart = chart,
            question = "修改后的问题",
            scope = AiInterpretationScope.FULL_PLATE,
            profile = profile,
            displayedPayloadFingerprint = outbound.payloadFingerprint,
            dispatchConsentFingerprint = dispatch.dispatchFingerprint,
        )

        assertIs<RemoteAiExecutionPlanError.PayloadPreviewChanged>(result.exceptionOrNull())
    }

    @Test
    fun `destination change after consent invalidates execution plan`() {
        val outbound = preview()
        val oldProfile = RemoteAiProfile("https://api.example.com/v1/chat", "model-a")
        val oldDispatch = RemoteAiDispatchGate.preview(outbound, oldProfile).getOrThrow()

        val result = RemoteAiExecutionPlanner.prepare(
            chart = chart,
            question = outbound.question,
            scope = AiInterpretationScope.FULL_PLATE,
            profile = RemoteAiProfile("https://api.example.com/v1/chat", "model-b"),
            displayedPayloadFingerprint = outbound.payloadFingerprint,
            dispatchConsentFingerprint = oldDispatch.dispatchFingerprint,
        )

        assertIs<RemoteAiDispatchError.ConsentMismatch>(result.exceptionOrNull())
    }

    @Test
    fun `transport policy refuses redirects and unbounded resource settings`() {
        assertFailsWith<IllegalArgumentException> {
            RemoteAiTransportPolicy(followRedirects = true)
        }
        assertFailsWith<IllegalArgumentException> {
            RemoteAiTransportPolicy(connectTimeoutMs = 31_000)
        }
        assertFailsWith<IllegalArgumentException> {
            RemoteAiTransportPolicy(maxResponseBytes = 8_000_001)
        }
    }

    @Test
    fun `safe log is structural whitelist and contains no question prompt or model`() {
        val question = "这是不应该出现在日志中的问题文本"
        val outbound = preview(question)
        val profile = RemoteAiProfile("https://api.example.com/v1/chat", "model-sensitive-name")
        val dispatch = RemoteAiDispatchGate.preview(outbound, profile).getOrThrow()
        val plan = RemoteAiExecutionPlanner.prepare(
            chart = chart,
            question = question,
            scope = AiInterpretationScope.FULL_PLATE,
            profile = profile,
            displayedPayloadFingerprint = outbound.payloadFingerprint,
            dispatchConsentFingerprint = dispatch.dispatchFingerprint,
        ).getOrThrow()

        val log = RemoteAiSafeLog.event(
            plan = plan,
            phase = RemoteAiLogPhase.SUCCEEDED,
            statusCode = 200,
            elapsedMs = 1234,
        )
        val rendered = log.toString()

        assertEquals("api.example.com", log.destinationHost)
        assertEquals(16, log.dispatchFingerprintPrefix.length)
        assertFalse(rendered.contains(question))
        assertFalse(rendered.contains("model-sensitive-name"))
        assertFalse(rendered.contains("SYSTEM"))
        assertFalse(rendered.contains("ENGINE_VERIFIED"))
        assertFalse(rendered.contains("Authorization", ignoreCase = true))
    }

    @Test
    fun `credential reference is a generated identifier not a place to paste a secret`() {
        RemoteAiCredentialRef("cred_0123456789abcdef")
        assertFailsWith<IllegalArgumentException> {
            RemoteAiCredentialRef("provider-profile-1")
        }
        assertFailsWith<IllegalArgumentException> {
            RemoteAiCredentialRef("Bearer secret value")
        }
        assertFailsWith<IllegalArgumentException> {
            RemoteAiCredentialRef("cred_key\nsecret")
        }
    }
}
