# Autonomous Repository & Architecture Discovery Report

## 1. System Architecture & Dependency Map

### Core Components
* **Root Monorepo & Business Orchestrator (`conxian-business`)**:
  - Serves as the canonical governance, business logic, and B2B orchestration root for the Conxian Sovereign Autonomous Business (SAB) ecosystem.
  - Contains Python runtime controllers (`admin_runtime_server.py`, `transparency_custodian.py`), verification suites, and business specifications (`docs/BOS_BUSINESS_BUILDOUT.md`, `conxian-business/BOS_PLATFORM_SPEC.md`, `conxian-business/BOS_MULTI_TENANT_ORCHESTRATION.md`).
* **Core Cryptographic & Protocol Primitives (`lib-conxian-core`)**:
  - **Status:** Fully built & active crate (`v0.3.3`, pinned commit `f3f248ed9a552d9206268f679453b845d8986291`).
  - Implements Bitcoin BitVM2 settlement bridges (364 verification segments), FROST threshold signing, Lightning/L2 adapters, and ISO 20022 message parsers.
  - Root `Cargo.toml` intentionally excludes `lib-conxian-core` from top-level workspace members to avoid nested workspace conflict errors in Cargo resolver v2 during Unified CI runs.
* **B2B Gateway Execution Engine (`conxian-gateway`)**:
  - **Status:** Fully built & active crate (`v0.1.5`, pinned commit `f402b050c75b8a23a78b961ac966112067b8a8be`).
  - Contains `cmd/gateway`, `cmd/conxian-cli` (`cxn`), `internal/engine`, `internal/api`, `internal/compliance`, and `pkg/conxian-core`.
  - Exposes REST/gRPC settlement endpoints, x402 attestation handling, and developer sandbox utilities (`CONXIAN_API_TOKEN` entropy generation).
* **Universal Settlement Hub & Relayer (`conxian-nexus`)**:
  - **Status:** Fully built & active crate (`v0.4.23`, pinned commit `e6259fd8b32e0cf0299c5d34212c60d7b4860689`). Listed as a workspace member in root `Cargo.toml`.
  - Implements `x402` HTTP/v2 payment attestation protocol (`conxian-nexus/src/verification/x402.rs`), Tier-1 chain family parsing (Bitcoin, EVM, Solana, Stacks, Cosmos), and SQLx PostgreSQL persistence.
* **Hardware & TEE Enclave Security SDK (`conxius-enclave-sdk`)**:
  - **Status:** Fully built & active crate (`v2.0.17`, pinned commit `b3d79d9c5aca0b9adee53bce0d0c0c11ff81ff43`). Listed as a workspace member in root `Cargo.toml`.
  - Provides hardware-backed root of trust, WebAuthn/FIDO2 verifiers (`webauthn-rs`), PKCS#11 HSM integration (`cryptoki`), ZF FROST (`frost-secp256k1-tr` v3.0.0), and Groth16/BLS12-381 pairing checks (`bls12_381`). Software simulators (`development-simulators`, `mock-cloud-enclave`) are strictly gated and opt-in only.
* **B2C Sovereign Wallet & Interfaces (`conxius-wallet`)**:
  - **Status:** Active Vite/TypeScript UI application (pinned commit `e51ab324f251a02fe6e6bfdebf493a222bd709c4`).
* **AI Marketplace & Agentic Commerce (`conxian_market`)**:
  - **Status:** Active Node.js/TypeScript submodule (pinned commit `9965b850b3a225be56107b867d721a0f4ad3697b`) mapped under `pnpm-workspace.yaml`.
* **Public Protocol & Commercial Surface (`conxian-labs-site`, `showcase-dapp`)**:
  - **Status:** Active static site / application surfaces auto-deploying via Render and Cloud Run.
* **Zero Strategic Exposure (ZSE) Pointer Stubs**:
  - Top-level directories `Fiscal-Vault-Oracle/`, `Nakamoto-Guardian/`, `Sovereign-Ops-Orchestrator/`, `Sovereign-Strategy-Nexus/`, and `cxn-grid-oracle/` contain public-safe pointer stubs (`.md` / `.json` pointers) to prevent leakage of internal IP while ensuring documentation links continue to resolve.

### Dependency Topology
* **Rust Base Layer:**
  - `rustc 1.98.1` edition 2021 across `conxian-gateway`, `conxian-nexus`, `conxius-enclave-sdk`, and `lib-conxian-core`.
  - Core Crates: `bitcoin = "0.32"`, `secp256k1 = "0.29"`, `tokio = "1.52"`, `axum = "0.8"`, `sqlx = "0.9"`.
  - Cryptographic Primitives: `k256 = "0.14"`, `bls12_381 = "0.8"`, `frost-secp256k1-tr = "3.0.0"`, `musig2 = "0.4"`, `ed25519-dalek = "3.0"`, `alloy = "2.1"`.
* **Node / TypeScript Layer:**
  - Root `pnpm-workspace.yaml` manages `conxius-wallet`, `conxius-platform`, `conxian_market`, `packages/client-sdk`, `packages/schemas`, `apps/control-plane`, and `cxn-sandbox`.
  - React type dependencies pinned to `@types/react = "^19.2.18"` in root `package.json`.

### Active Configurations
* **CI/CD Workflows (`.github/workflows/`)**:
  - `.github/workflows/conxian-unified-ci.yml`: Unified multi-suite orchestration across B2B suite and core libraries.
  - `.github/workflows/branch-promotion-policy.yml`: Enforces mainnet evidence packs (`#### Promotion metadata`, etc.) for PRs targeting `main` and feature promotion checklists.
  - `.github/workflows/neon_workflow.yml`: Resilient Neon PostgreSQL preview branch provisioning (bypasses gracefully with warnings if `NEON_PROJECT_ID` or `NEON_API_KEY` are unconfigured).
  - `.github/workflows/secret-scan.yml` & `.github/workflows/action-version-audit.yml`: Automated secret scanning and GitHub Action SHA pinning audits.
* **Container & Docker Tooling**:
  - Root `docker-compose.yml`, `docker-compose.env.example`, `docker-compose.env.mainnet.example`, and `docker-compose.env.testnet.example`.
  - Dockerfiles present in `conxian-gateway/Dockerfile` and `conxian-nexus/Dockerfile`.
* **Model Context Protocol (MCP) Tools**:
  - `openspec/config.yaml` and `Fiscal-Vault-Oracle/TREASURY_MCP_CONFIG.json` for agentic MCP intent execution.

---

## 2. Knowledge Base & Context Audit

### Existing Documentation Manifest
* **Root Documents:** `README.md`, `CHANGELOG.md`, `SECURITY.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `LICENSE`, `SUMMARY.md`, `AGENTS.md`, `BOS_KNOWLEDGE_GRAPH.md`, `spec.md`, `DEVELOPER_QUICKSTART.md`, `RELEASING.md`, `DEPENDENCY_BASELINE.md`.
* **Canonical Architecture & Specs (`docs/`)**:
  - `docs/CONXIAN_MASTER_RECONNAISSANCE_AND_ARCHITECTURE_REVIEW.md`: Organization-wide 5-phase review across 12 core repositories.
  - `docs/CLIENT_ONBOARDING_AND_UNIFIED_INSTALLER_SPEC.md`: Unified `conxian-cli` (`cxn`) installer specification (TTFV < 15m) and commercial packaging tiers.
  - `docs/SLA.md` & `docs/SLA_POLICY.md`: B2B Gateway enterprise SLA (99.5% uptime, SEV1 response, zero financial credits in v1).
  - `docs/COMMERCIAL_PACKAGING_DOCTRINE.md`: BaaP 3-layer monetization model.
  - `docs/GAPS.md`, `docs/PORTFOLIO.md`, `docs/ALIGNMENT.md`: Source-of-truth gap matrix, capability matrix, and cross-repo alignment audit.

### Context Alignment (The Reality Check)
* **Version Baseline:** System-wide version alignment to `v1.9.5` across Root `README.md`, `CHANGELOG.md`, and `AGENTS.md` accurately reflects crate tags and submodule release pins.
* **Bitcoin-Native Base Layer:** Stated protocol posture (Bitcoin as base layer and settlement utility asset without a native ecosystem token) is 100% verified across `lib-conxian-core` and `conxian-gateway` codebase logic.
* **Submodule Release Pin Hygiene:** All 8 active submodules in `.gitmodules` are configured with `update=checkout` and match local workspace commit SHAs, passing `python3 scripts/verify_submodule_integrity.py` and `python3 scripts/verify_release_hygiene.py`.

### Outdated / Missing Guidance
* **GitHub CLI Dependency in Utility Scripts:** `scripts/bos_org_review.py` attempts to execute `gh` directly without checking if the binary exists, causing a `FileNotFoundError: 'gh'` crash in environments lacking `gh`, whereas `scripts/verify_promotion_controls.py` was hardened using `shutil.which('gh')`.
* **ZSE Pointer Stub Clarity:** Developer onboarding docs (`DEVELOPER_QUICKSTART.md`) should explicitly note that directories such as `Fiscal-Vault-Oracle/` and `Nakamoto-Guardian/` are public-safe ZSE pointer stubs rather than active Rust/Node modules.
* **Workspace Directory Exclusion:** `conxian-ui` and `conxius-orbit` are referenced in `docs/PORTFOLIO_REPOSITORY_INVENTORY.md` but are intentionally handled as external repositories outside the current root submodule tree, as flagged by `scripts/verify_contamination_guard.py`.

---

## 3. Security & Repository Hygiene

### Boundary Risks
* **Hardcoded Credentials & Secrets:** Zero exposed hardcoded private keys, JWT secrets, or production API tokens were discovered. `.gitleaks.toml` rules and `.gitignore` patterns actively protect secret files (`.env`, `.env.*`, `*.pem`, `*.key`).
* **Hardware Security vs. Simulators:** `conxius-enclave-sdk` enforces strict feature gating (`development-simulators` and `mock-cloud-enclave` are default-disabled), preventing mock cloud enclave code from leaking into production builds.
* **Public vs. Corporate Surface Separation:** Enforces domain firewall standards separating public protocol developer documentation (`conxian.org`) from corporate B2B operations (`conxian-labs.com`).

### Governance Gaps
* **Governance Baseline:** Full compliance with open-source governance standards (`SECURITY.md`, `.github/CODEOWNERS`, `CONTRIBUTING.md`, `LICENSE`, `GOVERNANCE.md`).
* **Codeowner Routing:** `.github/CODEOWNERS` explicitly routes pull requests for `.github/`, `scripts/`, `lib-conxian-core/`, `conxian-gateway/`, `conxius-wallet/`, `docs/`, `SECURITY.md`, and `GOVERNANCE.md` to designated maintainers.

### Git Hygiene
* **Tracked Artifacts & Clean Working Tree:** `git status --ignored` confirms no untracked or accidentally committed build artifacts (`dist/`, `target/`, `node_modules/`, `.env`).
* **Submodule Integrity:** `python3 scripts/verify_submodule_integrity.py` and `python3 scripts/verify_release_hygiene.py` pass cleanly with zero warnings or uncommitted submodule drift.

---

## 4. Prioritized Recommendations

### [HIGH] Hardening `scripts/bos_org_review.py` against missing `gh` CLI
* **Description:** Update `scripts/bos_org_review.py` to check for the presence of the `gh` binary using `shutil.which('gh')` before execution, matching the resilient pattern implemented in `scripts/verify_promotion_controls.py`.
* **File Path:** `scripts/bos_org_review.py`
* **Suggested Code Adjustment:**
```python
import shutil

def main():
    if not shutil.which("gh"):
        print("INFO: 'gh' CLI binary not found in PATH. Skipping GitHub org review.")
        return 0
```

### [MAINTENANCE] Clarify ZSE Pointer Stub Scope in Developer Quickstart
* **Description:** Add an explicit notice in `DEVELOPER_QUICKSTART.md` clarifying that directories `Fiscal-Vault-Oracle/`, `Nakamoto-Guardian/`, `Sovereign-Ops-Orchestrator/`, `Sovereign-Strategy-Nexus/`, and `cxn-grid-oracle/` contain Zero Strategic Exposure (ZSE) public-safe pointer stubs and documentation links rather than runnable application code.
* **File Path:** `DEVELOPER_QUICKSTART.md`

### [MAINTENANCE] Periodic Verification Execution
* **Description:** Regularly execute the full repository validation suite during developer workflows to ensure continued zero-drift compliance.
* **Suggested Command:**
```bash
python3 scripts/bos_repo_check.py && PYTHONPATH=. python3 -m unittest discover -s scripts/tests
```
