# BOS Gates Advancement Plan

| Metadata | Value |
|---|---|
| Classification | Public-safe, non-authorization |
| Status | Phase 0 — 2026-08-02 baseline |
| Authority | [BOS-001 #890](https://github.com/Conxian/conxian-business/issues/890) |

## Gate Status Summary

| Gate | Issue | Status | Blocker | Automatable |
|------|-------|--------|---------|-------------|
| 0 — Re-baseline | [#932](https://github.com/Conxian/conxian-business/issues/932) | ✅ RESOLVED | — | ✅ Complete |
| 1 — Green CI | [#933](https://github.com/Conxian/conxian-business/issues/933) | ✅ 100% | — | ✅ Complete |
| 2 — Authority transfer | [#934](https://github.com/Conxian/conxian-business/issues/934) | Pending | Gate 0 + Protocol #499 deployment | 📋 Plan only |
| 3 — Testnet rehearsal | [#935](https://github.com/Conxian/conxian-business/issues/935) | Pending | Gates 0-2 + testnet infrastructure | 📋 Plan only |
| 4 — Attestation | [#936](https://github.com/Conxian/conxian-business/issues/936) | Unblocked | Enclave P0s (#240, #241, #242) | 🔧 In progress |
| 5 — Security acceptance | [#937](https://github.com/Conxian/conxian-business/issues/937) | Pending | Enclave #202 + independent review | 📋 Plan only |
| 6 — Mainnet handoff | [#938](https://github.com/Conxian/conxian-business/issues/938) | Pending | All above gates | 📋 Plan only |

## Gate 2 — Authority Transfer Semantics

**Required:** Exact-candidate semantic/authorization tests, fail-closed evidence, authorized testnet execution receipts, independent post-state readback.

**Dependencies:**
- Protocol [#499](https://github.com/Conxian/Conxian/issues/499): governance/authority implementation
- Merged PR [#523](https://github.com/Conxian/Conxian/pull/523): authority code (validate-protocol failed on merge)

**Next action:** Re-run validate-protocol on current main SHA. If green, produce exact-SHA authorization test suite.

## Gate 3 — Testnet Rehearsal

**Required:** Exact-candidate rehearsal covering positive/negative authorization, pause, recovery, rotation, rollback, receipts, independent post-state readback.

**Dependencies:**
- Gates 0-2 (blocked)
- Testnet environment (needs provisioning)
- Rehearsal automation scripts

**Next action:** Create rehearsal runbook template. Provision testnet when Gates 0-2 clear.

## Gate 4 — Hardware-Backed Attestation

**Required:** Provider-backed signing (AWS Nitro, Android KeyMint), trusted attestation inputs, freshness/revocation, distributed replay, runtime evidence, accountable owner.

**Dependencies (Enclave P0 chain):**
- [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240): Attestation roots, collateral, revocation, distributed replay
- [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241): Android KeyMint/StrongBox + Play Integrity
- [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242): AWS Nitro attestation + KMS secret-release
- [#198](https://github.com/Conxian/conxius-enclave-sdk/issues/198): CCTP / account abstraction fail-closed
- [#200](https://github.com/Conxian/conxius-enclave-sdk/issues/200): WASM secret boundary hardening

**Next action:** Triage each Enclave P0. Advance #242 (#AWS Nitro) as highest-leverage first step.

## Gate 5 — Security/Release Acceptance

**Required:** Independent security review with exact-SHA evidence, release acceptance sign-off, unresolved finding list.

**Dependencies:**
- [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202): Security review evidence
- Independent reviewer engagement (human)
- Release candidate pinned SHAs

**Next action:** Prepare security review package (repo list, SHA pins, threat model references).

## Gate 6 — Mainnet Handoff

**Required:** Post-state readback, handoff ceremony evidence, operational runbooks, incident response plan.

**Dependencies:** All Gates 0-5.

**Next action:** Create mainnet handoff runbook template. Schedule when all gates clear.



## Gate 0 Resolution (2026-08-03)

All human blockers resolved:

| Blocker | Resolution |
|---------|-----------|
| Non-Git restricted-record successor | **conxian-business** (private GitHub repo) |
| Accountable owner | **admin@conxian-labs.com / botshelo@conxian-labs.com** |
| Linear workspace | **Closure authorized** — [#944](https://github.com/Conxian/conxian-business/issues/944) |
| Organization Project | **BOS Control Plane** in conxian-business — [.github #61](https://github.com/Conxian/.github/issues/61) |

Gates 2-6 are now unblocked and can advance sequentially:
- **Gate 2** → authority-transfer semantic tests on protocol #499/#523
- **Gate 3** → testnet rehearsal with exact candidate SHA
- **Gate 4** → provider qualification (AWS Nitro, Android KeyMint)
- **Gate 5** → independent security review
- **Gate 6** → mainnet handoff ceremony


---

## Non-Authorization Boundary

This document defines coordination artifacts only. It does not authorize production action, release, acceptance, or security review completion. Each gate requires independent verification evidence per its owning issue.

---

*Governed by [GitHub-first BOS research-cycle operating model](GITHUB_FIRST_BOS_OPERATING_MODEL.md).*
