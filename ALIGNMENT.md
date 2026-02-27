# Conxian Labs: Strategic Alignment & Ecosystem Overview

This document is the **Central Nervous System** for Conxian Labs. It provides high-level alignment across all repositories, submodules, and business functions.

## 1. Vision & Core Philosophy
**Code is Law.**
Conxian Labs replaces human discretion with mathematical certainty. All system states are anchored to the Bitcoin burn-block height, ensuring a strictly non-custodial, sovereign architecture.

- **Bitcoin Anchoring**: All temporal logic is anchored to Bitcoin burn-block-height.
- **Sovereign Services**: Native integration with Bitcoin-adjacent protocols: Bisq (DEX), RGB (Smart Assets), BitVM (Computation), and Lightning (Payments).
- **L2 Synergy**: Leveraging Stacks (Nakamoto) as the primary smart contract layer with sBTC for Bitcoin liquidity.

## 2. Ecosystem Architecture
The ecosystem is organized into specialized microservices and clients:
- **[conxius-platform](./conxius-platform)**: The master orchestrator. Used for local development stacks and full-system synergy.
- **[lib-conxian-core](./lib-conxian-core)**: Shared Rust/TypeScript logic. The **Single Source of Truth** for protocol primitives.
- **[conxian-gateway](./conxian-gateway)**: The high-performance Fusion gateway (Rust/Actix-web). Orchestrates cross-chain atomic swaps and tiered institutional access.
- **[Conxian](./Conxian)**: Stacks-native DeFi protocol and smart contracts (Clarity 4).
- **[conxian-ui](./conxian-ui)**: The ecosystem's web lens (TypeScript/Next.js).
- **[conxius-wallet](./conxius-wallet)**: The Sovereign Android Vault (TypeScript/Android TEE). Hardware-level security for retail and institutional users.
- **[conxian-nexus](./conxian-nexus)**: API bridge and **Decentralized Risk Oracle**. Provides verifiable state proofs and risk scoring.
- **[stacksorbit](./stacksorbit)**: Professional TUI/GUI deployment and monitoring tool.
- **[conxian-labs-site](./conxian-labs-site)**: Institutional research and legal registry frontend.

## 3. Strategic Roadmap (Master Alignment)
Conxian follows a 6-Phase execution strategy, mapped to Operational Levels and Milestones.

| Phase | Level | Status | Focus | Key Milestones |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1-3** | **L0-L1** | ✅ | **Foundation** | Bitcoin L1, Lightning, sBTC, Core Enclave (M1-M4) |
| **Phase 4** | **L2** | ✅ | **Interoperability** | Wormhole NTT, Sovereign Bridging, Gas Abstraction (M5-M8) |
| **Phase 5** | **L3** | 🚀 | **Orchestration** | Global Liquidity Mesh, Gateway Beta, Risk Oracle (M9-M11) |
| **Phase 6** | **L4** | ⏳ | **Sovereign AI** | AI-Driven Asset Allocation, Universal Bitcoin Identity (M12-M15) |

For detailed milestones, see **[Full Roadmap](./02_strategy/ROADMAP.md)**.

## 4. Design & UX Standards (Earthy Corporate Finance)
- **Theme**: Professional trust and stability (Tier0 light theme).
- **Palette**:
  - Primary: `#2E403B` (Forest Green)
  - Accent: `#D4A017` (Gold)
  - Background: `#F5F5F5` / `#FFFFFF`
- **Telemetry**: "Glass Node Architecture" via Prometheus (9090) and Grafana (3001).

## 5. Security & Compliance (Sentinel & Fusion)
- **Non-Custodial**: User keys remain in on-device TEE/StrongBox.
- **Fusion Auth**: Unified JWT/Enclave-based authentication.
- **MVCR**: Mathematically Verifiable Compliance Reports for MiCA (EU) and IRS (US).

---
[Return to Root README](./README.md) | [View Whitepaper](./WHITEPAPER.md)
