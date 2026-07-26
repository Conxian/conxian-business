# GitHub-native BOS workspace

**Status:** Canonical

**Decision date:** 2026-07-26

**Canonical tracker:** [Conxian/conxian-business#942](https://github.com/Conxian/conxian-business/issues/942)

## Operating decision

GitHub Issues and pull requests are authoritative for all new Business Operations System (BOS) work. `Conxian/conxian-business` is the governance and evidence authority; each owning repository remains authoritative for its implementation and repository-local acceptance.

One organization Project v2, **`BOS — Portfolio Operations`**, is the intended portfolio planning view once a Conxian organization administrator creates it. The Project is a view over authoritative issues and pull requests, not a second source of truth. Project creation is an administrator dependency recorded in [#942](https://github.com/Conxian/conxian-business/issues/942).

Linear references are immutable historical provenance or archive pointers only. Do not create new canonical Linear items, mirror authority into Linear, or require a Linear record before GitHub work can proceed.

## Authority boundaries

| Surface | Authority and responsibility |
| --- | --- |
| `Conxian/conxian-business` | Portfolio policy, business governance, decision status, cross-repository coordination, sanitized evidence index, and knowledge crystallization. |
| Owning repository | Implementation, repository-local design and acceptance criteria, tests, CI, release artifacts, and exact-SHA technical evidence. |
| Organization Project v2 | Planning view, prioritization, and reporting across linked authoritative artifacts. It must not invent legal, gate, deployment, or release status. |
| Approved restricted store | Credentials, restricted configuration, privileged legal material, and restricted operational detail. GitHub stores only sanitized status and approved pointers. |

Business governance must not duplicate implementation trackers. Implementation repositories must link back to the applicable business decision or policy record when portfolio governance is required.

## Zero Secret Egress and information classification

Private GitHub repositories are not secret stores. Do not place any of the following in issues, pull requests, Projects, comments, Actions logs, artifacts, or committed files:

- credentials, tokens, private keys, or recovery material;
- private endpoints, internal network identifiers, or access paths;
- signer identities, signer data, quorum details, or ceremony records;
- raw configuration or secret-bearing logs;
- privileged legal advice, contracts, or restricted legal rationale;
- restricted deployment, incident, custody, treasury, or recovery runbooks.

GitHub may contain sanitized status, authorized public-safe decisions, exact-SHA evidence, non-sensitive acceptance results, and approved restricted-store pointers. A pointer must identify the record class and accountable role without reproducing restricted content.

Use these classifications:

| Classification | GitHub handling |
| --- | --- |
| Public-safe | May be committed or posted when accurate and necessary. |
| Internal sanitized | Status, decision outcome, and evidence pointer only; omit restricted detail. |
| Restricted | Do not place in GitHub. Store only in an approved restricted system. |
| Secret | Do not place in GitHub or general documentation systems. Use the approved secret-management system. |

## Issue and pull-request linkage

1. Create new BOS governance, intake, and decision work in `conxian-business` using the applicable issue form.
2. Create implementation work in the repository that owns the changed behavior.
3. Link child implementation issues and pull requests to the governing business issue when a portfolio decision, dependency, or evidence roll-up exists.
4. Link the governing business issue to each owning-repository artifact once; avoid duplicate trackers for the same authority.
5. Record acceptance evidence against immutable commit SHAs or durable artifacts. A default branch, open PR, or Project status is not acceptance evidence.
6. Historical Linear URLs may remain when they establish dated provenance. Label them explicitly as historical, archive, or migration context.

## Status taxonomy

Use status words consistently in issues, Project fields, and evidence summaries:

- **Proposed** — scope exists but accountable approval has not been recorded.
- **Decision required** — work is blocked on a named decision authority.
- **Approved** — an authorized decision is recorded; this does not imply implementation or release.
- **In progress** — an accountable owner is executing accepted scope.
- **Blocked** — a named dependency prevents progress.
- **In review** — a pull request or decision record awaits review.
- **Accepted** — repository-local acceptance criteria passed for an immutable candidate.
- **Done** — the scoped artifact is complete; separate gates may remain open.
- **Archived** — retained only for history and not active authority.

Do not infer `Approved`, `Accepted`, release authorization, deployment, production, mainnet, or legal approval from issue closure, merge state, or Project placement.

## Evidence conventions

- Prefer links to issues, pull requests, commits, Actions runs, release artifacts, and versioned policy documents.
- Name the evidence producer, observed date, exact candidate SHA, check or artifact, and outcome.
- Separate **observed**, **approved**, **merged**, **accepted**, **deployed**, and **operational** claims.
- Record negative results and blockers; do not convert missing evidence into implied success.
- Keep raw restricted evidence outside GitHub and publish only a sanitized result plus an approved pointer.
- Update `BOS_KNOWLEDGE_GRAPH.md` when a session changes a decision, entity, relationship, authority boundary, or material blocker.

## Project v2 schema

The organization administrator should create **`BOS — Portfolio Operations`** with these fields:

| Field | Type | Values / use |
| --- | --- | --- |
| Status | Single select | Proposed, Decision required, Approved, In progress, Blocked, In review, Accepted, Done, Archived |
| Owning repository | Text | Canonical `owner/repo` value. |
| Accountable role | Text | Role, not a secret identity or credential-bearing record. |
| Workstream / control domain | Single select or text | Governance, Legal/licensing, Security, Quality, Service management, Resilience, Privacy, Partner governance, Release. |
| Classification | Single select | Public-safe, Internal sanitized, Restricted pointer only. |
| Decision authority | Text | Role authorized to decide; do not infer from repository access. |
| Target / review date | Date | Planning signal only, not authorization. |
| Evidence | Text | Durable sanitized evidence link or pointer. |
| Dependencies | Text | Linked authoritative issues/PRs or named external dependency. |

Add each authoritative issue or pull request once. Project automation may update planning fields, but it must not overwrite issue/PR authority or infer legal and release states.

## Migration rules

1. All new work starts in GitHub after the 2026-07-26 decision.
2. Do not bulk-copy restricted or secret content from Linear into GitHub.
3. Preserve useful Linear links as dated historical/archive provenance. Add a GitHub successor link when active work continues.
4. Do not maintain synchronized GitHub/Linear status or duplicate canonical descriptions.
5. If a legacy Git stub points to Linear for restricted content, retain it as archive/migration context until an approved restricted-store pointer replaces it.
6. Update active intake, contribution, governance, and release documents when they require Linear-first work.

## Branch and default-branch administration

Repository branch roles remain governed by `docs/BRANCHING_AND_PROMOTION_POLICY.md`. Feature work targets `dev`; promotions proceed through `staged` to `main` as defined there.

The organization/repository administrator owns any GitHub default-branch or ruleset configuration decision. Documentation must not silently redefine the configured default branch. A default-branch change requires an explicit admin decision, updated protection/rulesets, and aligned documentation; it does not authorize production or mainnet release.

## Source-of-truth precedence

When records conflict, use this order:

1. Authorized, dated decisions in the governing GitHub issue or merged policy document.
2. Owning-repository source, issue, pull request, and exact-SHA acceptance evidence for implementation facts.
3. `conxian-business` evidence indexes and knowledge-graph summaries.
4. Project v2 planning fields.
5. Historical/archive Linear records and other dated snapshots.

Higher precedence does not expand an artifact's authority. Business policy cannot prove implementation; implementation cannot invent legal or portfolio decisions; planning state cannot prove acceptance.
