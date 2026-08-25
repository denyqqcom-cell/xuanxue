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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.ai.QueryDomain
import com.xuanxue.ai.ReadingContext
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.qimen.QimenEngine.QimenChart
import java.util.Calendar

private val QIMEN_LAYOUT = listOf(
    listOf(4, 9, 2),
    listOf(3, 5, 7),
    listOf(8, 1, 6),
)

private val QIMEN_PALACE_NAME = mapOf(
    1 to "坎一",
    2 to "坤二",
    3 to "震三",
    4 to "巽四",
    5 to "中五",
    6 to "乾六",
    7 to "兑七",
    8 to "艮八",
    9 to "离九",
)

/** 奇门遁甲排盘页。盘面先保持术数结构，问事上下文与解读放在盘面之后。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QimenScreen() {
    val now = remember { Calendar.getInstance() }
    var year by remember { mutableStateOf(now.get(Calendar.YEAR)) }
    var month by remember { mutableStateOf(now.get(Calendar.MONTH) + 1) }
    var day by remember { mutableStateOf(now.get(Calendar.DAY_OF_MONTH)) }
    var hourText by remember { mutableStateOf(now.get(Calendar.HOUR_OF_DAY).toString()) }
    var minuteText by remember { mutableStateOf(now.get(Calendar.MINUTE).toString()) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<QimenChart?>(null) }

    var queryDomain by remember { mutableStateOf(QueryDomain.GENERAL) }
    var question by remember { mutableStateOf("") }
    var knownFacts by remember { mutableStateOf("") }

    val hour = hourText.toIntOrNull()
    val minute = minuteText.toIntOrNull()
    val timeValid = hour != null && hour in 0..23 && minute != null && minute in 0..59
    val timeLabel = if (timeValid) "%02d:%02d".format(hour, minute) else "--:--"

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

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(
                Modifier.padding(12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历 $year-$month-$day  $timeLabel", Modifier.weight(1f))
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }

                Text("时间（24小时制）", fontWeight = FontWeight.SemiBold)
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    OutlinedTextField(
                        value = hourText,
                        onValueChange = { if (it.length <= 2) hourText = it.filter(Char::isDigit) },
                        label = { Text("时 0-23") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                    )
                    OutlinedTextField(
                        value = minuteText,
                        onValueChange = { if (it.length <= 2) minuteText = it.filter(Char::isDigit) },
                        label = { Text("分 0-59") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                    )
                }
                if (!timeValid) {
                    Text(
                        "请输入有效时间：小时 0-23、分钟 0-59",
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.error,
                    )
                }

                Text("时辰快捷", fontWeight = FontWeight.SemiBold)
                Row(
                    Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                ) {
                    listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23).forEach { h ->
                        TextButton(onClick = { hourText = h.toString(); minuteText = "30" }) {
                            Text(
                                "%02d:30".format(h),
                                color = if (hour == h) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 12.sp,
                            )
                        }
                    }
                }
                Button(
                    onClick = { chart = QimenEngine.bySolar(year, month, day, hour!!, minute!!) },
                    enabled = timeValid,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text("起局")
                }
            }
        }

        chart?.let { c ->
            QimenResult(c)

            Text("问事与现实条件", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            QuestionContextCard(
                domain = queryDomain,
                question = question,
                knownFacts = knownFacts,
                onDomainChange = { queryDomain = it },
                onQuestionChange = { question = it },
                onKnownFactsChange = { knownFacts = it },
            )
            ReadingCard(com.xuanxue.ai.XuanxueAI.qimen(c, readingContext))
        } ?: Text(
            "选择日期与时间后起局。盘面本身与问事解读分开显示。",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
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
                Modifier.padding(10.dp),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(c.juText, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    Text(c.jieQi, fontWeight = FontWeight.SemiBold)
                }
                Text("四柱 ${c.yearGZ}　${c.monthGZ}　${c.dayGZ}　${c.hourGZ}", fontSize = 13.sp)
                Text("农历 ${c.lunarDateStr}", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("值符 ${c.zhiFu}　值使 ${c.zhiShi}", fontSize = 13.sp)
                Text("旬首 ${c.xunShou}遁${c.dunGan}　马星 ${c.maXing}", fontSize = 12.sp)
                Text(
                    "日空 ${c.dayKong.joinToString("、")}　时空 ${c.hourKong.joinToString("、")}",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        Text("九宫盘", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        val byPalace = c.gongs.associateBy { it.palace }
        QIMEN_LAYOUT.forEach { row ->
            Row(Modifier.fillMaxWidth()) {
                row.forEach { palace ->
                    QimenPalaceCell(
                        palace = palace,
                        gong = byPalace[palace],
                        modifier = Modifier
                            .weight(1f)
                            .padding(1.dp)
                            .aspectRatio(1f),
                    )
                }
            }
        }

        Text(
            "盘面位置按洛书九宫恢复为「巽四、离九、坤二 / 震三、中五、兑七 / 艮八、坎一、乾六」。日空、时空与时支马星已用来源实例锁定；当前星、门、神和值符值使旋转算法仍属于待完整黄金盘夹具复核的实现，不因界面完成而升格为已验证术理。",
            fontSize = 11.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun QimenPalaceCell(
    palace: Int,
    gong: QimenEngine.Gong?,
    modifier: Modifier = Modifier,
) {
    val background = when {
        gong?.isMaXing == true -> MaterialTheme.colorScheme.secondaryContainer
        gong?.isKong == true -> MaterialTheme.colorScheme.surfaceVariant
        else -> MaterialTheme.colorScheme.surface
    }

    Box(
        modifier
            .background(background)
            .border(1.dp, MaterialTheme.colorScheme.outline)
            .padding(5.dp),
    ) {
        Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    QIMEN_PALACE_NAME[palace] ?: palace.toString(),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.weight(1f))
                if (gong?.isMaXing == true) {
                    Text("马", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)
                }
                when {
                    gong?.isDayKong == true && gong.isHourKong -> Text(" 日时空", fontSize = 8.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    gong?.isDayKong == true -> Text(" 日空", fontSize = 8.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    gong?.isHourKong == true -> Text(" 时空", fontSize = 8.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }

            gong?.shenPan?.takeIf { it.isNotBlank() }?.let {
                Text(it, fontSize = 9.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }

            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(1.dp)) {
                    gong?.renMen?.takeIf { it.isNotBlank() }?.let {
                        Text(it, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    gong?.tianXing?.takeIf { it.isNotBlank() }?.let {
                        Text(it, fontSize = 11.sp, color = MaterialTheme.colorScheme.primary)
                    }
                }
                gong?.diGan?.takeIf { it.isNotBlank() }?.let {
                    Text(
                        it,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.error,
                        textAlign = TextAlign.Center,
                    )
                }
            }
        }
    }
}
