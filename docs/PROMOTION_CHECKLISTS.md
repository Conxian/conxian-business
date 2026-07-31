# Promotion checklists

Branch roles and routes are defined normatively in
`openspec/specs/git-management/spec.md` and operationally in
`docs/BRANCH_AND_PROMOTION_STANDARD.md`.

## Ordinary work -> `dev`

Use for allowed feature, fix, documentation, chore, hotfix, and dependency
branches, including ordinary fork pull requests.

<!-- PROMOTION:FEATURE->DEV -->
### Feature -> dev promotion checklist

- [ ] I targeted `dev`, the non-production integration branch.
- [ ] I ran and recorded relevant local validation for the touched scope.
- [ ] The pull request is focused and contains no unrelated branch-governance or product changes.
- [ ] Any wallet, signer, treasury, or deployment boundary affected by the work is described for the non-production lane.

## `dev` -> `staged`

Use for direct `dev` promotion or an exact immutable
`promotion/dev-to-staged-<source-sha>` candidate. Promotions must be
same-repository. Generated candidates also include the exact-evidence block.

<!-- PROMOTION:DEV->STAGED -->
### Dev -> staged promotion checklist

- [ ] Integrated non-production/testnet validation completed on `dev` and is linked.
- [ ] Required checks are recorded for the exact promotion source SHA; hosted-check blockers are distinguished from code failures.
- [ ] Wallet boundary checks are explicitly recorded.
- [ ] Signer boundary checks are explicitly recorded.
- [ ] Treasury boundary checks are explicitly recorded.
- [ ] Deployment boundary checks are explicitly recorded.
- [ ] Applicable pins, lockfiles, and artifact provenance are recorded without rewriting unrelated pins.

### Exact promotion evidence

Required for a generated candidate:

- Promotion source SHA: `<40-character lowercase source SHA>`
- Promotion target-base SHA: `<40-character lowercase target SHA at creation>`
- Promotion commit window: `<target-base-sha>..<source-sha>`

## `staged` -> `main`

Use for direct `staged` promotion or an exact immutable
`promotion/staged-to-main-<source-sha>` candidate. Promotions must be
same-repository. There is no direct `dev` or Dependabot route to `main`.

<!-- PROMOTION:STAGED->MAIN -->
### Mainnet acceptance evidence pack

Complete every section required by
`openspec/specs/mainnet-acceptance-evidence-pack/spec.md` in the pull request
body or link a versioned in-repository pack. Generated candidates also include
the exact promotion evidence block above. A heading without completed evidence
does not authorize merge.
