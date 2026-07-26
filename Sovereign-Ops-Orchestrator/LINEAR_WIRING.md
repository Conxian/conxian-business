# Deprecated Linear wiring compatibility stub

**Status:** Archived compatibility pointer as of 2026-07-26.

GitHub Issues and pull requests are authoritative for all new BOS work. Follow [`docs/GITHUB_NATIVE_BOS_WORKSPACE.md`](../docs/GITHUB_NATIVE_BOS_WORKSPACE.md) and the repository issue forms. Do not create a new Linear issue or mirror canonical authority into Linear.

Existing Linear URLs may be retained only as immutable historical/archive provenance. This filename remains to preserve old links; it is not an active intake standard.

## Historical compatibility fields

When interpreting an archived Linear intake record, the historical fields were:

1. **Operating lens**
2. **Owner** (single accountable owner)
3. **Repo/business surface**
4. **Urgency/priority**
5. **Outcome + acceptance signal**
6. **Source links**

## GitHub-native successor

New work uses the BOS work intake or governance/legal decision request issue form. Protocol-adapter work also includes the lane extension fields from
[`docs/architecture/PROTOCOL_ADAPTER_MATURITY_LANES.md`](../docs/architecture/PROTOCOL_ADAPTER_MATURITY_LANES.md):

1. **Maturity lane** (`Build-now`, `Pilot`, `Partner`, `Research`)
2. **Default handling note** (if lane was omitted at creation, record that it defaulted to `Research`)
3. **Rail scope**
4. **Target adapter interface**
5. **Owner** (single accountable owner)
6. **Review cadence**
7. **Risk register**
8. **Promotion blockers**

## ZSE boundary

Private GitHub is not a secret store. Credentials, private endpoints, signer data, raw configuration, privileged legal advice, and restricted runbooks stay in approved restricted stores. GitHub contains sanitized status and approved pointers only.
