package com.xuanxue.app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun OpenSourceScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val notices = remember(context) {
        runCatching {
            val openSource = context.assets.open("licenses/OPEN_SOURCE_NOTICES.txt")
                .bufferedReader()
                .use { it.readText() }
            val apache = context.assets.open("licenses/APACHE-2.0.txt")
                .bufferedReader()
                .use { it.readText() }
            "$openSource\n\n$apache"
        }.getOrElse { "开源许可文件读取失败：${it.message.orEmpty()}" }
    }

    Column(Modifier.fillMaxSize()) {
        Row(
            Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 8.dp),
        ) {
            OutlinedButton(onClick = onBack) { Text("返回") }
            Text(
                "开源许可",
                modifier = Modifier.padding(start = 14.dp, top = 10.dp),
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
            )
        }
        Text(
            text = notices,
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            style = MaterialTheme.typography.bodySmall,
            fontFamily = FontFamily.Monospace,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
