package com.xuanxue.app

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import androidx.compose.material3.Typography

private val LightColors = lightColorScheme(
    primary = Color(0xFF315D58),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFD7E9E4),
    onPrimaryContainer = Color(0xFF102E2B),
    secondary = Color(0xFF725B35),
    secondaryContainer = Color(0xFFF0E2C5),
    onSecondaryContainer = Color(0xFF2B2110),
    tertiary = Color(0xFF72536A),
    error = Color(0xFFA13A32),
    background = Color(0xFFF7F4ED),
    surface = Color(0xFFFFFCF5),
    surfaceVariant = Color(0xFFEDE9E0),
    onSurface = Color(0xFF252522),
    onSurfaceVariant = Color(0xFF5B5A54),
    outline = Color(0xFF858078),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFFA9D1C9),
    onPrimary = Color(0xFF143733),
    primaryContainer = Color(0xFF274D48),
    onPrimaryContainer = Color(0xFFD7E9E4),
    secondary = Color(0xFFD8C49B),
    secondaryContainer = Color(0xFF554521),
    onSecondaryContainer = Color(0xFFF0E2C5),
    tertiary = Color(0xFFE0B9D3),
    error = Color(0xFFFFB4AB),
    background = Color(0xFF191A18),
    surface = Color(0xFF1F201D),
    surfaceVariant = Color(0xFF454641),
    onSurface = Color(0xFFE5E2DA),
    onSurfaceVariant = Color(0xFFC8C6BE),
    outline = Color(0xFF92938C),
)

private val AppTypography = Typography(
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Bold,
        fontSize = 28.sp,
        lineHeight = 34.sp,
    ),
    headlineSmall = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Bold,
        fontSize = 23.sp,
        lineHeight = 30.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 20.sp,
        lineHeight = 27.sp,
    ),
)

@Composable
fun XuanxueTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors,
        typography = AppTypography,
        content = content,
    )
}
