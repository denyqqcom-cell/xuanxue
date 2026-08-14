package com.xuanxue.app.ui.qimen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.interpretation.AiExecutionMode
import com.xuanxue.qimen.core.interpretation.AiInterpretationGate
import com.xuanxue.qimen.core.interpretation.AiInterpretationPolicy
import com.xuanxue.qimen.core.interpretation.AiInterpretationScope
import com.xuanxue.qimen.core.interpretation.AiOutboundPreview

/**
 * Android 侧 AI 解盘第一道交互门：先生成“本次将发送什么”的精确预览，再允许用户确认。
 * 这个组件不发 HTTP、不保存密钥，也不绑定任何模型厂商。
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
    var preview by remember { mutableStateOf<AiOutboundPreview?>(null) }
    var consent by remember { mutableStateOf(false) }
    var status by remember { mutableStateOf<String?>(null) }

    fun refreshPreview() {
        status = null
        consent = false
        preview = AiInterpretationGate.preview(chart, question, scope)
            .onFailure { status = it.message ?: it::class.java.simpleName }
            .getOrNull()
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
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = mode == AiExecutionMode.DISABLED,
                        onClick = { mode = AiExecutionMode.DISABLED; preview = null; consent = false },
                        label = { Text("关闭") },
                    )
                    FilterChip(
                        selected = mode == AiExecutionMode.LOCAL_MODEL,
                        onClick = { mode = AiExecutionMode.LOCAL_MODEL; preview = null; consent = false },
                        label = { Text("本地模型") },
                    )
                    FilterChip(
                        selected = mode == AiExecutionMode.REMOTE_USER_CONFIGURED,
                        onClick = { mode = AiExecutionMode.REMOTE_USER_CONFIGURED; preview = null; consent = false },
                        label = { Text("自定义远程 AI") },
                    )
                }
                Text(
                    when (mode) {
                        AiExecutionMode.DISABLED -> "默认关闭，不生成任何 AI 请求。"
                        AiExecutionMode.LOCAL_MODEL -> "仅准备本地模型请求；当前 App 尚未内置模型运行时。"
                        AiExecutionMode.REMOTE_USER_CONFIGURED -> "远程模式必须先预览本次字段，并对这一次 payload 单独确认。"
                    },
                    style = MaterialTheme.typography.bodySmall,
                )
            }
        }

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("2. 提问与解盘范围", fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = question,
                    onValueChange = {
                        question = it
                        preview = null
                        consent = false
                    },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("你具体想问什么？") },
                    minLines = 3,
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = scope == AiInterpretationScope.DUTY_RUNTIME,
                        onClick = { scope = AiInterpretationScope.DUTY_RUNTIME; preview = null; consent = false },
                        label = { Text("值符值使") },
                    )
                    FilterChip(
                        selected = scope == AiInterpretationScope.FULL_PLATE,
                        onClick = { scope = AiInterpretationScope.FULL_PLATE; preview = null; consent = false },
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
                    Text("3. 本次将交给 AI 的内容", fontWeight = FontWeight.Bold)
                    Text("问题：${outbound.question}")
                    Text("字段数：${outbound.evidence.facts.size}")
                    Text("Payload 指纹：${outbound.payloadFingerprint.take(16)}…", style = MaterialTheme.typography.bodySmall)

                    outbound.evidence.facts.forEach { fact ->
                        Text("${fact.label}：${fact.value}", style = MaterialTheme.typography.bodySmall)
                    }

                    Text("不会由核心自动发送：姓名、联系方式、设备标识、历史命盘、API Key。", fontWeight = FontWeight.SemiBold)
                    outbound.evidence.caveats.forEach { caveat ->
                        Text("• $caveat", style = MaterialTheme.typography.bodySmall)
                    }

                    if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(
                                checked = consent,
                                onCheckedChange = { consent = it },
                            )
                            Text("我确认仅将上面这一次预览的数据交给我配置的远程 AI")
                        }
                    }

                    Button(
                        onClick = {
                            val policy = AiInterpretationPolicy(
                                executionMode = mode,
                                scope = scope,
                                explicitRemoteConsent = mode != AiExecutionMode.REMOTE_USER_CONFIGURED || consent,
                                remoteConsentFingerprint = if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) {
                                    outbound.payloadFingerprint
                                } else {
                                    null
                                },
                            )
                            status = AiInterpretationGate.prepare(chart, question, policy)
                                .fold(
                                    onSuccess = {
                                        "请求已通过核心门禁。当前仅准备请求，尚未联网，也未绑定任何 AI 厂商。"
                                    },
                                    onFailure = { it.message ?: it::class.java.simpleName },
                                )
                        },
                        enabled = mode != AiExecutionMode.REMOTE_USER_CONFIGURED || consent,
                    ) {
                        Text(if (mode == AiExecutionMode.REMOTE_USER_CONFIGURED) "确认本次远程请求" else "准备本地 AI 请求")
                    }
                }
            }
        }

        status?.let {
            Text(it, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
        }
    }
}
