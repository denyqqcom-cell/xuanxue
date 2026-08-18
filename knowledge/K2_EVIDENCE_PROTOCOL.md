# K2B Evidence Extraction Protocol

K2B is the first stage that actually reads the local books. It still does **not** create or reconcile Claims.

## 0. Execution ownership

The project-side main agent owns K2B engineering and knowledge normalization:

- repository code/schema/validator changes;
- final Reading Ledger construction;
- final atomic Evidence normalization;
- Git commits/pushes and project-state transitions;
- project review and acceptance.

The local AI is a **helper only**. It may:

- fetch/pull the requested branch;
- run project-owned scripts/tests without modifying them;
- locate private local sources;
- mechanically expose page text packets or page metadata from local files;
- report logs, missing files, extractor failures, or vision failures.

The local AI must not design schemas, repair validators, normalize Evidence, modify tracked repository files, commit, push, or decide project acceptance.

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

## 3. Canonical source identity is byte identity

K2B reading credit must attach to the exact K1 canonical source bytes.

The authoritative identity test is:

`official K1 file_sha256 == actual local file SHA256`

A private K1 registry containing `local_path` is only an optional resolution aid. When that registry is unavailable on another machine, project-owned tooling may search explicitly supplied local corpus roots and resolve a source by canonical SHA256.

Filename similarity, title similarity, directory placement, page count, or visual resemblance cannot substitute for SHA256 identity.

A source that cannot be resolved to canonical bytes is `FILE_MISSING`; no reading credit is granted.

## 4. Reading coverage is a first-class artifact

Evidence count does not prove a book was read.

Every selected unique-coverage carrier receives a reading-ledger row. For paged documents, COMPLETE requires page-range coverage of the whole carrier. If pages are unreadable, mark BLOCKED rather than pretending completion.

For multi-volume works, all selected WORK_PART carriers are tracked separately while sharing the same `work_id`.

## 5. Execution lanes

Wave planning assigns each selected source an execution lane from K1 readability:

- `TEXT_DIRECT`: `TEXT_OK`; existing text layer may be mechanically extracted page-by-page and then reviewed by the project-side main agent.
- `VISUAL_REQUIRED`: `SCAN`, `OCR_WEAK`, or `OCR_FAIL`; OCR/text alone is not admissible. COMPLETE requires original-page visual verification.
- `ACCESS_REVIEW`: any other readability state; must be explicitly resolved before COMPLETE.

The lane is descriptive and fail-closed. It must never be weakened just to increase completion counts.

A `VISUAL_REQUIRED` source may be recorded as BLOCKED with:

- `verification_mode=NONE`
- `blocker_code=VISION_UNAVAILABLE`

when the local vision backend cannot inspect the original pages. Such a source remains a valid Wave1 obligation and is not treated as read.

## 6. Local page packets

`tools/build_k2_local_page_packets.py` is a mechanical local-only helper.

It resolves source bytes in this order:

1. optional `PRIVATE_REGISTRY` fast path from a private K1 intake registry;
2. `CANONICAL_SHA256_SEARCH` under explicit user-supplied corpus roots.

The second path is the supported portable fallback for Windows/WSL/Linux when the original private intake path is absent. It accepts a file only when the actual bytes hash to the official canonical `file_sha256` in the Wave1 plan.

For `TEXT_DIRECT` sources the helper:

- extracts existing PDF text layers with `pdftotext -layout`;
- preserves page boundaries;
- records canonical source SHA256, per-page text SHA256, character counts, and full packet SHA256;
- writes raw page packets only outside the repository.

For `VISUAL_REQUIRED` sources the helper verifies canonical bytes but does not OCR-substitute visual review; if vision is unavailable it records `VISION_UNAVAILABLE`.

It **does not** create Evidence, Claims, Git-tracked knowledge files, or project acceptance state.

Raw page packets can contain copyrighted source text and therefore remain local/private.

## 7. Wave 1 selection

Wave 1 is balanced across all six governed arts.

Selection rules:

1. Select every P0 unique-coverage textual row.
2. Expand each selected `work_id` to include every PRIMARY_WORK / WORK_PART member needed for complete unique coverage, even if some parts are P1/P2.
3. For Liuyao and Liuren, include all governed unique textual coverage in Wave 1 because their corpora are thin.
4. Do not finish one rich domain before the other five begin.
5. Variants are backup carriers, not new reading obligations when their target carrier is readable.

## 8. Reading Ledger execution fields

Every public Wave1 reading row includes:

- `execution_lane`: `TEXT_DIRECT | VISUAL_REQUIRED | ACCESS_REVIEW`
- `verification_mode`: `TEXT_LAYER_FULL | VISUAL_PAGE | WHOLE_TEXT_DOCUMENT | NONE`
- `blocker_code`: canonical machine-readable blocker or null
- `blocker_reason`: short human-readable explanation or null

Rules:

- `TEXT_DIRECT + COMPLETE` requires full text/page coverage and `TEXT_LAYER_FULL`, `VISUAL_PAGE`, or `WHOLE_TEXT_DOCUMENT` verification.
- `VISUAL_REQUIRED + COMPLETE` requires `VISUAL_PAGE` verification.
- `BLOCKED` requires `verification_mode=NONE`, a canonical blocker code, and zero Evidence.
- A blocked source may not emit Evidence.

## 9. Atomic evidence fields

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

## 10. Source location

Use stable locators such as:

- `pdf:p12`
- `pdf:p12-p13`
- `printed:p35|pdf:p41`
- `chapter:卷二/节三|pdf:p88`

Do not write local filesystem paths.

If a fact depends on a table or diagram spanning pages, cite the smallest page range that fully supports the normalized fact.

## 11. Evidence types

- EXPLICIT_RULE
- WORKED_EXAMPLE
- TABLE
- DIAGRAM
- COMMENTARY
- HISTORICAL_CLAIM
- CASE_RECORD
- META_METHOD

## 12. Scope

Use one of:

STRUCTURE / ALGORITHM / SYMBOLISM / SELECTION / INTERPRETATION / TIMING / CASE / HISTORY / META_METHOD.

This scope is descriptive. It does not promote the evidence to a Claim.

## 13. Normalization rules

`normalized_fact` must:

- preserve the source's actual meaning;
- be one atomic proposition or procedure step;
- preserve important conditions and exceptions;
- identify school-specific context when the source itself provides it;
- avoid stronger certainty than the source uses;
- avoid modern scientific endorsement language unless the source itself is being recorded as a historical/meta claim.

Suspected printing/OCR mistakes are not silently corrected. Record the visible/source-supported fact and add a short note such as `suspected source/OCR issue; requires cross-check`.

## 14. Claim readiness

- READY
- CONTEXT_REQUIRED
- CONFLICT_CANDIDATE
- NOT_CLAIM

READY means only that K2C may later consider the atomic evidence. It is not a validated rule.

## 15. Unknown semantic sources

K2A intentionally left 96 textual rows as semantic UNKNOWN.

They are not discarded. K2B maintains a discovery backlog. Content may be opened to determine what system the work actually concerns. Until content-based routing is established, no six-domain Evidence record may be created from it.

## 16. Copyright boundary

Original books, scans, screenshots, OCR text, local page packets and long quotations stay local.

Public Git may contain only source/work identifiers, page/section locators, independently written atomic paraphrases, short metadata, and derived reading coverage.

Default `verbatim_quote` is null.

## 17. Wave acceptance

Project review requires:

- every selected reading unit has a ledger row;
- COMPLETE coverage matches page counts where known;
- blocked visual sources are reported honestly and emit no Evidence;
- every Evidence row points to an eligible COMPLETE source/work and reviewed location;
- `VISUAL_REQUIRED` evidence is visually verified rather than OCR-derived;
- no Evidence comes from NOTE/CODE/AUX as traditional doctrine;
- no variant creates an extra corroboration vote;
- all six domains have begun;
- thin Liuyao/Liuren coverage is not starved;
- no Claim files are created during K2B.
