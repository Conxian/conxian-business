# Governance

This repository is governed by the Conxian Sovereign Autonomous Business (SAB).

This is a public repository. Governance rules must be documented without leaking privileged operational details.

Canonical business-purpose and public/private split guidance for this repo lives in `docs/BOS_BUSINESS_BUILDOUT.md`.

## Ownership

- **Repo owners:** defined by `CODEOWNERS`.
- **Policy owners:** `CODEOWNERS` is authoritative for governance, security, and documentation-policy changes.

## Approval model

1. All changes land via pull request.
2. Pull requests must link to a Linear issue.
3. Any change must be reviewed by the relevant code owners.
4. Changes that impact governance, security posture, OpenSpec requirements, or BOS boundaries must be documented:
   - update the relevant canonical docs (often `docs/DOCUMENTATION_ALIGNMENT_INDEX.md`), and
   - add a `CHANGELOG.md` entry when the change is externally visible.

## Documentation confidentiality (ZSE)

Conxian operates under a Zero Secret Egress (ZSE) mandate.

- Public-safe documentation may live in Git.
- Strategic, legal, operational, and administrative documents that are internal-only must be stored in the Linear Virtual Office and referenced from Git with a pointer.

## Policies

- Contributing guidelines: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](./SECURITY.md)
- License: [`LICENSE`](./LICENSE) (GNU GPL v3.0)
