# Conxian Labs: Strategic Alignment & Structural Integrity

This document is the **Central Nervous System** for Conxian Labs. It provides high-level alignment across all repositories, submodules, and business functions, accurately mapping verified technical pull requests into the institutional documentation.

## 1. Vision: Non-Custodial Sovereign Truth
**Code is Law. Sovereignty is Absolute.**
Conxian Labs engineers systems that mathematically prevent centralized TradFi failures (fractional reserves, commingled funds). The ecosystem's resilience is anchored in self-custody and deterministic, Nakamoto-ready state proofs, entirely rejecting centralized intermediary reliance.

## 2. Ecosystem Architecture (Phase 4 Unbundled)
The system is structurally unbundled into three isolated suites to ensure cryptographic truth and operational focus:

### 2.1 B2B Suite (Infrastructure & SDK)
- **[lib-conclave-sdk](./lib-conclave-sdk)**: Platform-agnostic Enclave SDK (Android TEE / iOS Secure Enclave).
- **[conxian-nexus](./conxian-nexus)**: Decentralized "Glass Node" Risk Oracle & State Sync. Implements **Compliance Circuit Breakers**.

### 2.2 B2C Suite (Autonomous Agentic Interface)
- **[conxius-wallet](./conxius-wallet)**: Flagship interface features a native **Kotlin Model Context Protocol (MCP) server** and hardware-enclosed **StrongBox** signing (Zero Secret Egress).

### 2.3 Core Infrastructure & Orchestration
- **[conxian-gateway](./conxian-gateway)**: High-performance Fusion gateway. **Nexus-First polling active.**
- **[lib-conxian-core](./lib-conxian-core)**: Single Source of Truth for protocol primitives.

## 3. Verified Technical Implementation (Ground Truth)
- **Agent Payments Protocol (AP2)**: Integrated Verifiable Mandates (VCs) to govern autonomous agent behavior.
- **StrongBox Hardware Isolation**: Enforced hardware-enclosed signing to mathematically mitigate LLM/agent prompt injection.
- **A402 Atomic Service Channels**: Executed trust-minimized M2M commerce utilizing TEE-assisted adaptor signatures.
- **On-Chain Guardrails**: Deployed strictly enforced agent spend limits utilizing Clarity on the Stacks blockchain.

## 4. Operational Standards
- **Zero Secret Egress**: Private keys never enter application memory or leave the hardware enclave.
- **Unbundled Integrity**: Successful completion of Phase 1-4 structural unbundling.
- **Theme**: Earthy Corporate Finance (#2E403B / #D4A017).

---
© 2026 Conxian Labs. Sovereign Autonomous Business.
[Return to Root README](./README.md) | [View Whitepaper](./WHITEPAPER.md)
