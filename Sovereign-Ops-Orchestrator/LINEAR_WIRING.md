# Historical ExCo intake and wiring migration record

> **Status:** Legacy migration material; not an active intake standard
> **Superseded by:** [`docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md`](../docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md)
> **Authority details:** [`docs/GITHUB_NATIVE_BOS_WORKSPACE.md`](../docs/GITHUB_NATIVE_BOS_WORKSPACE.md)
> **Migration tracking:** [conxian-business#944](https://github.com/Conxian/conxian-business/issues/944)

This file preserves public-safe historical context for the former ExCo workflow. It must not be used to route new work, require a new external issue, or establish an external system as canonical.

## Current rule

- GitHub is canonical for public-safe BOS intake, status, pull-request traceability, sanitized decisions, and immutable evidence links.
- Create public-safe work in the owning repository and link implementation pull requests to that GitHub issue.
- Restricted legal, financial, security, identity, custody, recovery, strategy, or privileged operational records remain outside Git in an approved non-Git restricted-record system.
- When a restricted record must be acknowledged publicly, use only a non-descriptive `sha256(<64-lowercase-hex>)` commitment. Do not include a system name, location, access path, or sensitive metadata.

## Preserved historical model

Historical record: before the GitHub-first baseline, ExCo intake originated in Linear and public-safe GitHub artifacts were treated as mirrors. The former intake captured:

1. **Operating lens**
2. **Owner** (single accountable owner)
3. **Repo/business surface**
4. **Urgency/priority**
5. **Outcome + acceptance signal**
6. **Source links**

Protocol-adapter intake also captured the maturity lane fields defined in
[`docs/architecture/PROTOCOL_ADAPTER_MATURITY_LANES.md`](../docs/architecture/PROTOCOL_ADAPTER_MATURITY_LANES.md), including lane, rail scope, adapter interface, owner, cadence, risks, and promotion blockers.

The historical flow was:

1. discover the signal;
2. create or route a historical Linear issue (archived behavior);
3. triage ownership and urgency; and
4. link GitHub implementation artifacts back to that issue.

These steps are retained only as evidence of past state. They are superseded for current public-safe work and must not be copied into active guidance.

## Migration boundary

Issue #944 owns the classification-led migration of remaining Linear references. Do not mechanically replace protected pointers, copy restricted content into GitHub, or infer an unapproved restricted-record system. Historical references may remain only when clearly labelled as historical.
