# Changelog

All notable changes to the Conxian Business Operations System (BOS) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Release note and changelog guidance lives in [docs/RELEASE_NOTES_AND_CHANGELOG.md](docs/RELEASE_NOTES_AND_CHANGELOG.md).

## [Unreleased]

### Clarified (2026-10-15 — corporate identity and alert research)
- Added [corporate identity and alert routing research](docs/research/ZOHO_MAIL_IDENTITY_AND_ALERT_ROUTING_FIREWALL_RESEARCH.md) separating proposed controls from verified implementation, including application-specific offboarding and session/token revocation evidence.
- Retained current development knowledge and the existing promotion policy and negative tests. This documentation change does not configure an identity provider, mail alias, runtime credential, or signing provider.

### Added & Synthesized (2026-10-24 — System-Wide Evaluation & Agentic Transformation Blueprint)
- **Agentic Transformation Blueprint (`docs/research/AGENTIC_SYSTEM_WIDE_EVALUATION_AND_TRANSFORMATION_BLUEPRINT_2026.md`)**: Authored canonical specification detailing Conxian's architectural elevation from deterministic rails into an Agentic, AI-First Autonomous Business Stack across all 6 core pillars.
- **CXIP Proposal Taxonomy**: Established unified improvement proposal taxonomy across workspace repositories: CXBIP (`conxian-business`), CXPIP (`conxius-platform`), CXMIP (`conxian_market`), CXWIP (`conxius-wallet`), CXCIP (`lib-conxian-core`), CXGIP (`conxian-gateway`), CXNIP (`conxian-nexus`).
- **Release Hygiene Alignment**: Synchronized `conxius-enclave-sdk/CHANGELOG.md` version heading `[2.1.0]` with `Cargo.toml` v2.1.0, restoring 100% PASS status across all release hygiene audits.
- **Knowledge Base & Candidate Ledger Upgrade**: Upgraded `docs/BOS_KNOWLEDGE_FRAMEWORK.md` to Version 4.1 (Session 71), expanded candidate ledger `docs/bos_research_candidate_ledger.json` (`agentic-system-wide-evaluation-blueprint-gap`), updated `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`, `BOS_KNOWLEDGE_GRAPH.md`, and indexed in `SUMMARY.md`.

### Added & Synthesized (2026-10-12 — Org-Wide Strategic Boundary & Research Expansion)
- **Dependency Purge & Boundary Audit (`docs/research/DEPENDENCY_PURGE_AND_BOUNDARY_AUDIT_2026.md`)**: Conducted an exhaustive org-wide codebase audit confirming zero custom tokenomics or speculative token dependencies across `conxian-nexus`, `conxian-gateway`, `conxius-enclave-sdk`, and `conxius-platform`. Enforced Bitcoin L1 anchoring.
- **Target A — `conxian-nexus` (ZK Proving Expansion)**: Added `src/verification/zkvm.rs` supporting SP1 and RISC Zero 2026 zkVM proof environment adapters for Bitcoin L1 state verification, re-exported in `src/verification/mod.rs`, created `conxian-nexus/ARCHITECTURE.md`, and updated `README.md`.
- **Target B — `conxian-gateway` (ISO 20022 Enterprise Gateway)**: Created ISO 20022 translation engine (`internal/compliance/src/iso20022.rs` converting `pacs.008`, `pacs.002`, `camt.053` to CJCS v2.0 tokenless routing events), added commercial API key authentication middleware (`internal/api/src/middleware.rs`), created `conxian-gateway/ARCHITECTURE.md`, and updated `README.md`.
- **Target C — `conxius-enclave-sdk` (Hardware Security & StrongBox TEE)**: Created Android StrongBox Keymaster/KeyMint TEE driver (`src/enclave/strongbox_tee.rs`) for hardware-isolated signing, re-exported in `src/enclave/mod.rs`, created `conxius-enclave-sdk/ARCHITECTURE.md`, updated `README.md`, and aligned release hygiene version to `[2.1.0]` in `CHANGELOG.md`.
- **Target D — `conxius-platform` (Enterprise SLA Orchestration)**: Created multi-tenant SLA node deployment schema (`platform/sla_node_orchestrator.json`), TypeScript orchestrator client (`services/admin-dashboard/src/lib/sla_orchestration.ts`), `conxius-platform/ARCHITECTURE.md`, and updated `README.md`.
- **Knowledge Framework Upgrade**: Upgraded `docs/BOS_KNOWLEDGE_FRAMEWORK.md` to Version 4.0 (Session 70), updated `BOS_KNOWLEDGE_GRAPH.md` and candidate scoring ledger (`docs/bos_research_candidate_ledger.json`).

### Added & Synthesized (2026-10-12 — UX Surface Mapping & Domain Alignment)
- **UX Asset Mapping & Verification (`no ui repo`)**: Formulated canonical research report `docs/research/UX_SURFACE_AND_DOMAIN_ALIGNMENT_RESEARCH_2026.md` capturing the full empirical UX inventory (`conxian-labs-site`, `conxius-wallet`, `apps/control-plane`, `showcase-dapp`, `conxius-platform/services/admin-dashboard`) and confirming that no active `conxian-ui` repository exists following its explicit deletion and deprecation.
- **Domain Separation Firewall**: Reinforced strict boundary rules separating Developer Protocol Surface (`conxian.org`: `nexus`, `gateway`, `sdk`, `platform`, `market`, `wallet`) from Corporate Governance Surface (`conxian-labs.com`: `www`, `bos`, `api`, `status`).
- **Ecosystem Governance & Knowledge Base Upgrade**: Updated portfolio docs (`PORTFOLIO_REPOSITORY_INVENTORY.md`), candidate ledger (`docs/bos_research_candidate_ledger.json`), upgraded `docs/BOS_KNOWLEDGE_FRAMEWORK.md` to Version 3.8, and updated `BOS_KNOWLEDGE_GRAPH.md`.

### Added & Synthesized (2026-10-11 — Phased Research & Org-Wide Business Operations System Expansion)
