package com.xuanxue.app.ui.module

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.xuanxue.app.domain.PracticeModule
import com.xuanxue.app.ui.components.XuanxueTopBar

@Composable
fun ModuleIntroScreen(
    module: PracticeModule,
    onBack: () -> Unit,
) {
    Column(modifier = Modifier.fillMaxSize()) {
        XuanxueTopBar(title = module.title, onBack = onBack)
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Surface(
                color = MaterialTheme.colorScheme.primaryContainer,
                shape = MaterialTheme.shapes.large,
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text(module.title, style = MaterialTheme.typography.headlineMedium)
                    Text(module.description, style = MaterialTheme.typography.bodyMedium)
                    Text(
                        "已纳入 App 主架构 · 核心算法等待资料验证后接入",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary,
                    )
                }
            }

            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("当前需要完成", style = MaterialTheme.typography.titleMedium)
                    Text(
                        module.corpusRequest,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("接入标准", style = MaterialTheme.typography.titleMedium)
                    Text("① 原始资料可追溯；② 流派差异不强行混合；③ 排盘规则必须可计算；④ 断法规则与案例分开；⑤ 有黄金夹具或可复现命例后才标记为“可用”。")
                    Text(
                        "学习资料不会直接打进发行包。最终 App 只使用经过版权审查、重新结构化后的规则与必要数据。",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            TextButton(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
                Text("返回排盘工具")
            }
        }
    }
}
