# Conxian AGENTS.md

## BOS Operational Standards
> **Version**: 1.3 (2026-08-07 — Session 58)
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

### CI Status
All repos green on main. Known non-blocking issues:
- **enclave-sdk Release Strict**: Publish verify step false-positive (crates.io rate-limit); crate is live.
- **Secret Scan (gitleaks)**: Blocked by org-level ruleset — admin intervention needed.

### Active PRs
- **conxian-nexus #221**: `fix/dependency-policy-v0.3.2` — dependency policy v0.3.2 alignment, all CI green.
- **conxian-nexus #222**: `docs/version-fix` — README version badge fix.

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
- **Branch policy**: feature → dev → staged → main. PRs require CI green.
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
| Branch protection | Verify feature→dev→staged→main promotion path |
| PR body missing checklist | Add checklist per `docs/PROMOTION_CHECKLISTS.md` |

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
