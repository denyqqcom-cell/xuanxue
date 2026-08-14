# AI outbound preview + consent binding

Date: 2026-08-14

## Why this change exists

The earlier remote-AI contract required `explicitRemoteConsent=true`, which prevented silent remote use but still left a subtle UI/security weakness: a boolean consent did not prove that the payload being sent was the same question/evidence the user had just reviewed.

This is a TOCTOU-style consent problem. The App could display preview A, receive a yes/no confirmation, then accidentally or incorrectly prepare payload B after state changed.

## New two-step contract

### 1. Preview first

`AiInterpretationGate.preview(chart, question, scope)` produces:

- normalized question;
- exact `AiEvidencePacket` for that scope;
- list of outbound fact ids;
- SHA-256 `payloadFingerprint` covering the canonical question + schema + scope + ordered facts + provenance + caveats.

The UI can render exactly this preview before any network adapter is invoked.

### 2. Bind consent to the preview

For `REMOTE_USER_CONFIGURED`, `AiInterpretationGate.prepare(...)` now requires all of:

- `explicitRemoteConsent=true`;
- a non-null `remoteConsentFingerprint`;
- that fingerprint must equal the fingerprint of the current question/evidence payload.

Failure states are distinct:

- `RemoteConsentRequired`
- `RemoteConsentFingerprintRequired`
- `RemoteConsentMismatch`

A stale confirmation therefore cannot authorize a changed question or changed evidence packet.

`LOCAL_MODEL` does not require remote consent binding because no remote transmission is being authorized.

## What the fingerprint is and is not

It is a deterministic SHA-256 integrity binding for the previewed payload. It is not a secret, not an API key, not user authentication, and not proof that a human physically clicked a button. The Android/UI layer remains responsible for presenting the preview and collecting the user's action.

No crypto/network dependency was added; the implementation uses the JDK `MessageDigest` already available to the JVM core.

## Scope lock still wins

`preview()` itself calls `AiEvidenceBuilder`. Therefore a chart whose `FULL_PLATE` is center-target locked cannot even obtain a fake full-plate outbound preview. The user/adapter cannot bypass the deterministic plate lock merely by supplying a consent fingerprint.

## Acceptance tests

The contract tests now verify:

1. remote mode without explicit consent is rejected;
2. explicit consent without a preview fingerprint is rejected;
3. two different questions on the same chart produce different fingerprints;
4. fingerprint format is 64 lowercase hexadecimal characters;
5. consent from preview A cannot authorize changed question B (`RemoteConsentMismatch`);
6. a real center-target locked chart cannot preview or prepare `FULL_PLATE`;
7. a resolved full source chart prepares successfully with a matching fingerprint;
8. earth-only preview includes `earth_plate` and does not leak duty/full-plate fields;
9. local mode remains usable without remote consent.

GitHub Actions `Qimen Core CI` run `31818916609`: **PASS**.

## Product/UI implication

Recommended Android flow is now mechanically enforceable rather than just copywriting guidance:

`选择 AI 模式 -> 输入问题 -> 选择 scope -> 生成本次发送预览 -> 用户查看字段 -> 用户确认 -> 将 preview fingerprint 带入 remote prepare -> provider adapter`

If the chart/question/scope changes after confirmation, the fingerprint changes and the old consent is invalid.

## Privacy/copyright note

This feature adds no third-party SDK, asset, model provider, copied teaching text or prompt corpus. The outbound packet contains the user's question plus engine-generated structured facts/caveats. Modern source material is used to validate plate algorithms separately; it is not embedded as long-form AI context.
