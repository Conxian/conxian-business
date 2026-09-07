# Conxian AGENTS.md

## BOS Operational Standards
> **Version**: 1.8 (2026-09-07 — System upgrade: Rust 1.98.1 + Node 24)
> **Archive**: `docs/archive/AGENTS_archive_session_58.md` (historical session log)

---

### Session 63 Summary (2026-09-07)
- **Rust 1.97.1 → 1.98.1** (latest stable, 2026-09-03 patch fixes a rustc vtable miscompilation) across all 4 Rust repos (#346/#305/#380/#279). Two new clippy lints fixed by refactor: `needless_late_init` (enclave-sdk `src/enclave/cloud.rs`) + `chunks_exact_to_as_chunks` (lib-core fuzz `as_chunks::<33>()`).
- **Node 20/22 → 24** across all JS repos (wallet #530, ui #173, platform #1265, labs-site #66); `actions/setup-node` v4 → v7.
- **Neon branch limit (#1073)** — resolved by pruning 9 stale `preview/*` branches.
- **Stale/broken dependabot PRs closed** — gateway #372 (stale `dev`), wallet #527/#528 (secp256k1 partial bump → needs coordinated `bitcoin 0.32.102` + `secp256k1 0.33.1`), platform #1263 (lockfile drift), business #1091 (Vercel no-op).

### Session 62 Summary (2026-09-07)
- **Submodule full sync** — every public submodule gitlink advanced to its latest `main` (PR #1088 ✅): gateway `bb48a13`, nexus `ceb8791`, ui `f6a3ead`, enclave-sdk `12c4351`, platform `e171a7a` (captures CONXIAN_API_TOKEN #1264), wallet `a0809ec`, lib-core `101ef0c`; labs-site `b106176` (at tip); market frozen (`update=none`).
- **Lockfile regen** — `Cargo.lock` sha3 0.11→0.12 (+`sponge-cursor`); `pnpm-lock.yaml` conxius-wallet `@noble/curves`/`@noble/hashes` + overrides. Resolved #1072 (pnpm drift) and #1087 (submodule sync).
- **MSRV normalization** — gateway `rust-version` 1.97→1.97.1 (PR #378 ✅); enclave-sdk pin → v2.0.17 (PR #1086 ✅).
- **No-regression verification** — `cargo check --locked` + `cargo test --locked --workspace` + `pnpm install --frozen-lockfile` + `pnpm --filter control-plane build` all pass.
- **Toolchain** — Rust `1.97.1` (LTS anchor); Node `24`; pnpm `10.28.0`.

## Current State

### Repository Map

| Repo | Crate/Package | Version | Tag | Published |
|------|-------|---------|-----|-----------|
| conxius-enclave-sdk | `conxius-enclave-sdk` | 2.0.17 | v2.0.17 | ✅ crates.io |
| lib-conxian-core | `lib-conxian-core` | 0.3.3 | v0.3.3 | ✅ crates.io |
| conxian-gateway | `conxian-gateway` | 0.1.5 | v0.1.5 | — |
| conxian-nexus | `conxian-nexus` | 0.4.23 | v0.4.22 | — |
| conxius-platform | `conxius-platform` (npm) | 0.2.5 | v0.2.5 | — |
| conxius-wallet | `conxius-wallet` (npm) | 1.9.5 | v1.9.2 | — |

> **Submodule gitlinks now track each repo's `main`** (re-synced 2026-09-07, PR #1092), not release tags:
> gateway `d77952e`, nexus `bc87000`, ui `bee4e03`, enclave-sdk `11add87`, platform `1a2f78d`, wallet `4bf89aa`, lib-core `c14f2e5`; labs-site `9dabf1c`; market frozen (`update=none`).
> `conxius-orbit` is no longer a submodule (dangling gitlink removed). `conxian-market` remains `update = none`.
> Nexus `0.4.23` and wallet `1.9.5` are ahead of their latest tags (unreleased bumps).

### CI Status (2026-09-07)
| Repo | Status | Note |
|------|--------|------|
| lib-conxian-core | 🟢 Green | All CI, audit, hygiene checks pass |
| conxian-gateway | 🟢 Green | rust-version normalized (#378); Build/Clippy/Test/audit green |
| conxius-wallet | 🟢 Green | Dependency audit, unit tests, lint, typecheck pass |
| conxian-nexus | 🟢 Green | Latest main green; prior #250/#252/#253 no longer open |
| conxius-enclave-sdk | 🟡 Coverage Enforcement | Known false-positive (crates.io rate-limit) |
| conxian-business | 🟢 Mostly green | `Validate workspace` passes; Neon branch limit resolved (#1073); Node 24 via `setup-node` v7 (#1074) |

### Secrets Configured
| Secret | Where | Status |
|--------|-------|--------|
| GITLEAKS_LICENSE | repo → Settings → Actions secrets | ✅ Set (license key present) |
| CI_SUBMODULES_PAT | repo? | Unknown — may be needed for repo-hygiene submodule init |

### Active PRs (2026-09-07)
- **conxian-business #1090** — `chore(deps)` consolidate submodule `pnpm.overrides` + pin conxian-ui (Node 24).
- All other repos: 0 open PRs. (Merged this sprint: Rust 1.98.1 bumps enclave-sdk #346 / lib-core #305 / gateway #380 / nexus #279; Node 24 wallet #530 / ui #173 / platform #1265 / labs-site #66; business #1086/#1088/#1089/#1092. Stale dependabot PRs closed: gateway #372, wallet #527/#528, platform #1263, business #1091.)

### Known Issues (flagged, not yet resolved)
- **h2 DoS advisory (RUSTSEC-2026-0258)**: `h2 0.4.15` (transitive via hyper→axum/tonic) has an unbounded-empty-DATA-frames DoS fixed in `0.4.16`. Unblocked (yank resolved) — regenerate gateway/nexus lockfiles to bump `h2` → `0.4.16`.
- **Rust toolchain**: **1.98.1 adopted** (latest stable, 2026-09-03) across all 4 Rust repos — supersedes the 1.97.1 hold. The 1.98 upgrade surfaced two clippy lints, fixed by refactor (no `#[allow]`). Pin exact patch (e.g. `1.98.1`), not the `1.98` minor.
- **Dependabot (conxian-business)**: open alerts (high/moderate/low) across JS packages in the parent monorepo.
- **CI failures (conxian-business, 2026-09-07)**: RESOLVED — Neon branch limit (#1073, pruned 9 stale `preview/*` branches) + Node 20→24 (#1074, `setup-node` v7).
- **Open follow-ups (2026-09-07)**: production KMS release-signing key (#1076); coordinated `bitcoin 0.32.102` + `secp256k1 0.33.1` migration (silent-payments — supersedes closed #527/#528); portfolio mapping drift (#1078 — under verification).

### Resolved (this sprint)
- **secp256k1 yank** → resolved via enclave-sdk v2.0.17 (yanked-crate-free).
- **Module count drift** → canonical count is **43 (25 blockchain + 18 infrastructure)**.
- **pnpm-lock drift (#1072)** → resolved by #1088 lockfile regen.
- **Submodule sync (#1087)** → resolved by #1088.

---

## Architecture

### Dependency Chain
```
conxius-enclave-sdk (v2.0.17)  ← lib-conxian-core (v0.3.3)
                                              ↓
                               conxian-gateway  +  conxian-nexus
```

Dependency pins (from `Cargo.toml`):
- `lib-conxian-core` → `conxius-enclave-sdk` git `tag = "v2.0.17"`.
- `conxian-gateway` → `lib-conxian-core` git `tag = "v0.3.3"`.
- `conxian-nexus` → `lib-conxian-core` git `rev = "b85625f"` (v0.3.3); nexus `sha3 = "0.12"` (dependabot group bump 0.11→0.12).
- Enclave-SDK is published to crates.io and consumed by lib-conxian-core as a git dependency.
- Note: `SDK_OWNERSHIP_POLICY.md` (`.github-private`, 2026-06-13) says consumers should use "pinned Git SHAs" until a stable release cadence — conflicts with tag-based practice (gateway + core use tags). Flagged; policy needs refresh.

### Key Conventions
- **Branch policy**: feature → dev → staged → main. PRs into `main` require a "Mainnet Acceptance Evidence Pack" (see `scripts/branch_promotion_policy.py`). PRs require CI green.
- **Submodule management**: `git submodule update --remote` in conxian-business to sync all repos to main; then regen lockfiles (see below).
- **Version bumps**: Update Cargo.toml, CHANGELOG.md, then `scripts/sync-kb-versions.sh` to propagate to docs.
- **Release process**: Push semver tag → Release Strict workflow (enclave-sdk) or Publish workflow (lib-core).
- **Rust toolchain**: `1.98.1` (latest stable) across all Rust repos (enclave-sdk, gateway, lib-conxian-core, nexus).
- **Node.js**: **24** (approved LTS — do NOT pin Node 20). pnpm `10.28.0` (matches `conxian-unified-ci.yml`).

### Build Commands
```bash
# Per-repo
cargo build --locked
cargo test --locked
cargo clippy -- -D warnings
cargo audit

# Full workspace (conxian-business root)
cargo build --workspace --locked
cargo test --workspace --locked

# JS workspace (conxian-business root, pnpm 10.28 + Node 24)
pnpm install --frozen-lockfile --ignore-scripts
pnpm --filter control-plane build
```

### Submodule-sync + lockfile-regen runbook
```bash
# 1. Sync all submodules to main (market is frozen via update=none)
git submodule update --init --remote

# 2. Regen Rust lockfile for a specific dep bump (e.g. sha3)
cargo update -p <crate>

# 3. Regen pnpm lockfile for JS dep changes
pnpm install --ignore-scripts

# 4. Verify no regression
cargo check --locked --workspace && cargo test --locked --workspace
pnpm install --frozen-lockfile --ignore-scripts && pnpm --filter control-plane build

# 5. Commit gitlinks + lockfiles, then open PR with Mainnet evidence pack
git add <submodules> Cargo.lock pnpm-lock.yaml && git commit
```

### Key Documentation References
- **Release runbooks**: `conxius-enclave-sdk/RELEASING.md`, `lib-conxian-core/docs/RELEASE_PROCESS.md`
- **Architecture**: `docs/architecture/` (ADRs), `conxian-gateway/docs/`
- **Dependency policy**: `conxian-nexus/scripts/check_dependency_declarations.py`
- **Compliance**: `conxian-nexus/scripts/generate_compliance_artifacts.sh`
- **BOS Knowledge Graph**: `BOS_KNOWLEDGE_GRAPH.md`
- **Historical session log**: `docs/archive/AGENTS_archive_session_58.md`

---

## Operational Runbooks

### CI Failure Resolution
| Failure | Fix |
|---------|-----|
| RUSTSEC advisory (transitive) | `--ignore RUSTSEC-XXXX` in CI workflow; file upstream issue |
| `cargo generate-lockfile` fails on yanked version | Audit the committed `Cargo.lock` (drop `generate-lockfile`); no stable `bitcoin 0.33.0` exists yet |
| Submodule pin drift | `git submodule update --init --remote` + regen lockfiles + PR |
| Branch promotion "Mainnet Acceptance Evidence Pack" missing | Add the 6 required `####` headings (Promotion metadata, Mainnet-only production scope, Contamination and residue proof, Successful production validation, Release-readiness sign-off, Owner accountability) |
| pnpm lockfile drift | `pnpm install --ignore-scripts` (Node 24 + pnpm 10.28.0) |
| conxian-business: runner unavailable | Admin → Settings → Actions → Runners: verify GitHub-hosted runners |
| enclave-sdk: Coverage Enforcement | Known false-positive (crates.io rate-limit after publish) |

### Common Operations
```bash
# Check all CI status
for repo in conxius-enclave-sdk lib-conxian-core conxian-gateway conxian-nexus; do
  echo "=== $repo ===" && gh run list -R "Conxian/$repo" -L 3 --json name,status,conclusion
done

# Re-trigger publish workflow
git push origin --delete vX.Y.Z && sleep 5 && git push origin vX.Y.Z

# Sync all submodules to main + regen lockfiles
git submodule update --init --remote && cargo update -p <crate> && pnpm install --ignore-scripts && git add -A && git commit -m "chore: sync submodules"
```
