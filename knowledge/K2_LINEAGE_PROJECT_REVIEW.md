# K2 Source Lineage — Project Review

## Review status

`REVIEW_REQUIRED`

Claim Extraction remains blocked.

## What passed

The 515-row local lineage draft correctly preserved one row per K1 canonical source and already separated many important classes: textual work, commentary derivative, secondary note, implementation, auxiliary index, out-of-scope and unknown. The local review also exposed only one issue under the first K2 validator: `ZW-SRC-0087 ChengGu`.

That ChengGu issue is a validator design bug, not a reason to rewrite K1 semantic routing. K1 correctly says the code is semantically outside the six governed arts, while its evidence role is still `IMPLEMENTATION_EVIDENCE`. K2 must preserve both facts: relation `IMPLEMENTATION`, `IMPLEMENTATION_ONLY`, non-eligible, SKIP.

## New project-side blocker: coverage was conflated with variant identity

The first K2 lineage model used `SAME_WORK_VARIANT` both for alternate carriers of the same content and for complementary volumes/page splits of one work. Those are not the same thing.

Concrete confirmed example:

- `ZW-SRC-0003` = 紫微斗数全集（一）
- `ZW-SRC-0004` = 紫微斗数全集（三）
- `ZW-SRC-0005` = 紫微斗数全集（二）
- `ZW-SRC-0006` = 紫微斗数全集（五）
- `ZW-SRC-0007` = 紫微斗数全集（六）
- `ZW-SRC-0008` = 紫微斗数全集（四）

The initial lineage put all six under `WORK-000003`, made the first source `PRIMARY_WORK`, and labelled the other five `SAME_WORK_VARIANT`. These six files are complementary volumes, not alternate scans of identical coverage. If K2B later reads only one representative carrier, five volumes of unique material could be silently lost.

The same risk exists in reported large families containing 上/中/下册、卷、篇、分册、分页、全集分卷 or a full-work file mixed with split parts.

## Corrected model

K2 lineage now distinguishes:

- `PRIMARY_WORK`: complete-work carrier;
- `WORK_PART`: complementary volume/part/page segment of the same underlying work; not an independent vote, but still K2-eligible because it contains unique coverage;
- `SAME_WORK_VARIANT`: alternate carrier of substantially the same coverage, which must point via `variant_of_source_id` to a PRIMARY_WORK or WORK_PART;
- `part_label`: required for WORK_PART and inherited by variants of that part.

A titled series of genuinely separate works must not be collapsed into one `work_id` just because the series prefix matches. Conversely, different volumes of one actual work must not be split into fake independent works simply to increase source count.

## Required remediation scope

Re-review all current `SAME_WORK_VARIANT` rows and every member of those work families. The starting draft contains 97 `SAME_WORK_VARIANT` rows. Each must be resolved as one of:

1. true SAME_WORK_VARIANT with a direct `variant_of_source_id`;
2. WORK_PART with a `part_label`;
3. distinct PRIMARY_WORK with a new work_id when it is actually a separate intellectual work in a series;
4. UNKNOWN if evidence is insufficient.

The re-review must especially cover the previously reported large families such as 紫微斗数全集、命理探原/探源、八字真诀启示录、命谱、斗数四书、中州派玄空资料、甲遁真授秘录、图解奇门遁甲大全、奇门遁甲应用学、烟波钓叟歌、曾子南三元奇门讲义 and any page-split/full-text families.

## Gate

Do not promote `knowledge/K2_SOURCE_LINEAGE_STATE.json.status` locally.

Project acceptance requires:

- 515 lineage rows exactly;
- all structural validators pass;
- no unresolved `variant_of_source_id` relationships;
- all WORK_PART rows have unique meaningful `part_label` within their work family;
- no volume/part is discarded as a mere alternate carrier;
- no series is collapsed into one work solely by normalized title;
- project-side independent review passes;
- `claim_extraction_blocked=true` until this review is closed.

The current public lineage remains a draft. Its previous one-issue result must not be interpreted as K2A acceptance because the old validator did not model part coverage.
