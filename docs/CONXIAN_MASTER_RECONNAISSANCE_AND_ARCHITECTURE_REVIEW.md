# Conxian Master Reconnaissance & Architecture Review (2026)

**Classification:** Confirmed Sovereign Architecture Specification & Reconnaissance Report
**Date:** September 2026
**System Version Alignment:** BOS v1.9.5
**Author:** Lead Systems Engineer (Jules AI)

---

## Executive Summary & B2B Infrastructure Mandate

Conxian is a **pure Deep-Tech B2B infrastructure vendor** specializing in hardware-secured, memory-safe sovereign infrastructure for Bitcoin Layer 1 (L1), legacy banking systems (ISO 20022 messaging), and AI settlement.

Conxian does **NOT** operate public DeFi protocols, consumer tokens, liquidity pools, or speculative DEX platforms. Instead, Conxian licenses stateless container images, cryptographic verification primitives, and hardware execution parameters (AWS Nitro Enclaves, Intel SGX, AMD SEV) for enterprise clients—including tier-1 financial institutions, institutional custodians, and sovereign treasury nodes—to run strictly within their own private clouds or hardware enclaves.

---

## 1. Domain Separation & Routing Firewall Matrix

Conxian enforces a strict legal, architectural, and network firewall between the open-source protocol developer surface (`conxian.org`) and the corporate governance/commercial surface (`conxian-labs.com`). All NGINX, Caddy, CORS, API gateways, and document references must strictly adhere to the following domain topology:

| Surface Category | Subdomain / Target | Primary Purpose | Repository / Service Source |
| :--- | :--- | :--- | :--- |
| **Protocol & Dev Surface** | `conxian.org` | Pure tech distribution, protocol specs, SDKs, open developer APIs | `conxian-org-site` |
| | `nexus.conxian.org` | Cross-chain state verification & settlement proofs | `conxian-nexus` |
| | `gateway.conxian.org` | Stateless RPC, ISO 20022 message normalizers & OData v4 callbacks | `conxian-gateway` |
| | `sdk.conxian.org` | Enclave hardware SDKs, attestation bindings & client libs | `conxius-enclave-sdk` |
| | `platform.conxian.org` | Sovereign node orchestration, Docker/Nix deployment specs | `conxius-platform` |
| | `market.conxian.org` | Agentic commerce, CJCS v2.0 job card ledger & AI market | `conxian_market` |
| **Corporate Surface** | `conxian-labs.com` | B2B Sales, Enterprise Licensing, Legal & Corporate Governance | `conxian-labs-site` |
| | `www.conxian-labs.com` | B2B Corporate Homepage | `conxian-labs-site` |
| | `bos.conxian-labs.com` | Sovereign Autonomous Business (SAB) Operations & Governance | `conxian-business` |

---

## 2. Phase 1: Repository Sync & Organizational Baseline

All 9 submodules within the Conxian ecosystem were fetched, recursively initialized, audited, and verified against release pin SHAs. All active working trees match the root release pins, passing `scripts/bos_repo_check.py` and `scripts/verify_submodule_integrity.py` with 0 errors.

### Repository Status Matrix (Session 64 Baseline)

| Repository Name | Submodule Directory | Release Pin SHA | Update Policy | Status | Primary Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `lib-conxian-core` | `lib-conxian-core` | `c14f2e57` | `checkout` | **ALIGNED** | BitVM2 SNARK verifier, MuSig2, DLC, ISO 20022 primitives |
| `conxian-gateway` | `conxian-gateway` | `d77952e3` | `checkout` | **ALIGNED** | API Gateway, ISO 20022 XML normalizers, Job Card handler |
| `conxian-nexus` | `conxian-nexus` | `bc870003` | `checkout` | **ALIGNED** | Cross-chain state proof engine & settlement relay |
| `conxius-enclave-sdk`| `conxius-enclave-sdk`| `11add871` | `checkout` | **ALIGNED** | TEE attestation (Nitro/SGX) & enclave runtime bindings |
| `conxius-platform` | `conxius-platform` | `1a2f78d1` | `checkout` | **ALIGNED** | NixOS / Docker orchestration & admin plane |
| `conxius-wallet` | `conxius-wallet` | `f985384a` | `checkout` | **ALIGNED** | Hardware-secured sovereign key lifecycle manager |
| `conxian-labs-site` | `conxian-labs-site` | `9dabf1cd` | `checkout` | **ALIGNED** | Enterprise B2B commercial portal (www.conxian-labs.com) |
| `conxian_market` | `conxian_market` | `276d9f4f` | `none` (override)| **ALIGNED** | AI Marketplace & Agentic Commerce surface |
| `conxian-business` | `conxian-business` | Root Local | Local | **ALIGNED** | Parent governance, SAB controls & SLA verification |

*Note on Legacy Assets:* `Conxian/Conxian` and `stackorbit` are strictly deprecated/deleted legacy repositories and are excluded from all active operational reporting.

---

## 3. Phase 2: Org-Wide Platform Review & Purge Audit

### Platform-to-Core Rust Primitives Dependency Map

```
┌────────────────────────────────────────────────────────────────────────┐
│                        conxius-platform (NixOS / Docker)              │
└───────┬───────────────────┬────────────────────┬───────────────────────┘
        │                   │                    │
        ▼                   ▼                    ▼
┌──────────────┐    ┌───────────────┐    ┌───────────────┐
│conxian-gateway│   │ conxian-nexus │    │conxius-enclave│
│ (ISO 20022 / │    │ (State Proofs/│    │     -sdk      │
│ Job Cards)   │    │  Settlement)  │    │ (TEE Nitro)   │
└───────┬──────┘    └───────┬───────┘    └───────┬───────┘
        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │   lib-conxian-core     │
               │ (BitVM2 / MuSig2 / DLC)│
               └────────────────────────┘
```

### Deprecation & Purge Verification
- **Altcoin & General Web3 Purge:** Verified that all core transaction signing and settlement pathways are exclusively dedicated to Bitcoin L1 (native UTXO, BitVM2 bridge, MuSig2, DLC) and ISO 20022 financial messaging. Archived cross-chain scripts (such as legacy Ethereum/Solana references in research archives) have been isolated and decoupled from active production build targets.
- **Strict B2B Alignment:** All client-facing interfaces interact exclusively via authenticated gRPC/REST endpoints, OData v4 callbacks, or TEE attestation channels.

---

## 4. Phase 3: B2B Client Deployment Simulation & Unified CLI Analysis

### Enterprise Client Journey Overview

1. **Purchase & Licensing:**
   - Enterprise clients procure container licensing via `www.conxian-labs.com` / `bos.conxian-labs.com`.
   - Clients pull signed, stateless container images from `registry.conxian.org/enterprise/*`.
2. **Setup & Configuration Inputs:**
   - Client specifies `.env` parameters:
     - `CONXIAN_API_TOKEN`: Environment token (`cxn_live_...` or `cxn_test_...`).
     - `BITCOIN_RPC_URL` & `BITCOIN_NETWORK`: Bitcoin L1 RPC endpoint and network setting (`mainnet`).
     - `TEE_ATTESTATION_PROVIDER`: `aws_nitro` | `intel_sgx` | `mock_dev`.
     - `ISO20022_INBOUND_QUEUE`: SWIFT/ISO 20022 MQ connection string.
3. **Deployment Flow:**
   - `conxius-platform` orchestrates container spin-up.
   - `conxian-gateway` validates incoming ISO 20022 XML messages (e.g. `pacs.008`, `camt.053`), converts them to CJCS v2.0 Job Cards, and passes execution to `conxian-nexus` and `lib-conxian-core` inside the TEE enclave.
   - `lib-conxian-core` computes BitVM2 SNARK verification (364 Hashing Tap segments) and constructs Bitcoin L1 settlement transactions.

### Unified Installer (`cxn`) Efficacy
To achieve the **TTFV < 15 minute** target for enterprise clients, a unified CLI installer (`conxian-cli` / `cxn`) is required. The installer will:
- Perform pre-flight hardware TEE attestation verification (checking CPU flags, Nitro driver availability, PKCS#11 hardware security modules).
- Validate `.env` configuration, Bitcoin RPC connectivity, and API keys prior to Docker/Nix container startup.

---

## 5. Phase 4: Issue Mapping & Criticality-Scored Gap Analysis

Cross-referencing codebase state, open tracking issues, and enterprise readiness requirements yields the following prioritized gap matrix:

| Gap ID | Description | Category | Criticality Score (0-100) | Required Solution / Remediation |
| :--- | :--- | :--- | :--- | :--- |
| **GAP-SEC-01** | Root `SECURITY.md` required explicit "Reporting a Vulnerability" section heading for automated compliance. | Security | **98** | **Remediated**: Added canonical section heading in `SECURITY.md`; verified by `verify_repo_governance_baseline.py`. |
| **GAP-ROUT-01** | `conxian.org` Developer Protocol Surface repository (`conxian-org-site`) scaffolding not yet initialized in root workspace. | Enterprise Routing | **88** | Initialize `conxian-org-site` using Astro/Starlight with static export for protocol documentation (`nexus`, `gateway`, `sdk`, `platform`, `market`). |
| **GAP-CLI-01** | Enterprise client deployment currently requires manual multi-container docker-compose setup without automated hardware TEE parameter verification. | Enterprise Routing / Installation | **84** | Implement `conxian-cli` (`cxn`) binary spec per `CLIENT_ONBOARDING_AND_UNIFIED_INSTALLER_SPEC.md`. |
| **GAP-DOC-01** | Documentation alignment index required updating to reference Master Reconnaissance & Architecture Review. | Compliance / Governance | **75** | Update `docs/DOCUMENTATION_ALIGNMENT_INDEX.md` and `CHANGELOG.md`. |

---

## 6. Protocol Surface (`conxian.org`) Architecture Specification

To maintain a zero-trust, ultra-high performance protocol surface:
- **Framework:** **Astro with Starlight** (or Next.js static export `output: 'export'`). Astro + Starlight is strongly recommended as it ships zero client JS by default, minimizing the attack surface.
- **Build & Package Management:** `pnpm` workspace integration, strict TypeScript.
- **CI/CD Security:** Node CI workflow with Gitleaks secret scanning and strict `CODEOWNERS` review enforcement.
- **Hosting / Deployment:** Containerized Nginx/Caddy static export deployed via `conxius-platform` or self-hosted TEE node with Caddy automatic TLS.
- **Subdomain Routing:**
  - `conxian.org` -> Main Protocol Hub & Deep-Tech Whitepaper
  - `nexus.conxian.org` -> State Proofs & BitVM2 API Docs
  - `gateway.conxian.org` -> ISO 20022 Normalizer & Gateway API
  - `sdk.conxian.org` -> Conxius Enclave TEE SDK Docs
  - `platform.conxian.org` -> NixOS / Docker Orchestration Specs
  - `market.conxian.org` -> Agentic Commerce & Job Card Schema Docs

---

## 7. Phase 5: Execution Plan & Immediate Code Tasks

1. **Governance & Baseline Fixes:** Completed repair of `SECURITY.md` (passed `scripts/verify_repo_governance_baseline.py` and `scripts/bos_repo_check.py`).
2. **Documentation Synchronization:** Updated `CHANGELOG.md`, `BOS_KNOWLEDGE_GRAPH.md`, and `docs/DOCUMENTATION_ALIGNMENT_INDEX.md`.
3. **Next Session Immediate Code Tasks:**
   - Scaffolding the `conxian-org-site` protocol documentation repository using Astro/Starlight (`pnpm create astro@latest --template starlight`).
   - Implementation of pre-flight environment checks in `conxian-cli` (`cxn`).
