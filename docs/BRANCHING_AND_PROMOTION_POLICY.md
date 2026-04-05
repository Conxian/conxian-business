# Branching and Promotion Policy (CON-381, CON-389)

To ensure the integrity of the Conxian Production Environment, all repositories in the portfolio must adhere to the following branch model and promotion gates.

## 1. Branch Taxonomy

| Branch | Network / Scope | Rules |
| --- | --- | --- |
| `main` | **Mainnet-Only** | Only production-ready, mainnet-validated code. No stubs, mocks, or placeholders. |
| `staged` | Mainnet Candidate | Pre-production validation branch for mainnet releases. The only branch allowed to merge into `main`. |
| `dev` | **Testnet-Only** | Default development branch. Non-production validation and testnet-oriented logic. |
| `feat/*`, `fix/*` | Local/Asynchronous | Ephemeral branches for individual work. Must merge into `dev`. |

## 2. Required Promotion Path

1. **Development & Unit Testing**: All work starts on feature branches and is merged into `dev` after passing standard CI checks and unit tests.
2. **Testnet Validation**: Functional validation is performed on the `dev` branch against testnet (Stacks Testnet, Bitcoin Testnet/Signet).
3. **Staging (Promotion Candidate)**: Once testnet validation is complete, code is promoted from `dev` to `staged`.
4. **Mainnet Acceptance Evidence**: Promotion from `staged` to `main` requires a strict "Mainnet Acceptance Evidence Pack" proving:
   - No non-production logic (stubs/mocks) in production paths.
   - Successful validation in a mainnet-identical environment.
   - Owner/Maintainer sign-off on release readiness.
5. **Production Merge**: Only after the evidence pack is verified can `staged` be merged into `main`. **Direct merges from `dev` to `main` are strictly prohibited.**

## 3. Enforcement (CI/CD Gates)

- **Main Branch Protection**: `main` must be protected with required reviews and passing status checks.
- **Contamination Guard**: CI suites on `main` and `staged` must run a blocking scan for and reject non-production patterns, and the scan must be explicitly scoped to avoid false positives.
  - **Scope**: Scan only production source trees (repo-defined allowlist; e.g., `contracts/**`, `src/**`).
  - **Exclusions**: Explicitly exclude `docs/**`, `audit/**`, `**/*.md`, and test/mocks/fixtures paths.
  - **Patterns**: Prefer precise patterns (word boundaries) over broad substrings (avoid generic terms like "placeholder" unless heavily scoped).
  - **Example**:
    ```bash
    if rg -n \
      --glob 'contracts/**' \
      --glob 'src/**' \
      --glob '!**/test/**' \
      --glob '!**/tests/**' \
      --glob '!**/__tests__/**' \
      --glob '!**/fixtures/**' \
      --glob '!**/mocks/**' \
      '\bMOCK_[A-Z0-9_]+\b|\bstub-func\b'; then
      echo 'ERROR: non-production patterns detected in production paths'
      exit 1
    fi
    ```
- **Submodule Integrity**: Parent repositories (like `conxian-business`) must ensure all submodules are pinned to their respective production-ready commits before merging to `main`.

---
**Verified by:** Jules (cxn-arch-guardian)
**Date:** April 5, 2026
