# Conxian Market × BOS Integration Research
> **Purpose**: Identify alignment points and integration gaps between `conxian_market` and Business Operating System (BOS)
> **Generated**: 2026-07-14
> **Status**: Initial Research

---

## 1. Executive Summary

The `conxian_market` submodule represents the **Settlement Core** for autonomous AI labor. The BOS provides the **Operational Framework** and **Knowledge Architecture** for the entire ecosystem. Integration research reveals strong alignment in core principles with specific gaps in implementation and documentation.

### Key Finding
**Alignment**: 85% - Core principles align perfectly (DeFi-Agnostic, Sovereign AI, Federated Network)
**Gaps**: Critical economic stubs, documentation synchronization, Linear issue tracking

---

## 2. Core Principle Alignment Matrix

| Principle | Market Docs | BOS Framework | Status |
|-----------|-------------|---------------|--------|
| **DeFi-Agnostic Orchestration** | ✅ ROADMAP.md: "Orchestrate, don't recreate" | ✅ BOS: External rail integration | ✅ ALIGNED |
| **BYOK/Sovereign AI** | ✅ GOVERNANCE.md: "BYOK mandate" | ✅ AGENTS.md: Hardware-backed signing | ✅ ALIGNED |
| **MCP-Native** | ✅ GOVERANCE.md: "MCP Native" | ✅ Nexus/Gateway: MCP support | ✅ ALIGNED |
| **ZK-Compliant** | ✅ GOVERANCE.md: "ZK-Proofs" | ✅ lib-conxian-core: ZKC support | ✅ ALIGNED |
| **80/10/10 Yield Matrix** | ✅ GOVERANCE.md: "Builder Revenue Matrix" | ⚠️ Stubs exist (CON-1427) | 🔴 GAP |
| **On-Chain Governance** | ✅ GOVERANCE.md: "DAO-Governed" | ⚠️ Admin-Key control persists | 🔴 GAP |

---

## 3. Integration Architecture

### 3.1 Market → BOS Dependencies

```
conxian_market (Settlement Core)
├── Settlement: CON-1427 (80/10/10 fee collection) ← BOS: CONXIAN_UNIFIED_THEORY
├── Escrow: ERC-8183 ← BOS: DAO_GOVERNANCE_SPEC
├── Unit of Account: CON-1425 (CXD stablecoin) ← BOS: Treasury Operations
├── Sovereign Infrastructure: BYOK, MCP, ZK ← BOS: Security Patterns
└── Marketplace Discovery: Reputation Registry ← BOS: Linear Task Inventory
```

### 3.2 BOS → Market Dependencies

```
conxian_business (Operational Framework)
├── Job Card Standard (CJCS v2.0) → CONXIAN_MARKET: "AI Labor Exchange"
├── Operating Lane Boundaries → CONXIAN_MARKET: "Agent Constraints"
├── Commercial Packaging Doctrine → CONXIAN_MARKET: "Yield Matrix Tiers"
└── Trust & Readiness Verification → CONXIAN_MARKET: "Builder Network Quality"
```

---

## 4. Critical Gaps & Risks

### 4.1 Revenue Blockers (P0)

| Issue | Description | Impact | Reference |
|-------|-------------|--------|-----------|
| **CON-1427** | Protocol fee collection is a "no-op" | Cannot capture platform value | `org_reality_issue_audit.md` |
| **CON-1425** | CXD stablecoin lacks peg mechanism | Broken unit of account | `org_reality_issue_audit.md` |
| **CON-1434** | 33% of contracts are stubs | Trust deficit in marketplace | `org_reality_issue_audit.md` |

### 4.2 Security Gaps (P1)

| Issue | Description | Impact | Reference |
|-------|-------------|--------|-----------|
| **CON-1422** | 73+ Admin variables | Sovereign promise compromised | `vulnerability_registry` |
| **CON-1424** | Access control tautology bugs | Anyone can pause system | `vulnerability_registry` |

### 4.3 Documentation Gaps (P2)

| Gap | Location | Recommended Action |
|-----|----------|-------------------|
| Market not listed in BOS repository registry | `BOS_KNOWLEDGE_FRAMEWORK.md` | Add REPO-MARKET entry |
| Cross-repo dependency map missing | Multiple docs | Create `CROSS_REPO_DEPENDENCY_MAP.md` |
| CON-1427/CON-1425 status not in BOS | Linear not synced to Git | Add to weekly automation |

---

## 5. Alignment Verification: Vision vs. Implementation

### 5.1 "AI Office" Alignment (Market Enhancement Strategy)

| Vision Item | Market Status | BOS Gap |
|-------------|--------------|---------|
| **Thin Orchestrator (MCP)** | ✅ MCP specified | ⚠️ Nexus MCP integration incomplete |
| **BYOK/Edge Inference** | ✅ BYOK mandated | ⚠️ SDK implementation pending |
| **80/10/10 Yield** | ✅ Specified | 🔴 CON-1427 blocking |
| **ERC-8183 Escrow** | ✅ Specified | 🔴 Contract stub only |

### 5.2 "Multi-Dimensional Scaling" Alignment

| Component | Vision | Implementation | Gap |
|-----------|--------|----------------|-----|
| **Hub Coordinator** | O(1) cost scaling | In progress (Nexus) | Medium |
| **Edge Inference** | User bears cost | SDK not released | High |
| **External Rails** | Fedimint, Citrea | Gateways incomplete | Medium |

---

## 6. Recommended Integration Actions

### 6.1 Immediate (This Sprint)

1. **Add conxian_market to BOS Knowledge Framework**
   - Add `REPO-MARKET` entry with ID sequence
   - Link to yield matrix, escrow spec, governance

2. **Sync Linear Issues to Market Docs**
   - CON-1427 status → Governance.md
   - CON-1425 status → Roadmap.md

3. **Create Cross-Repo Dependency Map**
   - Map Market → Gateway → Nexus dependencies
   - Update `ECOSYSTEM_KNOWLEDGE_BASE.md`

### 6.2 Short-Term (Next Sprint)

4. **Implement CON-1427 (Fee Collection)**
   - Unblocks platform value capture
   - Enables 80/10/10 revenue distribution

5. **Implement CON-1425 (CXD Peg)**
   - Establishes functional unit of account
   - Required for stable marketplace pricing

6. **Transition Admin-Key to DAO Governance**
   - Fulfills Sovereign mandate
   - Aligns with CON-1439 roadmap item

### 6.3 Medium-Term (Phase 2)

7. **Publish @conxian/sdk npm package** (CON-1440)
8. **Launch Developer Sandbox** (CON-1437)
9. **Integrate Nexus Glass Node** into Market discovery UI

---

## 7. Repository Relationships

### 7.1 Current BOS Registry (from BOS_KNOWLEDGE_FRAMEWORK.md)

| ID | Repo | Purpose | Market Dependency |
|----|------|---------|-------------------|
| REPO-001 | conxian-business | Knowledge-ops | Owns integration standards |
| REPO-002 | conxian-nexus | Settlement layer | Market → Nexus state |
| REPO-003 | conxian-gateway | ISO 20022 bridge | Market → Gateway rails |
| REPO-004 | conxius-wallet | Client wallet | Market → Wallet settlement |
| REPO-005 | conxius-platform | Dev orchestration | Market → Sandbox |
| REPO-006 | conxius-enclave-sdk | TEE abstraction | Market → BYOK |
| REPO-007 | lib-conxian-core | Crypto primitives | Market → ZKC, SYI |

### 7.2 Missing Entry

| ID | Repo | Purpose |
|----|------|---------|
| REPO-**TBD** | conxian_market | AI Labor Exchange / Settlement Core |

---

## 8. Next Steps

1. **Request Linear API access** to sync CON-1427/CON-1425 status
2. **Create PR** to add `REPO-MARKET` to BOS_KNOWLEDGE_FRAMEWORK.md
3. **Schedule integration sync** between Market team and BOS ops

---

## 9. References

- **Vision**: `conxian-market/ROADMAP.md`, `vision_alignment_check.md`
- **Governance**: `conxian-market/docs/GOVERNANCE.md`
- **BOS**: `docs/BOS_KNOWLEDGE_FRAMEWORK.md`, `OPERATING_LANE_BOUNDARIES.md`
- **Critical Issues**: `conxian-market/docs/research/org_reality_issue_audit.md`
- **Strategy**: `conxian-market/docs/research/market_enhancement_strategy.md`

---

*Research by OpenHands agent on behalf of Conxian-Labs (Pty) Ltd*
