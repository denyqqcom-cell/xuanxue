# K2A Source Lineage — Final Project Acceptance

## Decision

`PASS`

Accepted lineage data head: `d942b28c01b862a404784cefdb5a8e64fc5fcb86`.

Accepted CI run: `32043681020` (`Knowledge Engine V1 CI`) — SUCCESS. The same PR merge ref passed K1 sanitization/source-quality/semantic-routing, K2 source-lineage tests, K2 lineage state enforcement, research-binary guard, and `:ziwei-core:test`.

## Accepted inventory

- 515 canonical source rows
- 371 distinct non-null work IDs
- 58 PRIMARY_WORK
- 39 WORK_PART
- 19 SAME_WORK_VARIANT
- 6 COMMENTARY_DERIVATIVE
- 159 SECONDARY_NOTE
- 65 IMPLEMENTATION
- 67 AUXILIARY_INDEX
- 6 OUT_OF_SCOPE textual rows
- 96 UNKNOWN textual rows

The upgraded validator reports:

```text
k2-source-lineage: REVIEW_REQUIRED
sources=515 lineage_rows=515 issues=0; promote state only after project review
```

The project review therefore promotes `K2_SOURCE_LINEAGE_STATE.status` to `COMPLETE`.

## Family-level checks performed by project review

- 《紫微斗数全集》一至六卷 are preserved as six eligible WORK_PART carriers under one work family; no volume is discarded as a duplicate.
- The 八字真诀启示录 family separates 火/电/雷/风 as unique WORK_PART coverage and points redundant page-split carriers at their corresponding part.
- ChengGu remains IMPLEMENTATION / IMPLEMENTATION_ONLY / SKIP while K1 semantic routing may remain OUT_OF_SCOPE; source role and semantic domain are orthogonal.
- 六爻 thin corpus preserves three direct registry books plus the cross-routed 火珠林 source as independent textual candidates; implementation rows remain SKIP.
- 大六壬 keeps the two《大六壬探原》carriers in one work family, with one primary carrier and one same-work variant; commentary dependency remains explicit.

## Evidence-counting rule carried forward

K2B/K2C may not count files as independent votes. Independence starts from `work_id`, then is refined at claim level for commentary, author/source dependence, shared quotations and school lineage.

WORK_PART contributes unique coverage but never creates an additional independent corroboration vote. SAME_WORK_VARIANT is a redundant/alternate carrier and cannot independently corroborate a claim.

## Remaining non-blocking uncertainty

96 K1 semantic-UNKNOWN textual sources remain intentionally unresolved. K2B must not silently ignore them. They enter a separate discovery-reading backlog: content may be inspected to resolve domain/role, but no domain claim may be extracted from an unresolved source until routing is established from the content itself.

K2A is closed. K2B Evidence Extraction is now open. Claim Extraction remains blocked.
