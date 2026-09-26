# Commercial Packaging Doctrine — Offer Structure, Pricing, and Customer Journey

> **Issue**: [#829](https://github.com/Conxian/conxian-business/issues/829) — Maintain canonical packaging, customer journey, and pricing doctrine set
> **Status**: Canonical Business-as-a-Platform (BaaP) Doctrine
> **Last updated**: 2026-09-26
> **Owner**: Packaging lane (per [OPERATING_LANE_BOUNDARIES.md](OPERATING_LANE_BOUNDARIES.md))

---

## Purpose

This document defines the canonical commercial packaging doctrine and pricing architecture for Conxian-Labs (Pty) Ltd. Conxian transforms from a standard transaction fee collector into a high-margin **Business-as-a-Platform (BaaP)** by combining volume-based protocol settlement, enterprise software node licensing, and metered x402 edge compute/attestations.

---

## 1) Primary Offer Structure

Conxian offers three primary product lines across all commercial packaging tiers:

| Product | Type | What It Is | Maturity |
|---------|------|------------|----------|
| **`conxian-gateway`** | B2B Infrastructure | ISO 20022 compliance pipe bridging Bitcoin/Stacks with legacy banking. Includes ZKC (Zero-Knowledge Compliance) and SYI (Sovereign Yield Index). | Beta |
| **Conxius Wallet** | B2C / Enterprise Client | Sovereign Bitcoin command center (Android-first, offline-first). Hardware-enforced key custody via StrongBox/TEE. | Stable (v1.9.5) |
| **`conxius-enclave-sdk`** | Developer Tool | Cross-platform Rust/WASM SDK for hardware enclave abstractions. Enables third-party builders to integrate sovereign key management. | Beta |

**Supporting Platform Submodules**:
- **Conxian Nexus**: Multi-protocol state verification node & bridge solver (`conxian-nexus`)
- **Conxian Market**: AI Marketplace & Agentic Commerce surface (`conxian_market`)
- **Core Library**: BitVM2/3 proof verification & Taproot primitives (`lib-conxian-core`)

---

## 2) Multi-Tiered Monetization Engine (BaaP Architecture)

Conxian captures value across three distinct monetization layers: Protocol Volume (M2M Escrow), Enterprise SaaS (Private Business Nodes), and Metered Utility (x402 Edge Compute & Attestations).

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      TOTAL REVENUE STREAM MATRIX                         │
├──────────────────────────┬───────────────────────┬───────────────────────┤
│   1. PROTOCOL ESCROW     │  2. ENTERPRISE NODE   │   3. METERED EDGE     │
│ (2% Volume Settlement)   │  (Private BaaP SaaS)  │  (x402 Attestations)  │
│                          │                       │                       │
│ • 80% Developer Pool     │ • Annual License ($)  │ • Per-Attestation Fee │
│ • 10% Operations Pool    │ • Custom SLA Matrix   │ • ZK Proof Verifier   │
│ • 10% Network Pool       │ • Dedicated TEE Config│ • ISO 20022 Engine    │
└──────────────────────────┴───────────────────────┴───────────────────────┘
```

### Layer 1: M2M Escrow & Transaction Routing (Volume-Based)

The baseline protocol model charges a **2.0% gross market fee** on all machine-to-machine (M2M) escrow settlement volume moving through the Nexus and Gateway.

#### Fixed Fee Split Structure
- **80% Developer Pool**: Distributed to dApp builders, AI agent developers, and job card executors generating transactions on the network.
- **10% Operations Pool**: Allocated directly to Conxian Labs corporate treasury for core system maintenance, engineering, and platform orchestration.
- **10% Network Pool**: Allocated to decentralized node operators and proof verifiers running network infrastructure.

#### Tiered Volume Fee Decay (Enterprise Scale)
To maintain competitiveness against legacy bridges on institutional volumes while maximizing margins on micro-agent tasks, Conxian enforces a dynamic fee decay schedule:

| Monthly Volume Tier | Gross Escrow Fee % | Developer Pool (80%) | Operations Pool (10%) | Network Pool (10%) |
|---|---|---|---|---|
| **Tier 1 ($0 – $10M)** | **2.00%** | 1.60% | 0.20% | 0.20% |
| **Tier 2 ($10M – $100M)** | **1.50%** | 1.20% | 0.15% | 0.15% |
| **Tier 3 ($100M – $500M)** | **1.00%** | 0.80% | 0.10% | 0.10% |
| **Tier 4 ($500M+)** | **0.50%** | 0.40% | 0.05% | 0.05% |

---

### Layer 2: Enterprise BaaP Node Licensing (Recurring SaaS)

For institutions and fintechs requiring deployment of the Conxian Gateway and Nexus behind their own corporate firewall:

1. **Community / Sandbox Node ($0/month)**:
   - Public endpoint routing (`gateway.conxian.org`).
   - Shared rate limits and standard community support (No SLA).

2. **Enterprise Private Gateway ($2,500 – $7,500/month)**:
   - Self-hosted Docker/Kubernetes container deployment behind corporate firewall.
   - Custom ISO 20022 banking normalizer & OData v4 callback engine.
   - Contractual 99.5% uptime SLA with business-hours technical support.

3. **Sovereign Private Nexus Node ($15,000 – $40,000/month)**:
   - Full multi-chain observation, MMR proof verification, and local execution enclave (AWS Nitro / Intel SGX TEE).
   - Bring-Your-Own (BYO) DeFi vault integration and custom risk parameter orchestration.
   - Dedicated contract SLA with transparent RCA delivery.

---

### Layer 3: Edge Compute & x402 Attestation Fees (Metered Utility)

Autonomous AI agents and edge applications interact via HTTP 402 (Payment Required) payment demands, settling per-request execution costs on-chain:

- **Hardware Enclave Attestation**: **$0.005 – $0.020** per cryptographic key generation / signing attestation proof.
- **Zero-Knowledge Compliance (ZKC) Proofs**: **$0.010 – $0.050** per risk verification proof generated by the Nexus proof solver.
- **ISO 20022 Financial Message Mapping**: **$0.002** per normalized banking payload processed through the Gateway.

---

## 3) Revenue Retention Scenarios ($200M BTC Volume Base)

On a **$200,000,000 raw escrow volume benchmark** (yielding $4,000,000 in gross fees), Conxian Labs' net retention varies based on operational scope:

```
┌──────────────────────────────────────────────────────────────────────────┐
│             NET CONXIAN LABS RETENTION ON $200M VOLUME                   │
├──────────────────────────────────────────────────────────────────────────┤
│ Scenario A: Pure Software Vendor (Ops Only) ──────► $400,000             │
│ Scenario B: Infrastructure Operator (Ops + Network) ─► $800,000          │
│ Scenario C: In-House Core Builder (Ops + Devs) ───► $3,600,000           │
│ Scenario D: Full Vertically Integrated Platform ──► $4,000,000           │
└──────────────────────────────────────────────────────────────────────────┘
```

1. **Pure Software Licensing (Base Scenario — $400,000 Retained)**: Conxian Labs collects the 10% Operations Pool fee. 80% goes to external developers, and 10% to independent validators.
2. **Operator Model ($800,000 Retained)**: Conxian Labs collects the 10% Operations Pool fee and operates the primary verification node network (10% Network Pool).
3. **Core Developer + Operator Model ($3,600,000 Retained)**: Conxian Labs operates core protocol applications (80% Dev Pool) and manages platform operations (10% Ops Pool).
4. **Complete In-House Execution ($4,000,000 Retained)**: Conxian Labs maintains first-party control across application development, operational management, and initial network routing nodes.

---

## 4) Financial Projection Scaling Matrix

| Metric / Milestone | Phase 1 (Initial Pilot) | Phase 2 (Growth Stage) | Phase 3 (Institutional Scale) |
|---|---|---|---|
| **Annual Escrow Volume** | $50,000,000 | $200,000,000 | $1,000,000,000 |
| **Active Enterprise Private Nodes** | 5 Nodes | 25 Nodes | 100 Nodes |
| **Annual x402 Compute Calls** | 1,000,000 calls | 10,000,000 calls | 100,000,000 calls |
| **Gross Escrow Fees (Avg 1.75%)** | $875,000 | $3,500,000 | $12,500,000 |
| **Node License Revenue (SaaS)** | $300,000 | $1,500,000 | $6,000,000 |
| **Edge Compute / Attestation Revenue**| $15,000 | $150,000 | $1,500,000 |
| **Total Top-Line Gross Revenue** | **$1,190,000** | **$5,150,000** | **$20,000,000** |
| **Developer Payouts (80% of Escrow)**| $700,000 | $2,800,000 | $10,000,000 |
| **Network Node Payouts (10% of Escrow)**| $87,500 | $350,000 | $1,250,000 |
| **Net Conxian Labs Operations + SaaS**| **$402,500** | **$2,000,000** | **$8,750,000** |

---

## 5) Sales Strategy & Pricing Positioning (TCO Advantage)

To win enterprise deals against standard cross-chain messaging solutions, sales conversations lead with Total Cost of Ownership (TCO) advantages:

1. **Eliminate Double-Sided Gas Friction**: Universal intent routing and local Gateway execution prevent clients from paying double-sided gas or relayer markups across destination chains.
2. **Zero-Custody Escrow Safety**: Instead of depositing capital into shared bridge vaults, clients keep capital in their own self-deployed private nodes or preferred DeFi vaults (Bring-Your-Own DeFi).
3. **Integrated Business Operating System (BOS)**: Enterprise clients purchase a complete Sovereign Autonomous Business (SAB) platform with built-in SLA boundaries, x402 agent billing, and ISO 20022 banking integration.

---

## Related Documents

- [Conxian SLA Policy](SLA.md)
- [Master Gap Register](GAPS.md)
- [Portfolio & Capability Matrix](PORTFOLIO.md)
- [BOS Knowledge Framework](BOS_KNOWLEDGE_FRAMEWORK.md)
