# Conxian Cross-Repo Alignment Audit Report

| Metadata | Value |
|---|---|
| Classification | Public-safe alignment audit |
| Audit Date | 2026-10-03 |
| Target Release | Conxian BOS v1.9.5 |
| Authority | [Business Issue #943](https://github.com/Conxian/conxian-business/issues/943) |

---

## Executive Summary

An ecosystem-wide alignment audit was executed across all 8 submodules and root governance repositories. All active submodules were validated against the Three Pillars (Vertical Sovereignty, Operational Unification, Nakamoto Readiness) and verified using deterministic scripts (`python3 scripts/bos_repo_check.py`, `python3 scripts/verify_submodule_integrity.py`).

---

## Repository Alignment Status

| Repository | Pinned SHA | Update Policy | Pillar Alignment | Audit Status | Notes |
|---|---|---|---|---|---|
| `conxian-gateway` | `e33f6e5d` | `checkout` | Operational Unification | **PASS** | Settlement bridge & ISO 20022 message routing aligned |
| `conxian-nexus` | `907d729d` | `checkout` | Operational Unification | **PASS** | Universal chain sync & MMR state proofs aligned |
| `conxius-wallet` | `19e7394e` | `checkout` | Vertical Sovereignty | **PASS** | Non-custodial mobile wallet reference client aligned |
| `conxian_market` | `bcfecbf9` | `checkout` | Vertical Sovereignty | **PASS** | M2M marketplace & DLC escrow surface activated |
| `lib-conxian-core` | `e1d8d2c8` | `checkout` | Nakamoto Readiness | **PASS** | Bitcoin L1 & Stacks primitives aligned |
| `conxius-enclave-sdk` | `62f34c39` | `checkout` | Vertical Sovereignty | **PASS** | Nitro TEE hardware signing SDK & v2.1.0 changelog aligned |
| `conxius-platform` | `643253c1` | `checkout` | Operational Unification | **PASS** | Platform compose & environment scaffolding aligned |
| `conxian-labs-site` | `3a1eb75d` | `checkout` | Operational Unification | **PASS** | Public site & corporate governance surface aligned |

---

## Deprecation & Realignment Directives

1. **Legacy Protocol Deprecation**: `Conxian/Conxian` Clarity protocol repository is explicitly deprecated in favor of active modular repos (`lib-conxian-core`, `conxian-gateway`, `conxian-nexus`).
2. **Domain Separation Standard**: Protocol surfaces (`conxian.org`) are strictly separated from Corporate Governance surfaces (`conxian-labs.com`).
3. **Submodule Pin Policy**: All submodules enforce `pin-to-parent` policy with `update=checkout` in `.gitmodules`.
