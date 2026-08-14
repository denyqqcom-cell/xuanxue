package com.xuanxue.app

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.qimen.QimenEngine.QimenChart
import java.util.Calendar

/** 奇门遁甲排盘页。完整九宫当前按实验能力展示，不冒充黄金夹具已核验。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QimenScreen() {
    var year by remember { mutableStateOf(2026) }
    var month by remember { mutableStateOf(8) }
    var day by remember { mutableStateOf(12) }
    var hour by remember { mutableStateOf(15) }
    var minute by remember { mutableStateOf(37) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<QimenChart?>(null) }

    Column(
        Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("奇门遁甲", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)

        Surface(
            color = MaterialTheme.colorScheme.errorContainer,
            shape = MaterialTheme.shapes.large,
        ) {
            Column(
                Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                Text(
                    "实验九宫 · 不作为已核验标准盘",
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                )
                Text(
                    "handoff/qimen 当前有 17 条历法/表/映射夹具，但完整九宫黄金盘为 0；地盘走法与人盘方向仍有资料冲突。因此可以查看当前实现用于工程核对，但离线解释不会据此直接断成败、吉凶或应期。",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                )
            }
        }

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(
                Modifier.padding(12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历: $year-$month-$day  $hour:${"%02d".format(minute)}", Modifier.weight(1f))
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }
                Text("时辰快捷选择", fontWeight = FontWeight.SemiBold)
                Row(
                    Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                ) {
                    listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22).forEach { h ->
                        TextButton(onClick = { hour = h; minute = 30 }) {
                            Text(
                                "%02d:30".format(h),
                                color = if (hour == h) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 12.sp,
                            )
                        }
                    }
                }
                Button(
                    onClick = { chart = QimenEngine.bySolar(year, month, day, hour, minute) },
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text("生成当前实验局")
                }
            }
        }

        chart?.let { c ->
            QimenResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.qimen(c))
        }
    }

    if (showDatePicker) {
        val today = Calendar.getInstance()
        val state = rememberDatePickerState(initialSelectedDateMillis = runCatching {
            java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse("$year-$month-$day")!!.time
        }.getOrDefault(System.currentTimeMillis()).coerceIn(
            java.text.SimpleDateFormat("yyyy", java.util.Locale.US).parse("1900")!!.time,
            today.timeInMillis,
        ))
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    state.selectedDateMillis?.let { ms ->
                        val cal = Calendar.getInstance().apply { timeInMillis = ms }
                        year = cal.get(Calendar.YEAR)
                        month = cal.get(Calendar.MONTH) + 1
                        day = cal.get(Calendar.DAY_OF_MONTH)
                    }
                    showDatePicker = false
                }) { Text("确定") }
            },
            dismissButton = { TextButton(onClick = { showDatePicker = false }) { Text("取消") } },
        ) { DatePicker(state = state) }
    }
}

@Composable
fun QimenResult(c: QimenChart) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(
                Modifier.padding(12.dp),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Text("基础结果", fontWeight = FontWeight.Bold)
                Text("农历: ${c.lunarDateStr}", fontSize = 14.sp)
                Text("四柱: ${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}", fontSize = 14.sp)
                Text("节气: ${c.jieQi}", fontSize = 14.sp)
                Text("局: ${c.juText}", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                Text("旬首: ${c.xunShou}遁${c.dunGan}   旬空: ${c.xunKong.joinToString("、")}", fontSize = 14.sp)
                Text("马星: ${c.maXing}", fontSize = 14.sp)
                Text(
                    "值符/值使与下方九宫来自当前实验旋转实现，尚未通过完整九宫黄金夹具。",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.error,
                )
                Text("实验值符: ${c.zhiFu}   实验值使: ${c.zhiShi}", fontSize = 14.sp)
            }
        }

        Text("实验九宫（开发核对视图）", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        val layout = listOf(listOf(4, 9, 2), listOf(3, 5, 7), listOf(8, 1, 6))
        val byPalace = c.gongs.associateBy { it.palace }
        layout.forEach { row ->
            Row(Modifier.fillMaxWidth()) {
                row.forEach { p ->
                    val g = byPalace[p]
                    val cellBackground = when {
                        g?.isMaXing == true -> MaterialTheme.colorScheme.secondaryContainer
                        g?.isKong == true -> MaterialTheme.colorScheme.surfaceVariant
                        else -> MaterialTheme.colorScheme.surface
                    }
                    Box(
                        Modifier
                            .weight(1f)
                            .padding(2.dp)
                            .aspectRatio(1f)
                            .border(1.dp, MaterialTheme.colorScheme.outline, MaterialTheme.shapes.small)
                            .background(cellBackground)
                            .padding(4.dp),
                    ) {
                        Column {
                            Row {
                                Text("$p", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Spacer(Modifier.weight(1f))
                                if (g?.isMaXing == true) Text("马", fontSize = 10.sp, color = MaterialTheme.colorScheme.secondary)
                                if (g?.isKong == true) Text("空", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            g?.diGan?.let {
                                Text(
                                    it,
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                            g?.tianXing?.takeIf { it.isNotBlank() }?.let {
                                Text("星 $it", fontSize = 11.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                            }
                            g?.renMen?.takeIf { it.isNotBlank() }?.let {
                                Text("门 $it", fontSize = 11.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                            }
                            g?.shenPan?.takeIf { it.isNotBlank() }?.let {
                                Text("神 $it", fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                            }
                        }
                    }
                }
            }
        }
        Text(
            "工程状态来源：handoff/qimen/HANDOFF_SUMMARY.md、04_CONFLICTS.md、05_FIXTURES.jsonl。研究资料本身不会打包进 APK。",
            fontSize = 11.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
