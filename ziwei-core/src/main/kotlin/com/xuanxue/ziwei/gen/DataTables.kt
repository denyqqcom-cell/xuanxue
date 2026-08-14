// AUTO-GENERATED from iztro (https://github.com/SylarLong/iztro) MIT - do not edit by hand
package com.xuanxue.ziwei.gen

object DataTables {
    val HEAVENLY_STEMS: List<String> = listOf("jiaHeavenly", "yiHeavenly", "bingHeavenly", "dingHeavenly", "wuHeavenly", "jiHeavenly", "gengHeavenly", "xinHeavenly", "renHeavenly", "guiHeavenly")
    val EARTHLY_BRANCHES: List<String> = listOf("ziEarthly", "chouEarthly", "yinEarthly", "maoEarthly", "chenEarthly", "siEarthly", "wuEarthly", "weiEarthly", "shenEarthly", "youEarthly", "xuEarthly", "haiEarthly")
    val ZODIAC: List<String> = listOf("rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "rooster", "dog", "pig")
    val PALACES: List<String> = listOf("soulPalace", "parentsPalace", "spiritPalace", "propertyPalace", "careerPalace", "friendsPalace", "surfacePalace", "healthPalace", "wealthPalace", "childrenPalace", "spousePalace", "siblingsPalace")
    val CHINESE_TIME: List<String> = listOf("earlyRatHour", "oxHour", "tigerHour", "rabbitHour", "dragonHour", "snakeHour", "horseHour", "goatHour", "monkeyHour", "roosterHour", "dogHour", "pigHour", "lateRatHour")
    val TIME_RANGE: List<String> = listOf("00:00~01:00", "01:00~03:00", "03:00~05:00", "05:00~07:00", "07:00~09:00", "09:00~11:00", "11:00~13:00", "13:00~15:00", "15:00~17:00", "17:00~19:00", "19:00~21:00", "21:00~23:00", "23:00~00:00")
    val MUTAGEN: List<String> = listOf("sihuaLu", "sihuaQuan", "sihuaKe", "sihuaJi")
    val TIGER_RULE: Map<String, String> = mapOf("jiaHeavenly" to "bingHeavenly", "yiHeavenly" to "wuHeavenly", "bingHeavenly" to "gengHeavenly", "dingHeavenly" to "renHeavenly", "wuHeavenly" to "jiaHeavenly", "jiHeavenly" to "bingHeavenly", "gengHeavenly" to "wuHeavenly", "xinHeavenly" to "gengHeavenly", "renHeavenly" to "renHeavenly", "guiHeavenly" to "jiaHeavenly")
    val RAT_RULE: Map<String, String> = mapOf("jiaHeavenly" to "jiaHeavenly", "yiHeavenly" to "bingHeavenly", "bingHeavenly" to "wuHeavenly", "dingHeavenly" to "gengHeavenly", "wuHeavenly" to "renHeavenly", "jiHeavenly" to "jiaHeavenly", "gengHeavenly" to "bingHeavenly", "xinHeavenly" to "wuHeavenly", "renHeavenly" to "gengHeavenly", "guiHeavenly" to "renHeavenly")
    val GENDER: Map<String, String> = mapOf("male" to "阳", "female" to "阴")
    val FIVE_ELEMENTS_VALUE: Map<String, Int> = mapOf("water2nd" to 2, "wood3rd" to 3, "metal4th" to 4, "earth5th" to 5, "fire6th" to 6)
    val STARS_INFO: Map<String, StarInfo> = mapOf(
        "ziweiMaj" to StarInfo(listOf("wang", "wang", "de", "wang", "miao", "miao", "wang", "wang", "de", "wang", "ping", "miao"), "土", "阴"),
        "tianjiMaj" to StarInfo(listOf("de", "wang", "li", "ping", "miao", "xian", "de", "wang", "li", "ping", "miao", "xian"), "木", "阴"),
        "taiyangMaj" to StarInfo(listOf("wang", "miao", "wang", "wang", "wang", "de", "de", "xian", "bu", "xian", "xian", "bu"), "", ""),
        "wuquMaj" to StarInfo(listOf("de", "li", "miao", "ping", "wang", "miao", "de", "li", "miao", "ping", "wang", "miao"), "金", "阴"),
        "tiantongMaj" to StarInfo(listOf("li", "ping", "ping", "miao", "xian", "bu", "wang", "ping", "ping", "miao", "wang", "bu"), "水", "阳"),
        "lianzhenMaj" to StarInfo(listOf("miao", "ping", "li", "xian", "ping", "li", "miao", "ping", "li", "xian", "ping", "li"), "火", "阴"),
        "tianfuMaj" to StarInfo(listOf("miao", "de", "miao", "de", "wang", "miao", "de", "wang", "miao", "de", "miao", "miao"), "土", "阳"),
        "taiyinMaj" to StarInfo(listOf("wang", "xian", "xian", "xian", "bu", "bu", "li", "bu", "wang", "miao", "miao", "miao"), "水", "阴"),
        "tanlangMaj" to StarInfo(listOf("ping", "li", "miao", "xian", "wang", "miao", "ping", "li", "miao", "xian", "wang", "miao"), "水", ""),
        "jumenMaj" to StarInfo(listOf("miao", "miao", "xian", "wang", "wang", "bu", "miao", "miao", "xian", "wang", "wang", "bu"), "土", "阴"),
        "tianxiangMaj" to StarInfo(listOf("miao", "xian", "de", "de", "miao", "de", "miao", "xian", "de", "de", "miao", "miao"), "水", ""),
        "tianliangMaj" to StarInfo(listOf("miao", "miao", "miao", "xian", "miao", "wang", "xian", "de", "miao", "xian", "miao", "wang"), "土", ""),
        "qishaMaj" to StarInfo(listOf("miao", "wang", "miao", "ping", "wang", "miao", "miao", "miao", "miao", "ping", "wang", "miao"), "", ""),
        "pojunMaj" to StarInfo(listOf("de", "xian", "wang", "ping", "miao", "wang", "de", "xian", "wang", "ping", "miao", "wang"), "水", ""),
        "wenchangMin" to StarInfo(listOf("xian", "li", "de", "miao", "xian", "li", "de", "miao", "xian", "li", "de", "miao"), "", ""),
        "wenquMin" to StarInfo(listOf("ping", "wang", "de", "miao", "xian", "wang", "de", "miao", "xian", "wang", "de", "miao"), "", ""),
        "huoxingMin" to StarInfo(listOf("miao", "li", "xian", "de", "miao", "li", "xian", "de", "miao", "li", "xian", "de"), "", ""),
        "lingxingMin" to StarInfo(listOf("miao", "li", "xian", "de", "miao", "li", "xian", "de", "miao", "li", "xian", "de"), "", ""),
        "qingyangMin" to StarInfo(listOf("", "xian", "miao", "", "xian", "miao", "", "xian", "miao", "", "xian", "miao"), "", ""),
        "tuoluoMin" to StarInfo(listOf("xian", "", "miao", "xian", "", "miao", "xian", "", "miao", "xian", "", "miao"), "", ""),
    )
}

data class StarInfo(
    val brightness: List<String>,
    val fiveElements: String = "",
    val yinYang: String = "",
)

data class EarthlyBranchInfo(
    val yinYang: String,
    val fiveElements: String,
    val crash: String,
    val soul: String,
    val body: String,
    val inside: String,
    val outside: String,
    val healthTip: String,
)

val EARTHLY_BRANCH_INFO: Map<String, EarthlyBranchInfo> = mapOf(
    "ziEarthly" to EarthlyBranchInfo("阳", "水", "wuEarthly", "tanlangMaj", "huoxingMin", "胆", "下体", "生殖系统、膀胱、尿道之疾病，听觉障碍"),
    "chouEarthly" to EarthlyBranchInfo("阴", "土", "weiEarthly", "jumenMaj", "tianxiangMaj", "肝", "小腿、脚（右）", "胸部、肋膜炎、胃病、脚部"),
    "yinEarthly" to EarthlyBranchInfo("阳", "木", "shenEarthly", "lucunMin", "tianliangMaj", "肺", "大腿（右）", "胆囊、关节、胫部、神经痛、风湿"),
    "maoEarthly" to EarthlyBranchInfo("阴", "木", "youEarthly", "wenquMin", "tiantongMaj", "大肠", "腰（右）、背", "肝病、颜面神经、失眠、神经衰弱"),
    "chenEarthly" to EarthlyBranchInfo("阳", "土", "xuEarthly", "lianzhenMaj", "wenchangMin", "胃", "胸、胳膊（右）", "消化系统、脊椎、皮肤疾病"),
    "siEarthly" to EarthlyBranchInfo("阴", "火", "haiEarthly", "wuquMaj", "tianjiMaj", "脾", "左肩", "喉头、牙病、感冒"),
    "wuEarthly" to EarthlyBranchInfo("阳", "火", "ziEarthly", "pojunMaj", "huoxingMin", "心", "头", "心脏、视觉、味觉障碍、火难"),
    "weiEarthly" to EarthlyBranchInfo("阴", "土", "chouEarthly", "wuquMaj", "tianxiangMaj", "小肠", "脸", "消化系统、胰脏、健忘症、疲倦、手腕、嘴唇"),
    "shenEarthly" to EarthlyBranchInfo("阳", "金", "yinEarthly", "lianzhenMaj", "tianliangMaj", "膀胱", "胸、胳膊（左）", "呼吸系统、肺部、消化系统、大肠"),
    "youEarthly" to EarthlyBranchInfo("阴", "金", "maoEarthly", "wenquMin", "tiantongMaj", "肾", "腰（左）、腹", "吐血、痢血、小肠之疾、脑出血、头腕部"),
    "xuEarthly" to EarthlyBranchInfo("阳", "土", "chenEarthly", "lucunMin", "wenchangMin", "心包", "大腿（左）", "下半身之疾、子宫、痔疮、脚部"),
    "haiEarthly" to EarthlyBranchInfo("阴", "水", "siEarthly", "jumenMaj", "tianjiMaj", "三焦", "小腿、脚（左）", "排泄机能障碍、肾脏、尿道、偏头痛"),
)

data class HeavenlyStemInfo(
    val yinYang: String,
    val fiveElements: String,
    val crash: String,
    val mutagen: List<String>,
)

val HEAVENLY_STEM_INFO: Map<String, HeavenlyStemInfo> = mapOf(
    "jiaHeavenly" to HeavenlyStemInfo("阳", "木", "gengHeavenly", listOf("lianzhenMaj", "pojunMaj", "wuquMaj", "taiyangMaj")),
    "yiHeavenly" to HeavenlyStemInfo("阴", "木", "xinHeavenly", listOf("tianjiMaj", "tianliangMaj", "ziweiMaj", "taiyinMaj")),
    "bingHeavenly" to HeavenlyStemInfo("阳", "火", "renHeavenly", listOf("tiantongMaj", "tianjiMaj", "wenchangMin", "lianzhenMaj")),
    "dingHeavenly" to HeavenlyStemInfo("阴", "火", "guiHeavenly", listOf("taiyinMaj", "tiantongMaj", "tianjiMaj", "jumenMaj")),
    "wuHeavenly" to HeavenlyStemInfo("阳", "土", "", listOf("tanlangMaj", "taiyinMaj", "youbiMin", "tianjiMaj")),
    "jiHeavenly" to HeavenlyStemInfo("阴", "土", "", listOf("wuquMaj", "tanlangMaj", "tianliangMaj", "wenquMin")),
    "gengHeavenly" to HeavenlyStemInfo("阳", "金", "jiaHeavenly", listOf("taiyangMaj", "wuquMaj", "taiyinMaj", "tiantongMaj")),
    "xinHeavenly" to HeavenlyStemInfo("阴", "金", "yiHeavenly", listOf("jumenMaj", "taiyangMaj", "wenquMin", "wenchangMin")),
    "renHeavenly" to HeavenlyStemInfo("阳", "水", "bingHeavenly", listOf("tianliangMaj", "ziweiMaj", "zuofuMin", "wuquMaj")),
    "guiHeavenly" to HeavenlyStemInfo("阴", "水", "dingHeavenly", listOf("pojunMaj", "jumenMaj", "taiyinMaj", "tanlangMaj")),
)