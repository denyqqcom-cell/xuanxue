package com.xuanxue.app

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
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
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.xuanxue.ai.MethodAudit
import com.xuanxue.ai.MethodAuditRegistry
import com.xuanxue.ai.MethodMaturity

private enum class RootPage {
    HOME,
    ZIWEI,
    BAZI,
    QIMEN,
    LIUYAO,
    LIUREN,
    HUANGLI,
    AUDIT,
}

private data class ModuleEntry(
    val page: RootPage,
    val id: String,
    val title: String,
    val subtitle: String,
)

private val moduleEntries = listOf(
    ModuleEntry(RootPage.ZIWEI, "ziwei", "紫微斗数", "十二宫 · 星曜 · 四化 · 大限"),
    ModuleEntry(RootPage.BAZI, "bazi", "八字", "四柱 · 藏干 · 十神 · 大运"),
    ModuleEntry(RootPage.QIMEN, "qimen", "奇门遁甲", "历法基础已核验 · 九宫仍实验"),
    ModuleEntry(RootPage.LIUYAO, "liuyao", "六爻", "纳甲 · 世应 · 动爻 · 变卦"),
    ModuleEntry(RootPage.LIUREN, "liuren", "大六壬", "四课 · 三传 · 九宗门 · 天将"),
    ModuleEntry(RootPage.HUANGLI, "huangli", "黄历", "宜忌 · 吉神凶煞 · 冲煞"),
)

/**
 * App 根导航。
 *
 * 旧版把六个模块硬塞在一行 Tab；这里改为首页卡片 + 独立页面，方便后续继续增加
 * 核验状态、案例工作流和 BYOK，而不是让导航宽度随功能数失控。
 */
@Composable
fun XuanxueRoot() {
    var page by remember { mutableStateOf(RootPage.HOME) }
    BackHandler(enabled = page != RootPage.HOME) { page = RootPage.HOME }

    when (page) {
        RootPage.HOME -> HomeHub(
            onOpen = { page = it },
            onAudit = { page = RootPage.AUDIT },
        )
        RootPage.AUDIT -> AuditCenter(onBack = { page = RootPage.HOME })
        else -> ModuleHost(
            page = page,
            onBack = { page = RootPage.HOME },
        )
    }
}

@Composable
private fun HomeHub(
    onOpen: (RootPage) -> Unit,
    onAudit: () -> Unit,
) {
    Scaffold { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(paddingValues)
                .padding(horizontal = 18.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Surface(
                color = MaterialTheme.colorScheme.primaryContainer,
                shape = MaterialTheme.shapes.extraLarge,
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("玄学工具箱", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                    Text(
                        "排盘、资料核验与解释层分开管理。能证明到哪一层，就只开放到哪一层；传统解释不会伪装成算法事实。",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                    Button(onClick = onAudit) { Text("查看方法核验中心") }
                }
            }

            Text("排盘与历法", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            moduleEntries.forEach { entry ->
                val audit = MethodAuditRegistry.byId(entry.id)
                ModuleCard(entry = entry, audit = audit, onClick = { onOpen(entry.page) })
            }

            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(
                    Modifier.padding(15.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Text("本地优先", fontWeight = FontWeight.Bold)
                    Text(
                        "当前版本不需要账号、广告或自有服务器。离线解释只消费本机排盘结果；未来若加入 BYOK，必须继续经过逐次数据预览与目标授权。",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

@Composable
private fun ModuleCard(
    entry: ModuleEntry,
    audit: MethodAudit?,
    onClick: () -> Unit,
) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(15.dp),
            verticalArrangement = Arrangement.spacedBy(7.dp),
        ) {
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(entry.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                if (audit != null) {
                    Text(
                        audit.maturity.label,
                        style = MaterialTheme.typography.labelMedium,
                        color = maturityColor(audit.maturity),
                    )
                }
            }
            Text(entry.subtitle, style = MaterialTheme.typography.bodyMedium)
            audit?.let {
                Text(
                    it.summary,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            TextButton(onClick = onClick) { Text("打开") }
        }
    }
}

@Composable
private fun ModuleHost(page: RootPage, onBack: () -> Unit) {
    val title = moduleEntries.firstOrNull { it.page == page }?.title ?: "模块"
    Column(Modifier.fillMaxSize()) {
        Surface(color = MaterialTheme.colorScheme.surfaceVariant) {
            Row(
                Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                OutlinedButton(onClick = onBack) { Text("返回首页") }
                Text(
                    title,
                    modifier = Modifier.padding(top = 10.dp),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
            }
        }
        Box(Modifier.weight(1f)) {
            when (page) {
                RootPage.ZIWEI -> XuanxueApp()
                RootPage.BAZI -> BaziScreen()
                RootPage.QIMEN -> QimenScreen()
                RootPage.LIUYAO -> LiuYaoScreen()
                RootPage.LIUREN -> LiuRenScreen()
                RootPage.HUANGLI -> HuangLiScreen()
                else -> Unit
            }
        }
    }
}

@Composable
private fun AuditCenter(onBack: () -> Unit) {
    Scaffold { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(paddingValues)
                .padding(horizontal = 18.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("方法核验中心", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                OutlinedButton(onClick = onBack) { Text("返回") }
            }
            Text(
                "这里展示的是当前仓库的工程核验成熟度，不是对术数作科学有效性背书。测试通过、书例对齐、上游一致性三者也不会被混写成同一种证据。",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            MethodAuditRegistry.all.forEach { audit -> AuditCard(audit) }
        }
    }
}

@Composable
private fun AuditCard(audit: MethodAudit) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(15.dp),
            verticalArrangement = Arrangement.spacedBy(7.dp),
        ) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(audit.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(audit.maturity.label, style = MaterialTheme.typography.labelMedium, color = maturityColor(audit.maturity))
            }
            Text(audit.summary, style = MaterialTheme.typography.bodyMedium)
            if (audit.verified.isNotEmpty()) {
                Text("已核验", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                audit.verified.forEach { Text("• $it", style = MaterialTheme.typography.bodySmall) }
            }
            if (audit.limitations.isNotEmpty()) {
                Text("边界 / 未解决", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                audit.limitations.forEach {
                    Text("• $it", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            if (audit.sourceIds.isNotEmpty()) {
                Text(
                    "证据索引：${audit.sourceIds.joinToString(" · ")}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun maturityColor(maturity: MethodMaturity) = when (maturity) {
    MethodMaturity.IMPLEMENTATION_PARITY -> MaterialTheme.colorScheme.primary
    MethodMaturity.SOURCE_BACKED -> MaterialTheme.colorScheme.primary
    MethodMaturity.PARTIAL_FIXTURES -> MaterialTheme.colorScheme.tertiary
    MethodMaturity.INTERNAL_REGRESSION -> MaterialTheme.colorScheme.tertiary
    MethodMaturity.EXPERIMENTAL -> MaterialTheme.colorScheme.error
}
