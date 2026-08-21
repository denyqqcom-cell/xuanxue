# QM-SRC-0022 Targeted Deity-Lineage Visual Review

Status: TARGETED_VISUAL_REVIEW / LINEAGE_ONLY / NO_FULL_READING_CREDIT / NO_EMPIRICAL_CREDIT

Date: 2026-08-21

Source: `QM-SRC-0022 / 《甲遁真授秘录》上册` indexed carrier.

Indexed metadata currently gives:

- source type: `ANCIENT_TEXT`;
- era: `PRE_MODERN`;
- title/薛凤祚 attribution still originates from filename-level metadata, not this session's authorship verification;
- canonical SHA256: `f329d9d13ef7e8ad78de5d6a29801427445dba15bcd1a9df152fa1cd5b436e03`;
- PDF pages: `188`;
- K2 lineage row remains `UNKNOWN / k2_eligible=false / work_id=null` pending formal lineage intake.

This session therefore does **not** upgrade author, edition, full-source lineage eligibility or whole-book Reading status.

## 1. Why this source was opened

AQ-003 asks for an earlier/independent witness that can attack the unresolved `勾陈/朱雀` versus `白虎/玄武` taxonomy with actual naming + movement context.

The target was not “find an old book that agrees with us”.

The target was:

> does an early carrier expose a deity sequence that the current four-hypothesis model does not already cover?

## 2. Navigation discipline

The PDF text layer/OCR is noisy. Keyword search for `朱雀 / 白虎 / 玄武 / 九地 / 九天` was used only to locate candidate pages.

All accepted observations below were rechecked on rendered original pages.

A critical false-positive example occurred on PDF p44: the page discusses `天将阴阳干支所属` and a twelve-deity/general context. Terms such as `白虎` there are **not automatically Qimen eight-deity evidence**.

This is a concrete `SEMANTIC_DOMAIN_COLLISION` warning:

`same token != same method object`.

Keyword/OCR hit alone is not lineage evidence.

## 3. Original-page observations

### PDF p21-p22 — Qimen algorithm context

The surrounding pages visibly discuss Qimen objects such as:

- 六甲遁仪；
- 八门；
- 九星；
- 顺逆飞遁；
- 阴阳二至；
- 直符。

PDF p22 left page contains the key sequence in one continuous method context. The visible wording includes:

`天乙隨六甲加時干，是以名直符`

followed by an eight-position sequence visibly abbreviated as:

`直符 / 蛇 / 陰 / 六合 / 朱 / 白 / 九地 / 九天`

and then movement wording:

`照順逆飛遁，陰陽二至分順逆...`

The review intentionally preserves the page's abbreviations `蛇 / 陰 / 朱 / 白`. It does not silently expand them into normalized modern enum names where the page itself is abbreviated.

### PDF p37 — five auspicious members inside the eight-deity set

In the same carrier, PDF p37 right page visibly states in substance that the `五勝` are five auspicious deities among the eight and names:

`天乙 / 太陰 / 六合 / 九地 / 九天`.

This independently clarifies two points relevant to p22:

1. `天乙` belongs to the source's deity framework and is tied to the `直符` discussion;
2. `太陰 / 六合 / 九地 / 九天` are explicit full names corresponding to part of the abbreviated p22 sequence.

The remaining p22 positions visibly contain both `朱` and `白` at the same time.

## 4. Lineage consequence

The current project previously considered at least:

- `ALIAS_WITH_CONTEXT`;
- `LAYERED_HIDDEN_DEITY`;
- `YIN_YANG_SUBSTITUTION`;
- `EDITORIAL_SYNTHESIS / MULTIPLE_METHOD_LAYERS`.

QM-SRC-0022 adds a materially different source witness:

`ZHU_BAI_DUAL_POSITION_WITNESS`

Meaning only:

> in this visually checked Qimen method context, the eight-position sequence contains both `朱` and `白` simultaneously, with no visible need on these pages to collapse one into the other.

This is **not** yet normalized as `朱雀 + 白虎` in runtime code, because the p22 list itself uses single-character abbreviations. It is also not evidence that every section of the carrier uses the same taxonomy.

## 5. What this attacks

This witness makes several universal claims harder to defend:

- `白虎 = 勾陈` universally;
- `玄武 = 朱雀` universally;
- `阳遁必为勾陈/朱雀，阴遁必为白虎/玄武` universally;
- one modern eight-deity enum can be projected backwards into every textual lineage.

The correct update is not “the old book wins”.

It is:

`deity taxonomy has at least one additional source-specific naming lineage`.

Therefore Test C remains `UNRESOLVED`, but the space of plausible source lineages is now better constrained and a universal two-name-pair synthesis is further weakened.

## 6. Source-topology lesson

This carrier also demonstrates why whole-book keyword search can be dangerous.

Within one scanned volume, nearby regions can use overlapping tokens such as `白虎 / 玄武 / 朱雀` in different method objects. A lexical match is not enough; every hit needs:

`TOKEN -> LOCAL_SECTION -> METHOD_OBJECT -> RELATION -> LINEAGE_CLAIM`.

This is the source-reading analogue of `Sequence-Object Type Safety` and `Representation-Object Type Safety`.

Working label:

**Semantic-Object Type Safety**

A familiar symbol name does not identify its method role by itself.

This is a research discipline, not a new theory version or runtime gate yet.

## 7. AQ-003 stopping discipline

This round had predeclared at most two early-source probes:

1. `QM-SRC-0024` — provenance improved, deity movement `NO-OP`;
2. `QM-SRC-0022` — one usable early Qimen deity-sequence/movement witness.

The project will **not immediately open a third ancient source just to accumulate supporting examples**. AQ-003 pauses here for this round so that the new witness is integrated and challenged before more source accumulation.

This is deliberate `STOPPING_DOF` control.

## 8. Credit boundary

Allowed credit:

`TARGETED PAGE-LEVEL SOURCE/LINEAGE WITNESS`.

Not allowed:

- `QM-SRC-0022 Reading COMPLETE`;
- verified historical authorship/edition;
- runtime deity taxonomy replacement;
- prediction validity;
- Empirical Support;
- v0.4 theory upgrade.
