# Qimen cases

Classification is about **when the outcome was known**, not how clever the write-up is.

| class | definition |
|---|---|
| 回溯 | outcome already printed in a book or already known when the chart was read |
| 半盲 | chart or prediction written first; some context known |
| 真盲 | prediction timestamped before the outcome |

This pass does **not** ingest book case narratives as evidence. Book pages cited below are pointers for a later reader with disk access.

---

## 真盲 (from user logs)

### CASE-2026-06-15-ASHARE

- **class:** 真盲 (failed)  
- **input:** 2026-06-15, 时家盘 used for A-share session (exact hour not re-verified this pass)  
- **pre-registered call:** 偏弱震荡, 小阴或平盘  
- **reality:** 沪指 +1.61% close 4096; 深成 +3.79%; 创业板 +5.3%  
- **rules used (author later listed):** 天芮+死门 as whole-board bearish; 甲子戊逢空 = 量能不足; 马星+白虎 as ominous; ignored 乾6 开门+天心  
- **hindsight:** the write-up *after* the close is analysis, not a second prediction  
- **reproducible by another person?** the **call vs close** is reproducible; the **chart** is not, because hour and ju method were not frozen in the log I read  
- **hit / miss:** direction miss  
- **source:** `修炼日志/实战预测_2026-06-15_A股.md`, `实战预测失败反省_2026-06-15.md`

### CASE-2026-06-16-WX

- **class:** 真盲 (user labeled ✅ weather)  
- **input / chart:** not reconstructed this pass  
- **rule claimed:** 值符五行定天象  
- **hindsight risk:** seasonal base rate (user later warned 6/27)  
- **source:** 规则回收 §六

### CASE-2026-06-19-ASHARE

- **class:** 真盲 / invalid  
- **call:** A-share day  
- **reality:** market closed  
- **lesson:** precondition “object exists today”  
- **source:** 规则回收 §六

### CASE-2026-06-22 / 24 / 29 / 07-01 / 07-02 A-share

- **class:** 真盲 (user self-scores mixed)  
- **this pack:** listed only. Charts not rebuilt. **Do not promote any of these to fixtures.**  
- **source:** 规则回收 §六

### CASE-2026-06-27-WX

- **class:** 真盲 miss  
- **note:** user: seasonal weather can override plate signal

### CASE-2026-08-12-GZ-WX

- **class:** 半盲 / pending in the 8/11 note (prediction written 8/11 for 8/12 Guangzhou weather)  
- **call:** 多云为主, 短时零星阵雨, 闷热  
- **this pass:** did not look up whether the 8/12 outcome was later filled  
- **source:** `批判分析与理论进化_2026-08-11.md`

---

## 半盲

### CASE-2026-08-07-BOUNDARY

- **class:** 半盲 calendar check (not a fortune)  
- **input:** 2026-08-07  
- **computed:** 癸丑 (two anchors); 立秋; 阴遁; 拆补 vs 置闰 may disagree  
- **not a prediction**  
- **source:** `学习笔记/交叉验证记录_2026-08-07.md`

### CASE-2026-08-12-SCRIPT

- **class:** 半盲 / diary  
- **input:** 2026-08-12 申时 15:37 hardcoded in `paipan_core.py`  
- **author status:** 天盘/门盘/神盘 **not emitted**  
- **source:** N05  
- **use:** proves the script is incomplete; **not** a fixture

---

## 回溯 (book)

User notes summarize many printed cases (B01 work/lawsuit/fengshui; B02 45 cases; B04 sports/debt).  

**Rule for the next agent:** each book case is 回溯 unless a timestamped pre-registration exists.  
**Do not** compute “accuracy” from them.  
**Do not** copy case stories into the App.

If a later pass needs a **chart-only** fixture from a book, extract only: datetime, school, expected 九宫 仪/星/门/神 — never the omen essay.

---

## Counts this pass

| class | listed | chart independently rebuilt |
|---|---:|---:|
| 真盲 | 8+ (A-share/weather series) | 0 |
| 半盲 | 2 | 0 |
| 回溯 | many in notes, not imported | 0 |
