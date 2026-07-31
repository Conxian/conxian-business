# Conxian Ecosystem Dashboard — Session 46
## Generated: 2026-07-31 03:43 UTC

---

## 1. Repository Map (16 repos)

| Repo | Type | Issues | PRs | Dependabot |
|------|------|--------|-----|------------|
| `Conxian/Conxian` | Clarity/TS (npm) | 10 | 1 (#611) | 4 (1 fixed) |
| `Conxian/conxian-business` | Monorepo (submodules) | 13 | 1 (#978) | 61 (1 fixed) |
| `Conxian/conxius-wallet` | TS (pnpm) | 3 | 0 | 3 |
| `Conxian/conxius-orbit` | TS (pnpm) | 2 | 0 | 0 |
| `Conxian/conxian-gateway` | Rust/TS (cargo+pnpm) | 5 | 0 | 9 |
| `Conxian/lib-conxian-core` | Rust | 2 | 0 | 0 |
| `Conxian/conxian-nexus` | Rust (cargo) | 2 | 2 | 3 |
| `Conxian/conxius-platform` | TS (pnpm) | 5 | 0 | 7 |
| `Conxian/conxian_ui` | Next.js (pnpm) | 1 | 0 | 13 |
| `Conxian/conxian_market` | — | 2 | 0 | 0 |
| `Conxian/conxian-labs-site` | — | 2 | 0 | — |
| `Conxian/conxius-enclave-sdk` | — | 2 | 0 | — |
| `Conxian/conxian.github.io` | — | 1 | 0 | — |
| `Conxian/.github` | — | — | — | — |
| `Conxian/.github-private` | — | — | — | — |
| `Conxian/demo-repository` | — | 0 | 0 | — |
| **TOTAL** | | **48** | **4** | **~100** |

---

## 2. Priority Breakdown — Open Issues

### P0 (Critical)
| Issue | Repo | Title | Code Location | Status |
|-------|------|-------|---------------|--------|
| #480 | Conxian | Developer Sandbox: TTFV < 15 minutes | `cxn-sandbox/` uses old `@conxian/sdk` + `ConxianGateway`. Live SDK is `@conxian/client-sdk` at `packages/client-sdk/`. Sandbox inside gateway at `conxian-gateway/examples/developer-sandbox/` uses correct SDK. | Sandbox uses stale mock SDK. Gateway sandbox is current. |
| #943 | conxian-business | Establish GitHub-first operating model | Meta: BOS governance restructure | BLOCKED by Linear capacity |

### P1 (High)
| Issue | Repo | Title | Code Location |
|-------|------|-------|---------------|
| #532 | Conxian | Partnership security, legal, and commercialization launch gate | Meta: needs legal/compliance sign-off |
| #530 | Conxian | Partnership gateway, Stacks.js SDK, event indexing | `contracts/partners/` (if exists) or new contract work |
| #529 | Conxian | Partner usage ledger and atomic split settlement | `contracts/treasury/revenue-distributor.clar`, `contracts/agents/fiscal-orchestrator.clar` |
| #527 | Conxian | Partnership fee policy, legal model, asset scope | Meta: business decision precedes code |
| #515 | Conxian | Enforce Main Branch Merge Gates, Reconcile CODEOWNERS | `.github/CODEOWNERS`, branch protection rules, `scripts/branch_promotion_policy.py` |
| #496 | Conxian | Partnership Fee Contracts | Fee collection: `contracts/treasury/` path; related to #488, #529 |
| #488 | Conxian | 2% Protocol Fee Collection | `contracts/treasury/revenue-distributor.clar`, `contracts/treasury/allocation-policy.clar` |
| #944 | conxian-business | Retire Linear-first references, publish migration map | Meta: BOS governance |

### P2
| Issue | Repo | Title |
|-------|------|-------|
| #507 | Conxian | sBTC Vault Implementation |
| #500 | Conxian | Production oracle config + DEX wiring |

### BOS Governance Gates (#890 → #932–#938)

**Root cause:** No approved restricted Linear tracker exists (Linear `USAGE_LIMIT_EXCEEDED` on `activeIssueCount`). Without an internal system-of-record, no gate can formally advance. GitHub issue hierarchy (#932–#938) serves as public-safe coordination mirrors only.

**Gate 0 blockers:** Linear capacity, accountable role assignment, accepted immutable baseline.
**Gate 1 blockers:** Divergent SHAs between main/dev/staged; two required business validators absent; GitHub Actions blocked by billing/spending limit (runs don't execute); no candidate-wide green CI.
**Gates 4-5 blockers:** Hardware-backed signing/attestation depends on enclave-sdk issues #195, #200, #202.
**Gate 6:** Not authorized until all prior gates clear.

| Gate | Status | Title | Actual Blocker |
|------|--------|-------|----------------|
| #932 Gate 0 | BLOCKED | Re-baseline and accountable ownership | Linear capacity + accountable roles unassigned |
| #933 Gate 1 | NOT MET | Reproducible candidate, pins, validators, green CI | SHA divergence + Actions billing block + 2 validators absent |
| #934 Gate 2 | NOT MET | Safe authority-transfer semantics | Depends on Gate 0+1 |
| #935 Gate 3 | NOT MET | Testnet rehearsal, readback, failure drills | Depends on Gate 0-2 |
| #936 Gate 4 | BLOCKED | Hardware-backed signing/attestation | Depends on enclave-sdk #195, #200, #202 |
| #937 Gate 5 | BLOCKED | Independent security/release acceptance | Depends on Gate 4 |
| #938 Gate 6 | NOT AUTHORIZED | Mainnet handoff and post-state readback | All prior gates |

---

## 3. Session 46 PRs

| PR | Repo | Title | Addresses |
|----|------|-------|-----------|
| [#611](https://github.com/Conxian/Conxian/pull/611) | Conxian | Clarity fixes + service stubs | Chain-check compliance, test coverage |
| [#978](https://github.com/Conxian/conxian-business/pull/978) | conxian-business | Session 46 submodule pin + Dependabot guide | Submodule tracking, security documentation |

---

## 4. Dependabot Security Alerts — Status

| Status | Count | Detail |
|--------|-------|--------|
| ✅ Fixed | 1 | postcss GHSA-r28c-9q8g-f849 (Conxian/Conxian) |
| ⚠️ Unfixable | 1 | elliptic GHSA-848j — no patch (Conxian/Conxian) |
| 📋 Documented | ~60 | pnpm repos need local `pnpm update` (see `dependabot-fixes.md`) |

### Critical alert
- **node-tar** GHSA-23hp-3jrh-7fpw (critical): Fixed by updating tar transitive dep in pnpm workspace

### Top fix command (run locally)
```bash
cd conxian-business
for dir in conxian-ui conxius-platform conxian-gateway conxius-wallet; do
  (cd $dir && pnpm update)
done
cd conxian-gateway && cargo update webpki-roots
cd ../conxian-nexus && cargo update webpki-roots
```

---

## 5. Next Steps / Gaps

| Gap | Priority | Action |
|-----|----------|--------|
| Pnpm repos Dependabot | HIGH | Run `pnpm update` locally in conxian-ui, conxius-platform, conxian-gateway, conxius-wallet |
| Cargo Dependabot | HIGH | `cargo update` in conxian-gateway, conxian-nexus |
| BOS Gate 0 (#932) | P0 | Session 46 work partially addresses re-baseline; needs explicit gate evidence |
| BOS Gate 1 (#933) | P0 | Session 46 CI is green (18/18 tests); submodule pins established |
| Conxian PR #611 merge | P1 | Needs review → merge → update submodule pin |
| conxian-business PR #978 merge | P1 | Needs review → merge |
| Issue #888 (MAINTENANCE) | P2 | Marked "Completed" — can likely be closed |
| elliptic replacement | P3 | Replace elliptic with noble-curves (@noble/secp256k1) |
