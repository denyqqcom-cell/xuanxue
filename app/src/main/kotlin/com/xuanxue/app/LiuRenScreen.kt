package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.QueryDomain
import com.xuanxue.ai.ReadingContext
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuren.LiuRenEngine.LiuRenChart
import java.util.Calendar

/** 大六壬排盘页。课型与三传先作为结构层，类神与应事必须结合具体事体。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiuRenScreen() {
    val now = remember { Calendar.getInstance() }
    var year by remember { mutableStateOf(now.get(Calendar.YEAR)) }
    var month by remember { mutableStateOf(now.get(Calendar.MONTH) + 1) }
    var day by remember { mutableStateOf(now.get(Calendar.DAY_OF_MONTH)) }
    var hour by remember { mutableStateOf(now.get(Calendar.HOUR_OF_DAY)) }
    var night by remember { mutableStateOf(false) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<LiuRenChart?>(null) }

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
        Text("大六壬", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Text(
            "当前引擎可以计算天地盘、四课、三传、九宗门与天将，但类神取用、应事和应期不能脱离具体问题。",
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
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历: $year-$month-$day  ${"%02d".format(hour)}:00", Modifier.weight(1f))
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

                Row {
                    TextButton(onClick = { night = false }) {
                        Text(
                            "昼占",
                            color = if (!night) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = if (!night) FontWeight.Bold else FontWeight.Normal,
                        )
                    }
                    TextButton(onClick = { night = true }) {
                        Text(
                            "夜占",
                            color = if (night) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = if (night) FontWeight.Bold else FontWeight.Normal,
                        )
                    }
                }

                Button(
                    onClick = { chart = LiuRenEngine.bySolar(year, month, day, hour, 0, night) },
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text("起课")
                }
            }
        }

        chart?.let { c ->
            LiuRenResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.liuren(c, readingContext))
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
fun LiuRenResult(c: LiuRenChart) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text("农历: ${c.lunarDateStr}", fontSize = 14.sp)
                Text("四柱: ${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}", fontSize = 14.sp)
                Text("月将: ${c.yueJiang}（日干寄宫: ${c.ganJi}）  贵人: ${c.guiRen}  旬空: ${c.xunKong.joinToString("")}", fontSize = 14.sp)
                Text(
                    "三传: ${c.sanChuan.chu} → ${c.sanChuan.zhong} → ${c.sanChuan.mo}",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text("取法: ${c.sanChuan.fa}", fontSize = 13.sp, color = MaterialTheme.colorScheme.tertiary)
            }
        }

        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedCard(Modifier.weight(1f), border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)) {
                Column(Modifier.padding(10.dp)) {
                    Text("四课", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    c.siKe.forEachIndexed { i, k ->
                        Row(Modifier.padding(vertical = 2.dp)) {
                            Text("课${i + 1}", Modifier.width(36.dp), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text("${k.zhi}(${k.dunGan})", fontSize = 14.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            OutlinedCard(Modifier.weight(1f), border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)) {
                Column(Modifier.padding(10.dp)) {
                    Text("天地盘", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    LiuRenEngine.ZHI.forEachIndexed { i, z ->
                        Row(Modifier.padding(vertical = 1.dp)) {
                            Text(z, Modifier.width(20.dp), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text(
                                c.tianPan[i],
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (c.tianPan[i] == c.yueJiang) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
                            )
                        }
                    }
                }
            }
        }

        Text(
            "结构注：天盘月将${c.yueJiang}加时；三传为初传→中传→末传。课型名称本身不直接等同现实吉凶。",
            fontSize = 11.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
