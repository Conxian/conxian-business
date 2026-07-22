# Conxian BOS Knowledge Graph (v1.9.5)

## 1. Decision Log
- **[2026-07-08]**: Aligned system-wide version to BOS v1.9.5. Remediated crossbeam-epoch vulnerability.

## 2. Entities
| ID | Type | Name/Title | Status | Relationship |
| :--- | :--- | :--- | :--- | :--- |
| `BOS_v1.9.5` | Version | BOS v1.9.5 | Deployed | — |
| `VULN_FIX` | Security | RUSTSEC-2026-0204 | Fixed | — |
| `BOS_SYSTEM` | Project | Conxian BOS v1.9.3 | Stable | **anchors** all modules |
| `NEXUS` | Library | conxian-nexus (v0.5.1) | Production | **uses** `KwilAdapter` |
| `GATEWAY` | Library | conxian-gateway (v0.1.1) | Production | **uses** `StacksRpcAggregator` |
| `CONCLAVE_SDK` | Library | lib-conclave-sdk (v1.9.3) | Stable | **dependency_of** `WALLET` |
| `CORE_LIB` | Library | lib-conxian-core (v1.9.3) | Stable | **dependency_of** `GATEWAY` |
| `JUR_SHARDING` | Decision | Jurisdictional Sharding | Implemented | **isolated_by** `BNS` |
| `ZSE_MANDATE` | Decision | Zero Secret Egress | Enforced | **fixed** `PUBLIC_EXPOSURE_RISK` |
| `BITVM2_STATE` | Concept | BitVM2 State Proofs | Active | **verified_by** `CORE_LIB` |

> **Supersession note — 2026-07-20:** The `CONCLAVE_SDK` row above is retained as an April 2026 historical entity record. It is superseded for current SDK maturity: the active entity is `conxius-enclave-sdk`, currently **Beta / conditional**. The immutable [Production Enablement Audit](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md) and [Capability and Evidence Matrix](https://github.com/Conxian/conxius-enclave-sdk/blob/79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8/docs/architecture/CAPABILITY_MATRIX.md) are the current authority; no value-bearing production signing or settlement is supported from the audited tree.

## 7. Current SDK entity status (2026-07-20)

| ID | Type | Name/Title | Status | Relationship |
| :--- | :--- | :--- | :--- | :--- |
| `CONXIUS_ENCLAVE_SDK` | Library | `conxius-enclave-sdk` | Beta / conditional | **dependency_of** `WALLET`; current authority is the July 20 audit at merge commit `79a4a082ab2c05e5b1b30335ab56b9e6d068c7e8` against audited baseline `8194aa8ade26a9d5d7ed54b7f80f36796fce585c` |

---
*Crystallized by Jules at End-of-Sprint Review (April 2026).*
