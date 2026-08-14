# V1.0 Release Candidate acceptance

Current train: `1.0.0-rc1`.

RC means the product surface is frozen for acceptance. It does **not** mean the divination methods are scientifically validated, and it does not upgrade any module beyond the evidence shown in the App's method-audit center.

## RC scope

The candidate includes six local modules: 紫微、八字、奇门、六爻、大六壬、黄历. It also includes offline `XuanxueAI` evidence/interpretation presentation, but no network provider, no account system, no ads, no payment and no push.

`奇门` full nine-palace output remains an experimental engineering view until full-board golden fixtures and unresolved school conflicts are closed. RC acceptance therefore verifies that this limitation is visible and enforced; it does not relabel the experimental board as a verified standard chart.

## Automated hard gates

A source head may be called an RC build only when the same GitHub Actions run passes all of the following:

1. release copyright boundary;
2. `tools/validate_rc.py` RC metadata/security invariants;
3. completed handoff validation;
4. core/evidence tests;
5. Android `lintDebug` and `lintRelease`;
6. debug and release assembly;
7. APK content audit on both variants;
8. audited artifact packaging with source-head/base/checked-out provenance and SHA256 files.

The release APK generated in CI is intentionally unsigned. No keystore or signing secret may be committed to the repository. The debug APK is the installable artifact for device acceptance.

## Manual hard gate

`DEVICE_ACCEPTANCE.md` must be executed against the exact audited debug APK produced from the candidate source head. At minimum the result must cover a narrow phone and a wider device class, light/dark mode, airplane mode and all six module paths.

Any crash/ANR, blocked primary action, clipped critical content, incorrect current-time initialization, loss of the 奇门 experimental warning, unauthorized interpretation escalation, missing notices, or unexpected network/packaged research asset is a merge blocker.

## Final V1.0 promotion

Only after automated gates and manual device acceptance pass on the same source head should the candidate be promoted:

- change launcher label from `玄学排盘 RC1` to `玄学排盘`;
- change `versionName` from `1.0.0-rc1` to `1.0.0`;
- change `RELEASE_CHANNEL` from `rc` to `stable`;
- update the RC validation gate for stable metadata;
- rerun the full debug + release pipeline;
- mark PR ready for review and merge only after the final head is green.

Signing/distribution credentials remain outside Git. A signed store/release artifact requires a separate secret-management and signing acceptance step; an unsigned CI release APK is packaging evidence, not a production-distribution binary.
