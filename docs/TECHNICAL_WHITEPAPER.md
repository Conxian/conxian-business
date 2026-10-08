# Conxian: A Sovereign-First Financial Operating System for Bitcoin

**Version**: 2.0.0-draft
**Status**: Technical whitepaper (single authoritative technical artifact)
**Last verified against code**: 2026-10-03
**Source of truth**: this document supersedes the vision-level `conxius-platform/docs/WHITEPAPER.md` and the `TECHNICAL_WHITEPAPER_OUTLINE.md` from which it is derived.

> **Reading guide.** Every claim in this paper is classified using the org's trust taxonomy — **Implemented** (code exists, CI enforces it), **Verified** (implemented + independently checked), **Production-ready** (verified + deployed with monitoring/rollback), **Target-state** (designed/spec'd, not yet built), **Experimental** (built with known gaps). Claims without a pointer are explicitly labeled aspirational. Evidence paths point to actual source, not prose.

---

## Abstract

Conxian is a sovereign-first, non-custodial financial operating system built directly on Bitcoin and Stacks. It binds enterprise financial operations to on-chain truth through three code-verified primitives: a **Business Operating System (BOS)** that expresses governance and treasury workflows as a programmatic state machine; **hardware-enforced sovereignty** (TEE/StrongBox/Nitro attestation, threshold FROST/MuSig2 signing); and **Zero Secret Egress** — sensitive logic isolated in enclaves and vaults, with public repos fail-closed on contamination. The execution layer (Nexus) synchronizes 10+ protocol families with Merkle-Mountain-Range state proofs and a 53-route REST/gRPC surface; the compliance layer (Gateway) maps enterprise ERP traffic to ISO 20022 with zero-knowledge compliance; the client layer (Conxius Wallet) keeps keys in Android StrongBox. This paper states the system's five-plane architecture, its threat model, what is implemented versus target-state, and its known limitations.

---

## 1. Introduction & Motivation

### 1.1 The Sovereignty Gap

Bitcoin solved *monetary* sovereignty: it lets any party hold value without a custodian. It did not solve *operational* sovereignty — the running of a financial business. Enterprises that want to build on Bitcoin today face three forced trade-offs:

1. **Custodial by default.** The common path to Bitcoin-native operations routes through an exchange, a hosted gateway, or a managed key service — reintroducing the centralized trust anchor Bitcoin was built to remove.
2. **Centralized operational logic.** Reconciliation, compliance, treasury, and settlement workflows live in private databases and opaque SaaS, so "what the business did" is not provable to a third party.
3. **No bridge between enterprise systems and chain truth.** SAP/Oracle-style ERP environments speak ISO 20022 and OData; Bitcoin speaks transactions and proofs. The translation layer is where most "enterprise crypto" products collapse into a trusted middleman.

Conxian's position is that these three gaps are one gap — the absence of a *sovereign operations layer* — and that it is solvable with code, hardware, and cryptography rather than with a counterparty.

### 1.2 Design Philosophy

Four invariants govern the system and are enforced, not aspirational:

- **Sovereignty by Design.** Private keys never leave the user's or operator's hardware. Signing is hardware-bound (StrongBox/TEE/Nitro) or threshold-distributed (FROST/MuSig2), never software-exposed.
- **Zero Secret Egress (ZSE).** No sensitive operational, strategy, or financial material is tracked in the active Git index. Sensitive logic lives in enclaves and restricted vaults; public repositories contain only fail-closed stubs and proof primitives. *(Evidence: `docs/BOUNDARY_DECISION_LOG.md`, `scripts/verify_knowledge_retention.py`.)*
- **Fail-Closed.** Every privileged workflow must prove its validity or abort with a durable error state. There is no "best effort" path for custody-critical operations. *(Evidence: the `ProductionRuntimeGuard.failClosed` pattern in the wallet; `ORACLE_SERVICE_IS_STUBBED` fail-closed config in Nexus.)*
- **Open-Core.** Protocol primitives, verification logic, and state-proof code are public and reviewable; operational runbooks and secret material are not.

### 1.3 Scope

**Covered:** system architecture (five planes, three lanes), the BOS state machine, the security/threat model, the protocol/execution/compliance/client layers, and an honest implementation-maturity matrix.

**Not covered:** API reference, deployment runbooks, pricing, secret management, and forward-looking roadmap commitments beyond what is labeled target-state.

---

## 2. System Architecture

### 2.1 The Five-Plane Model

The runtime is decomposed into five planes with distinct trust roles. This is the canonical model from `docs/architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md` (CON-455).

| Plane | Role | Trust authority |
|---|---|---|
| **Settlement + policy** | Bitcoin L1 (settlement), Stacks (execution), protocol-neutral rails/adaptors (policy/timelocks/state roots via `lib-conxian-core` `SettlementRail`/`TrustTier`) | On-chain — canonical truth |
| **Proof** | `lib-conxian-core` SNARK/state-proof verification (BitVM bridge verification, MMR commitments) | Cryptographic |
| **Data** | BOS orchestrator, Gateway (ingress/broadcast boundary), Nexus (indexing/projection), oracle publishers | Derived, non-authoritative |
| **Control** | deploy/upgrade, key rotation, identity/authorization, policy gates | Operator root (MS/HSM/DAO/SAB signer boundary) |
| **Derived / UX** | dashboards, public web, non-custodial wallets | Consumers only — never correctness/custody anchors |

**Core invariants** (hold in every deployment lane):

1. Canonical truth is on-chain; all off-chain stores are derived.
2. No dashboard-to-contract coupling — dashboards never hold signing keys or broadcast value-bearing transactions.
3. Dynamic principals — privileged workflows resolve principals via `operational-treasury.clar`, never hardcoded addresses.
4. Signed, replay-resistant events — correctness/custody-impacting workflows are signed envelopes.
5. Fail closed — unverifiable privileged workflows abort with a durable error.

### 2.2 Three Deployment Lanes

One architecture, three custody/ownership profiles:

- **Community sovereign-node** — self-hosted, bring-your-own runtime.
- **Business-managed** — managed hosting with shared controls.
- **Enterprise / private-cloud** — customer-operated control plane and data plane.

Lane-specific choices are limited to control-plane ownership, custody boundaries, and infrastructure placement; protocol correctness is identical across lanes.

### 2.3 Cross-Chain State Verification

Nexus commits to off-chain state using **Merkle Mountain Range (MMR)** roots and verifies Bitcoin-side state with **BitVM Groth16** verification. *(Evidence: `conxian-nexus/src/state/mod.rs`, `src/sync/mod.rs`, `src/executor/bitvm_groth16.rs`, `src/executor/canonical_bitvm.rs`.)* Protocol adapters normalize state across EVM (receipts), Cosmos (IBC updates), and Stacks (transactions). *(Evidence: `conxian-nexus/src/executor/{evm,cosmos,stacks}.rs`.)*

### 2.4 Ecosystem Repository Map

| Repo | Role | Language |
|---|---|---|
| `lib-conxian-core` | Shared protocol + crypto primitives, fee model, ERC-7683 intents | Rust |
| `conxius-enclave-sdk` | Hardware enclave abstractions, attestation, threshold signing | Rust |
| `conxian-gateway` | Compliance/ingress layer (ISO 20022, ZKC) | Rust |
| `conxian-nexus` | Execution + proof layer (multi-protocol node) | Rust |
| `conxius-wallet` | Non-custodial client (Android) | TypeScript/Kotlin |
| `conxius-platform` | Control-plane / dashboard scaffolding | TypeScript |
| `conxian_market` | AI-labor settlement + escrow SDK | TypeScript |
| `conxian-business` | Governance, CI/CD, specification surface | Python |

*(Evidence: `docs/REPO_PORTFOLIO.md`.)*

---

## 3. The BOS: Business Operations as a State Machine

The BOS turns "how the business runs" into a programmatic state machine with cryptographic proof of correct operation.

### 3.1 Unified Theory v2.0

The deployment of capital, time, and code is governed by four variables (plus network effects). *(Evidence: `docs/CONXIAN_UNIFIED_THEORY_v2.md`.)*

- **C_R (Cost of Reproduction)** — structural moat: TEE/StrongBox coverage, protocol-neutral rail/adaptor complexity, compliance integration, ERP stickiness.
- **O_C (Opportunity Cost)** — founder/operator manual hours on critical-path workflows.
- **V_X (Execution Velocity)** — AI/tooling leverage on shipped scope.
- **A_S (System Autonomy)** — fraction of recurring operations run by the BOS without human intervention.
- **N_E (Network Effects)** — per-participant uplift from adoption.

Four-phase lifecycle, with the governing ratios:

$$V_{base} = \frac{C_R}{O_C} \qquad V_{dev} = \frac{C_R \times V_X}{O_C} \qquad V_{ops} = \frac{C_R \times A_S}{O_C} \qquad \text{Total} = (C_R \times A_S)^{N_E}$$

The operational target is driving $O_C \to 0$: any recurring workflow that requires daily manual oversight is an autonomy failure.

### 3.2 Programmatic Governance

- **Promotion pipeline** `dev → staged → main` with CI enforcement; PRs into `main` require a Mainnet Acceptance Evidence Pack.
- **Contamination guard** — production-track `.clar` files are scanned for testnet/simnet principals; a violation breaks the build.
- **Sovereign-first deployment** — contracts resolve principals dynamically via `operational-treasury.clar`, never hardcoded.

*(Evidence: `scripts/branch_promotion_policy.py`, `scripts/verify_contamination_guard.py`, `docs/BRANCH_AND_PROMOTION_STANDARD.md`.)*

### 3.3 Operational Metrics

The variables are instrumented with defined formulas and data contracts. *(Evidence: `docs/operations/CON-682_APPROVED_METRIC_SPEC.md`.)*

- **C_R** = `0.35·TEE + 0.25·ProtocolComplexity + 0.20·Compliance + 0.20·IntegrationStickiness` (0–100).
- **O_C** = sum of manual hours on founder-critical paths.
- **V_X** = completed weighted scope / median cycle time.
- **A_S** = automated recurring runs / total recurring runs (guardrail: ≥99.5% reconciliation, ≤15m autonomous recovery).
- **N_E** = average participant uplift over a trailing 30d window.

---

## 4. Security & Trust Model

### 4.1 Threat Model (adversary assumptions)

Conxian assumes the following adversary, stated up front:

1. **A network attacker** who can observe and tamper with traffic but cannot extract hardware-bound private keys.
2. **A compromised operator device** — a device whose OS or application layer is malicious, but whose TEE/StrongBox-backed keys remain non-exportable.
3. **A malicious or buggy internal workflow** — code or an operator that attempts to sign a value-bearing transaction without authorization.
4. **A dishonest counterparty** in a cross-chain exchange.

**Honest assumptions.** On-chain finality relies on Bitcoin's honest-majority assumption. Threshold signing assumes no more than the threshold of signers is simultaneously compromised (FROST 2-of-3).

**Residual risk (acknowledged).** Software-only enclave abstractions (`android_strongbox.rs` `SOFTWARE_ONLY = true`) and the TPM path (marked `…unavailable.v1`) are **not** production security boundaries — they are development stand-ins for the hardware-backed implementations in the Android wallet and Nitro. See §9.2.

### 4.2 Cryptographic Sovereignty

- **Hardware-backed identity** — enterprise device/workload keys are non-exportable and held in TPM/TEE/HSM-class hardware. *(Evidence: `docs/architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md`.)*
- **Attestation-gated access** — privileged surfaces require a verifiable attestation chain (key origin + device posture) before session issuance; failure fails closed.
- **Short-lived, capability-scoped sessions** — no bearer tokens for privileged surfaces; proof-of-possession (mTLS/DPoP) binding.
- **Nitro attestation** — AWS Nitro Enclave attestation documents verified offline (COSE + PCR + root-CA trust chain). *(Evidence: `conxius-enclave-sdk/src/enclave/nitro.rs`, `src/enclave/verifiers/nitro_verifier.rs`.)*
- **Threshold signing** — FROST 2-of-3 and MuSig2 for value-bearing signing. *(Evidence: `conxius-enclave-sdk/src/protocol/frost_crypto.rs`, `musig2.rs`.)*

### 4.3 Zero Secret Egress (ZSE)

Three layers: secrets → restricted vault/Supabase; on-chain → state-proof primitives only; public stubs → fail-closed (`err-u501`/`err-u503`). The contamination guard breaks builds on testnet-principal leakage in production contracts. *(Evidence: `docs/BOUNDARY_DECISION_LOG.md`.)*

### 4.4 Trust Boundaries — what is and is not claimed

**Claimed:** verifiable CI pipeline, ZSE compliance, cryptographic proof of state, honest maturity labeling.

**Not claimed:** third-party security audits, production SLAs, full decentralization, or payable bug bounties. The enclave SDK is **Beta/conditional**: build success, API presence, and simulated paths are not production-support evidence.

*(Evidence: `docs/TRUST_AND_READINESS_VERIFICATION.md`.)*

### 4.5 Supply Chain Integrity

- Submodule pin integrity audit (daily).
- GitHub Actions pinned to commit SHAs.
- `cargo audit` / Dependabot in CI.

---

## 5. Protocol Layer: ConxianCSF

### 5.1 Smart Contract Architecture

> **Status: Target-state / re-architecting.** The original ConxianCSF Clarity contract set (16+ contracts: `bridge-nft`, `yield-optimizer`, `payment-forge`, `operational-treasury`, …) lived in the `Conxian` repository, which has been deprecated and removed from GitHub. The surviving on-chain surface is smaller and is being re-architected under the **Sovereign Redesign (2026)**.

Currently present in-tree: two Clarity contracts (`dlc-bond` — a SIP-010 DLC bond token with subscribe/coupon/claim/redeem/default lifecycle; `jurisdictional-sharding`) plus `lib-conxian-core`'s `contract_bridge.rs`, `control_model/`, and `fee.rs` primitives. *(Evidence: `Fiscal-Vault-Oracle/dlc-bond.clar`, `Sovereign-Strategy-Nexus/contracts/jurisdictional-sharding.clar`, `lib-conxian-core/src/contract_bridge.rs`.)*

### 5.2 Oracle System

Nexus publishes a **Purchasing-Power-Parity (PPP) FX oracle**: it fetches universal FX rates and pushes signed state updates to a Stacks contract via `ContractBridge::create_signed_call`, signed by a real (non-ephemeral) wallet. *(Evidence: `conxian-nexus/src/oracle/aggregator.rs` — `PppState`, `update-fx-rates`, `signer_stacks_address`.)*

> **Correction vs. earlier wording.** The vision whitepaper described a "Decentralized Risk Oracle" emitting cryptographically signed "Risk Proofs." The implemented oracle is a **PPP FX price oracle**; risk-scoring as a first-class signed artifact is not implemented. This paper does not claim it is.

### 5.3 Fiscal Vault & Treasury

Sovereign treasury with yield optimization and compliance gating, following the no-dashboard-to-contract-coupling invariant. *(Evidence: `docs/architecture/BOS_TREASURY_AND_YIELD_INTEGRATION_ARCHITECTURE.md`.)*

### 5.4 Mainnet Readiness

**Conditional Go** — pending ALEX funding verification; all P0 blockers (admin centralization, ST→SP, secret cleanup) remediated. No payout-ready commitments until ConxianCSF deploys via the ALEX path. *(Evidence: `docs/CSF_MAINNET_READINESS_GATE.md`.)*

---

## 6. Execution Layer: Conxian Nexus

### 6.1 Multi-Protocol Engine

Nexus normalizes and verifies state across protocol families through adapters: **Bitcoin (BitVM3 Groth16), EVM, Cosmos (IBC), Stacks, Lightning, RGB, Fedimint, Aptos, Solana, Sui.** *(Evidence: `conxian-nexus/src/executor/{bitvm3,evm,cosmos,stacks,lightning,rgb,fedimint,aptos,solana,sui}.rs`.)* State roots are committed via MMR.

### 6.2 API Surface

- **REST**: 53 route paths including `/proof-envelope`, `/bitvm3`, `/attestations`, `/frost`, `/safety-mode`, `/governance/decision`, `/promotion-evidence/{release}`, `/health`, `/drift`, `/cet/verify`. *(Evidence: `conxian-nexus/src/api/rest.rs`.)*
- **gRPC**: tonic/prost gateway. *(Evidence: `conxian-nexus/src/api/grpc.rs`.)*
- **Admin API**: CRUD, diagnostics, public auth metadata.

> **Note.** Earlier docs cited "18 routes incl. `/v1/proof` and `/v1/bitvm2/verify-state-root`." The current surface is larger (53) and renamed (BitVM2→BitVM3, `/v1/proof`→`/proof-envelope`). This paper reflects the current code.

### 6.3 Storage Layer

Decentralized SQL (Kwil) and sharded persistence (Tableland) with safety-mode circuit breakers. *(Evidence: `conxian-nexus/src/storage/`, `src/safety/`.)*

---

## 7. Compliance Layer: conxian-gateway

### 7.1 ISO 20022 Integration

The Gateway maps enterprise traffic to ISO 20022 and provides **Zero-Knowledge Compliance (ZKC)** — proving compliance without exposing raw data. *(Evidence: `conxian-gateway/internal/compliance/src/zkc.rs`, `internal/api/src/camt.rs`, `internal/api/src/a2p.rs`.)* The "Sentinel" secret filter and JWT/enclave auth live in `internal/api/src/auth.rs`; tiered institutional access is expressed in `pkg/conxian-core/src/trust_policy.rs`.

> **Correction vs. earlier wording.** The outline specified "pacs.008 wrapping." The implemented message set is **camt** (cash-management); pacs.008 appears only as a settlement reference. This paper reflects the implemented camt surface.

### 7.2 Cross-Border Settlement

x402 settlement pipeline and cross-fiat pricing are implemented in `pkg/conxian-core/src/settlement.rs` and `conxian-nexus/src/verification/x402.rs`.

> **Correction.** The "Global Liquidity Mesh" (cross-chain atomic swaps via HTLC state machines) is **research/target-state**, not implemented. It appears only in research notes (`conxian-gateway/docs/research/`), not in engine code. Swap-adjacent code today is Stacks ALEX/DEX integration and NTT relaying, which is not the same as a general HTLC mesh.

---

## 8. Client Layer: Conxius Wallet

### 8.1 Sovereign-First Wallet

Android-first, offline-first, non-custodial. Keys are generated and held in **Android StrongBox / KeyMint** hardware. *(Evidence: `conxius-wallet/android/core-crypto/.../StrongBoxManager.kt`, `KeyMintAuthorizationManager.kt`.)* Intent review is a real gate (`services/value-operation-gate.ts`): the UI can express user intent but can never authorize by itself.

### 8.2 Protocol Integration

| Layer | Status (code-verified) |
|---|---|
| Bitcoin L1 | **Implemented** |
| Lightning (Breez SDK, BOLT 11/12) | **Experimental** — `ProductionRuntimeGuard.failClosed`; no live Breez backend |
| Liquid & Stacks | **Partial** — address derivation + fee APIs real; native signing fail-closed |
| BOB & RSK (EVM L2) | **Partial** — RSK fee/network real; BOB cosmetic; native bridge fail-closed |
| RGB | **Experimental** — schema types present; validation `failClosed` |
| Ark & state chains | **Experimental** — types only |
| Babylon staking & DLC | **Experimental** — read-only stats; staking tx fail-closed |

> **Honest labeling.** The wallet's breadth is real at the type/surface level, but several integrations are fail-closed stubs, not production paths. This is deliberate (fail-closed is the ZSE default) and is stated here to avoid over-claiming.

### 8.3 Security Model

The "CXN Guardian" is currently an AI assistant persona (`services/gemini.ts`), **not** a deployed privacy-preserving transaction guardian. The actual security boundary is the hardware-backed intent-signing gate (§8.1), which is real.

---

## 9. Implementation Maturity

### 9.1 Current State by Component

| Component | Status | Basis |
|---|---|---|
| Conxius Wallet | **Stable** (v1.9.x) | StrongBox/KeyMint real; broad protocol surface partial/experimental |
| Conxian Nexus | **Beta** | 53 routes, 10+ adapters, MMR, x402, gRPC all implemented; oracle = PPP FX |
| conxian-gateway | **Beta** | camt ISO 20022 + ZKC + Sentinel + trust_policy implemented |
| lib-conxian-core | **Stable** | fee model (`fee.rs`), ERC-7683, crypto, control_model implemented |
| conxius-enclave-sdk | **Beta/conditional** | Nitro attestation + FROST/MuSig2 verified; StrongBox software-only; TPM unavailable |
| ConxianCSF (protocol) | **Target-state / re-architecting** | original `Conxian` repo removed; 2 contracts + core primitives survive |
| conxian_market | **Implemented but isolated** | 19-module SDK, unpublished/unconsumed |

### 9.2 Known Limitations & Open Problems

1. **Protocol layer re-architecture.** The Clarity contract set is being rebuilt; the "16+ contracts" of prior docs no longer reflect a live repository.
2. **Wallet protocol depth.** Lightning/RGB/Ark/Babylon are fail-closed stubs; production support requires the native backends.
3. **Enclave software paths.** `SOFTWARE_ONLY` StrongBox and `unavailable.v1` TPM are development stand-ins; they are not security boundaries.
4. **Risk oracle** (signed risk scoring) is not implemented; only the PPP FX oracle is.
5. **Global Liquidity Mesh** (HTLC atomic swaps) is research, not code.
6. **ISO 20022 scope** is camt, not the full pacs family.
7. **Third-party audit gap.** No independent security audit is claimed; the enclave SDK's independent review and real-device evidence remain open.

---

## References / Evidence Index

- Architecture: `docs/architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md`
- Theory: `docs/CONXIAN_UNIFIED_THEORY_v2.md`
- Trust/readiness: `docs/TRUST_AND_READINESS_VERIFICATION.md`
- Metrics: `docs/operations/CON-682_APPROVED_METRIC_SPEC.md`
- Mainnet gate: `docs/CSF_MAINNET_READINESS_GATE.md`
- Identity: `docs/architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md`
- Treasury: `docs/architecture/BOS_TREASURY_AND_YIELD_INTEGRATION_ARCHITECTURE.md`
- Code (as cited inline): `conxian-nexus/src/**`, `conxian-gateway/internal/**` and `pkg/**`, `lib-conxian-core/src/**`, `conxius-enclave-sdk/src/**`, `conxius-wallet/**`.

---

© 2026 Conxian Labs. This document is public-safe and contains no secret material.
