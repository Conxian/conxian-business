# Mainnet Readiness Checklist — Conxian Nexus (CON-396)

## Status: IN PROGRESS (v0.4.0)

This document is a lightweight index for `conxian-nexus` mainnet readiness. It is **not** an audit report.

The canonical evidence pack lives in the `conxian-nexus` repo (pinned by this repo’s `conxian-nexus` submodule):
- [conxian-nexus/docs/MAINNET_EVIDENCE.md](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/docs/MAINNET_EVIDENCE.md)

Links in this document are pinned to the same `conxian-nexus` submodule SHA shown above. If the submodule pin is updated, update the links here in the same change.

### Evidence index

| Area | Claim | Evidence |
| --- | --- | --- |
| Production sanitization | No testnet principals (`ST...`) in production paths | [scripts/check_production_boundary.sh](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/scripts/check_production_boundary.sh#L6-L44) |
| CI guardrails | Production boundary check runs in CI | [workflows/rust.yml](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/.github/workflows/rust.yml#L13-L30) |
| Core implementation | FSOC (First-Seen-On-Chain) sequencer logic exists | [src/executor/mod.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/executor/mod.rs#L24-L75) |
| Core implementation | Microblock reorg detection + rollback exists | [src/sync/mod.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/sync/mod.rs#L312-L343) |
| Core implementation | MMR persistence hooks exist | [src/sync/mod.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/sync/mod.rs#L369-L382), [src/state/mod.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/state/mod.rs#L397-L459) |
| Institutional ingress | ISO20022/PAPSS/BRICS trigger handler exists | [src/api/settlement.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/api/settlement.rs#L1-L162) |
| Institutional ingress | TEE attestation floor enforced | [src/api/settlement.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/api/settlement.rs#L38-L51) |
| Institutional ingress | 144-block time-lock proposal persisted | [src/api/settlement.rs](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/src/api/settlement.rs#L106-L161) |
| Release & hygiene | README / CHANGELOG exist | [README.md](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/README.md), [CHANGELOG.md](https://github.com/Conxian/conxian-nexus/blob/06531dc72a34f19a81a71aa44226399808d02b4c/CHANGELOG.md) |

### Notes

- “Implemented in code” is not the same as “verified in production.” Before declaring readiness, each claim should link to concrete evidence (tests, configs, runbooks, sign-off).
- In this repo, `Cargo.lock` should remain reproducible (`cargo metadata --locked`). Avoid landing lockfile diffs that don’t correspond to actual manifest changes.

### Gating criteria (before declaring READY)

- Link the evidence pack to specific CI runs (build/test) for the release tag or commit being asserted.
- Link an operational runbook for microblock reorg handling and a rollback validation procedure.
- Link an operational runbook for external settlement ingress (attestation floor, incident response, and time-lock release).
