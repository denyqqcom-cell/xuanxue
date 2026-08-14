package com.xuanxue.app

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.qimen.QimenAiScreen
import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest

/**
 * 旧首页与后续 UI/UX v2 之间的薄入口层。
 * 奇门 AI 功能独立成新屏，避免把 AI 状态塞进紫微排盘组件。
 */
@Composable
fun XuanxueRoot() {
    var showQimenAi by remember { mutableStateOf(false) }

    if (showQimenAi) {
        val qimenChartResult = remember {
            QimenEngine.cast(
                QimenRequest(
                    instantEpochMs = System.currentTimeMillis(),
                ),
            )
        }
        val chart = qimenChartResult.getOrNull()
        if (chart != null) {
            QimenAiScreen(
                chart = chart,
                onBack = { showQimenAi = false },
            )
        } else {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(
                    "当前奇门盘无法生成：${qimenChartResult.exceptionOrNull()?.message ?: "unknown"}",
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
        return
    }

    Box(Modifier.fillMaxSize()) {
        XuanxueApp()
        ExtendedFloatingActionButton(
            onClick = { showQimenAi = true },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
            text = { Text("奇门 AI 解盘") },
        )
    }
}
