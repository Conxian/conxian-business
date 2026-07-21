# Mainnet readiness checklist — lib-conclave-sdk (CON-171)

## Status: READY FOR MAINNET (v1.6.0)

This checklist tracks the mainnet readiness for the `lib-conclave-sdk` repository.

The CON-1518 telemetry implementation scope landed upstream in [PR #210](https://github.com/Conxian/conxius-enclave-sdk/pull/210) at merge commit `593af0d9120b612de5b2817866b0528e5c877570`, and this business repo pins that exact SHA. See the public-safe [CON-1518 telemetry privacy and operational evidence](operations/CON-1518_TELEMETRY_PRIVACY_EVIDENCE.md) for the minimized payload, transport, bounded delivery, non-gating, monitoring, rollback, and evidence boundaries. This does not close independent review, service-side retention/deletion evidence, deployed monitoring/recovery evidence, or final production acceptance; the SDK remains **Beta / conditional**.

### 1) Governance + public repo standards
- [x] README includes `## Purpose`, `## Status`, `## Ownership`, and `## Releases`.
- [x] `SECURITY.md` includes a stable reporting path (and avoids private operational detail).
- [x] `CODEOWNERS` covers high-risk surfaces (enclave interfaces, signing flows, and any rails that can materially affect custody or settlement).
- [x] Governance content is public-safe (no key custody procedures, partner terms, private endpoints, or other ZSE-restricted content).

### 2) Release + versioning discipline
- [x] `Cargo.toml` crate version matches the release tag.
- [x] Tags are SemVer (`vX.Y.Z`), including `0.x.y` during beta.
- [x] `CHANGELOG.md` follows Keep a Changelog with a top-level `## [Unreleased]` section.
- [x] Each tag has a GitHub Release (or equivalent release notes artifact) that links the CI evidence.

### 3) CI and supply-chain gates
- [x] `cargo fmt --all -- --check`
- [x] `cargo clippy -- -D warnings`
- [x] `cargo test`
- [x] WASM build is reproducible and does not commit generated `pkg/` artifacts.
- [x] Dependency vulnerability scan is enforced (preferred: `cargo audit` as a CI gate).

### 4) Hygiene: generated artifacts + vendored dependencies
- [x] No generated artifacts are committed (`target/`, `pkg/`, `node_modules/`).
- [x] No runtime secrets/config are committed (`.env.example` only).
- [x] Any vendored source or copied third-party code includes clear attribution and license compatibility.

### 5) Canonical trackers
- Sovereign Coordination Layer: https://sovereign.conxian.com/issue/CON-171
- GitHub repo: https://github.com/Conxian/lib-conclave-sdk

## Related work

- Telemetry privacy and operations: [CON-1518 evidence](operations/CON-1518_TELEMETRY_PRIVACY_EVIDENCE.md)
- Release hygiene: https://sovereign.conxian.com/issue/CON-214/release-hygiene-lib-conclave-sdk
- Secret/artifact cleanup: https://sovereign.conxian.com/issue/CON-215/secret-and-artifact-cleanup-lib-conclave-sdk
- Security hardening: https://sovereign.conxian.com/issue/CON-210/security-hardening-lib-conclave-sdk
