# Conxian BOS Knowledge Graph

## 1. Governance Baseline
- **Version**: v1.9.5
- **Status**: Mainnet Ready
- **Authoritative Source**: `conxian-business/README.md`

## 2. Core Entities

### Projects
- **BOS_SYSTEM**: The Conxian Business Operations System (v1.9.5).
- **CONXIAN_PROTOCOL**: Clarity 4.0 smart contracts (Stacks/Bitcoin).
- **CONXIAN_GATEWAY**: High-performance Rust middleware.
- **CONXIAN_NEXUS**: State node for cross-chain truth.

### Libraries
- **LIB_CONXIAN_CORE**: Shared primitives for BitVM2 and CJCS.
- **CONXIUS_ENCLAVE_SDK**: TEE/StrongBox abstraction layer.

## 3. Decisions & Mandates
- **ZSE_MANDATE**: Zero Secret Egress enforced across all documentation.
- **SOVEREIGN_FIRST**: Dynamic principal resolution via `operational-treasury.clar`.
- **UNIFIED_THEORY_v2**: Execution velocity and autonomy optimization framework.

## 4. Relationship Map
- `CORE_LIB` **verified_by** `BITVM2_STATE`
- `GATEWAY` **uses** `CORE_LIB`
- `NEXUS` **anchors** `STATE_ROOTS`
- `WALLET` **requires** `ENCLAVE_SDK`

## 5. Recent Crystallization (v1.9.5 - June 2026)
- **CI_VALIDATION_RESTORED**: Restored 9 missing scripts in `scripts/` to enforce unified CI policy.
- **TESTNET_PRINCIPAL_REMEDIATION**: Replaced all hardcoded `ST...` addresses in production track with `SP...` (Sovereign Treasury).
- **CODEOWNERS_STANDARDIZATION**: Unified ownership across the BOS repository.

---
*Crystallized by Jules (June 2026).*
