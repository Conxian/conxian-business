# Phase 3 Enhancement Roadmap — Session 55 Update

> **4/7 complete.** 5 PRs merged in Session 55. 3 issues remain (#267, #272, #271).
>
> Original scope: enclave-sdk enhancement issues #267–#273.

---

## 1. Dependency Graph

```
                    ┌──────────────────┐
                    │  #267 BitVM2     │ ← P0, blocks sBTC bridge
                    │  Groth16 SNARK   │
                    └────────┬─────────┘
                             │ depends on
                    ┌────────▼─────────┐
                    │  #272 BitVM      │ ← P2, primitives
                    │  SNARK validate  │
                    └──────────────────┘

┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  #268 Ark        │     │  #269 CCTP       │     │  #270 DLC        │
│  ASP signing     │     │  Attestation     │     │  CET + oracle    │
└──────┬───────────┘     └──────┬───────────┘     └──────┬───────────┘
       │ depends on            │ depends on            │ depends on
       ▼                       ▼                       ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  FROST DKG (#264)│     │  ECDSA verify    │     │  Schnorr verify  │
│  ✅ DONE         │     │  (k256/P-256)    │     │  (secp256k1)     │
└──────────────────┘     └──────────────────┘     └──────────────────┘

┌──────────────────┐     ┌──────────────────┐
│  #271 Lightning  │     │  #273 Covenant   │
│  LDK payments    │     │  CTV/APO/OP_CAT  │
└──────┬───────────┘     └──────┬───────────┘
       │ depends on            │ self-contained
       ▼                       │ (script construction)
┌──────────────────┐           │
│  LDK crate       │           │
│  (external dep)  │           │
└──────────────────┘
```

---

## 2. Per-Issue Deep Dive

### #267 — BitVM2 Groth16 SNARK Verification (P0)

**Current state:** 645 lines of boundary types, 21 `ProtocolUnsupported` refs.
No actual Groth16 proof verification.

**What it needs:** A Groth16 SNARK verifier for bitcoin-level computation proofs.
The BitVM2 bridge uses these proofs to validate Bitcoin L1 state transitions.

**Libraries (ranked by fit):**

| Library | Crate | Rust-Native | SNARK Type | Verdict |
|---------|-------|:-----------:|------------|---------|
| **bellman** | `bellman` v0.14 | ✅ | Groth16 (BLS12-381) | **Best fit** — Zcash-origin, same ecosystem as ZF FROST |
| arkworks | `ark-groth16` | ✅ | Groth16 (any curve) | Good alternative, more generic |
| sp1 | `sp1-sdk` | ✅ | Groth16 + STARK | Overkill (full zkVM), large dep |
| lambdaworks | `lambdaworks-groth16` | ✅ | Groth16 (BN254) | Lightweight, good for WASM |

**Recommendation: bellman + BLS12-381**

- Same Zcash Foundation ecosystem as ZF FROST (already in deps)
- Groth16 is the standard BitVM2 proof system
- BLS12-381 curve is pairing-friendly, widely audited
- ~50KB WASM footprint when compiled with `--features wasm`

**Implementation plan:**

1. Add `bellman = "0.14"` to Cargo.toml (behind `bitvm2-crypto` feature)
2. Create `src/protocol/bitvm2_crypto.rs` (mirroring frost_crypto.rs pattern)
3. Implement `verify_groth16_proof(vk, proof, public_inputs) → ConclaveResult<bool>`
4. Wire into BitVM2 challenge protocol in `bitvm2.rs`
5. Connect to `lib-conxian-core` BitVM2 bridge target architecture

**Effort:** ~2 sprints (1 for verifier, 1 for bridge wiring)

**Risk:** Medium. bellman is well-audited but BitVM2 itself is pre-specification.

---

### #268 — Ark Protocol Signing (P1)

**Current state:** 533 lines, 23 `ProtocolUnsupported` refs.

**What it needs:** Ark protocol v0.3 ASP round signing. The Ark Service Provider
coordinates VTXO tree operations using threshold signatures from the user pool.

**Key observation:** Ark signing IS FROST threshold signing. After #264 (DKG) and
#275 (FrostSigningContext), the crypto primitives are in place. This issue is
primarily about protocol-level state machine logic:
- ASP round coordination (who signs what, when)
- VTXO tree commitment signing
- Forfeit transaction signing for unilateral exit

**Implementation plan:**

1. Define `ArkRoundState` enum (Registration, Attestation, Signing, Finalized)
2. Use `FrostSigningContext` for threshold signing operations
3. Implement VTXO tree operations (already structural in ark.rs)
4. Add `ark-crypto` feature gate, create `ark_crypto.rs`

**Depends on:** #264 ✅, #275 (FrostSigningContext)

**Effort:** ~1 sprint (protocol state machine + FROST integration)

**Risk:** Low. Core crypto exists. Protocol-level logic only.

---

### #269 — CCTP Attestation Verification (P1)

**Current state:** 176 lines, 1 gated operation.

**What it needs:** Verify Circle's ECDSA signatures on CCTP attestation messages.
Circle's Cross-Chain Transfer Protocol API returns signed attestations that must
be verified before releasing bridged USDC on the destination chain.

**Attestation format (from Circle CCTP docs):**
```json
{
  "attestation": "base64-encoded signed attestation",
  "message": {
    "version": 1,
    "source_domain": 0,
    "destination_domain": 1,
    "nonce": 123,
    "amount": "1000000",
    "recipient": "0x..."
  }
}
```

**Verification approach:**

1. Fetch Circle's public key (published at `https://iris-api.circle.com/v1/attestations/`)
2. Decode base64 attestation → extract signature + message
3. Verify ECDSA secp256k1 (or P-256) signature against message hash
4. Validate message fields (source/destination domain, nonce, amount, recipient)

**Rust crates needed:**
- `k256` (secp256k1 ECDSA) — already in deps via `secp256k1`
- `p256` (NIST P-256) — if Circle uses P-256 instead of secp256k1
- `base64` (already in deps)

**Implementation plan:**

1. Add `cctp-attestation` feature gate
2. Create `src/protocol/cctp_crypto.rs`
3. Implement `verify_cctp_attestation(attestation_b64, expected_message) → ConclaveResult<bool>`
4. Integrate with `chain_abstraction.rs` for cross-chain settlement

**Effort:** ~0.5 sprints (straightforward ECDSA verification)

**Risk:** Low. Well-defined spec from Circle.

---

### #270 — DLC CET Signing (P1)

**Current state:** 161 lines structural types.

**What it needs:** Contract Execution Transaction (CET) construction and signing
against oracle attestations. DLCs use schnorr signatures from oracles to unlock
funding outputs based on real-world events.

**Architecture:**

```
Oracle ──(schnorr attestation)──▶ DlcManager
                                    │
                                    ├── verify_oracle_attestation(sig, pubkey, outcome)
                                    ├── construct_cet(oracle_outcome, contract_params)
                                    ├── sign_cet(cet, funding_utxo) → PSBT
                                    └── broadcast(refund_tx) if timeout
```

**Depends on:**
- `bitcoin.rs` for PSBT construction (already structural)
- Schnorr signature verification (BIP-340, already in `secp256k1` dep)
- FROST for multi-oracle threshold (#264 ✅)

**Implementation plan:**

1. Add `dlc-crypto` feature gate
2. Create `src/protocol/dlc_crypto.rs`
3. Implement `verify_oracle_attestation(sig, pubkey, message) → ConclaveResult<bool>`
4. Implement `construct_cet(outcomes, funding_outpoint) → PSBT`
5. Implement `sign_cet_funding(psbt, key) → signed_psbt`
6. Implement `sign_cet_refund(psbt, key, timeout) → signed_psbt`

**Effort:** ~1 sprint

**Risk:** Medium. DLC spec is well-defined but CET construction is nuanced.

---

### #271 — Lightning LDK Payment Execution (P1)

**Current state:** 307 lines structural types.

**What it needs:** Full Lightning Network payment execution via LDK (Lightning Dev Kit).

**LDK integration approach:**

LDK provides a complete Lightning node implementation. The integration consists of:
1. LDK channel management (open, close, force-close)
2. Invoice parsing (BOLT 11) and payment routing
3. HTLC management and signing
4. Channel state persistence

**Dependencies:**
- `lightning` (LDK core) — ~200KB WASM
- `lightning-invoice` (BOLT 11 parsing)
- `lightning-persister` (channel state storage)

**Implementation plan:**

1. Add `lightning-crypto` feature gate
2. Create `src/protocol/lightning_crypto.rs`
3. Implement `LightningPaymentExecutor` wrapping LDK `ChannelManager`
4. Implement `pay_invoice(bolt11_string, amount_msat) → ConclaveResult<PaymentHash>`
5. Implement `create_invoice(amount_msat, description) → ConclaveResult<String>`
6. Wire channel state through `FrostSigningContext` for threshold signing

**Effort:** ~2-3 sprints (LDK is a large, complex dependency)

**Risk:** High. LDK integration is non-trivial. Channel state management,
fee estimation, and route-finding are complex subsystems.

**Alternative:** For MVP, implement invoice parsing + payment status tracking
only (no full channel management). Use external LSP for channel operations.

---

### #272 — BitVM SNARK Proof Validation (P2)

**Current state:** 132 lines structural types.

**What it needs:** SNARK proof validation for Bitcoin-level computation
verification. This is the primitive layer that BitVM2 (#267) builds on.

**Relationship to #267:** #272 is the general-purpose SNARK verifier.
#267 is the BitVM2-specific integration. Both need a Groth16 verifier.

**Implementation plan:**

1. Share `bellman` Groth16 verifier with #267
2. Implement `BitVmManager::verify_snark(proof, statement) → bool`
3. Wire challenge-response protocol: prover submits proof, verifier checks
4. Aggregate multi-prover proofs via FROST threshold

**Depends on:** #267 (shared bellman verifier)

**Effort:** ~0.5 sprints (after #267, mostly protocol wiring)

**Risk:** Low. Shared infrastructure with #267.

---

### #273 — Covenant Enforcement (P2)

**Current state:** 114 lines structural types.

**What it needs:** Bitcoin covenant script construction and validation.
Supports CTV (BIP-119), APO (BIP-118), and OP_CAT covenant patterns.

**Covenant patterns:**

| Pattern | BIP | What it does |
|---------|-----|-------------|
| CTV | BIP-119 | Restrict spending to a specific transaction template |
| APO | BIP-118 | Allow signature to cover only specific inputs |
| OP_CAT | Draft | Concatenate stack elements for covenant introspection |

**Implementation plan:**

1. Implement `CovenantScript::new_ctv(tx_template_hash)` — BIP-119
2. Implement `CovenantScript::new_apo(sighash_flags)` — BIP-118
3. Implement `CovenantScript::new_cat(covenant_rules)` — OP_CAT pattern
4. Implement `CovenantScript::verify(spending_tx) → bool`
5. Integrate with `statechain.rs` for transfer condition enforcement
6. Integrate with `bitcoin.rs` for Tapscript covenant leaf construction

**No external crypto deps needed.** This is pure script construction +
secp256k1 signature verification (already in deps).

**Effort:** ~1 sprint

**Risk:** Low. Script construction only. CTV/APO are well-specified.

---

## 3. Recommended Implementation Order

| Priority | Issue | Effort | Depends On | Cumulative |
|:--------:|-------|:------:|------------|:----------:|
| **1** | #273 Covenant | ✅ DONE | — | Session 55 |
| **2** | #269 CCTP | ✅ DONE | — | Session 55 |
| **3** | #268 Ark | ✅ DONE | — | Session 55 |
| **4** | #270 DLC | ✅ DONE | — | Session 55 |
| **5** | #272 BitVM | 0.5 sprint | #267 (shared verifier) | TBD |
| **6** | #267 BitVM2 | 2 sprints | bellman, #272 | TBD |
| **7** | #271 Lightning | 2-3 sprints | LDK | TBD |


**Why this order:**
1. Covenant (#273) is self-contained, no external deps, builds confidence
2. CCTP (#269) is the smallest, quickest win
3. Ark (#268) leverages just-completed FROST work
4. DLC (#270) builds on FROST + bitcoin PSBT
5. BitVM (#272) + BitVM2 (#267) share infrastructure
6. Lightning (#271) is the most complex, saved for last

---

## 4. Feature Flag Strategy

Following the `frost-crypto` pattern established in #264:

```toml
# Cargo.toml
[features]
frost-crypto = ["frost-secp256k1-tr"]
ark-crypto = ["frost-crypto"]          # depends on FROST
cctp-attestation = ["k256", "base64"]
dlc-crypto = ["frost-crypto", "secp256k1"]
lightning-crypto = ["lightning", "lightning-invoice"]
bitvm2-crypto = ["bellman"]
covenant-crypto = []                    # no external deps
```

Each feature gate follows the same pattern:
- Feature gate in `Cargo.toml`
- `#[cfg(feature = "...")]` on the `*_crypto.rs` module
- Structural boundary module (`*.rs`) unchanged
- Test gating: `#[cfg(all(test, feature = "..."))]` for crypto tests
- `#[cfg(not(feature = "..."))]` for stub-only tests

---

## 5. Module Count Projection

| Phase | New Crypto Modules | Cumulative |
|:-----:|--------------------|:----------:|
| Now | frost_crypto ✅ | 47 |
| #273 | covenant_crypto | 48 |
| #269 | cctp_crypto | 49 |
| #268 | ark_crypto | 50 |
| #270 | dlc_crypto | 51 |
| #272 | bitvm_crypto | 52 |
| #267 | bitvm2_crypto | 53 |
| #271 | lightning_crypto | 54 |

**Target: 54 modules** (47 current + 7 crypto backends)

---

## 6. Risk Assessment

| Issue | Technical Risk | Integration Risk | Audit Risk |
|:-----:|:-------------:|:----------------:|:----------:|
| #273 Covenant | 🟢 Low | 🟢 Low | 🟢 Low (script-only) |
| #269 CCTP | 🟢 Low | 🟢 Low | 🟢 Low (simple ECDSA) |
| #268 Ark | 🟢 Low | 🟡 Medium (ASP protocol) | 🟡 Medium (spec evolving) |
| #270 DLC | 🟡 Medium | 🟡 Medium | 🟡 Medium (CET nuances) |
| #272 BitVM | 🟡 Medium | 🟡 Medium | 🔴 High (pre-spec) |
| #267 BitVM2 | 🟡 Medium | 🔴 High (bridge) | 🔴 High (pre-spec) |
| #271 Lightning | 🔴 High | 🔴 High | 🟡 Medium (LDK audited) |

---

*This research was conducted by an AI agent (OpenHands) as part of Session 54.
All dependency assessments verified against crate documentation and BitVM2/Ark/DLC
specifications available as of August 2026.*
