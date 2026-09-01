# Conxian AGENTS.md

## BOS Operational Standards
> **Version**: 1.6 (2026-09-01 — KB/Code Audit Remediation + AWS Signer)
> **Archive**: `docs/archive/AGENTS_archive_session_58.md` (historical session log)

---

### Session 59 Summary (2026-09-01)
- **KB/Code audit** — SDK module count 50→43 (PR #331 ✅); core MSRV 1.94.0→1.97.1 + count 52→43 (PR #290 ✅). Tooling added to `conxian-business` (PR #1071 ✅): `scripts/audit_doc_module_counts.py`, `scripts/verify_external_state.py`, `scripts/setup_conxian_signer.py`.
- **AWS** — `conxian-sdk-signer` IAM user provisioned (EC2 Nitro + KMS release-signing + self key-rotation); key rotated + verified end-to-end.
- **Git identity** — commits authored as `Botshelo Mokoka <41502979+botshelomokoka@users.noreply.github.com>` (GitHub noreply).
- **Node.js**: **24 is the approved LTS** (do NOT pin Node 20).
- **Open follow-ups**: #1072 (pnpm lockfile drift), #1073 (Neon branch 422), #1074 (Node 20→24), #1075 (org-wide audit — remaining repos), #1076 (prod KMS signing key).

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

> `conxius-orbit` is no longer a submodule (dangling gitlink removed — no `.gitmodules` entry). `conxian-market` remains a submodule with `update = none`.
> Nexus `0.4.23` and wallet `1.9.5` are ahead of their latest tags (unreleased bumps).

### CI Status (2026-08-29)
| Repo | Status | Note |
|------|--------|------|
| lib-conxian-core | 🟢 Green | All CI, audit, hygiene check pass |
| conxian-gateway | 🟢 Green | Secret scan, Node.js CI, cargo audit pass (post #333) |
| conxius-wallet | 🟢 Green | Dependency audit, unit tests, lint, typecheck pass (post #496/#512) |
| conxian-nexus | 🟢 Green | #245 (deps) merged; #250/#252 CI green (Build & Test + audit pass) but blocked on code-owner review (self-approval disallowed) |
| conxius-enclave-sdk | 🟡 Coverage Enforcement | Known false-positive (crates.io rate-limit) |
| conxian-business | 🟡 Partial | Runner now available; `Validate workspace` (pnpm drift #1072), `Create Neon Branch` (#1073), Node 20 deprecation (#1074) fail — non-required |

### Secrets Configured
| Secret | Where | Status |
|--------|-------|--------|
| GITLEAKS_LICENSE | repo → Settings → Actions secrets | ✅ Set (license key present) |
| CI_SUBMODULES_PAT | repo? | Unknown — may be needed for repo-hygiene submodule init |

### Active PRs (2026-08-29)
- **conxian-nexus #245** — Rust deps group bump (7 updates incl. nostr-sdk 0.44→0.45, sha3 0.10→0.11). **MERGED** (squash). nostr-sdk 0.45 API migration (`Client::builder().signer` → explicit `EventBuilder::finalize` + `Client::send_event`; `RelayPoolNotification` → `ClientNotification`; `notifications().recv()` → `StreamExt::next()`).
- **conxian-nexus #250** — idempotency store. **CI green** (Build & Test + audit pass); blocked on code-owner review (`admin-conxian-labs`) — author self-approval disallowed.
- **conxian-nexus #252** — KB/code audit alignment (conxius-enclave-sdk v2.0.16, 52 modules). **CI green** (Build & Test + audit pass); blocked on code-owner review (`admin-conxian-labs`) — author self-approval disallowed.
- **conxian-nexus #253** — align `lib-conxian-core` to `tag = "v0.3.2"` (pull enclave-sdk v2.0.16). `cargo check --locked` passes. (New this session.)
- All other repos: 0 open PRs.

### Known Issues (flagged, not yet resolved)
- **secp256k1 yank**: RESOLVED 2026-09-01 — `conxius-enclave-sdk` v2.0.17 ships yanked-crate-free (`bitcoin 0.32.102` + `secp256k1 0.33.1`, no `0.32.0-beta.2`), re-enabling `full-sdk` downstream (gateway #356, nexus #264).
- **h2 DoS advisory (RUSTSEC-2026-0258)**: `h2 0.4.15` (transitive via hyper→axum/tonic) has an unbounded-empty-DATA-frames DoS fixed in `0.4.16`. Now unblocked (yank resolved) — regenerate lockfiles to bump `h2` to `0.4.16`.
- **Rust 1.98.0 assessment (2026-09-01)**: hold production at **1.97.1** (LTS anchor). 1.98.0 (2026-08-20) adds algebraic floats + `format_into`/`NumBuffer`, irrelevant to our consensus/signing integer math — do not adopt yet. (External report trait-solver/ManuallyDrop-RFC-3336/Release-Strict-CI/CVE-2026-5223 claims unverified/fabricated — CVE-2026-5223 is Medium, third-party-registry-only, fixed in 1.96.0.)
- **Module count drift (enclave-sdk)**: RESOLVED 2026-09-01 — canonical count is **43 (25 blockchain + 18 infrastructure)**; corrected in SDK AGENTS.md (PR #331) and core AGENTS.md (PR #290).
- **Dependabot (conxian-business)**: 12 open alerts (7 high / 3 moderate / 2 low) across JS packages in the parent monorepo.
- **CI failures (conxian-business, 2026-09-01)**: `Validate workspace` — `pnpm-lock.yaml` out of sync with `conxius-wallet` (#1072); `Create Neon Branch` — Neon API 422 (#1073); Node 20 deprecation → migrate to **Node 24** (#1074).
- **Open follow-ups (2026-09-01)**: org-wide audit remaining repos (#1075); production KMS release-signing key (#1076).

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
- `conxian-nexus` → `lib-conxian-core` git `rev = "b85625f"` (v0.3.3). **PR #261 merged** (pins v0.3.3 rev; pulls enclave-sdk v2.0.17).
- Enclave-SDK is published to crates.io and consumed by lib-conxian-core as a git dependency.
- Note: `SDK_OWNERSHIP_POLICY.md` (`.github-private`, 2026-06-13) says consumers should use "pinned Git SHAs" until a stable release cadence is established — this conflicts with the current tag-based practice (gateway + core use tags). Flagged; policy needs a refresh.

### Key Conventions
- **Branch policy**: feature → dev → staged → main. PRs require CI green.
- **Submodule management**: `git submodule update --remote` in conxian-business to sync all repos.
- **Version bumps**: Update Cargo.toml, CHANGELOG.md, then `scripts/sync-kb-versions.sh` to propagate to docs.
- **Release process**: Push semver tag → Release Strict workflow (enclave-sdk) or Publish workflow (lib-core).
- **Rust toolchain**: `1.97.1` across all Rust repos (enclave-sdk, gateway, lib-conxian-core, nexus — normalized 2026-09-01).
- **Node.js**: **24** (approved LTS — do NOT pin Node 20).

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
| `cargo generate-lockfile` fails on yanked version (`secp256k1 0.32.0-beta.2`) | **Workaround (applied)**: audit the committed `Cargo.lock` (drop `generate-lockfile`). **Real fix blocked upstream**: `bitcoin 0.33.0-beta` requires `secp256k1 ^0.32.0-beta.2`, whose entire beta line was yanked (2026-08-28) when `secp256k1 0.33.0` shipped; no stable `bitcoin 0.33.0` exists yet |
| Submodule pin drift | `git submodule update --remote && git add . && git commit` |
| Branch protection | Verify feature→dev→staged→main promotion path |
| PR body missing checklist | Add checklist per `docs/PROMOTION_CHECKLISTS.md` |
| conxian-business: runner unavailable | Admin -> Settings -> Actions -> Runners: verify GitHub-hosted runners enabled for this repo |
| enclave-sdk: Coverage Enforcement | Known false-positive (crates.io rate-limit after publish) |

### Common Operations
```bash
# Check all CI status
for repo in conxius-enclave-sdk lib-conxian-core conxian-gateway conxian-nexus; do
  echo "=== $repo ===" && gh run list -R "Conxian/$repo" -L 3 --json name,status,conclusion
done

# Re-trigger publish workflow
git push origin --delete vX.Y.Z && sleep 5 && git push origin vX.Y.Z

# Sync all submodules
git submodule update --remote && git add . && git commit -m "chore: sync submodules"
```
