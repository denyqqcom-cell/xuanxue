# Qimen copyright gate

This is an engineering gate, not a legal opinion.

## Allow in the App (code + short UI copy)

| item | why |
|---|---|
| 60-jiazi, 五鼠遁, 旬首/旬空 maps | traditional calendrical procedures; rewritten; multi-source |
| 洛书 palace numbers, 九星/八门 home lists as **data enums** | standard structure; do not ship decorative 图解 |
| User-written rules that are procedures (拆补 day-count, 击刑 map as numbers) | user’s rewrite, still cite school |
| MIT/Apache notices already in `xuanxue` | existing |
| This `handoff/qimen/` pack | written for engineering; no book facsimile |

## Research only (repo notes OK, **do not pack into APK**)

| item | why |
|---|---|
| `奇门/` study notes, 修炼日志, qclaw | user commentary; qclaw still quotes modern books |
| Page citations to 幺学声 / 王云鹏 / 善天道 | necessary attribution |
| Conflict write-ups | commentary |
| 十干克应 / 八门静应 **name lists** in notes | derived from B06 modern book; if ever used, only as optional research overlay, never default APK copy |

## Forbidden to package

| item | why |
|---|---|
| Any PDF in F:\ or E:\ | modern publication or modern scan/edition |
| `_txt/*`, `生成内容/*全文.txt`, `_scan_txt`, `_scan_pages` | full OCR / page images = substitute for the book |
| 图解 540/1080 局 diagrams | modern book art |
| 善天道 / 曾子南 / 姜春龙 / 费秉勋 1991 running text | modern copyright |
| 金函玉镜 / 甲遁 / 烟波钓叟歌 **library scans and modern punctuation editions** | photos + modern typesetting/notes are not a public-domain grant |
| 梁湘润《奇门遁甲入门》 | modern |
| Third-party “在线排盘” output as a bundled database | unknown license + unknown algorithm |
| Commercial fonts, icons, other app screenshots | already banned in UI/UX v2 |

## Software already on disk

| file | license | commercial? | copy of third party? | gate |
|---|---|---|---|---|
| `paipan_core.py` | user, no SPDX | user-owned | no; **wrong to treat as correct** | research; do not ship as engine |
| `ganzhi_check.py` / extract_*.py | user | user-owned | scrapers for local PDFs | do not ship extractors or their output |
| No iztro-like qimen MIT library found | — | — | — | write original Kotlin |

## Yellow leftovers

- qclaw files contain **block quotations** from B01/B02/B03/B07. They stay in the research tree. Do not copy those quotations into `handoff` or APK.  
- User knowledge-base 十干克应 90 / 八门静应 64 is a compact of B06. **Do not** paste those omen strings into Android strings.xml.

## Release checklist (qimen module)

- [ ] No file from `F:\奇门遁甲` or E-disk books in the APK  
- [ ] No OCR dump in assets  
- [ ] Every user-visible omen line has `school` + `source_id` or is omitted  
- [ ] Calendar tables in code are rewritten procedures, not scanned pages
