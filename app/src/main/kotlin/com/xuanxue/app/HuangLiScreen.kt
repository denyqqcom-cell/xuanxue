package com.xuanxue.app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
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
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar
import java.util.Calendar

/** 黄历页（lunar-java 宜忌/吉神/凶煞/彭祖百忌/冲煞，纯净本地） */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HuangLiScreen() {
    var year by remember { mutableStateOf(2026) }
    var month by remember { mutableStateOf(8) }
    var day by remember { mutableStateOf(15) }
    var showDatePicker by remember { mutableStateOf(false) }

    val lunar = remember(year, month, day) { Solar.fromYmd(year, month, day).lunar }

    Column(
        Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("黄历（万年历）", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Row {
                    Text("公历: $year-$month-$day", Modifier.weight(1f), fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }
                Text(lunar.toString(), fontSize = 15.sp)
            }
        }

        Spacer(Modifier.height(12.dp))
        InfoCard("干支", listOf(
            "年柱: ${lunar.eightChar.year}    月柱: ${lunar.eightChar.month}",
            "日柱: ${lunar.eightChar.day}    时柱: ${lunar.eightChar.time}",
            "生肖: ${lunar.getYearShengXiao()}    星座: ${Solar.fromYmd(year, month, day).getXingZuo()}",
            "纳音: ${lunar.getYearNaYin()} ${lunar.getMonthNaYin()} ${lunar.getDayNaYin()}",
        ))

        Spacer(Modifier.height(12.dp))
        InfoCard("宜", lunar.getDayYi(), color = Color(0xFF2E7D32))

        Spacer(Modifier.height(12.dp))
        InfoCard("忌", lunar.getDayJi(), color = Color(0xFFC62828))

        Spacer(Modifier.height(12.dp))
        InfoCard("吉神", lunar.getDayJiShen(), color = Color(0xFF1E88E5))

        Spacer(Modifier.height(12.dp))
        InfoCard("凶煞", lunar.getDayXiongSha(), color = Color(0xFF6D4C41))

        Spacer(Modifier.height(12.dp))
        InfoCard("冲煞", listOf(
            "冲: ${lunar.getDayChong()}（${lunar.getDayChongShengXiao()}）    煞: ${lunar.getDaySha()}",
            "彭祖百忌: 天干 ${lunar.getPengZuGan()} / 地支 ${lunar.getPengZuZhi()}",
            "喜神: ${lunar.getDayPositionXiDesc()}    福神: ${lunar.getDayPositionFuDesc()}    财神: ${lunar.getDayPositionCaiDesc()}",
        ))

        Spacer(Modifier.height(8.dp))
        Text("数据来源：lunar-java (MIT) 本地计算，无网络。", fontSize = 11.sp, color = Color.Gray)
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
fun InfoCard(title: String, items: List<String>, color: Color = Color.Unspecified) {
    if (items.isEmpty()) return
    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp)) {
            Text(title, fontWeight = FontWeight.Bold, color = if (color == Color.Unspecified) Color.Unspecified else color)
            Spacer(Modifier.height(4.dp))
            items.forEach { Text(it, fontSize = 14.sp, lineHeight = 22.sp) }
        }
    }
}
