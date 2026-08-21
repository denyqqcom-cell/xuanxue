# K2 VISUAL_REQUIRED Page Handoff Protocol

Status: ACTIVE

Purpose: make SCAN / VISUAL_REQUIRED sources reviewable without weakening the rule that only genuine original-page visual inspection earns Reading Credit.

## 1. Separation of responsibilities

There are three distinct acts:

1. **Canonical resolution** — locate exact local bytes and verify official SHA256.
2. **Mechanical rendering** — turn each original PDF page into a local page image.
3. **Semantic visual review** — the main reviewer actually inspects every page and creates Reading/Evidence judgments.

Only step 3 is reading.

A renderer, OCR engine, text extractor, local helper or packet manifest can never mark a book COMPLETE by itself.

## 2. Local-only renderer

`tools/build_k2_visual_page_packet.py` is the governed mechanical renderer.

It must:

- read the official K2 plan;
- accept only a source routed as `VISUAL_REQUIRED`;
- resolve the source through private K1 metadata or explicit local search roots;
- verify exact canonical `file_sha256` before rendering;
- verify registered PDF page count;
- render every original page to PNG without OCR;
- keep all page images outside the repository;
- write a manifest without leaking the local source path;
- set `review_credit_granted=false`;
- use packet status `READY_FOR_VISUAL_REVIEW`, never `COMPLETE` or `READ`.

If canonical bytes, dependency health or page count cannot be verified, the helper fails closed.

## 3. Render packet is not Evidence

Rendered PNGs are transport/view artifacts only.

They are not:

- Atomic Evidence;
- Reading Ledger rows;
- Book Distillates;
- Claims;
- empirical validation;
- OCR substitutes.

No semantic statements may be generated solely from the manifest metadata.

## 4. Main-reviewer visual obligation

For a source to become `COMPLETE`, the main reviewer must inspect all registered pages, including pages that appear to be:

- cover/title/copyright pages;
- contents/index pages;
- diagrams, grids, plates and tables;
- handwritten annotations or marginalia when present;
- blank or near-blank pages;
- example charts whose meaning depends on spatial layout;
- final colophon/author/source pages.

A page may be judged semantically empty only after it was actually viewed.

## 5. Page accounting

Visual review must maintain exact coverage accounting:

- registered pages;
- pages rendered;
- pages visually reviewed;
- pages needing re-render at higher DPI;
- pages temporarily unreadable/obscured;
- pages accepted as blank/non-semantic after inspection.

`pages_reviewed_count` must equal registered page count before Reading status may become COMPLETE.

Packet readiness cannot be substituted for this count.

## 6. Resolution quality

Default renderer DPI is 144. Review may request a higher-DPI re-render for pages with:

- dense small print;
- faint scans;
- complex 奇门盘 grids;
- vertical traditional text;
- diagrams where line position matters.

Increasing DPI changes only the transport image. It does not alter canonical source identity because identity remains tied to original PDF SHA256.

## 7. No OCR substitution

OCR may be used only as a secondary navigation aid if separately authorized, and its output cannot replace the image review requirement.

For `VISUAL_REQUIRED`:

`OCR_SEEN != VISUAL_PAGE_REVIEWED`

Any conflict between OCR and visible page content is resolved in favor of the original page image, while recording the extraction discrepancy.

## 8. Evidence creation after visual inspection

Atomic Evidence may be created only after the relevant page(s) were visually inspected.

Evidence locators must remain page-based and within reviewed coverage. For modern copyrighted books, Evidence should normally paraphrase rather than reproduce extended text.

When a claim depends on a diagram/table/chart layout, Evidence should state that the basis is visual layout rather than pretending it came from a text layer.

## 9. Provenance correction

Title, author, edition and other metadata imported from filenames remain provisional until stronger page-internal evidence is visually verified.

When title/copyright/colophon pages provide stronger provenance, record it in the governed verified-metadata layer. Do not silently rewrite source identity from memory or external catalog guesses.

## 10. Copyright and repository boundary

Original PDFs and rendered page PNGs are local research artifacts and must not be committed under `knowledge/`, `奇门/`, or other repository paths.

The repository may contain only:

- source hashes and metadata;
- reading/evidence/distillate records;
- local helper code;
- non-infringing analytical notes and paraphrases.

The CI binary guard remains authoritative for the knowledge tree.

## 11. QM-SRC-0001 immediate use

For `QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》`:

- registered pages: 57;
- lane: `VISUAL_REQUIRED`;
- canonical SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`;
- Pre-Book Retrospective: already required before reading;
- packet status may become `READY_FOR_VISUAL_REVIEW` only after the exact canonical file is resolved and all 57 pages render;
- Reading remains NOT COMPLETE until the main reviewer visually inspects p1-p57.

## 12. Closure chain

For VISUAL_REQUIRED books:

`canonical bytes`
→ `Pre-Book Retrospective`
→ `local original-page render packet`
→ `main-reviewer full visual reading`
→ `Atomic Evidence`
→ `Book Distillate`
→ `Conflict / Anti-pattern Review`
→ `Method Delta`
→ `Prospective Test Plan`
→ `aggregate validators/tests`
→ `CI`
→ `CLOSED`

The visual handoff removes an access bottleneck. It does not lower the epistemic bar.
