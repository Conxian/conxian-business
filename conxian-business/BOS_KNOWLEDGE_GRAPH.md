# Conxian BOS Knowledge Graph

## 1. Governance & Standards
- **Sovereign-First Mandate**: All systems must be BTC-native, strictly sovereign-first (TEE/StrongBox), and yield-only financial.
- **Zero Secret Egress (ZSE)**: No secrets in Git. Enforcement via `scripts/verify_contamination_guard.py`.
- **Clarity 4 Compliance**: Mandatory for all smart contracts.

## 2. Branding & Architecture
- **Conxian**: B2B, Enterprise, Protocol Layer (Gateway, Nexus, Protocol).
- **Conxius**: Client, Access Layer (Wallet, Platform, Orbit).

## 3. Technical Primitives
- **BitVM2**: SNARK verification on Bitcoin.
- **CJCS v2.0**: Conxian Job Card Schema for B2B intents.
- **ZKC**: Zero-Knowledge Compliance.
- **SYI**: Sovereign Yield Index.

## 4. Operational Metrics
- **Vx**: Execution Velocity (AI leverage).
- **As**: System Autonomy (Minimize manual oversight).
- **Oc**: Founder's Tax (Manual oversight cost).

## 5. Decision Log
- **[2026-07-03]**: Transitioned to mandatory branch promotion rules (Feature -> dev -> staged -> main).
- **[2026-07-05]**: Standardized Render deployment port binding for `conxian-ui`.
- **[2026-07-08]**: Aligned system-wide version to BOS v1.9.5.

## 6. Crystallized Entities (v1.9.5 - July 2026)

| ID | Type | Name/Title | Status | Relationship |
| :--- | :--- | :--- | :--- | :--- |
| `BOS_SYSTEM` | Project | Conxian BOS v1.9.5 | Stable | **anchors** all modules |
| `NEXUS` | Library | conxian-nexus (v0.5.1) | Production | **uses** `KwilAdapter` |
| `GATEWAY` | Library | conxian-gateway (v0.1.1) | Production | **uses** `StacksRpcAggregator` |
| `CONCLAVE_SDK` | Library | lib-conclave-sdk (v1.9.5) | Stable | **dependency_of** `WALLET` |
| `CORE_LIB` | Library | lib-conxian-core (v1.9.5) | Stable | **dependency_of** `GATEWAY` |
| `JUR_SHARDING` | Decision | Jurisdictional Sharding | Implemented | **isolated_by** `BNS` |
| `ZSE_MANDATE` | Decision | Zero Secret Egress | Enforced | **fixed** `PUBLIC_EXPOSURE_RISK` |
| `BITVM2_STATE` | Concept | BitVM2 State Proofs | Active | **verified_by** `CORE_LIB` |
| `CXN_SANDBOX` | Tooling | Developer Sandbox | Enhanced | **enables** < 15m TTFV |
| `REACT_PIN` | Decision | React Type Pinning | Enforced | **fixes** UI build registry errors |
| `VULN_FIX` | Security | RUSTSEC-2026-0204 | Fixed | **upgrades** `crossbeam-epoch` |

---
*Crystallized by Jules at End-of-Sprint Review (July 2026).*
