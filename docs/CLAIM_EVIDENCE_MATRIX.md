# Claim vs Evidence Matrix

## Purpose

Provide a reusable decision surface for evaluating whether a technical or product claim is safe to make publicly.

## Evidence levels

- **Doc-only**: claim exists in README, PRD, roadmap, or strategy docs, but code/test/runtime proof is not yet verified.
- **Code-visible**: repository code or configuration exists that supports the claim.
- **Test-visible**: repository tests or CI evidence support the claim.
- **Release-visible**: tagged release, changelog, or release workflow supports the claim.
- **Environment-verified**: confirmed outside GitHub in runtime, device, testnet, or deployment validation.
- **Externally verified**: confirmed by independent audit, assessment, or third-party validation.

## Status labels

- **Simulated**: development or validation path only; not safe to frame as production-enforced.
- **Implemented**: code exists, but production enforcement may still depend on environment or control activation.
- **Production-enforced**: protected by runtime controls, release policy, and readiness gates.
- **Externally verified**: independently reviewed or audited.
- **Interface/code presence only**: a public surface or implementation is visible, but that evidence cannot be promoted to production support.

## Current SDK authority — 2026-07-20

For `conxius-enclave-sdk`, the current authority is the immutable [Production Enablement Audit — 2026-07-20](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md) and [Capability and Evidence Matrix](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/architecture/CAPABILITY_MATRIX.md), recorded by merged [PR #193](https://github.com/Conxian/conxius-enclave-sdk/pull/193) at merge commit `79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8` against audited baseline `8194aa8ade26a9d5d7ed54b7f80f36796fce585c`.

The SDK is **Beta / conditional**. No value-bearing production signing or settlement is supported from the audited tree. Open gates [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195)–[#196](https://github.com/Conxian/conxius-enclave-sdk/issues/196) and [#198](https://github.com/Conxian/conxius-enclave-sdk/issues/198)–[#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) remain required; [#197](https://github.com/Conxian/conxius-enclave-sdk/issues/197) is closed, but closure does not authorize production support. This business-repo matrix records claim boundaries; it cannot upgrade upstream evidence or reclassify a capability as production-supported.

### CON-1513 canonical Bitcoin/Ethereum evidence addendum — 2026-07-22

The immutable `dev` candidate selected by [business PR #939](https://github.com/Conxian/conxian-business/pull/939) is [`3af2cb83988582073f726bebfffe21093a5e3b65`](https://github.com/Conxian/conxius-enclave-sdk/commit/3af2cb83988582073f726bebfffe21093a5e3b65). It descends from the older reviewed fail-closed ancestor [`451202f51a9efed8fde70b7a5567a3e7e16c1db9`](https://github.com/Conxian/conxius-enclave-sdk/commit/451202f51a9efed8fde70b7a5567a3e7e16c1db9), which in turn descends from the reviewed canonical Bitcoin/Ethereum evidence ancestor [`dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570`](https://github.com/Conxian/conxius-enclave-sdk/commit/dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570) via [`5cd6fd4d486ccb00bd7057051bf5e1eb0abf47c7`](https://github.com/Conxian/conxius-enclave-sdk/commit/5cd6fd4d486ccb00bd7057051bf5e1eb0abf47c7) (WASM/provider boundary remediation). `451202f` remains the reviewed fail-closed ancestor, not the current `dev` selection. Selecting `3af2cb8` as an immutable development candidate does not establish release or production acceptance.

The capability-specific, test-visible subset inherited from the reviewed ancestor chain is:

- **Bitcoin:** BIP-322 native P2WPKH and P2TR key-path witnesses without annexes; canonical BIP-340/341 Taproot behavior; and canonical BIP-86 path parsing/output-key derivation.
- **Ethereum:** EIP-191 personal-sign hashing; strict signature, recovery, and address validation; Keccak address derivation; and EIP-55 checksum handling.
- **Unsupported/excluded:** P2WSH, Taproot script-path BIP-322 verification, and annex-bearing Taproot verification remain unsupported. EIP-155 transaction serialization and domain APIs remain out of scope.

Issue [#197](https://github.com/Conxian/conxius-enclave-sdk/issues/197) is closed, but that closure does not authorize production support. Open gates [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195)–[#196](https://github.com/Conxian/conxius-enclave-sdk/issues/196) and [#198](https://github.com/Conxian/conxius-enclave-sdk/issues/198)–[#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) remain, with [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) as final acceptance. Focused test results are capability-specific and historical where recorded; the historical **136 passed / 1 failed** result is not a current mandatory acceptance gate.

### CON-1518 telemetry addendum — 2026-07-21

The telemetry implementation scope landed upstream in [PR #210](https://github.com/Conxian/conxius-enclave-sdk/pull/210) at merge commit `593af0d9120b612de5b2817866b0528e5c877570`. This reviewed PR retains the exact parent gitlink `451202f51a9efed8fde70b7a5567a3e7e16c1db9` and records the public-safe privacy, delivery, monitoring, rollback, and evidence boundary in [CON-1518 telemetry privacy and operational evidence](operations/CON-1518_TELEMETRY_PRIVACY_EVIDENCE.md). This closes the upstream implementation scope only; independent review, service-side retention/deletion evidence, deployed monitoring/recovery evidence, and final production gates remain open. The capability remains **Beta / conditional**.

## Current matrix

| Surface | Claim | Current evidence | Public-safe status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `conxius-wallet` | StrongBox/TEE-backed security exists | Code-visible | Implemented | Real Android keystore and StrongBox-oriented code paths are present. |
| `conxius-wallet` | Play Integrity is production-enforced | Code-visible, but stubbed path inspected | Not yet safe | Release builds now fail closed until end-to-end production path exists. |
| `conxius-wallet` | DLC execution is production-ready | Code-visible, but simulated path inspected | Not yet safe | Simulated flow is now debug-only and fails closed in release builds. |
| `conxius-enclave-sdk` | Signing and attestation interfaces/code paths are present | Code-visible | Interface/code presence only | Public APIs and implementation paths are visible, but this does not establish hardware-backed production support. See the current audit and capability matrix. |
| `conxius-enclave-sdk` | Active production attestation is hardware-bound | Code-visible, mixed with software-driver simulation | Not yet safe — Beta / conditional | Depends on hardware-bound drivers, full caller enforcement, and evidence beyond repo-visible software paths. |
| `conxius-enclave-sdk` | Value-bearing production signing or settlement is supported | July 20 audit and capability matrix explicitly say not to enable it | Not claimed — Beta / conditional | No value-bearing production signing or settlement from the audited tree; open acceptance work remains in #195–#196 and #198–#202. #197 is closed, but closure does not close production acceptance. |
| `conxius-enclave-sdk` | Bitcoin canonical verification subset is implemented | Selected immutable `dev` candidate [`3af2cb8`](https://github.com/Conxian/conxius-enclave-sdk/commit/3af2cb83988582073f726bebfffe21093a5e3b65), descended from older reviewed fail-closed ancestor [`451202f`](https://github.com/Conxian/conxius-enclave-sdk/commit/451202f51a9efed8fde70b7a5567a3e7e16c1db9) and canonical ancestor [`dd1fc4f`](https://github.com/Conxian/conxius-enclave-sdk/commit/dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570) through [`5cd6fd4`](https://github.com/Conxian/conxius-enclave-sdk/commit/5cd6fd4d486ccb00bd7057051bf5e1eb0abf47c7); focused evidence covers the reviewed paths | Implemented — test-visible; not production-supported | BIP-322 is limited to native P2WPKH and P2TR key-path witnesses without annexes; BIP-340/341 Taproot behavior and BIP-86 path parsing/output-key derivation are covered. P2WSH, Taproot script-path, and annex-bearing Taproot verification remain unsupported. Candidate selection does not prove release or production acceptance. |
| `conxius-enclave-sdk` | Ethereum canonical derivation and signed-message subset is implemented | Selected immutable `dev` candidate [`3af2cb8`](https://github.com/Conxian/conxius-enclave-sdk/commit/3af2cb83988582073f726bebfffe21093a5e3b65), descended from older reviewed fail-closed ancestor [`451202f`](https://github.com/Conxian/conxius-enclave-sdk/commit/451202f51a9efed8fde70b7a5567a3e7e16c1db9) and canonical ancestor [`dd1fc4f`](https://github.com/Conxian/conxius-enclave-sdk/commit/dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570); focused evidence covers EIP-191, strict signature/recovery/address validation, Keccak derivation, and EIP-55 | Implemented — test-visible; not production-supported | EIP-155 transaction serialization and domain APIs remain out of scope. Cryptographic subset evidence does not close the hardware, provider, release, or final acceptance gates; candidate selection does not prove release or production acceptance. |
| `conxius-enclave-sdk` | Telemetry is privacy-minimized and non-gating | Upstream PR #210 at `593af0d9120b612de5b2817866b0528e5c877570`; parent retains exact reviewed gitlink `451202f51a9efed8fde70b7a5567a3e7e16c1db9`; public-safe CON-1518 evidence doc | Implemented upstream, not production evidence | Payload minimization, HTTPS/config validation, bounded delivery, failure observability, and rail non-gating are implemented upstream. Independent review, service-side retention/deletion, deployed monitoring/recovery, and final acceptance remain open. |
| `conxian-gateway` | Institutional middleware runtime exists | Code-visible, Release-visible | Implemented | Real runtime code and release history exist. |
| `conxian-gateway` | All critical verification paths are production-enforced | Code-visible with simulated validation references | Not yet safe | Must stay tied to readiness gates and environment-backed verification. |
| `Conxian` protocol | Material protocol implementation exists | Code-visible | Implemented | Real Clarity and sBTC-related surface exists. |
| `Conxian` protocol | Security and correctness are externally proven | No external audit artifact established here | Not yet safe | Requires explicit external verification evidence. |
| `conxian-business` | Public/private boundary is controlled | Code-visible, policy-visible | Implemented | Repo is private and boundary docs are improved. |

## Rules for public claims

1. Do not present **Simulated** as production-ready.
2. Do not present **Implemented** as **Production-enforced** unless the runtime control path is confirmed.
3. Do not present **Production-enforced** as independently validated without external evidence.
4. Prefer precise wording:
   - "implemented"
   - "available in code"
   - "validated in test"
   - "gated in release builds"
   - "verified in environment"
   - "independently reviewed"

## Review cadence

- update after any readiness, release, audit, or security-control change
- check GitHub first
- attach environment-backed evidence separately when available
