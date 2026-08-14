package com.xuanxue.app.ui.qimen

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import com.xuanxue.qimen.core.interpretation.AiOutboundPreview

/**
 * Android 侧 AI 解盘安全入口：
 * 1) 先生成精确 evidence preview；
 * 2) 远程模式再把 consent 绑定到 payload + endpoint + model；
 * 3) 通过双层门禁后才生成 provider-neutral prompt。
 *
 * 当前仍不发 HTTP、不保存密钥、不绑定任何 AI 厂商。
 */
@Composable
fun QimenAiScreen(
    chart: QimenChart,
    onBack: () -> Unit,
    modifier: Modifier = Modifier,
) {
    var question by remember { mutableStateOf("") }
    var mode by remember { mutableStateOf(AiExecutionMode.DISABLED) }
    var scope by remember { mutableStateOf(AiInterpretationScope.FULL_PLATE) }
    var remoteEndpoint by remember { mutableStateOf("") }
    var remoteModel by remember { mutableStateOf("") }
    var preview by remember { mutableStateOf<AiOutboundPreview?>(null) }
    var dispatchPreview by remember { mutableStateOf<RemoteAiDispatchPreview?>(null) }
    var remoteConsentFingerprint by remember { mutableStateOf<String?>(null) }
    var preparedPrompt by remember { mutableStateOf<QimenPreparedPrompt?>(null) }
    var status by remember { mutableStateOf<String?>(null) }

    fun invalidatePreparedState() {
        preview = null
        dispatchPreview = null
        remoteConsentFingerprint = null
        preparedPrompt = null
        status = null
    }

    fun refreshPreview() {
        dispatchPreview = null
        remoteConsentFingerprint = null
        preparedPrompt = null
        status = null

        val outbound = AiInterpretationGate.preview(chart, question, scope)
            .onFailure { status = it.message ?: it::class.java.simpleName }
            .getOrNull() ?: return

        if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
            val dispatch = RemoteAiDispatchGate.preview(
                outbound = outbound,
                profile = RemoteAiProfile(remoteEndpoint, remoteModel),
            ).onFailure { status = it.message ?: it::class.java.simpleName }
                .getOrNull() ?: return
            dispatchPreview = dispatch
        }

        preview = outbound
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column {
                Text("奇门 AI 解盘", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("实验功能 · AI 只解释核心已算出的盘面", style = MaterialTheme.typography.bodySmall)
            }
            OutlinedButton(onClick = onBack) { Text("返回") }
        }

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("1. 选择 AI 方式", fontWeight = FontWeight.Bold)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    FilterChip(
                        selected = mode == AiExecutionMode.DISABLED,
                        onClick = {
                            mode = AiExecutionMode.DISABLED
                            invalidatePreparedState()
                        },
                        label = { Text("关闭") },
                    )
                    FilterChip(
                        selected = mode == AiExecutionMode.LOCAL_MODEL,
                        onClick = {
                            mode = AiExecutionMode.LOCAL_MODEL
                            invalidatePreparedState()
                        },
                        label = { Text("本地模型") },
                    )
                    FilterChip(
                        selected = mode == AiExecutionMode.REMOTE_USER_CONFIGURED,
                        onClick = {
                            mode = AiExecutionMode.REMOTE_USER_CONFIGURED
                            invalidatePreparedState()
                        },
                        label = { Text("自定义远程 AI") },
                    )
                }
                Text(
                    when (mode) {
                        AiExecutionMode.DISABLED -> "默认关闭，不生成任何 AI 请求。"
                        AiExecutionMode.LOCAL_MODEL -> "仅准备本地模型请求；当前 App 尚未内置模型运行时。"
                        AiExecutionMode.REMOTE_USER_CONFIGURED -> "远程模式会把授权同时绑定到本次盘面 payload、Endpoint 与模型 ID；当前仍不会真正联网。"
                    },
                    style = MaterialTheme.typography.bodySmall,
                )

                if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                    OutlinedTextField(
                        value = remoteEndpoint,
                        onValueChange = {
                            remoteEndpoint = it
                            invalidatePreparedState()
                        },
                        modifier = Modifier.fillMaxWidth(),
                        label = { Text("HTTPS Endpoint") },
                        placeholder = { Text("https://api.example.com/v1/chat") },
                        supportingText = { Text("v1 禁止 HTTP、localhost、私有字面 IP、URL query 与 URL 内账号密码。") },
                        singleLine = true,
                    )
                    OutlinedTextField(
                        value = remoteModel,
                        onValueChange = {
                            remoteModel = it
                            invalidatePreparedState()
                        },
                        modifier = Modifier.fillMaxWidth(),
                        label = { Text("模型 ID") },
                        placeholder = { Text("example-model") },
                        supportingText = { Text("这里只记录目标模型；本阶段没有 API Key 输入或存储。") },
                        singleLine = true,
                    )
                }
            }
        }

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("2. 提问与解盘范围", fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = question,
                    onValueChange = {
                        question = it
                        invalidatePreparedState()
                    },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("你具体想问什么？") },
                    minLines = 3,
                )
                Text(
                    "你的问题文本本身会进入 AI 请求；如选择远程 AI，请不要在问题里填写姓名、电话、邮箱、证件号等不必要的个人信息。",
                    style = MaterialTheme.typography.bodySmall,
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = scope == AiInterpretationScope.DUTY_RUNTIME,
                        onClick = {
                            scope = AiInterpretationScope.DUTY_RUNTIME
                            invalidatePreparedState()
                        },
                        label = { Text("值符值使") },
                    )
                    FilterChip(
                        selected = scope == AiInterpretationScope.FULL_PLATE,
                        onClick = {
                            scope = AiInterpretationScope.FULL_PLATE
                            invalidatePreparedState()
                        },
                        label = { Text("完整四盘") },
                    )
                }
                Button(
                    onClick = { refreshPreview() },
                    enabled = mode != AiExecutionMode.DISABLED && question.isNotBlank(),
                ) {
                    Text("生成本次数据预览")
                }
            }
        }

        preview?.let { outbound ->
            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("3. 本次 AI 数据预览", fontWeight = FontWeight.Bold)
                    Text("问题：${outbound.question}")
                    Text("字段数：${outbound.evidence.facts.size}")
                    Text("Payload 指纹：${outbound.payloadFingerprint.take(16)}…", style = MaterialTheme.typography.bodySmall)

                    dispatchPreview?.let { dispatch ->
                        Text("目标：${dispatch.profile.endpoint}", fontWeight = FontWeight.SemiBold)
                        Text("模型：${dispatch.profile.model}")
                        Text("Dispatch 指纹：${dispatch.dispatchFingerprint.take(16)}…", style = MaterialTheme.typography.bodySmall)
                    }

                    outbound.evidence.facts.forEach { fact ->
                        Text("${fact.label}：${fact.value}", style = MaterialTheme.typography.bodySmall)
                    }

                    Text(
                        "核心不会额外附加姓名、联系方式、设备标识、历史命盘或 API Key；但你在“问题”中主动输入的文字会随本次请求发送。",
                        fontWeight = FontWeight.SemiBold,
                    )
                    outbound.evidence.caveats.forEach { caveat ->
                        Text("• $caveat", style = MaterialTheme.typography.bodySmall)
                    }

                    if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                        val dispatch = dispatchPreview
                        val checked = dispatch != null && remoteConsentFingerprint == dispatch.dispatchFingerprint
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(
                                checked = checked,
                                onCheckedChange = { isChecked ->
                                    remoteConsentFingerprint = if (isChecked) dispatch?.dispatchFingerprint else null
                                    preparedPrompt = null
                                    status = null
                                },
                                enabled = dispatch != null,
                            )
                            Text("我确认本次 payload 仅用于上面显示的 Endpoint 与模型")
                        }
                    }

                    Button(
                        onClick = {
                            if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                                val dispatch = dispatchPreview
                                if (dispatch == null) {
                                    status = "远程目标预览不存在，请重新生成数据预览。"
                                    return@Button
                                }
                                val authorized = RemoteAiDispatchGate.authorize(dispatch, remoteConsentFingerprint)
                                if (authorized.isFailure) {
                                    status = authorized.exceptionOrNull()?.message ?: "remote dispatch authorization failed"
                                    return@Button
                                }
                            }

                            val policy = AiInterpretationPolicy(
                                executionMode = mode,
                                scope = scope,
                                explicitRemoteConsent = mode != AiExecutionMode.REMOTE_USER_CONFIGURED || remoteConsentFingerprint != null,
                                remoteConsentFingerprint = if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                                    outbound.payloadFingerprint
                                } else {
                                    null
                                },
                            )
                            preparedPrompt = QimenAiUiPreparation.preparePrompt(chart, question, policy)
                                .onFailure { status = it.message ?: it::class.java.simpleName }
                                .getOrNull()
                            if (preparedPrompt != null) {
                                status = "已通过 payload + destination 双层门禁并生成提示词。当前仍未联网。"
                            }
                        },
                        enabled = mode != AiExecutionMode.REMOTE_USER_CONFIGURED || (
                            dispatchPreview != null && remoteConsentFingerprint == dispatchPreview?.dispatchFingerprint
                        ),
                    ) {
                        Text(if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) "确认目标并生成 AI 提示词" else "生成本地 AI 提示词")
                    }
                }
            }
        }

        preparedPrompt?.let { prompt ->
            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("4. 可复制 AI 提示词", fontWeight = FontWeight.Bold)
                    Text(
                        "以下内容由同一份已通过门禁的 evidence 生成。长按选择即可复制；App 本阶段不会自动发送。",
                        style = MaterialTheme.typography.bodySmall,
                    )
                    Text("SYSTEM", fontWeight = FontWeight.SemiBold)
                    SelectionContainer {
                        Text(prompt.systemInstruction, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodySmall)
                    }
                    Text("USER", fontWeight = FontWeight.SemiBold)
                    SelectionContainer {
                        Text(prompt.userContent, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }

        status?.let {
            Text(it, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
        }
    }
}
