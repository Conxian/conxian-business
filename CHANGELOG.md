# Changelog

All notable changes to the Conxian Sovereign Business Operations System (BOS) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.1] - 2026-03-20

### Changed
- Refactored repository structure to improve hygiene and governance.
- Consolidated temporary scripts, logs, reports, and patches into structured `archive/` subdirectories.
- Updated root-level `.gitignore` to prevent tracking of artifacts, logs, and temporary files.

### Added
- Root-level `LICENSE` (GPL-3.0) for unified governance.
- `CHANGELOG.md` to track significant system updates.
- Centralized `scripts/check_links.py` for markdown link verification.

### Fixed
- Remediated root directory clutter from historical audit and repair sessions.

## [1.7.0] - 2026-03-15

### Added
- Initial release of the Sovereign Business Operations System (BOS).
- Deployment of Agentic EXCO Suite for Bitcoin-native orchestration.
- Integration of Fiscal Vault Oracle for Bitcoin treasury management.
- Implementation of Nakamoto Guardian for immutable IP registry.
