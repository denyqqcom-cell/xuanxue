package com.xuanxue.app.ui.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.components.SectionTitle

@Composable
fun HomeScreen(
    onNewChart: () -> Unit,
    onLicenses: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 18.dp, vertical = 22.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text("玄学", style = MaterialTheme.typography.displaySmall)
            Text(
                "本地排盘 · 私密保存 · 无广告干扰",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }

        Surface(
            color = MaterialTheme.colorScheme.primaryContainer,
            shape = MaterialTheme.shapes.large,
        ) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                Text("把复杂的盘，先变得看得懂。", style = MaterialTheme.typography.headlineSmall)
                Text(
                    "先完成准确排盘，再按宫位逐层展开星曜、大限与细节。算法留在本机，界面只负责把信息讲清楚。",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                )
                Button(onClick = onNewChart, modifier = Modifier.fillMaxWidth()) {
                    Text("新建紫微命盘")
                }
            }
        }

        SectionTitle("排盘工具", "当前只开放已经完成算法验证的模块")
        ModuleCard(
            title = "紫微斗数",
            description = "十二宫 · 主星四化 · 大限小限",
            status = "可用",
            enabled = true,
            onClick = onNewChart,
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            ModuleCard(
                title = "奇门遁甲",
                description = "知识库已整理",
                status = "开发中",
                enabled = false,
                modifier = Modifier.weight(1f),
            )
            ModuleCard(
                title = "八字",
                description = "研究验证中",
                status = "开发中",
                enabled = false,
                modifier = Modifier.weight(1f),
            )
        }
        ModuleCard(
            title = "风水",
            description = "暂不开放排盘入口",
            status = "规划中",
            enabled = false,
        )

        Spacer(Modifier.height(2.dp))
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(7.dp),
            ) {
                Text("隐私与版权", style = MaterialTheme.typography.titleMedium)
                Text(
                    "App 不申请网络权限，不含广告、支付或推送。新版界面为独立设计，不使用商业命理 App 的图片、字体、截图或文案。",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                TextButton(onClick = onLicenses) { Text("查看开源许可") }
            }
        }
    }
}

@Composable
private fun ModuleCard(
    title: String,
    description: String,
    status: String,
    enabled: Boolean,
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
) {
    OutlinedCard(modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(15.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Row(modifier = Modifier.fillMaxWidth()) {
                Text(title, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                Text(
                    status,
                    style = MaterialTheme.typography.labelLarge,
                    color = if (enabled) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Text(
                description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (enabled && onClick != null) {
                TextButton(onClick = onClick) { Text("开始排盘") }
            }
        }
    }
}
