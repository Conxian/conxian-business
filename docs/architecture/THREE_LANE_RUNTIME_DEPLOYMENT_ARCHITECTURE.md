# Three-lane runtime deployment architecture (CON-455)

This document defines the **canonical, public-safe** Conxian runtime architecture across three deployment lanes:

1. **Community sovereign-node** (self-hosted / bring-your-own runtime)
2. **Business-managed** (managed hosting + shared controls)
3. **Enterprise / private-cloud** (customer-operated control plane and data plane)

The goal is a single conceptual architecture whose **core invariants** hold in every lane, with lane-specific choices limited to control-plane ownership, custody boundaries, and infrastructure placement.

## 1) Goals and non-goals

Goals:

- Define the shared runtime components (what “the Conxian runtime” is).
- Specify which components must be treated as **control plane** vs **data plane** vs **derived/UX**.
- Document lane-specific controls: custody boundaries, upgrade authority, identity roots, and operational trust assumptions.
- Define upgrade/migration paths across lanes without changing protocol correctness.

Non-goals:

- Vendor-specific infrastructure templates (K8s manifests, Terraform modules, managed service names).
- Secret management details (ZSE: these live in Linear).
- Contract-level protocol specs (covered by Conxian/OpenSpec docs).

## 2) Core invariants (must always hold)

These invariants apply to every lane.

1. **Canonical truth is on-chain**
   - Off-chain databases and indexes are derived and non-authoritative.

2. **No dashboard-to-contract coupling**
   - Dashboards/UX surfaces MUST NOT hold production signing keys and MUST NOT broadcast value-bearing transactions.

3. **Dynamic principals (no hardcoded production addresses)**
   - Contracts and privileged workflows MUST resolve principals dynamically via `operational-treasury.clar`.

4. **Signed, replay-resistant events**
   - Inter-service requests (especially privileged actions) SHOULD be expressed as signed envelopes (see `docs/protocols/SIGNED_EVENT_ENVELOPE_V1.md`).

5. **Fail closed**
   - If a privileged workflow cannot prove it is valid, the runtime MUST stop and record an explicit error state.

## 3) Canonical component model

The Conxian runtime is best understood as four planes.

### 3.1 Settlement + policy plane (on-chain)

- **Bitcoin L1**: base settlement layer.
- **Stacks L1/L2**: execution layer for Conxian policy/state.
- **Conxian protocol contracts**: role-based policy, timelocks, and state roots.

### 3.2 Proof plane (verification)

- **`lib-conxian-core`**: SNARK-based state proof verification primitives.
- **State proof artifacts**: proofs, commitments, and verification receipts used to bind off-chain observations to on-chain state.

### 3.3 Data plane (runtime services)

Lane-neutral services (deployment location varies by lane):

- **BOS orchestrator**: validates intents, enforces guardrails, prepares unsigned transactions, and coordinates execution.
- **Gateway**: broadcast boundary + ingress enforcement for value-bearing transactions (no generic relay behavior).
- **Nexus**: state indexing/projection + derived query surfaces.
- **Oracle publishers**: signed feeds and derived read-model publishing (never a correctness dependency).

### 3.4 Control plane (who can mutate production)

Control plane surfaces are the “roots” that can:

- deploy/upgrade runtime services
- rotate keys or change allowlists
- modify identity/authorization
- change policy gates or environment promotion rules

The enterprise custody baseline (`docs/protocols/ENTERPRISE_CUSTODY_BASELINE.md`) defines minimum requirements for these protected actions.

## 4) Reference topology (lane-neutral)

```text
                        +-----------------------+
                        |      Dashboards       |
                        | (observe / propose)   |
                        +-----------+-----------+
                                    |
                                    | (signed intents, requests)
                                    v
+---------------------+   +---------------------+   +---------------------+
|   Intent adapters   |-->|   BOS orchestrator  |-->|   Signer boundary   |
| (ERP/MCP, tooling)  |   | (policy + guardrails)|   | (MS/HSM/DAO/SAB)   |
+----------+----------+   +----------+----------+   +----------+----------+
            |                         |                         |
            |                         | (broadcast)             | (execute)
            v                         v                         v
   +----------------+        +----------------+         +-------------------+
   |  Derived stores|<-------|      Nexus     |<--------|      Gateway       |
   | (read models)  | (index)| (projections)  | (events)| (ingress boundary) |
   +----------------+        +----------------+         +----------+--------+
                                                                |
                                                                v
                                                       +-------------------+
                                                       |   Stacks / Bitcoin |
                                                       | (policy + settle)  |
                                                       +-------------------+
```

Notes:

- “Derived stores” can include SQL read models (e.g., treasury/oracle) and cache layers.
- The signer boundary is explicitly separated so hosting the data plane does not imply custody.

## 5) Lane definitions

### 5.1 Lane A: Community sovereign-node (self-hosted)

**Intent:** maximize operator sovereignty. The operator controls both the control plane and data plane.

Placement:

- Control plane: operator-owned (local CI/CD, infra admin).
- Data plane: operator-hosted (Akash, Kubernetes, bare metal).
- Settlement/policy: public chains (Stacks/Bitcoin).

Controls:

- Keys and signing: operator-managed.
- Upgrades: operator decides when/if to upgrade (pin container digests/versions).
- Observability: local-first; any external telemetry is optional and must not be correctness-critical.

Trust assumptions:

- Users/partners trust the operator not to censor or misreport derived state.
- Correctness remains bounded by on-chain policy + verification; derived views may be incomplete.

### 5.2 Lane B: Business-managed (managed hosting + shared controls)

**Intent:** provide a managed runtime with operational reliability while preserving explicit custody boundaries.

Placement:

- Control plane: managed by the business operator (often Conxian) with audited promotion gates.
- Data plane: managed hosting (multi-tenant or single-tenant).
- Settlement/policy: public chains.

Controls:

- Upgrades: managed via the `dev` -> `staged` -> `main` promotion model (see `docs/BRANCH_AND_PROMOTION_STANDARD.md`).
- Custody: MUST be explicit and separable from hosting.
  - Minimum expectation: the managed operator cannot unilaterally move value or change policy without the required signer quorum.
- Isolation: multi-tenant deployments MUST enforce strict tenant namespace isolation at every persistence boundary.

Trust assumptions:

- Tenants trust the managed operator for availability, incident response, and correct operation of the data plane.
- Tenants do not need to trust the operator with unilateral value movement if custody boundaries are implemented correctly.

### 5.3 Lane C: Enterprise / private-cloud (customer-operated)

**Intent:** enterprise-owned control plane and data plane, integrated with enterprise IAM and security posture.

Placement:

- Control plane: enterprise-owned (IdP roots, deployment pipeline, allowlists).
- Data plane: enterprise-hosted (private cloud/VPC, on-prem, or hybrid).
- Settlement/policy: public chains, accessed through enterprise-controlled egress.

Controls:

- Protected actions (deploy/upgrade, key rotation, policy mutation) MUST meet the enterprise custody baseline.
- Optional “split-plane” operation is allowed:
  - internal execution logs and operational data stay private
  - a public audit manifest may be anchored to Stacks L1 (see enterprise custody baseline implementation note)

Trust assumptions:

- Enterprise trusts itself as the operator; third parties trust on-chain proofs and published audit commitments.

## 6) Upgrade and migration paths

The runtime should support changing lanes without changing protocol correctness.

### 6.1 Common upgrade rules

- Treat the control plane as the highest-risk surface; require quorum for production mutations.
- Prefer version pinning with explicit promotion rather than “always latest.”
- Any backward-incompatible change in event formats or read models must provide an export/import path.

### 6.2 Migration patterns

1. **Lane B -> Lane A (managed -> self-hosted)**
   - Tenant takes ownership of deployments + observability.
   - Derived state is rebuilt by replaying signed events and on-chain receipts.

2. **Lane B -> Lane C (managed -> enterprise)**
   - Enterprise assumes control-plane roots (IdP + CI/CD + allowlists).
   - Re-deploy data plane inside enterprise perimeter and re-point chain egress.

3. **Lane A -> Lane C (self-hosted -> enterprise)**
   - Move from operator-local keys and infra to enterprise custody/IAM and hardened promotion gates.

In all cases, the protocol correctness boundary stays anchored to on-chain policy and proof verification.

## 7) Lane comparison matrix (public-safe)

| Area | Lane A: Community sovereign-node | Lane B: Business-managed | Lane C: Enterprise/private-cloud |
| --- | --- | --- | --- |
| Control plane owner | Operator | Managed operator | Enterprise |
| Data plane hosting | Operator | Managed operator | Enterprise |
| Custody boundary | Operator-managed | Explicit separation required | Enterprise custody baseline |
| Upgrade authority | Operator | Managed promotion gates | Enterprise promotion gates |
| Primary trust | Operator liveness + honesty for derived views | Operator availability + correct isolation | Enterprise internal controls |
| Correctness anchor | On-chain + proofs | On-chain + proofs | On-chain + proofs |
