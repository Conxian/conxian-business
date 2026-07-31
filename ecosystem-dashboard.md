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
| Issue | Repo | Title |
|-------|------|-------|
| #480 | Conxian | Developer Sandbox: TTFV < 15 minutes |
| #943 | conxian-business | Establish GitHub-first operating model |

### P1 (High)
| Issue | Repo | Title |
|-------|------|-------|
| #532 | Conxian | Partnership security, legal, and commercialization launch gate |
| #530 | Conxian | Partnership gateway, Stacks.js SDK, event indexing |
| #529 | Conxian | Partner usage ledger and atomic split settlement |
| #527 | Conxian | Partnership fee policy, legal model, asset scope |
| #515 | Conxian | Enforce Main Branch Merge Gates, Reconcile CODEOWNERS |
| #496 | Conxian | Partnership Fee Contracts |
| #488 | Conxian | 2% Protocol Fee Collection |
| #944 | conxian-business | Retire Linear-first references, publish migration map |

### P2
| Issue | Repo | Title |
|-------|------|-------|
| #507 | Conxian | sBTC Vault Implementation |
| #500 | Conxian | Production oracle config + DEX wiring |

### BOS Governance Gates (#890 → #932–#938)
| Gate | Status | Title |
|------|--------|-------|
| #932 Gate 0 | BLOCKED | Re-baseline and accountable ownership |
| #933 Gate 1 | NOT MET | Reproducible candidate, pins, validators, green CI |
| #934 Gate 2 | NOT MET | Safe authority-transfer semantics |
| #935 Gate 3 | NOT MET | Testnet rehearsal, readback, failure drills |
| #936 Gate 4 | BLOCKED | Hardware-backed signing/attestation |
| #937 Gate 5 | BLOCKED | Independent security/release acceptance |
| #938 Gate 6 | NOT AUTHORIZED | Mainnet handoff and post-state readback |

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
