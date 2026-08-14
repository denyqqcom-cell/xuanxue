package com.xuanxue.app.ui.legal

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.components.ScreenTopBar

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
        ScreenTopBar(
            title = "开源许可",
            subtitle = "第三方版权与许可证随 App 一并分发",
            onBack = onBack,
        )
        Text(
            text = notices,
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
