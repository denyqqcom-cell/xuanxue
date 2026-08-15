package com.xuanxue.app

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.xuanxue.ai.QueryDomain

/**
 * 事占模块共用的现实问题输入。
 *
 * 它不是“让用户多填资料”，而是防止解释器脱离具体事体，仅凭盘面标签自动下结论。
 */
@Composable
fun QuestionContextCard(
    domain: QueryDomain,
    question: String,
    knownFacts: String,
    onDomainChange: (QueryDomain) -> Unit,
    onQuestionChange: (String) -> Unit,
    onKnownFactsChange: (String) -> Unit,
) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(9.dp),
        ) {
            Text("事体与现实条件", fontWeight = FontWeight.Bold)
            Text(
                "奇门、六爻、大六壬必须先知道你在问什么。未填写时只展示结构，不自动取用神/类神，也不判断成败或应期。",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Row(
                Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                QueryDomain.entries.forEach { item ->
                    FilterChip(
                        selected = item == domain,
                        onClick = { onDomainChange(item) },
                        label = { Text(item.label) },
                    )
                }
            }

            OutlinedTextField(
                value = question,
                onValueChange = { onQuestionChange(it.take(180)) },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("具体问题") },
                placeholder = { Text("例如：已拿到两个 offer，未来三个月是否适合换工作？") },
                minLines = 2,
                maxLines = 4,
            )

            OutlinedTextField(
                value = knownFacts,
                onValueChange = { onKnownFactsChange(it.take(240)) },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("已知现实条件（可选）") },
                placeholder = { Text("例如：当前工作稳定；新 offer 薪资更高但需异地；最晚下周答复。") },
                minLines = 2,
                maxLines = 4,
            )
        }
    }
}
