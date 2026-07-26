# Governance

This repository is governed by the Conxian Sovereign Autonomous Business (SAB).

This repository is private (as of April 8, 2026), but is treated as public for boundary purposes under Zero Secret Egress (ZSE). Governance rules must be documented without leaking privileged operational details.

Canonical GitHub-first workflow and public-safe boundary guidance lives in `docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md`. Supporting business-purpose guidance lives in `docs/BOS_BUSINESS_BUILDOUT.md`.

Canonical parent-control alignment guidance for this repo (scope boundaries, control-domain mapping, evidence, rollback, and accountability) lives in `docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md`.

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

All public-safe work is coordinated through GitHub Issues, pull requests, and the organization Project when available. Changes must link the owning-repository GitHub issue, receive `CODEOWNERS` review, and follow documentation-alignment/`CHANGELOG.md` rules for boundary or policy changes. Use only an opaque external restricted-record token when a protected decision must be referenced.

## Documentation confidentiality (ZSE)

Conxian operates under a Zero Secret Egress (ZSE) mandate.

- Public-safe documentation may live in Git.
- Restricted legal, financial, security, identity, custody, recovery, strategy, and privileged operational records must remain in an approved non-Git restricted-record system. GitHub may contain only a minimum opaque token when needed; never copy protected content or access details.

## Policies

- Repository boundary: Treat this repo as public for ZSE boundary purposes. Restricted strategy, legal interpretations, operational runbooks, and infrastructure identifiers must remain in an approved non-Git restricted-record system.
- Contributing guidelines: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](./SECURITY.md)
- BOS business buildout and repo operating model: [`docs/BOS_BUSINESS_BUILDOUT.md`](./docs/BOS_BUSINESS_BUILDOUT.md)
- GitHub-first BOS operating model: [`docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md`](./docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md)
- Parent-control alignment baseline (CON-694): [`docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md`](./docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md)
- Branching and promotion: [`docs/BRANCHING_AND_PROMOTION_POLICY.md`](./docs/BRANCHING_AND_PROMOTION_POLICY.md)
- License: [`LICENSE`](./LICENSE) (GNU GPL v3.0)
