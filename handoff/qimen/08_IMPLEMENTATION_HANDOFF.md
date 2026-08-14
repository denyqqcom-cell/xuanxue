# Implementation handoff (Kotlin / Android)

Audience: a developer AI that **cannot** see Joe’s disks.  
You may use this folder + the public `xuanxue` repo. You may **not** assume any PDF content beyond what is written here.

## Goal for v1 core

Ship **时家 · 拆补(日数分段) · 转盘** as far as tests allow:

1. Civil datetime → day/hour pillars + xun + 空亡  
2. Jieqi via an astronomy/calendar library → `{yinYangDun, jieqi, dayIndex}`  
3. Ju lookup from ALG-JU-TABLE  
4. Stop before 天/门/神 rotation until ALG-PLATE-03 has fixtures  

Do **not** implement judgement, 年家, 飞宫, or omen dictionaries in v1.

## Package

```
com.xuanxue.qimen.core
  calendar/    Ganzhi, HourBranch, JieqiClock
  ju/          JuMethod, JuId, JuResolver
  plate/       PalaceId, Yi, Star, Gate, Spirit, EarthPlate   // sky/gate/spirit later
  api/         QimenEngine, QimenRequest, QimenChart, QimenError
  school/      QimenSchoolConfig
```

New Gradle module `:qimen-core` (JVM, same as `:ziwei-core`). App depends on it later. Do not put this logic in `MainActivity`.

## Public API (suggested)

```kotlin
data class QimenRequest(
    val instantEpochMs: Long,
    val zoneId: String = "Asia/Shanghai",
    val longitudeEastDeg: Double? = null, // ignored unless useTrueSolarTime
    val school: QimenSchoolConfig = QimenSchoolConfig.Default,
)

data class QimenSchoolConfig(
    val juMethod: JuMethod = JuMethod.CHAI_BU_DAYCOUNT,
    val lateZiRollsToNextDay: Boolean = true,
    val useTrueSolarTime: Boolean = false, // must error if true in v1
    val boardSchool: BoardSchool = BoardSchool.ZHUAN_PAN,
    val personToken: PersonToken = PersonToken.DAY_STEM,
)

enum class JuMethod { CHAI_BU_DAYCOUNT, CHAI_BU_FUTOU, ZHI_RUN, MAO_SHAN }
enum class BoardSchool { ZHUAN_PAN, FEI_GONG }
enum class PersonToken { DAY_STEM, YEAR_PILLAR }

data class QimenChart(
    val civil: CivilStamp,
    val dayPillar: StemBranch,
    val hourPillar: StemBranch,
    val xunShou: StemBranch,
    val dunYi: Yi,
    val xunKong: List<Branch>,
    val dun: Dun,          // YANG / YIN
    val ju: Int,           // 1..9
    val yuan: Yuan,
    val juMethodUsed: JuMethod,
    val earth: EarthPlate?, // null until walk is tested
)

sealed class QimenError {
    data class UnsupportedSchool(val flag: String) : QimenError()
    data class AmbiguousJieqi(val detail: String) : QimenError()
    data class InvalidInstant(val detail: String) : QimenError()
}
```

v1 `QimenEngine.cast(req): Result<QimenChart>` must:

- return `UnsupportedSchool` if `useTrueSolarTime`, `ZHI_RUN`, `FEI_GONG`, `CHAI_BU_FUTOU`, or `MAO_SHAN`  
- never call a network “online pan”  
- never read files from `F:\` or `E:\`

## Layering

```
QimenEngine
  ├─ ClockPolicy          // 13 shichen + late zi
  ├─ GanzhiCalendar       // two-anchor day index
  ├─ JieqiClock           // solar longitude or well-tested lib
  ├─ JuResolver.chaiBuDayCount
  └─ EarthPlateBuilder    // gated by fixture; else return earth=null
```

Judgement (用神, 格局 names, 应期) is a **later** module `qimen-judge` that only consumes `QimenChart`. Do not mix.

## Tests

Reuse the ziwei style: `src/test/resources/fixtures.jsonl` in `:qimen-core`.

```kotlin
class CalendarFixtureTest {
    // read 05_FIXTURES.jsonl
    // compare only fields listed in compare_fields
}
```

Rules:

- Fail the build if 1900-01-01 and 2000-01-01 anchors disagree on a random 20th/21st century date.  
- Do not add a 9-palace expected board until `04_CONFLICTS` C-PLATE-WALK is closed.  
- Do not assert omen text.

## Fixtures method

`05_FIXTURES.jsonl` in this folder is the seed. Copy into the module **without** adding book-page “expected 全盘” rows.

## UI (not this module, but contract)

- Show `juMethodUsed`, `dun`, `ju`, pillars, 旬空.  
- If `earth == null`, show “地盘算法未解锁” — do not draw a fake 九宫.  
- School picker later; v1 no picker except debug.

## What you must not do

- Do not invent 洛书 walk order.  
- Do not port `paipan_core.py`.  
- Do not scrape 在线排盘.  
- Do not paste 十干克应 strings.  
- Do not claim iztro contains qimen (it does not).
