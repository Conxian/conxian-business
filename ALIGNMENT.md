# Conxian Labs: Strategic Alignment & Ecosystem Overview

This document is the "Central Nervous System" for Conxian Labs. It provides high-level alignment across all repositories, submodules, and business functions.

## 1. Vision & Core Philosophy
**Code is Law.**
Conxian Labs replaces human discretion with mathematical certainty. All system states are anchored to the Bitcoin burn-block height, ensuring a strictly non-custodial, sovereign architecture.

## 2. Ecosystem Architecture
The ecosystem is organized into specialized microservices and clients:
- **[conxius-platform](./conxius-platform)**: The orchestrator. Used for local development stacks and full-system synergy.
- **[lib-conxian-core](./lib-conxian-core)**: Shared Rust/TypeScript logic. The single source of truth for protocol primitives.
- **[conxian-gateway](./conxian-gateway)**: The high-performance Fusion gateway (Rust/Actix-web).
- **[Conxian](./Conxian)**: Stacks-native DeFi protocol and smart contracts (Clarity).
- **[conxian-ui](./conxian-ui)**: The ecosystem's web lens (TypeScript/Next.js).
- **[conxius-wallet](./conxius-wallet)**: The Sovereign Android Vault (TypeScript/Android TEE).
- **[conxian-nexus](./conxian-nexus)**: API bridge and orchestration layer.
- **[stacksorbit](./stacksorbit)**: Professional TUI/GUI deployment tool for Stacks smart contracts.
- **[conxian-labs-site](./conxian-labs-site)**: Institutional research, institutional gateways, and legal registry frontend.

## 3. Strategic Roadmap (5-Year Plan)
Technical decisions support the .5M Pre-seed to $100M+ Series C roadmap.
- **Infrastructure**: Cloud-only for the first 3.5 years (GCP/Render).
- **Scaling**: Triggered by monthly revenue milestones and TVL growth.
- **Sovereignty**: Progressive decentralization, anchoring all critical state to Bitcoin.

## 4. Design & UX Standards
- **Theme**: "Earthy Corporate Finance" (Professional trust and stability).
- **Telemetry**: "Glass Node Architecture" via Prometheus (9090) and Grafana (3001).
- **Palette**: Forest Green (#2E403B), Gold (#D4A017), and Professional Whites/Grays.

## 5. Security & Compliance (Sentinel)
- **Non-Custodial**: User keys remain in on-device TEE/StrongBox.
- **Fusion Auth**: Unified JWT/Enclave-based authentication.
- **Secret Management**: Automated filtering and local provisioning via `make auth`.

## 6. Repository Governance
- **Main Branch**: Protected. Requires PRs for all changes.
- **Documentation**: All strategic, legal, and operational documents reside in the `01_company` through `07_assets` folder hierarchy.

---
*Last Updated: February 2026*
