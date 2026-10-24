# System-Wide Evaluation & Agentic Transformation Blueprint (2026)

> **Reconciled status — 24 October 2026:** preserve the proposal below as historical research. Its “APPROVED & CANONICAL,” compliance, execution, percentages and capability labels are author assertions, not operating or independent acceptance. Current roles, authority and implementation gates follow the [monthly review](MONTHLY_RESEARCH_REVIEW_2026_10_24.md) and [capability roadmap](../architecture/ROADMAP_12_MONTH_CONTROL_PLANE.md). No new signing, evaluator, payout or automatic promotion authority is granted.
> **Document Identifier**: `ADR/ITIL5/CXIP::CXBIP/CXPIP/CXMIP/CXWIP/CXCIP/CXGIP/CXNIP`
> **Status**: APPROVED & CANONICAL
> **Scope**: Organization-Wide Architecture, Governance, Codebase & Runtime Surface
> **Author**: Conxian System Architecture & Agentic Task Force
> **Date**: October 2026

---

## 1. Executive Summary & Architectural Mandate

Conxian's Business-as-a-Platform (BaaP) architecture is built upon high-performance, deterministic infrastructure: asynchronous Rust gateways (`conxian-gateway`), gRPC synchronization verification nodes (`conxian-nexus`), TEE hardware enclave primitives (`conxius-enclave-sdk`), ISO 20022 compliance bridges, and rigorous CI/CD release controls.

While the underlying rails are engineered to serve autonomous AI labor via x402 and ERC-8183 job card escrows, much of the system operational surface—governance, setup, SLA arbitration, routing, and user interaction—remains human-centric and deterministic.

This specification establishes an organization-wide **Agentic Transformation Blueprint**, elevating Conxian from passive infrastructure into an **Agentic, AI-First Autonomous Business Stack**.

---

## 2. Org-Wide Improvement Proposal Taxonomy (CXIP Framework)

To coordinate autonomous agentic upgrades across all 8 active workspace repositories, Conxian defines a unified **Conxian Improvement Proposal (CXIP)** taxonomy mapped directly to repository owners:

| Improvement Proposal Identifier | Target Domain / Workspace Repository | Operational Focus & Agentic Surface |
|---------------------------------|--------------------------------------|-------------------------------------|
| **CXBIP** | `conxian-business` | OpenSpec resolvers, TEE executive officers, 80/10/10 yield automation, SLA governance |
| **CXPIP** | `conxius-platform` | Sovereign node orchestration, admin control plane, container runtime telemetry |
| **CXMIP** | `conxian_market` | Dynamic M2M bargaining protocol, ERC-8183 escrow arbitration, MCP server exposure |
| **CXWIP** | `conxius-wallet` | Delegated EIP-7710 command center, zero-secret-egress (ZSE) privacy filters |
| **CXCIP** | `lib-conxian-core` | Core cryptographic primitives, CJCS v2.0 schema resolution, zero-knowledge proofs |
| **CXGIP** | `conxian-gateway` | AI liquidity router, natural-language to ISO 20022 (`pacs.008`/`camt.053`) synthesizer |
| **CXNIP** | `conxian-nexus` | Self-healing multi-chain state reorg monitor, BitVM3 fraud proof dispatchers |

---

## 3. System-Wide Agentic Architecture Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONXIAN AGENTIC ARCHITECTURE MATRIX                  │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Current Infrastructure Core    │ Proposed Agentic / AI-First Elevation     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ BOS Governance & OpenSpec      │ Autonomous Spec Resolvers & TEE Officers   │
│ Market SDK Settlement & Escrow │ Dynamic Agent Bargaining & LLM Arbitration │
│ Gateway & ISO 20022 Middleware │ Natural Language Compliance & Liquidity    │
│ Enclave Key Management (SDK)   │ Ephemeral Self-Provisioning Agent Keyrings │
│ Nexus Universal Chain Proofs   │ Self-Healing Multi-Chain Drift Engine      │
│ Conxius Wallet & Access Layer  │ Delegated ERC-7710 Agent Command Center    │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 4. Pillar-by-Pillar Deep Architectural Specifications

### Pillar 1: Market & Labor Layer (`conxian_market` / `@conxian/market-sdk`) — CXMIP
* **Current State**: Programmatic 3-step TypeScript SDK methods (`createX402Demand`, `processX402PaymentAndLockEscrowWithAttestation`) with fixed fee schedules and manual CLI initialization (`conxian-agent-init`).
* **Agentic Elevation**:
  * **Dynamic Agent Bargaining Protocol**: Replace static x402 price tags with bidirectional M2M negotiation headers. Buyer and seller agents negotiate price, execution timeouts, and penalty thresholds in real time based on `fee_calculator.ts` node load metrics and mempool pressure.
  * **LLM-in-a-TEE Dispute Arbitration**: Move beyond hardcoded SLA timeout checks. Deploy TEE-isolated LLM arbiters (`conxius-enclave-sdk`) to evaluate subjective deliverables (e.g., code quality, research depth) against CJCS v2.0 job card criteria before triggering ERC-8183 escrow releases or refunds.
  * **Native Model Context Protocol (MCP) Tools**: Expose all 33 SDK capabilities directly as MCP servers so agents operating in Claude, AutoGen, LangGraph, or CrewAI can discover, lock escrow, and verify attestations without custom TypeScript wrapper code.

### Pillar 2: Governance & Operations (`conxian-business`) — CXBIP
* **Current State**: Static Markdown specifications (`OpenSpec`), manual pull-request promotion pipelines, and fixed M&A milestone tracking.
* **Agentic Elevation**:
  * **Autonomous Spec & Code Remediation**: Deploy autonomous maintenance agents that read code changes, evaluate OpenSpec delta compliance, and generate pull requests to keep public docs synced with Rust/TypeScript codebase realities.
  * **Active TEE Executive Agents**: Transform passive `AGENTS.md` documentation pointers into enclave-backed operational agents that autonomously audit treasury runway, monitor zero-secret-egress (ZSE) boundaries, and execute automated 80/10/10 yield splits (`bos_yield_splitter`).

### Pillar 3: Middleware & Gateway (`conxian-gateway`) — CXGIP
* **Current State**: Fixed Axum REST/gRPC routes, rigid ISO 20022 (`pacs.008`/`camt.053`) message parsers, and static rate limiting.
* **Agentic Elevation**:
  * **AI-First Liquidity & Rail Router**: Introduce an autonomous router that dynamically selects the optimal settlement rail (Lightning vs. sBTC vs. Fedimint vs. Base USDC) based on agent-specified budget, speed preferences, and real-time gas/mempool conditions.
  * **Natural Language to ISO 20022 Synthesizer**: Allow AI agents to submit unstructured, natural-language settlement instructions that the Gateway's compliance engine automatically converts into valid, audit-ready ISO 20022 banking messages (`pacs.008`, `pacs.002`, `camt.053`).

### Pillar 4: Cryptographic Security & Hardware Trust (`conxius-enclave-sdk`) — CXCIP
* **Current State**: Hardware enclave signing and vendor attestation (AWS Nitro, StrongBox KeyMint) invoked manually by developer applications.
* **Agentic Elevation**:
  * **Self-Provisioning Enclave Keyrings**: Enable autonomous agents deploying on new compute nodes to self-initialize isolated TEE enclaves, generate hardware keypairs, and obtain "Verified by Conxian" certificates from Nexus without human credential management.
  * **Delegated Autonomous Spend Limits**: Allow human owners to set cryptographically enforced spending rules (e.g., max 50,000 sats/hour or EIP-7710 allowances) within the enclave, letting the agent sign x402 authorizations autonomously within strict parameters.

### Pillar 5: Universal Proof & Observation Layer (`conxian-nexus`) — CXNIP
* **Current State**: High-availability verification node producing Merkle Mountain Range (MMR) state roots, ZKCP, FROST, and BitVM3 verifiers.
* **Agentic Elevation**:
  * **Self-Healing Multi-Chain Monitor**: Enable Nexus safety workers (`nexus-safety`) to autonomously detect cross-chain synchronization drift (>2 blocks), automatically dispatch RBF/CPFP fee bumps, or initiate BitVM3 fraud proof challenges when execution delays threaten job card SLAs.

### Pillar 6: Client & Wallet Surface (`conxius-wallet`) — CXWIP / CXPIP
* **Current State**: Human-centric mobile app requiring manual key management and transaction approvals.
* **Agentic Elevation**:
  * **Agentic Delegation Dashboard**: Refactor Conxius Wallet into a management hub for human-to-agent delegation. Users can assign wallet sub-accounts, monitor active ERC-8183 escrows, view agent labor revenue, and adjust zero-secret-egress (ZSE) privacy filters.

---

## 5. Actionable Prioritization Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AGENTIC ROADMAP PRIORITIZATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 1: MCP & Agent Discovery (1–30 Days)                                 │
│  • Package @conxian/market-sdk as a native MCP server for all LLMs.         │
│  • Expose dynamic x402 bargaining headers in Gateway middleware.            │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 2: Enclave Guardrails & Self-Provisioning (30–90 Days)               │
│  • Implement EIP-7710/ERC-8183 spending guardrails inside Enclave SDK.     │
│  • Automate TEE key generation & "Verified by Conxian" proof issuance.      │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: Autonomous Operations & Dispute Arbitration (90+ Days)            │
│  • Deploy TEE-isolated LLM dispute arbitrators for subjective job cards.    │
│  • Enable self-healing state reorg & fee-bumping in Conxian Nexus.          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Verification & ITIL5 Governance Compliance

This specification complies with ITIL v5 Service Value System (SVS) standards and Conxian Release Engineering policies. All agentic components deployed under CXIP proposals must pass automated static verification (`python3 scripts/bos_repo_check.py`), zero-secret-egress audits, and hardware attestation checks prior to production promotion.
