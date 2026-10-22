# Dependency Purge & Strategic Boundary Audit (Session 70 — October 2026)

## Executive Summary

Pursuant to the Conxian Org-Wide Research & Expansion Mandate, an exhaustive codebase and dependency audit was executed across the core modular stack (`conxian-nexus`, `conxian-gateway`, `conxius-enclave-sdk`, `conxius-platform`, `lib-conxian-core`, `conxian_market`).

This audit confirms that the Conxian ecosystem is strictly anchored to **Bitcoin L1 (Native UTXO, Lightning, RGB, Babylon, FROST, OP_CAT)** with **Zero Protocol Tokens, Zero Custom Tokenomics, and Zero Staking/Liquidity Token Logic**.

---

## 1. Dependency Purge & Legacy Token Inspection

### Audited Repositories
1. `conxian-nexus`
2. `conxian-gateway`
3. `conxius-enclave-sdk`
4. `conxius-platform`
5. `lib-conxian-core`

### Audit Results: Dependency Purge Baseline
- **Custom Native Token / Speculative Token Logic**: **0 Found** (Strictly Prohibited).
- **Legacy Stacks Tokenized Assumptions**: **Purged / Non-Existent**. Stacks logic is strictly limited to Bitcoin L2 contract interaction without speculative token dependencies.
- **EVM Native Token / ERC-20 Dependencies**: **0 Found**. EVM support is strictly scoped to x402 / EIP-712 payment attestation and cross-chain hashlock settlement.
- **Bitcoin L1 Focus**: All state verification, transaction building, and cryptographic proof envelopes are anchored to Bitcoin UTXO finality and Schnorr/Taproot/FROST signatures.

---

## 2. Strategic Boundary Architectural Mapping (.org vs .com)

| Repository | Public Open-Source Protocol Boundary (`conxian.org`) | Commercial Enterprise Surface (`conxian-labs.com`) |
| :--- | :--- | :--- |
| **`conxian-nexus`** | Universal ZK state verifier node, open SP1/RISC Zero zkVM proving adapters, stateless public good (`nexus.conxian.org`). | High-availability managed Nexus node clusters, SLA-backed instance pooling (99.5% uptime), multi-tenant attestation (`bos.conxian-labs.com`). |
| **`conxian-gateway`** | Open-core RPC, REST, and WebSocket transport bridge, basic tokenless CJCS v2.0 intent routing (`gateway.conxian.org`). | ISO 20022 message translation engine (`pacs.008`, `pacs.002`, `camt.053`), commercial API rate limiting, multi-tenant API key auth, SOC2 audit logging. |
| **`conxius-enclave-sdk`** | Open-source client-side SDK for non-custodial key isolation, FROST threshold signing, Android StrongBox TEE, and AWS Nitro attestation (`sdk.conxian.org`). | Bespoke enterprise HSM & KMS integrations, institutional enclave policy auditing, white-glove security reviews. |
| **`conxius-platform`** | Public JSON schemas for platform manifest, service catalogs, and open-source deployment specifications (`platform.conxian.org`). | Multi-tenant cluster deployment orchestrator, load-balanced SLA node management, admin control plane (`services/admin-dashboard`). |

---

## 3. Scaffolding & Code Deliverables Summary

1. **`conxian-nexus`**:
   - `src/verification/zkvm.rs`: SP1 and RISC Zero 2026 zkVM proof environment adapters for Bitcoin state verification.
   - `ARCHITECTURE.md`: Explicit `.org` vs `.com` boundary specification.

2. **`conxian-gateway`**:
   - `internal/compliance/src/iso20022.rs`: Field-level ISO 20022 (`pacs.008`, `pacs.002`, `camt.053`) to CJCS v2.0 translation engine.
   - `internal/api/src/middleware.rs`: Commercial API key authentication middleware (`cxn_live_`, `cxn_test_`, `cxn_agent_`, `cxn_sub_`).
   - `ARCHITECTURE.md`: Commercial gateway boundary specification.

3. **`conxius-enclave-sdk`**:
   - `src/enclave/strongbox_tee.rs`: Android StrongBox Keymaster/KeyMint TEE driver for hardware-isolated signing.
   - `ARCHITECTURE.md`: Non-custodial hardware boundary specification.
   - `CHANGELOG.md`: Release hygiene version alignment [2.1.0].

4. **`conxius-platform`**:
   - `platform/sla_node_orchestrator.json`: JSON schema for multi-tenant enterprise SLA Nexus node orchestration.
   - `services/admin-dashboard/src/lib/sla_orchestration.ts`: TypeScript SLA node orchestrator client.
   - `ARCHITECTURE.md`: Platform control plane boundary specification.
