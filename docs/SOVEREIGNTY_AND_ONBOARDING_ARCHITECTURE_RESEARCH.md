# Conxian Onboarding, Initial System Configuration & Configurable Sovereignty Research Report

> **Document Version**: 1.0.0
> **Status**: Approved Architectural & Strategic Framework
> **Date**: 2026-09-19
> **Target Audience**: System Architects, Integration Engineers, Compliance Officers, Executive Leadership

---

## Executive Summary

This research report evaluates the initial startup, onboarding, and operational deployment models for the **Conxian Sovereign Business Operations System (BOS)**. It establishes an architectural paradigm called the **Configurable Sovereignty Dial**, enabling clients (developers, SMEs, fintechs, and sovereign entities) to dynamically select their desired level of decentralization and infrastructure ownership without forcing Conxian-Labs into custodial or regulatory exposure.

By combining out-of-the-box zero-friction local defaults (Time-To-First-Value / TTFV < 15 minutes) with a flexible hybrid deployment topology, Conxian offers a seamless developer experience alongside enterprise-grade institutional isolation.

---

## 1. Initial System Configuration & First Startup Experience

### 1.1 Out-of-the-Box Zero-Friction Setup (TTFV < 15m)

A primary friction point during initial client onboarding is mandatory secret provisioning before first execution. Standard container orchestration stacks often fail or panic during `docker compose up --build` when non-critical environment variables (such as payment gateway webhooks or external RPC credentials) are unassigned.

To guarantee a **Time-To-First-Value (TTFV) under 15 minutes**:
1. **Fallback Environment Interpolation**: The core `docker-compose.yml` provides robust local development fallbacks (e.g., `${DB_PASSWORD:-postgres_dev_password}`, `${STACKS_NODE_RPC_URL:-https://api.mainnet.hiro.so}`, `${BITCOIN_RPC_URL:-https://bitcoin-rpc.publicnode.com}`) across all services (`db`, `nexus`, `gateway`).
2. **Developer Stub/Dev Mode**: Optional secrets (Investec, Ramp, Banxa, AlchemyPay, Infobip) default to non-blocking development tokens (`dev_investec_client_id`, `dev_ramp_api_key`), enabling full stack bootup in offline or simulated mode without external API dependencies.
3. **Reference Environment Lane Pre-configs**: Environment files (`docker-compose.env.local.example`, `docker-compose.env.testnet.example`, `docker-compose.env.mainnet.example`) allow instant environment switching via a simple `cp docker-compose.env.<lane>.example .env`.

---

## 2. The Configurable Sovereignty Dial

Clients have fundamentally different infrastructure requirements, security models, and compliance boundaries. Rather than imposing a binary choice between "100% self-hosted complexity" and "centralized SaaS lock-in," Conxian introduces a multi-tier **Configurable Sovereignty Dial**:

| Sovereignty Level | Hosting Topology | Control Plane | Key Custody / Signing | Typical User / Client |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0: Dev Sandbox** | Cloud-Hosted / Public Preview | Conxian Shared Sandbox | Ephemeral / Mock Keys | Hackathon builders, initial evaluators |
| **Level 1: Managed Hybrid** | Conxian / Partner Managed Endpoints | Conxian Public Infrastructure | User Self-Custody (Mobile TEE / StrongBox) | Fintechs, payment apps, SMEs |
| **Level 2: Partner Sovereign** | Certified Partner Cloud (AWS/GCP/Azure) | Dedicated Partner Tenant | User TEE or Managed KMS/HSM | Regional banks, institutional payment hubs |
| **Level 3: Full Sovereign** | Client Private Cloud / On-Prem | 100% Client Operated | Dedicated Hardware HSM + AWS Nitro Enclave | Global banks, sovereign wealth funds, nation-states |

### Key Architectural Invariant
**Key custody and signing authority remain strictly non-custodial across all dial settings.** Conxian never holds, signs with, or manages customer private keys. Higher sovereignty levels grant greater control over node indexing (`nexus`), compliance routing (`gateway`), and hardware isolation—not key custody.

---

## 3. Regulatory Alignment & Regulatory Boundary Protections

Conxian-Labs maintains a strict **Sovereign Non-Custodial Software Vendor** posture:

1. **Zero AUM / Zero Asset Custody**: Conxian provides pure software logic (Rust/WASM binaries, Docker containers, Smart Contract primitives). Assets remain on Bitcoin L1 and Stacks L2 under client-controlled keys.
2. **Yield-Only OpEx (Zero-Credit Model)**: Platform monetization is driven by software licensing and node indexing APIs, operating under non-financial, non-banking regulatory scopes.
3. **Zero-Knowledge Compliance (ZKC)**: Sanction screening, proof-of-reserves, and ISO 20022 message formatting are executed locally inside client gateways or enclaves. Compliance attestations are verified cryptographically without exfiltrating raw financial transaction data to central servers.

---

## 4. Multi-Tier Deployment Topology & Hybrid Architecture

To offer maximal capability without trapping clients or creating vendor lock-in, Conxian supports four distinct deployment topologies:

```
+-----------------------------------------------------------------------------------+
|                            CONFIGURABLE DEPLOYMENT SPECTRUM                       |
+-------------------+-------------------+-------------------+-----------------------+
|  Hosted Dev Env   | Public Endpoints  |  Partner Hosting  | Self-Hosted Sovereign |
|  (Developer)      | (Business)        |  (Enterprise)     | (Nation-State)        |
+-------------------+-------------------+-------------------+-----------------------+
| • Quickstart      | • Shared Nexus    | • Dedicated K8s   | • On-prem / Air-gap   |
| • Pre-seeded DB   | • Public RPC      | • Managed HSM     | • Dedicated Node      |
| • Ephemeral TEE   | • Managed Gateway | • Regional Hub    | • AWS Nitro / Hardware|
+-------------------+-------------------+-------------------+-----------------------+
```

### 4.1 Hybrid Operational Flow
A client can start on **Public Managed Endpoints** (Level 1) for rapid prototyping, transition to **Partner Hosting** (Level 2) during regional expansion, and seamlessly export state/relocate to **Self-Hosted Sovereign Cloud** (Level 3) without code modifications or protocol migration friction.

---

## 5. Summary & Verification Matrix

- **Zero-Friction Initial Startup**: Verified via `docker compose config` with default environment fallbacks.
- **Client Sovereignty Control**: Fully specified across 4 tiers with non-custodial invariants.
- **Regulatory Safety**: Zero custody, software-only liability boundary validated against `docs/COMMERCIAL_PACKAGING_DOCTRINE.md`.
