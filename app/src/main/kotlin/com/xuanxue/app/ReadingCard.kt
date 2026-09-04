package com.xuanxue.app

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.EvidenceGrade
import com.xuanxue.ai.MethodAuditRegistry
import com.xuanxue.ai.ProductProvenance
import com.xuanxue.ai.Reading
import com.xuanxue.ai.ReadingItem

/**
 * 离线解释卡：结论和“我们凭什么这样显示”放在同一处。
 *
 * 奇门产品层额外启用四类 provenance 分层。现实输入保持在四类之外，避免用户条件、
 * 盘面字段、来源规则、项目推论和未验证候选在 UI 上被呈现成同一证据层级。
 */
@Composable
fun ReadingCard(reading: Reading) {
    if (reading.items.isEmpty() && reading.contextSummary.isBlank()) return
    val audit = MethodAuditRegistry.byId(reading.toolName)
    val provenanceMode = reading.toolName == "qimen"

    Spacer(Modifier.height(12.dp))
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(9.dp),
        ) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(
                    if (provenanceMode) "解释与来源分层" else "离线解释",
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                )
                if (audit != null) {
                    Surface(
                        color = MaterialTheme.colorScheme.secondaryContainer,
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.wrapContentWidth(),
                    ) {
                        Text(
                            audit.maturity.label,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSecondaryContainer,
                        )
                    }
                }
            }

            if (reading.overall.isNotBlank()) {
                Text(
                    reading.overall,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            if (reading.contextSummary.isNotBlank()) {
                Surface(
                    color = MaterialTheme.colorScheme.primaryContainer,
                    shape = MaterialTheme.shapes.medium,
                ) {
                    Column(
                        Modifier.padding(10.dp),
                        verticalArrangement = Arrangement.spacedBy(5.dp),
                    ) {
                        Text(
                            "现实输入（不属于四类分析结论）",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(reading.contextSummary, fontSize = 14.sp, lineHeight = 21.sp)
                        if (reading.contextCaveat.isNotBlank()) {
                            Text(
                                reading.contextCaveat,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }

            if (provenanceMode) {
                Text(
                    "以下四类只表示信息性质，不表示吉凶强弱，也不能互相升格。",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                ProductProvenance.entries.forEach { provenance ->
                    val sectionItems = reading.items.filter { it.provenance == provenance }
                    ProvenanceSection(provenance, sectionItems)
                }
            } else {
                reading.items.forEach { item ->
                    ReadingItemSurface(item, item.evidenceGrade == EvidenceGrade.USER_CONTEXT)
                }
            }

            if (reading.caveats.isNotEmpty()) {
                Text("核验边界", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                reading.caveats.distinct().forEach { caveat ->
                    Text(
                        "• $caveat",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

@Composable
private fun ProvenanceSection(
    provenance: ProductProvenance,
    items: List<ReadingItem>,
) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(10.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                "${provenance.label} · ${items.size}",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
            )
            Text(
                provenance.description,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (items.isEmpty()) {
                Text(
                    "本次没有该类条目。",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            } else {
                items.forEach { item -> ReadingItemSurface(item, false) }
            }
        }
    }
}

@Composable
private fun ReadingItemSurface(item: ReadingItem, isUserContext: Boolean) {
    Surface(
        color = if (isUserContext) {
            MaterialTheme.colorScheme.primaryContainer
        } else {
            MaterialTheme.colorScheme.surfaceVariant
        },
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(
            Modifier.padding(10.dp),
            verticalArrangement = Arrangement.spacedBy(5.dp),
        ) {
            Text(
                "${item.title} · ${gradeLabel(item.evidenceGrade)}",
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.SemiBold,
            )
            Text(item.summary, fontSize = 14.sp, lineHeight = 21.sp)
            if (item.detail.isNotBlank()) {
                Text(item.detail, style = MaterialTheme.typography.bodySmall)
            }
            if (item.sourceIds.isNotEmpty()) {
                Text(
                    "来源：${item.sourceIds.joinToString(" · ")}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            if (item.caveat.isNotBlank()) {
                Text(
                    "边界：${item.caveat}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

private fun gradeLabel(grade: EvidenceGrade): String = when (grade) {
    EvidenceGrade.USER_CONTEXT -> "用户输入"
    EvidenceGrade.VERIFIED_FIXTURE -> "夹具核验"
    EvidenceGrade.SOURCE_DERIVED -> "来源可追溯"
    EvidenceGrade.TRADITIONAL_HEURISTIC -> "传统启发式"
    EvidenceGrade.EXPERIMENTAL -> "实验"
}
