# Conxian Labs Knowledge Base Gap Analysis & Upgrade Plan
> Generated: 2026-07-06 | Status: DRAFT

## Executive Summary

This document synthesizes findings from the Conxian Labs knowledge base against the 27 open issues in `Conxian/Conxian` and the ecosystem requirements for a production-grade, sovereign-first financial platform.

**Critical Finding:** The protocol has fundamental architectural issues that cannot be resolved through documentation alone. These require code-level remediation aligned with Clarity best practices, DAO governance patterns, and the Conxian Unified Theory v2.0.

> **Current-status boundary (2026-07-25):** Parts I–VI preserve the 2026-07-06 historical baseline and original upgrade plan. The BOS graph now exists, the governance inventory has been reconciled in [Part VII](#part-vii-con-1421-governance-stub-reconciliation-2026-07-21), and the revenue-collection state has been reconciled in [Part VIII](#part-viii-con-1542-revenue-automation-handoff-2026-07-25). Do not read older “missing,” blanket “16 stubs,” or wholly absent fee-collection statements as current closure or inventory proof.

---

## Part I: Knowledge Base Audit

### 1.1 Existing Knowledge Assets

| Asset | Location | Coverage | Currency |
|-------|----------|----------|----------|
| **AGENTS.md** | `conxian-business/AGENTS.md` | ✅ Comprehensive | ✅ Current |
| **CONXIAN_UNIFIED_THEORY_v2** | `lib-conxian-core/docs/` | ✅ Mathematical framework | ✅ Current |
| **Knowledge Maps** | `conxian-gateway/docs/research/KNOWLEDGE_MAP.md` | ⚠️ Partial | ⚠️ Needs update |
| **Security Advisory** | `lib-conxian-core/docs/ADVISORY_REPORT_2026_07_06.md` | ✅ Technical | ✅ Current |
| **GAP_ANALYSIS** | `lib-conxian-core/docs/GAP_ANALYSIS_AND_SCORING.md` | ✅ Scoring | ✅ Current |
| **BOS_KNOWLEDGE_GRAPH.md** | ✅ Present | ✅ Current CON-1421 reconciliation | `BOS_KNOWLEDGE_GRAPH.md` |
| **Protocol Upgrade Pattern Guide** | ❌ Missing | ❌ Critical gap | N/A |
| **DAO Governance Specification** | ❌ Missing | ❌ Critical gap | N/A |
| **ISO 20022 Integration Spec** | ❌ Missing | ❌ Critical gap | N/A |

### 1.2 Knowledge Graph Status

The 2026-07-06 baseline recorded the mandated BOS Knowledge Graph as missing. It is now present at `conxian-business/BOS_KNOWLEDGE_GRAPH.md`; the current structured reconciliation is recorded in the dated digest for CON-1421.

**Required Action:** Maintain the graph as the authoritative entity, relationship, decision, and issue-resolution record.

---

## Part II: Critical Issues Analysis vs. Knowledge Base

### 2.1 Conxian/Conxian Issues Mapped to Required Knowledge

| Issue | Severity | Required Knowledge | Current Coverage |
|-------|----------|-------------------|-----------------|
| Historical `collect-protocol-fees` no-ops | CRITICAL | Clarity tokenomics patterns and deployment evidence | Partially remediated: collector and lending migration merged; actual DEX settlement and live deployment evidence remain unresolved (Part VIII) |
| `CXLP` mint/burn broken | CRITICAL | SIP-010 trait compliance | ❌ Missing |
| `CXD` no peg mechanism | CRITICAL | Stablecoin design patterns | ❌ Missing |
| No upgrade mechanism | CRITICAL | Clarity upgrade patterns | ❌ Missing |
| Single deployer key | CRITICAL | Multisig + DAO patterns | ⚠️ Partial |
| `pausable.clar` zero ACL | CRITICAL | Access control patterns | ❌ Missing |
| 71 stubs (33%) | HIGH | Contract completion guide | ❌ Missing |
| Historical “16 governance stubs” claim | MEDIUM | Typed governance inventory and decision record | Reconciled in Part VII; broader gap remains open |

### 2.2 Pattern Library Gaps

Based on research findings from Stacks documentation and DAO frameworks:

#### Gap #1: Upgrade Mechanism Patterns
**Current State:** No Clarity upgrade pattern documentation exists in the knowledge base.

**Required Patterns:**
```
1. Immutable redeploy + migration (auditability-focused)
2. Modular/registry pattern (upgradeability-focused)
3. Governance-controlled replacement (decentralization-focused)
4. Multisig + timelock (operator-controlled)
```

**Source Evidence:**
- Stacks Cookbook: https://docs.stacks.co/cookbook/clarity/example-contracts
- DAO frameworks: https://github.com/DA0-DA0/dao-contracts
- Operator patterns: https://forum.stacks.org/t/identicon-for-contracts/18637

#### Gap #2: Access Control Patterns
**Current State:** `pausable.clar` has no access control - anyone can call `set-paused`.

**Required Pattern:**
```clarity
;; SECURE: Access-controlled pausable
(define-constant PAUSE_ADMIN 'ST_PAUSE_ADMIN)

(define-public (set-paused (new-state bool))
  (begin
    (asserts! (is-eq tx-sender PAUSE_ADMIN) ERR_UNAUTHORIZED)
    (var-set paused new-state)
    (ok true)
  )
)
```

**Source Evidence:** CertiK Clarity best practices checklist

#### Gap #3: Fee Collection Patterns
**Historical State:** The 2026-07-06 baseline found `collect-protocol-fees` paths that returned `(ok true)` without an actual token transfer.

**Evidence-accurate State (2026-07-25):** The canonical scheduled collector in [Conxian PR #544](https://github.com/Conxian/Conxian/pull/544), lending-interest migration in [Conxian PR #556](https://github.com/Conxian/Conxian/pull/556), and fail-closed DEX hardening in merged [Conxian PR #572](https://github.com/Conxian/Conxian/pull/572) at landed commit [`daaea0cd6eab33a0f167cf16c09eee227311dcf4`](https://github.com/Conxian/Conxian/commit/daaea0cd6eab33a0f167cf16c09eee227311dcf4) are merged source evidence. The 200/150/100-bps implementation in PRs #544/#556 does not by itself ratify that schedule or supersede the separate observed, non-immutable 100-bps governance boundary in Conxian #538 / CON-1542; fee-policy reconciliation remains a governed decision. PR #572 removes false-success DEX collection when segregated fee custody is unavailable, but actual asset-segregated DEX settlement remains unresolved. These source artifacts do not establish deployment or live revenue.

**Remaining Pattern Gap:** Define and verify asset-segregated DEX fee custody and settlement in the protocol repository, then produce independent deployment and on-chain realization evidence. Do not infer production realization from merged code, plans, routing, or observation records.

---

## Part III: ISO 20022 Integration Knowledge Gap

### 3.1 Current State
No comprehensive ISO 20022 integration specification exists in the knowledge base.

### 3.2 Required Knowledge Components

| Component | Description | Source |
|-----------|-------------|--------|
| **Message Mapping** | pain.001 → pacs.008 → camt.054 flow | BIS CPM-I d218 |
| **OP_RETURN Schema** | On-chain commitment format | BIP-0110, BIP-0074 |
| **Lightning Integration** | BOLT11 invoice settlement | Lightspark research |
| **Travel Rule** | VASP KYC data sharing | FATF guidance |
| **Tokenized Settlement** | Wrapped BTC DTI mapping | ISO-24165 |

### 3.3 Knowledge Map for the gateway service

```
┌─────────────────────────────────────────────────────────────┐
│                    ISO 20022 Message Flow                    │
├─────────────────────────────────────────────────────────────┤
│  pain.001 (Customer Credit Transfer Init)                    │
│       ↓                                                     │
│  [Gateway service: Validation, KYC, FX]                     │
│       ↓                                                     │
│  pacs.008 (Financial Institution Credit Transfer)           │
│       ↓                                                     │
│  [Settlement Adapter: BTC/Lightning/Wrapped]                 │
│       ↓                                                     │
│  camt.054 (Credit/Debit Notification)                       │
└─────────────────────────────────────────────────────────────┘

On-Chain Commitment:
┌─────────────────────────────────────────────────────────────┐
│  OP_RETURN: SHA256(pacs.008_hash + timestamp + LEI)         │
│  BIP-322 Signed Message for non-repudiation                  │
│  ISO Digital Token Identifier (DTI) for wrapped assets       │
└─────────────────────────────────────────────────────────────┘
```

**Source Evidence:**
- ISO 20022 Best Practices: https://iso20022.org/sites/default/files/media/file/ISO_20022_and_Web_APIs_An_Implementation_Best_Practices_White_Paper_10June2025.pdf
- Chainlink ISO integration: https://chain.link/article/iso-20022-integration

---

## Part IV: DAO Governance Specification Gap

### 4.1 Historical baseline and current boundary
The 2026-07-06 baseline stated that no DAO governance specification existed and repeated the “16 of 28” issue wording. The original issue body names 15 contracts; `proposal-engine-trait.clar` is the likely omitted 16th entry, and six listed entries are partial skeletons rather than blank stubs. The current typed reconciliation and the scoped community-voting decision are recorded in Part VII and `BOS_KNOWLEDGE_GRAPH.md`.

### 4.2 Required Governance Architecture

Based on research from Stacks SIP process and DAO frameworks:

```
┌─────────────────────────────────────────────────────────────┐
│                 Governance Hierarchy                         │
├─────────────────────────────────────────────────────────────┤
│  Level 1: IMMUTABLE (Cannot change)                         │
│  ├── Token supply cap                                       │
│  ├── Core tokenomics constants                              │
│  ├── Upgrade mechanism type                                 │
│  └── Treasury multisig threshold                            │
├─────────────────────────────────────────────────────────────┤
│  Level 2: GOVERNANCE-CONTROLLED                            │
│  ├── Operational parameters (thresholds, fees)              │
│  ├── New contract deployments                               │
│  ├── Treasury disbursements                                 │
│  └── Emergency pause (with timelock)                       │
├─────────────────────────────────────────────────────────────┤
│  Level 3: OPERATOR-CONTROLLED (DAO can override)            │
│  ├── Daily parameter tuning                                 │
│  ├── Bug fixes via migration                                │
│  └── Performance optimizations                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Voting Mechanism Pattern

```clarity
;; SECURE: Timelocked governance proposal
(define-constant PROPOSAL_TIMELOCK u144) ;; ~24 hours
(define-constant QUORUM_THRESHOLD u50000000000) ;; 50% of supply

(define-public (execute-proposal (proposal-id uint))
  (let (
    (proposal (unwrap! (map-get? proposals proposal-id) ERR_NOT_FOUND))
    (voting-ends (+ (get created-at proposal) PROPOSAL_TIMELOCK))
  )
    (asserts! (>= stacks-block-height voting-ends) ERR_TIMELOCK_ACTIVE)
    (asserts! (>= (get votes-for proposal) QUORUM_THRESHOLD) ERR_NO_QUORUM)
    (execute-proposal-actions proposal-id)
  )
)
```

**Source Evidence:**
- Stacks SIP Process: https://github.com/stacksgov/sips
- Voting guide: https://stacks.org/nakamoto-voting-guide

---

## Part V: Upgrade Path Recommendation

### 5.1 Immediate Actions (Week 1-2)

| Priority | Action | Knowledge Gap Addressed |
|----------|--------|------------------------|
| P0 | Maintain `BOS_KNOWLEDGE_GRAPH.md` | Mandated authoritative entity and decision record; initial creation is complete |
| P0 | Fix `pausable.clar` access control | CRITICAL security |
| P1 | Complete asset-segregated DEX fee settlement and deployment evidence | Revenue realization; collector and lending migration are already merged |
| P1 | Create upgrade mechanism spec | Modular/registry pattern |
| P2 | Create DAO governance spec | 16 stub contracts |

### 5.2 Knowledge Asset Creation Plan

```
PHASE 1: Foundation (Week 1)
├── Create: BOS_KNOWLEDGE_GRAPH.md
├── Create: SECURITY_PATTERNS.md (Clarity access control, pausable, multisig)
├── Create: UPGRADE_MECHANISMS.md (Registry pattern, migration)
└── Update: AGENTS.md with new pattern references

PHASE 2: Protocol (Week 2-3)
├── Create: DAO_GOVERNANCE_SPEC.md (Voting, timelock, treasury)
├── Create: TOKENOMICS_PATTERNS.md (SIP-010, fee collection, CXD/CXLP)
└── Create: ISO_20022_INTEGRATION_SPEC.md (Message mapping, OP_RETURN)

PHASE 3: Ecosystem (Week 4+)
├── Create: CXN_VALIDATOR_ONBOARDING.md
├── Create: TEE_ATTESTATION_GUIDE.md
└── Create: DEVELOPER_SANDBOX_TUTORIAL.md
```

---

## Part VI: Evidence Sources

### Academic & Standards
- [BIS ISO 20022 Requirements](https://bis.org/cpmi/publ/d218.pdf)
- [ISO 20022 Web APIs White Paper (2025)](https://iso20022.org/sites/default/files/media/file/ISO_20022_and_Web_APIs_An_Implementation_Best_Practices_White_Paper_10June2025.pdf)
- [ISO Digital Token Identifier (DTI)](https://21x.eu/21x-implements-the-iso-digital-token-identifier-dti-standard)

### Stacks & Clarity
- [Clarity Language Overview](https://github.com/clarity-lang/overview)
- [Clarity 4 Announcement](https://stacks.co/blog/clarity-4-bitcoin-smart-contract-upgrade)
- [SIP-033 Clarity 4](https://stacks.org/sip-033-clarity-4)
- [Stacks Cookbook](https://docs.stacks.co/cookbook/clarity/example-contracts)
- [CertiK Clarity Best Practices](https://www.certik.com/resources/blog/clarity-best-practices-and-checklist)
- [Stacks SIP Process](https://github.com/stacksgov/sips)

### Bitcoin & Cross-Chain
- [BIP-322 Generic Signed Message](https://bips.dev/322)
- [BIP-0074 PSBT](https://github.com/bitcoin/bips/blob/master/bip-0074.mediawiki)
- [Lightspark ISO 20022](https://lightspark.com/glossary/iso-20022)
- [Chainlink ISO Integration](https://chain.link/article/iso-20022-integration)
- [sBTC Security Review](https://clarityalliance.org/reports/sbtc)

### DAO & Governance
- [DAO-DAO (CosmWasm)](https://github.com/DA0-DA0/dao-contracts)
- [Velocity DAO (Clarity)](https://github.com/SaadTahir28/Velocity-DAO-Clarity)
- [Nakamoto Voting Guide](https://stacks.org/nakamoto-voting-guide)

---

## Part VII: CON-1421 Governance Stub Reconciliation (2026-07-21)

This section supersedes the current-status wording in the 2026-07-06 baseline while preserving that baseline for historical traceability. The authoritative entity, relationship, and decision digest is [BOS_KNOWLEDGE_GRAPH.md](../BOS_KNOWLEDGE_GRAPH.md).

### Inventory correction

- The [CON-1421 Linear issue](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs) and [Conxian #463](https://github.com/Conxian/Conxian/issues/463) body name 15 contracts, not 16.
- `proposal-engine-trait.clar` is the likely omitted 16th governance-gap entry.
- Six listed entries are partial skeletons rather than blank stubs. Future reporting must distinguish blank stubs, partial skeletons, implemented-but-under-review contracts, deferred architecture, and intentionally inactive source.

### Scoped remediation and review boundary

- [`community-voting-engine.clar`](https://github.com/Conxian/Conxian/blob/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1/contracts/governance/community-voting-engine.clar) is implemented in [protocol PR #521](https://github.com/Conxian/Conxian/pull/521) at exact audited head [`90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1`](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1).
- PR #521 is open, clean, mergeable, and currently reports all checks passing. It remains **under review** until merged into `main`; the parent repository pin is therefore **pinned for review**, not deployed or merged.
- The community-voting path was selected over isolated `upgrade-controller` work because it has no production callers, documented requirements, and a complete self-contained vertical. `upgrade-controller.clar` depends on proposal/timelock plumbing and overlaps the active [Conxian #499](https://github.com/Conxian/Conxian/issues/499) scope.

### Implemented behavior recorded at the audited head

The reviewed community-voting engine provides:

- dynamic `operational-treasury` route checks for the CXVG token and compliance adapter;
- real SIP-010 CXVG escrow rather than a mock balance update;
- compliance checks at proposal creation and voting;
- future start blocks and bounded voting windows;
- aggregate total-supply snapshots with a safe cap on cumulative escrow;
- quorum and approval thresholds with strict tie failure;
- permissionless finalization after the exclusive voting window;
- historical, one-time stake claims that remain tied to the proposal’s stored token principal;
- no arbitrary proposal execution or treasury withdrawal in the voting engine; and
- reputation weighting explicitly deferred until a trustworthy source and rules are independently reviewed.

### Remaining gaps and non-closure

- `upgrade-controller.clar` and `proposal-engine-trait.clar` remain stubs/deferred, and the other governance entries require their own typed status.
- The existing execution-oriented path remains `proposal-engine → proposal-registry → proposal-executor → timelock`; community voting is a separate non-executing ledger.
- The clean PR #521 and the parent pin do not fully resolve the broader governance backlog. The historical [#463 umbrella](https://github.com/Conxian/Conxian/issues/463) is not treated as fully resolved by implication.
- No protocol source or PR #521 changes are made in this parent-repository task; only the parent gitlink and knowledge records are updated.

### Canonical evidence

| Evidence | Link |
|----------|------|
| Linear work item | [CON-1421](https://linear.app/conxian-labs/issue/CON-1421/medium-16-of-28-governance-contracts-are-stubs) |
| Historical umbrella | [Conxian #463](https://github.com/Conxian/Conxian/issues/463) |
| Active overlap | [Conxian #499](https://github.com/Conxian/Conxian/issues/499) |
| Implementation PR | [Conxian PR #521](https://github.com/Conxian/Conxian/pull/521) |
| Exact protocol head | [`90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1`](https://github.com/Conxian/Conxian/commit/90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1) |
| Parent knowledge graph | [`BOS_KNOWLEDGE_GRAPH.md`](../BOS_KNOWLEDGE_GRAPH.md) |

---

## Part VIII: CON-1542 Revenue Automation Handoff (2026-07-25)

This section supersedes the current-status interpretation of the 2026-07-06 fee-collection baseline while preserving the original defect record. The authoritative typed entity, relationship, status, and decision digest is [BOS_KNOWLEDGE_GRAPH.md](../BOS_KNOWLEDGE_GRAPH.md).

### Ownership boundary

- [`Conxian/Conxian`](https://github.com/Conxian/Conxian) owns protocol economics, Clarity implementation, deployment policy, and fee-bearing behavior.
- [`Conxian/conxius-platform`](https://github.com/Conxian/conxius-platform) owns observation, routing, and runbook integration; it does not own custody or protocol economics. Merged [platform PR #1197](https://github.com/Conxian/conxius-platform/pull/1197) is observation evidence only.
- [`Conxian/conxian-business`](https://github.com/Conxian/conxian-business) owns governance, knowledge crystallization, and evidence classification; it does not implement protocol contracts.

### Evidence classification

| Artifact | Status on 2026-07-25 | What it establishes | What it does not establish |
|----------|----------------------|---------------------|----------------------------|
| [Protocol PR #544](https://github.com/Conxian/Conxian/pull/544) | **MERGED** | Canonical scheduled protocol fee collector with a 200/150/100-bps implementation exists in protocol source. | Fee-policy ratification, supersession of the observed 100-bps governance boundary, deployment, on-chain execution, or live revenue. |
| [Protocol PR #556](https://github.com/Conxian/Conxian/pull/556) | **MERGED** | Lending-interest collection migrated to that scheduled implementation. | Fee-policy ratification, final approval of either schedule, DEX settlement, or live lending revenue. |
| [Protocol PR #572](https://github.com/Conxian/Conxian/pull/572) at landed commit [`daaea0cd6eab33a0f167cf16c09eee227311dcf4`](https://github.com/Conxian/Conxian/commit/daaea0cd6eab33a0f167cf16c09eee227311dcf4) | **MERGED** | DEX collection fails closed instead of reporting false success when segregated fee custody is unavailable. | Asset-segregated DEX settlement, deployment, or actual DEX fee transfer. |
| Actual DEX settlement | **UNRESOLVED** | No production-realization claim is approved. | Asset-segregated fee custody, transfer, or revenue. |
| Live deployment and revenue evidence | **UNRESOLVED** | Production status remains unproven. | Deployed collector execution or realized revenue. |

### Decisions and non-goals

- Never infer production realization from code, a deployment plan, routing, or observation evidence.
- Never transfer from unsegregated DEX balances that may include LP or user assets; unsupported custody paths fail closed.
- Never apply both legacy and canonical charges to the same fee base.
- Treat fee-policy reconciliation as a separate governed decision: PRs #544/#556 are merged source evidence only, while Conxian #538 / CON-1542 retain the observed 100-bps baseline as a non-immutable governance boundary rather than final policy approval.
- CON-1542 does not approve a founder allocation, beneficiary, custody route, rate, or allocation semantics.
- This business-repository handoff does not change protocol code, deployment plans, rates, addresses, or secrets. It advances only the `Conxian` submodule gitlink from `90ef8a2f883ddab7cb0cfd00f68ba4d829f0a8e1` to the validated landed remediation commit `daaea0cd6eab33a0f167cf16c09eee227311dcf4`.

### Canonical evidence

| Evidence | Link |
|----------|------|
| Linear policy handoff | [CON-1542](https://linear.app/conxian-labs/issue/CON-1542/handoff-own-and-harden-revenue-automation-policy-from-conxius-platform) |
| Protocol handoff | [Conxian #538](https://github.com/Conxian/Conxian/issues/538) |
| Historical defect | [Conxian #469](https://github.com/Conxian/Conxian/issues/469) |
| Canonical collector | [Conxian PR #544](https://github.com/Conxian/Conxian/pull/544) |
| Lending migration | [Conxian PR #556](https://github.com/Conxian/Conxian/pull/556) |
| Merged fail-closed DEX hardening | [Conxian PR #572](https://github.com/Conxian/Conxian/pull/572) |
| Platform observation boundary | [conxius-platform PR #1197](https://github.com/Conxian/conxius-platform/pull/1197) |

---

## Appendix A: Issue → Knowledge Gap Mapping

| GitHub Issue | Root Cause | Required Pattern | Knowledge Doc |
|--------------|------------|------------------|---------------|
| #469 historical collect-fees no-ops | Collector and lending paths merged; DEX settlement and live deployment evidence unresolved | Asset-segregated fee custody, fail-closed settlement, and evidence classification | Part VIII + BOS knowledge graph |
| #468 CXLP mint/burn | Trait implementation gap | SIP-010 ft-trait | TOKENOMICS_PATTERNS.md |
| #467 CXD no peg | No price oracle | Pyth/Stacks oracle | ORACLE_INTEGRATION.md |
| #465 No upgrade | Design gap | Registry pattern | UPGRADE_MECHANISMS.md |
| #464 Single deployer | No multisig | N-of-M multisig | SECURITY_PATTERNS.md |
| #472 pausable ACL | Missing assert | Access control | SECURITY_PATTERNS.md |
| #470 rug-pull | Direct transfer | Treasury governance | DAO_GOVERNANCE_SPEC.md |

---

## Appendix B: Action Items

- [x] **CREATE / MAINTAIN** `BOS_KNOWLEDGE_GRAPH.md` (entity extraction and dated decision digests)
- [ ] **CREATE** `SECURITY_PATTERNS.md` (access control, multisig, pausable)
- [ ] **CREATE** `UPGRADE_MECHANISMS.md` (registry pattern, migration)
- [ ] **CREATE** `DAO_GOVERNANCE_SPEC.md` (voting, timelock, treasury)
- [ ] **CREATE** `TOKENOMICS_PATTERNS.md` (SIP-010, fee collection, stablecoin)
- [ ] **CREATE** `ISO_20022_INTEGRATION_SPEC.md` (message mapping, OP_RETURN)
- [ ] **FIX** `pausable.clar` access control (PR to Conxian repo)
- [ ] **COMPLETE** asset-segregated DEX fee settlement and independent live deployment/revenue evidence (collector and lending migration are merged)
- [ ] **FIX** `CXLP` SIP-010 trait compliance (PR to Conxian repo)
- [ ] **UPDATE** AGENTS.md with pattern doc references

---

*Generated by OpenHands Strategic Council per Conxian Unified Theory v2.0*
*Next session: Debate implementation priority of Phase 1 knowledge assets*
