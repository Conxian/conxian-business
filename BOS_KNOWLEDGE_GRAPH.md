# Conxian Labs BOS Knowledge Graph
> Clarity-version: 4 | Epoch: latest | Generated: 2026-07-22

## Overview

This document is the **mandatory BOS Knowledge Graph** referenced in `AGENTS.md`. It provides structured entity extraction for graph-aware traversal by agentic systems.

---

## Doctrine decision — CON-1530 (2026-07-22)

The current doctrine relationship is:

- **Conxian-Labs (Pty) Ltd** is the legal builder/operator company and a non-custodial software and infrastructure builder/operator. It provides routing, orchestration, compliance integration, and verification; it is not a market participant, discretionary fund manager, or user-data extraction business.
- **Conxian** is the protocol/DAO layer. **Conxius** is the client/access/developer-tooling layer. Internal strategy and operations remain separate in the authorized Linear workspace under ZSE.
- **CSF / Conxian Finance Protocol**, **Fusion**, and **Nexus** are protocol/infrastructure product domains or legacy operating labels under the Conxian/Conxius crosswalk; they are not standalone legal custodians, fund controllers, or ambiguous business entities.
- Protocol contracts and DAO rules may implement escrow, settlement, treasury, or yield behavior. Those are protocol-level state transitions and do not establish Conxian-Labs custody, discretionary fund control, or market operation.
- Dated strategy, research, market-narrative, and planning surfaces are public-safe stubs with their restricted canonical source referenced by CON-1530; removed detail was not copied elsewhere in Git.
- Current technical artifact identity uses the exact repository slugs `conxian-gateway`, `conxius-enclave-sdk`, `conxius-orbit`, and `conxian_ui`; deprecated display aliases remain only in the narrowly documented normative/URL exceptions.
- Current role, audience, operating label, maturity, claim state, and document classification are governed by [`docs/PORTFOLIO_DOCTRINE_REGISTER.md`](docs/PORTFOLIO_DOCTRINE_REGISTER.md) and [`docs/DOCTRINE_ALIGNMENT_STANDARD.md`](docs/DOCTRINE_ALIGNMENT_STANDARD.md).

| Entity | Relationship | Boundary |
|--------|--------------|----------|
| Conxian-Labs (Pty) Ltd | builds/operates | Non-custodial software and infrastructure; no discretionary control over participant funds. |
| Conxian | defines | Protocol and DAO rules, contract state, verification, and governance interfaces. |
| Conxius | provides | Client, access, wallet, deployment, platform, and enclave-tooling surfaces. |
| CSF / Conxian Finance Protocol | classifies | Protocol/infrastructure product domain under Conxian; not a legal entity or custodian. |
| Fusion | classifies | Enterprise integration/infrastructure product domain under Conxian; not a legal entity or custodian. |
| Nexus | classifies | State/proof/telemetry infrastructure product domain under Conxian; not a legal entity or custodian. |
| Internal strategy and operations | remains separate from | Public-safe repository documentation; canonical restricted material is maintained in Linear. |


## Entity Registry

### 🏢 Organizations

| Entity | Type | Relationships | Source |
|--------|------|---------------|--------|
| **Conxian-Labs (Pty) Ltd** | Legal Entity | builds/operates non-custodial Conxian and Conxius software; does not custody participant assets | `docs/DOCTRINE_ALIGNMENT_STANDARD.md` |
| **Conxian** | Protocol/DAO Brand | defines protocol rules, contracts, verification, and governance interfaces | `docs/DOCTRINE_ALIGNMENT_STANDARD.md` |
| **Conxius** | Client/Access Brand | provides wallet, platform, deployment, and enclave-tooling surfaces | `docs/DOCTRINE_ALIGNMENT_STANDARD.md` |

### 🧭 Product domains and legacy taxonomy

| Domain | Canonical relationship | Boundary |
|--------|-----------------------|----------|
| **CSF / Conxian Finance Protocol** | Conxian protocol/infrastructure product domain | Contract, asset, fee, and protocol-state scope; not a standalone legal custodian. |
| **Fusion** | Conxian enterprise-infrastructure product domain | Gateway and compliance integration scope; not an independent fund or custody authority. |
| **Nexus** | Conxian state/proof infrastructure product domain | State, synchronization, proof, and telemetry scope; not a standalone legal entity. |

### 📦 Repositories (Submodules)

| Entity | GitHub | Language | Focus | Operating label / maturity and claim state |
|--------|--------|----------|-------|--------|
| `conxian-business` | Conxian/conxian-business | Mixed | Governance and specifications | Production intent / Beta; Implemented governance, Target-state proposals |
| `Conxian` | Conxian/Conxian | Clarity | Protocol contracts | Production intent / Beta; Implemented code, readiness conditional |
| `conxian-gateway` | Conxian/conxian-gateway | Rust | Routing and compliance middleware | Production intent / Beta; Implemented runtime, verification conditional |
| `conxian-nexus` | Conxian/conxian-nexus | Clarity/Rust | State and proof node | Production intent / Beta; Implemented code, deployment claims conditional |
| `conxius-wallet` | Conxian/conxius-wallet | TypeScript | Android client and signing surface | Production intent / Stable; capability-scoped Implemented claims |
| `conxius-platform` | Conxian/conxius-platform | TypeScript | Local developer orchestration | Reference implementation / Incubating |
| `conxius-orbit` | Conxian/conxius-orbit | TypeScript | Contract deployment toolkit | Reference implementation / Incubating |
| `conxius-enclave-sdk` | Conxian/conxius-enclave-sdk | Rust | Enclave and attestation abstraction | Reference implementation / Beta, conditional |
| `conxian_ui` | `Conxian/Conxian_UI` | TypeScript | Public web interaction surface | Reference implementation / Incubating; interface/code presence |
| `lib-conxian-core` | Conxian/lib-conxian-core | Rust | Shared cryptographic and state primitives | Production intent / Beta; Implemented code-visible |
| `conxian-labs-site` | Conxian/conxian-labs-site | TypeScript | Public website and docs surface | Reference implementation / Incubating |

### 🔐 Smart Contracts (Core)

| Entity | File | Tier | Clarity 4 | Issues |
|--------|------|------|-----------|--------|
| `bridge-nft.clar` | cross-chain/ | Core | ✅ | 0 |
| `yield-optimizer.clar` | yield/ | Core | ✅ | 0 |
| `payment-forge.clar` | agents/ | Core | ✅ | 0 |
| `jurisdictional-sharding.clar` | compliance/ | Compliance | ✅ | 0 |
| `block-utils.clar` | utils/ | Util | ✅ | 0 |
| `operational-treasury.clar` | agents/ | **Critical** | ✅ | 0 |
| `pausable.clar` | access/ | **Critical** | ✅ | ❌ ACL missing |

### 🪙 Tokens

| Entity | Type | Trait | Issue |
|--------|------|-------|-------|
| **CXD** | Stablecoin | ft-trait | No peg mechanism |
| **CXLP** | LP Token | sip-010-ft-trait | Mint/burn broken |
| **CXVG** | Governance | sip-010-ft-trait | No distribution |

### 🔧 Technical Components

| Component | Technology | Purpose | Status |
|-----------|------------|---------|--------|
| **CXN Guardian** | TEE (SGX/TrustZone) | Hardware key isolation | ✅ Implemented |
| **ZKC** | Zero-Knowledge | Compliance verification | ✅ Designed |
| **SYI** | Sovereign Yield Index | Yield measurement | ✅ Designed |
| **BitVM2** | Groth16 | L2 state verification | ⚠️ Stub |
| **RGB** | Client-side | Asset validation | ⚠️ In progress |

### 🔧 CI/CD & DevOps

| Component | Technology | Purpose | Status |
|-----------|------------|---------|--------|
| **Gitleaks** | v8.24.2 | Secret scanning | ✅ Configured |
| **cargo audit** | Rust advisory db | Dependency vulnerability scanning | ✅ Active |
| **Conxian Unified CI** | GitHub Actions | Multi-suite test orchestration | ✅ Active |
| **Secret Scan** | Gitleaks workflow | Pre-commit secret detection | ✅ Active |
| **Branch Promotion Policy** | GitHub Actions | Enforce dev → staged → main flow | ✅ Active |

### 🛡️ Vulnerability Allowlist (Cargo Audit)

| RUSTSEC ID | Crate | Status | Rationale |
|------------|-------|--------|------------|
| RUSTSEC-2026-0204 | crossbeam-epoch | ✅ Ignored | Transitive via sled → bdk → electrum-client; no local upgrade path |
| RUSTSEC-2026-0104 | (various) | ✅ Ignored | Transitive dep chain |
| RUSTSEC-2026-0099 | rustls-webpki | ✅ Ignored | Transitive via bdk/electrum-client |
| RUSTSEC-2026-0098 | rustls-webpki | ✅ Ignored | Transitive via bdk/electrum-client |
| RUSTSEC-2024-0388 | instant | ✅ Ignored | Transitive via parking_lot |

### 📦 Dependabot Security Alerts (2026-07-08)

#### High Severity (8) - Action Required
| Alert | Package | Issue | Fixable | Mitigation |
|-------|---------|-------|---------|------------|
| #148 | form-data | CRLF injection | ⚠️ Update | `pnpm update form-data` |
| #143 | vite | fs.deny bypass (Windows) | ⚠️ Update | `pnpm update vite` |
| #149 | ws | Memory exhaustion DoS | ⚠️ Update | `pnpm update ws` |
| #21 | bigint-buffer | Buffer Overflow | ❌ Transitive | Via bdk - no local fix |
| #153 | undici | WebSocket DoS | ⚠️ Update | `pnpm update undici` |
| #146 | undici | TLS cert bypass | ⚠️ Update | `pnpm update undici` |
| #150 | undici | SOCKS5 pool reuse | ⚠️ Update | `pnpm update undici` |
| #58 | rustls-webpki | DoS via panic | ❌ Transitive | Via bdk - no local fix |

#### Moderate Severity (8) - Monitor
| Alert | Package | Issue |
|-------|---------|-------|
| #139 | uuid | Buffer bounds check |
| #60 | postcss | XSS (showcase-dapp) |
| #147 | undici | Cache whitespace bypass |
| #152 | undici | Header injection |
| #144 | launch-editor | NTLMv2 hash (Windows) |
| #145 | protobufjs | Property shadowing |
| #159 | cmov | aarch64 wrong results |
| #142 | ws | Uninitialized memory |

#### Low Severity (7) - Acceptable Risk
| Alert | Package | Issue |
|-------|---------|-------|
| #154 | undici | SameSite downgrade |
| #151 | undici | Response queue |
| #22 | elliptic | Risky crypto |
| #38 | tracing-subscriber | ANSI escape |
| #45 | webpki | Wildcard names |
| #44 | webpki | URI constraints |
| #52 | rand | Custom logger |

#### Known Unfixable Transitive Chains
```mermaid
graph LR
    A[undici] --> B[fetch-hock]
    A --> C[ws]
    D[rustls-webpki] --> E[bdk]
    E --> F[electrum-client]
    G[bigint-buffer] --> E
    H[ws] --> I[wswrapper]
```

### 👥 People (Entity Relationships)

| Role | Entity | Repository Access | Responsibility |
|------|--------|-------------------|----------------|
| Governance maintainer | - | Governance baseline | Maintains public-safe policy and repository boundaries; no custody claim |
| Protocol maintainer | - | Conxian | Maintains protocol/DAO specifications and evidence boundaries |
| Verification reviewer | - | lib-conxian-core | Reviews proof and compliance evidence; no discretionary fund role |
| Protocol metric maintainer | - | `conxian-gateway` | Maintains reference metrics and integrations; no managed-yield claim |

---

## Relationship Graph

```mermaid
graph TB
    subgraph "Legal Entity"
        CL[Conxian-Labs Pty Ltd]
    end

    subgraph "Conxian (Protocol Layer)"
        CNX[Conxian]
        CXD[CXD Token]
        CXLP[CXLP Token]
        CXVG[CXVG Token]
        NEXUS[conxian-nexus]
        GATEWAY[conxian-gateway]
    end

    subgraph "Conxius (Client Layer)"
        WALLET[conxius-wallet]
        PLATFORM[conxius-platform]
        ORBIT[conxius-orbit]
        ENCLAVE[conxius-enclave-sdk]
    end

    subgraph "Core Library"
        CORE[lib-conxian-core]
    end

    CL -.->|builds/operates non-custodial software| CNX
    CL -.->|builds/operates client software; users retain key control| WALLET

    CNX --> CXD
    CNX --> CXLP
    CNX --> CXVG

    CNX --> GATEWAY
    CNX --> NEXUS

    GATEWAY --> CORE
    NEXUS --> CORE
    ENCLAVE --> CORE

    WALLET --> ENCLAVE
    PLATFORM --> ORBIT
```

---

## Decision Registry

| Decision | Date | Rationale | Superseded By |
|----------|------|----------|---------------|
| Clarity 4 only | 2026-04-23 | Security + epoch features | - |
| epoch = "latest" mandatory | 2026-04-23 | Always use newest epoch | - |
| Dynamic principals from treasury | 2026-04-23 | Eliminate hardcoded SPOF | - |
| TEE via `conxius-enclave-sdk` | 2026-04-23 | Hardware key isolation | - |
| ISO 20022 via `conxian-gateway` | 2026-04-23 | Legacy banking bridge | - |
| Doctrine alignment: company is non-custodial infrastructure builder/operator | 2026-07-22 | Separate company role from protocol/DAO and client/access layers; qualify custody, data, market, and protocol-fund language | `docs/DOCTRINE_ALIGNMENT_STANDARD.md` + `docs/PORTFOLIO_DOCTRINE_REGISTER.md` |
| Canonical taxonomy crosswalk and ZSE stub disposition | 2026-07-22 | Keep Conxian-Labs, Conxian, and Conxius as the canonical company/brand boundaries; classify CSF/Fusion/Nexus as product domains and move dated strategy surfaces to authorized Linear under CON-1530 | `docs/DOCTRINE_ALIGNMENT_STANDARD.md` + `docs/DOCUMENTATION_ALIGNMENT_INDEX.md` |
| Cargo audit allowlist for transitive deps | 2026-07-08 | Transitive vulnerabilities without local upgrade path | Upgrade dep chain |
| Gitleaks license via GitHub Secrets | 2026-07-08 | ZSE compliance; no hardcoded secrets | - |
| Infrastructure fixes to main, cherry-pick to PR | 2026-07-08 | Workflow configs belong in main | - |
| Dependabot allowlist for transitive npm deps | 2026-07-08 | undici/ws transitive chains via bdk/wswrapper | Fix upstream |
| GitGuardian var naming convention (no PASSWORD/SECRET in keys) | 2026-07-08 | Avoid false positives from variable names | - |
| Docker env vars use DB_* prefix, not *_PASSWORD | 2026-07-08 | GitGuardian pattern avoidance | - |
| Community governance remediation scope | 2026-07-21 | Prefer the self-contained, non-executing community-voting ledger in protocol PR #521 over isolated `upgrade-controller` work; keep the broader governance gap open until proposal/timelock plumbing and the overlapping #499 scope are resolved. | Protocol PR #521 merge and broader governance decision |

---

## Knowledge Citation Index

| Topic | Knowledge Doc | Last Updated |
|-------|---------------|--------------|
| Operational Standards | `AGENTS.md` | 2026-07-06 |
| Mathematical Framework | `lib-conxian-core/docs/CONXIAN_UNIFIED_THEORY_v2.md` | 2026-04-23 |
| Security Audit | `lib-conxian-core/docs/ADVISORY_REPORT_2026_07_06.md` | 2026-07-06 |
| Knowledge Gaps | `docs/KNOWLEDGE_GAP_ANALYSIS.md` | 2026-07-21 |
| Gateway Research | `conxian-gateway/docs/research/KNOWLEDGE_MAP.md` | 2026-04-23 |
| ISO 20022 Patterns | External: BIS d218, ISO white paper | 2025 |
| Clarity Patterns | External: Stacks Cookbook, CertiK | 2026 |

---

## Critical Links

### Standards
- [Clarity 4](https://stacks.co/blog/clarity-4-bitcoin-smart-contract-upgrade)
- [SIP-033](https://stacks.org/sip-033-clarity-4)
- [SIP Process](https://github.com/stacksgov/sips)
- [ISO 20022 Web APIs](https://iso20022.org)

### Security
- [CertiK Clarity Checklist](https://www.certik.com/resources/blog/clarity-best-practices-and-checklist)
- [sBTC Security Review](https://clarityalliance.org/reports/sbtc)

### Integration
- [Chainlink ISO 20022](https://chain.link/article/iso-20022-integration)
- [BIP-322 Signed Messages](https://bips.dev/322)
- [Lightspark ISO](https://lightspark.com/glossary/iso-20022)

---

## Dated Digest: CON-1506 Production Enablement (2026-07-20)

### Status

| Field | Record |
|-------|--------|
| Linear umbrella | [CON-1506 — production enablement](https://linear.app/conxian-labs/issue/CON-1506/production-enablement) — **authenticated/internal reference only; not public evidence**. Private Linear content is not reproduced here. |
| GitHub umbrella | [conxius-enclave-sdk issue #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191) (**OPEN / REOPENED**) |
| Historical status snapshot | **Beta / conditional**; the latest mandatory gate recorded in [the failed-gate comment](https://github.com/Conxian/conxius-enclave-sdk/issues/191#issuecomment-5027149779) was **136 passed, 1 failed** because of a nondeterministic future-timestamp attestation test. This July 20 snapshot is historical. Current issue state is recorded in the July 22 CON-1512 digest below: #195, #198, #200, and #202 remain open; #196, #197, #199, and #201 are closed. Production enablement remains blocked for value-bearing use. |
| Review boundary | The dated audit remains historical evidence; current status is governed by live GitHub records and the July 22 CON-1512 research/phase-plan record while provider, runtime, release, and independent-acceptance gaps remain open. |
| Historical-status boundary | Older closure/readiness indexes are point-in-time records and are superseded for current status by live GitHub #191 and #195–#202. The 2026-06-03 readiness report is dated and marked internal at [lines 3–6](docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md#L3-L6), records its earlier readiness verdict at [lines 27–35](docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md#L27-L35), and records historical closure indexes at [lines 529–564](docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md#L529-L564). |

### Typed Entities

| Entity | Type | Role / state | Evidence |
|--------|------|--------------|----------|
| `CON-1506` | Linear umbrella issue | Authenticated/internal tracking reference only, not public evidence; private Linear content is not reproduced, and no value-bearing production approval is implied | [Linear issue](https://linear.app/conxian-labs/issue/CON-1506/production-enablement) |
| `#191` | GitHub umbrella issue | **OPEN / REOPENED** historical public umbrella for the enablement review; current unresolved blockers are tracked in #195, #198, #200, and #202, while #196, #197, #199, and #201 are closed but do not by themselves authorize production support | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/191) |
| `#191 comment 5027149779` | GitHub issue comment / mandatory-gate result | Latest public gate evidence: **136 passed, 1 failed** because of a nondeterministic future-timestamp attestation test; implementation is paused pending remediation and a repeatable exact-full-gate pass | [Failed-gate comment](https://github.com/Conxian/conxius-enclave-sdk/issues/191#issuecomment-5027149779) |
| `#193` | Audit documentation pull request | Merged public-safe audit baseline; corrects readiness language to Beta / conditional | [Audit PR](https://github.com/Conxian/conxius-enclave-sdk/pull/193) |
| `conxius-enclave-sdk` | Canonical technical repository/package identifier; shared runtime | Audited at the recorded source revision; support is capability-specific and remains conditional until the required gates pass | [Audited SDK main SHA](https://github.com/Conxian/conxius-enclave-sdk/commit/8194aa8ade26a9d5d7ed54b7f80f36796fce585c) |
| `#195–#202` | Production-enablement gate set | Historical gate set with current public states: **open** #195, #198, #200, #202; **closed** #196, #197, #199, #201. Closed issue state does not promote unsupported capabilities or bypass final acceptance in #202. | [Child gate backlog](https://github.com/Conxian/conxius-enclave-sdk/issues/195) |

### Relationships

| From | Relationship | To | Boundary / meaning |
|------|--------------|----|--------------------|
| `CON-1506` | tracks | [GitHub #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191) | Linear and GitHub records represent the same production-enablement review. |
| `CON-1506` | is an authenticated/internal reference for | [GitHub #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191) | Linear is not public evidence; current public status is taken from live GitHub records, without reproducing private Linear content. |
| [Failed-gate comment #5027149779](https://github.com/Conxian/conxius-enclave-sdk/issues/191#issuecomment-5027149779) | reports the latest mandatory-gate result for | [GitHub #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191) | The public comment records 136 passed and 1 failed due to a nondeterministic future-timestamp attestation test. |
| [GitHub #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191) | is evidenced by | [Audit PR #193](https://github.com/Conxian/conxius-enclave-sdk/pull/193) | The audit establishes the Beta / conditional status and identifies the remaining blockers. |
| [Audit PR #193](https://github.com/Conxian/conxius-enclave-sdk/pull/193) | gates | [Child issues #195–#202](https://github.com/Conxian/conxius-enclave-sdk/issues/195) | P0/P1 work and final acceptance remain required before any affected value-bearing capability is enabled. |
| `conxius-enclave-sdk` | is consumed by | downstream wallet, gateway, and state-node integrations | The SDK is a shared runtime; application UX and protocol authority remain with downstream integrations. |
| [Child issues #195–#201](https://github.com/Conxian/conxius-enclave-sdk/issues/195) | are prerequisites for | [Final acceptance #202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | Final acceptance is capability-by-capability and applies only to the exact reviewed candidate. |

### Decisions

| Decision | Operational meaning |
|----------|---------------------|
| Fail closed | Missing, insufficient, unsupported, or unverifiable security and protocol evidence produces a typed disabled/unsupported outcome rather than a permissive success path. |
| Simulation is not production evidence | Simulated, mock, structural, or placeholder paths cannot satisfy production acceptance for signing, attestation, verification, settlement, or recovery. |
| Trace every production claim | Each supported capability requires a requirement → code → test → CI → artifact evidence chain tied to the exact reviewed candidate. |
| Support is capability-specific | A working build or repository-level audit does not imply support for every chain, adapter, hardware tier, runtime, or protocol; unsupported capabilities remain disabled or conditional. |
| Public documentation stays ZSE-safe | Public records contain only minimum necessary status, evidence, and ownership boundaries; private endpoints, credentials, privileged identifiers, financial strategy, recovery procedures, incident secrets, and raw configurations remain excluded. |
| Preserve the failed-gate boundary | The historical **136 passed, 1 failed** result is not an acceptance pass. Current progress is represented by merged #237/#239 and open containment PR #244, but provider, runtime, release, and independent evidence still block production enablement. |
| Keep Linear evidence internal | CON-1506 is an authenticated/internal reference, not public evidence; no private Linear content is copied into this graph. |

### Risks

| Risk | Current implication / follow-up |
|------|-------------------------------|
| Software or simulated signer boundary | Value-bearing signing must not instantiate a software or simulated signer; remediation and negative evidence are tracked in [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195). |
| Incomplete attestation enforcement | Hardware trust, freshness, replay protection, trusted roots, and purpose binding require explicit enforcement evidence; tracked in [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195). |
| Protocol correctness and placeholders | Bitcoin/Ethereum verification, threshold/settlement, CCTP, account abstraction, asset metadata, and rail-address behavior remain conditional until canonical evidence or typed disablement exists; tracked in [#196](https://github.com/Conxian/conxius-enclave-sdk/issues/196), [#197](https://github.com/Conxian/conxius-enclave-sdk/issues/197), and [#198](https://github.com/Conxian/conxius-enclave-sdk/issues/198). |
| Release, MSRV, and version evidence drift | Toolchain, dependency, release, provenance, and exact-artifact records must reconcile before a stable support statement; tracked in [#199](https://github.com/Conxian/conxius-enclave-sdk/issues/199). |
| WASM secret boundary and platform evidence | Build success alone does not prove opaque secret handling or runtime support across browser, Node, bundler, and worker surfaces; tracked in [#200](https://github.com/Conxian/conxius-enclave-sdk/issues/200). |
| Telemetry and operations | Privacy-safe defaults, payload minimization, monitoring, rollback, and public-safe operational evidence remain required; tracked in [#201](https://github.com/Conxian/conxius-enclave-sdk/issues/201). |
| Nondeterministic future-timestamp attestation test | At the July 20 historical snapshot, the mandatory gate was non-repeatable at **136 passed, 1 failed**. Current progress is represented by merged #237/#239 and open containment PR #244; the exact provider, runtime, release, and independent-acceptance gates still remain. Evidence: [#191 failed-gate comment](https://github.com/Conxian/conxius-enclave-sdk/issues/191#issuecomment-5027149779). |
| Historical readiness-index drift | Older closure/readiness indexes can overstate current readiness when treated as live status; use GitHub #191 and #195–#202 as the current public boundary, with the dated report retained only as historical evidence ([lines 3–6](docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md#L3-L6), [lines 529–564](docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md#L529-L564)). |
| Stale BOS repository identity or submodule pin | Repository inspection verified legacy SDK identity references in existing BOS records, a `.gitmodules` branch reference that does not match the public remote default, and a current gitlink distinct from the audited SHA. Reconcile these separately; this PR intentionally changes neither submodule pins nor unrelated stale documentation. |

### Gates

| Gate | Priority | Required outcome | Status |
|------|----------|------------------|--------|
| [#195 — hardware signing and mandatory attestation](https://github.com/Conxian/conxius-enclave-sdk/issues/195) | P0 | Hardware-backed signing and complete attestation policy for value-bearing operations; no simulated signer fallback | Open; blocks affected production claims |
| [#196 — canonical Bitcoin and Ethereum verification](https://github.com/Conxian/conxius-enclave-sdk/issues/196) | P0 | Canonical verification, hashing, derivation, vectors, and deterministic negative behavior | **Closed; capability claims remain evidence-scoped** |
| [#197 — threshold and settlement placeholders](https://github.com/Conxian/conxius-enclave-sdk/issues/197) | P0 | Audited protocol-conformant implementations or typed unsupported/disabled paths | **Closed; capability claims remain evidence-scoped** |
| [#198 — CCTP, account abstraction, and asset metadata](https://github.com/Conxian/conxius-enclave-sdk/issues/198) | P0 | Canonical adapter, address, asset, network, provenance, and checksum evidence or fail-closed disablement | Open; blocks affected rail and asset claims |
| [#199 — reproducible release and toolchain](https://github.com/Conxian/conxius-enclave-sdk/issues/199) | P1 | One supported toolchain and release path with exact artifact, provenance, SBOM, and scan evidence | **Closed; current business pin/release synchronization remains separate** |
| [#200 — WASM boundary and platform evidence](https://github.com/Conxian/conxius-enclave-sdk/issues/200) | P1 | Opaque secret boundary plus runtime/platform support evidence and mock separation | Open; required for WASM support claims |
| [#201 — telemetry, privacy, and operations](https://github.com/Conxian/conxius-enclave-sdk/issues/201) | P1 | Minimized telemetry, safe defaults, and public-safe monitoring/recovery evidence | **Closed; current production evidence remains capability-specific** |
| [#202 — independent review and release acceptance](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | P0 | Final capability-by-capability acceptance for the exact candidate after #195–#201 are resolved or explicitly scoped | Open; final gate, cannot be bypassed |

### Evidence Index

| Evidence | Link |
|----------|------|
| Linear umbrella | [CON-1506 — production enablement](https://linear.app/conxian-labs/issue/CON-1506/production-enablement) — authenticated/internal reference only; not public evidence |
| Current public status boundary | [conxius-enclave-sdk issue #191](https://github.com/Conxian/conxius-enclave-sdk/issues/191), current [#195–#202](https://github.com/Conxian/conxius-enclave-sdk/issues/195), and the July 22 [CON-1512 research/phase plan](docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md) |
| Current mandatory-gate evidence | [#191 comment 5027149779](https://github.com/Conxian/conxius-enclave-sdk/issues/191#issuecomment-5027149779) — **136 passed, 1 failed**; nondeterministic future-timestamp attestation test; implementation paused pending a fix and repeatable exact-full-gate pass |
| Historical audit documentation | [PR #193](https://github.com/Conxian/conxius-enclave-sdk/pull/193) |
| Historical audit PR head / changeset | [`39f9a885e03f7d259bcbdfe33f0722db76a83ec9`](https://github.com/Conxian/conxius-enclave-sdk/commit/39f9a885e03f7d259bcbdfe33f0722db76a83ec9) |
| Historical SDK main merge commit | [`79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8`](https://github.com/Conxian/conxius-enclave-sdk/commit/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8) |
| Historical audited SDK baseline | [`8194aa8ade26a9d5d7ed54b7f80f36796fce585c`](https://github.com/Conxian/conxius-enclave-sdk/commit/8194aa8ade26a9d5d7ed54b7f80f36796fce585c) |

---

## Dated Digest: CON-1512 Hardware Signing and Attestation Research (2026-07-22)

### Status

| Field | Record |
|-------|--------|
| Linear umbrella | [CON-1512 — enforce hardware-backed signing and mandatory attestation](https://linear.app/conxian-labs/issue/CON-1512/p0-enforce-hardware-backed-signing-and-mandatory-attestation-for-value) — current implementation/research authority; private Linear detail is not reproduced here. |
| Child issues | [CON-1543](https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and), [CON-1544](https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity), and [CON-1545](https://linear.app/conxian-labs/issue/CON-1545/p0-qualify-aws-nitro-attestation-and-kms-secret-release-boundary) |
| Live state revalidation | GitHub and Linear states were revalidated on **July 22, 2026**: CON-1512 is **Urgent / In Progress**; CON-1543 and CON-1519 are **Urgent / Triage**; CON-1544 is **Urgent / In Review** and remains open; CON-1546 is **Urgent / Triage**; SDK #241 and #240 are open; SDK #243 and wallet #441/#442 are merged; SDK #246 is **MERGED** as of **2026-07-22 16:36:34 UTC**, while wallet #443 remains open. These administrative states do not establish production support. |
| Current boundary | Authorization proof, platform attestation, and protocol-key custody/signing are separate claims. Their intersection is required for value-bearing operations; unsupported paths remain fail closed. Administrative closure/completion of a tracker is not production qualification evidence. |
| Provider decision | Split portfolio: Android KeyMint/StrongBox plus server-verified Play Integrity for phone/client evidence; AWS Nitro plus attested KMS release for server/cloud evidence. Neither track is current production support or a substitute for protocol-key custody evidence. |
| Current implementation point | Merged SDK PRs [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237), [#239](https://github.com/Conxian/conxius-enclave-sdk/pull/239), and [#243](https://github.com/Conxian/conxius-enclave-sdk/pull/243) provide bounded containment evidence. Merged SDK PR [#246](https://github.com/Conxian/conxius-enclave-sdk/pull/246) (**2026-07-22 16:36:34 UTC**) is a bounded hardening artifact; wallet [#443](https://github.com/Conxian/conxius-wallet/pull/443) remains an open hardening follow-up. Wallet [#441](https://github.com/Conxian/conxius-wallet/pull/441) and [#442](https://github.com/Conxian/conxius-wallet/pull/442) are merged bounded client boundaries. Open SDK PR [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244) at current head [`e3b1a69752f3e40f26b373e36ecab440c78419a9`](https://github.com/Conxian/conxius-enclave-sdk/commit/e3b1a69752f3e40f26b373e36ecab440c78419a9) remains the selected canonical six-proof rail convergence candidate; follow-up review [#4755756667](https://github.com/Conxian/conxius-enclave-sdk/pull/244#pullrequestreview-4755756667) reports no actionable findings after the replay-capacity fix and all reported SDK checks passing. |
| Downstream gate | [Business Gate #890](https://github.com/Conxian/conxian-business/issues/890) remains open and blocked at Gate 0; it is not an execution authorization. |

### Six evidence lanes

The three-claim boundary is expanded into six auditable evidence lanes. Progress in one lane cannot be promoted into another.

| Evidence lane | Current boundary | Promotion requirement | No-go claim |
|----------------|------------------|-----------------------|-------------|
| **Android client evidence/token collection and deterministic request binding** | Merged SDK [#243](https://github.com/Conxian/conxius-enclave-sdk/pull/243) and wallet [#441](https://github.com/Conxian/conxius-wallet/pull/441) / [#442](https://github.com/Conxian/conxius-wallet/pull/442), with merged hardening [SDK #246](https://github.com/Conxian/conxius-enclave-sdk/pull/246) (**2026-07-22 16:36:34 UTC**) / open wallet [#443](https://github.com/Conxian/conxius-wallet/pull/443), define bounded client/SDK evidence collection and binding interfaces. | Canonical operation digest, nonce/challenge, audience, package/signing identity, key identity, purpose, algorithm, and evidence/token digests with deterministic positive and negative vectors. | Client-collected evidence, a bound request envelope, or a merged interface PR does not qualify a real device/provider or create an authoritative backend verdict. |
| **Trusted backend certificate/token verification and revocation** | Open SDK [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240), [CON-1543](https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and), and [CON-1544](https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity) own the operational trust boundary. | Versioned verifier registry, certificate-chain/trusted-root validation, current collateral, revocation, server-side Play Integrity token verification, exact release identity/request binding, and a normalized policy verdict. | Token presence, client-side parsing, or structural certificate evidence does not prove backend verification, current revocation status, or provider qualification. |
| **Freshness and durable replay** | Shared under open SDK [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) / [CON-1543](https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and); no completed distributed replay service is claimed. | Trusted time/expiry, stale-result rejection, nonce/challenge uniqueness, and atomic durable `consume_once` across restarts, replicas, and recovery. | A process-local cache, client timestamp, fixture, or one successful request does not establish durable replay protection. |
| **Production authorization enforcement** | The merged boundaries are inputs only. Wallet gate/envelope work is tracked in [#444 / CON-1546](https://github.com/Conxian/conxius-wallet/issues/444); the canonical SDK rail remains open in [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244). | A centralized fail-closed gate must combine authoritative evidence, exact operation binding, freshness/replay, signer policy, and typed outcomes; software, mock, debug, and synthetic-success routes must be ineligible for value operations. | Merged interface code, green CI, a current branch, or UI confirmation does not authorize production value operations. |
| **Protocol-key custody** | Protocol-key custody remains separate under [CON-1512](https://linear.app/conxian-labs/issue/CON-1512/p0-enforce-hardware-backed-signing-and-mandatory-attestation-for-value) and SDK [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195). Android P-256 authorization is distinct from Bitcoin/Stacks secp256k1/Schnorr signing. | Exact protocol-key identity, non-exportability or approved custody boundary, signer authorization, algorithm/payload binding, deterministic protocol vectors, and exact runtime/release evidence. | KeyMint/StrongBox or Play Integrity evidence does not establish custody of the Bitcoin/Stacks protocol key or prove the required protocol signature path. |
| **Independent release acceptance** | [CON-1519](https://linear.app/conxian-labs/issue/CON-1519/p0-complete-independent-security-review-and-release-acceptance) and SDK [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) remain the independent review and release gate. | Exact source/artifact identity, SBOM, provenance, dependency/security evidence, version/pin synchronization, capability-level tests, and independent review of the claimed scope. | A merged PR, current head, green CI, or generated documentation does not establish independent release acceptance. |

The no-go boundary is explicit: merged SDK #243 and #246 and wallet #441/#442 do not qualify real devices/providers, prove trusted backend verification or revocation, establish durable replay, authorize production value operations, establish protocol-key custody, or satisfy independent release acceptance. Wallet #443 remains an open hardening follow-up; open SDK #240 and CON-1544 remain prerequisite tracks.

### Typed Entities

| Entity | Type | Current state | Evidence |
|--------|------|---------------|----------|
| `CON-1512` | Linear implementation umbrella | Current research and sequencing authority for hardware-backed signing and mandatory attestation | [Linear issue](https://linear.app/conxian-labs/issue/CON-1512/p0-enforce-hardware-backed-signing-and-mandatory-attestation-for-value) |
| `CON-1543` | Linear shared prerequisite | Trust roots, collateral, revocation, and distributed replay | [Linear issue](https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and) |
| `CON-1544` | Linear provider track | **URGENT / IN REVIEW**; remains open as of July 22, 2026 | Android qualification remains incomplete: trusted roots/collateral, server-side verification, real-device/runtime evidence, exact key/operation binding, replay, and independent release acceptance remain required; unsupported production paths stay fail closed. [Linear issue](https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity) |
| `CON-1545` | Linear provider track | AWS Nitro attestation and KMS secret-release boundary qualification | [Linear issue](https://linear.app/conxian-labs/issue/CON-1545/p0-qualify-aws-nitro-attestation-and-kms-secret-release-boundary) |
| `#195` | SDK issue | **OPEN** P0 hardware-backed signing and mandatory attestation umbrella | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/195) |
| `#196` | SDK issue | **CLOSED** canonical Bitcoin/Ethereum verification and derivation; closure is not universal production support | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/196) |
| `#197` | SDK issue | **CLOSED** threshold and settlement placeholder quarantine/remediation; closure is capability-scoped | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/197) |
| `#198` | SDK issue | **OPEN** CCTP, account abstraction, and asset metadata fail-closed work | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/198) |
| `#199` | SDK issue | **CLOSED** toolchain/dependency/release evidence work; current pin/release drift remains separate | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/199) |
| `#200` | SDK issue | **OPEN** WASM secret boundary and runtime/platform evidence | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/200) |
| `#201` | SDK issue | **CLOSED** telemetry privacy and public-safe operational work; current capability evidence remains scoped | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/201) |
| `#202` | SDK issue | **OPEN** independent security review and release acceptance | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/202) |
| `#240` | SDK issue | **OPEN** shared trust/collateral/revocation/replay prerequisite | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/240) |
| `#241` | SDK issue | **OPEN** Android provider track; corresponding Linear CON-1544 is **URGENT / IN REVIEW** | Qualification remains incomplete; real trusted roots/collateral, server-side verification, real-device/runtime evidence, exact key/operation binding, replay, and independent release acceptance remain required; unsupported production paths stay fail closed. [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/241) |
| `#242` | SDK issue | **OPEN** AWS Nitro provider track | [GitHub issue](https://github.com/Conxian/conxius-enclave-sdk/issues/242) |
| `#444 / CON-1546` | Wallet issue / Linear tracker | **OPEN / TRIAGE** centralized wallet value-operation gate and software/synthetic-success quarantine; **next 86/100 containment candidate; not production support** | [GitHub issue](https://github.com/Conxian/conxius-wallet/issues/444) |
| `#237` | SDK pull request | **MERGED** independent proof-factor verification at `8f3fa687f4a880c0a12ec1fabc613ecc9e043df4` | [GitHub PR](https://github.com/Conxian/conxius-enclave-sdk/pull/237) |
| `#239` | SDK pull request | **MERGED** independent proof verification at `0510ecd5096c39eed4b8909f9e48e56697a7bc57` | [GitHub PR](https://github.com/Conxian/conxius-enclave-sdk/pull/239) |
| `#243` | SDK pull request | **MERGED** Android authorization-evidence boundary | Bounded SDK evidence/request interface only; no provider, real-device, backend-verifier, custody, or release claim. [GitHub PR](https://github.com/Conxian/conxius-enclave-sdk/pull/243) |
| `#246` | SDK pull request | **MERGED** (2026-07-22 16:36:34 UTC) Android authorization-binding hardening | Merged implementation evidence remains bounded; no provider/device qualification, production support, durable replay, protocol-key custody, authorization enforcement, or independent release acceptance claim. [GitHub PR](https://github.com/Conxian/conxius-enclave-sdk/pull/246) |
| `#441` | Wallet pull request | **MERGED** KeyMint authorization boundary | Bounded wallet-side authorization interface only; no real-device/provider, backend-verification, custody, or production value-authorization claim. [GitHub PR](https://github.com/Conxian/conxius-wallet/pull/441) |
| `#442` | Wallet pull request | **MERGED** Play Integrity SDK request boundary | Bounded client token/request collection and binding only; server-side verification, revocation, real-device qualification, and production authorization remain open. [GitHub PR](https://github.com/Conxian/conxius-wallet/pull/442) |
| `#443` | Wallet pull request | **OPEN** KeyMint authorization-evidence hardening follow-up | Unmerged review/implementation evidence; no production qualification claim. [GitHub PR](https://github.com/Conxian/conxius-wallet/pull/443) |
| `#244` | SDK pull request | **OPEN** canonical six-proof rail convergence at current head `e3b1a69752f3e40f26b373e36ecab440c78419a9`; follow-up review [#4755756667](https://github.com/Conxian/conxius-enclave-sdk/pull/244#pullrequestreview-4755756667) reports no actionable findings after the replay-capacity fix and all reported checks pass | [GitHub PR](https://github.com/Conxian/conxius-enclave-sdk/pull/244) |
| `CON-1517` | Linear runtime/release issue | Runtime/platform evidence and WASM secret-boundary work remain required | [Linear issue](https://linear.app/conxian-labs/issue/CON-1517/p1-harden-the-wasm-secret-boundary-and-add-runtimeplatform-evidence) |
| `CON-1519` | Linear acceptance issue | Independent security review and release acceptance remain required | [Linear issue](https://linear.app/conxian-labs/issue/CON-1519/p0-complete-independent-security-review-and-release-acceptance) |
| `#890` | Business issue / downstream gate | **OPEN**, Gate 0 blocked; not execution authorization | [GitHub issue](https://github.com/Conxian/conxian-business/issues/890) |

### Relationships

| From | Relationship | To | Boundary / meaning |
|------|--------------|----|--------------------|
| `CON-1512` | decomposes into | `CON-1543`, `CON-1544`, `CON-1545` | Shared trust/replay work precedes Android and Nitro qualification. |
| `#240` | blocks | `#241`, `#242` | Provider tracks require common roots, collateral, revocation, normalized results, freshness, and durable replay. |
| `#237` | strengthens | authorization proof | Independent proof factors are typed and checked separately. |
| `#239` | enforces | fail-closed authorization | Independent verification contains missing or invalid proof outcomes. |
| `#243` and wallet `#441` / `#442` | provide | client evidence/request-boundary artifacts | Merged interface/containment evidence only; SDK `#246` is also merged hardening, while wallet `#443` remains open. |
| SDK `#246` and wallet `#443` | harden | deterministic Android authorization binding | SDK `#246` merged at **2026-07-22 16:36:34 UTC**; wallet `#443` remains open. Neither qualifies providers, backend verification, protocol-key custody, or production value operations. |
| `#244` | contains | canonical six-proof settlement rail | Selected containment candidate; open and not a hardware qualification. |
| `#444 / CON-1546` | executes | wallet gate/envelope phase | After canonical rail convergence; no provider qualification claim. |
| `#195` | governs | value-bearing signing/attestation claims | No production claim is allowed without the full acceptance chain. |
| `CON-1517` | blocks | runtime/platform claims | Build success does not prove secret-boundary or runtime evidence. |
| `CON-1519` / `#202` | gates | immutable release and independent acceptance | Exact artifact and capability-by-capability acceptance remain required. |
| `#890` | depends on | hardware/attestation and independent acceptance | Downstream control-plane handoff remains blocked and cannot authorize execution. |

### Decisions and risks

| Decision / risk | Operational meaning |
|----------------|---------------------|
| Split providers | Keep phone/client and server/cloud evidence as separate tracks; do not make a universal hardware-support claim. |
| Authorization ≠ attestation ≠ custody | A valid user proof, platform report, or signature is insufficient in isolation. |
| Unsupported paths fail closed | Software, simulated, heuristic, unverified, stale, and unregistered provider paths remain disabled. |
| Wallet readiness language is stale/high-risk | Merged KeyMint/Play Integrity boundaries are bounded interface evidence; open hardening and backend verification remain, so older StrongBox/Play Integrity wording is not current production evidence. |
| Pin/release drift is separate | `.gitmodules` tracks `master` while upstream default is `main`; business pin, SDK release, and current upstream `main` must not be conflated. Pin/release drift is not current evidence and is not changed in this docs PR. |
| Historical records remain historical | The July 20 CON-1506 digest is preserved; current issue states and PR progress are recorded here rather than retroactively rewriting history. |

### Evidence Index

| Evidence | Link |
|----------|------|
| Canonical research and phase plan | [`docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md`](docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md) |
| Stable bounded interface/containment artifacts | Merged SDK Android boundary [#243](https://github.com/Conxian/conxius-enclave-sdk/pull/243), merged SDK hardening [#246](https://github.com/Conxian/conxius-enclave-sdk/pull/246) (**2026-07-22 16:36:34 UTC**), open provider-neutral contracts [#245](https://github.com/Conxian/conxius-enclave-sdk/pull/245) with current review findings [#4755943314](https://github.com/Conxian/conxius-enclave-sdk/pull/245#pullrequestreview-4755943314), merged wallet KeyMint boundary [#441](https://github.com/Conxian/conxius-wallet/pull/441), merged wallet Play Integrity request boundary [#442](https://github.com/Conxian/conxius-wallet/pull/442), and open wallet hardening follow-up [#443](https://github.com/Conxian/conxius-wallet/pull/443). These are bounded interface/containment artifacts only: they do not establish production provider verification, durable replay, real-device qualification, protocol-key custody evidence, or independent release acceptance. PR #245's current review identified unresolved policy-digest/expected-collateral binding, idempotent-vs-conflicting replay outcome, deserialization invariant, and non-production replay-store registration gaps; SDK [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240), [CON-1543](https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and), and [CON-1544](https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity) remain open prerequisite tracks, and this update does not modify PR #245. |
| SDK umbrella | [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195) |
| Shared prerequisite | [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) |
| Android track | [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) |
| AWS Nitro track | [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) |
| Merged proof verification | [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237), [#239](https://github.com/Conxian/conxius-enclave-sdk/pull/239) |
| Current rail-convergence candidate | [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244) at current head [`e3b1a69752f3e40f26b373e36ecab440c78419a9`](https://github.com/Conxian/conxius-enclave-sdk/commit/e3b1a69752f3e40f26b373e36ecab440c78419a9); follow-up review [#4755756667](https://github.com/Conxian/conxius-enclave-sdk/pull/244#pullrequestreview-4755756667) |
| Runtime/platform evidence | [CON-1517](https://linear.app/conxian-labs/issue/CON-1517/p1-harden-the-wasm-secret-boundary-and-add-runtimeplatform-evidence) |
| Independent review/release acceptance | [CON-1519](https://linear.app/conxian-labs/issue/CON-1519/p0-complete-independent-security-review-and-release-acceptance), [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) |
| Downstream business gate | [#890](https://github.com/Conxian/conxian-business/issues/890) |

## Dated Digest: CON-1421 Governance Stub Reconciliation (2026-07-21)

### Status

| Field | Record |
|-------|--------|
| Linear issue | [CON-1421 — 16 of 28 governance contracts are stubs](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs) — **In Progress** |
| Historical accounting | The issue body names 15 contracts. `proposal-engine-trait.clar` is the likely omitted 16th entry; six listed entries are partial skeletons rather than blank stubs, so the original “16 non-functional stubs” wording requires typed reconciliation. |
| Community-voting implementation | [Protocol PR #521](https://github.com/Conxian/Conxian/pull/521) is **OPEN / MERGEABLE / CLEAN** at audited head [`90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1`](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1); all currently reported checks pass and the independent re-audit reports no P0/P1 findings. State is **implemented and pinned for review**, not merged or deployed. |
| Historical umbrella | [Conxian #463](https://github.com/Conxian/Conxian/issues/463) is an OPEN / REOPENED historical umbrella. This scoped remediation does not close the broader governance gap or make the umbrella a proof of full resolution. |
| Active overlap | [Conxian #499](https://github.com/Conxian/Conxian/issues/499) remains the active overlapping scope for `upgrade-controller`, `sab-election`, and `gauge-manager`. |
| Remaining gap | `upgrade-controller.clar`, `proposal-engine-trait.clar`, and other governance gaps remain stub, partial, deferred, or separately scoped. Community voting is one reviewed remediation path, not a claim that all governance contracts are complete. |

### Projects and Records

| Entity | Type | Role / state | Evidence |
|--------|------|--------------|----------|
| `Governance remediation workstream` | Project | Reconciles the historical governance-stub inventory while preserving explicit review and deployment boundaries | [CON-1421](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs), [#463](https://github.com/Conxian/Conxian/issues/463), [#499](https://github.com/Conxian/Conxian/issues/499) |
| `conxian-business` | Parent repository | Carries the review-only `Conxian` submodule pin and this knowledge crystallization | [Parent repository](https://github.com/Conxian/conxian-business) |
| `Conxian` | Protocol repository | Supplies the audited governance implementation candidate; the parent pin is review-bound to the exact protocol commit | [Protocol repository](https://github.com/Conxian/Conxian) |
| `CON-1421` | Linear issue | Tracks the medium-priority governance inventory correction and scoped remediation; remains In Progress | [Linear issue](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs) |
| `#521` | Protocol pull request | Implements the community-voting lifecycle; open and not merged | [Protocol PR #521](https://github.com/Conxian/Conxian/pull/521) |
| `90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1` | Audited protocol commit | Exact reviewed head to pin; not a deployment or merge claim | [Protocol commit](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1) |

### Contracts / Libraries

| Entity | Type | Role / state | Evidence |
|--------|------|--------------|----------|
| `community-voting-engine.clar` | Governance contract | Escrowed, non-executing strategic voting ledger implemented on PR #521; remains under review until the PR merges | [Source at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/community-voting-engine.clar), [governance README](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/README.md) |
| `operational-treasury.clar` | Routing / treasury contract | Runtime source of truth for the `cxvg-token` and `regulatory-adapter` routes used by the voting engine | [Source at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/core/operational-treasury.clar) |
| `cxvg-token.clar` | SIP-010 governance token | Real token transferred into escrow as voting power | [Source at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/tokens/cxvg-token.clar) |
| `proposal-engine → proposal-registry → proposal-executor → timelock` | Governance contract path | Existing execution-oriented path; kept separate from the non-executing community-voting ledger | [Governance README at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/README.md) |
| `proposal-engine-trait.clar` | Governance trait / stub | Likely omitted 16th inventory entry; remains a stub and is not remediated by PR #521 | [Source at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/proposal-engine-trait.clar) |
| `upgrade-controller.clar` | Governance contract / stub | Deferred; no isolated implementation in PR #521 because upgrade routing depends on proposal/timelock plumbing and overlaps #499 | [Source at audited head](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/upgrade-controller.clar) |

### Relationships

| From | Relationship | To | Boundary / meaning |
|------|--------------|----|--------------------|
| `CON-1421` | tracks | [Protocol PR #521](https://github.com/Conxian/Conxian/pull/521) | The PR addresses one bounded governance path selected after inventory reconciliation. |
| `CON-1421` | reconciles | [Conxian #463](https://github.com/Conxian/Conxian/issues/463) | Corrects the “16 of 28” accounting without claiming full umbrella closure. |
| [Protocol PR #521](https://github.com/Conxian/Conxian/pull/521) | implements | `community-voting-engine.clar` | Functional escrowed voting lifecycle at the exact reviewed head. |
| [`90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1`](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1) | is the reviewed head of | [Protocol PR #521](https://github.com/Conxian/Conxian/pull/521) | Current candidate for the parent gitlink; PR remains open. |
| `community-voting-engine.clar` | reads routes from | `operational-treasury.clar` | Dynamic token and compliance route checks fail closed on missing or mismatched principals. |
| `community-voting-engine.clar` | escrows | `cxvg-token.clar` | Successful votes use real SIP-010 transfers into the engine. |
| `community-voting-engine.clar` | complements | `proposal-engine → proposal-registry → proposal-executor → timelock` | Voting records and settlement do not execute arbitrary proposal actions. |
| `upgrade-controller.clar` | overlaps | [Conxian #499](https://github.com/Conxian/Conxian/issues/499) | Isolated upgrade routing is deferred until the surrounding governance architecture is resolved. |
| `proposal-engine-trait.clar` | is counted as | corrected 16th governance-gap entry | The likely omitted entry is recorded without asserting that every listed item is a blank stub. |

### Decisions

| Decision | Operational meaning |
|----------|---------------------|
| Prefer community voting over isolated `upgrade-controller` work | Community voting has no production callers, documented requirements, and a complete self-contained vertical. Upgrade routing depends on proposal/timelock plumbing and overlaps the active #499 scope. |
| Record implemented behavior precisely | The reviewed engine performs dynamic operational-treasury route checks, real CXVG escrow, compliance checks, future and bounded voting windows, aggregate supply snapshot/cap enforcement, quorum and approval thresholds with strict tie failure, permissionless finalization, and historical one-time stake claims. |
| Keep the execution boundary explicit | The engine does not execute arbitrary actions or withdraw treasury assets; the existing proposal/execution path remains separate. |
| Defer reputation weighting | Voting uses raw escrowed CXVG; reputation weighting waits for a trustworthy, independently reviewed reputation source and rules. |
| Treat PR #521 as under review | The parent may pin the exact audited head for provenance, but the state remains pinned for review until PR #521 merges into `main`; no deployment claim is made. |
| Preserve typed gap states | Partial skeletons, blank stubs, implemented-but-under-review contracts, and deferred architecture must not be collapsed into one resolved count. |
| Do not close #463 by implication | One clean, audited PR does not resolve the historical or active governance backlog. |

### Risks and Gates

| Risk / gate | Current implication |
|-------------|---------------------|
| Protocol PR merge order | The parent pin must merge only with or after [PR #521](https://github.com/Conxian/Conxian/pull/521) so the gitlink remains backed by the audited provenance. |
| Broader governance completion | `upgrade-controller`, `proposal-engine-trait`, and other remaining gaps require separate design, implementation, or explicit retirement decisions. |
| Historical inventory quality | The original issue body lists 15 contracts and six listed entries are partial skeletons; a future full inventory should classify every contract rather than reuse the blanket 16-stub label. |

### Evidence Index

| Evidence | Link |
|----------|------|
| Linear issue | [CON-1421](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs) |
| Historical umbrella | [Conxian #463](https://github.com/Conxian/Conxian/issues/463) |
| Active overlapping scope | [Conxian #499](https://github.com/Conxian/Conxian/issues/499) |
| Protocol implementation PR | [Conxian PR #521](https://github.com/Conxian/Conxian/pull/521) |
| Exact protocol commit | [`90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1`](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1) |
| Parent repository | [Conxian/conxian-business](https://github.com/Conxian/conxian-business) |

---

## Typed Digest CON-1542 Conxian 538 Revenue Automation Policy Handoff 2026-07-25

### Entities

| Entity | Type | Status | Role / boundary | Canonical evidence |
|--------|------|--------|-----------------|--------------------|
| `CON-1542` | Linear governance/knowledge work item | **OBSERVED — IN REVIEW** on 2026-07-25 | Owns the business-policy handoff, evidence classification, and knowledge crystallization. It does not implement contracts or prove deployment. | [Linear issue](https://linear.app/conxian-labs/issue/CON-1542/handoff-own-and-harden-revenue-automation-policy-from-conxius-platform) |
| `Conxian/Conxian` | Protocol repository | **APPROVED SOURCE OF TRUTH** for protocol behavior | Owns protocol economics, Clarity contracts, deployment policy, and fee-bearing behavior. | [Protocol repository](https://github.com/Conxian/Conxian), [handoff #538](https://github.com/Conxian/Conxian/issues/538) |
| `Conxian/conxius-platform` | Observation/routing repository | **OBSERVED BOUNDARY** | Owns observation, routing, and runbooks; it is not a custody or protocol-economics authority. | [Platform repository](https://github.com/Conxian/conxius-platform), [merged PR #1197](https://github.com/Conxian/conxius-platform/pull/1197) |
| `Conxian/conxian-business` | Governance/knowledge repository | **APPROVED CLASSIFICATION BOUNDARY** | Owns governance records, knowledge crystallization, and evidence classification; it does not implement protocol contracts. | [Business repository](https://github.com/Conxian/conxian-business) |
| Protocol PR #544 | Canonical collector change | **MERGED** on 2026-07-22 | Adds the scheduled protocol fee collector and its protocol-source behavior. | [Conxian PR #544](https://github.com/Conxian/Conxian/pull/544) |
| Protocol PR #556 | Lending migration change | **MERGED** on 2026-07-23 | Migrates lending-interest collection to the canonical collector. | [Conxian PR #556](https://github.com/Conxian/Conxian/pull/556) |
| Protocol PR #572 | DEX hardening change | **OPEN** on 2026-07-25 at [`6d2f66ec5c6927bd05f2d668d03f366532ec46b6`](https://github.com/Conxian/Conxian/commit/6d2f66ec5c6927bd05f2d668d03f366532ec46b6) | Proposes fail-closed DEX behavior when segregated fee custody is unavailable; it does not transfer unsegregated LP/user balances. | [Conxian PR #572](https://github.com/Conxian/Conxian/pull/572) |
| Actual DEX fee settlement | Protocol capability | **UNRESOLVED** | Requires asset-segregated custody and a verified transfer path in the protocol repository. | [Conxian #538](https://github.com/Conxian/Conxian/issues/538), [legacy defect #469](https://github.com/Conxian/Conxian/issues/469) |
| Live deployment and revenue realization | Operational evidence class | **UNRESOLVED** | Requires independent deployment and on-chain execution evidence; code, plans, routing, and observation records are insufficient. | [Conxian #538](https://github.com/Conxian/Conxian/issues/538) |
| Historical 0.1% founder carve-out | OpenSpec proposal | **PROPOSAL-ONLY / GOVERNANCE-GATED** | Preserved as historical context; CON-1542 does not approve or activate any beneficiary, custody route, rate, or allocation semantics. | [Launch mechanics proposal](openspec/changes/csf-autonomous-launch/specs/launch-mechanics/spec.md) |

### Relationships

| From | Relationship | To | Status / meaning |
|------|--------------|----|------------------|
| `CON-1542` | hands protocol-policy ownership to | [`Conxian/Conxian`](https://github.com/Conxian/Conxian) | **APPROVED BOUNDARY:** protocol economics and implementation remain in the protocol repository. |
| [`Conxian/conxius-platform`](https://github.com/Conxian/conxius-platform) | observes/routes | protocol revenue evidence | **OBSERVED ONLY:** merged [PR #1197](https://github.com/Conxian/conxius-platform/pull/1197) does not create custody, economics, deployment, or realization authority. |
| [`Conxian/conxian-business`](https://github.com/Conxian/conxian-business) | classifies/governs evidence for | [Conxian #538](https://github.com/Conxian/Conxian/issues/538) | **APPROVED BOUNDARY:** records policy and claim states without implementing contracts. |
| [Protocol PR #544](https://github.com/Conxian/Conxian/pull/544) | provides | canonical scheduled collector | **MERGED:** source evidence, not deployment evidence. |
| [Protocol PR #556](https://github.com/Conxian/Conxian/pull/556) | migrates | lending-interest collection | **MERGED:** source evidence, not proof of live lending revenue. |
| [Protocol PR #572](https://github.com/Conxian/Conxian/pull/572) | hardens | unavailable DEX fee custody | **OPEN:** fails closed instead of transferring unsegregated balances; not merged or deployed. |
| Actual DEX settlement | remains blocked by | missing segregated fee custody and verified transfer semantics | **UNRESOLVED:** no actual DEX revenue claim. |
| Deployment/live revenue claim | requires | independent on-chain realization evidence | **UNRESOLVED:** no inference from source, plan, routing, or observation artifacts. |
| Historical founder carve-out | requires before activation | separate ratified governance | **GOVERNANCE-GATED:** beneficiary, custody, rate, and allocation semantics must all be defined outside CON-1542. |

### Decisions

| Decision | Status | Operational meaning |
|----------|--------|---------------------|
| Protocol behavior source of truth is `Conxian/Conxian` | **APPROVED** | Clarity, deployment policy, fee-bearing behavior, and protocol economics are not owned by platform observation or business documentation. |
| Never infer production realization from code, plans, routing, or observation | **APPROVED** | “Merged,” “planned,” and “observed” remain distinct from “deployed” and “live revenue.” |
| Never transfer from unsegregated DEX balances | **APPROVED** | Any balance that may contain LP or user assets must not be treated as protocol fees; unsupported custody paths fail closed. |
| Never apply additive legacy and canonical charges to one fee base | **APPROVED** | Migration must not double-charge the same economic event. |
| No founder allocation through CON-1542 | **APPROVED** | The historical 0.1% language is proposal-only and cannot activate without separate ratified governance defining beneficiary, custody, rate, and allocation semantics. |
| Do not pin the parent repository to PR #572 | **APPROVED** | The open DEX hardening commit remains protocol-review evidence only; this digest makes no submodule change. |

### Evidence Classification Rules

| Classification | Meaning in this digest |
|----------------|------------------------|
| **OBSERVED** | State checked from the canonical external system; observation alone grants no protocol authority. |
| **APPROVED** | Governance or ownership boundary adopted by this business-policy handoff. |
| **MERGED** | Change is present in the target repository's default branch; deployment and execution remain separate claims. |
| **OPEN** | Change is under review and must not be described as merged, deployed, or live. |
| **UNRESOLVED** | Required implementation or independent operational evidence is absent. |
| **PROPOSAL-ONLY / GOVERNANCE-GATED** | Historical design context with no activation authority absent separate ratified governance. |

### Risks and Gates

| Risk / gate | Current implication |
|-------------|---------------------|
| DEX asset commingling | No settlement transfer may use balances that are not demonstrably segregated from LP/user assets. |
| Review-state inflation | PR #572 and commit `6d2f66ec5c6927bd05f2d668d03f366532ec46b6` remain open review evidence only. |
| Revenue-claim inflation | Merged collectors, plans, and observation records do not establish deployment or live revenue. |
| Fee-base duplication | Legacy and canonical collection paths must not both charge the same fee base. |
| Founder allocation ambiguity | No allocation may activate until separate governance ratifies beneficiary, custody, rate, and allocation semantics. |

### Evidence Index

| Evidence | Link | Classified status |
|----------|------|-------------------|
| Linear handoff | [CON-1542](https://linear.app/conxian-labs/issue/CON-1542/handoff-own-and-harden-revenue-automation-policy-from-conxius-platform) | **OBSERVED — IN REVIEW** |
| Protocol handoff | [Conxian #538](https://github.com/Conxian/Conxian/issues/538) | **OBSERVED — OPEN** |
| Legacy defect | [Conxian #469](https://github.com/Conxian/Conxian/issues/469) | **OBSERVED — CLOSED**, not proof that every settlement/deployment gap is resolved |
| Canonical collector | [Conxian PR #544](https://github.com/Conxian/Conxian/pull/544) | **MERGED** |
| Lending migration | [Conxian PR #556](https://github.com/Conxian/Conxian/pull/556) | **MERGED** |
| DEX fail-closed hardening | [Conxian PR #572](https://github.com/Conxian/Conxian/pull/572) | **OPEN** |
| Exact open DEX hardening commit | [`6d2f66ec5c6927bd05f2d668d03f366532ec46b6`](https://github.com/Conxian/Conxian/commit/6d2f66ec5c6927bd05f2d668d03f366532ec46b6) | **OPEN REVIEW EVIDENCE** |
| Platform observation boundary | [conxius-platform PR #1197](https://github.com/Conxian/conxius-platform/pull/1197) | **MERGED / OBSERVATION ONLY** |

---

## Maintenance

**Crystallization Rule:** Every agent session MUST update this document with:
1. New entities discovered
2. Relationship changes
3. Decision outcomes
4. Issue resolutions

**Verification:** Cross-reference claims against this graph before acting.

---

*Generated per AGENTS.md Knowledge Management mandate*
*Next update: After Phase 1 remediation (Week 2)*
