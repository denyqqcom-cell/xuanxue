# QM-SRC-0001 Evidence Locator Correction — bureau table bodies

Status: ACTIVE CORRECTION OVERLAY  
Date: 2026-08-21  
Scope: source-location semantics only; does not grant Claim or Empirical Support.

## 1. Why this overlay exists

The first `LIANG_18_BUREAU` fixture pass treated each PDF raster as if it contained one semantic page and associated a bureau title visible on the right side of a spread with the large table body on the left.

That created a one-bureau shift and a false `YIN-01 / p49 table missing` interpretation.

Main-reviewer reinspection of the canonical scan, using printed-page topology plus table-internal `甲子` structure, corrected the table-body locations.

## 2. Corrected table-body ranges

For broad K2 Evidence references:

- `K2E-W1-QM-0001-0022` 阳遁九局查表体系:
  - old coarse locator: `pdf:p30-p40`
  - corrected table-body span: `pdf:p31-p39`
  - caveat: Yang5 is p36 and Yang6 is p35 because those PDF scans are out of printed-page order.

- `K2E-W1-QM-0001-0023` 阴遁九局查表体系:
  - old locator: `pdf:p41-p49`
  - corrected table-body span: `pdf:p40-p48`.

- `K2E-W1-QM-0001-0024` 十二日图式:
  - remains `pdf:p49-p50`; p49 body belongs here, not to a missing Yin1 table.

## 3. Exact fixture map

- Yang1 p31
- Yang2 p32
- Yang3 p33
- Yang4 p34
- Yang5 p36
- Yang6 p35
- Yang7 p37
- Yang8 p38
- Yang9 p39
- Yin9 p40
- Yin8 p41
- Yin7 p42
- Yin6 p43
- Yin5 p44
- Yin4 p45
- Yin3 p46
- Yin2 p47
- Yin1 p48

## 4. Epistemic effect

The substantive source claim remains narrow:

the book contains mechanically structured Yang/Yin bureau lookup tables.

What changed is **where the table bodies were semantically located**.

This correction therefore changes Source Fidelity metadata and the fixture reference map. It does not increase predictive validity.

Until the underlying Atomic Evidence JSONL locators are normalized in a later maintenance pass, this overlay supersedes the two old coarse table-body locators for implementation work.

## 5. Error class

`MAIN_REVIEWER_SEMANTIC_ASSOCIATION_ERROR`

Not:

- `SOURCE_INCONSISTENCY`
- `SOURCE_TABLE_MISSING`
- `EMPIRICAL_FAILURE`

The Git history is intentionally preserved so the project can audit how the false anomaly arose.
