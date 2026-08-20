# ☿ Local execution prompt — QM-SRC-0001 18局 sparse-anchor candidate packet

execution_mode: EXECUTION_HELPER_ONLY
review_mode: MAIN_AGENT_OWNS_ACCEPTANCE
target_branch: k2-qm0001-liang-retrospective

You are the local execution helper. Do not redesign schemas, do not modify tracked repository files, do not commit/push, and do not grant Reading/Evidence/Distillate/Claim credit.

## A. Sync and provenance

1. `git fetch` the repository and fast-forward/switch to the latest `k2-qm0001-liang-retrospective`.
2. Report exact `HEAD`.
3. Verify tracked worktree state. Do not delete unrelated untracked files.
4. Locate the local canonical PDF for:
   - source_id: `QM-SRC-0001`
   - title: `梁湘潤《奇門遁甲入門》`
   - expected SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
   - expected PDF pages: `57`
5. If SHA256 or page count mismatches, STOP with `CANONICAL_MISMATCH`.

## B. Render-only visual packet

Use project-owned tooling where possible. Render only PDF p32-p49 at 300 DPI or higher into a repository-external temporary directory.

Expected table-title/page mapping:

- p32 陽遁一局圖
- p33 陽遁二局圖
- p34 陽遁三局圖
- p35 陽遁四局圖
- p36 陽遁五局圖
- p37 陽遁六局圖
- p38 陽遁七局圖
- p39 陽遁八局圖
- p40 陽遁九局圖
- p41 陰遁九局圖
- p42 陰遁八局圖
- p43 陰遁七局圖
- p44 陰遁六局圖
- p45 陰遁五局圖
- p46 陰遁四局圖
- p47 陰遁三局圖
- p48 陰遁二局圖
- p49 陰遁一局圖

For each page, produce two local crops if feasible:
- `TABLE`: the large 值符/值使 table area.
- `TITLE`: the smaller bureau-title / seasonal mapping area.

Do not put PNG/JPG/PDF artifacts under the Git repository.

## C. Candidate sparse-anchor transcription

This is navigation/transcription assistance only.

For each of the 18 bureau tables:

1. Confirm the visible bureau title.
2. Select at most **four** candidate anchors, prioritizing:
   - clearly legible cells;
   - different parts of the table (top/middle/bottom where possible);
   - cells useful for implementation regression;
   - no attempt to reproduce the full table.
3. For each candidate anchor report:
   - `fixture_id` (`K2F-QM-0001-YANG-01` etc.);
   - `pdf_page`;
   - human-readable row/column locator;
   - exact candidate text as visually read;
   - confidence: HIGH / MEDIUM / LOW;
   - crop filename;
   - any ambiguity or alternative reading.
4. If OCR is used, mark it `NAVIGATION_ONLY`. OCR output does not override visible page content and does not count as review.
5. Do not normalize these candidates into project Evidence or fixture truth.

## D. Local output only

Write a repository-external local report named:

`QM-SRC-0001_BUREAU_ANCHOR_CANDIDATES.jsonl`

and a short summary text file with:

- HEAD
- canonical SHA256
- PDF page count
- rendered pages count
- crop count
- candidate anchors count
- LOW-confidence / unreadable cells
- exact local output directory

The JSONL may contain local paths because it must remain outside Git.

## E. Hard prohibitions

- no tracked file edits;
- no `git add`, commit, push, PR, merge;
- no full-table transcription into Git;
- no claim that code or tables predict reality;
- no Reading Credit;
- no silent correction of suspected source typos;
- no replacing 勾陳/朱雀 or other source terminology with modern equivalents.

## F. Return format

Return only:

1. `HEAD`
2. `CANONICAL_SHA256`
3. `PDF_PAGES`
4. `RENDER_STATUS`
5. `CANDIDATE_ANCHORS=<count>`
6. `LOW_CONFIDENCE=<count>`
7. `OUTPUT_DIR=<path>`
8. concise blocker list, if any

Do not summarize doctrine or make method decisions. Main agent will visually recheck and decide which sparse anchors, if any, enter the repository.
