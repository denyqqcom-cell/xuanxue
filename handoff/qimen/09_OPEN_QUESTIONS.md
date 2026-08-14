# Open questions (qimen)

## Cannot decide yet

1. **洛书 walk** after 戊 is placed on ju (C-PLATE-WALK).  
2. **人盘** clockwise-only vs 阴逆 (C-GATE-ROTATION).  
3. **拆补** on jieqi longer than 15 days (day 16+).  
4. Whether **交节时刻** uses 真太阳时 or civil clock. No local spec.  
5. **飞宫** full mapping (中门, 神名). Only a chapter outline in notes.  
6. Outcome of CASE-2026-08-12 Guangzhou weather — note was still waiting.  
7. Author identity on several filenames (“佚名” vs 幺学声 / 王云鹏) — taken from user notes, not title pages reopened this pass.  
8. B22 烟波钓叟歌: table in notes vs the actual scan.

## Highest-conflict rules

1. B01 pp.66–68 拆补 self-contradiction.  
2. 人盘 rotation.  
3. 晚子时 20–23 vs 23–24 (treat 20–23 as a bad note).  

## Missing evidence

- No independently rebuilt full 九宫 from two books for the same datetime.  
- No open-source licensed qimen engine in the corpus.  
- 24 jieqi ju table not checked against B22 this pass.  
- 费秉勋 1991, 曾子南, 姜春龙, 图解三部: unread.

## Next books to open (disk required)

1. B01 + B02 text layer: verify ju chapters only (do not ingest omen chapters).  
2. B22 scan: jieqi ju mnemonic only.  
3. One **single** worked 阴遁 and one 阳遁 full plate from B07 or B02 with datetime printed.  
4. Ignore B08/B09 (540-ju pictures) until the engine exists.

## Blind tests to run

1. Freeze `QimenRequest` for the next 5 civil days (hour=午) **before** looking at any website; compare only pillars + ju.  
2. Do not use A-share or weather for engine tests.  
3. If a website disagrees, log it as `UNTRUSTED_ORACLE`, not as ground truth.
