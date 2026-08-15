# V1.0 Final Release Acceptance

Current release train: `1.0.0` / `stable`.

This document defines the software release gate only. It does **not** claim scientific validation of traditional divination methods, and it does not upgrade any module beyond the evidence grade shown in the App's method-audit center.

## Product boundary

V1.0 includes six local modules: 紫微、八字、奇门、六爻、大六壬、黄历. `XuanxueAI` remains local/provider-neutral architecture only: no enabled cloud provider, account system, ads, payment, analytics or push.

奇门完整九宫仍是实验工程视图，直到完整 golden board 和尚未关闭的流派冲突得到可复核证据。正式版必须继续把这一边界展示给用户，不能因为版本号变为 stable 就把未核验内容改写成“已验证”。

## Same-head automated gates

The exact release source head must pass both GitHub Actions workflows:

1. **App Integration V3 CI**
   - copyright/package boundary;
   - stable release metadata/security invariants;
   - completed handoff validation;
   - core/evidence tests;
   - `lintDebug` + `lintRelease`;
   - debug + unsigned release assembly;
   - APK content audit on both variants;
   - source-head provenance + SHA256 artifact packaging.

2. **V1.0 Emulator Acceptance**
   - Android 35 AOSP emulator boots successfully;
   - airplane mode is enabled and remains enabled;
   - narrow/light profile and wide/dark profile both run;
   - all six modules open and return;
   - core module actions produce structural results without crashing;
   - 奇门 experimental warning, context gate and current device date remain visible;
   - method-audit and open-source notices are reachable;
   - screenshots are captured for every acceptance path;
   - any visible Android crash/ANR dialog causes the test to fail closed;
   - installed debug acceptance package has no INTERNET permission and reports the expected stable debug version.

## Visual evidence review

The emulator artifact contains the exact screenshots and Android test XML for the source head. Promotion is not closed merely because Compose semantics pass: the evidence screenshots must also be reviewed for blocking visual defects such as unreadable contrast, system error overlays, clipped primary controls or missing warnings.

A visual defect found in evidence invalidates that head. Fixes must produce a new head, rerun both workflows, and generate a fresh evidence artifact.

## Release package identity

- stable application id: `com.xuanxue.app`
- debug acceptance application id: `com.xuanxue.app.debug`
- stable version name: `1.0.0`
- debug acceptance version name: `1.0.0-debug`
- release channel: `stable`
- launcher label: `玄学排盘`

The CI release APK remains intentionally unsigned. No keystore or signing secret may be committed to Git. Store/public distribution signing is a separate secret-management step and must not be confused with software acceptance.

## Merge rule

Only a head for which **both workflows pass and its evidence screenshots have been reviewed** may be marked ready for merge. Any later source change invalidates the closure and requires both gates to run again.
