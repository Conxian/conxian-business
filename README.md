# Conxian Business Operations System (BOS)

[![Conxian Unified CI](https://github.com/Conxian/conxian-business/actions/workflows/conxian-unified-ci.yml/badge.svg)](https://github.com/Conxian/conxian-business/actions/workflows/conxian-unified-ci.yml)
[![Deploy Documentation](https://github.com/Conxian/conxian-business/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/Conxian/conxian-business/actions/workflows/deploy-docs.yml)

This repository is the governance and specification surface for the Conxian Business Operations System (BOS). It documents infrastructure, routing, orchestration, compliance integration, and verification patterns anchored to Bitcoin; it is not a custody system or market-operation console.

Governance baseline — OpenSpec, portfolio doctrine, and submodule wiring for the Conxian ecosystem.

See the [repo portfolio](docs/REPO_PORTFOLIO.md#ecosystem-repos) for the portfolio trust-surface map and `docs/BOS_BUSINESS_BUILDOUT.md` for the public/internal split.

## Canonical documentation

- [`docs/REPO_PORTFOLIO.md`](./docs/REPO_PORTFOLIO.md)
- [`docs/PORTFOLIO_BUSINESS_UNIT_MAP.md`](./docs/PORTFOLIO_BUSINESS_UNIT_MAP.md)
- [`docs/DOCTRINE_ALIGNMENT_STANDARD.md`](./docs/DOCTRINE_ALIGNMENT_STANDARD.md)
- [`docs/PORTFOLIO_DOCTRINE_REGISTER.md`](./docs/PORTFOLIO_DOCTRINE_REGISTER.md)
- [`docs/DOCUMENTATION_ALIGNMENT_INDEX.md`](./docs/DOCUMENTATION_ALIGNMENT_INDEX.md)

## Purpose

Define and version Conxian's Business Operations System (BOS) as an auditable, programmatic state machine (OpenSpec, governance, and operational artifacts).

## Status

**Beta.** Governance and specification artifacts are **Implemented**; architecture and deployment proposals remain **Target-state** until named evidence exists. Hosting visibility may differ by deployment, but this repository is treated as public-safe for documentation-boundary purposes.

This status framing is being kept aligned during the `conxius-platform` documentation transition.

Documentation here follows public-safe boundary rules; internal-only strategy, legal, security, financial, and operational details remain in the authorized Linear workspace under ZSE.

Release and SemVer tagging follows the process in `RELEASING.md` (`vX.Y.Z`), with history tracked in `CHANGELOG.md`.

## Audience

- Contributors implementing Conxian's protocol, infrastructure, and tools.
- Partners and auditors who need a canonical, versioned view of OpenSpec.

## Relation to Conxian stack

The Conxian ecosystem is organized by function to ensure clarity and modularity across the Sovereign Autonomous Business (SAB) stack. See the **[BOS Runtime Ownership Map](./conxian-business/BOS_RUNTIME_OWNERSHIP_MAP.md)** for detailed responsibility boundaries.

### 1. Platform & Governance
- **[`conxian-business/`](./conxian-business)**: **BOS Governance**. Public-safe specifications, templates, and ZSE pointer stubs.
- **[`conxius-platform/`](./conxius-platform)**: **Orchestration**. Stack orchestration and local development.
- **[`conxius-orbit/`](./conxius-orbit)**: **Ops Tooling**. Deployment and operations automation.

### 2. Core Operating Suite (EXCO Agents)
- **[`conxian-nexus/`](./conxian-nexus)**: **State Node**. High-level orchestration, state roots (MMR), and decentralized storage.
- **[`conxian-gateway/`](./conxian-gateway)**: **Middleware**. x402 mandates, RPC pooling, and ZKML compliance.
- **[`Fiscal-Vault-Oracle/`](./Fiscal-Vault-Oracle)**: **Protocol/reference oracle**. Contract- and tenant-defined policy constraints; not company treasury control.
- **[`Nakamoto-Guardian/`](./Nakamoto-Guardian)**: **Compliance**. Policy enforcement and anti-fragility monitoring.

### 3. Protocol & SDKs
- **[`Conxian/`](./Conxian)**: **[Deprecated] Protocol/DAO**. Legacy Clarity smart contracts repository (deprecated; active protocol owned by lib-conxian-core, conxian-gateway, conxian-nexus, conxian-business).
- **[`conxian-market/`](./conxian-market)**: **AI Marketplace**. AI Marketplace and Agentic Commerce surface mapped in business repo.
- **[`conxius-enclave-sdk/`](./conxius-enclave-sdk)**: **Enclave SDK**. Enclave and hardware-attestation primitives.
- **[`lib-conxian-core/`](./lib-conxian-core)**: **Shared Core**. Common models for BitVM2, CJCS, and Gateway engine.

### 4. User Interfaces
- **[`conxius-wallet/`](./conxius-wallet)**: **Mobile**. User-controlled, hardware-backed mobile client.
- **[`conxian-ui/`](./conxian-ui)**: **Web**. `conxian_ui` public interaction surface (upstream slug retained).
- **[`conxian-labs-site/`](./conxian-labs-site)**: **Website**. Public ecosystem landing.

## Quick start / Next action

This repository uses Git submodules.

```bash
git clone --recurse-submodules https://github.com/Conxian/conxian-business
cd conxian-business
```

`conxius-platform/` is configured with `update = none`, so it will be skipped by default during recursive submodule updates. To opt in:

```bash
git -c submodule.conxius-platform.update=checkout submodule update --init conxius-platform
```

If you need the `conxius-platform/` nested submodules, initialize them from within that repo (for example):

```bash
cd conxius-platform
git submodule update --init services/conxian-ui
```

Next action after clone: review `docs/REPO_PORTFOLIO.md` for ecosystem context and `docs/BOS_BUSINESS_BUILDOUT.md` for public/internal boundary rules.

## Ownership

Ownership and review requirements are defined in [`.github/CODEOWNERS`](./.github/CODEOWNERS). `CODEOWNERS`-designated policy owners are authoritative for governance, security, and documentation-policy changes.

## Security / Governance

For general support and non-security bug reports, open a GitHub issue. For security vulnerabilities, follow the private reporting process in [`SECURITY.md`](./SECURITY.md).

This repository follows Zero Secret Egress (ZSE) boundary discipline. See [Repository visibility and public/private boundary](#repository-visibility-and-publicprivate-boundary).

## Repository visibility and public/private boundary

Treat this repository as public-safe for boundary purposes. Detailed strategy, legal interpretations, operational runbooks, infrastructure identifiers, and any secret inventory are maintained in the authorized Linear workspace (not in git), in compliance with our Zero Secret Egress (ZSE) mandate.

Detailed strategy and roadmap content must not be duplicated in this README; see `docs/BOS_BUSINESS_BUILDOUT.md` for the public vs internal documentation rules.

Some files are intentionally kept as stubs so existing links continue to resolve.

## Protocol and client control boundaries

Conxian-Labs builds and operates non-custodial software and infrastructure. The Conxian protocol/DAO layer may define contract state and governance rules; the Conxius client/access layer supports user-controlled keys and signing. Neither relationship makes Conxian-Labs a custodian, discretionary fund controller, or market participant.

- **Wallet boundary**: See [`docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md`](./docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md) for the documented signer and user/protocol boundary; read custody terms as boundary records, not as a company-custody claim.
- **Governance handoff**: [`docs/SAB_DAO_HANDOFF_PROTOCOL.md`](./docs/SAB_DAO_HANDOFF_PROTOCOL.md) describes protocol/DAO governance transitions; detailed signer procedures remain outside Git.
- **Operational mappings**: Detailed signer and infrastructure mappings are maintained in authorized systems; public stubs are retained only for link continuity.

## Ground truth (OpenSpec)

The definitive technical specifications for the Conxian ecosystem are maintained in the `openspec/` directory. See the [Enterprise Sovereignty Baseline](./openspec/changes/remediate-enterprise-sovereignty/specs.md) for the latest architectural standards.

## Governance and security

We adhere to strict sovereignty and security standards.

For general support and non-security bug reports, open a GitHub issue. For security vulnerabilities, follow the private reporting process in `SECURITY.md`.

This repository is licensed under the GNU GPL v3.0 (see `LICENSE`).

Exception note: some Conxian public repositories use MIT (for example, `.github` and `conxius-platform`). This repository remains GPL v3.0 because it is the BOS governance and OpenSpec source of truth.

- [**CONTRIBUTING.md**](./CONTRIBUTING.md): Guidelines for contributing to the BOS.
- [**SECURITY.md**](./SECURITY.md): How to report vulnerabilities and our security posture.
- [**Trust & Proof Messaging**](./docs/TRUST_AND_PROOF_MESSAGING.md): Public-facing trust surface guidance.
- [**LICENSE**](./LICENSE): GNU GPL v3.0.
- [**CHANGELOG.md**](./CHANGELOG.md): History of BOS changes.
- [**RELEASING.md**](./RELEASING.md): Release process and changelog discipline.
- [**CODEOWNERS**](./.github/CODEOWNERS): Repository ownership and review guidance.

## Repository catalog

See [`docs/REPOSITORY_CATALOG.md`](./docs/REPOSITORY_CATALOG.md) for the org-level submodule catalog and pinning guidance.

## Repository hygiene

To maintain a clean and sovereign workspace, we adhere to strict hygiene standards:

- **`scripts/`**: Contains active utility scripts (e.g., `check_links.py`).
- **`ARCHIVE_MIGRATION.md`**: ZSE-safe pointers to legacy material intentionally kept out of the Git index.
- **`openspec/`**: Definitive technical specifications.
- **Artifact Hygiene**: Scratch scripts and temporary fix-up files (e.g., `*_fix.py`) are excluded from the repository to maintain a clean production environment.
