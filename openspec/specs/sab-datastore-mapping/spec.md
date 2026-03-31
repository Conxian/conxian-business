# SAB Datastore Mapping Specification

## 1. Purpose
This specification translates the Conxian Sovereign Autonomous Business (SAB) current-state inventory into target-state datastore decisions. It defines the mapping of major data domains to canonical systems of record (on-chain for public state, and hardware enclaves for secrets) and derived query layers.

## 2. Scope
- Mapping transactional application state.
- Mapping proof-oriented analytics.
- Mapping immutable governance and audit records.
- Identifying central versus edge responsibilities.

## 3. Requirements

### 3.1. Major Data Domain Mappings

The long-horizon direction is to make all non-secret SAB-critical business state fully on-chain. Off-chain systems may exist for performance and query ergonomics, but they must be treated as derived/indexed replicas rather than the authoritative system of record. Secrets and signing keys remain exclusively in hardware enclaves (ZSE), referenced on-chain by identifiers only.

This table describes the target-state canonical systems of record. Any current production deviations should be documented as temporary exceptions with an explicit migration path back to this mapping.

| Data Domain | Canonical System of Record | Derived / Query Layer (Non-authoritative) | Notes |
| :--- | :--- | :--- | :--- |
| **Transactional Application State** | **Stacks L1 (Clarity contracts)** | **PostgreSQL** (currently **Neon**, later sovereign/self-hosted) | Write-path is on-chain. Postgres is a materialized read model for Nexus/Gateway sync, MMR node indexing, and service-level query performance. |
| **Proof-Oriented Analytics** | **Stacks L1 (events + state roots)** | **Supabase** (or equivalent SQL analytics layer) | Analytics datasets are derived from the on-chain event stream. Verification is anchored by on-chain checkpoints/hashes of derived datasets; canonical truth is always the raw L1 events/state. |
| **Immutable Governance & Audit** | **Stacks L1 (event log + audit registry contract)** | **Tableland** (optional mirror) | Default is on-chain auditability. If used, Tableland MUST be a pure mirror: every row must be derivable from on-chain audit contracts/events (or data cryptographically committed on-chain), and it must not introduce protocol-relevant fields that cannot be reconstructed from L1. For this spec, protocol-relevant means any data that can affect protocol behavior, user balances, or governance outcomes; Tableland may add presentational/performance fields recomputable from L1 (denormalized joins, precomputed aggregates). |
| **Identity Claims & Capabilities** | **Stacks L1 (DID / capability / revocation registry)** | N/A | Public identity state lives on-chain. |
| **Identity Secrets (ZSE)** | **StrongBox / Secure Enclave** | N/A | Mandated for Zero Secret Egress (ZSE). Private keys and DID-ZK disclosure material are derived and stored in hardware, never leaving the device. |

#### 3.1.1. Data Flow & Verification

1. **Stacks L1 emits canonical state transitions** via contract state + events.
2. **Indexers derive replicas** (Postgres/Supabase/Tableland) by consuming L1 events and projecting them into query-optimized schemas.
3. **Verification** is performed by anchoring periodic dataset checkpoints on-chain (e.g., a hash of normalized events / materialized views) and requiring indexers/clients to match those checkpoints.
4. **Mismatch handling**: any replica that fails checkpoint validation is treated as stale/corrupted and must be rebuilt from the on-chain event stream.

Checkpoint computation must follow a deterministic, versioned normalization/materialization spec, and the checkpoint anchor must reference the spec version. In all cases, raw Stacks L1 events/state remain the ultimate canonical truth; checkpoints exist only to validate replicas.

Checkpoint cadence should be defined over fixed windows (e.g., block ranges) and anchored on protocol-defined epochs to control on-chain costs. Infrastructure services and full indexers MUST validate their replicas against on-chain checkpoints; light clients MAY rely on indexer endpoints that are monitored against those checkpoints.

At minimum, the following derived replicas MUST anchor and validate checkpoints:

- Transactional Postgres read models used by Nexus/Gateway for settlement, risk, or compliance decisions.
- Analytics projections used to drive keeper/agent actions or governance/audit reporting.
- Any public audit mirror (e.g., Tableland).

#### 3.1.2. Non-canonical Caches

| Cache / Local Store | Target | Canonical Source | Notes |
| :--- | :--- | :--- | :--- |
| **High-Frequency Caching** | **Redis** | Derived from canonical sources above (L1 + indexer read models) | Volatile cache for millisecond-latency session management, mempool tracking, and telemetry buffering. |
| **Offline Wallet Cache** | **Local SQLite** | Derived from canonical sources above (L1 + enclave-held secrets) | Offline lookups and UX continuity. Must be treated as a local cache. |

### 3.2. Central vs. Edge Responsibilities

#### Central Datastores (PostgreSQL, Supabase)
- **Aggregation**: Consolidating materialized views derived from on-chain state across multiple Nexus instances.
- **Historical Persistence**: Maintaining long-term records for reporting and institutional compliance as query-optimized replicas; all compliance evidence must remain provably derivable from on-chain state and published checkpoints.
- **Query Acceleration**: Serving as derived read models for inter-module communication (e.g., Nexus to Gateway) without becoming the source of truth.

#### Edge Datastores (Enclave, Redis, Local SQLite)
- **Identity & Security**: Managing the critical path for signing and identity verification (ZSE).
- **Latency Sensitivity**: Handling high-frequency updates that would bottleneck central databases.
- **Offline Capability**: Ensuring the Conxius Wallet remains functional for local lookups without network connectivity.

### 3.3. Conditional Datastores
- **Tableland**: Identified as **Conditional**. It is acceptable only as a non-authoritative mirror of on-chain audit state and must not be required for protocol correctness.

## 4. Open Questions & Unsettled Decisions

| Question | Context | Impact |
| :--- | :--- | :--- |
| **Yield Rebalancing State** | Should yield rebalancing triggers execute fully on-chain, or remain off-chain (keeper/agent) with on-chain commitments? | High: Affects <= 5 minutes end-to-end trigger-to-finality latency targets under load. |
| **Principal Locking** | Should `cxn_locked_principal` move entirely to L1 (Stacks), with off-chain replicas derived from events, or remain hybrid during the transition? | Critical: Security of user funds vs. operational flexibility. |
| **Tableland Mirror** | Is a decentralized SQL mirror necessary once on-chain audit registries are in place, or can this be replaced by indexer-backed query endpoints with checkpoint verification? | Strategic: Operational complexity vs. public discoverability. |

## 5. Acceptance Criteria
This specification is considered complete when:

- Each major data domain (Transactional, Analytical, Audit) has a documented canonical record and derived query mapping.
- Rationale for each decision is explicitly captured.
- Central vs. Edge responsibilities are clearly delineated.
- Conditional status of non-authoritative datastores (e.g., Tableland mirror) is identified.
