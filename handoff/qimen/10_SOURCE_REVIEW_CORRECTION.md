# Qimen source re-read correction — 2026-08-14

Purpose: record a correction discovered after the original disk handoff was produced. This file does **not** rewrite or erase the original handoff; it documents why implementation decisions changed after direct source access became available.

## 1. What changed

The original handoff separated two candidate meanings of “拆补”:

- `CHAI_BU_DAYCOUNT`: after a jieqi boundary, day 1–5 / 6–10 / 11–15 directly means 上 / 中 / 下元.
- `CHAI_BU_FUTOU`: the jieqi changes immediately at the exact term instant, but 元 continues to be determined by the nearest 甲/己日符头 and its branch group.

The first handoff promoted `CHAI_BU_DAYCOUNT` as the default mainly because that pass could not independently reopen the PDFs. That promotion is now withdrawn.

## 2. Direct source review

Two independently readable modern sources were re-checked directly:

### B01 幺学声《奇门遁甲预测学》

The relevant section around pp. 66–68 describes 拆补 as:

- entering the new jieqi immediately at the actual term boundary;
- still using the day stem/branch futou to determine 上、中、下元;
- allowing a partial yuan around the term boundary, which is why the method is called “拆补”.

Worked example recorded by the source: on 2004-02-04 after 立春, day pillar 癸丑 looks back to futou 己酉; 己酉 belongs to the 上元 branch group, therefore 立春 uses 阳遁八局.

### B05 善天道《奇门遁甲讲义》

The section titled “拆补法定局” gives the same runtime structure:

- 子午卯酉 → 上元;
- 寅申巳亥 → 中元;
- 辰戌丑未 → 下元;
- the exact jieqi instant switches the jieqi system immediately;
- the current futou-defined yuan does not automatically reset to 上元.

Worked example recorded by the source: 1996-02-04 at the 立春节气 boundary changes from 大寒 to 立春, while the current futou remains 己巳, so the new 立春局 is 中元阳五局 rather than 上元阳八局.

## 3. Engineering correction

Effective for `qimen-core-v1`:

- default method becomes `CHAI_BU_FUTOU`;
- `CHAI_BU_DAYCOUNT` is kept as an explicit unresolved/unsupported method id so historical handoff data is not silently deleted;
- exact jieqi time and yuan resolution are separate functions;
- `civilDayIndex` since a jieqi is metadata only and must **not** be used as the default yuan resolver;
- 置闰、茅山、飞宫、真太阳时 remain unsupported;
- this correction still does not unlock the nine-palace plate.

## 4. Jieqi clock

The rounded dates such as “立春 2.4 / 立秋 8.7” remain teaching approximations and are not valid software boundaries.

`qimen-core` uses the already-declared MIT dependency `cn.6tail:lunar:1.7.7` for local exact jieqi timestamps and tests exact second-level boundaries. No network lookup is used.

## 5. Copyright boundary

No source prose, page image, full table facsimile, OCR dump, omen dictionary, or modern commentary is copied into the App.

The implementation keeps only:

- short identifiers;
- algorithmic relationships rewritten in project language;
- numeric/branch mapping data required for computation;
- minimal factual worked-case inputs used as tests.

Original PDFs and OCR derivatives remain research-only and must not be packaged into APK/AAB.

## 6. Still unresolved

This correction only closes the default 拆补“如何定元” ambiguity for the current source set. It does **not** establish that one lineage is universally correct. Other schools remain separate configuration candidates and require their own sources plus fixtures before they can be enabled.

The next hard blocker remains the complete earth-plate walk and then full-board fixtures. Until that is closed, `plateState=LOCKED_UNVERIFIED` is intentional.
