# Branching and promotion policy

The normative policy is
[`openspec/specs/git-management/spec.md`](../openspec/specs/git-management/spec.md).
The concise operating instructions are
[`docs/BRANCH_AND_PROMOTION_STANDARD.md`](./BRANCH_AND_PROMOTION_STANDARD.md).

## Hierarchy

1. `main` is the GitHub default and production branch.
2. `dev` is the non-production integration branch, never the GitHub default.
3. `staged` is the candidate lane between `dev` and `main`.

Normal work starts from an ordinary work branch and targets `dev`. Promotion is
ordered `dev` -> `staged` -> `main`.

## Enforced routes

- Ordinary `feat/*`, `feature/*`, `fix/*`, `docs/*`, `chore/*`, `hotfix/*`, and
  `dependabot/*` pull requests may target `dev`; ordinary fork pull requests
  are allowed there.
- Only same-repository `dev` or
  `promotion/dev-to-staged-<full-source-sha>` may target `staged`.
- Only same-repository `staged` or
  `promotion/staged-to-main-<full-source-sha>` may target `main`.
- Direct `dev` -> `main`, Dependabot -> `main`, forked promotions, generic
  `promotion/*`, malformed candidates, and evidence/SHA mismatches are blocked.

Generated routes are immutable snapshots. Their bodies record the exact source
SHA, target-base SHA, and `<target-base-sha>..<source-sha>` commit window.

## Trusted enforcement execution

The branch-policy workflow runs on `pull_request_target` with read-only
permissions. It shallow-checks out the repository default branch and runs only
that trusted copy of `scripts/branch_promotion_policy.py` against the event JSON.
It does not check out/import/execute a PR head or merge commit, and it does not
interpolate PR-controlled title/body/head fields into shell commands.

Draft PR #971 is the finite, manually owner-reviewed bootstrap for this design.
It cannot securely self-prove the new workflow because GitHub evaluates the live
PR with the older workflow on `main`. Operational proof requires a later
sentinel PR after the trusted workflow is merged.

## Merge evidence

- Use the route checklist in `docs/PROMOTION_CHECKLISTS.md`.
- Every direct or generated route into `main` requires the full Mainnet
  Acceptance Evidence Pack defined by
  `openspec/specs/mainnet-acceptance-evidence-pack/spec.md`.
- Runtime, deployment, contamination, signer, treasury, and ownership evidence
  remains governed by the applicable specialist policies.

## Administration status

Checked-in policy describes expected behavior and can be tested locally. It is
not evidence that live GitHub default-branch or protection settings are active.
Those settings require separate authorized administrator verification. An
inaccessible settings API is an unverified/blocked result, not a pass.
