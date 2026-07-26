# Governance

This repository is governed by the Conxian Sovereign Autonomous Business (SAB).

This repository is private (as of April 8, 2026), but is treated as public for boundary purposes under Zero Secret Egress (ZSE). Governance rules must be documented without leaking privileged operational details.

Canonical business-purpose and public/private split guidance for this repo lives in `docs/BOS_BUSINESS_BUILDOUT.md`.

Canonical parent-control alignment guidance for this repo (scope boundaries, control-domain mapping, evidence, rollback, and accountability) lives in `docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md`.

Canonical GitHub-native intake, coordination, evidence, and source-of-truth rules live in [`docs/GITHUB_NATIVE_BOS_WORKSPACE.md`](./docs/GITHUB_NATIVE_BOS_WORKSPACE.md). GitHub Issues and pull requests are authoritative for all new BOS work; Linear references are historical/archive provenance only.

## Ownership

- **Repo owners:** defined by `CODEOWNERS`.
- **Policy owners:** `CODEOWNERS` is authoritative for governance, security, and documentation-policy changes.

## Branching and Promotion

All repositories in the Conxian portfolio must adhere to the [**Branching and Promotion Policy**](./docs/BRANCHING_AND_PROMOTION_POLICY.md).

- **`main` branch**: Reserved for mainnet-only production code. No stubs, mocks, or placeholders.
- **`staged` branch**: Reserved for mainnet candidate validation and promotion to `main`.
- **`dev` branch**: Default branch for development and testnet-oriented logic.

Feature branches should validate locally first, then land in `dev` via pull request.

## Approval model

All changes land via pull request and must follow the workflow defined in `docs/BOS_BUSINESS_BUILDOUT.md` (GitHub issue/PR linkage, `CODEOWNERS` review, and documentation-alignment/`CHANGELOG.md` update rules for boundary or policy changes).

## Documentation confidentiality (ZSE)

Conxian operates under a Zero Secret Egress (ZSE) mandate.

- Public-safe documentation may live in Git.
- Credentials, private endpoints, signer data, raw configuration, privileged legal advice, and restricted runbooks must remain in approved restricted stores. GitHub may contain sanitized status and approved pointers only.

## Policies

- Repository boundary: Treat this repo as public for ZSE boundary purposes. Internal-only strategy, legal interpretations, operational runbooks, and infrastructure identifiers must live in the sovereign coordination layer.
- Contributing guidelines: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](./SECURITY.md)
- BOS business buildout and repo operating model: [`docs/BOS_BUSINESS_BUILDOUT.md`](./docs/BOS_BUSINESS_BUILDOUT.md)
- GitHub-native BOS workspace: [`docs/GITHUB_NATIVE_BOS_WORKSPACE.md`](./docs/GITHUB_NATIVE_BOS_WORKSPACE.md)
- Nexus licensing governance: [`docs/NEXUS_LICENSING_GOVERNANCE.md`](./docs/NEXUS_LICENSING_GOVERNANCE.md)
- Parent-control alignment baseline (CON-694): [`docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md`](./docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md)
- Branching and promotion: [`docs/BRANCHING_AND_PROMOTION_POLICY.md`](./docs/BRANCHING_AND_PROMOTION_POLICY.md)
- License: [`LICENSE`](./LICENSE) (GNU GPL v3.0)
