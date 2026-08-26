# K2 Source Lineage Protocol

K2 does not start by extracting rules from all 515 sources. The first step is to determine which records are truly independent works, which are editions or copies of the same work, which are complementary volumes/parts of one work, which are later commentaries, and which are notes/code/indexes derived from other material.

## Why this gate exists

SHA256 deduplication only removes byte-identical copies. It does not prevent two different scans, two editions, a modern typeset edition, an AI note and project code derived from the same underlying book from being counted as five independent confirmations.

A second failure mode is equally dangerous: **a multi-volume work or page-split corpus can be mistaken for a SAME_WORK_VARIANT family.** Different volumes may contain complementary content. Treating volume 2 as merely an alternate copy of volume 1 can silently drop unique evidence during K2B reading.

K2 therefore assigns exactly one lineage disposition to every K1 canonical source and separates **work identity** from **coverage inside that work**.

## Public lineage record

One row per canonical `source_id` in `knowledge/K2_SOURCE_LINEAGE.jsonl`.

Core fields:

- `work_id`: stable identity for the underlying intellectual work where known.
- `relation`: PRIMARY_WORK / WORK_PART / SAME_WORK_VARIANT / COMMENTARY_DERIVATIVE / SECONDARY_NOTE / IMPLEMENTATION / AUXILIARY_INDEX / OUT_OF_SCOPE / UNKNOWN.
- `part_label`: short label for a complementary volume/part/page segment when `relation=WORK_PART`; null otherwise unless a SAME_WORK_VARIANT targets that part.
- `variant_of_source_id`: direct canonical carrier that a SAME_WORK_VARIANT duplicates or re-expresses. Variants may point only to PRIMARY_WORK or WORK_PART, never to another variant.
- `parent_work_ids`: dependency links for commentary/derivative material.
- `independence_class`: how this source may be counted during later cross-verification.
- `lineage_basis` and `lineage_evidence`: evidence for the relationship.
- `k2_eligible`: whether the source enters a governed K2 processing lane.
- `read_priority`: P0–P3 or SKIP.

## Work / part / variant rules

1. `PRIMARY_WORK` is a carrier representing the complete underlying work. It may be the sole `PRIMARY_CANDIDATE` in its work family.
2. `WORK_PART` is a complementary portion of the same work: volume, fascicle, upper/middle/lower book, or non-overlapping page segment. It shares the same `work_id`, uses `SAME_WORK_NOT_INDEPENDENT`, **but remains `k2_eligible=true` so its unique content is still read**.
3. `SAME_WORK_VARIANT` is an alternate carrier of substantially the same coverage as another canonical source: another scan, typesetting, edition, OCR-derived carrier or clean copy. It must set `variant_of_source_id` to a PRIMARY_WORK or WORK_PART in the same `work_id` family.
4. If two files cover different volumes or page ranges, they are not SAME_WORK_VARIANT merely because a normalized title becomes identical after stripping volume/page markers.
5. If a full-work carrier and split parts both exist, the full carrier may be PRIMARY_WORK while each split carrier is WORK_PART. Alternate copies of a particular split part are SAME_WORK_VARIANT of that WORK_PART.
6. If only split parts exist and no complete carrier exists, the work family may have zero PRIMARY_CANDIDATE. The `work_id` still represents one independent work family; all unique parts remain eligible for reading.
7. A titled series containing separate intellectual works must not be collapsed into one `work_id` merely because the books share a series prefix. Work identity must follow actual bibliographic/content identity, not title normalization convenience.

## Independence rules

1. Different scans/editions/typesettings of the same coverage never become multiple independent votes.
2. Different parts of one underlying work also do not become independent votes; they provide complementary coverage under the same `work_id`.
3. Secondary notes never become independent textual votes merely because they have a different SHA256.
4. Project code is implementation evidence only. It may prove what the current engine does, not what traditional doctrine says.
5. Commentary on an older work has its own authorship and may contain novel claims, but its dependence on the parent work must remain explicit. Claim-level independence is decided later, not assumed at source level.
6. `UNKNOWN` is valid. If lineage cannot be established from file/title/content evidence, keep it unknown.
7. `OUT_OF_SCOPE` is a semantic-routing decision, while IMPLEMENTATION / SECONDARY_NOTE / AUXILIARY_INDEX are source roles. An out-of-scope code file remains `IMPLEMENTATION`, not `OUT_OF_SCOPE`; it is still non-eligible and SKIP for the six-domain textual lane.

## Balanced reading

K2 must not finish Qimen before the other domains begin. Source-lineage coverage is global: all 515 K1 canonical source IDs receive a disposition before Claim Extraction is unlocked.

After lineage closure, reading waves are selected per semantic domain. Thin corpora such as Liuyao/Liuren are processed completely before their scarcity is interpreted as evidence strength.

## Copyright boundary

Local books, scans, OCR and extracted page images remain outside Git. Public K2 files contain only derived metadata, short evidence descriptions and later normalized claims/evidence records. Modern long-form text is never copied into the repository.
