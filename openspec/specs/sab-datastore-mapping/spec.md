# SAB Datastore Mapping Specification

## 1. Purpose
This specification translates the Conxian Sovereign Autonomous Business (SAB) current-state inventory into target-state datastore decisions. It defines the mapping of major data domains to their preferred sovereign targets, verifiable query layers, and append-only record systems.

## 2. Scope
- Mapping transactional application state.
- Mapping proof-oriented analytics.
- Mapping immutable governance and audit records.
- Identifying central versus edge responsibilities.

## 3. Requirements

### 3.1. Major Data Domain Mappings

| Data Domain | Datastore Type | Preferred Target | Rationale |
| :--- | :--- | :--- | :--- |
| **Transactional Application State** | Sovereign Target | **Neon (PostgreSQL)** + **Stacks L1 (State Roots)** | High-throughput required for Conxian Nexus block sync, MMR node updates, and real-time settlement logic. State roots are periodically anchored to Stacks L1 for sovereign finality. |
| **Proof-Oriented Analytics** | Verifiable Query Layer | **Supabase** | Provides rich SQL query capabilities for historical yield tracking, deployment efficiency metrics, and runway analysis. Verifiable against L1 state roots. |
| **Immutable Governance & Audit** | Append-Only Record System | **Tableland** (Decentralized SQL) | Censorship-resistant and cost-effective storage for MEV audit logs, ATS violations, and governance events that require public auditability without L1 storage costs. |
| **Hardware-Anchored Identity** | Edge Sovereign Target | **StrongBox / Secure Enclave** | Mandated for Zero Secret Egress (ZSE). Private keys and DID-ZK disclosures are derived and stored in hardware, never leaving the device. |
| **High-Frequency Caching** | Edge Volatile Target | **Redis** | Used for millisecond-latency session management, real-time mempool tracking, and "Sovereign Grace Period" telemetry buffering. |

### 3.2. Central vs. Edge Responsibilities

#### Central Datastores (Neon, Supabase)
- **Aggregation**: Consolidating data from multiple Nexus instances.
- **Historical Persistence**: Maintaining long-term records for reporting and institutional compliance.
- **Cross-Module Sync**: Serving as the ground truth for inter-module communication (e.g., Nexus to Gateway).

#### Edge Datastores (Enclave, Redis, Local SQLite)
- **Identity & Security**: Managing the critical path for signing and identity verification (ZSE).
- **Latency Sensitivity**: Handling high-frequency updates that would bottle-neck central databases.
- **Offline Capability**: Ensuring the Conxius Wallet remains functional for local lookups without network connectivity.

### 3.3. Conditional Datastores
- **Tableland**: Identified as **Conditional**. While core for decentralized audit logs, its use is contingent on network latency and the cost-benefit ratio vs. batching state-roots to Stacks L1.

## 4. Open Questions & Unsettled Decisions

| Question | Context | Impact |
| :--- | :--- | :--- |
| **Yield Rebalancing State** | Should sBTC yield rebalancing triggers reside in Neon or Tableland? | High: Affects < 5m latency target if decentralized sharding adds lag. |
| **Principal Locking** | Should `cxn_locked_principal` move entirely to L1 (Stacks) or remain as a Neon/Supabase hybrid with Merkle proofs? | Critical: Security of user funds vs. operational flexibility. |
| **Tableland Maturity** | Is Tableland's current validator set sufficiently decentralized for "Sovereign Persistence" status? | Strategic: Compliance with Conxian Ethos. |

## 5. Acceptance Criteria
- [ ] Each major data domain (Transactional, Analytical, Audit) has a documented preferred target.
- [ ] Rationale for each decision is explicitly captured.
- [ ] Central vs. Edge responsibilities are clearly delineated.
- [ ] Conditional status of edge datastores is identified.
