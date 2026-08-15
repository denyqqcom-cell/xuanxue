# V1.0 Release Candidate acceptance — historical

This file records the RC1 promotion contract that was used before V1.0 stable promotion. The active release gate is now `RELEASE_ACCEPTANCE.md`.

Historical train: `1.0.0-rc1`.

RC meant the product surface was frozen for acceptance. It did **not** mean the divination methods were scientifically validated, and it did not upgrade any module beyond the evidence shown in the App's method-audit center.

## Historical RC scope

The candidate included six local modules: 紫微、八字、奇门、六爻、大六壬、黄历. It also included offline `XuanxueAI` evidence/interpretation presentation, but no network provider, no account system, no ads, no payment and no push.

`奇门` full nine-palace output remained an experimental engineering view until full-board golden fixtures and unresolved school conflicts are closed. RC acceptance therefore verified that this limitation was visible and enforced; it did not relabel the experimental board as a verified standard chart.

## Historical promotion conditions

RC1 required copyright/package checks, metadata/security validation, completed handoff validation, core/evidence tests, Android lint, debug/release assembly, APK-content audit, an audited artifact, and narrow/wide device acceptance in airplane mode.

During evidence review, the release process was strengthened further: screenshots became a required review surface, visible Android crash/ANR dialogs became fail-closed conditions, and the emulator image was changed to a lean AOSP image to remove an unrelated Pixel Launcher background ANR from acceptance evidence.

## Stable successor

V1.0 stable uses:

- `versionName = 1.0.0`;
- `RELEASE_CHANNEL = stable`;
- launcher label `玄学排盘`;
- stable package `com.xuanxue.app`;
- debug acceptance package `com.xuanxue.app.debug`.

See `RELEASE_ACCEPTANCE.md` and `tools/validate_release.py` for the current same-head release gate.
