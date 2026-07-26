# GitHub-First BOS Operating Model

> **Status:** Proposed implementation baseline
> **Scope:** Public-safe Business Operations System (BOS) coordination
> **Tracking:** [conxian-business#943](https://github.com/Conxian/conxian-business/issues/943)
> **Last updated:** 2026-07-26

## Purpose and Zero Secret Egress boundary

GitHub is the canonical coordination surface for **public-safe** BOS work intake, prioritization, delivery status, pull-request traceability, sanitized decisions, and immutable evidence links. Repository visibility does not change this boundary: a private GitHub repository is still not a secret store and does not authorize restricted data.

Do not place restricted legal, financial, security, identity, custody, recovery, strategy, or privileged operational records in Git repositories, GitHub Issues, pull requests, Projects, Actions logs, releases, advisories, attachments, or comments. Those records remain in an **approved non-Git restricted-record system**. GitHub may contain only the minimum opaque reference token needed to prove that a restricted record exists; it must not reveal protected content, access details, or sensitive metadata.

The approved opaque restricted-record token is a non-descriptive SHA-256 commitment in `sha256(<64-lowercase-hex>)` form, consistent with the boundary log's `sha256(hex)` rule. The commitment must not encode a record name, system name, location, access path, person, or other descriptive metadata. Any alternate token or commitment format requires separately approved governance before use. This document does not create a token or hash for any real restricted record.

If classification is uncertain, stop before posting. Ask an accountable maintainer to classify the material through an approved channel, then continue with a sanitized issue or opaque token only.

## Sources of truth

| Surface | Canonical public-safe use | Must not contain |
| --- | --- | --- |
| GitHub Issues | Intake, scope, owner repository, control domain, priority, acceptance criteria, dependencies, sanitized decisions, and delivery state | Restricted details or copied restricted records |
| Pull requests | Proposed changes, linked issue, review history, exact diff, validation results, and merge traceability | Restricted rationale, credentials, privileged configuration, or protected attachments |
| Organization `BOS Control Plane` Project | Cross-repository prioritization, status, dependencies, decision flags, evidence state, and portfolio views | Restricted records or descriptive fields that expose their contents |
| Repository documentation | Versioned policies, specifications, decisions, interfaces, and public-safe operating guidance | Secrets, restricted records, or privileged operational instructions |
| GitHub Actions and checks | Reproducible validation state tied to a commit SHA | Secret values, restricted payloads, or unnecessarily verbose sensitive logs |
| GitHub Releases and security advisories | Release provenance and public release notes; private advisories for vulnerability coordination within GitHub's security model | General restricted business records, secrets, or unrelated privileged operations data |
| Approved non-Git restricted-record system | Canonical restricted legal, financial, security, identity, custody, recovery, strategy, and privileged operational records | Public-safe execution status may be summarized, but protected content must not be copied back into GitHub |

## Public-safe issue lifecycle

1. **Classify before submission.** Confirm the proposed issue is public-safe. If it is not clearly public-safe, stop and move the protected record through the approved restricted process.
2. **Create in the owning repository.** The repository responsible for the deliverable owns the canonical issue. Portfolio-level coordination may be tracked in `conxian-business`, but it does not replace the owning repository's issue or pull request.
3. **Triage and prioritize.** Set or record the required metadata below. Add the issue to the organization Project when available and appropriate.
4. **Plan and deliver.** Link dependencies and the implementing pull request. Keep implementation discussion public-safe.
5. **Validate.** Record checks and evidence using immutable links wherever possible.
6. **Close with outcome.** State the delivered, declined, superseded, or blocked outcome and link the merged commit, release, or follow-up tracker.

### Required metadata

Every active BOS issue must identify:

- data classification acknowledgement (`public-safe`);
- owning repository;
- accountable role or repository owner, without inventing a person or approval;
- control domain;
- status and priority;
- target lane or delivery stage when applicable;
- acceptance criteria;
- dependencies and blockers;
- evidence state and immutable evidence links when evidence exists;
- whether a decision is required;
- an opaque restricted-record token only when necessary.

Project field values may carry this metadata once the Project exists. Until then, issue-form fields, labels, links, and checklists are the public-safe record.

The required `evidence_state` vocabulary is deterministic across the BOS issue forms and the target Project schema:

- `Not started` — evidence work has not begun;
- `Planned` — evidence work is scoped or scheduled but no qualifying evidence is available;
- `Evidence available` — qualifying public-safe immutable or commit-bound links exist and must be recorded where the form requires or provides an evidence field;
- `Blocked` — evidence cannot currently be produced; record the public-safe blocker without exposing restricted detail; and
- `Not applicable` — the issue has no evidence-producing outcome; explain this in the issue scope or acceptance criteria when it is not self-evident.

Evidence state is lifecycle metadata, not evidence itself. Selecting `Evidence available` does not replace immutable links. The cross-repository delivery form continues to require an evidence plan or links; the BOS change form requires links when evidence exists but permits them to remain empty before evidence is available.

## Cross-repository ownership and evidence

The repository that owns a deliverable retains its issue, implementation, validation, release, license artifacts, and rollback responsibility. A portfolio issue may coordinate multiple owning-repository issues, but must link to them rather than duplicate their full content.

Evidence links must be immutable or commit-bound whenever the platform supports it. Prefer a full commit SHA, check run tied to that SHA, release tag, advisory identifier, merged pull request, or permalink to a specific issue comment. Do not use mutable branch heads, local paths, screenshots without provenance, or copied restricted records as final evidence.

## Licensing responsibility split

`conxian-business` coordinates public-safe portfolio licensing policy, status, dependencies, and evidence. Each owning repository retains control of its own license text, package metadata, notices, dependency policy, CI checks, and release artifacts. Only an authorized legal rights-holder can select or approve legal terms.

A repository does not legally license another repository. A BOS tracker, Project item, pull request, or policy summary is not legal approval and must not be treated as authority to relicense first-party work. Licensing implementation remains tracked in [Conxian/.github#60](https://github.com/Conxian/.github/issues/60) and [Conxian/conxian-nexus#174](https://github.com/Conxian/conxian-nexus/issues/174).

## Legacy Linear-reference migration

The dated audit found 102 tracked files and 293 Linear-first references. This baseline does not mechanically replace them. [conxian-business#944](https://github.com/Conxian/conxian-business/issues/944) owns a controlled, classification-led migration in which each reference receives exactly one disposition:

| Disposition | Rule |
| --- | --- |
| `historical` | Retain only when the reference is evidence of past state; label the surrounding text clearly as historical. |
| `retire` | Remove an obsolete active instruction or pointer with no replacement required. |
| `GitHub mapping` | Replace active public-safe intake, delivery, or status instructions with the canonical GitHub issue, pull request, Project, or repository-document link. |
| `restricted-record token` | Replace a protected pointer with the approved non-descriptive `sha256(<64-lowercase-hex>)` commitment without copying content, access details, or descriptive metadata. |
| `rewrite` | Rewrite the surrounding guidance so it states the current GitHub-first workflow and ZSE boundary accurately. |

Migration must not copy restricted content into GitHub, infer a restricted system name, or transform a protected record into a descriptive public summary. Inventory, exceptions, and validation belong to #944.

## Organization Project schema and safe use

The proposed private organization Project is named `BOS Control Plane`. Creation and administration are tracked in [Conxian/.github#61](https://github.com/Conxian/.github/issues/61) and are currently blocked on authorized organization administration.

The target schema is:

- Status
- Priority
- Program
- Owning repository
- Control domain
- Data classification
- Target lane
- Dependency
- Evidence state
- Decision required

Recommended views are Gate / executive, Delivery, Security / compliance, ZSE migration, and Blocked on admin. The Project is an index of public-safe GitHub artifacts, not a document store. Do not paste restricted records into fields, item descriptions, drafts, or attachments. Use an opaque restricted-record token only when necessary.

## Branch and promotion policy

The repository currently has a documented `dev` → `staged` → `main` promotion flow while GitHub reports `main` as the default branch. This operating model does not silently choose between a `main`-default trunk model and a `dev`-default promotion model. Reconciliation, settings verification, and any policy change are deferred to [conxian-business#945](https://github.com/Conxian/conxian-business/issues/945).

Until #945 records an approved model, contributors must follow the applicable repository policy and explicit pull-request target for the work at hand without claiming unverified branch protections.

## Governance and change control

- Changes to this operating model require a GitHub issue, a linked pull request, repository-owner review through `CODEOWNERS`, and public-safe validation evidence.
- Boundary changes require an update to `docs/BOUNDARY_DECISION_LOG.md`, `docs/DOCUMENTATION_ALIGNMENT_INDEX.md`, and `BOS_KNOWLEDGE_GRAPH.md` when entity or relationship semantics change.
- Formal approval must not be inferred from implementation. Until an authorized approval record exists, this document remains a proposed implementation baseline.
- Restricted decisions may be represented only by an opaque token plus a sanitized outcome necessary for public-safe execution.
- Cross-repository changes must be implemented and reviewed in each owning repository.

### Rollback criteria

Rollback or suspend a workflow change if it:

- causes or risks restricted-data egress;
- breaks issue or pull-request traceability;
- assigns ownership to the wrong repository;
- weakens required reviews, checks, or evidence retention;
- treats a Project or BOS tracker as legal approval;
- depends on an unapproved branch model; or
- cannot be reversed without restoring restricted content to GitHub.

Rollback must remove or revert only public-safe workflow artifacts. Never restore restricted content to GitHub as part of rollback. Record the reason, affected commit or pull request, and safe follow-up issue.

## Canonical trackers

- [conxian-business#943 — GitHub-first operating model and restricted-record boundary](https://github.com/Conxian/conxian-business/issues/943)
- [conxian-business#944 — Linear-reference migration map](https://github.com/Conxian/conxian-business/issues/944)
- [conxian-business#945 — branch and promotion reconciliation](https://github.com/Conxian/conxian-business/issues/945)
- [Conxian/.github#61 — BOS Control Plane Project](https://github.com/Conxian/.github/issues/61)
- [Conxian/.github#60 — portfolio licensing implementation](https://github.com/Conxian/.github/issues/60)
- [Conxian/conxian-nexus#174 — Nexus licensing governance](https://github.com/Conxian/conxian-nexus/issues/174)
