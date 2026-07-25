# Public repository control matrix

> **Observation date:** 2026-07-25 (organization pin metadata rechecked at 2026-07-25T10:39:55Z)
>
> **Assurance boundary:** This is a public-presentation control review of repository metadata, root documentation, public ownership surfaces, and release discoverability. It is not a security audit, production certification, deployment attestation, or statement that every documented capability is operational.

## Scope and canonical references

This matrix covers the 12 public repositories named in [CON-1552](https://linear.app/conxian-labs/issue/CON-1552/produce-public-repo-control-matrix-and-portfolio-map). It records observable GitHub presentation controls and routes remediation to the owning repository. It does not redefine portfolio doctrine, maturity, readiness gates, or document classification.

Use these sources for the governing definitions and acceptance criteria:

- [`PORTFOLIO_DOCTRINE_REGISTER.md`](https://github.com/Conxian/conxian-business/blob/main/docs/PORTFOLIO_DOCTRINE_REGISTER.md) and [`DOCTRINE_ALIGNMENT_STANDARD.md`](https://github.com/Conxian/conxian-business/blob/main/docs/DOCTRINE_ALIGNMENT_STANDARD.md) — role, audience, claim-state, and public-safe boundaries. These canonical sources currently reside on `main`; the feature branch targets `dev` under the promotion policy.
- [`PORTFOLIO_BUSINESS_UNIT_MAP.md`](./PORTFOLIO_BUSINESS_UNIT_MAP.md), [`REPO_PORTFOLIO.md`](./REPO_PORTFOLIO.md), and [`PORTFOLIO_REPOSITORY_INVENTORY.md`](./PORTFOLIO_REPOSITORY_INVENTORY.md) — portfolio placement and repository relationships.
- [`REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md`](./REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md) — risk-adjusted readiness controls.
- [`GOVERNANCE_FILES_STANDARDIZATION.md`](./GOVERNANCE_FILES_STANDARDIZATION.md), [`GOVERNANCE.md`](../GOVERNANCE.md), [`RELEASING.md`](../RELEASING.md), and [`BRANCHING_AND_PROMOTION_POLICY.md`](./BRANCHING_AND_PROMOTION_POLICY.md) — governance, release, and promotion expectations.

### Posture legend

| Value | Meaning |
| --- | --- |
| `Pass` | The inspected public presentation has the expected baseline and no material clarification was identified in this review. |
| `Clarify` | The baseline is substantially present, but metadata, claims, versioning, terminology, or release evidence needs a bounded correction. |
| `Gap` | A material public baseline element is absent or not discoverable. |

Ownership below means only the publicly visible `CODEOWNERS` or governance file surface. It does not identify internal owners, approvers, or sensitive operating assignments.

## Primary control matrix

| Repository | Canonical role and intended audience | Visibility / default / metadata | Release presence | Public ownership surface | Posture | README or metadata clarification action | Release-process tightening action | Profile pin | Portfolio class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`Conxian/Conxian`](https://github.com/Conxian/Conxian) | Protocol contracts and integration interfaces; integrators, researchers, and compliance reviewers. | Public; `main`; not archived; description and root README present. | Latest GitHub release [`v1.0.0-rc1`](https://github.com/Conxian/Conxian/releases/tag/v1.0.0-rc1), 2025-09-20; a newer `v1.0.0` tag is visible without a corresponding latest-release record. | [`CODEOWNERS`](https://github.com/Conxian/Conxian/blob/main/CODEOWNERS) | `Clarify` | Qualify the README readiness badge as evidence-scoped; do not imply this presentation review certifies mainnet deployment. | Reconcile the release channel with the newer tag and publish or document the intended exception. | **Recommend** — protocol entrypoint. | Core |
| [`Conxian/conxian_ui`](https://github.com/Conxian/conxian_ui) | Browser interaction surface; end users, institutions, and integrators. | Public; `main`; not archived; root README present; repository description is blank. | Latest release [`v0.1.0`](https://github.com/Conxian/conxian_ui/releases/tag/v0.1.0), 2026-07-10. | [`CODEOWNERS`](https://github.com/Conxian/conxian_ui/blob/main/CODEOWNERS) | `Clarify` | Add a concise audience, scope, and non-custody description; keep browser UI claims separate from protocol implementation claims. | Document the release trigger, artifact/deployment evidence, and rollback reference for subsequent releases. | **Recommend** — visible browser access surface. | Supporting |
| [`Conxian/.github`](https://github.com/Conxian/.github) | Organization governance defaults and contributor templates; maintainers and contributors. | Public; `main`; not archived; description and root README present. | No GitHub release or tag. This is an acceptable governance-only exception when changes remain commit-addressable and reviewed. | [`CODEOWNERS`](https://github.com/Conxian/.github/blob/main/CODEOWNERS) | `Clarify` | Qualify broad operational/readiness wording as organization-default guidance, not portfolio-wide production evidence. | Record the no-release exception in the README and use dated change notes for material governance baseline changes. | **Currently pinned; not in proposed target** — important governance, but not a primary portfolio discovery surface. | Internal-adjacent (public governance) |
| [`Conxian/lib-conxian-core`](https://github.com/Conxian/lib-conxian-core) | Shared protocol, serialization, cryptographic, and state primitives; developers and integrators. | Public; `main`; not archived; description and root README present. | Latest release [`v0.2.11`](https://github.com/Conxian/lib-conxian-core/releases/tag/v0.2.11), 2026-07-15; root manifest, README, and changelog present `0.3.0`. | [`.github/CODEOWNERS`](https://github.com/Conxian/lib-conxian-core/blob/main/.github/CODEOWNERS) | `Clarify` | Preserve the shared-library boundary and avoid upgrading implementation text into audit or support certification. | Resolve the `0.3.0` manifest/documentation versus `v0.2.11` release mismatch before the next compatibility claim. | Do not pin — shared dependency is discoverable through core repositories. | Supporting |
| [`Conxian/conxian.github.io`](https://github.com/Conxian/conxian.github.io) | Public documentation and site hub; users, researchers, and partners. | Public; `main`; not archived; blank description and no root README observed. | No GitHub release or tag; no documented release/deployment exception was discoverable. | No public `CODEOWNERS` or governance file observed. | `Gap` | Add the public baseline: README, description, purpose, audience, canonical links, and public-safe claim boundary. | Define either a tagged release process or a documented commit-addressable site-deployment exception with rollback evidence. | Do not pin until the baseline is established. | Supporting |
| [`Conxian/conxian-gateway`](https://github.com/Conxian/conxian-gateway) | Institutional integration and compliance middleware; enterprise integrators and compliance reviewers. | Public; `main`; not archived; description and root README present, with a display-terminology conflict noted below. | Latest release [`v0.1.4`](https://github.com/Conxian/conxian-gateway/releases/tag/v0.1.4), 2026-07-13. | [`CODEOWNERS`](https://github.com/Conxian/conxian-gateway/blob/main/CODEOWNERS) | `Clarify` | Use the repository slug in portfolio copy and qualify institutional-grade, verification, and settlement statements by linked capability evidence. | Link each release to exact source identity, supported capability scope, and rollback/provenance evidence. | **Recommend** — enterprise integration entrypoint. | Core |
| [`Conxian/conxius-platform`](https://github.com/Conxian/conxius-platform) | Local stack composition and developer orchestration; developers, operators, and contributors. | Public; `main`; not archived; description and root README present and explicitly scoped to control-plane scaffolding. | Latest release [`v0.2.5`](https://github.com/Conxian/conxius-platform/releases/tag/v0.2.5), 2026-07-10. | [`CODEOWNERS`](https://github.com/Conxian/conxius-platform/blob/main/CODEOWNERS); [`GOVERNANCE.md`](https://github.com/Conxian/conxius-platform/blob/main/GOVERNANCE.md) | `Pass` | Keep the contributor/operator and orchestration boundary explicit; do not present it as an end-user or core protocol surface. | Continue linking releases to changelog, composition compatibility, and rollback evidence. | Do not pin — developer orchestration is a supporting discovery path. | Supporting |
| [`Conxian/conxian-nexus`](https://github.com/Conxian/conxian-nexus) | State, proof, synchronization, and telemetry infrastructure; institutions, integrators, and operators. | Public; `main`; not archived; description and root README present. | Latest release [`v0.4.22`](https://github.com/Conxian/conxian-nexus/releases/tag/v0.4.22), 2026-07-15; root manifest matches, but README status still presents `v0.4.19`. | [`.github/CODEOWNERS`](https://github.com/Conxian/conxian-nexus/blob/main/.github/CODEOWNERS) | `Clarify` | Update the README version and keep authoritative-state language bounded to documented proof and synchronization behavior. | Add an automated README/manifest/tag/release consistency gate. | **Recommend** — state and proof infrastructure entrypoint. | Core |
| [`Conxian/conxius-wallet`](https://github.com/Conxian/conxius-wallet) | Offline-first wallet and user-controlled signing client; end users and client integrators. | Public; `main`; not archived; description and root README present. | Latest release [`v1.9.2`](https://github.com/Conxian/conxius-wallet/releases/tag/v1.9.2), 2026-05-30; package manifest and README present `1.9.5`. | [`CODEOWNERS`](https://github.com/Conxian/conxius-wallet/blob/main/CODEOWNERS) | `Clarify` | Keep self-custody and hardware-isolation statements capability-scoped and aligned with current provider/release evidence. | Resolve the `1.9.5` manifest/README versus `v1.9.2` GitHub release mismatch and enforce a release-version check. | **Recommend** — primary user and signing surface. | Core |
| [`Conxian/conxian-labs-site`](https://github.com/Conxian/conxian-labs-site) | Public website and documentation distribution surface; users, partners, and researchers. | Public; `main`; not archived; root README present; description is only `Conxian-Labs`. | Latest release [`v1.1.0`](https://github.com/Conxian/conxian-labs-site/releases/tag/v1.1.0), 2026-07-10. | [`CODEOWNERS`](https://github.com/Conxian/conxian-labs-site/blob/main/CODEOWNERS); [`GOVERNANCE.md`](https://github.com/Conxian/conxian-labs-site/blob/main/GOVERNANCE.md) | `Clarify` | Replace the weak description with purpose, audience, and public-site scope; retain the legal builder/operator versus protocol boundary. | A no-GitHub-release exception is acceptable for this deployment-only site only if the README documents commit-addressable deployments and rollback evidence. The observed `v1.1.0` release means that exception is not currently invoked. | **Recommend** — public company and portfolio narrative surface. | Supporting |
| [`Conxian/conxius-enclave-sdk`](https://github.com/Conxian/conxius-enclave-sdk) | Enclave, signing, and attestation abstractions; integrators and security researchers. | Public; `main`; not archived; description and root README present, with a display-terminology conflict noted below. | Latest release [`v2.0.11`](https://github.com/Conxian/conxius-enclave-sdk/releases/tag/v2.0.11), 2026-07-15; root manifest presents `2.0.12`. | [`CODEOWNERS`](https://github.com/Conxian/conxius-enclave-sdk/blob/main/CODEOWNERS); [`GOVERNANCE.md`](https://github.com/Conxian/conxius-enclave-sdk/blob/main/GOVERNANCE.md) | `Clarify` | Use the repository slug in public copy and retain the README's beta/conditional, capability-specific evidence boundary. | Close the already-disclosed `2.0.12` manifest versus `v2.0.11` release gap before compatibility or production-support claims. | Do not pin — specialized supporting security library. | Supporting |
| [`Conxian/conxius-orbit`](https://github.com/Conxian/conxius-orbit) | Stacks contract deployment and operations tooling; developers, operators, and contributors. | Public; `main`; not archived; description and root README present, with a display-terminology conflict noted below. | Latest release [`v1.0.0`](https://github.com/Conxian/conxius-orbit/releases/tag/v1.0.0), 2025-10-04. | [`CODEOWNERS`](https://github.com/Conxian/conxius-orbit/blob/main/CODEOWNERS); [`GOVERNANCE.md`](https://github.com/Conxian/conxius-orbit/blob/main/GOVERNANCE.md) | `Clarify` | Use the repository slug in public display text and keep deployment-tooling claims separate from deployed-contract readiness. | Refresh or explicitly support the older release with current toolchain, compatibility, and rollback evidence. | Do not pin — developer deployment tooling is supporting. | Supporting |

## Organization profile pins

### Observed state

At 2026-07-25T10:39:55Z, the organization profile exposed two pinned repositories: [`Conxian/Conxian`](https://github.com/Conxian/Conxian) and [`Conxian/.github`](https://github.com/Conxian/.github). This is observed state only; this control matrix did not change organization settings.

### Recommended six-repository set

| Repository | Rationale |
| --- | --- |
| [`Conxian/Conxian`](https://github.com/Conxian/Conxian) | Protocol and integration entrypoint. |
| [`Conxian/conxius-wallet`](https://github.com/Conxian/conxius-wallet) | Primary user-controlled wallet and signing surface. |
| [`Conxian/conxian-gateway`](https://github.com/Conxian/conxian-gateway) | Enterprise integration and compliance middleware entrypoint. |
| [`Conxian/conxian-nexus`](https://github.com/Conxian/conxian-nexus) | State, synchronization, proof, and telemetry entrypoint. |
| [`Conxian/conxian-labs-site`](https://github.com/Conxian/conxian-labs-site) | Public company and portfolio orientation. |
| [`Conxian/conxian_ui`](https://github.com/Conxian/conxian_ui) | Browser-based public interaction and demonstration surface. |

This proposed target balances protocol, enterprise infrastructure, user access, public narrative, and browser discovery. It intentionally excludes `.github` even though that repository is currently pinned. The set is a recommendation only, not a record of applied organization settings; no organization-setting change is part of this control matrix.

## Outliers, ambiguities, and follow-up register

| Priority | Repository(s) | Finding | Follow-up action |
| --- | --- | --- | --- |
| P0 | [`Conxian/conxian.github.io`](https://github.com/Conxian/conxian.github.io) | Public baseline is missing: no root README, description, release/tag, public ownership surface, or documented deployment exception was observed. | Add the minimum public repository baseline before promoting or pinning the repository. |
| P1 | [`Conxian/lib-conxian-core`](https://github.com/Conxian/lib-conxian-core), [`Conxian/conxian-nexus`](https://github.com/Conxian/conxian-nexus), [`Conxian/conxius-wallet`](https://github.com/Conxian/conxius-wallet) | Public version/release mismatches: `0.3.0` versus `v0.2.11`; README `v0.4.19` versus manifest/release `v0.4.22`; `1.9.5` versus `v1.9.2`. | Reconcile the declared version surfaces and add deterministic consistency checks. |
| P1 | [`Conxian/Conxian`](https://github.com/Conxian/Conxian), [`Conxian/conxian-gateway`](https://github.com/Conxian/conxian-gateway), [`Conxian/.github`](https://github.com/Conxian/.github) | Public badges or copy can read as broader readiness, operational, or capability assurance than the evidence linked from the page establishes. | Add explicit claim-state qualifiers and links to exact readiness/capability evidence; avoid certification language. |
| P1 | [`Conxian/conxius-enclave-sdk`](https://github.com/Conxian/conxius-enclave-sdk) | The already-disclosed root-manifest/release gap remains visible (`2.0.12` versus `v2.0.11`). | Complete release coordination or revert the declared version before making compatibility or production-support claims. |
| P2 | [`Conxian/conxian_ui`](https://github.com/Conxian/conxian_ui), [`Conxian/conxian-labs-site`](https://github.com/Conxian/conxian-labs-site) | GitHub descriptions are blank or too weak to communicate scope and audience. | Add compact descriptions aligned with the doctrine register and public-safe boundary. |
| P2 | [`Conxian/conxian-gateway`](https://github.com/Conxian/conxian-gateway), [`Conxian/conxius-enclave-sdk`](https://github.com/Conxian/conxius-enclave-sdk), [`Conxian/conxius-orbit`](https://github.com/Conxian/conxius-orbit) | Repository descriptions or README headings use display terminology that conflicts with the current repository-slug nomenclature. This is a presentation finding only; it does not rename repositories or alter historical artifacts. | Use the exact repository slugs in new public copy and correct active presentation surfaces through each repository's normal review path. |
| P2 | [`Conxian/conxian-labs-site`](https://github.com/Conxian/conxian-labs-site) | A deployment-only no-release exception is reasonable, but must be explicit and evidence-backed; a GitHub release currently exists. | Document the exception criteria, commit/deployment traceability, and rollback evidence; otherwise continue the tagged-release path. |

## Evidence and reproducibility

Evidence was collected from each canonical GitHub repository page and its public `releases`, `tags`, root README, `CODEOWNERS`, governance file, and root manifest where applicable. Organization pin state was read from the GitHub organization pinned-items metadata and rechecked at 2026-07-25T10:39:55Z. The observation is time-bound; later repository or organization changes supersede this snapshot.

No private repository content, internal named ownership, organization settings, secret material, deployment credentials, or security-certification conclusions are included.

## BOS crystallization digest

### Entities

- **Repositories:** the 12 linked public repositories in the primary matrix.
- **Portfolio documents:** [`PORTFOLIO_DOCTRINE_REGISTER.md`](https://github.com/Conxian/conxian-business/blob/main/docs/PORTFOLIO_DOCTRINE_REGISTER.md), [`PORTFOLIO_BUSINESS_UNIT_MAP.md`](./PORTFOLIO_BUSINESS_UNIT_MAP.md), [`REPO_PORTFOLIO.md`](./REPO_PORTFOLIO.md), [`PORTFOLIO_REPOSITORY_INVENTORY.md`](./PORTFOLIO_REPOSITORY_INVENTORY.md), and [`REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md`](./REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md).

### Decisions

- The matrix is limited to public presentation controls and does not certify security, production readiness, or deployed capability.
- The recommended organization profile set is the six-repository set above; it is not an organization-settings change.
- Public ownership is represented only by observable `CODEOWNERS` and governance surfaces.

### Relationships

- Repository roles and audiences are derived from the canonical doctrine and portfolio maps; readiness actions route to the control-domain gates rather than creating a new taxonomy.
- The public repository set is related to the portfolio/document entities already indexed in [`BOS_KNOWLEDGE_GRAPH.md`](../BOS_KNOWLEDGE_GRAPH.md). This digest is a cross-reference only and does not assert new knowledge-graph edges or modify graph claims.
