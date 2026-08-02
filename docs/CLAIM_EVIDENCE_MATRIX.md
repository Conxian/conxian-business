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

The SDK is **Beta / conditional**. No value-bearing production signing or settlement is supported from the audited tree, and issues [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195)–[#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) remain open. This business-repo matrix records claim boundaries; it cannot upgrade upstream evidence or reclassify a capability as production-supported.

## Current matrix

| Surface | Claim | Current evidence | Public-safe status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `conxius-wallet` | StrongBox/TEE-backed security exists | Code-visible | Implemented | Real Android keystore and StrongBox-oriented code paths are present. |
| `conxius-wallet` | Play Integrity is production-enforced | Code-visible, but stubbed path inspected | Not yet safe | Release builds now fail closed until end-to-end production path exists. |
| `conxius-wallet` | DLC execution is production-ready | Code-visible, but simulated path inspected | Not yet safe | Simulated flow is now debug-only and fails closed in release builds. |
| `conxius-enclave-sdk` | Signing and attestation interfaces/code paths are present | Code-visible | Interface/code presence only | Public APIs and implementation paths are visible, but this does not establish hardware-backed production support. See the current audit and capability matrix. |
| `conxius-enclave-sdk` | Active production attestation is hardware-bound | Code-visible, mixed with software-driver simulation | Not yet safe — Beta / conditional | Depends on hardware-bound drivers, full caller enforcement, and evidence beyond repo-visible software paths. |
| `conxius-enclave-sdk` | Value-bearing production signing or settlement is supported | July 20 audit and capability matrix explicitly say not to enable it | Not claimed — Beta / conditional | No value-bearing production signing or settlement from the audited tree; unresolved acceptance work remains in issues #195–#202. |
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
