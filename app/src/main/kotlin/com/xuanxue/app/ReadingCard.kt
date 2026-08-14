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
import com.xuanxue.ai.Reading

/**
 * 离线解释卡：结论和“我们凭什么这样显示”放在同一处。
 */
@Composable
fun ReadingCard(reading: Reading) {
    if (reading.items.isEmpty()) return
    val audit = MethodAuditRegistry.byId(reading.toolName)

    Spacer(Modifier.height(12.dp))
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(9.dp),
        ) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("离线解释", fontWeight = FontWeight.Bold, fontSize = 15.sp)
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

            reading.items.forEach { item ->
                val isUserContext = item.evidenceGrade == EvidenceGrade.USER_CONTEXT
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

private fun gradeLabel(grade: EvidenceGrade): String = when (grade) {
    EvidenceGrade.USER_CONTEXT -> "用户输入"
    EvidenceGrade.VERIFIED_FIXTURE -> "夹具核验"
    EvidenceGrade.SOURCE_DERIVED -> "来源可追溯"
    EvidenceGrade.TRADITIONAL_HEURISTIC -> "传统启发式"
    EvidenceGrade.EXPERIMENTAL -> "实验"
}
