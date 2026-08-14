package com.xuanxue.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val Ink = Color(0xFF20211E)
val Paper = Color(0xFFF6F1E7)
val Ivory = Color(0xFFFFFBF3)
val Jade = Color(0xFF31584E)
val Cinnabar = Color(0xFF9A3428)
val MutedGold = Color(0xFF84683A)
val MutedInk = Color(0xFF66645E)
val Hairline = Color(0xFFD5CEC1)

private val LightColors = lightColorScheme(
    primary = Jade,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFDDE9E2),
    onPrimaryContainer = Ink,
    secondary = MutedGold,
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFEFE3CB),
    onSecondaryContainer = Ink,
    background = Paper,
    onBackground = Ink,
    surface = Ivory,
    onSurface = Ink,
    surfaceVariant = Color(0xFFEDE6D9),
    onSurfaceVariant = MutedInk,
    error = Cinnabar,
    outline = Hairline,
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFFA8CFC0),
    onPrimary = Color(0xFF10372F),
    primaryContainer = Color(0xFF24483F),
    onPrimaryContainer = Color(0xFFDDE9E2),
    secondary = Color(0xFFD9C08A),
    onSecondary = Color(0xFF3A2F18),
    background = Color(0xFF171816),
    onBackground = Color(0xFFECE8DF),
    surface = Color(0xFF1E201D),
    onSurface = Color(0xFFECE8DF),
    surfaceVariant = Color(0xFF2A2D29),
    onSurfaceVariant = Color(0xFFC8C4BB),
    error = Color(0xFFFFB4A8),
    outline = Color(0xFF555851),
)

private val AppTypography = Typography(
    displaySmall = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 36.sp,
        lineHeight = 44.sp,
    ),
    headlineSmall = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 24.sp,
        lineHeight = 32.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 20.sp,
        lineHeight = 28.sp,
    ),
    titleMedium = TextStyle(
        fontWeight = FontWeight.SemiBold,
        fontSize = 16.sp,
        lineHeight = 24.sp,
    ),
    bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontSize = 14.sp, lineHeight = 21.sp),
    bodySmall = TextStyle(fontSize = 12.sp, lineHeight = 18.sp),
    labelLarge = TextStyle(fontWeight = FontWeight.SemiBold, fontSize = 14.sp),
)

private val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small = RoundedCornerShape(10.dp),
    medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(22.dp),
    extraLarge = RoundedCornerShape(28.dp),
)

@Composable
fun XuanxueTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors,
        typography = AppTypography,
        shapes = AppShapes,
        content = content,
    )
}
