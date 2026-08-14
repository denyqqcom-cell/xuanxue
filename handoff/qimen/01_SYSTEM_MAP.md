# Qimen system map

This is a map, not a unified theory. Three layers must stay separate.

```
civil datetime + timezone + (optional) longitude
        │
        ▼
[A] calendar   节气 / 阴阳遁 / 日柱时柱 / 早晚子时 / 旬首遁仪旬空
        │
        ▼
[A] ju         拆补 | 置闰 | 茅山     ← school fork, do not merge
        │
        ▼
[A] plates     地盘九仪 → 值符值使 → 天盘九星 → 人盘八门 → 神盘八神
        │                   (转盘/排宫 default)     (飞宫 is another school)
        ▼
[B] structure  九宫 / 三奇六仪 / 八门 / 九星 / 八神 / 马星 / 空亡
        │
        ▼
[B] yongshen   时家默认：日干=人, 时干=事 + 事项用神
               善天道可改用 年命
        │
        ▼
[B/C] relations  生克 / 主客(地盘=主,天盘=客) / 伏吟反吟 / 门迫击刑入墓
        │
        ▼
[C] timing     应期（空墓冲填 / 值使落宫数 / 马星 / 合处逢冲）
        │
        ▼
output         QimenChart + optional judgement objects that are NEVER auto-truth
```

## Layer tags

| Tag | Meaning |
|---|---|
| A | Encodable if inputs are exact. Still has school forks. |
| B | School rule. Must be a config enum, not a silent default merge. |
| C | Experience / judgement. May be shown as hint, never as math. |

## A — chart construction

Determined enough to design code, **not** all ready for golden fixtures:

- 60-jiazi indexing, 五鼠遁 hour pillar
- 旬首 → 遁仪 → 旬空
- 阳遁冬至后 / 阴遁夏至后 (boundary = exact solar term, not “8.7”)
- 九仪 order 戊己庚辛壬癸丁丙乙; 阳顺阴逆 on 洛书
- “甲子戊在 X 宫 = X 局”
- 拆补 (recommended default in this corpus): 节气内第 1–5 / 6–10 / 11–15 日 → 上/中/下元, then 24-jieqi ju table
- 转盘: 值符星随时干; 值使门随时支 (notes also say 八门永远顺时针 — see conflicts)

Not determined this pass:

- Exact 飞宫 algorithm (only a chapter outline in B02 notes)
- 年家 / 月家 / 日家 full engines
- 天盘/门盘/神盘 of the local Python script (author left them unimplemented on purpose)

## B — school forks (keep all)

| Fork | Options in this corpus |
|---|---|
| Ju method | 拆补 / 置闰(符头甲己) / 茅山 / B02 also names 不拆不闰、灵机诹局 |
| Hour / day change | 早子 00–01; 晚子 23–00. Notes disagree whether 20–23 is 晚子 |
| True solar time | mentioned as open practice, **no local algorithm verified** |
| Yongshen | 幺学声 日干人+时干事 vs 善天道 年命偏重 |
| Urgency | 幺学声 fixed priority 开门>值符>生门 vs 善天道 急从神/缓从门 |
| Board | 转盘/排宫 vs 飞宫 (中门, 八神 names differ: 勾陈/太常/朱雀 vs 白虎/玄武…) |
| Scope | 时家 (default) / 日家 / 月家 / 年家 |

## C — experience

- 凶格计分, 开门政策优先, 马星中性, 逢空=方向待定
- 求财用神套件, 天气值符五行
- 情境推演 v0.1/v0.2
- Book omen tables (90 十干克应, 64 八门静应)

These can be data tables + UI copy. They cannot be scoring oracles.

## What the App should expose

1. A reproducible **时家拆补转盘** chart.  
2. School switches for 置闰 / 飞宫 / 年命, disabled or labeled experimental until fixtures exist.  
3. Judgement text as “sourced hint”, never “the answer”.
