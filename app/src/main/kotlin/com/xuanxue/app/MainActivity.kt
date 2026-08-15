package com.xuanxue.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ziwei.core.ZiweiAstro
import com.xuanxue.ziwei.core.ZiweiAstro.Astrolabe
import com.xuanxue.ziwei.core.ZiweiStars.Star
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            XuanxueTheme {
                XuanxueRoot()
            }
        }
    }
}

val SHICHEN = listOf(
    "早子时 00:00-01:00", "丑时 01:00-03:00", "寅时 03:00-05:00", "卯时 05:00-07:00",
    "辰时 07:00-09:00", "巳时 09:00-11:00", "午时 11:00-13:00", "未时 13:00-15:00",
    "申时 15:00-17:00", "酉时 17:00-19:00", "戌时 19:00-21:00", "亥时 21:00-23:00",
    "晚子时 23:00-00:00",
)

/** 命盘格子：地支方位固定。row/col 映射到 palaces 索引（寅=0…丑=11）。 */
val PAN_LAYOUT = listOf(
    listOf(3, 4, 5, 6),
    listOf(2, null, null, 7),
    listOf(1, null, null, 8),
    listOf(0, 11, 10, 9),
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun XuanxueApp() {
    var solarDate by remember { mutableStateOf("1990-05-20") }
    var timeIndex by remember { mutableStateOf(6) }
    var gender by remember { mutableStateOf("male") }
    var fixLeap by remember { mutableStateOf(false) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<Astrolabe?>(null) }
    var selectedPalaceIndex by remember { mutableStateOf(0) }

    val datePickerState = rememberDatePickerState(initialSelectedDateMillis = millisOf("1990-05-20"))

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("紫微斗数") })
        },
    ) { pad ->
        Column(
            modifier = Modifier
                .padding(pad)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("公历生日", fontWeight = FontWeight.Bold)
                        Spacer(Modifier.width(12.dp))
                        Text(solarDate, Modifier.clickable { showDatePicker = true })
                    }
                    Text("时辰", fontWeight = FontWeight.Bold)
                    Row(
                        Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState()),
                    ) {
                        SHICHEN.forEachIndexed { i, label ->
                            FilterChip(
                                selected = timeIndex == i,
                                onClick = { timeIndex = i },
                                label = { Text(label.split(" ")[0]) },
                                modifier = Modifier.padding(end = 4.dp),
                            )
                        }
                    }
                    Text("性别", fontWeight = FontWeight.Bold)
                    Row {
                        FilterChip(selected = gender == "male", onClick = { gender = "male" }, label = { Text("男") })
                        Spacer(Modifier.width(8.dp))
                        FilterChip(selected = gender == "female", onClick = { gender = "female" }, label = { Text("女") })
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        FilterChip(
                            selected = fixLeap,
                            onClick = { fixLeap = !fixLeap },
                            label = { Text("闰月修正") },
                        )
                        Spacer(Modifier.width(8.dp))
                        Button(onClick = {
                            val next = ZiweiAstro.bySolar(solarDate, timeIndex, gender, fixLeap)
                            chart = next
                            selectedPalaceIndex = next.palaces.indexOfFirst { it.name == "命宫" }.coerceAtLeast(0)
                        }) { Text("排盘") }
                    }
                }
            }

            val a = chart
            if (a != null) {
                HeaderInfo(a)
                Text(
                    "十二宫概览 · 点击宫位查看完整星曜与限运",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                PanGrid(
                    a = a,
                    selectedIndex = selectedPalaceIndex,
                    onSelect = { selectedPalaceIndex = it },
                )
                PalaceDetail(a.palaces[selectedPalaceIndex.coerceIn(a.palaces.indices)])
                ReadingCard(com.xuanxue.ai.XuanxueAI.ziwei(a))
            } else {
                Text("输入信息后点击「排盘」", Modifier.padding(16.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }

    if (showDatePicker) {
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    datePickerState.selectedDateMillis?.let { solarDate = fmt(it) }
                    showDatePicker = false
                }) { Text("确定") }
            },
            dismissButton = { TextButton(onClick = { showDatePicker = false }) { Text("取消") } },
        ) { DatePicker(state = datePickerState) }
    }
}

@Composable
fun HeaderInfo(a: Astrolabe) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(
                "${a.gender}命 · ${a.solarDate} · ${a.time}（${a.timeRange}）",
                fontWeight = FontWeight.Bold,
            )
            Text("农历 ${a.lunarDate} · 命宫干支 ${a.chineseGanZhi()}")
            Text("五行局：${a.fiveElementsClass}    命主：${a.soul}    身主：${a.body}")
        }
    }
}

/** 这里只返回命宫的天干地支，避免把它误标成整盘“四柱干支”。 */
fun Astrolabe.chineseGanZhi(): String {
    val soul = palaces.first { it.name == "命宫" }
    return "${soul.heavenlyStem}${soul.earthlyBranch}"
}

@Composable
fun PanGrid(
    a: Astrolabe,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
) {
    Column(Modifier.fillMaxWidth()) {
        PAN_LAYOUT.forEach { row ->
            Row(Modifier.fillMaxWidth()) {
                row.forEach { idx ->
                    if (idx == null) {
                        Spacer(Modifier.weight(1f).aspectRatio(1f))
                    } else {
                        PanCell(
                            p = a.palaces[idx],
                            selected = selectedIndex == idx,
                            onClick = { onSelect(idx) },
                            modifier = Modifier.weight(1f).aspectRatio(1f),
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun PanCell(
    p: ZiweiAstro.Palace,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val isSoul = p.name == "命宫"
    val background = when {
        selected -> MaterialTheme.colorScheme.tertiaryContainer
        isSoul -> MaterialTheme.colorScheme.primaryContainer
        p.isBodyPalace -> MaterialTheme.colorScheme.secondaryContainer
        else -> MaterialTheme.colorScheme.surface
    }
    val borderColor = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline
    val borderWidth = if (selected) 2.dp else 1.dp

    Box(
        modifier
            .padding(1.dp)
            .background(background)
            .border(BorderStroke(borderWidth, borderColor))
            .clickable(onClick = onClick)
            .padding(4.dp),
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(1.dp)) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(
                    p.name + if (p.isBodyPalace) "·身" else "",
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp,
                )
                Text(
                    p.earthlyBranch,
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Text(
                "${p.heavenlyStem}${p.earthlyBranch}",
                fontSize = 10.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (p.majorStars.isEmpty()) {
                Text("无主星", fontSize = 9.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                p.majorStars.take(3).forEach { star ->
                    Text(
                        fmtStar(star),
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 10.sp,
                        color = if (star.mutagen == "忌") MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary,
                        maxLines = 1,
                    )
                }
                if (p.majorStars.size > 3) {
                    Text("+${p.majorStars.size - 3} 主星", fontSize = 9.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            Spacer(Modifier.weight(1f))
            p.decadal?.let {
                Text(
                    "大限 ${it.range[0]}-${it.range[1]}",
                    fontSize = 9.sp,
                    color = MaterialTheme.colorScheme.secondary,
                )
            }
        }
    }
}

@Composable
fun PalaceDetail(p: ZiweiAstro.Palace) {
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(7.dp),
        ) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(
                    "${p.name}${if (p.isBodyPalace) "（身宫）" else ""}",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    "${p.heavenlyStem}${p.earthlyBranch}",
                    style = MaterialTheme.typography.titleSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            p.decadal?.let {
                Text("大限：${it.range[0]}-${it.range[1]} 岁", style = MaterialTheme.typography.bodySmall)
            }

            StarGroup("主星", p.majorStars)
            StarGroup("辅星", p.minorStars)
            StarGroup("杂曜", p.adjectiveStars)

            p.ages?.takeIf { it.isNotEmpty() }?.let { ages ->
                Text("小限", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.labelLarge)
                Text(
                    ages.take(12).joinToString("、"),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            Text(
                "这里先展示盘面结构与实现结果；星曜、四化、宫位不会被单独翻译成确定人格或具体事件。",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun StarGroup(title: String, stars: List<Star>) {
    if (stars.isEmpty()) return
    Text(title, fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.labelLarge)
    Text(
        stars.joinToString("　") { fmtStar(it) },
        style = MaterialTheme.typography.bodySmall,
        lineHeight = 19.sp,
    )
}

fun fmtStar(s: Star): String = buildString {
    append(s.name)
    if (s.brightness.isNotEmpty()) append("·${s.brightness}")
    if (s.mutagen.isNotEmpty()) append("·${s.mutagen}")
}

fun millisOf(dateStr: String): Long {
    val c = Calendar.getInstance()
    val parts = dateStr.split("-").map { it.toInt() }
    c.set(parts[0], parts[1] - 1, parts[2])
    return c.timeInMillis
}

fun fmt(millis: Long): String = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date(millis))
