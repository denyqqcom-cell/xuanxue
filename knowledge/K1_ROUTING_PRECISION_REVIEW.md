# K1 Semantic Routing Precision Review

Project-side final recheck after local commit `78c56e3174c2595294aa3451544f49ec010c53e8`.

## Accepted evidence

The local remediation successfully closed the previously known routing and contributor-role defects:

- `BZ-SRC-0114/0115` are now `OUT_OF_SCOPE` instead of bazi.
- `BZ-SRC-0122` is routed to `liuyao` while retaining its stable BZ source identity.
- `FS-SRC-0011/0012` are no longer treated as fengshui knowledge.
- `LR-SRC-0001/0002` retain 袁树珊 as author while editor/proofreader names are no longer collapsed into authorship.
- GitHub Actions run `32030193888` on the user remediation head passed sanitized import, source quality, semantic routing, research-binary boundary and stable-core regression under the then-current validator.

## Precision defect found by project-side recheck

The previous semantic validator searched the entire canonical filename for domain keywords. This can create false positives when an **author name itself contains a domain word**.

Example: `紫微杨+《清室气数录》b` was routed to `ziwei` because the author name `紫微杨` contains `紫微`, even though the work-title remainder does not establish a ziwei domain.

The validator has therefore been hardened to remove verified author tokens before evaluating `TITLE_FILENAME` domain hints, while still recognizing legacy mixed Chinese-pinyin filenames and explicit English code identifiers.

## Remaining high-risk records

After correcting validator false positives for mixed filenames, English code names and additional out-of-scope labels, **7 records remain**:

- `ZW-SRC-0027` — `紫微扬-术数述异b`
- `ZW-SRC-0028` — `紫微杨+《清室气数录》b`
- `ZW-SRC-0034` — `紫微杨+《蕉窗传灯录》b`
- `ZW-SRC-0036` — `紫微杨-燃犀日知录b`
- `ZW-SRC-0037` — `紫微杨传灯录b`
- `ZW-SRC-0038` — `紫微杨：天网搜索录b`
- `ZW-SRC-0087` — `ChengGu`

For the first six, `TITLE_FILENAME -> ziwei` is not justified after removing the verified author token. They require actual title-page/TOC/content evidence or must be conservatively reset to `UNKNOWN`.

For `ZW-SRC-0087`, `TITLE_FILENAME -> bazi` is not justified by the identifier `ChengGu`; inspect the actual project code path/content and use `PROJECT_CODE_PATH` or `CONTENT_VERIFIED` only if the code truly belongs to the governed bazi domain. Otherwise use `UNKNOWN` or `OUT_OF_SCOPE` as supported by evidence.

## Gate

K2 remains blocked. K1 semantic routing closes only when the latest validator reports:

```text
k1-semantic-routing: PASS
sources=515 issues=0
```

The remediation must preserve all 515 source IDs and file SHA256 identities and must regenerate the sanitized registries through the official sanitizer rather than editing GitHub registries as the source of truth.
