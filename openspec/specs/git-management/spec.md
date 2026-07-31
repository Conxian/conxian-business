# git-management Specification

## Purpose

Define the normative Git branch hierarchy, promotion routes, evidence, ownership,
and safe synchronization requirements for the Conxian workspace.

## Requirements

### Requirement: Canonical branch hierarchy

The repository MUST use these roles without ambiguity:

- `main` is the GitHub default branch and the production branch.
- `dev` is the non-production integration branch. It MUST NOT be configured or
  described as the GitHub default branch.
- `staged` is the candidate branch between integration and production.

Normal feature, fix, documentation, chore, hotfix, and dependency-update work
MUST target `dev` first. Fork pull requests MAY target `dev` under the same
ordinary-work checklist requirements.

#### Scenario: Selecting a base for ordinary work

- **WHEN** a contributor opens ordinary work from an allowed work branch
- **THEN** the pull request targets `dev`
- **AND** includes the Feature -> dev checklist

### Requirement: Exact promotion route matrix

The repository MUST enforce only these routes:

| Target | Accepted source |
|---|---|
| `dev` | ordinary `feat/*`, `feature/*`, `fix/*`, `docs/*`, `chore/*`, `hotfix/*`, or `dependabot/*` work branch, including a fork |
| `staged` | in-repository `dev`, or `promotion/dev-to-staged-<source-sha>` |
| `main` | in-repository `staged`, or `promotion/staged-to-main-<source-sha>` |

`<source-sha>` MUST be the full lowercase 40-character source commit SHA.
Broad `promotion/*` matching MUST NOT authorize a route. Direct `dev` ->
`main`, Dependabot -> `main`, forked promotions, malformed candidates, merges,
resets, bulk cherry-picks, and bypasses based only on actor identity MUST be
rejected.

#### Scenario: Promoting integration to candidate

- **WHEN** a pull request targets `staged`
- **THEN** its source is exactly `dev` or an exact generated dev candidate
- **AND** the source repository is this repository
- **AND** the Dev -> staged checklist is present

#### Scenario: Promoting candidate to production

- **WHEN** a pull request targets `main`
- **THEN** its source is exactly `staged` or an exact generated staged candidate
- **AND** the source repository is this repository
- **AND** the Mainnet Acceptance Evidence Pack is complete

### Requirement: Immutable generated candidates

Automation-generated candidates MUST use the exact source SHA in the branch
name and MUST record these values in the pull request body:

- `Promotion source SHA`
- `Promotion target-base SHA`
- `Promotion commit window` as `<target-base-sha>..<source-sha>`

The candidate branch suffix, pull request head SHA, recorded source SHA, target
base SHA, and commit window MUST agree. Candidate publication MUST NOT rewrite
an existing ref with a bare force push. Re-running automation for the same lane
and source SHA MUST find the same candidate pull request idempotently.

If automation cannot create the pull request, it MUST fail closed and report a
manual-PR fallback that preserves the immutable candidate ref and evidence.

### Requirement: Mainnet acceptance evidence

Both direct and generated routes into `main` MUST include a Mainnet Acceptance
Evidence Pack satisfying
[`openspec/specs/mainnet-acceptance-evidence-pack/spec.md`](../mainnet-acceptance-evidence-pack/spec.md).

### Requirement: Finite governance bootstrap

A governance change that introduces this exact enforcement MAY use one finite
bootstrap exception only when it is keyed to one pull request number, the exact
`promotion/con-1571-governance-bootstrap` head, the `main` base, and this
repository. It MUST reject every near-match and MUST NOT authorize another pull
request after that numbered pull request closes or merges.

PR #971 is a manually owner-reviewed bootstrap. It MUST NOT be described as
self-validating: until it merges, the live pull request is evaluated by the
older workflow already present on the default branch. The trusted enforcement
design introduced here can be operationally proven only after merge, through a
later sentinel pull request that exercises the default-branch workflow.

### Requirement: Trusted branch-policy execution

The branch-promotion enforcement workflow MUST run on `pull_request_target`
with explicit read-only permissions. It MUST shallow-check out
`${{ github.event.repository.default_branch }}` and execute only the policy
script from that trusted checkout against `GITHUB_EVENT_PATH`.

The enforcement job MUST NOT check out, import, or execute a pull request head,
pull request merge commit, or other pull-request-controlled file. Pull request
title, body, head SHA, and head ref MUST NOT be interpolated into a shell
command. Policy decisions MAY parse those fields only as untrusted data from
the event JSON.

### Requirement: Checked-in policy versus live administration

Tracked workflows and validators define the policy Git can review. GitHub
default-branch, ruleset, required-check, review, deletion, and force-push
settings are separate administrator-controlled state. Documentation and static
validation MUST describe inaccessible live settings as unverified or blocked,
never as passing or enforced.

### Requirement: Ownership and business-unit boundaries

- `CODEOWNERS` MUST express review ownership.
- Governance and release-policy changes under `openspec/`, `.github/`, `docs/`,
  or `scripts/` MUST receive the owners' review required by live repository
  administration.

### Requirement: Safe repository and submodule synchronization

Repository tooling MUST report dirty trees, unmerged paths, detached submodule
heads, and missing/inconsistent gitlink definitions. Synchronization MUST stop
when the root or a submodule is dirty or when a gitlink lacks a valid
`.gitmodules` mapping.
