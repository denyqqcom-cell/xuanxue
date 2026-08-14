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
import com.xuanxue.app.domain.ModuleStage
import com.xuanxue.app.domain.PracticeModule
import com.xuanxue.app.domain.PracticeModules
import com.xuanxue.app.ui.components.SectionTitle

@Composable
fun HomeScreen(
    onNewChart: () -> Unit,
    onOpenModule: (PracticeModule) -> Unit,
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
                Text("五套术数，一个本地工具箱。", style = MaterialTheme.typography.headlineSmall)
                Text(
                    "紫微已经可用，奇门进入基础起局阶段；八字、六爻、大六壬继续按“资料→规则→夹具→核心”的顺序推进。不会为了凑功能画出未经验证的盘。",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                )
                Button(onClick = onNewChart, modifier = Modifier.fillMaxWidth()) {
                    Text("新建紫微命盘")
                }
            }
        }

        SectionTitle("排盘工具", "完整盘与基础核心分级开放，未验证能力不会伪装成可用")
        ModuleCard(
            module = PracticeModules.Ziwei,
            onClick = onNewChart,
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            ModuleCard(
                module = PracticeModules.Qimen,
                modifier = Modifier.weight(1f),
                onClick = { onOpenModule(PracticeModules.Qimen) },
            )
            ModuleCard(
                module = PracticeModules.Bazi,
                modifier = Modifier.weight(1f),
                onClick = { onOpenModule(PracticeModules.Bazi) },
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            ModuleCard(
                module = PracticeModules.Liuyao,
                modifier = Modifier.weight(1f),
                onClick = { onOpenModule(PracticeModules.Liuyao) },
            )
            ModuleCard(
                module = PracticeModules.Liuren,
                modifier = Modifier.weight(1f),
                onClick = { onOpenModule(PracticeModules.Liuren) },
            )
        }

        Spacer(Modifier.height(2.dp))
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(7.dp),
            ) {
                Text("隐私与版权", style = MaterialTheme.typography.titleMedium)
                Text(
                    "App 不申请网络权限，不含广告、支付或推送。学习资料不会直接打进发行包；规则进入核心前先做来源、许可、流派和案例验证。",
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
    module: PracticeModule,
    modifier: Modifier = Modifier,
    onClick: () -> Unit,
) {
    val (status, action, highlighted) = when (module.stage) {
        ModuleStage.Ready -> Triple("可用", "开始排盘", true)
        ModuleStage.Foundation -> Triple("基础可用", "基础起局", true)
        ModuleStage.CorpusPrep -> Triple("资料准备", "查看接入进度", false)
    }
    OutlinedCard(modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(15.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Row(modifier = Modifier.fillMaxWidth()) {
                Text(module.title, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                Text(
                    status,
                    style = MaterialTheme.typography.labelLarge,
                    color = if (highlighted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Text(
                module.description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            TextButton(onClick = onClick) { Text(action) }
        }
    }
}
