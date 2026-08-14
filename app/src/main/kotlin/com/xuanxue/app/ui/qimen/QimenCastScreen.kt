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
import com.xuanxue.qimen.core.api.QimenEngine

/**
 * 正式奇门起局入口。当前方法只接受 Asia/Shanghai 民用时钟；真太阳时仍由 core 明确拒绝。
 */
@Composable
fun QimenCastScreen(
    onBack: () -> Unit,
    onOpenAi: (QimenChart) -> Unit,
    modifier: Modifier = Modifier,
) {
    val initial = remember { QimenCastInput.displayForEpochMs(System.currentTimeMillis()) }
    var dateText by remember { mutableStateOf(initial.dateText) }
    var timeText by remember { mutableStateOf(initial.timeText) }
    var chart by remember { mutableStateOf<QimenChart?>(null) }
    var error by remember { mutableStateOf<String?>(null) }

    fun cast() {
        chart = null
        error = null
        val request = QimenCastInput.toRequest(dateText, timeText)
            .onFailure { error = it.message ?: it::class.java.simpleName }
            .getOrNull() ?: return

        chart = QimenEngine.cast(request)
            .onFailure { error = it.message ?: it::class.java.simpleName }
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
                Text("奇门遁甲起局", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("当前支持：时家转盘 · 北京时间 Asia/Shanghai", style = MaterialTheme.typography.bodySmall)
            }
            OutlinedButton(onClick = onBack) { Text("返回") }
        }

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("起局时间", fontWeight = FontWeight.Bold)
                Text(
                    "请输入事件/问事采用的北京时间。当前核心没有启用真太阳时，也不会用手机当前时区偷偷改写这里的时间。",
                    style = MaterialTheme.typography.bodySmall,
                )
                OutlinedTextField(
                    value = dateText,
                    onValueChange = {
                        dateText = it
                        chart = null
                        error = null
                    },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("日期 YYYY-MM-DD") },
                    singleLine = true,
                )
                OutlinedTextField(
                    value = timeText,
                    onValueChange = {
                        timeText = it
                        chart = null
                        error = null
                    },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("时间 HH:mm") },
                    supportingText = { Text("分钟级输入用于精确节气边界，不把时辰近似当成交节时刻。") },
                    singleLine = true,
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(onClick = {
                        val now = QimenCastInput.displayForEpochMs(System.currentTimeMillis())
                        dateText = now.dateText
                        timeText = now.timeText
                        chart = null
                        error = null
                    }) {
                        Text("此刻（北京时间）")
                    }
                    Button(onClick = { cast() }) { Text("生成奇门盘") }
                }
            }
        }

        error?.let {
            OutlinedCard(Modifier.fillMaxWidth()) {
                Text(
                    text = it,
                    modifier = Modifier.padding(12.dp),
                    color = MaterialTheme.colorScheme.error,
                    fontWeight = FontWeight.SemiBold,
                )
            }
        }

        chart?.let { value ->
            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("已生成", fontWeight = FontWeight.Bold)
                    Text("北京时间：${value.localDateTime}")
                    Text("日柱 ${value.dayPillar.zh} · 时柱 ${value.hourPillar.zh}")
                    Text("${value.jieqi.jieqi.zh} · ${if (value.jieqi.dun.name == "YANG") "阳遁" else "阴遁"}${value.ju}局 · ${value.yuan.zh}")
                    Text("旬首 ${value.xun.xunShou.zh} · 旬空 ${value.xun.xunKong.joinToString("") { it.zh }}")
                    Text("盘面状态：${value.plateState.name}", style = MaterialTheme.typography.bodySmall)
                    if (value.isWuBuYu) {
                        Text("盘前标记：五不遇时", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.SemiBold)
                    }
                    Button(onClick = { onOpenAi(value) }) {
                        Text("基于这张盘进入 AI 解盘")
                    }
                }
            }
        }
    }
}
