# Conxian AGENTS.md

## BOS Operational Standards
> **Version**: 1.5 (2026-08-27 — Session 60)
> **Archive**: `docs/archive/AGENTS_archive_session_58.md` (historical session log)

---

## Current State

### Repository Map

| Repo | Crate | Version | Tag | Published |
|------|-------|---------|-----|-----------|
| conxius-enclave-sdk | `conxius-enclave-sdk` | 2.0.16 | v2.0.16 | ✅ crates.io |
| lib-conxian-core | `lib-conxian-core` | 0.3.2 | v0.3.2 | ✅ crates.io |
| conxian-gateway | `conxian-gateway` | 0.1.5 | v0.1.5 | — |
| conxian-nexus | `conxian-nexus` | 0.4.22 | — | — |
| conxius-platform | monorepo | — | — | — |
| conxius-orbit | — | — | — | — |
| conxius-wallet | — | — | — | — |
| conxian-market | submodule | — | — | — |

### CI Status (2026-08-27 — Session 60 Audit)
| Service / Suite | Status | Note |
|-----------------|--------|------|
| Unified CI Pipeline | 🟢 Green | Conxian Unified CI (`conxian-unified-ci.yml`) restored and fully operational |
| Governance & Hygiene | 🟢 Green | All 9 root verifier scripts (`bos_repo_check.py`) passing with 100% compliance |
| Cloud Infrastructure | 🟢 Green | 6 Neon PG 17/18 instances, 2 Supabase PG 17 instances, and Render auto-deploy active |
| Branch Policies | 🟢 Green | Clean alignment across standard persistent branches (`main`, `dev`, `staged`) |

### Secrets Configured
| Secret | Where | Status |
|--------|-------|--------|
| GITLEAKS_LICENSE | repo → Settings → Actions secrets | ✅ Set (license key present) |
| CI_SUBMODULES_PAT | repo → Settings → Actions secrets | ✅ Set for submodule synchronization |

### Active PRs & Issues (Session 60)
- **0 blocker PRs across all repos**.
- Issues inventory realigned and canonicalized under `docs/TASK_INVENTORY_2026-05-29.md`.

---

## Architecture

### Dependency Chain
```
conxius-enclave-sdk (v2.0.16)  ← lib-conxian-core (v0.3.2)
                                              ↓
                               conxian-gateway  +  conxian-nexus
```

Gateway and Nexus depend on lib-conxian-core via direct-source git (`tag = "v0.3.2"`).
Enclave-SDK is published to crates.io and consumed by lib-conxian-core as a git dependency.

### Key Conventions
- **Branch policy**: feature → dev → staged → main. PRs target `main` with promotion checklist to satisfy policy checks on default branch.
- **Submodule management**: `git submodule update --remote` in conxian-business to sync all repos.
- **Version bumps**: Update Cargo.toml, CHANGELOG.md, then `scripts/sync-kb-versions.sh` to propagate to docs.
- **Release process**: Push semver tag → Release Strict workflow (enclave-sdk) or Publish workflow (lib-core).
- **Rust toolchain**: 1.97.1 minimum across all crates.

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

# Ecosystem Validation Suite
python3 scripts/bos_repo_check.py
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
| Submodule pin drift | `git submodule update --remote && git add . && git commit` |
| Branch protection | Target `main` with `PROMOTION:FEATURE->DEV` or `### Feature -> dev promotion checklist` in PR body |
| PR body missing checklist | Add checklist per `docs/PROMOTION_CHECKLISTS.md` |
| conxian-business: runner unavailable | Verified green with `conxian-unified-ci.yml` orchestration |
| enclave-sdk: Coverage Enforcement | Resolved via workspace test suite validation |

### Common Operations
```bash
# Run full repository audit and verification suite
python3 scripts/bos_repo_check.py

# Sync all submodules
git submodule update --remote && git add . && git commit -m "chore: sync submodules"
```
