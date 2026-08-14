package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.interpretation.AiOutboundPreview
import java.net.URI
import java.security.MessageDigest

/**
 * 远程 AI 真正联网前的 App 层安全合同。
 *
 * consent 不仅绑定奇门 payload，还必须绑定“发到哪里 / 用哪个模型”。
 * 本文件只做离线校验与 fingerprint，不发网络请求、不接触 API key。
 */
data class RemoteAiProfile(
    val endpoint: String,
    val model: String,
)

data class ValidatedRemoteAiProfile(
    val endpoint: String,
    val model: String,
)

data class RemoteAiDispatchPreview(
    val profile: ValidatedRemoteAiProfile,
    val payloadFingerprint: String,
    val dispatchFingerprint: String,
)

sealed class RemoteAiDispatchError(message: String) : IllegalArgumentException(message) {
    class InvalidEndpoint(message: String) : RemoteAiDispatchError(message)
    class InvalidModel(message: String) : RemoteAiDispatchError(message)
    class ConsentFingerprintRequired : RemoteAiDispatchError("Remote dispatch consent fingerprint is required")
    class ConsentMismatch : RemoteAiDispatchError("Remote dispatch destination or payload changed after consent")
}

object RemoteAiProfileValidator {
    fun validate(profile: RemoteAiProfile): Result<ValidatedRemoteAiProfile> = runCatching {
        val endpointValue = profile.endpoint.trim()
        val modelValue = profile.model.trim()

        if (endpointValue.length !in 1..2048) {
            throw RemoteAiDispatchError.InvalidEndpoint("远程 AI Endpoint 长度无效")
        }
        val uri = try {
            URI(endpointValue)
        } catch (_: Exception) {
            throw RemoteAiDispatchError.InvalidEndpoint("远程 AI Endpoint 不是有效 URI")
        }

        if (!uri.scheme.equals("https", ignoreCase = true)) {
            throw RemoteAiDispatchError.InvalidEndpoint("远程 AI 只允许 HTTPS；本地模型请使用“本地模型”模式")
        }
        if (uri.host.isNullOrBlank()) {
            throw RemoteAiDispatchError.InvalidEndpoint("远程 AI Endpoint 必须包含明确主机名")
        }
        if (uri.userInfo != null) {
            throw RemoteAiDispatchError.InvalidEndpoint("Endpoint 不允许在 URL 中携带用户名或密码")
        }
        if (uri.fragment != null) {
            throw RemoteAiDispatchError.InvalidEndpoint("Endpoint 不允许 fragment")
        }
        if (uri.rawQuery != null) {
            throw RemoteAiDispatchError.InvalidEndpoint("当前 v1 Endpoint 不允许 query；避免把密钥或动态参数放入可记录 URL")
        }
        if (isLocalOrPrivateHost(uri.host)) {
            throw RemoteAiDispatchError.InvalidEndpoint("远程 AI Endpoint 不允许 localhost、.local 或私有/回环字面 IP")
        }

        if (modelValue.isBlank() || modelValue.length > 200 || modelValue.any { it == '\n' || it == '\r' || it == '\t' }) {
            throw RemoteAiDispatchError.InvalidModel("模型 ID 不能为空、不能超过 200 字符，也不能包含控制换行")
        }

        ValidatedRemoteAiProfile(
            endpoint = uri.normalize().toASCIIString(),
            model = modelValue,
        )
    }

    private fun isLocalOrPrivateHost(host: String): Boolean {
        val h = host.lowercase().trimEnd('.')
        if (h == "localhost" || h.endsWith(".localhost") || h.endsWith(".local")) return true

        val ipv4 = h.split('.').takeIf { parts ->
            parts.size == 4 && parts.all { part -> part.toIntOrNull() in 0..255 }
        }?.map { it.toInt() }
        if (ipv4 != null) {
            val a = ipv4[0]
            val b = ipv4[1]
            if (a == 0 || a == 10 || a == 127) return true
            if (a == 100 && b in 64..127) return true
            if (a == 169 && b == 254) return true
            if (a == 172 && b in 16..31) return true
            if (a == 192 && b == 168) return true
            if (a == 198 && b in 18..19) return true
            if (a >= 224) return true
        }

        // URI.host returns IPv6 literals without [] on the JDK used by Android/JVM.
        val ipv6 = h.removePrefix("[").removeSuffix("]")
        if (ipv6 == "::" || ipv6 == "::1") return true
        if (ipv6.startsWith("fc") || ipv6.startsWith("fd")) return true
        if (Regex("^fe[89ab].*", RegexOption.IGNORE_CASE).matches(ipv6)) return true

        return false
    }
}

object RemoteAiDispatchGate {
    fun preview(
        outbound: AiOutboundPreview,
        profile: RemoteAiProfile,
    ): Result<RemoteAiDispatchPreview> = RemoteAiProfileValidator.validate(profile).map { validated ->
        val canonical = buildString {
            appendLine("qimen-remote-dispatch-v1")
            appendLine(outbound.payloadFingerprint)
            appendLine(validated.endpoint)
            append(validated.model)
        }
        RemoteAiDispatchPreview(
            profile = validated,
            payloadFingerprint = outbound.payloadFingerprint,
            dispatchFingerprint = sha256(canonical),
        )
    }

    fun authorize(
        preview: RemoteAiDispatchPreview,
        consentFingerprint: String?,
    ): Result<Unit> = runCatching {
        if (consentFingerprint.isNullOrBlank()) throw RemoteAiDispatchError.ConsentFingerprintRequired()
        if (consentFingerprint != preview.dispatchFingerprint) throw RemoteAiDispatchError.ConsentMismatch()
    }

    private fun sha256(value: String): String = MessageDigest.getInstance("SHA-256")
        .digest(value.toByteArray(Charsets.UTF_8))
        .joinToString("") { byte -> "%02x".format(byte) }
}
