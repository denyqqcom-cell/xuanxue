# ☿ Local execution prompt — QM-SRC-0001 18局 table-body / implementation packet

execution_mode: EXECUTION_HELPER_ONLY
review_mode: MAIN_AGENT_OWNS_ACCEPTANCE
target_branch: k2-qm0001-liang-retrospective

You are the local execution helper. Do not redesign schemas, do not modify tracked repository files, do not commit/push, and do not grant Reading/Evidence/Distillate/Claim credit.

## A. Sync and provenance

1. `git fetch` the repository.
2. Switch to `k2-qm0001-liang-retrospective` and fast-forward to the latest remote branch head.
3. Report the exact resulting `HEAD` SHA.
4. Verify tracked worktree state. Do not delete unrelated untracked files.
5. Locate the local canonical PDF:
   - source_id: `QM-SRC-0001`
   - title: `梁湘潤《奇門遁甲入門》`
   - expected SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
   - expected PDF pages: `57`
6. If SHA256 or page count mismatches, STOP with `CANONICAL_MISMATCH`.

## B. Corrected spread topology

The earlier p32-p49 title-based index was wrong.

This PDF contains two-page/spread scans. A bureau title visible on the right side of one PDF raster does **not** automatically label the large table body visible on the left side of that same raster.

Also, PDF p35/p36 are out of printed physical-page order.

Authoritative table-body mapping for this task:

- YANG-01 p31
- YANG-02 p32
- YANG-03 p33
- YANG-04 p34
- YANG-05 p36
- YANG-06 p35
- YANG-07 p37
- YANG-08 p38
- YANG-09 p39
- YIN-09 p40
- YIN-08 p41
- YIN-07 p42
- YIN-06 p43
- YIN-05 p44
- YIN-04 p45
- YIN-03 p46
- YIN-02 p47
- YIN-01 p48

PDF p49 is the `十二日圖式` body. Do not report a Yin-1 missing-table anomaly.

Table identity must be checked from the table-internal 甲子 palace/star/door relation plus polarity/printed-page progression, not same-raster title proximity alone.

## C. Render-only local packet

If re-rendering is needed, render only PDF p31-p48 at 300 DPI or higher into a repository-external temporary directory.

Do not put PNG/JPG/PDF artifacts under the Git repository.

No full-table transcription is requested.

## D. Implementation comparison assistance

After syncing the latest branch, inspect the project-owned Qimen implementation and tests.

You may locally run existing tests and produce an **uncommitted diagnostic report** comparing the implementation against the tracked `LIANG_18_BUREAU` sparse anchors.

Required controls:

1. positive: correct bureau-specific Jiazi star/door pairs;
2. wrong-bureau: shift each bureau to an adjacent bureau and verify the comparison detects mismatch;
3. shifted-page: use the superseded old mapping (Yang1=p32 ... Yin1=p49) and verify it fails;
4. permuted-anchor: permute star/door pairs between bureaus and verify mismatch;
5. report bureau 5 separately if the implementation uses an empty center-gate value.

Do not modify implementation code. Do not upgrade any fixture to `IMPLEMENTATION_CHECKED`.

## E. Hard prohibitions

- no tracked file edits;
- no `git add`, commit, push, PR, merge;
- no full-table transcription into Git;
- no claim that code or tables predict reality;
- no Reading Credit;
- no silent correction of suspected source typos;
- no using right-side spread title as sole table identity;
- no changing Prospective Registry or granting empirical support.

## F. Return format

Return only:

1. `HEAD`
2. `CANONICAL_SHA256`
3. `PDF_PAGES`
4. `TEST_COMMANDS_RUN=<...>`
5. `POSITIVE_MATCH=<count>/<18>`
6. `NEGATIVE_CONTROLS=<PASS|FAIL|BLOCKED>`
7. `BUREAU5_NOTE=<...>`
8. `OUTPUT_DIR=<path>`
9. concise blocker list

Main agent owns any implementation change, fixture status upgrade, and Git publication.
