# Branch and promotion standard

This is the concise operational source for branch usage. The normative
requirements are in `openspec/specs/git-management/spec.md`.

## Branch roles

- `main` is the GitHub default branch and the production branch.
- `dev` is the non-production integration branch; it is never the GitHub
  default branch.
- `staged` is the candidate branch between integration and production.

## Exact routes

| Work | Pull request route |
|---|---|
| Normal feature/fix/docs/chore/hotfix/dependency work | allowed ordinary work branch -> `dev` |
| Integration promotion | `dev` -> `staged` |
| Immutable generated integration promotion | `promotion/dev-to-staged-<source-sha>` -> `staged` |
| Production promotion | `staged` -> `main` |
| Immutable generated production promotion | `promotion/staged-to-main-<source-sha>` -> `main` |

Ordinary fork pull requests may target `dev`. Promotions into `staged` or
`main` must be same-repository. There is no direct `dev` -> `main` route, no
generic `promotion/*` route, and no Dependabot-to-`main` exception.

Generated candidates use the full source SHA in the branch name and record the
exact source SHA, target-base SHA, and commit window in the pull request body.
The recorded values must match the pull request refs and SHAs.

## Evidence

- Every route includes its matching checklist from
  `docs/PROMOTION_CHECKLISTS.md`.
- Every direct or generated route into `main` includes the complete Mainnet
  Acceptance Evidence Pack.
- Generated candidate creation is idempotent for one source SHA and never
  rewrites an immutable candidate with a bare force push.

## Enforcement boundary

`.github/workflows/branch-promotion-policy.yml` and
`scripts/branch_promotion_policy.py` are checked-in controls. The workflow uses
`pull_request_target`, explicit read-only permissions, and a shallow checkout of
the repository default branch. It executes only that trusted policy script
against `GITHUB_EVENT_PATH`; it never checks out or executes PR head/merge code
and never interpolates PR-controlled title, body, head SHA, or head ref into a
shell command.

PR #971 is a manually owner-reviewed bootstrap, not secure self-validation. The
live PR continues to use the older workflow from `main` until this change is
merged. Only a later sentinel PR can prove the new trusted default-branch
workflow operationally.

Default-branch selection, branch protections/rulesets, required checks,
approval counts, deletion rules, and force-push rules are administrator-owned
settings. Until an authorized administrator verifies them, their state is
**not administrator-verified**. If the settings API is inaccessible, report
that state as **unverified/blocked**, never passing.
