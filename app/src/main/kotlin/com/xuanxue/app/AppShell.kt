package com.xuanxue.app

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
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
    LEGAL,
}

private data class ModuleEntry(
    val page: RootPage,
    val id: String,
    val title: String,
    val subtitle: String,
    val badge: String,
)

private val moduleEntries = listOf(
    ModuleEntry(RootPage.ZIWEI, "ziwei", "紫微斗数", "十二宫 · 星曜 · 四化 · 大限", "离线排盘"),
    ModuleEntry(RootPage.BAZI, "bazi", "八字", "四柱 · 藏干 · 十神 · 大运", "离线排盘"),
    ModuleEntry(RootPage.QIMEN, "qimen", "奇门遁甲", "九宫 · 九星 · 八门 · 定元选择", "多流派 · 实验"),
    ModuleEntry(RootPage.LIUYAO, "liuyao", "六爻", "本卦 · 变卦 · 纳甲 · 世应", "纳甲排卦"),
    ModuleEntry(RootPage.LIUREN, "liuren", "大六壬", "四课 · 三传 · 九宗门 · 天将", "书例核对"),
    ModuleEntry(RootPage.HUANGLI, "huangli", "黄历", "宜忌 · 吉神凶煞 · 冲煞", "本地历法"),
)

/** App 根导航：模块发现、方法核验、合规入口和响应式布局统一管理。 */
@Composable
fun XuanxueRoot() {
    var page by remember { mutableStateOf(RootPage.HOME) }
    BackHandler(enabled = page != RootPage.HOME) { page = RootPage.HOME }

    when (page) {
        RootPage.HOME -> HomeHub(
            onOpen = { page = it },
            onAudit = { page = RootPage.AUDIT },
            onLegal = { page = RootPage.LEGAL },
        )
        RootPage.AUDIT -> AuditCenter(onBack = { page = RootPage.HOME })
        RootPage.LEGAL -> OpenSourceScreen(onBack = { page = RootPage.HOME })
        else -> ModuleHost(page = page, onBack = { page = RootPage.HOME })
    }
}

@Composable
private fun HomeHub(
    onOpen: (RootPage) -> Unit,
    onAudit: () -> Unit,
    onLegal: () -> Unit,
) {
    Scaffold { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .testTag("home-root"),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .widthIn(max = 1120.dp)
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
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
                            "六术离线排盘，命例不上传、不需要账号。排盘结构、传统解释与方法来源分层呈现，需要深挖时再进入核验中心。",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                        )
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Button(onClick = onAudit, modifier = Modifier.testTag("open-audit")) { Text("方法核验中心") }
                            OutlinedButton(onClick = onLegal, modifier = Modifier.testTag("open-legal")) { Text("开源许可") }
                        }
                    }
                }

                Text("排盘与历法", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                ResponsiveModuleGrid(onOpen)

                OutlinedCard(Modifier.fillMaxWidth().testTag("privacy-card")) {
                    Column(
                        Modifier.padding(15.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        Text("纯净离线", fontWeight = FontWeight.Bold)
                        Text(
                            "不含广告，不要求登录，排盘在本机完成。方法来源、验证范围和未解决分歧集中放在核验中心，首页只保留使用时真正需要的信息。",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ResponsiveModuleGrid(onOpen: (RootPage) -> Unit) {
    BoxWithConstraints(Modifier.fillMaxWidth()) {
        val twoColumns = maxWidth >= 720.dp
        if (!twoColumns) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                moduleEntries.forEach { entry ->
                    ModuleCard(
                        entry = entry,
                        onClick = { onOpen(entry.page) },
                    )
                }
            }
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                moduleEntries.chunked(2).forEach { entries ->
                    Row(
                        Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        entries.forEach { entry ->
                            ModuleCard(
                                entry = entry,
                                onClick = { onOpen(entry.page) },
                                modifier = Modifier.weight(1f),
                            )
                        }
                        if (entries.size == 1) Spacer(Modifier.weight(1f))
                    }
                }
            }
        }
    }
}

@Composable
private fun ModuleCard(
    entry: ModuleEntry,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    OutlinedCard(modifier.fillMaxWidth().testTag("module-card-${entry.id}")) {
        Column(
            Modifier.padding(15.dp),
            verticalArrangement = Arrangement.spacedBy(7.dp),
        ) {
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(entry.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(
                    entry.badge,
                    modifier = Modifier.testTag("module-badge-${entry.id}"),
                    style = MaterialTheme.typography.labelMedium,
                    color = if (entry.id == "qimen") MaterialTheme.colorScheme.tertiary else MaterialTheme.colorScheme.primary,
                )
            }
            Text(entry.subtitle, style = MaterialTheme.typography.bodyMedium)
            TextButton(onClick = onClick, modifier = Modifier.testTag("module-open-${entry.id}")) { Text("进入排盘") }
        }
    }
}

@Composable
private fun ModuleHost(page: RootPage, onBack: () -> Unit) {
    val entry = moduleEntries.firstOrNull { it.page == page }
    val title = entry?.title ?: "模块"
    val pageId = entry?.id ?: "unknown"
    Column(Modifier.fillMaxSize().testTag("module-host-$pageId")) {
        Surface(color = MaterialTheme.colorScheme.surfaceVariant) {
            Row(
                Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                OutlinedButton(onClick = onBack, modifier = Modifier.testTag("back-home")) { Text("返回首页") }
                Text(
                    title,
                    modifier = Modifier.padding(top = 10.dp),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
            }
        }
        Box(
            Modifier
                .weight(1f)
                .fillMaxWidth(),
            contentAlignment = Alignment.TopCenter,
        ) {
            Box(
                Modifier
                    .widthIn(max = 1120.dp)
                    .fillMaxWidth(),
            ) {
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
}

@Composable
private fun AuditCenter(onBack: () -> Unit) {
    Scaffold { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .testTag("audit-root"),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .widthIn(max = 900.dp)
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 18.dp, vertical = 14.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("方法核验中心", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                    OutlinedButton(onClick = onBack, modifier = Modifier.testTag("audit-back-home")) { Text("返回") }
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
