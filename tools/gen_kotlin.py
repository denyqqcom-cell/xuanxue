#!/usr/bin/env python3
"""Generate Kotlin data tables + i18n maps from iztro TypeScript source."""
import re, json, os

SRC = "/home/joe/iztro/src"
OUT = "/home/joe/xuanxue/ziwei-core/src/main/kotlin/com/xuanxue/ziwei/gen"
os.makedirs(OUT, exist_ok=True)

def strip_ts(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'\bas const\b', '', text)
    text = re.sub(r'export (default|const)\s*', '', text)
    # convert single-quoted strings to double-quoted
    text = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", r'"\1"', text)
    # quote unquoted keys
    text = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', text)
    # strip trailing commas before } or ]
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    return text

def parse_obj(path):
    t = strip_ts(open(path, encoding='utf-8').read())
    m = re.search(r'(\{.*\})\s*;?\s*$', t, re.S)
    if not m:
        raise ValueError("cannot find object in " + path)
    return json.loads(m.group(1))

# ---------- i18n ----------
LOC = os.path.join(SRC, "i18n", "locales", "zh-CN")
i18n = {}
i18n.update(parse_obj(os.path.join(LOC, "common.json")))
for f in ["fiveElementsClass.ts", "heavenlyStem.ts", "earthlyBranch.ts",
          "brightness.ts", "mutagen.ts", "star.ts", "palace.ts", "gender.ts"]:
    i18n.update(parse_obj(os.path.join(LOC, f)))

def kot_str(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

# en-US reverse-lookup tables (iztro relies on these for pinyin arg resolution, e.g. 'woo' -> wuEarthly)
def parse_ts_obj(path):
    t = strip_ts(open(path, encoding='utf-8').read())
    m = re.search(r'(\{.*\})\s*;?\s*$', t, re.S)
    return json.loads(m.group(1)) if m else {}

en_eb = parse_ts_obj(os.path.join(SRC, "i18n", "locales", "en-US", "earthlyBranch.ts"))
en_hs = parse_ts_obj(os.path.join(SRC, "i18n", "locales", "en-US", "heavenlyStem.ts"))

lines = ['// AUTO-GENERATED from iztro (https://github.com/SylarLong/iztro) MIT - do not edit by hand',
         'package com.xuanxue.ziwei.gen', '',
         'object I18nZh {',
         '    val map: Map<String, String> = mapOf(']
for k, v in sorted(i18n.items()):
    lines.append('        "' + k + '" to "' + kot_str(v) + '",')
lines += ['    )', '',
          '    fun t(key: String): String = map[key] ?: ""', '',
          '    // en-US reverse lookups: iztro resolves pinyin args ("shen", "woo"...) through the en-US locale',
          '    val enEarthly: Map<String, String> = mapOf(' +
          ', '.join('"' + v + '" to "' + k + '"' for k, v in en_eb.items()) + ')',
          '    val enHeavenly: Map<String, String> = mapOf(' +
          ', '.join('"' + v + '" to "' + k + '"' for k, v in en_hs.items()) + ')',
          '',
          '    fun kot(value: String, prefix: String? = null): String {',
          '        for ((k, v) in map) {',
          '            if ((prefix == null || k.contains(prefix)) && v == value) return k',
          '        }',
          '        if (prefix == "Earthly") enEarthly[value]?.let { return it }',
          '        if (prefix == "Heavenly") enHeavenly[value]?.let { return it }',
          '        return value',
          '    }', '}']
open(os.path.join(OUT, "I18nZh.kt"), "w", encoding="utf-8").write("\n".join(lines))
print("I18nZh.kt:", len(i18n), "entries")

# ---------- data ----------
D = os.path.join(SRC, "data")
ct = strip_ts(open(os.path.join(D, "constants.ts"), encoding='utf-8').read())

def grab(name, kind):
    pat = name + r'\s*=\s*(' + kind + r')'
    m = re.search(pat, ct, re.S)
    return json.loads(m.group(1)) if m else None

HEAVENLY_STEMS = grab('HEAVENLY_STEMS', r'\[.*?\]')
EARTHLY_BRANCHES = grab('EARTHLY_BRANCHES', r'\[.*?\]')
ZODIAC = grab('ZODIAC', r'\[.*?\]')
PALACES = grab('PALACES', r'\[.*?\]')
CHINESE_TIME = grab('CHINESE_TIME', r'\[.*?\]')
TIME_RANGE = grab('TIME_RANGE', r'\[.*?\]')
TIGER_RULE = grab('TIGER_RULE', r'\{.*?\}')
RAT_RULE = grab('RAT_RULE', r'\{.*?\}')
GENDER = grab('GENDER', r'\{.*?\}')
assert HEAVENLY_STEMS and EARTHLY_BRANCHES and PALACES and CHINESE_TIME, "constants parse failed"

stars_ts = strip_ts(open(os.path.join(D, "stars.ts"), encoding='utf-8').read())
m = re.search(r'MUTAGEN\s*=\s*(\[.*?\])', stars_ts, re.S)
MUTAGEN = json.loads(m.group(1)) if m else None
m = re.search(r'STARS_INFO\s*=\s*(\{.*?\})\s*;?\s*$', stars_ts, re.S)
STARS_INFO = json.loads(m.group(1)) if m else None
assert MUTAGEN and STARS_INFO, "stars parse failed"

hs = parse_obj(os.path.join(D, "heavenlyStems.ts"))
eb = parse_obj(os.path.join(D, "earthlyBranches.ts"))

def klist(arr):
    return ', '.join('"' + x + '"' for x in arr)

out = ['// AUTO-GENERATED from iztro (https://github.com/SylarLong/iztro) MIT - do not edit by hand',
       'package com.xuanxue.ziwei.gen', '',
       'object DataTables {',
       '    val HEAVENLY_STEMS: List<String> = listOf(' + klist(HEAVENLY_STEMS) + ')',
       '    val EARTHLY_BRANCHES: List<String> = listOf(' + klist(EARTHLY_BRANCHES) + ')',
       '    val ZODIAC: List<String> = listOf(' + klist(ZODIAC) + ')',
       '    val PALACES: List<String> = listOf(' + klist(PALACES) + ')',
       '    val CHINESE_TIME: List<String> = listOf(' + klist(CHINESE_TIME) + ')',
       '    val TIME_RANGE: List<String> = listOf(' + klist(TIME_RANGE) + ')',
       '    val MUTAGEN: List<String> = listOf(' + klist(MUTAGEN) + ')',
       '    val TIGER_RULE: Map<String, String> = mapOf(' +
       ', '.join('"' + k + '" to "' + v + '"' for k, v in TIGER_RULE.items()) + ')',
       '    val RAT_RULE: Map<String, String> = mapOf(' +
       ', '.join('"' + k + '" to "' + v + '"' for k, v in RAT_RULE.items()) + ')',
       '    val GENDER: Map<String, String> = mapOf(' +
       ', '.join('"' + k + '" to "' + v + '"' for k, v in GENDER.items()) + ')',
       '    val FIVE_ELEMENTS_VALUE: Map<String, Int> = mapOf(' +
       ', '.join('"' + k + '" to ' + str(v) for k, v in
                 {"water2nd": 2, "wood3rd": 3, "metal4th": 4, "earth5th": 5, "fire6th": 6}.items()) + ')',
       '    val STARS_INFO: Map<String, StarInfo> = mapOf(']
for star, info in STARS_INFO.items():
    b = info.get('brightness', [])
    bl = ', '.join('"' + x + '"' for x in b)
    out.append('        "' + star + '" to StarInfo(listOf(' + bl + '), "' + info.get('fiveElements', '') + '", "' + info.get('yinYang', '') + '"),')
out += ['    )', '}', '',
        'data class StarInfo(',
        '    val brightness: List<String>,',
        '    val fiveElements: String = "",',
        '    val yinYang: String = "",',
        ')',
        '',
        'data class EarthlyBranchInfo(',
        '    val yinYang: String,',
        '    val fiveElements: String,',
        '    val crash: String,',
        '    val soul: String,',
        '    val body: String,',
        '    val inside: String,',
        '    val outside: String,',
        '    val healthTip: String,',
        ')',
        '',
        'val EARTHLY_BRANCH_INFO: Map<String, EarthlyBranchInfo> = mapOf(']
for k, v in eb.items():
    yy = v["yinYang"]; fe = v["fiveElements"]; cr = v["crash"]; so = v["soul"]
    bo = v["body"]; ins = v["inside"]; outs = v["outside"]; ht = v["healthTip"]
    out.append('    "' + k + '" to EarthlyBranchInfo("' + yy + '", "' + fe + '", "' + cr + '", "' + so + '", "' + bo + '", "' + ins + '", "' + outs + '", "' + ht + '"),')
out += [')', '',
        'data class HeavenlyStemInfo(',
        '    val yinYang: String,',
        '    val fiveElements: String,',
        '    val crash: String,',
        '    val mutagen: List<String>,',
        ')',
        '',
        'val HEAVENLY_STEM_INFO: Map<String, HeavenlyStemInfo> = mapOf(']
for k, v in hs.items():
    ml = ', '.join('"' + x + '"' for x in v['mutagen'])
    out.append('    "' + k + '" to HeavenlyStemInfo("' + v["yinYang"] + '", "' + v["fiveElements"] + '", "' + v.get("crash", "") + '", listOf(' + ml + ')),')
out += [')']
open(os.path.join(OUT, "DataTables.kt"), "w", encoding="utf-8").write("\n".join(out))
print("DataTables.kt written. stars:", len(STARS_INFO), "earthlyBranches:", len(eb), "heavenlyStems:", len(hs))
