package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import java.net.URI

/**
 * 真正接入网络 transport 之前的最后一道离线执行计划。
 *
 * 计划会重新从当前 chart/question/scope 计算 payload fingerprint，再重新从当前
 * endpoint/model 计算 dispatch fingerprint。UI 中任何旧 preview/旧授权都不能直接拿来执行。
 */
data class RemoteAiTransportPolicy(
    val connectTimeoutMs: Int = 10_000,
    val readTimeoutMs: Int = 60_000,
    val maxResponseBytes: Int = 2_000_000,
    val followRedirects: Boolean = false,
) {
    init {
        require(connectTimeoutMs in 1_000..30_000) { "connectTimeoutMs must be 1000..30000" }
        require(readTimeoutMs in 1_000..180_000) { "readTimeoutMs must be 1000..180000" }
        require(maxResponseBytes in 1_024..8_000_000) { "maxResponseBytes must be 1024..8000000" }
        require(!followRedirects) { "Remote AI v1 does not allow redirects because destination consent is exact" }
    }
}

data class RemoteAiExecutionPlan(
    val profile: ValidatedRemoteAiProfile,
    val payloadFingerprint: String,
    val dispatchFingerprint: String,
    val prompt: QimenPreparedPrompt,
    val transportPolicy: RemoteAiTransportPolicy,
)

sealed class RemoteAiExecutionPlanError(message: String) : IllegalStateException(message) {
    class PayloadPreviewChanged : RemoteAiExecutionPlanError("AI payload changed after the displayed preview")
}

object RemoteAiExecutionPlanner {
    fun prepare(
        chart: QimenChart,
        question: String,
        scope: AiInterpretationScope,
        profile: RemoteAiProfile,
        displayedPayloadFingerprint: String,
        dispatchConsentFingerprint: String?,
        transportPolicy: RemoteAiTransportPolicy = RemoteAiTransportPolicy(),
    ): Result<RemoteAiExecutionPlan> = runCatching {
        val freshOutbound = AiInterpretationGate.preview(chart, question, scope).getOrThrow()
        if (freshOutbound.payloadFingerprint != displayedPayloadFingerprint) {
            throw RemoteAiExecutionPlanError.PayloadPreviewChanged()
        }

        val freshDispatch = RemoteAiDispatchGate.preview(freshOutbound, profile).getOrThrow()
        RemoteAiDispatchGate.authorize(freshDispatch, dispatchConsentFingerprint).getOrThrow()

        val prompt = QimenAiUiPreparation.preparePrompt(
            chart = chart,
            question = question,
            policy = AiInterpretationPolicy(
                executionMode = AiExecutionMode.REMOTE_USER_CONFIGURED,
                scope = scope,
                explicitRemoteConsent = true,
                remoteConsentFingerprint = freshOutbound.payloadFingerprint,
            ),
        ).getOrThrow()

        RemoteAiExecutionPlan(
            profile = freshDispatch.profile,
            payloadFingerprint = freshOutbound.payloadFingerprint,
            dispatchFingerprint = freshDispatch.dispatchFingerprint,
            prompt = prompt,
            transportPolicy = transportPolicy,
        )
    }
}

/**
 * 凭据只以引用 ID 出现在执行计划周边；真实 secret 不进入 plan、日志或持久化模型。
 * 后续具体安全存储实现必须单独审计。
 */
data class RemoteAiCredentialRef(val id: String) {
    init {
        require(id.matches(Regex("^[A-Za-z0-9._-]{1,80}$"))) { "credential ref id contains unsupported characters" }
    }
}

interface RemoteAiCredentialProvider {
    /**
     * 实现必须在 block 返回后尽可能擦除临时字符数组；不得记录 secret。
     * 当前仓库没有任何实现，因此本 PR 不存储 API key。
     */
    suspend fun <T> withCredential(ref: RemoteAiCredentialRef, block: suspend (CharArray) -> T): T
}

data class RemoteAiTransportResult(
    val statusCode: Int,
    val responseBody: String,
)

interface RemoteAiTransport {
    /**
     * transport 只能消费已经由 RemoteAiExecutionPlanner 生成的 plan。
     * 当前仓库没有网络实现，也没有 INTERNET 权限。
     */
    suspend fun execute(
        plan: RemoteAiExecutionPlan,
        credentialRef: RemoteAiCredentialRef,
        credentialProvider: RemoteAiCredentialProvider,
    ): Result<RemoteAiTransportResult>
}

enum class RemoteAiLogPhase {
    PREPARED,
    STARTED,
    SUCCEEDED,
    FAILED,
}

data class RemoteAiSafeLogEvent(
    val phase: RemoteAiLogPhase,
    val destinationHost: String,
    val model: String,
    val dispatchFingerprintPrefix: String,
    val statusCode: Int? = null,
    val elapsedMs: Long? = null,
)

object RemoteAiSafeLog {
    /**
     * 只允许生成白名单字段日志；不接收 prompt、question、credential 或 response body。
     */
    fun event(
        plan: RemoteAiExecutionPlan,
        phase: RemoteAiLogPhase,
        statusCode: Int? = null,
        elapsedMs: Long? = null,
    ): RemoteAiSafeLogEvent {
        val host = URI(plan.profile.endpoint).host ?: error("validated endpoint lost host")
        return RemoteAiSafeLogEvent(
            phase = phase,
            destinationHost = host,
            model = plan.profile.model,
            dispatchFingerprintPrefix = plan.dispatchFingerprint.take(16),
            statusCode = statusCode,
            elapsedMs = elapsedMs,
        )
    }
}
