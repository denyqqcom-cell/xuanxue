# QM-SRC-0024 Targeted Provenance Visual Review

Status: TARGETED_VISUAL_REVIEW / PROVENANCE_ONLY / NO_FULL_READING_CREDIT / NO_EMPIRICAL_CREDIT

Date: 2026-08-21

Source: `QM-SRC-0024 / 《笺元遁甲句解烟波钓叟歌》` candidate ancient-text witness.

Canonical SHA256 checked locally before review:

`fdcbe9fff20917c4e65e07ca04d0d025f3e1b635051f13e882b3b719d0f2913a`

Matches the indexed Qimen source registry.

PDF page count: `110`.

## Why this page was opened

Legacy `qimen-yange` had treated the label

`《笺元遁甲句解烟波钓叟歌》宋·赵普撰，明刊本`

as one bundled attribution even though the current runtime/provenance migration had not yet returned to the scanned witness itself.

The purpose of this session was narrow:

- verify what the scanned witness visibly says about title / Zhao Pu attribution;
- **not** infer historical authorship truth from a filename;
- **not** verify the whole edition description;
- **not** award full-book reading credit;
- **not** operationalize any verse as a Qimen rule.

## Pages visually inspected

Rendered from the canonical PDF at high resolution:

`p1-p12`, with p5 re-rendered at higher DPI for the title/attribution column.

### p1-p3

Cover / blank or library-imaging preliminaries. National Central Library, Taiwan scan/watermark is visible.

### p4

A handwritten/cover-leaf style bibliographic note is visible. This page was **not** treated as sufficient proof of the carrier being a particular Ming edition because the exact note/edition lineage has not yet been independently decoded and checked against a colophon/catalog record.

### p5

This is the key provenance witness.

The original page visibly carries the work title column corresponding to:

`箋元遁甲句解煙波釣叟歌`

Adjacent to it is a separate vertical attribution column naming:

`大宋……同中書門下平章事趙普……`

The middle official-title characters are visually readable enough to identify the Zhao Pu attribution context, but this review deliberately does **not** normalize every historical office-title character into a modern bibliographic statement when the page is not needed for that purpose.

What can now be said safely:

> The canonical scanned witness itself visibly attributes the work/text context to `趙普` on p5.

What cannot yet be said from this alone:

> Zhao Pu historically authored the received text exactly as preserved here.

Witness attribution and historical authorship are different claims.

### p6-p12

Early textual/diagram pages visually confirm that this is a traditional vertical-layout Dunjia textual witness rather than a modern project compilation. These pages were only structurally surveyed in this session; they do not receive Atomic Evidence or full Reading Credit here.

## Provenance decision

Previous project state:

`赵普 attribution = LEGACY_ATTRIBUTION`

New narrow state:

`赵普 attribution on this scanned witness = PAGE_VERIFIED_WITNESS_ATTRIBUTION`

This does **not** automatically upgrade:

- historical authorship truth;
- `明刊本` as a verified edition statement;
- every verse previously copied into legacy `qimen-yange`;
- any method/algorithm claim;
- any Empirical Support.

The edition phrase remains unresolved until a reliable colophon/catalog/witness-level edition check is completed.

## Self-audit lesson

The old project bundled four different assertions into one filename-like string:

`work title + person attribution + dynasty attribution + edition attribution`

One visible p5 witness now supports only part of that bundle.

Therefore provenance fields should be independently upgradable:

`TITLE_WITNESS / PERSON_ATTRIBUTION_WITNESS / HISTORICAL_AUTHORSHIP / EDITION_WITNESS`

This is the same general lesson as sequence-object and representation-object type safety:

**a convenient single label may hide several claims with different evidence.**

No new top-level K2 schema is added solely for this observation. The distinction is recorded in the yange provenance skill and used during future full-source reading.

## Next step

A future full `QM-SRC-0024` K2 reading must proceed page-by-page/meaningful-unit under `VISUAL_REQUIRED` and separately determine:

- textual units / commentary units;
- title/attribution/edition witnesses;
- verse variants relative to later modern transcriptions;
- which formulas actually belong to this witness;
- whether operational setup verses carry enough method context to enter qimen-qiju comparison.

Until then, this remains a targeted provenance improvement, not a claim that the source has been fully learned.
