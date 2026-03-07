# Conxian Labs: Internal Business Repository

This private repository is the **Central Nervous System** for Conxian Labs. It orchestrates three distinct, isolated product suites designed for institutional M&A readiness and regulatory fencing.

## 🚀 Strategic Foundation
- **[Strategic Alignment (ALIGNMENT.md)](./ALIGNMENT.md)** - Unbundled architecture and master roadmap.
- **[System Whitepaper (WHITEPAPER.md)](./WHITEPAPER.md)** - Theoretical and technical foundation.
- **[Full Roadmap](./02_strategy/ROADMAP.md)** - Phase-based milestones including iOS Parity (M13).

## 📦 Isolated Product Suites
The ecosystem is structurally unbundled into three independent suites:

### 1. B2B Suite (Infrastructure & SDK)
*Focus: Institutional tooling, enclave security, and risk oracles.*
- **[lib-conclave-sdk](./lib-conclave-sdk)**: Platform-agnostic Enclave SDK (Android TEE / iOS Secure Enclave).
- **[conxian-nexus](./conxian-nexus)**: Decentralized "Glass Node" Risk Oracle & State Sync.

### 2. B2C Suite (Consumer Interface)
*Focus: Retail self-sovereignty and "Citadel" UX.*
- **[conxius-wallet](./conxius-wallet)**: Sovereign Android/iOS Vault. Hardware-grade security for the full Bitcoin stack.
- **[conxian-ui](./conxian-ui)**: Unified Web Lens for retail portfolio management.

### 3. Core Infrastructure & Orchestration
*Focus: Routing, compliance, and developer operations.*
- **[conxian-gateway](./conxian-gateway)**: High-performance Fusion gateway. MVCR-attested compliance routing.
- **[lib-conxian-core](./lib-conxian-core)**: Single Source of Truth for protocol primitives.
- **[conxius-platform](./conxius-platform)**: Master Orchestrator for local dev and system synergy.

## 📂 Navigation
- **[01_company](./01_company)** - Org structure and unit compartmentalization.
- **[02_strategy](./02_strategy)** - M&A readiness and 5-year roadmap.
- **[03_infrastructure](./03_infrastructure)** - NTT routing and ERP integration.
- **[04_legal](./04_legal)** - MiCA/IRS compliance and Risk Registry.

## 🛠️ Management
Use the root **Makefile** to manage isolated suites:
- `make build-b2b`: Build SDK and Nexus.
- `make build-b2c`: Build consumer wallet.
- `make unbundle`: Verify architectural compartmentalization.

## 🛡️ Access & Confidentiality
All documents are confidential and proprietary. © 2026 Conxian Labs. Sovereign Autonomous Business.
