package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.material3.TextField
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
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.liuyao.LiuYaoEngine.LiuYaoChart
import java.util.Calendar

/** 六爻排卦页（纳甲筮法，纯净版：时间起卦 + 数字起卦） */
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
    var mode by remember { mutableStateOf("time") } // time | number
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<LiuYaoChart?>(null) }

    Column(
        Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("六爻排卦（纳甲筮法）", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Row {
                    TextButton(onClick = { mode = "time" }) {
                        Text("时间起卦", color = if (mode == "time") Color(0xFF1E88E5) else Color.Gray, fontWeight = if (mode == "time") FontWeight.Bold else FontWeight.Normal)
                    }
                    TextButton(onClick = { mode = "number" }) {
                        Text("数字起卦", color = if (mode == "number") Color(0xFF1E88E5) else Color.Gray, fontWeight = if (mode == "number") FontWeight.Bold else FontWeight.Normal)
                    }
                }
                if (mode == "time") {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("公历: $year-$month-$day  $hour:00", Modifier.weight(1f))
                        Button(onClick = { showDatePicker = true }) { Text("选日期") }
                    }
                } else {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        TextField(value = n1, onValueChange = { n1 = it.filter { c -> c.isDigit() }.take(3) }, label = { Text("上卦数") }, modifier = Modifier.weight(1f))
                        TextField(value = n2, onValueChange = { n2 = it.filter { c -> c.isDigit() }.take(3) }, label = { Text("下卦数") }, modifier = Modifier.weight(1f))
                        TextField(value = n3, onValueChange = { n3 = it.filter { c -> c.isDigit() }.take(3) }, label = { Text("动爻数") }, modifier = Modifier.weight(1f))
                    }
                }
                Spacer(Modifier.height(8.dp))
                Button(onClick = {
                    chart = if (mode == "time") {
                        LiuYaoEngine.bySolar(year, month, day, hour)
                    } else {
                        LiuYaoEngine.byNumbers(n1.toIntOrNull() ?: 1, n2.toIntOrNull() ?: 1, n3.toIntOrNull() ?: 1, year, month, day, hour)
                    }
                }, modifier = Modifier.fillMaxWidth()) {
                    Text("起卦")
                }
            }
        }

        chart?.let { c ->
            Spacer(Modifier.height(16.dp))
            LiuYaoResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.liuyao(c))
        }
    }

    if (showDatePicker) {
        val today = Calendar.getInstance()
        val state = rememberDatePickerState(initialSelectedDateMillis = runCatching {
            java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse("$year-$month-$day")!!.time
        }.getOrDefault(System.currentTimeMillis()).coerceIn(
            java.text.SimpleDateFormat("yyyy", java.util.Locale.US).parse("1900")!!.time, today.timeInMillis
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
        ) { DatePicker(state = state) }
    }
}

@Composable
fun LiuYaoResult(c: LiuYaoChart) {
    Column {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("农历: ${c.lunarDateStr}   日: ${c.dayGZ}   时: ${c.hourGZ}", fontSize = 14.sp)
                Text("本卦: ${c.benGua.name}（${c.benGua.up}上${c.benGua.down}下，${c.benGua.palace}${if (c.benGua.palaceIndex == 0) "本宫" else if (c.benGua.palaceIndex == 6) "游魂" else if (c.benGua.palaceIndex == 7) "归魂" else "${c.benGua.palaceIndex}世"}）", fontSize = 14.sp)
                Text("动爻: ${if (c.dongYaoIndexes.isEmpty()) "无（静卦）" else c.dongYaoIndexes.joinToString("、") + "爻"}",
                    fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                c.bianGua?.let {
                    Text("变卦: ${it.name}（${it.up}上${it.down}下，${it.palace}）")
                }
            }
        }

        Spacer(Modifier.height(12.dp))
        YaoList(c.benGua, title = "本卦")
        c.bianGua?.let {
            Spacer(Modifier.height(12.dp))
            YaoList(it, title = "变卦")
        }
    }
}

@Composable
fun YaoList(gua: LiuYaoEngine.Gua, title: String) {
    OutlinedCard(Modifier.fillMaxWidth(), border = BorderStroke(1.dp, Color(0xFFBDBDBD))) {
        Column(Modifier.padding(8.dp)) {
            Text(title + ": " + gua.name + "（" + gua.up + "上" + gua.down + "下，" + gua.palace + "）", fontWeight = FontWeight.Bold, fontSize = 14.sp)
            gua.yao.sortedByDescending { it.index }.forEach { y ->
                Row(
                    Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp)
                        .background(if (y.isDong) Color(0xFFFFF8E1) else Color.Transparent)
                        .border(BorderStroke(0.dp, Color.Transparent)),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("${y.index}爻", Modifier.width(32.dp), fontSize = 12.sp, color = Color.Gray)
                    Text(y.liuShen, Modifier.width(48.dp), fontSize = 12.sp, color = Color(0xFF6D4C41))
                    Text(y.liuQin, Modifier.width(52.dp), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                    Text(y.gan + y.zhi, Modifier.width(56.dp), fontSize = 13.sp, color = Color(0xFF1E88E5))
                    Text(if (y.isYang) "———" else "— —", Modifier.width(40.dp), fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text(
                        if (y.isShi) "[世]" else if (y.isYing) "[应]" else if (y.isDong) "[动]" else "",
                        fontSize = 12.sp, color = Color(0xFFE65100)
                    )
                }
            }
        }
    }
}
