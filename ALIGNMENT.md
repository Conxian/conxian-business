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
- **[conxian-gateway](./conxian-gateway)**: The high-performance Fusion gateway (Rust/Actix-web). Unified entry point for all protocol state.
- **[Conxian](./Conxian)**: Stacks-native DeFi protocol and smart contracts (Clarity 4).
- **[conxian-ui](./conxian-ui)**: The ecosystem's web lens (TypeScript/Next.js).
- **[conxius-wallet](./conxius-wallet)**: The Sovereign Android Vault (TypeScript/Android TEE).
- **[conxian-nexus](./conxian-nexus)**: API bridge and orchestration layer (The Glass Node).
- **[stacksorbit](./stacksorbit)**: Professional TUI/GUI deployment and monitoring tool.
- **[conxian-labs-site](./conxian-labs-site)**: Institutional research and legal registry frontend.

## 3. Strategic Roadmap (5-Year Plan)
Technical decisions support the .5M Pre-seed to 00M+ Series C roadmap.
- **Infrastructure**: Cloud-only for the first 3.5 years (GCP/Render).
- **Scaling**: Triggered by monthly revenue milestones and TVL growth.
- **Sovereignty**: Progressive decentralization, anchoring all critical state to Bitcoin.

### 📈 Market Strategy (2026)
- **TAM:** Global Bitcoin L2 market (~0B TVL in 2026).
- **SAM:** Stacks ecosystem (~30M TVL).
- **SOM:** Capture 10% of Stacks TVL and 5,000 active users within 24 months.

## 4. Design & UX Standards (Earthy Corporate Finance)
- **Theme**: Professional trust and stability (Tier0 light theme).
- **Palette**:
  - Primary: `#2E403B` (Forest Green)
  - Accent: `#D4A017` (Gold)
  - Background: `#F5F5F5` / `#FFFFFF`
  - Text: `#333333`
- **Telemetry**: "Glass Node Architecture" via Prometheus (9090) and Grafana (3001).
- **Typography**: Inter (Sans-serif) for professional clarity.

## 5. Security & Compliance (Sentinel & Fusion)
- **Non-Custodial**: User keys remain in on-device TEE/StrongBox.
- **Fusion Auth**: Unified JWT/Enclave-based authentication.
- **Secret Management**: Automated filtering and local provisioning via `make auth`.
- **Compliance**: Regulated actions (KYC, Fiat) are delegated to authorized partners (Transak, VALR).

## 6. Repository Governance & Directives
- **Main Branch**: Protected. Requires PRs for all changes.
- **Single Source of Truth**: Protocol state monitored via the **Conxian Gateway**.
- **Shared Logic**: All shared cryptographic and protocol logic resides in `lib-conxian-core`.
- **Nakamoto Native**: All contracts (`Conxian`) must use Clarity 4 and Bitcoin-anchored height logic.

---
*Last Updated: February 2026*
