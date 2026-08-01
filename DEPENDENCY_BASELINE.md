# BOS Gate 0 — Dependency Baseline Inventory

**Accepted**: 2026-08-01
**Business head**: [`ba8ae6b`](https://github.com/Conxian/conxian-business/commit/ba8ae6b5e58ed2444c7f527c28324a442d1931c3)
**System of record**: GitHub (Linear workspace deprecated)

## Submodule pins

Pins are read from `.gitmodules` at the accepted business head. Divergence from
remote default-branch heads is noted where observed.

| Component | Business pin | Remote head (2026-08-01) | Diverged? |
|-----------|-------------|--------------------------|:---------:|
| **Conxian** (protocol) | [`bb2e68b`](https://github.com/Conxian/Conxian/commit/bb2e68b6) | [`79ec331`](https://github.com/Conxian/Conxian/commit/79ec3311) | ✅ yes |
| **conxian-gateway** | [`e61c839`](https://github.com/Conxian/conxian-gateway/commit/e61c8399) | same | no |
| **conxius-wallet** | [`a272223`](https://github.com/Conxian/conxius-wallet/commit/a2722237) | same | no |
| **conxian-nexus** | [`7b2ff9a`](https://github.com/Conxian/conxian-nexus/commit/7b2ff9ac) | same | no |
| **conxian-ui** | [`9d20038`](https://github.com/Conxian/Conxian_UI/commit/9d20038a) | — | — |
| **conxius-platform** | [`bb8b555`](https://github.com/Conxian/conxius-platform/commit/bb8b555e) | same | no |
| **conxius-orbit** | [`ded4954`](https://github.com/Conxian/conxius-orbit/commit/ded4954) | same | no |
| **conxius-enclave-sdk** | [`b9b264b`](https://github.com/Conxian/conxius-enclave-sdk/commit/b9b264b7) | same | no |
| **lib-conxian-core** | [`6f7e037`](https://github.com/Conxian/lib-conxian-core/commit/6f7e037e) | same | no |
| **conxian-market** | [`7c2afb0`](https://github.com/Conxian/conxian_market/commit/7c2afb04) (`update = none`) | [`369913c`](https://github.com/Conxian/conxian_market/commit/369913c6) | ✅ yes |
| **conxian-labs-site** | [`64e6f2a`](https://github.com/Conxian/conxian-labs-site/commit/64e6f2ab) | — | — |

## `.gitmodules` branch hints

All branch hints reconciled with upstream defaults:

| Submodule | Branch hint | Upstream default | Match? |
|-----------|------------|------------------|:------:|
| conxius-enclave-sdk | `main` | `main` | ✅ |
| All others | `main` | `main` | ✅ |

> Fixed in [`ba8ae6b`](https://github.com/Conxian/conxian-business/commit/ba8ae6b5): `conxius-enclave-sdk` was `master` → `main`.

## CI status against this baseline

All 9 repos green at the remote heads listed above. See [#933](https://github.com/Conxian/conxian-business/issues/933#issuecomment-5152984326) for full CI matrix.

## Role accountability

Recorded in [BOS governance tracker #942](https://github.com/Conxian/conxian-business/issues/942). Roles are public-safe (role-level only, no identities or secrets).

## Acceptance

This baseline is accepted as the Gate 0 dependency inventory. Any change to
submodule pins after this acceptance requires a new baseline revision and
re-verification of CI against the updated tuple.

---

*This manifest was created by an AI agent (OpenHands) on behalf of botshelomokoka.
It is a public-safe coordination artifact under Zero Secret Egress.*
