# Conxian AGENTS.md

## BOS Operational Standards
> **Version**: 1.5 (2026-08-29 тАФ Ecosystem Maintenance & KB/Code Audit)
> **Archive**: `docs/archive/AGENTS_archive_session_58.md` (historical session log)

---

## Current State

### Repository Map

| Repo | Crate/Package | Version | Tag | Published |
|------|-------|---------|-----|-----------|
| conxius-enclave-sdk | `conxius-enclave-sdk` | 2.0.16 | v2.0.16 | тЬЕ crates.io |
| lib-conxian-core | `lib-conxian-core` | 0.3.2 | v0.3.2 | тЬЕ crates.io |
| conxian-gateway | `conxian-gateway` | 0.1.5 | v0.1.5 | тАФ |
| conxian-nexus | `conxian-nexus` | 0.4.23 | v0.4.22 | тАФ |
| conxius-platform | `conxius-platform` (npm) | 0.2.5 | v0.2.5 | тАФ |
| conxius-wallet | `conxius-wallet` (npm) | 1.9.5 | v1.9.2 | тАФ |

> `conxius-orbit` is no longer a submodule (dangling gitlink removed тАФ no `.gitmodules` entry). `conxian-market` remains a submodule with `update = none`.
> Nexus `0.4.23` and wallet `1.9.5` are ahead of their latest tags (unreleased bumps).

### CI Status (2026-08-29)
| Repo | Status | Note |
|------|--------|------|
| lib-conxian-core | ЁЯЯв Green | All CI, audit, hygiene check pass |
| conxian-gateway | ЁЯЯв Green | Secret scan, Node.js CI, cargo audit pass (post #333) |
| conxius-wallet | ЁЯЯв Green | Dependency audit, unit tests, lint, typecheck pass (post #496/#512) |
| conxian-nexus | ЁЯЯб Two PRs blocked | #245 Build&Test fail (nostr-sdk migration); #250 audit fail (secp256k1 yanked) |
| conxius-enclave-sdk | ЁЯЯб Coverage Enforcement | Known false-positive (crates.io rate-limit) |
| conxian-business | ЁЯФ┤ No runner available | `runner_name: ""` тАФ all jobs fail in queue; admin intervention needed |

### Secrets Configured
| Secret | Where | Status |
|--------|-------|--------|
| GITLEAKS_LICENSE | repo тЖТ Settings тЖТ Actions secrets | тЬЕ Set (license key present) |
| CI_SUBMODULES_PAT | repo? | Unknown тАФ may be needed for repo-hygiene submodule init |

### Active PRs (2026-08-29)
- **conxian-nexus #245** тАФ Rust deps group bump (7 updates incl. nostr-sdk 0.44тЖТ0.45). **Build & Test fails**: breaking nostr-sdk API migration (`ClientBuilder::signer`, `Client::send_event_builder`, `Stream::recv`, `RelayPoolNotification`).
- **conxian-nexus #250** тАФ idempotency store. **audit fails**: `secp256k1 = "^0.32.0-beta.2"` is yanked (root cause in `conxius-enclave-sdk`); Build & Test passes.
- All other repos: 0 open PRs.

---

## Architecture

### Dependency Chain
```
conxius-enclave-sdk (v2.0.16)  тЖР lib-conxian-core (v0.3.2)
                                              тЖУ
                               conxian-gateway  +  conxian-nexus
```

Dependency pins (from `Cargo.toml`):
- `lib-conxian-core` тЖТ `conxius-enclave-sdk` git `tag = "v2.0.16"`.
- `conxian-gateway` тЖТ `lib-conxian-core` git `tag = "v0.3.2"`.
- `conxian-nexus` тЖТ `lib-conxian-core` git `rev = "6075ef7c"` (not the `v0.3.2` tag; 4 commits pre-release).
- Enclave-SDK is published to crates.io and consumed by lib-conxian-core as a git dependency.

### Key Conventions
- **Branch policy**: feature тЖТ dev тЖТ staged тЖТ main. PRs require CI green.
- **Submodule management**: `git submodule update --remote` in conxian-business to sync all repos.
- **Version bumps**: Update Cargo.toml, CHANGELOG.md, then `scripts/sync-kb-versions.sh` to propagate to docs.
- **Release process**: Push semver tag тЖТ Release Strict workflow (enclave-sdk) or Publish workflow (lib-core).
- **Rust toolchain**: `1.97.1` (enclave-sdk, gateway) / `1.97` (nexus) / `1.94.0` (lib-conxian-core `rust-version`).

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
| `cargo generate-lockfile` fails on yanked version (`secp256k1 0.32.0-beta.2`) | Bump the pinned crate in `conxius-enclave-sdk`, publish, then propagate through `lib-conxian-core` → consumers (blocked nexus #250) |
| Submodule pin drift | `git submodule update --remote && git add . && git commit` |
| Branch protection | Verify featureтЖТdevтЖТstagedтЖТmain promotion path |
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
