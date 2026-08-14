package com.xuanxue.app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.Reading

/**
 * 解读卡片（离线规则解读，无网络）。
 * 将来 BYOK 云端 AI 启用时，本卡片可切换为"模型 + 工具调用"输出。
 */
@Composable
fun ReadingCard(reading: Reading) {
    if (reading.items.isEmpty()) return
    Spacer(Modifier.height(12.dp))
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp)) {
            Text("✎ 解读（离线规则）", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = Color(0xFF6D4C41))
            Spacer(Modifier.height(6.dp))
            reading.items.forEach { item ->
                Text(item.summary, fontSize = 14.sp, lineHeight = 22.sp, modifier = Modifier.padding(bottom = 4.dp))
            }
        }
    }
}
