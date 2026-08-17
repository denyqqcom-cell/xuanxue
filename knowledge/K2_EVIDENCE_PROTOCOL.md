# K2B Evidence Extraction Protocol

K2B is the first stage that actually reads the local books. It still does **not** create or reconcile Claims.

## 1. Evidence is not a Claim

An Evidence record is a faithful, atomic paraphrase of what one identifiable source location explicitly states, demonstrates, tabulates, diagrams, or records as a case.

K2B must not:

- combine several pages into a new doctrine;
- decide which school is correct;
- silently repair a suspected typo;
- infer a rule that the source did not state;
- count another edition/scan as an independent confirmation;
- convert current project code into evidence of traditional doctrine.

If two books disagree, create separate evidence records. Conflict mapping happens later.

## 2. Reading unit follows coverage, not file count

The governed textual reading lane consists of unique-coverage carriers:

- PRIMARY_WORK
- WORK_PART
- COMMENTARY_DERIVATIVE

WORK_PART is not an independent corroboration vote, but it must be read because it contains complementary coverage.

SAME_WORK_VARIANT is normally a backup carrier. It may be consulted if the primary/part carrier is unreadable, but the resulting evidence still belongs to the same `work_id` and cannot create another independent vote.

SECONDARY_NOTE / IMPLEMENTATION / AUXILIARY_INDEX do not enter the traditional textual evidence lane.

## 3. Reading coverage is a first-class artifact

Evidence count does not prove a book was read.

Every selected unique-coverage carrier receives a reading-ledger row. For paged documents, COMPLETE requires page-range coverage of the whole carrier. If pages are unreadable, mark BLOCKED or PARTIAL rather than pretending completion.

For multi-volume works, all selected WORK_PART carriers are tracked separately while sharing the same `work_id`.

## 4. Wave 1 selection

Wave 1 is balanced across all six governed arts.

Selection rules:

1. Select every P0 unique-coverage textual row.
2. Expand each selected `work_id` to include every PRIMARY_WORK / WORK_PART member needed for complete unique coverage, even if some parts are P1/P2.
3. For Liuyao and Liuren, include all governed unique textual coverage in Wave 1 because their corpora are thin.
4. Do not finish one rich domain before the other five begin.
5. Variants are backup carriers, not new reading obligations when their target carrier is readable.

## 5. Atomic evidence fields

Every public evidence row records:

- `evidence_id`
- governed `domain`
- exact `source_id`
- `work_id`
- page/section locator in `source_location`
- `evidence_type`
- `scope`
- optional short `topic`
- `normalized_fact`
- `extraction_basis`
- `claim_readiness`
- `school_ids`
- `review_status`
- `copyright_class`

Public evidence should normally use `verbatim_quote=null`. Modern-book wording must not be copied into Git merely to prove extraction.

## 6. Source location

Use stable locators such as:

- `pdf:p12`
- `pdf:p12-p13`
- `printed:p35|pdf:p41`
- `chapter:卷二/节三|pdf:p88`

Do not write local filesystem paths.

If a claim depends on a table or diagram spanning pages, cite the smallest page range that fully supports the normalized fact.

## 7. Evidence types

- EXPLICIT_RULE: source explicitly states a rule or procedure.
- WORKED_EXAMPLE: source applies a method step by step.
- TABLE: structured table content normalized without copying the full table.
- DIAGRAM: information explicitly conveyed by a diagram.
- COMMENTARY: an author/commentator's interpretation of another work or doctrine.
- HISTORICAL_CLAIM: historical/origin/attribution statement; not treated as technical truth.
- CASE_RECORD: reported case, observation or divination record.
- META_METHOD: statements about methodology, limits, ethics or how to reason from a chart.

## 8. Scope

Use one of:

STRUCTURE / ALGORITHM / SYMBOLISM / SELECTION / INTERPRETATION / TIMING / CASE / HISTORY / META_METHOD.

This scope is descriptive. It does not promote the evidence to a Claim.

## 9. Normalization rules

`normalized_fact` must:

- preserve the source's actual meaning;
- be one atomic proposition or procedure step;
- preserve important conditions and exceptions;
- identify school-specific context when the source itself provides it;
- avoid stronger certainty than the source uses;
- avoid modern scientific endorsement language unless the source itself is being recorded as a historical/meta claim.

Suspected printing/OCR mistakes are not silently corrected. Record the visible/source-supported fact and add a short note such as `suspected source/OCR issue; requires cross-check`.

## 10. Claim readiness

- READY: atomic explicit evidence suitable for later Claim synthesis.
- CONTEXT_REQUIRED: cannot be interpreted safely without nearby context, definitions or prerequisites.
- CONFLICT_CANDIDATE: visibly disagrees with another already observed evidence item or a known legacy rule; do not resolve yet.
- NOT_CLAIM: useful case/history/meta information but not a normative rule.

## 11. Unknown semantic sources

K2A intentionally left 96 textual rows as semantic UNKNOWN.

They are not discarded. K2B maintains a discovery backlog. Content may be opened to determine what system the work actually concerns. Until that content-based routing is established, no six-domain Evidence record may be created from it.

K2B cannot be declared globally complete while these 96 sources remain completely unreviewed. They must eventually be resolved to a governed domain, OUT_OF_SCOPE, or a justified still-UNKNOWN state after content review.

## 12. Copyright boundary

Original books, scans, screenshots, OCR text and long quotations stay local.

Public Git may contain:

- source/work identifiers;
- page/section locators;
- independently written atomic paraphrases;
- short metadata;
- derived reading coverage.

Default `verbatim_quote` is null.

## 13. Wave acceptance

A local wave is not accepted merely because extraction scripts run.

Project review requires:

- every selected reading unit has a ledger row;
- COMPLETE coverage is consistent with page counts where known;
- every evidence row points to an eligible source/work and a reviewed location;
- no evidence comes from NOTE/CODE/AUX as traditional doctrine;
- no variant creates an extra corroboration vote;
- all six domains have begun;
- thin Liuyao/Liuren coverage is not starved;
- no Claim files are created during K2B.
