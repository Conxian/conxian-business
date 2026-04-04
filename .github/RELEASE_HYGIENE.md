# Release and merge hygiene

This repository uses GitHub Actions workflows in `.github/workflows/` as the source of truth for what must pass before merging to `main`.

The goals:

- Keep `main` always mergeable and safe to deploy.
- Ensure every merge has clear provenance (Linear issue + PR).
- Make releases and changelogs easy to audit.

## Required checks guidance

### Always-on checks for PRs targeting `main`

These workflows run on every pull request to `main` and are expected to be green before merge:

- `Conxian Unified CI` → `Repo Hygiene (ZSE & Submodules)`
  - Validates Zero Secret Egress (ZSE) knowledge retention via `scripts/verify_knowledge_retention.py`.
  - Validates submodule integrity via `scripts/verify_submodule_integrity.py`.
- `Secret Scan` → `Secret Scan (gitleaks)`
- `Dependency Review` → `Dependency Review`

### Label-gated suites (opt-in, based on change scope)

Some suites only run when a label is applied. Apply the label early so CI starts immediately.

| When you touch… | Add label | Expected CI jobs |
| --- | --- | --- |
| `conxian-gateway/` or infra deployment concerns | `infra` | `Conxian Unified CI` → `Gateway Suite` |
| `conxian-nexus/` or `lib-conclave-sdk/` | `b2b` | `Conxian Unified CI` → `B2B Suite (Nexus & SDK)` |
| `conxius-wallet/` | `b2c` | `Conxian Unified CI` → `B2C Wallet Suite` |
| transparency audit or documentation validation | `audit` | `Conxian Unified CI` → `Transparency Audit & Docs` |
| StacksOrbit testnet simulation scripts | `simulation` | `Conxian Unified CI` → `Testnet Simulation` |

Notes:

- The label-gated jobs only run for PRs opened from branches in this repository (not forks).
- For PRs opened from forks, a maintainer is responsible for ensuring the relevant suites run before merge.
- `showcase-dapp/` PRs can also trigger `Showcase DApp - Vercel Deployment` preview when `infra` is applied.

## PR and merge expectations

- No direct commits to `main`. Use a PR.
- One PR = one focused change (keep it reviewable).
- PRs should map to a Linear issue (include it in the PR description).
- Follow `CODEOWNERS` for review routing.
- Before merge:
  - Required checks are green.
  - Appropriate label-gated suites ran (when relevant).
  - Changelog is updated when user-facing behavior or security posture changes.

Merge preference:

- Prefer squash-merge so `main` stays readable and the merge commit message captures the PR intent.

## Changelog and release policy references

- Changelog file: `CHANGELOG.md`
- Changelog + release notes format: `docs/RELEASE_NOTES_AND_CHANGELOG.md`
- Templates:
  - `docs/templates/CHANGELOG_TEMPLATE.md`
  - `docs/templates/RELEASE_NOTES_TEMPLATE.md`
