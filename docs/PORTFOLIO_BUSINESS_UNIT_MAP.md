# Portfolio business-unit map and separation of concerns

This document is the portfolio-level map that assigns every repo/subrepo (submodule) and BOS asset to a **business unit** or **operating function**, and defines the separation-of-concerns boundaries needed for business development and business unit management.

This complements (and should remain consistent with):

- `docs/REPO_PORTFOLIO.md` (flagship vs supporting trust surface)
- `openspec/changes/remediate-enterprise-sovereignty/specs/enterprise-sovereignty/spec.md` (4-unit consolidation requirement)

## Target business-unit structure

OpenSpec anchors the ecosystem into four standalone businesses:

| Business unit | Market surface | Core obligation |
| --- | --- | --- |
| **Conxius** | B2C | Sovereign wallet and key custody (mobile-first) |
| **CSF (Conxian Finance Protocol)** | Protocol | On-chain contracts, assets, and fee logic |
| **Fusion** | B2B/B2G integration | Cross-layer gateway + compliance pipelines |
| **Nexus** | State + telemetry | Authoritative state node/services for the stack |

Alongside the four units, BOS requires separate operating functions that should not be mixed into product repos: governance/specs, treasury, compliance, ops, and strategy.

## Portfolio-level map (repos, subrepos, and BOS assets)

### Ecosystem repos (submodules pinned by this BOS repo)

| Asset | Type | Primary BU / function | Primary concern(s) | Notes |
| --- | --- | --- | --- | --- |
| `Conxian/` | Submodule | **CSF** (Protocol) | Protocol + contracts | Canonical on-chain source; should not contain off-chain service logic. |
| `conxius-wallet/` | Submodule | **Conxius** (Wallet) | Wallet + custody | Mobile client; no shared backend logic beyond boundary APIs. |
| `conxian-gateway/` | Submodule | **Fusion** (Gateway) | Gateway + compliance | Integration surface; consumes Nexus state; should not be a UI host. |
| `conxian-nexus/` | Submodule | **Nexus** (State node) | State + telemetry | Must remain the authoritative node/service surface. |
| `conxian-ui/` | Submodule | Operating function (UI) | UI | Web UI for interacting with the ecosystem; should avoid embedding protocol logic beyond calls. |
| `conxian-labs-site/` | Submodule | Operating function (Public web) | Public documentation + marketing | Public site; should not include internal-only strategy material. |
| `conxius-platform/` | Submodule | Operating function (Platform/DevEx) | Local stack orchestration | Dev stack only; should not become a home for core product logic. |
| `stacksorbit/` | Submodule | Operating function (DevOps tooling) | Deployment tooling | Primarily supports CSF protocol deployment. |
| `lib-conclave-sdk/` | Submodule | Operating function (Shared SDK) | Shared libraries | Supports services across Fusion/Nexus; should stay dependency-light. |
| `lib-conxian-core/` | Submodule | Operating function (Shared core) | Shared models + conventions | Currently tracked as a gitlink but missing a `.gitmodules` entry (see build/repair list). |

### BOS-native assets (tracked in this repo)

| Asset | Primary BU / function | Primary concern(s) | Notes |
| --- | --- | --- | --- |
| `openspec/` | Governance (OpenSpec) | Ground-truth technical requirements | Public, versioned specs; should not contain sensitive operational strategy. |
| `docs/` | Governance (Public docs) | Public documentation | Public trust surface docs and portfolio conventions. |
| `conxian-business/` | Governance (BOS runtime artifacts) | Machine-readable BOS state | State-machine artifacts (`BOS_STATE_MACHINE.json`, audit manifests). |
| `.github/` | Governance (Repo operations) | CI/CD, templates | Cross-unit repo hygiene enforcement entrypoint. |
| `scripts/` | Governance (Portfolio hygiene) | Audits, link checking | BOS utility scripts; avoid embedding product logic. |
| `audit/` | Governance (Assurance) | Audits and alignment reports | Outputs should be cross-unit and non-sensitive. |
| `infrastructure/terraform/` | Operating function (Infra) | Infrastructure as code | Shared infra definitions; avoid coupling to a single business unit. |
| `admin/` | Operating function (Admin) | Internal runbooks/ops | Must respect Zero Secret Egress; secrets must remain out of git. |
| `showcase-dapp/` | Operating function (Showcase) | Demonstration UI | Public demo surface; should stay clearly separate from flagship product repos. |
| `Fiscal-Vault-Oracle/` | Operating function (Treasury) | Treasury automation | Financial engine module (BOS EXCO suite). |
| `Nakamoto-Guardian/` | Operating function (Compliance) | Enforcement/compliance | Architecture + regulatory enforcement module (BOS EXCO suite). |
| `Sovereign-Ops-Orchestrator/` | Operating function (Ops) | Execution orchestration | Work/ops engine; connects BOS state machine to execution platforms. |
| `Sovereign-Strategy-Nexus/` | Operating function (Strategy) | Strategy and M&A | Strategic intelligence layer; keep internal strategy material in Linear Virtual Office. |
| `cxn-grid-oracle/` | Operating function (Grid oracle) | External oracle integration | Energy/grid orchestration module; separate from protocol and wallet. |

## Separation-of-concerns model (portfolio rules)

The goal is to keep each repo’s business unit legible to partners/auditors and to keep internal operations safe (ZSE) while still enabling end-to-end delivery.

### 1) Business unit boundaries (what must not mix)

1. **CSF / Protocol** (`Conxian/`) must not contain wallet UX, gateway service code, or BOS automation.
2. **Conxius / Wallet** (`conxius-wallet/`) must not contain server-side Fusion/Nexus logic; it consumes boundary APIs.
3. **Fusion / Gateway** (`conxian-gateway/`) must not become the authoritative chain state source; it consumes Nexus.
4. **Nexus / State node** (`conxian-nexus/`) must not become a UI repo; it provides state and telemetry.
5. **BOS / Governance** (this repo: `conxian-business`) must not become a dumping ground for product code; it defines specs, governance, and portfolio wiring.
6. **Operating functions** (strategy/treasury/compliance/ops/admin) must not leak sensitive information into git; internal-only strategy belongs in Linear.

### 2) Allowed dependency directions (high level)

This keeps “truth drift” low and preserves independent unit ownership.

```
OpenSpec + BOS docs  -> constrain all units (no runtime dependency)
Protocol (CSF)       -> exposes on-chain interfaces
Nexus                -> exposes state + telemetry interfaces
Fusion Gateway       -> integrates external systems; consumes Nexus + Protocol
Wallet/UI            -> consumes Gateway/Nexus/Protocol boundary interfaces
```

## Cross-unit governance + documentation requirements (missing/required)

These are the minimum cross-unit artifacts needed to operate the portfolio as four businesses plus operating functions.

1. **Business unit charters** (one page each): Conxius, CSF, Fusion, Nexus.
   - Scope, non-scope, primary KPIs, and “what this unit owns.”
2. **Portfolio ownership rules**:
   - Explicit maintainer/approver for each repo, plus escalation rules (CODEOWNERS is necessary but not sufficient).
3. **Boundary interface registry**:
   - Versioned list of APIs/schemas/contracts each unit exports, with compatibility expectations.
4. **Cross-unit change control**:
   - A lightweight rule for when a change requires a BOS/OpenSpec update vs. when it can stay within a single unit repo.
5. **Documentation classification** (ZSE):
   - Public docs in git (`docs/`, `openspec/`), sensitive strategy/ops in Linear Virtual Office.

## Unique value + scope definition (by repo)

Use this as the “business-end” positioning layer for partners and internal coordination.

| Repo / asset | Unique value | In scope | Out of scope |
| --- | --- | --- | --- |
| `Conxian` | Canonical protocol and on-chain assets | Contracts, traits, fee logic, registries | Wallet UX, off-chain integration services |
| `conxius-wallet` | Sovereign custody and signing surface | Key management, offline-first wallet UX | Running the state node, ERP integrations |
| `conxian-gateway` | Fusion integration and compliance | Webhooks, compliance pipelines, aggregation | Being the authoritative state source |
| `conxian-nexus` | Authoritative state + telemetry | Block height authority, state services, metrics | UI, treasury automation |
| `conxian-ui` | Web interaction surface | Web app UX consuming boundary APIs | Defining protocol logic |
| `conxius-platform` | End-to-end local stack | Dev orchestration, local ops | Shipping product features |
| `stacksorbit` | Protocol deployment tooling | Contract deployment and ops | Wallet features |
| `conxian-labs-site` | Public web presence | Marketing, docs surfacing | Internal strategy |
| `lib-conxian-core` | Shared conventions | Models, shared primitives | Business logic or product UX |
| `lib-conclave-sdk` | Enclave/crypto SDK | Attested flows, SDK primitives | Protocol decisions |
| `Fiscal-Vault-Oracle` | Treasury automation | Treasury, yield, bond issuance specs | Wallet UX |
| `Nakamoto-Guardian` | Enforcement and compliance | Compliance gating, anti-fragility loops | Product UX |
| `Sovereign-Ops-Orchestrator` | Execution orchestration | Work execution + Linear wiring | Protocol code |
| `Sovereign-Strategy-Nexus` | Strategic intelligence | M&A velocity, IP sovereignty | Public product marketing copy |
| `cxn-grid-oracle` | External oracle integration | Grid/demand-response routing | Protocol custody |

## Prioritized build/repair list (business operating maturity)

P0 (portfolio integrity and “who owns what”):

1. Add explicit **business unit charters** and a lightweight portfolio **ownership model** (approvers, escalation).
2. Fix submodule hygiene so the pinned portfolio is mechanically reliable (notably: `lib-conxian-core` missing `.gitmodules` entry).
3. Add a boundary **interface registry** (APIs/schemas/contracts) so units can move independently without silent drift.

P1 (separation enforcement and partner legibility):

1. Extend `make unbundle` into a portfolio-wide boundary check (disallowing known cross-contamination patterns).
2. Ensure every flagship repo README has a consistent role line and links back to `docs/REPO_PORTFOLIO.md` and this map.

P2 (operating controls):

1. Standardize cross-unit release signaling (what “ready” means for Protocol vs Wallet vs Gateway vs Nexus).
2. Add a stable “portfolio dashboard” document that tracks maturity status per unit (docs-only; no sensitive details).
