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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.QueryDomain
import com.xuanxue.ai.ReadingContext
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.qimen.QimenEngine.QimenChart
import java.util.Calendar

/** 奇门遁甲排盘页。完整九宫当前按实验能力展示，不冒充黄金夹具已核验。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QimenScreen() {
    val now = remember { Calendar.getInstance() }
    var year by remember { mutableStateOf(now.get(Calendar.YEAR)) }
    var month by remember { mutableStateOf(now.get(Calendar.MONTH) + 1) }
    var day by remember { mutableStateOf(now.get(Calendar.DAY_OF_MONTH)) }
    var hour by remember { mutableStateOf(now.get(Calendar.HOUR_OF_DAY)) }
    var minute by remember { mutableStateOf(now.get(Calendar.MINUTE)) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<QimenChart?>(null) }

    var queryDomain by remember { mutableStateOf(QueryDomain.GENERAL) }
    var question by remember { mutableStateOf("") }
    var knownFacts by remember { mutableStateOf("") }

    val readingContext = ReadingContext(
        domain = queryDomain,
        question = question,
        knownFacts = knownFacts,
    )

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
                    "handoff/qimen 当前只有历法/旬法/表/映射夹具，完整九宫黄金盘仍为 0；地盘 walk 与人盘方向仍有来源冲突。当前九宫只用于工程核对，结构测试通过不等于完整盘法已经术理验真。",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                )
            }
        }

        QuestionContextCard(
            domain = queryDomain,
            question = question,
            knownFacts = knownFacts,
            onDomainChange = { queryDomain = it },
            onQuestionChange = { question = it },
            onKnownFactsChange = { knownFacts = it },
        )

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
            ReadingCard(com.xuanxue.ai.XuanxueAI.qimen(c, readingContext))
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
                Text("局: ${c.juText}", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                Text(
                    "定元法: ${c.juMethod}（默认仅执行拆补·日数分段；未完成的方法必须 fail-closed）",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                if (c.isWuBuYu) {
                    Text("五不遇时（时干克日干、同阴阳）", fontSize = 13.sp, color = MaterialTheme.colorScheme.error)
                }
                if (c.patterns.isNotEmpty()) {
                    Text(
                        "实验格局候选: ${c.patterns.joinToString("、")}",
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.error,
                    )
                }
                Text(
                    "值符/值使与九宫来自当前实验转盘实现（物理环序、天禽寄坤2）；完整九宫黄金夹具仍未建立。",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.error,
                )
                Text("值符: ${c.zhiFu}   值使: ${c.zhiShi}   时旬首: ${c.xunShou}遁${c.dunGan}", fontSize = 14.sp)
                Text("日空: ${c.dayKong.joinToString("")}   时空: ${c.hourKong.joinToString("")}", fontSize = 14.sp)
                Text("马星（占时支）: ${c.maXing}", fontSize = 14.sp)
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
                        g?.isDayKong == true || g?.isHourKong == true -> MaterialTheme.colorScheme.surfaceVariant
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
                                if (g?.isMaXing == true) Text("马", fontSize = 9.sp, color = MaterialTheme.colorScheme.secondary)
                                if (g?.isDayKong == true) Text("日空", fontSize = 8.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                if (g?.isHourKong == true) Text("时空", fontSize = 8.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
