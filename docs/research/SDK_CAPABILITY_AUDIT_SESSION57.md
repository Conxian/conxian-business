# Cross-Repo SDK Capability Audit — Session 57

> **Date**: 2026-08-05 | **Scope**: enclave-sdk ↔ gateway ↔ nexus ↔ lib-conxian-core
> **Method**: Ground-truth analysis of every module, every import, every re-export

---

## 1. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│  conxian-gateway                  conxian-nexus          │
│  ┌─────────────────┐             ┌─────────────────┐    │
│  │ pkg/conxian-core │             │ lib-conxian-core │    │
│  │ (local wrapper)  │             │ (git rev dep)    │    │
│  │                  │             │ features: full-  │    │
│  │ features: full-  │             │   sdk            │    │
│  │   sdk            │             └────────┬────────┘    │
│  └────────┬─────────┘                      │             │
│           │                                │             │
│           ▼                                ▼             │
│  ┌─────────────────────────────────────────────────┐    │
│  │          lib-conxian-core (v0.3.x)               │    │
│  │  ┌──────────────────┐  ┌───────────────────────┐ │    │
│  │  │  Own types (17    │  │  sdk.rs bridge         │ │    │
│  │  │  modules)         │  │  (52 re-exports)       │ │    │
│  │  │  • ConxianError   │  │  ★ ZERO consumers     │ │    │
│  │  │  • TrustTier      │  │  ★ dead code          │ │    │
│  │  │  • ChainAdapter   │  └───────────┬───────────┘ │    │
│  │  │  • FedimintMint   │              │              │    │
│  │  └──────────────────┘              │              │    │
│  └────────────────────────────────────┼──────────────┘    │
│                                       │                    │
│                                       ▼                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │        conxius-enclave-sdk (v2.0.12)             │    │
│  │  83 modules: 5 boundary-only, 8 partial-logic,   │    │
│  │  13 signing (hidden), 57 full-logic               │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 2. KEY FINDINGS

### 2.1 The `sdk.rs` Bridge Is Dead Code

**Severity: HIGH**

Core's `src/sdk.rs` re-exports 52 SDK modules through 6 feature gates. Zero consumers exist.

| Consumer | Uses `core::sdk::*` path? |
|----------|:-------------------------:|
| Gateway | ❌ No — uses `conxian_core::ConxianError` etc (core's own types) |
| Nexus | ❌ No — uses `lib_conxian_core::*` (core's own types) |
| Core itself | ❌ Only `tests/sdk-compat/` touches SDK types |

Gateway and Nexus import core's OWN types (`ConxianError`, `ChainAdapter`, `TrustTier`, etc.),
not SDK types via the `sdk::` bridge. The bridge is 138 lines of unused code.

### 2.2 The `signing/` Crate Is Completely Invisible

**Severity: HIGH**

13 SDK signing modules with zero consumer visibility:

| Module | Lines | Description |
|--------|:-----:|-------------|
| `signing::bip322_signing` | — | BIP-322 signature execution |
| `signing::musig2_signing` | — | MuSig2 threshold signing |
| `signing::taproot` | — | Taproot key-path/script-path |
| `signing::threshold` | — | Generic threshold signing |
| `signing::ucs` | — | Universal Chain Signer |
| `signing::bip110_signing` | — | BIP-110 anchoring signing |
| `signing::bitvm2_signing` | — | BitVM2 proof signing |
| `signing::covenant_signing` | — | Covenant template signing |
| `signing::dlc_signing` | — | DLC CET signing |
| `signing::lightning_signing` | — | Lightning invoice signing |
| `signing::statechain_signing` | — | Statechain VTXO signing |
| `signing::wasm_runtime` | — | WASM signing runtime |
| `signing::zkml_signing` | — | ZKML proof signing |

**Root cause**: `src/sdk.rs` does not re-export any `signing::*` modules.

**Impact**: Gateway has its own `musig` and `Bip322Verifier` in `pkg/conxian-core`, duplicating
SDK signing capability. Nexus has no signing integration at all.

### 2.3 Boundary-Only Protocol Modules

**Severity: MEDIUM (known)**

6 modules are structural validation only — all execution paths return `ProtocolUnsupported`:

| Module | Lines | Since | Plan |
|--------|:-----:|-------|------|
| `protocol::bitvm2` | 1086 | v2.0.0 | P0 #267 — needs bellman Groth16 |
| `protocol::frost` | 1119 | v2.0.0 | Has `frost_crypto.rs` backend — feature-gated |
| `protocol::nexus::fedimint` | 767 | v2.0.0 | P1 — needs federation protocol |
| `protocol::ark` | 669 | v2.0.0 | P1 #268 — VTXO Merkle done, signing needed |
| `protocol::nexus::roast` | 640 | v2.0.12 | P1 #213 — needs ROAST coordinator |
| `protocol::statechain` | 601 | v2.0.12 | P2 #260 — FROST-based |

### 2.4 Version Mismatch: Core pins SDK v2.0.11, SDK is v2.0.12

**Severity: LOW**

- Core `Cargo.toml`: `conxius-enclave-sdk = { version = "=2.0.11" }`
- SDK current version: `v2.0.12`
- Impact: New modules (`statechain`, `roast`, `control_model_adapter`) can't be used even if bridge is fixed

### 2.5 Gateway Architecture: Local Core Wrapper

**Severity: INFO**

Gateway doesn't use `lib-conxian-core` directly. It has its own `pkg/conxian-core` crate that:
- Depends on `lib-conxian-core` with `features = ["full-sdk"]`
- Defines its own types: `ConxianError`, `ChainAdapter`, `GatewayState`, etc.
- Has its own `musig`, `lightning`, `settlement`, `persistence`, `trust_policy` modules
- The SDK types are available but never accessed

### 2.6 Nexus Architecture: Git Rev Dependency

**Severity: LOW**

Nexus depends on core via a pinned git revision, not workspace:
```toml
lib-conxian-core = { git = "...", rev = "d3d8b3bb...", features = ["full-sdk"] }
```
This means Nexus doesn't get core updates automatically. It also means the `sdk.rs` bridge
is included in the build but never used.

### 2.7 SDK Modules NOT Re-exported by Core

**Severity: MEDIUM**

| Module | Reason | Action |
|--------|--------|--------|
| `protocol::babylon` | Missing from `sdk.rs` | Add to blockchain re-exports |
| `protocol::rgb` | Missing from `sdk.rs` | Add to blockchain re-exports |
| `protocol::statechain` | Commented "v2.0.12+" | Uncomment after version bump |
| `protocol::control_model_adapter` | Commented "v2.0.12+" | Uncomment after version bump |
| `protocol::nexus::roast` | Commented "v2.0.12+" | Uncomment after version bump |
| `protocol::frost_crypto` | Feature-gated | Document gate requirements |
| `protocol::bip110` | Feature-gated | Document gate requirements |
| `enclave::nitro` | Not re-exported | Add to enclave re-exports |
| `enclave::durable_replay` | Commented "v2.0.12+" | Uncomment after version bump |
| `enclave::trust` | Not re-exported | Add to enclave re-exports |
| `enclave::trust_contracts` | Not re-exported | Add to enclave re-exports |
| `enclave::proof` | Not re-exported | Add to enclave re-exports |
| `enclave::proofs` | Not re-exported | Add to enclave re-exports |
| `enclave::verifiers::*` | Not re-exported | Add verifier re-exports |
| `signing::*` (all 13) | Not re-exported | **P0: Add signing re-exports** |
| `serde_big_array` | Not re-exported | Add utility re-exports |

## 3. RECOMMENDATIONS

### P0 — Immediate

| # | Action | Repo | Rationale |
|---|--------|------|-----------|
| 1 | **Add `signing` re-exports to core `sdk.rs`** | lib-conxian-core | 13 signing modules invisible. Gateway duplicates this capability. |
| 2 | **Bump SDK pin to v2.0.12** | lib-conxian-core | Unlock statechain, roast, control_model_adapter |
| 3 | **Uncomment v2.0.12 modules** | lib-conxian-core `sdk.rs` | statechain, roast, control_model_adapter, durable_replay |
| 4 | **Wire gateway signing to SDK signing** | conxian-gateway | Replace `pkg/conxian-core/src/musig.rs` with SDK's `signing::musig2_signing` |

### P1 — This Sprint

| # | Action | Repo | Rationale |
|---|--------|------|-----------|
| 5 | Add missing module re-exports (babylon, rgb, enclave::*) | lib-conxian-core | Close the 16-module gap |
| 6 | Wire Nexus to SDK signing via core bridge | conxian-nexus | Nexus has no signing integration |
| 7 | Add `sdk-infrastructure` + `sdk-signing` feature flags | lib-conxian-core | Granular feature gates for consumers |
| 8 | Create signing integration tests in core `tests/sdk-compat/` | lib-conxian-core | Verify signing bridge works end-to-end |

### P2 — Next Sprint

| # | Action | Repo | Rationale |
|---|--------|------|-----------|
| 9 | Convert gateway from local `conxian_core` wrapper to SDK-native | conxian-gateway | Eliminate type duplication |
| 10 | Implement ROAST coordinator backed by SDK's roast module | conxian-nexus | #213 |
| 11 | Document full SDK consumption path for new integrators | conxian-business | Developer onboarding |
| 12 | Add CI check that all SDK public types are consumed somewhere | .github | Prevent regression |

### P3 — Backlog

| # | Action | Rationale |
|---|--------|-----------|
| 13 | FROST DKG: Remove `frost-crypto` feature gate, make default | After #283 attestation gating |
| 14 | Ark signing: Bridge VTXO Merkle tree to signing module | #268 |
| 15 | BitVM2 Groth16: bellman integration | #267 |
| 16 | Fedimint: Federation protocol implementation | Long-lead research item |

## 4. CONSUMPTION MATRIX

### By SDK Module Category

| Category | Modules | Re-exported | Consumed | Dead |
|----------|:-------:|:-----------:|:--------:|:----:|
| Blockchain | 23 | 18 | 0 | 5 |
| Cross-cutting | 16 | 14 | 0 | 2 |
| Rails | 6 | 6 | 0 | 0 |
| Nexus | 2 | 1 | 0 | 1 |
| Infrastructure | 6 | 3 | 0 | 3 |
| Enclave | 17 | 4 | 0 | 13 |
| Signing | 13 | 0 | 0 | 13 |
| **TOTAL** | **83** | **46** | **0** | **37** |

> "Consumed" = actually imported and used by at least one higher-level repo (gateway/nexus).
> The core's `sdk.rs` re-exports don't count as consumption — they have zero downstream users.

### By Consumer

| Consumer | SDK Modules Used | SDK Types Used | Core Types Used |
|----------|:----------------:|:--------------:|:---------------:|
| Gateway | 0 | 0 | ~30 (ConxianError, TrustTier, etc.) |
| Nexus | 0 | 0 | ~15 (via lib-conxian-core at git rev) |
| Core (sdk-compat) | 3 | 5 | — |

## 5. SUMMARY

The SDK is a **well-built but disconnected component**. It has 83 modules, mature structural
validation, and real crypto backends for FROST, MuSig2, DLC, and BIP-322. But:

1. **Zero production consumers.** Gateway and Nexus don't know the SDK exists.
2. **The `sdk.rs` bridge is dead code.** Re-exports with no callers.
3. **13 signing modules are invisible.** Gateway built its own signing instead.
4. **5 protocol modules are boundary-only.** Structural validation without execution.
5. **Version pin is stale.** Core on v2.0.11, SDK at v2.0.12.

The fix is **not** more SDK work. The fix is **wiring**: update core's bridge, bump the
version pin, and have gateway/nexus consume SDK types through the bridge instead of
duplicating capabilities.

---

*This research was conducted by an AI agent (OpenHands) on behalf of Conxian.*
