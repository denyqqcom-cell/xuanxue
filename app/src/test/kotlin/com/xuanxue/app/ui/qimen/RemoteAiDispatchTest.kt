package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class RemoteAiDispatchTest {
    private fun outbound() = AiInterpretationGate.preview(
        chart = QimenEngine.cast(QimenCastInput.toRequest("1995-06-11", "09:30").getOrThrow()).getOrThrow(),
        question = "分析当前问题",
        scope = AiInterpretationScope.FULL_PLATE,
    ).getOrThrow()

    @Test
    fun `remote endpoint must use https`() {
        val result = RemoteAiProfileValidator.validate(
            RemoteAiProfile("http://api.example.com/v1/chat", "example-model"),
        )
        assertTrue(result.isFailure)
        assertIs<RemoteAiDispatchError.InvalidEndpoint>(result.exceptionOrNull())
    }

    @Test
    fun `localhost and private literal addresses are rejected`() {
        listOf(
            "https://localhost/v1/chat",
            "https://127.0.0.1/v1/chat",
            "https://10.0.0.8/v1/chat",
            "https://192.168.1.10/v1/chat",
            "https://[::1]/v1/chat",
        ).forEach { endpoint ->
            val result = RemoteAiProfileValidator.validate(RemoteAiProfile(endpoint, "example-model"))
            assertTrue(result.isFailure, "must reject $endpoint")
        }
    }

    @Test
    fun `url credentials query and fragment are rejected`() {
        listOf(
            "https://user:secret@api.example.com/v1/chat",
            "https://api.example.com/v1/chat?token=secret",
            "https://api.example.com/v1/chat#secret",
        ).forEach { endpoint ->
            val result = RemoteAiProfileValidator.validate(RemoteAiProfile(endpoint, "example-model"))
            assertIs<RemoteAiDispatchError.InvalidEndpoint>(result.exceptionOrNull(), endpoint)
        }
    }

    @Test
    fun `model id must be bounded and free of control line breaks`() {
        listOf("", "model\nother", "model\rsegment", "model\tsegment", "m".repeat(201)).forEach { model ->
            val result = RemoteAiProfileValidator.validate(
                RemoteAiProfile("https://api.example.com/v1/chat", model),
            )
            assertIs<RemoteAiDispatchError.InvalidModel>(result.exceptionOrNull(), "model=$model")
        }
    }

    @Test
    fun `dispatch consent fingerprint changes with endpoint or model`() {
        val outbound = outbound()
        val a = RemoteAiDispatchGate.preview(
            outbound,
            RemoteAiProfile("https://api.example.com/v1/chat", "model-a"),
        ).getOrThrow()
        val b = RemoteAiDispatchGate.preview(
            outbound,
            RemoteAiProfile("https://api2.example.com/v1/chat", "model-a"),
        ).getOrThrow()
        val c = RemoteAiDispatchGate.preview(
            outbound,
            RemoteAiProfile("https://api.example.com/v1/chat", "model-b"),
        ).getOrThrow()

        assertNotEquals(a.dispatchFingerprint, b.dispatchFingerprint)
        assertNotEquals(a.dispatchFingerprint, c.dispatchFingerprint)
        assertEquals(outbound.payloadFingerprint, a.payloadFingerprint)
    }

    @Test
    fun `stale remote destination consent is rejected`() {
        val outbound = outbound()
        val oldPreview = RemoteAiDispatchGate.preview(
            outbound,
            RemoteAiProfile("https://api.example.com/v1/chat", "model-a"),
        ).getOrThrow()
        val changed = RemoteAiDispatchGate.preview(
            outbound,
            RemoteAiProfile("https://api.example.com/v1/chat", "model-b"),
        ).getOrThrow()

        val result = RemoteAiDispatchGate.authorize(changed, oldPreview.dispatchFingerprint)
        assertIs<RemoteAiDispatchError.ConsentMismatch>(result.exceptionOrNull())
    }

    @Test
    fun `exact destination and payload consent is accepted`() {
        val preview = RemoteAiDispatchGate.preview(
            outbound(),
            RemoteAiProfile("https://api.example.com/v1/chat", "example-model"),
        ).getOrThrow()

        RemoteAiDispatchGate.authorize(preview, preview.dispatchFingerprint).getOrThrow()
    }
}
