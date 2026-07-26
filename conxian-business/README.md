# `conxian-business`

> **Classification:** Canonical · Public-safe
> **Role:** Governance and specification repository for the Conxian Business Operations System (BOS).
> **Audience:** Contributors, integrators, auditors, and partners.
> **Operating label:** Production intent.
> **Maturity / claim state:** Beta; governance and specification artifacts are **Implemented**, while architecture proposals remain **Target-state**.

This directory contains the public-safe BOS governance surface: OpenSpec references, architecture notes, service-loop descriptions, templates, and link-preserving stubs. It is not a production service, custody system, discretionary treasury, or market-operation console.

## Scope

- Define and explain BOS governance, ownership boundaries, and specification workflows.
- Describe infrastructure routing, orchestration, compliance integration, verification, and tenant-isolation patterns.
- Keep public documentation aligned with evidence and with the separation between Conxian protocol/DAO components and Conxius client/access/developer tooling.
- Preserve safe pointers when detailed strategy, legal, security, financial, or operational material belongs in the authorized Linear workspace under Zero Secret Egress (ZSE).

## Non-scope

- Holding, managing, or exercising discretionary control over user or customer assets.
- Operating a market, proprietary trading strategy, investment fund, or managed-yield service.
- Extracting, reselling, or monetizing raw user data.
- Serving as the canonical store for internal strategy, privileged operations, credentials, or custody procedures.

Protocol contracts and DAO rules may implement escrow, settlement, treasury, or yield behavior. In these documents those terms mean contract-, participant-, or governance-level state transitions; they do not mean Conxian-Labs custody, discretionary fund control, or market operation.

## Canonical doctrine and evidence

- [Doctrine Alignment Standard](../docs/DOCTRINE_ALIGNMENT_STANDARD.md)
- [Portfolio Doctrine Register](../docs/PORTFOLIO_DOCTRINE_REGISTER.md)
- [Documentation Alignment Index](../docs/DOCUMENTATION_ALIGNMENT_INDEX.md)
- [Portfolio Business-Unit Map](../docs/PORTFOLIO_BUSINESS_UNIT_MAP.md)
- [Repo Portfolio](../docs/REPO_PORTFOLIO.md)
- [Trust & Proof Messaging](../docs/TRUST_AND_PROOF_MESSAGING.md)
- [Claim vs Evidence Matrix](../docs/CLAIM_EVIDENCE_MATRIX.md)
- [Boundary Decision Log](../docs/BOUNDARY_DECISION_LOG.md)
- [OpenSpec](../openspec/README.md)

## Related specifications

- [BOS Runtime Ownership Map](./BOS_RUNTIME_OWNERSHIP_MAP.md)
- [BOS Platform Specification](./BOS_PLATFORM_SPEC.md)
- [Service Loop](./SERVICE_LOOP.md)
- [Multi-Tenant Orchestration Guide](./BOS_MULTI_TENANT_ORCHESTRATION.md)
- [BOS state-machine public-safe stub](./BOS_STATE_MACHINE.stub.json)

## Governance and security

Repository contribution, licensing, and security expectations are defined in [`GOVERNANCE.md`](../GOVERNANCE.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`SECURITY.md`](../SECURITY.md), and [`.github/CODEOWNERS`](../.github/CODEOWNERS). Do not place sensitive operational or strategy material in public-safe documentation.
