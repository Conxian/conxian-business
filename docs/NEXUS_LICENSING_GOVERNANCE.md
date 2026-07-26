# Nexus licensing governance

**Status:** Canonical governance and evidence map

**Verified:** 2026-07-26

**Business tracker:** [Conxian/conxian-business#942](https://github.com/Conxian/conxian-business/issues/942)

## Purpose

This document establishes authority, RACI, evidence, and blocker boundaries for Nexus licensing. It does not choose license terms, approve relicensing, or authorize release.

## Canonical artifact map

| Artifact | Authority |
| --- | --- |
| [Business #942](https://github.com/Conxian/conxian-business/issues/942) | Portfolio governance, decisions, coordination, and sanitized evidence index. |
| [Nexus #174](https://github.com/Conxian/conxian-nexus/issues/174) | Nexus-local license execution tracker and repository acceptance. |
| [Nexus PR #173](https://github.com/Conxian/conxian-nexus/pull/173) | Technical guardrails only; it does not select first-party license terms or configure enterprise policy. |
| [`.github` #60](https://github.com/Conxian/.github/issues/60) | Portfolio licensing standards, matrix, metadata/notice policy, and shared CI controls after authorized decisions exist. |
| [Business #933](https://github.com/Conxian/conxian-business/issues/933) | Gate 1 impact only. Licensing activity does not satisfy Gate 1. |

The current Linear-first blocker wording in `.github` #60 is legacy and must be migrated to Business #942 before the tracker is fully aligned with the GitHub-native BOS policy. Issue #60 remains the implementation tracker for portfolio standards, the licensing matrix, metadata/notice policy, and shared CI controls; it is not decision authority.

## Authority and RACI

`A` = accountable decision authority, `R` = responsible executor, `C` = consulted, `I` = informed.

| Work | Business governance | Authorized licensor / counsel | GitHub org admin | Nexus maintainer |
| --- | --- | --- | --- | --- |
| Maintain authority map, decision status, and sanitized evidence | A/R | C | I | C |
| Decide licensor/rightsholder and whether relicensing is authorized | I | A/R | I | C |
| Decide Additional Use Grant, Change Date, Change License, package identifier, and exceptions | I | A/R | I | C |
| Configure organization/enterprise license policy and preserve ruleset enforcement | C | C | A/R | I |
| Implement authorized root license text and first-party package metadata | C | C | I | A/R |
| Maintain Nexus technical guardrails, dependency policy, notices, and SBOM controls | I | C | C | A/R |
| Accept exact Nexus candidate against repository-local checks | I | C | C | A/R |
| Assess Gate 1 impact | A/R under [#933](https://github.com/Conxian/conxian-business/issues/933) | I | I | C |

Repository access, authorship, or merge permission does not establish legal decision authority.

## Verified current blockers

As recorded in [Business #942](https://github.com/Conxian/conxian-business/issues/942) and [Nexus #174](https://github.com/Conxian/conxian-nexus/issues/174):

- the Nexus root `LICENSE` is an incomplete six-line Business Source License 1.1 placeholder;
- first-party Cargo license metadata is absent;
- active ruleset `19543903` includes external `license_compliance_scanning`;
- the external License compliance check reports that no license policy is configured;
- Nexus #174 and PR #173 already track repository-local work and must not be duplicated;
- no authorized decision is recorded for the licensor/rightsholder, Additional Use Grant, Change Date, Change License, package identifier, exceptions, or release authorization;
- organization Project v2 creation remains dependent on a Conxian organization administrator creating **`BOS — Portfolio Operations`**.

These are point-in-time blockers, not license advice. Re-verify mutable repository and check state before relying on them.

## Decision and evidence flow

1. The authorized licensor/counsel records an authorized, sanitized decision in [Business #942](https://github.com/Conxian/conxian-business/issues/942), with restricted rationale kept outside GitHub.
2. The GitHub organization administrator configures the approved portfolio/enterprise policy without weakening ruleset `19543903` or its external scan.
3. Nexus maintainers implement only the authorized terms in [Nexus #174](https://github.com/Conxian/conxian-nexus/issues/174) and the applicable pull request.
4. Nexus maintainers attach exact-SHA repository-local evidence, including license-policy checks, package metadata validation, notices/SBOM outputs where required, and all required CI results.
5. Business governance indexes the sanitized outcome in #942. Gate 1 remains independently governed by [Business #933](https://github.com/Conxian/conxian-business/issues/933).

## Zero Secret Egress boundary

Do not place privileged legal advice, contracts, contributor assignment records, private repository excerpts, credentials, private endpoints, signer data, raw configuration, or restricted runbooks in GitHub. Record only authorized terms, sanitized status, accountable roles, exact-SHA technical evidence, and approved restricted-store pointers.

## Explicit non-claims

This document and its linked business tracker do **not**:

- choose BSL/BUSL parameters or any other license term;
- declare first-party package license metadata;
- replace or amend any license file;
- approve relicensing or assert legal approval;
- configure GitHub organization or enterprise licensing policy;
- satisfy Gate 1;
- authorize release, deployment, production, or mainnet activity.
