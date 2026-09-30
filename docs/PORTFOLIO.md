# Conxian Portfolio & Capability Matrix

| Metadata | Value |
|---|---|
| Classification | Public-safe portfolio capability matrix |
| Standard | Conxian BOS v1.9.5 |
| Authority | [Business Issue #943](https://github.com/Conxian/conxian-business/issues/943) |
| Last Updated | 2026-09-26 |

---

## Overview

The Conxian Ecosystem delivers Bitcoin-native business operations across decentralization-critical layers (L1-L3), user interfaces, and shared cryptographic runtimes.

---

## Capability × Chain Matrix

| Capability | Bitcoin L1 | Stacks L2 | EVM / Arbitrum | Cosmos / IBC | Reference Customer / Lead Target |
|---|---|---|---|---|---|
| **Non-Custodial Wallet** | Production (v1.9.5) | Production (v1.9.5) | Planned (v2.1) | - | Conxius Wallet Users |
| **Settlement Bridge** | BitVM2 / DLC (v0.1.5) | Clarity Epoch 3.0 | ERC-20 / Bridge | - | Enterprise B2B FinTech |
| **Universal Chain Sync (Nexus)** | Active (v0.4.23) | Active (v0.4.23) | Active (v0.4.23) | Active (v0.4.23) | Sovereign Infrastructure Nodes |
| **M2M Agent Marketplace** | DLC Escrow | SIP-010 Tokens | ERC-8183 Escrow | - | AI Agent Developers |
| **TEE Hardware Signer** | Nitro Enclave (v2.0.17) | Nitro Enclave | - | - | Institutional Custody / Fund Ops |
| **ISO 20022 Messaging** | pacs.008 Bridge | - | - | - | Commercial Banking Partners |

---

## Repository Mapping & SLA / Support Boundaries

| Repository | Surface / Layer | Primary Capability | License | SLA / Support Tier | Status |
|---|---|---|---|---|---|
| `conxian-business` | Governance (Root) | OpenSpec & Business Governance | GPL-3.0 | Community Best-Effort | Active |
| `conxian-gateway` | Layer 1 (Execution) | Settlement Bridge & ISO 20022 | GPL-3.0 | B2B Contract SLA (99.5%) | Active (v0.1.5) |
| `conxian-nexus` | Layer 1 (Verification) | Universal Chain Node & State Proofs | GPL-3.0 | B2B Node SLA / Open-Core | Active (v0.4.23) |
| `conxius-wallet` | Layer 2 (User) | Non-Custodial Mobile Wallet | MIT / Commercial | Open-Source / Self-Custody | Production (v1.9.5) |
| `conxian_market` | Layer 2 (Market) | M2M Agent Marketplace & Escrow | Commercial | Metered x402 / Open-Core | Active |
| `lib-conxian-core` | Layer 3 (Runtime) | Bitcoin & Cryptographic Primitives | MIT / Apache-2.0 | NO SLA (Open Protocol) | Active (v0.3.3) |
| `conxius-enclave-sdk` | Layer 3 (Security) | Nitro TEE & Hardware Attestation | MIT / Apache-2.0 | NO SLA (Open SDK) | Beta (v2.0.17) |
| `conxius-platform` | Control Plane | Deployment & Scaffolding | MIT | Community Best-Effort | Active |
| `conxian-labs-site` | Public Surface | Corporate & Portfolio Discovery | MIT | Public Web Surface | Active |

---

## Business-as-a-Platform (BaaP) Commercial Tiers

1. **Community Tier ($0)**: Open-source libraries (`lib-conxian-core`, `conxius-enclave-sdk`), self-hosted Wallet, public `gateway.conxian.org` sandbox.
2. **Business Tier ($2,500 - $7,500/mo)**: Managed Gateway instance, ISO 20022 normalizer, business-hours SEV1 SLA (1-hr ack).
3. **Enterprise Tier ($15,000 - $40,000/mo)**: Dedicated Sovereign Nexus Node, local Nitro/SGX TEE execution, Bring-Your-Own DeFi vault integration, dedicated SLA contract.
