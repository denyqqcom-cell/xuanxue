package com.xuanxue.app.ui.chart

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.app.ui.components.ScreenTopBar
import com.xuanxue.app.ui.components.SectionTitle
import com.xuanxue.ziwei.core.ZiweiAstro
import com.xuanxue.ziwei.core.ZiweiStars

@Composable
fun ChartScreen(
    profile: BirthProfile,
    chart: ZiweiAstro.Astrolabe,
    onBack: () -> Unit,
    onEdit: () -> Unit,
) {
    val initialIndex = chart.palaces.indexOfFirst { it.name == "命宫" }.coerceAtLeast(0)
    var selectedIndex by remember(chart) { mutableStateOf(initialIndex) }
    val selectedPalace = chart.palaces[selectedIndex]

    Column(Modifier.fillMaxSize()) {
        ScreenTopBar(
            title = "紫微命盘",
            subtitle = "${profile.solarDate} · ${profile.timeLabel.substringBefore(" ")}",
            onBack = onBack,
            actionLabel = "编辑",
            onAction = onEdit,
        )
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            HeaderSummary(profile, chart)
            SectionTitle("十二宫", "先看主星与四化，点宫位再展开全部细节")
            ZiweiBoard(
                chart = chart,
                selectedIndex = selectedIndex,
                onSelect = { selectedIndex = it },
            )
            PalaceDetail(selectedPalace)
            Spacer(Modifier.height(18.dp))
        }
    }
}

@Composable
private fun HeaderSummary(profile: BirthProfile, chart: ZiweiAstro.Astrolabe) {
    val soulPalace = chart.palaces.firstOrNull { it.name == "命宫" }
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                "${profile.genderLabel}命 · ${profile.solarDate} · ${profile.timeLabel}",
                style = MaterialTheme.typography.titleMedium,
            )
            Text(
                "农历 ${chart.lunarDate}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                SummaryMetric("五行局", chart.fiveElementsClass, Modifier.weight(1f))
                SummaryMetric("命主", chart.soul, Modifier.weight(1f))
                SummaryMetric("身主", chart.body, Modifier.weight(1f))
            }
            if (soulPalace != null) {
                Text(
                    "命宫 ${soulPalace.heavenlyStem}${soulPalace.earthlyBranch}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun SummaryMetric(label: String, value: String, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = MaterialTheme.shapes.small,
    ) {
        Column(Modifier.padding(horizontal = 10.dp, vertical = 9.dp)) {
            Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(value, style = MaterialTheme.typography.titleMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

@Composable
private fun ZiweiBoard(
    chart: ZiweiAstro.Astrolabe,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
) {
    Column(Modifier.fillMaxWidth()) {
        BoardRow(listOf(3, 4, 5, 6), chart, selectedIndex, onSelect)
        Row(Modifier.fillMaxWidth()) {
            Column(Modifier.weight(1f)) {
                PalaceCell(chart.palaces[2], selectedIndex == 2, onSelect, Modifier.fillMaxWidth().aspectRatio(1f))
                PalaceCell(chart.palaces[1], selectedIndex == 1, onSelect, Modifier.fillMaxWidth().aspectRatio(1f))
            }
            BoardCenter(
                chart = chart,
                selected = chart.palaces[selectedIndex],
                modifier = Modifier.weight(2f).aspectRatio(1f),
            )
            Column(Modifier.weight(1f)) {
                PalaceCell(chart.palaces[7], selectedIndex == 7, onSelect, Modifier.fillMaxWidth().aspectRatio(1f))
                PalaceCell(chart.palaces[8], selectedIndex == 8, onSelect, Modifier.fillMaxWidth().aspectRatio(1f))
            }
        }
        BoardRow(listOf(0, 11, 10, 9), chart, selectedIndex, onSelect)
    }
}

@Composable
private fun BoardRow(
    indices: List<Int>,
    chart: ZiweiAstro.Astrolabe,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
) {
    Row(Modifier.fillMaxWidth()) {
        indices.forEach { index ->
            PalaceCell(
                palace = chart.palaces[index],
                selected = selectedIndex == index,
                onSelect = onSelect,
                modifier = Modifier.weight(1f).aspectRatio(1f),
            )
        }
    }
}

@Composable
private fun PalaceCell(
    palace: ZiweiAstro.Palace,
    selected: Boolean,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    val background = when {
        selected -> MaterialTheme.colorScheme.primaryContainer
        palace.name == "命宫" -> MaterialTheme.colorScheme.secondaryContainer
        palace.isBodyPalace -> MaterialTheme.colorScheme.surfaceVariant
        else -> MaterialTheme.colorScheme.surface
    }
    Surface(
        modifier = modifier
            .padding(1.5.dp)
            .clickable { onSelect(palace.index) },
        color = background,
        shape = MaterialTheme.shapes.extraSmall,
        border = BorderStroke(
            width = if (selected) 2.dp else 1.dp,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline,
        ),
    ) {
        Column(
            modifier = Modifier.padding(6.dp),
            verticalArrangement = Arrangement.spacedBy(1.dp),
        ) {
            Text(
                palace.name + if (palace.isBodyPalace) " · 身" else "",
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
            Text(
                "${palace.heavenlyStem}${palace.earthlyBranch}",
                fontSize = 9.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            palace.majorStars.take(2).forEach { star ->
                Text(
                    compactStar(star),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (star.mutagen == "忌") MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            if (palace.majorStars.size > 2) {
                Text(
                    "+${palace.majorStars.size - 2} 主星",
                    fontSize = 8.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            palace.decadal?.let {
                Text(
                    "${it.range[0]}–${it.range[1]}",
                    fontSize = 8.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                )
            }
        }
    }
}

@Composable
private fun BoardCenter(
    chart: ZiweiAstro.Astrolabe,
    selected: ZiweiAstro.Palace,
    modifier: Modifier = Modifier,
) {
    Surface(
        modifier = modifier.padding(2.dp),
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text("紫微斗数", style = MaterialTheme.typography.titleLarge)
            Text(
                chart.fiveElementsClass,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Text("命主 ${chart.soul} · 身主 ${chart.body}", style = MaterialTheme.typography.bodySmall)
            Spacer(Modifier.height(2.dp))
            Text(
                "当前：${selected.name}",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.secondary,
            )
            Text(
                "点任一宫位查看完整星曜与运限",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun PalaceDetail(palace: ZiweiAstro.Palace) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(Modifier.fillMaxWidth()) {
                Column(Modifier.weight(1f)) {
                    Text(
                        palace.name + if (palace.isBodyPalace) " · 身宫" else "",
                        style = MaterialTheme.typography.headlineSmall,
                    )
                    Text(
                        "${palace.heavenlyStem}${palace.earthlyBranch}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                palace.decadal?.let {
                    Text(
                        "大限 ${it.range[0]}–${it.range[1]} 岁",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.secondary,
                    )
                }
            }

            StarGroup("主星", palace.majorStars)
            StarGroup("辅星", palace.minorStars)
            StarGroup("杂曜", palace.adjectiveStars)

            Text(
                "长生：${palace.changsheng12}　博士：${palace.boshi12}　岁前：${palace.suiqian12}　将前：${palace.jiangqian12}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            palace.ages?.let { ages ->
                if (ages.isNotEmpty()) {
                    Text(
                        "小限：${ages.joinToString("、")}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

@Composable
private fun StarGroup(title: String, stars: List<ZiweiStars.Star>) {
    if (stars.isEmpty()) return
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(title, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text(
            stars.joinToString("　") { detailedStar(it) },
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}

private fun compactStar(star: ZiweiStars.Star): String = buildString {
    append(star.name)
    if (star.mutagen.isNotEmpty()) append("·${star.mutagen}")
}

private fun detailedStar(star: ZiweiStars.Star): String = buildString {
    append(star.name)
    if (star.brightness.isNotEmpty()) append("·${star.brightness}")
    if (star.mutagen.isNotEmpty()) append("·${star.mutagen}")
}
