package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.QueryDomain
import com.xuanxue.ai.ReadingContext
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.liuyao.LiuYaoEngine.LiuYaoChart
import java.util.Calendar

/** 六爻排卦页（纳甲筮法：时间起卦 + 数字起卦）。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiuYaoScreen() {
    var year by remember { mutableStateOf(2026) }
    var month by remember { mutableStateOf(8) }
    var day by remember { mutableStateOf(15) }
    var hour by remember { mutableStateOf(10) }
    var n1 by remember { mutableStateOf("1") }
    var n2 by remember { mutableStateOf("1") }
    var n3 by remember { mutableStateOf("3") }
    var mode by remember { mutableStateOf("time") }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<LiuYaoChart?>(null) }

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
        Text("六爻排卦", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Text(
            "当前先把起卦、纳甲、世应、六亲、动变作为结构层；具体取用必须结合事体，不能只见六亲就下结论。",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

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
                Row {
                    TextButton(onClick = { mode = "time" }) {
                        Text(
                            "时间起卦",
                            color = if (mode == "time") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = if (mode == "time") FontWeight.Bold else FontWeight.Normal,
                        )
                    }
                    TextButton(onClick = { mode = "number" }) {
                        Text(
                            "数字起卦",
                            color = if (mode == "number") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = if (mode == "number") FontWeight.Bold else FontWeight.Normal,
                        )
                    }
                }

                if (mode == "time") {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("公历: $year-$month-$day  $hour:00", Modifier.weight(1f))
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
                            TextButton(onClick = { hour = h }) {
                                Text(
                                    "%02d:00".format(h),
                                    color = if (hour == h) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 12.sp,
                                )
                            }
                        }
                    }
                } else {
                    NumberInputs(
                        n1 = n1,
                        n2 = n2,
                        n3 = n3,
                        onN1 = { n1 = it.filter(Char::isDigit).take(3) },
                        onN2 = { n2 = it.filter(Char::isDigit).take(3) },
                        onN3 = { n3 = it.filter(Char::isDigit).take(3) },
                    )
                    Text(
                        "数字起卦仍使用当前日期/时辰作为日时信息；日期可先切回“时间起卦”修改。",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }

                Button(
                    onClick = {
                        chart = if (mode == "time") {
                            LiuYaoEngine.bySolar(year, month, day, hour)
                        } else {
                            LiuYaoEngine.byNumbers(
                                n1.toIntOrNull() ?: 1,
                                n2.toIntOrNull() ?: 1,
                                n3.toIntOrNull() ?: 1,
                                year,
                                month,
                                day,
                                hour,
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text("起卦")
                }
            }
        }

        chart?.let { c ->
            LiuYaoResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.liuyao(c, readingContext))
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
private fun NumberInputs(
    n1: String,
    n2: String,
    n3: String,
    onN1: (String) -> Unit,
    onN2: (String) -> Unit,
    onN3: (String) -> Unit,
) {
    BoxWithConstraints(Modifier.fillMaxWidth()) {
        val compact = maxWidth < 520.dp
        if (compact) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(n1, onN1, label = { Text("上卦数") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(n2, onN2, label = { Text("下卦数") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(n3, onN3, label = { Text("动爻数") }, modifier = Modifier.fillMaxWidth())
            }
        } else {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(n1, onN1, label = { Text("上卦数") }, modifier = Modifier.weight(1f))
                OutlinedTextField(n2, onN2, label = { Text("下卦数") }, modifier = Modifier.weight(1f))
                OutlinedTextField(n3, onN3, label = { Text("动爻数") }, modifier = Modifier.weight(1f))
            }
        }
    }
}

@Composable
fun LiuYaoResult(c: LiuYaoChart) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("农历: ${c.lunarDateStr}   日: ${c.dayGZ}   时: ${c.hourGZ}", fontSize = 14.sp)
                Text(
                    "本卦: ${c.benGua.name}（${c.benGua.up}上${c.benGua.down}下，${c.benGua.palace}${if (c.benGua.palaceIndex == 0) "本宫" else if (c.benGua.palaceIndex == 6) "游魂" else if (c.benGua.palaceIndex == 7) "归魂" else "${c.benGua.palaceIndex}世"}）",
                    fontSize = 14.sp,
                )
                Text(
                    "动爻: ${if (c.dongYaoIndexes.isEmpty()) "无（静卦）" else c.dongYaoIndexes.joinToString("、") + "爻"}",
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                )
                c.bianGua?.let { Text("变卦: ${it.name}（${it.up}上${it.down}下，${it.palace}）") }
            }
        }

        YaoList(c.benGua, title = "本卦")
        c.bianGua?.let { YaoList(it, title = "变卦") }
    }
}

@Composable
fun YaoList(gua: LiuYaoEngine.Gua, title: String) {
    OutlinedCard(Modifier.fillMaxWidth(), border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)) {
        Column(Modifier.padding(8.dp)) {
            Text("$title: ${gua.name}（${gua.up}上${gua.down}下，${gua.palace}）", fontWeight = FontWeight.Bold, fontSize = 14.sp)
            gua.yao.sortedByDescending { it.index }.forEach { y ->
                Row(
                    Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp)
                        .background(if (y.isDong) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent)
                        .border(BorderStroke(0.dp, Color.Transparent)),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("${y.index}爻", Modifier.width(32.dp), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(y.liuShen, Modifier.width(48.dp), fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                    Text(y.liuQin, Modifier.width(52.dp), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                    Text(y.gan + y.zhi, Modifier.width(56.dp), fontSize = 13.sp, color = MaterialTheme.colorScheme.primary)
                    Text(if (y.isYang) "———" else "— —", Modifier.width(40.dp), fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text(
                        if (y.isShi) "[世]" else if (y.isYing) "[应]" else if (y.isDong) "[动]" else "",
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.tertiary,
                    )
                }
            }
        }
    }
}
