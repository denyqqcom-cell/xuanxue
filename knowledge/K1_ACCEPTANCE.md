# K1 Source Registry — project-side acceptance

Acceptance update: 2026-08-17

## Verdict

`K1_LOCAL_INDEX = PASS`

`K1_SANITIZED_IMPORT_STRUCTURE = PASS`

`K1_ATTRIBUTION_QUALITY = PASS`

`K1_SEMANTIC_ROUTING = REVIEW_REQUIRED`

`K1_PROJECT_IMPORT = NOT_YET_CLOSED`

`K2_CLAIM_EXTRACTION = BLOCKED`

The attribution remediation commit `c3e92e3e85cb0919d30d2274c3e90ad014a48f33` successfully reduced the previous source-quality findings from 2586 to zero under `validate_k1_source_quality.py --force`. GitHub Actions run `32028311905` passed source-quality, sanitization, binary-boundary and stable-core checks.

However, project-side sampling found a second semantic layer that the previous contract did not test: **the registry bucket is still being treated as if it were the work's actual knowledge domain, and filename-associated contributor names can still be collapsed into authorship**.

## Confirmed examples

- `BZ-SRC-0114` / `BZ-SRC-0115` are titled `梁湘润-梅花心易实战详解...` but remain under the bazi registry.
- `BZ-SRC-0122` is `梁湘润-火珠林密本（古本）` but remains under the bazi registry. Physical location under an 八字/梁湘润 collection is not evidence that the work should feed bazi Claim Extraction.
- `FS-SRC-0011` is `周易變占法引論[談延祚]` and `FS-SRC-0012` is `揭露铁板神数之内幕`, yet both remain routed as fengshui sources.
- `LR-SRC-0001` / `LR-SRC-0002` titles explicitly distinguish `袁树珊撰`, `谢路军主编`, `邓同校`, while the current `author` field still joins all three names. Editor/proofreader roles are not authorship.

These are not cosmetic bibliography problems. If K2 routes source reading by registry folder/domain, a bazi extraction pass could ingest 梅花/火珠林, and a fengshui pass could ingest 铁板神数. That would create false cross-verification later.

## New semantic-routing contract

`knowledge/schema/source.schema.json` now defines optional routing provenance fields for the remediation pass:

- `knowledge_domains`
- `domain_basis`
- `domain_evidence`

The existing `domain` remains the stable registry bucket used by current IDs. It must no longer be treated as proof of semantic scope. K2 must ultimately route by `knowledge_domains`.

Allowed semantic scopes include the six official domains, `common`, `OUT_OF_SCOPE`, and `UNKNOWN`. `UNKNOWN` and `OUT_OF_SCOPE` must not be mixed with resolved in-scope domains.

## New fail-closed gate

`tools/validate_k1_semantic_routing.py` checks:

- every source has an explicit semantic routing decision;
- routing has provenance;
- strong title clues are not contradicted by folder-based routing;
- obvious out-of-scope systems are not silently promoted into one of the six domains;
- project code routing is explicit;
- filename contributors explicitly labeled `主编/校/译/整理` are not collapsed into `author`.

`tools/test_k1_semantic_routing.py` includes negative fixtures for `火珠林` misrouted to bazi, `铁板神数` misrouted to fengshui, missing semantic routing, and editor/proofreader names incorrectly included as authors.

`tools/validate_sanitized_k1.py` also now verifies that each registry's actual SHA256 matches `K1_SANITIZED_IMPORT.json`, closing a previous manifest-drift gap.

## Promotion rule

K1 project import closes only when all of the following hold on one exact head:

1. 515 canonical records remain reconciled with the accepted local index;
2. sanitized counts, source hashes, privacy boundary and manifest registry hashes pass;
3. source attribution quality remains zero-issue;
4. semantic routing is explicit for all 515 sources and `validate_k1_semantic_routing.py --force` reports zero issues;
5. out-of-scope/mixed-domain works are not routed by their physical folder;
6. editor/compiler/proofreader names are not mislabeled as authors;
7. no original books, scans, OCR bodies or private paths enter Git;
8. stable-core regression and Knowledge Engine CI pass.

Until then, `k2_blocked=true` remains mandatory.
