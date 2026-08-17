# K2 Source Lineage Protocol

K2 does not start by extracting rules from all 515 sources. The first step is to determine which records are truly independent works, which are editions or copies of the same work, which are later commentaries, and which are notes/code/indexes derived from other material.

## Why this gate exists

SHA256 deduplication only removes byte-identical copies. It does not prevent two different scans, two editions, a modern typeset edition, an AI note and project code derived from the same underlying book from being counted as five independent confirmations.

K2 therefore assigns exactly one lineage disposition to every K1 canonical source.

## Public lineage record

One row per canonical `source_id` in `knowledge/K2_SOURCE_LINEAGE.jsonl`.

Core fields:

- `work_id`: stable identity for the underlying work where known.
- `relation`: PRIMARY_WORK / SAME_WORK_VARIANT / COMMENTARY_DERIVATIVE / SECONDARY_NOTE / IMPLEMENTATION / AUXILIARY_INDEX / OUT_OF_SCOPE / UNKNOWN.
- `parent_work_ids`: dependency links for commentary/derivative material.
- `independence_class`: how this source may be counted during later cross-verification.
- `lineage_basis` and `lineage_evidence`: evidence for the relationship.
- `k2_eligible`: whether the source enters a governed K2 processing lane.
- `read_priority`: P0–P3 or SKIP.

## Independence rules

1. Two files that are editions/scans/typesettings of the same underlying work share a `work_id`; only one may be a primary independence candidate.
2. Secondary notes never become independent textual votes merely because they have a different SHA256.
3. Project code is implementation evidence only. It may prove what the current engine does, not what traditional doctrine says.
4. Commentary on an older work has its own authorship and may contain novel claims, but its dependence on the parent work must remain explicit. Claim-level independence is decided later, not assumed at source level.
5. `UNKNOWN` is valid. If lineage cannot be established from file/title/content evidence, keep it unknown.
6. `OUT_OF_SCOPE` remains preserved for provenance but is skipped by the six-domain claim pipeline.

## Balanced reading

K2 must not finish Qimen before the other domains begin. Source-lineage coverage is global: all 515 K1 canonical source IDs receive a disposition before Claim Extraction is unlocked.

After lineage closure, reading waves are selected per semantic domain. Thin corpora such as Liuyao/Liuren are processed completely before their scarcity is interpreted as evidence strength.

## Copyright boundary

Local books, scans, OCR and extracted page images remain outside Git. Public K2 files contain only derived metadata, short evidence descriptions and later normalized claims/evidence records. Modern long-form text is never copied into the repository.
