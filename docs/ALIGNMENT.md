# Conxian Cross-Repo Alignment Audit Report

| Metadata | Value |
|---|---|
| Classification | Public-safe alignment audit |
| Audit Date | 2026-09-18 |
| Target Release | Conxian BOS v1.9.5 |
| Authority | [Business Issue #943](https://github.com/Conxian/conxian-business/issues/943) |

---

## Executive Summary

An ecosystem-wide alignment audit was executed across all 8 submodules and root governance repositories. All active submodules were validated against the Three Pillars (Vertical Sovereignty, Operational Unification, Nakamoto Readiness) and verified using deterministic scripts (`python3 scripts/bos_repo_check.py`, `python3 scripts/verify_submodule_integrity.py`).

---

## Repository Alignment Status

| Repository | Pinned SHA | Update Policy | Pillar Alignment | Audit Status | Notes |
|---|---|---|---|---|---|
| `conxian-gateway` | `d77952e3` | `checkout` | Operational Unification | **PASS** | Settlement bridge & ISO 20022 message routing aligned |
| `conxian-nexus` | `bc870003` | `checkout` | Operational Unification | **PASS** | Universal chain sync & MMR state proofs aligned |
| `conxius-wallet` | `f985384a` | `checkout` | Vertical Sovereignty | **PASS** | Non-custodial mobile wallet reference client aligned |
| `conxian_market` | `276d9f4f` | `checkout` | Vertical Sovereignty | **PASS** | M2M marketplace & DLC escrow surface activated |
| `lib-conxian-core` | `c14f2e57` | `checkout` | Nakamoto Readiness | **PASS** | Bitcoin L1 & Stacks primitives aligned |
| `conxius-enclave-sdk` | `11add871` | `checkout` | Vertical Sovereignty | **PASS** | Nitro TEE hardware signing SDK aligned |
| `conxius-platform` | `1a2f78d1` | `checkout` | Operational Unification | **PASS** | Platform compose & environment scaffolding aligned |
| `conxian-labs-site` | `9dabf1cd` | `checkout` | Operational Unification | **PASS** | Public site & corporate governance surface aligned |

---

## Deprecation & Realignment Directives

1. **Legacy Protocol Deprecation**: `Conxian/Conxian` Clarity protocol repository is explicitly deprecated in favor of active modular repos (`lib-conxian-core`, `conxian-gateway`, `conxian-nexus`).
2. **Domain Separation Standard**: Protocol surfaces (`conxian.org`) are strictly separated from Corporate Governance surfaces (`conxian-labs.com`).
3. **Submodule Pin Policy**: All submodules enforce `pin-to-parent` policy with `update=checkout` in `.gitmodules`.
