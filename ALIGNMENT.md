# Conxian Labs: Strategic Alignment & Ecosystem Overview

This document is the **Central Nervous System** for Conxian Labs. It provides high-level alignment across all repositories, submodules, and business functions.

## 1. Vision & Core Philosophy
**Code is Law. Sovereignty by Design.**
Conxian Labs replaces human discretion with mathematical certainty. All system states are anchored to the Bitcoin burn-block height, ensuring a strictly non-custodial, sovereign architecture.

- **Bitcoin Anchoring**: All temporal logic is anchored to Bitcoin burn-block-height.
- **Sovereign Services**: Native integration with Bitcoin L1, Lightning, Stacks (Nakamoto), and Liquid.
- **L2 Synergy**: Leveraging sBTC for Bitcoin liquidity across EVM and non-EVM chains.

## 2. Ecosystem Architecture (Unit Compartmentalization)
The ecosystem is structured into three distinct, isolated suites to maximize acquisition readiness and facilitate regulatory fencing:

### 1. B2B Suite (Infrastructure & SDK)
- **[lib-conclave-sdk](./lib-conclave-sdk)**: Platform-agnostic Enclave SDK (Android TEE / iOS Secure Enclave).
- **[conxian-nexus](./conxian-nexus)**: Decentralized "Glass Node" Risk Oracle & State Sync. Implements **Compliance Circuit Breakers**.

### 2. B2C Suite (Consumer Interface)
- **[conxius-wallet](./conxius-wallet)**: Autonomous Agentic Interface. Hardware-grade security for the full Bitcoin stack via StrongBox.
- **[conxian-ui](./conxian-ui)**: Unified Web Lens for retail portfolio management.

### 3. Core Infrastructure & Orchestration
- **[conxian-gateway](./conxian-gateway)**: High-performance Fusion gateway. MVCR-attested compliance routing. **Nexus-First polling implemented.**
- **[lib-conxian-core](./lib-conxian-core)**: Single Source of Truth for protocol primitives.
- **[conxius-platform](./conxius-platform)**: Master Orchestrator for local dev and system synergy.

## 3. Strategic Roadmap (Level 5 Initiation)
Conxian follows a 6-Phase execution strategy, mapped to Operational Levels and Milestones.

| Phase | Level | Status | Focus | Key Milestones |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1-3** | **L0-L1** | ✅ | **Foundation** | Bitcoin L1, Lightning, sBTC, Core Enclave (M1-M4) |
| **Phase 4** | **L2** | ✅ | **Interoperability** | Wormhole NTT, Sovereign Bridging, Gas Abstraction (M5-M8) |
| **Phase 5** | **L3** | 🚀 | **Autonomous Agents** | Agentic Wallet, **AP2 Mandates**, **A402 Channels**, **Kotlin MCP Server** |
| **Phase 6** | **L4** | ⏳ | **Global Sovereignty** | AI-Driven Asset Allocation, Universal Bitcoin Identity (M12-M17) |

For detailed milestones, see **[Full Roadmap](./02_strategy/ROADMAP.md)**.

## 4. Design & UX Standards (Earthy Corporate Finance)
- **Theme**: Professional trust and stability (Tier0 light theme).
- **Palette**:
  - Primary: `#2E403B` (Forest Green)
  - Accent: `#D4A017` (Gold)
  - Background: `#F5F5F5` / `#FFFFFF`
- **Telemetry**: "Glass Node Architecture" via Prometheus (9090) and Grafana (3001).

## 5. Security & Compliance (Sentinel & Fusion)
- **Non-Custodial**: User keys remain in on-device TEE/StrongBox/Secure Enclave.
- **Fusion Auth**: Unified JWT/Enclave-based authentication.
- **MVCR**: Mathematically Verifiable Compliance Reports for MiCA (EU) and IRS (US).
- **Compliance Circuit Breakers**: Human-in-the-Loop fallback for critical regulatory interventions.

---
[Return to Root README](./README.md) | [View Whitepaper](./WHITEPAPER.md)

## 6. CSO & Lead Architect Review (March 2026 Update)

### 6.1. Strategic Pivot: Unit Compartmentalization
To maximize acquisition value and isolate risks, the Conxian ecosystem has been unbundled into distinct business units. The **Autonomous Agentic Wallet** is now the flagship product for retail sovereignty, while the **Conclave SDK** provides institutional enclave-as-a-service.

### 6.2. Autonomous Agentic Integrity
The elevation of conxius-wallet to an autonomous interface utilizes **AP2 Verifiable Mandates** to ensure machine-speed execution never violates human-set boundaries. Cryptographic guardrails are enforced inside the **Android StrongBox**, preventing prompt injection attacks.

### 6.3. Compliance Posture (MiCA/IRS)
Our "Edge Compliance" strategy ensures that M2M transactions generate **Hardware-Attested Compliance Reports (MVCR)**. This satisfies MiCA's Article 59 and IRS 1099-DA without centralized data collection, maintaining 100% sovereign custody.

## 7. Operational Resilience & Vertical Scaling

### 7.1. State Consolidation (Nexus-First)
By centralizing all chain-polling into **Conxian Nexus**, we have reduced cross-repo desync risk and lowered cloud compute costs. The **Conxian Gateway** now pulls verified state from Nexus.

### 7.2. Enterprise Durable Queueing
Scenario 1 (Enterprise Blackout) is mitigated via server-side durable queueing in Nexus using Redis, ensuring ISO 20022 financial data integrity during client ERP downtime.

### 7.3. Institutional UI & Enterprise Control
The Admin Dashboard includes the **Sovereign Grace Widget** (License telemetry), **Triad Health Monitor** (Real-time synergetic loops), and the **Circuit Breaker Control Module** for institutional risk management.
