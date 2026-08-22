# BOS Runtime Ownership Map
**Version:** v1.1 (August 2026)
**Status:** CANONICAL REFERENCE

> **Autonomy boundary (2026-08-22):** BOS is not certified for full M2M/autonomous execution. Capability-scoped evidence and unresolved blockers are tracked in `audit/m2m_autonomy_gap_ledger.json`; the safe lab is local/isolated-testnet-only and forbids production execution.

This document maps the Conxian Sovereign BOS capabilities to their respective runtime repositories. It distinguishes between conceptual documentation, public-safe stubs (ZSE), and actual production implementation.

## 1. Core Operating Suite (EXCO)

| Capability | Primary Repository | Responsibility | Implementation Status |
| :--- | :--- | :--- | :--- |
| **Strategy Nexus** | `conxian-nexus` | High-level orchestration, State Roots (MMR), Dec. Storage (Kwil/Tableland). | Production (v0.5.1) |
| **Sovereign Gateway** | `conxian-gateway` | x402 Mandates, Bitcoin/Stacks RPC Pooling, ZKML compliance pipe. | Production (v0.1.1) |
| **Fiscal Vault** | `Fiscal-Vault-Oracle` | Treasury management, DLC Bonds, Yield execution logic. | Active |
| **Nakamoto Guardian** | `Nakamoto-Guardian` | Policy enforcement, Compliance auditing, Anti-fragility monitoring. | Active |

## 2. Shared Libraries & SDKs

| Capability | Repository | Purpose | Implementation Status |
| :--- | :--- | :--- | :--- |
| **`conxius-enclave-sdk`** | `conxius-enclave-sdk` | Cross-platform security primitives (TEE, StrongBox, Musig2). | **Beta / conditional** — [July 20 audit](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md); no value-bearing production signing or settlement |
| **Sovereign Core** | `lib-conxian-core` | Shared models for BitVM2, CJCS, and gateway engine components. | Stable (v1.9.3) |

## 3. Interfaces & Platforms

| Capability | Repository | Audience | Implementation Status |
| :--- | :--- | :--- | :--- |
| **Conxian UI** | `conxian-ui` | Sovereign Operators | Active |
| **Conxius Wallet** | `conxius-wallet` | Retail/Mobile Users | Beta (Native-Track) |
| **Sovereign Platform** | `conxius-platform` | Developers & Ecosystem | Active |
| **BOS Operations** | `conxian-business` | Commercial, Legal, and Platform Specs (ZSE Stubs). | Canonical Reference |

## 4. Production Boundaries & Branch Policy

- **Main Branch (`main`)**: Strictly mainnet-ready, production-track code. Must pass all Contamination Guard checks.
- **ZSE Compliance**: Strategic material, PII, and sensitive secrets are NEVER committed. Use Linear stubs for strategic continuity.
- **Artifact Hygiene**: Generated binaries, `node_modules`, and local logs are excluded via global `.gitignore`.

---
*Maintained by Jules. Directly addresses CON-615.*
