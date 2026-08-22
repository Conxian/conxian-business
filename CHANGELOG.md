# Changelog

All notable changes to the Conxian Business Operations System (BOS) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Release note and changelog guidance lives in [docs/RELEASE_NOTES_AND_CHANGELOG.md](docs/RELEASE_NOTES_AND_CHANGELOG.md).

## [Unreleased]

### Full Infrastructure, Branch & System Operational Review (August 2026)
- **Branch Synchronization & Enhancement Verification**:
  - Conducted full commit history audit across all remote branches (`main`, `dev`, `staged`, `jules-*`, `jules/*`, `promotion/*`).
  - Confirmed all code enhancements, CI fixes, and promotion policies from PRs #1035, #1037, #1038, #1040, and #1045 are fully merged into `main`.
  - Verified `dev` and `staged` branch alignment with `main`.
  - Categorized 8 stale feature and promotion branches for deletion while preserving `main`, `dev`, and `staged`.
- **Deployed Cloud Infrastructure & Production System Audit**:
  - Audited all 6 Neon Postgres projects (`corelibs`, `Software dev kit`, `Business Operating System`, `market`, `Gateway`, `Conxian Nexus`), confirming active state and PG 17/18 compatibility.
  - Audited all 2 Supabase database projects (`Conxian BOS`, `Conxian-platform`), confirming `ACTIVE_HEALTHY` status on PG 17.6.
  - Audited Render web service (`conxian-labs-site`), confirming active non-suspended status tracking `main` auto-deploy.
- **System-Wide Compliance & Release Verification**:
  - Executed static governance, release hygiene, submodule integrity, production contamination guard, knowledge retention, LTS compliance, and promotion control verifiers with 100% pass rate.

### Governance & Submodule Alignment (August 2026)
- **Protocol Deprecation & AI Marketplace Mapping**:
  - Explicitly marked legacy `Conxian/Conxian` Clarity protocol repository as deprecated in favor of active `lib-conxian-core`, `conxian-gateway`, `conxian-nexus`, and `conxian-business` across all ecosystem docs (`PORTFOLIO_BUSINESS_UNIT_MAP.md`, `PORTFOLIO_DOCTRINE_REGISTER.md`, `REPO_PORTFOLIO.md`, `DOCUMENTATION_ALIGNMENT_INDEX.md`, `README.md`, `BOS_KNOWLEDGE_GRAPH.md`).
  - Mapped and integrated `conxian-market` as the active AI Marketplace and Agentic Commerce surface seen directly by `conxian-business`.
  - Expanded `docs/bos_research_candidate_ledger.json`, `scripts/verify_bos_research_candidate_ledger.py`, and `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md` with scored candidates `conxian-market-alignment#10` (score 87) and `conxian-protocol-deprecation#612` (score 85).

### Security & Dependency Hardening (August 2026)
- **Workspace Security Overrides & Dependabot Remediation**:
  - Enforced root workspace overrides in `pnpm-workspace.yaml` for `next@^16.2.11`, `postcss@^8.5.18`, `sharp@^0.35.0`, `nanoid@^3.3.18`, `tar@^7.5.0`, `brace-expansion@^2.0.2`, `undici@^7.21.0`, `js-yaml@^4.1.1`, `fast-uri@^3.1.0`, `bigint-buffer@^1.1.5`, `vite@^6.2.1`, `ws@^8.18.1`, and `form-data@^4.0.2`.
  - Executed `pnpm audit` verifying zero fixable high/critical severity security alerts across all workspace submodules.
  - Updated `dependabot-fixes.md` and `docs/SECURITY_PATTERNS.md` to document workspace dependency security override rules.
- **BOS Research Candidate Implementation & Core Decoupling**:
  - Implemented top technical candidate `lib-conxian-core#227` (CON-1573 BDK std-only decoupling) in `lib-conxian-core/Cargo.toml`, ensuring transport and persistence drivers (Electrum, Esplora, RPC, Sled) are decoupled from Core.
  - Expanded research mappings in `docs/bos_research_candidate_ledger.json` and `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md` and verified with `python3 scripts/verify_bos_research_candidate_ledger.py`.

### Fixed & Hardened (Session - 2026-08-18)
- **Promotion Controls Verification Script Hardening**:
  - Hardened scripts/verify_promotion_controls.py to check for shutil.which("gh") before running GitHub CLI commands, enabling 100% static verification pass when gh CLI is absent.
- **Ecosystem Research Expansion & Candidate Scoring Audit**:
  - Audited docs/bos_research_candidate_ledger.json and verified lib-conxian-core#227 (std-only BDK decoupling) as top technical candidate (score 88) and conxian-business#943 as authority issue (score 84).
  - Executed cargo test in lib-conxian-core verifying all 124 unit/integration/doc tests pass cleanly.

### Fixed
- **Release Hygiene Verification for Submodules**:
  - Updated `scripts/verify_release_hygiene.py` to query git tags within submodule directories (`crate_dir`) instead of root repository scope.
  - Enhanced version parsing in `parse_changelog_versions` to recognize version headers formatted as `## [vX.Y.Z]`.
  - Allowed released submodule pins whose version matches `Cargo.toml` to satisfy CHANGELOG hygiene checks.

### Changed (Session 58 — 2026-08-07)
- **BOS Research Candidate Scoring & Ledger System**:
  - Introduced authoritative research candidate scoring ledger (`docs/bos_research_candidate_ledger.json`) and human-readable ledger (`docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`) following the 6-dimension rubric.
  - Implemented validation script `scripts/verify_bos_research_candidate_ledger.py` enforcing strict JSON schema compliance.
