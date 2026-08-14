# Qimen handoff summary

Date: 2026-08-14.  
One module only. Bazi / liuyao / liuren are **not** in this folder.

## What was actually used

| class | n | how used |
|---|---:|---|
| Unique book PDFs inventoried | 30 | path, size, pages from `_books_toc.json`, text-layer flag |
| Duplicate PDFs skipped (E=F) | 29 | same name + same bytes |
| Book PDFs independently re-read this pass | **0** | no PDF library in this environment; scans have no text |
| Books with usable text layer but only via **user notes** | 4 (B01–B04) | 幺学声预测学, 王云鹏应用学, 善天道精华, 善天道高级班 |
| Unread / scan / OCR-fail | 26 | listed in `00_CORPUS_MANIFEST.md` |
| User notes / logs / skills read | yes | primary formal source |
| Local programs re-checked | 1 (`paipan_core.py`) | incomplete, hardcoded anchors, **not** an engine |

Failed / unusable as books this pass: B05 (no text), B07–B19/B22–B28 (scan), B21 (weak OCR), B29 (garbage OCR), B30 (path only), plus all `*全文.txt` (forbidden full OCR).

## Algorithms

| item | status |
|---|---|
| Day pillar (two-anchor) | encodable, fixtures exist |
| Hour pillar 五鼠遁 | encodable, fixtures exist |
| 13-slot 时辰 + 晚子滚日 | encodable as config |
| 旬首 / 遁仪 / 旬空 | encodable, fixtures exist |
| 五不遇时 generator | encodable |
| 六仪击刑 map | encodable as static data (B) |
| 拆补 ju **table** | encodable as data (B); jieqi **clock** not ready |
| 置闰 / 茅山 / 飞宫 / 年家月家日家 | not encodable |
| 地盘 walk / 天盘门盘神盘 | **not** encodable (conflicts + unsourced script) |
| Judgement / 应期 / 克应 strings | not algorithms |

## Rules in `03_RULES.jsonl`

36 rows: **A 3 · B 11 · C 17 · D 5**.  
`implementation_ready=true`: **11**.

## Golden fixtures

17 rows in `05_FIXTURES.jsonl`. All are calendar / table / map checks.  
**Zero** full 九宫 boards.  
**Zero** book fortune cases.

## Biggest school conflict

B01 拆补: 符头 yuan vs 交节日数 yuan (pp.66–68 as cited). Same datetime can yield two ju. App must expose two method ids, not one word “拆补”.

Second: 人盘 阴逆 vs always-clockwise — blocks shipping 人盘.

## Highest copyright risk

1. Shipping any F:/E: PDF or `生成内容/*全文.txt` / `_scan_pages`.  
2. Pasting B06 90+64 omen strings into the APK.  
3. Treating 善天道 / 曾子南 / 费秉勋 1991 / 图解 as “古法无版权”.

## Three tasks for the Kotlin AI (no disk)

1. Create `:qimen-core` and implement only calendar + 旬 + 五不遇时 + 击刑 map, driven by `05_FIXTURES.jsonl`.  
2. Add a jieqi clock behind a test; do not draw 九宫 yet.  
3. Wire `QimenSchoolConfig` enums from `08_IMPLEMENTATION_HANDOFF.md` so 置闰/飞宫/真太阳时 `UnsupportedSchool` instead of fake plates.

Do not “finish qimen” in one PR.
