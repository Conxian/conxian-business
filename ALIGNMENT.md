# Conxian Labs: Strategic Alignment & Ecosystem Overview

This document is the **Central Nervous System** for Conxian Labs. It provides high-level alignment across all repositories, submodules, and business functions.

## 1. Vision & Core Philosophy
**Code is Law. Sovereignty by Design.**
Conxian Labs replaces human discretion with mathematical certainty. All system states are anchored to the Bitcoin burn-block height, ensuring a strictly non-custodial, sovereign architecture.

- **Bitcoin Anchoring**: All temporal logic is anchored to Bitcoin burn-block-height.
- **Sovereign Services**: Native integration with Bitcoin L1, Lightning, Stacks (Nakamoto), and Liquid.
- **L2 Synergy**: Leveraging sBTC for Bitcoin liquidity across EVM and non-EVM chains.

## 2. Ecosystem Architecture (Unit Compartmentalization)
The ecosystem is structured into distinct, isolatable units to maximize acquisition readiness and focus:
- **[Conxius Wallet (B2C)](./conxius-wallet)**: The Sovereign Vault (Android TEE/iOS Secure Enclave). Focus on retail self-sovereignty.
- **[Conclave B2B SDK (SDK)](./lib-conclave-sdk)**: Platform-agnostic Enclave SDK for 3rd-party L2s and institutional apps.
- **[Conxian Gateway (B2M)](./conxian-gateway)**: Institutional routing and **MVCR-attested** compliance layer.
- **[Conxian Nexus (B2E)](./conxian-nexus)**: The "Glass Node" state-sync oracle. Focus on state proofs and **Compliance Circuit Breakers**.
- **[lib-conxian-core](./lib-conxian-core)**: Shared Rust primitives. The **Single Source of Truth** for the entire stack.
- **[Conxian Finance](./Conxian)**: Stacks-native DeFi protocol (Clarity 4).
- **[stacksorbit](./stacksorbit)**: Professional TUI/GUI tooling for ecosystem operations.

## 3. Strategic Roadmap (Level 4 Alignment)
Conxian follows a 6-Phase execution strategy, mapped to Operational Levels and Milestones.

| Phase | Level | Status | Focus | Key Milestones |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1-3** | **L0-L1** | ✅ | **Foundation** | Bitcoin L1, Lightning, sBTC, Core Enclave (M1-M4) |
| **Phase 4** | **L2** | ✅ | **Interoperability** | Wormhole NTT, Sovereign Bridging, Gas Abstraction (M5-M8) |
| **Phase 5** | **L3** | 🚀 | **Orchestration** | Global Liquidity Mesh, **Compartmentalization (M12)**, **iOS Parity (M13)** |
| **Phase 6** | **L4** | ⏳ | **Agentic Finance** | AI-Driven AgentOps 1.0, **Circuit Breakers (M14)**, **SSI Trust (M16)** |

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
To maximize acquisition value and isolate risks, the Conxian ecosystem has been restructured into distinct business units:
- **Wallet (Retail)**: Non-custodial super-app for Bitcoin and L2s.
- **SDK (Developer)**: The Conclave Enclave-as-a-Service model.
- **Gateway (Institutional)**: Institutional liquidity routing and compliance reporting (MVCR).

### 6.2. Strategic Recommendations (M13-M14)
1. **iOS Secure Enclave Parity**: Launch the **Conclave iOS Adapter** to capture the high-value iOS market.
2. **Compliance Circuit Breakers**: Implement human-in-the-loop multi-sig fallbacks for all automated compliance halts in Nexus.
3. **Consolidate State Layer**: Centralize chain polling into Nexus to reduce COGS and ensure state consistency. (Completed)

## 7. Institutional UI & Enterprise Control (March 2026)
The Admin Dashboard now includes the **Sovereign Grace Widget** (License telemetry), **Triad Health Monitor** (Real-time synergetic loops), and the **Circuit Breaker Control Module** for institutional risk management.
