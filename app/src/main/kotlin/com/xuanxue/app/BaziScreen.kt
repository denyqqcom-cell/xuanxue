package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
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
import com.xuanxue.bazi.BaziEngine
import com.xuanxue.bazi.BaziEngine.BaziChart
import com.xuanxue.bazi.BaziEngine.Zhu
import java.util.Calendar

/**
 * 八字排盘页面（纯净版：无广告/无品牌/无网络）。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BaziScreen() {
    var year by remember { mutableStateOf(1990) }
    var month by remember { mutableStateOf(5) }
    var day by remember { mutableStateOf(20) }
    var hour by remember { mutableStateOf(12) }
    var minute by remember { mutableStateOf(30) }
    var gender by remember { mutableStateOf("男") }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<BaziChart?>(null) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("八字排盘", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))

        // 日期选择
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历: $year-$month-$day  $hour:${"%02d".format(minute)}", Modifier.weight(1f))
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("男", "女").forEach { g ->
                        TextButton(onClick = { gender = g }) {
                            Text(if (gender == g) "● $g" else "○ $g", color = if (gender == g) Color(0xFF1E88E5) else Color.Gray)
                        }
                    }
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("时辰:", Modifier.align(Alignment.CenterVertically))
                    listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22).forEach { h ->
                        TextButton(onClick = { hour = h; minute = 30 }) {
                            Text("${hour / 2 + 1}时", color = if (hour == h) Color(0xFF1E88E5) else Color.Gray, fontSize = 12.sp)
                        }
                    }
                }
                Spacer(Modifier.height(8.dp))
                Button(onClick = {
                    chart = BaziEngine.bySolar(year, month, day, hour, minute, gender)
                }, modifier = Modifier.fillMaxWidth()) {
                    Text("排盘")
                }
            }
        }

        chart?.let { c ->
            Spacer(Modifier.height(16.dp))
            BaziResult(c)
        }
    }

    if (showDatePicker) {
        val today = Calendar.getInstance()
        val initMillis = remember { runCatching {
            java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US)
                .parse("$year-$month-$day")?.time ?: System.currentTimeMillis()
        }.getOrDefault(System.currentTimeMillis()) }
        val state = rememberDatePickerState(initialSelectedDateMillis = initMillis.coerceIn(
            java.text.SimpleDateFormat("yyyy", java.util.Locale.US).parse("1900")!!.time,
            today.timeInMillis
        ))
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    state.selectedDateMillis?.let { ms ->
                        val cal = Calendar.getInstance().apply { timeInMillis = ms }
                        year = cal.get(Calendar.YEAR); month = cal.get(Calendar.MONTH) + 1; day = cal.get(Calendar.DAY_OF_MONTH)
                    }
                    showDatePicker = false
                }) { Text("确定") }
            },
            dismissButton = { TextButton(onClick = { showDatePicker = false }) { Text("取消") } }
        ) {
            DatePicker(state = state)
        }
    }
}

@Composable
fun BaziResult(c: BaziChart) {
    Column {
        // 概览
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("农历: ${c.lunarDateStr}", fontSize = 14.sp)
                Text("性别: ${c.gender}", fontSize = 14.sp)
                Text("胎元: ${c.taiYuan}   命宫: ${c.mingGong}   身宫: ${c.shenGong}", fontSize = 14.sp)
                Text("日空亡: ${c.dayKong}", fontSize = 14.sp)
                Text("起运: ${c.startYunAge}岁", fontSize = 14.sp)
                c.chengGu?.let {
                    Text("称骨: ${it.weightText}", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                }
            }
        }

        // 四柱表
        Spacer(Modifier.height(12.dp))
        FourZhuTable(c.fourZhu)

        // 大运流年
        Spacer(Modifier.height(12.dp))
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("大运 (${if (c.yunGender == 1) "阳男/阴女顺排" else "阴男/阳女逆排"})", fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(Modifier.horizontalScroll(rememberScrollState())) {
                    c.daYun.forEach { dy ->
                        Column(
                            Modifier
                                .padding(horizontal = 8.dp)
                                .border(1.dp, Color(0xFFBDBDBD), MaterialTheme.shapes.small)
                                .padding(8.dp)
                        ) {
                            Text(dy.ganZhi, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                            Text("${dy.startYear}-${dy.endYear}岁", fontSize = 11.sp)
                            Text("首流年 ${dy.liuNian.firstOrNull()?.first ?: ""}", fontSize = 11.sp)
                        }
                    }
                }
            }
        }

        // 称骨歌
        c.chengGu?.let {
            if (it.poem.isNotEmpty()) {
                Spacer(Modifier.height(12.dp))
                OutlinedCard(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(12.dp)) {
                        Text("称骨歌（${it.weightText}）", fontWeight = FontWeight.Bold)
                        Spacer(Modifier.height(6.dp))
                        Text(it.poem, fontSize = 14.sp, lineHeight = 22.sp)
                    }
                }
            }
        }
    }
}

@Composable
fun FourZhuTable(zhus: List<Zhu>) {
    OutlinedCard(Modifier.fillMaxWidth(), border = BorderStroke(1.dp, Color(0xFFBDBDBD))) {
        Column {
            // 表头
            Row(Modifier.background(Color(0xFFEEEEEE)).padding(vertical = 6.dp)) {
                listOf("", "年柱", "月柱", "日柱", "时柱").forEach {
                    Text(it, Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                }
            }
            @Composable
            fun row(label: String, values: List<String>, highlight: Boolean = false) {
                Row(Modifier.padding(vertical = 4.dp)) {
                    Text(label, Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center, fontSize = 12.sp, color = Color.Gray)
                    values.forEachIndexed { i, v ->
                        val col = if (highlight && i == 2) Color(0xFF1E88E5) else Color.Unspecified
                        val w = if (highlight && i == 2) FontWeight.Bold else FontWeight.Normal
                        Text(v, Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center, fontSize = 14.sp, color = col, fontWeight = w)
                    }
                }
            }
            row("天干", zhus.map { it.gan }, highlight = true)
            row("地支", zhus.map { it.zhi })
            row("藏干", zhus.map { it.hideGan.joinToString("") })
            row("十神", zhus.map { it.shiShenGan })
            row("支十神", zhus.map { it.shiShenZhi.joinToString("") })
            row("纳音", zhus.map { it.naYin })
            row("五行", zhus.map { it.wuXing })
            row("十二运", zhus.map { it.diShi })
        }
    }
}
