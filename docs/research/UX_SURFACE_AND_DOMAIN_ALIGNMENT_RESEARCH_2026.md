# Conxian Ecosystem UX Surface Mapping & Domain Alignment Research Report (October 2026)

| Metadata | Value |
|---|---|
| Document Title | Conxian Ecosystem UX Surface Mapping & Domain Alignment Research Report |
| Date | October 2026 |
| Target Release | Conxian BOS v1.9.5 |
| Authority | [Business Issue #943](https://github.com/Conxian/conxian-business/issues/943) / [Issue #1317](https://github.com/Conxian/conxian-business/issues/1317) |
| Classification | Canonical Architecture Research & Domain Topology Specification |

---

## Executive Summary

This empirical research report resolves ambiguity surrounding User Experience (UX) assets, repository classifications, and network domain topology across the Conxian ecosystem. Following an exhaustive repository and codebase audit across all submodules and monorepo applications, this report confirms that **there is no active standalone `conxian-ui` repository**. The legacy `conxian_ui` / `conxian-ui` repository was explicitly deprecated and deleted from the GitHub organization (`.github-private#30`, `AGENTS.md`).

All active UX surfaces across the ecosystem have been comprehensively mapped, cataloged, and assigned to their canonical operational domains: either the **Developer Protocol Surface (`conxian.org`)** or the **Corporate Governance Surface (`conxian-labs.com`)**.

---

## 1. UX Asset Mapping & Verification (`no ui repo`)

### 1.1 Status of `conxian-ui`
- **Deprecation Verification**: The repository `conxian_ui` (`conxian-ui`) was deleted from GitHub in Sprint 2 (#1097 / commit `7fd8be4`) and removed from `conxius-platform/docker-compose.yml` (#1278).
- **Current File Tree Proof**: No `conxian-ui/` directory or gitlink submodule exists in the root repository workspace.
- **Protocol Policy**: Any remaining references to `conxian-ui` in legacy documentation represent deprecated artifacts that must be updated to reference the active UX applications.

### 1.2 Active UX Asset Inventory & Mapping

| UX Application / Surface | Location in Workspace | Framework / Stack | Domain Boundary | Functional Purpose & Scope |
|---|---|---|---|---|
| **Conxian Labs Portal** | `conxian-labs-site/` (Submodule) | HTML5 / Node.js / Express / Tailwind | `conxian-labs.com` (`www.conxian-labs.com`) | Corporate marketing, commercial packaging, pricing, enterprise pilot registration, privacy, and terms. |
| **Conxius Wallet UI** | `conxius-wallet/` (Submodule) | React / Vite / TypeScript / JNI | `conxian.org` (`wallet.conxian.org`) | Non-custodial end-user mobile and web wallet interface supporting Bitcoin L1, Stacks, and Silent Payments. |
| **Control Plane Dashboard** | `apps/control-plane/` & `conxian-gateway/apps/control-plane/` | Next.js 15 / React 19 / Tailwind / Drizzle | `conxian-labs.com` (`bos.conxian-labs.com`) | Enterprise operations control plane, release governance, workflow approvals, policy execution, and gateway administration. |
| **Node Admin Dashboard** | `conxius-platform/services/admin-dashboard/` | Next.js / Tailwind | `conxian.org` (`platform.conxian.org`) | Self-hosted sovereign node operator dashboard for metrics, peer management, and enclave status. |
| **Admin Pulse Component Library** | `conxius-platform/services/admin-pulse-bos/` | React / TypeScript | Component Library | Reusable UI component library for node admin interfaces and status displays. |
| **Showcase DApp** | `showcase-dapp/` | Next.js 15 / React 19 / Tailwind | `conxian.org` (`showcase.conxian.org`) | Proof-of-concept developer demonstration application for protocol interaction and contract testing. |
| **Developer Sandbox Examples** | `conxian-gateway/examples/developer-sandbox/` | Node.js / TypeScript | Developer Tool | Interactive terminal and web sandbox for gateway API key management and RPC testing. |

---

## 2. Domain Topology & Separation Firewall

Conxian enforces a strict architectural, legal, and operational firewall between the open-source developer protocol surface (`conxian.org`) and the commercial corporate entity (`conxian-labs.com`).

```
                                  CONXIAN ECOSYSTEM
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
      DEVELOPER PROTOCOL SURFACE                     CORPORATE GOVERNANCE SURFACE
           (conxian.org)                                 (conxian-labs.com)
                  │                                               │
   ┌──────────────┼──────────────┐                 ┌──────────────┼──────────────┐
   │              │              │                 │              │              │
 nexus.        gateway.         sdk.             www.            bos.         status.
conxian.org   conxian.org    conxian.org    conxian-labs.com conxian-labs.com conxian-labs.com
 (Nexus)       (Gateway)        (SDK)          (Marketing)    (Control Plane)   (SLA)
```

### 2.1 Developer Protocol Surface (`conxian.org`)
- **Target Audience**: Developers, node operators, open-source contributors, independent auditors.
- **SLA Policy**: **NO SLA**. Public repositories and endpoints are provided "AS IS" under open-source licenses (Apache 2.0 / MIT / BSL).
- **Subdomain Allocations**:
  - `conxian.org` -> Main Protocol Hub & Developer Documentation.
  - `nexus.conxian.org` -> Cross-chain state proof verification & MMR proof APIs (`conxian-nexus`).
  - `gateway.conxian.org` -> Stateless RPC, ISO 20022 message normalizers & OData callbacks (`conxian-gateway`).
  - `sdk.conxian.org` -> AWS Nitro Enclave TEE hardware SDKs & attestation docs (`conxius-enclave-sdk`).
  - `platform.conxian.org` -> Sovereign node orchestration & NixOS / Docker specs (`conxius-platform`).
  - `market.conxian.org` -> Agentic commerce, CJCS v2.0 job card ledger & AI marketplace (`conxian_market`).
  - `wallet.conxian.org` -> Non-custodial wallet web client (`conxius-wallet`).

### 2.2 Corporate Governance Surface (`conxian-labs.com`)
- **Target Audience**: Enterprise clients, institutional B2B partners, paid node subscribers.
- **SLA Policy**: **99.5% Monthly Uptime SLA** (Business / Enterprise Tiers) with 1-hour SEV1 acknowledgment.
- **Subdomain Allocations**:
  - `www.conxian-labs.com` -> Official Conxian Labs website, commercial packaging, pricing, enterprise pilot registration (`conxian-labs-site`).
  - `bos.conxian-labs.com` -> Managed Enterprise Control Plane & release governance (`apps/control-plane`).
  - `api.conxian-labs.com` -> Managed Subscriber API gateway (`api.conxian-labs.com/v1/agent`).
  - `status.conxian-labs.com` -> Real-time operational uptime and SLA status dashboard.

---

## 3. Mainnet Proof & Verification Criteria

To ensure complete alignment with mainnet production readiness standards, all UX assets and domain mappings adhere to the following proof criteria:

1. **Non-Custodial Enforcement**: No UX surface retains, transmits, or possesses user private keys or seed phrases. Key generation in `conxius-wallet` is strictly client-side.
2. **Environment Secret Protection**: Secret configuration files (`.env`, `.env.local`) across all UX applications (`showcase-dapp`, `apps/control-plane`, `conxius-platform/services/admin-dashboard`) are excluded from Git tracking via `.gitignore`.
3. **Stateless API Interactions**: Control-plane and admin dashboards interact with gateways via signed tokens (`cxn_live_`, `cxn_test_`, `cxn_agent_`) without stateful session coupling.
4. **Clean Asset Alignment**: Every UX asset is unambiguously classified as either open-source developer protocol (`conxian.org`) or commercial corporate (`conxian-labs.com`).

---

## 4. Actionable Alignment Recommendations

1. **Document Cleanup**: Update all governance and technical documentation (`PORTFOLIO_REPOSITORY_INVENTORY.md`, `PORTFOLIO_BUSINESS_UNIT_MAP.md`, `REPO_PORTFOLIO.md`, `ALIGNMENT.md`) to explicitly reflect that `conxian-ui` is deprecated and deleted, and reference active UX apps instead.
2. **Candidate Ledger Update**: Record candidate `ease-of-use-ux-domain-alignment-gap` in `docs/bos_research_candidate_ledger.json` and `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`.
3. **Knowledge Base Synchronization**: Upgrade `docs/BOS_KNOWLEDGE_FRAMEWORK.md` to Version 3.8 and update `BOS_KNOWLEDGE_GRAPH.md` with UX asset mappings.
