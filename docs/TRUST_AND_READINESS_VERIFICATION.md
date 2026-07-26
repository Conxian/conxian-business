# Trust & Readiness Verification — Public Surface Audit

> **Issue**: [#830](https://github.com/Conxian/conxian-business/issues/830) — Re-verify governance and buyer-trust standards across public repos after docs rollout
> **Status**: Canonical
> **Last verified**: 2026-07-20
> **Review cadence**: On every major release, docs rollout, or trust-surface change

## Purpose

This document consolidates the current trust and readiness story into a single evaluator-facing artifact. It verifies that public repo documentation, README status sections, governance files, and readiness language match current implementation truth — not aspirational target-state claims.

Reference framework: [`TRUST_AND_PROOF_MESSAGING.md`](TRUST_AND_PROOF_MESSAGING.md)

---

## 1) Implementation State Classification

Every claim in the audit below uses one of these classifications:

| Classification | Meaning |
|----------------|---------|
| **Implemented** | Code exists, tests pass, CI enforces it |
| **Verified** | Implemented + independently verified (audit, drill, gate evidence) |
| **Production-ready** | Verified + deployed to mainnet with monitoring and rollback |
| **Target-state** | Designed and spec'd but not yet implemented or verified |
| **Experimental** | Implemented but with known gaps; not for production |

---

## 2) Flagship Repo Audit

### 2.1 Conxius Wallet (`conxius-wallet`)

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | "Production (v1.9.2)" | v1.9.2 is current release tag; CI passing (B2C Wallet Suite green) | **Production-ready** | Minor: "Production" should be "Stable" per trust taxonomy |
| **Scope** | "Wallet app code, signer UX, reference client flows." | Correct. No protocol logic or infrastructure duplicated. | **Implemented** | None |
| **Security** | "CXN Guardian" badge | SECURITY.md exists; StrongBox/TEE boundary documented | **Verified** | None |
| **Governance** | "Maintained by Conxian-Labs as public infrastructure" | CODEOWNERS and CONTRIBUTING.md present | **Implemented** | None |
| **Release discipline** | v1.9.2 tag | CHANGELOG.md present; versioned releases | **Verified** | None |

**Verdict**: ✅ Trust language matches implementation. Minor: adopt "Stable" status label per TRUST_AND_PROOF_MESSAGING.md taxonomy.

### 2.2 Conxian Nexus (`conxian-nexus`)

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | "Active development (v0.4.17). Production intent exists." | v0.4.17; all CON-383 stubs removed; oracle flipped to real; CI 9/9 green | **Beta** (approaching Stable) | Status is honest. Should add explicit Beta label. |
| **Scope** | "Glass Node implementation, multi-chain state normalization, verifiable service interfaces" | Correct. 8 protocol adapters, MMR proofs, REST + gRPC APIs | **Implemented** | None |
| **Security** | SECURITY.md present | Real cryptographic signatures via lib-conxian-core; bitVM2 Groth16 verification; ZSE compliant | **Verified** | None |
| **Governance** | "Maintained by Conxian-Labs as public infrastructure" | CODEOWNERS, CONTRIBUTING.md, CHANGELOG.md present | **Implemented** | None |
| **API** | REST + gRPC surfaces | 18 routes + admin API documented in source; OpenAPI spec referenced | **Implemented** | OpenAPI spec may need regeneration |

**Verdict**: ✅ Trust language matches implementation. Honest about "active development" status. Upgrade to "Beta" label explicit.

### 2.3 Conxian Fusion (gateway service) (`conxian-gateway`)

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | README not accessible (submodule not initialized in workspace) | CI: Gateway Suite green; cargo check + cargo test pass | **Beta** | README needs trust section audit when submodule initialized |
| **Scope** | ISO 20022 compliance pipe; cross-layer state aggregation | Implemented per CI coverage | **Implemented** | None known |
| **Security** | — | ZSE compliant; contamination guard enforced | **Verified** | None known |

**Verdict**: ⚠️ Cannot fully verify — submodule not initialized in current workspace. CI evidence suggests Beta status. Schedule full audit when submodule accessible.

### 2.4 Conxian Core Protocol (`Conxian`)

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | Pinned submodule (update=none); mainnet deployment plan exists | CSF mainnet readiness gate: "Go (pending ALEX funding)"; 16 Clarity contracts with clarity-version=4 | **Production-ready** (gated) | Pending ALEX funding verification |
| **Scope** | Core protocol + on-chain contracts; sovereign treasury | Correct. Contracts use dynamic principals via operational-treasury.clar | **Implemented** | None |
| **Security** | CON-61 (admin centralization), CON-371 (ST→SP) remediated | ZSE + Contamination Guard active; all P0 blockers closed | **Verified** | None |
| **Governance** | CON-389 branch/promotion standard enforced | Promotion pipeline: dev→staged→main | **Implemented** | None |

**Verdict**: ✅ Trust language backed by gate evidence. Mainnet readiness: Conditional Go. Explicit about ALEX funding gate.

### 2.5 Conxian Labs Site (`conxian-labs-site`)

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | Submodule not initialized | Deployed via GitHub Pages (deploy-docs workflow); CI green | **Beta** | Schedule audit when submodule accessible |

**Verdict**: ⚠️ Cannot verify — submodule not initialized. Deploy-docs CI workflow runs successfully.

---

### 2.6 `conxius-enclave-sdk`

> **Current authority:** [Production Enablement Audit — 2026-07-20](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md) and [Capability and Evidence Matrix](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/architecture/CAPABILITY_MATRIX.md), recorded by merged [PR #193](https://github.com/Conxian/conxius-enclave-sdk/pull/193) at merge commit `79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8` against audited baseline `8194aa8ade26a9d5d7ed54b7f80f36796fce585c`.
>
> **Active business-repository integration pin:** [`451202f51a9efed8fde70b7a5567a3e7e16c1db9`](https://github.com/Conxian/conxius-enclave-sdk/commit/451202f51a9efed8fde70b7a5567a3e7e16c1db9), the safe fail-closed pin, descends from reviewed canonical ancestor [`dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570`](https://github.com/Conxian/conxius-enclave-sdk/commit/dd1fc4f14e950a0b6119aeffbcbb4ae8ecce570) through [`5cd6fd4d486ccb00bd7057051bf5e1eb0abf47c7`](https://github.com/Conxian/conxius-enclave-sdk/commit/5cd6fd4d486ccb00bd7057051bf5e1eb0abf47c7) and the active [`451202f51a9efed8fde70b7a5567a3e7e16c1db9`](https://github.com/Conxian/conxius-enclave-sdk/commit/451202f51a9efed8fde70b7a5567a3e7e16c1db9) fail-closed adapter remediation. `dd1fc4f` is the reviewed ancestor, not the active business-repository pin.

| Attribute | Claimed | Actual | Classification | Gap? |
|-----------|---------|--------|---------------|------|
| **Status** | Earlier readiness records used stronger labels | **Beta / conditional** under the July 20 audit; gates [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195)–[#196](https://github.com/Conxian/conxius-enclave-sdk/issues/196) and [#198](https://github.com/Conxian/conxius-enclave-sdk/issues/198)–[#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) remain open, while [#197](https://github.com/Conxian/conxius-enclave-sdk/issues/197) is closed without production authorization | **Beta / conditional** | Yes — current evidence does not support an unqualified production claim |
| **Interface/code presence** | Signing, attestation, protocol, and WASM surfaces exist | The matrix records API presence, but implementation completeness, integration evidence, independent review, and production support are not established across the surface | **Interface/code presence only** | Yes — presence cannot upgrade upstream evidence |
| **Value-bearing operations** | No current production enablement claim | The audit explicitly says not to enable value-bearing production signing or settlement from the audited tree | **Not claimed** | Yes — hardware, attestation, protocol, release, and operational gates remain incomplete |
| **Canonical Bitcoin subset** | Broad Bitcoin/BIP-322 support | The active safe pin covers BIP-322 native P2WPKH and P2TR key-path verification without annexes, canonical BIP-340/341 Taproot behavior, and canonical BIP-86 path parsing/output-key derivation; the reviewed canonical ancestor is `dd1fc4f`, with fail-closed descendants `5cd6fd4` and `451202f` | **Implemented** | P2WSH, Taproot script-path, and annex-bearing Taproot verification remain unsupported; this is not production support while #195–#196 and #198–#202 remain open |
| **Canonical Ethereum subset** | Broad Ethereum transaction and signing support | The active safe pin covers EIP-191 personal-sign hashing, strict signature/recovery/address validation, Keccak address derivation, and EIP-55 checksum handling | **Implemented** | EIP-155 transaction serialization and domain APIs remain out of scope; hardware/provider, release, and final acceptance evidence remain incomplete |

**Verdict**: ⚠️ The SDK is **Beta / conditional**. The active pin establishes a focused, test-visible Bitcoin/Ethereum cryptographic subset, not full multi-chain support or production authorization. Build success, API presence, simulated paths, or structural tests are not production-support evidence. Capability-specific focused tests and historical results remain bounded evidence; the historical **136 passed / 1 failed** result is not a current mandatory acceptance gate. The audit is a public repository evidence review, not an independent security certification.

---

#### CON-1518 telemetry addendum — 2026-07-21

The privacy and delivery implementation landed upstream in [PR #210](https://github.com/Conxian/conxius-enclave-sdk/pull/210) at `593af0d9120b612de5b2817866b0528e5c877570`; this reviewed PR retains the exact parent gitlink `451202f51a9efed8fde70b7a5567a3e7e16c1db9`. The public-safe [CON-1518 evidence record](operations/CON-1518_TELEMETRY_PRIVACY_EVIDENCE.md) documents minimized payloads, HTTPS/config validation, bounded timeout/retry, failure observability, rail non-gating behavior, and operational boundaries. Independent review, service-side retention/deletion evidence, deployed monitoring/recovery evidence, and final production gates remain open; no release-candidate or production-acceptance claim is made.

## 3) Cross-Cutting Trust Pillars

### 3.1 Security Posture

| Pillar | Evidence | Classification |
|--------|----------|---------------|
| Vulnerability reporting | `SECURITY.md` in conxius-wallet, conxian-nexus | **Implemented** |
| Secret hygiene | ZSE enforced; contamination guard blocks testnet principals in production .clar files | **Verified** |
| Dependency scanning | Dependabot active on all submodules; `cargo audit` runs in CI | **Implemented** |
| Automated checks | Conxian Unified CI: 9/9 jobs (B2B, B2C, Core, Gateway, Hygiene, Summary) | **Verified** |
| Code review ownership | `CODEOWNERS` present in all active repos | **Implemented** |
| Third-party audit | **Not claimed**. No public audit report exists. | **N/A — not claimed** |

### 3.2 Governance Standards

| Pillar | Evidence | Classification |
|--------|----------|---------------|
| Spec artifacts | `openspec/` directory; ADR-001 through ADR-006 | **Implemented** |
| Change tracking | PR-based workflow; CHANGELOG.md in all repos | **Implemented** |
| Contribution model | `CONTRIBUTING.md` present | **Implemented** |
| Public vs private split | `BOUNDARY_DECISION_LOG.md` documents boundary decisions; ZSE stubs for internal-only content | **Implemented** |

### 3.3 Release Discipline

| Pillar | Evidence | Classification |
|--------|----------|---------------|
| Versioning | Semantic versioning adopted; tags on releases | **Implemented** |
| Release notes | `CHANGELOG.md` maintained per Keep a Changelog | **Verified** |
| Breaking changes | Documented in changelog; controlled via promotion pipeline | **Implemented** |
| Promotion pipeline | dev → staged → main enforced by CI and branch-protection rules | **Verified** |

---

## 4) What Is NOT Claimed (Trust Boundary)

The following are explicitly **not claimed** on any public surface. This section exists to prevent evaluators from inferring guarantees that are not offered.

| Non-claim | Why |
|-----------|-----|
| "Third-party audited" | No public third-party audit report exists. Security posture is self-assessed with CI enforcement. |
| "SOC 2 / ISO 27001 certified" | Not applicable at current stage. Conxian-Labs is a non-custodial software vendor. |
| "Production SLA" | No uptime or latency SLA is offered for any component. |
| "Bug bounty program" | Bounty workflow exists (BOUNTY_WORKFLOW.md) but payouts are gated on ConxianCSF mainnet + ALEX funding. No payable bounties are currently open. |
| "Fully decentralized" | The BOS uses on-chain truth for critical state, but some components (Nexus, Gateway) are operated by Conxian-Labs. Community sovereign-node lane is target-state (see THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md). |
| "Production-ready" for all components | Only Conxius Wallet is classified as Production-ready. Nexus is Beta. Gateway is Beta. ConxianCSF is gated on ALEX funding. |
| "Value-bearing production signing or settlement from `conxius-enclave-sdk`" | **Not claimed.** The July 20 audit says not to enable these operations from the audited tree while the Beta / conditional acceptance gates remain open. |
| "Full BIP-322 support" | **Not claimed.** The active subset verifies native P2WPKH and P2TR key-path witnesses without annexes; P2WSH, Taproot script-path, and annex-bearing Taproot verification remain unsupported. |
| "EIP-155 transaction/domain support" | **Not claimed.** The active Ethereum subset covers EIP-191, strict signature/recovery/address validation, Keccak derivation, and EIP-55 checksums; EIP-155 transaction serialization and domain APIs remain out of scope. |

---

## 5) Recommended Actions

| Priority | Action | Issue |
|----------|--------|-------|
| P0 | Adopt "Stable" status label for conxius-wallet per trust taxonomy | #830 |
| P1 | Add explicit "Beta" status label to conxian-nexus README | #830 |
| P1 | Audit conxian-gateway and conxian-labs-site READMEs when submodules accessible | #830 |
| P2 | Regenerate OpenAPI spec for conxian-nexus | #830 |
| P2 | Add Trust & Proof section to all flagship READMEs per TRUST_AND_PROOF_MESSAGING.md template | #830 |
| P3 | Complete ALEX funding verification for ConxianCSF mainnet Go decision | CON-129 |

---

## 6) Evaluator Summary

**For technical evaluators, compliance reviewers, and advanced partners:**

The Conxian BOS is a **sovereign-first, non-custodial** financial infrastructure system with:

- **Proven CI pipeline**: 9/9 green across all suites (B2B, B2C, Core, Gateway, Hygiene)
- **Zero Secret Egress**: No secrets in Git; contamination guard enforces production principal hygiene
- **Verifiable state**: Cryptographic MMR proofs and BitVM2 Groth16 verification for cross-chain state
- **Honest maturity labeling**: Conxius Wallet is Stable/Production-ready; Nexus and the gateway service (Conxian Fusion) are Beta; `conxius-enclave-sdk` is Beta / conditional with no value-bearing production signing or settlement; ConxianCSF mainnet is gated on ALEX funding
- **Clear boundary model**: Public-safe architecture docs; internal-only operational detail in Linear per ZSE

**What we do not claim**: third-party audits, production SLAs, full decentralization, or payable bug bounties. See [Section 4](#4-what-is-not-claimed-trust-boundary) for the complete non-claim boundary.

---

## Related Documents

- [Trust & Proof Messaging](TRUST_AND_PROOF_MESSAGING.md)
- [Boundary Decision Log](BOUNDARY_DECISION_LOG.md)
- [CSF Mainnet Readiness Gate](CSF_MAINNET_READINESS_GATE.md)
- [Repo Portfolio](REPO_PORTFOLIO.md)
- [Portfolio Business-Unit Map](PORTFOLIO_BUSINESS_UNIT_MAP.md)
- [Developer Quickstart](DEVELOPER_QUICKSTART.md)
- [CON-1518 telemetry privacy and operational evidence](operations/CON-1518_TELEMETRY_PRIVACY_EVIDENCE.md)
