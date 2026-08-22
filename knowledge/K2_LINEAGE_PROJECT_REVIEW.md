# K2 Source Lineage — Project Review

## Review status

`PASS`

Accepted data head: `d942b28c01b862a404784cefdb5a8e64fc5fcb86`.

Accepted CI run: `32043681020` — SUCCESS.

## What was resolved

The first K2 lineage draft correctly separated source roles but conflated two different coverage relations: alternate carriers of the same content and complementary volumes/page segments. The remediation re-reviewed the old 97 SAME_WORK_VARIANT rows and closed the upgraded validator from 405 issues to 0.

Final accepted relation counts:

- PRIMARY_WORK 58
- WORK_PART 39
- SAME_WORK_VARIANT 19
- COMMENTARY_DERIVATIVE 6
- SECONDARY_NOTE 159
- IMPLEMENTATION 65
- AUXILIARY_INDEX 67
- OUT_OF_SCOPE 6
- UNKNOWN 96

There are 515 lineage rows and 371 non-null work IDs.

## Coverage model accepted

- PRIMARY_WORK: complete underlying work carrier.
- WORK_PART: complementary volume/part/page coverage. It is not another independent vote, but remains K2-eligible and must be read.
- SAME_WORK_VARIANT: redundant/alternate carrier pointing directly to a PRIMARY_WORK or WORK_PART through `variant_of_source_id`.
- SECONDARY_NOTE / IMPLEMENTATION / AUXILIARY_INDEX remain outside the traditional textual reading lane.
- semantic UNKNOWN textual sources remain unresolved rather than being guessed.

## Project-side family checks

- 《紫微斗数全集》一至六卷 are six WORK_PART rows under one work family and remain readable.
- 八字真诀启示录 separates 火/电/雷/风 unique coverage from redundant page-split carriers.
- ChengGu remains IMPLEMENTATION / IMPLEMENTATION_ONLY / SKIP while its K1 semantic OUT_OF_SCOPE status is preserved.
- 六爻 thin corpus retains the three direct books plus cross-routed《火珠林》as governed textual candidates.
- 大六壬 keeps two《大六壬探原》carriers in one work family rather than two independent votes.

## Decision

K2A Source Lineage is closed. `K2_SOURCE_LINEAGE_STATE.status = COMPLETE`.

K2B Evidence Extraction is open. Claim Extraction remains blocked.

The 96 semantic-UNKNOWN textual sources are a non-blocking K2A uncertainty but a mandatory K2B discovery backlog; they may not be silently dropped from the eventual all-books absorption process.
