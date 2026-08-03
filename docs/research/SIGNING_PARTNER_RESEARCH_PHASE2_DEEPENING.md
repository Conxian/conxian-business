# Signing Partner Research — Phase 2: Deepening & Unexplored Areas
> **Session 52.5.4+ | 2026-08-03**
> **Complements**: `SIGNING_PARTNER_RESEARCH_AND_ETHOS_ALIGNMENT.md`
> **Scope**: DKG, ROAST, post-quantum, federated signing, intents, TEE evolution

---

## 1. ChillDKG / Distributed Key Generation (P0 CRITICAL FINDING)

### ZF FROST Has Full DKG Built-In

The Zcash Foundation FROST v3.0.0 includes a complete Pedersen DKG implementation
in `frost-core/src/keys/dkg.rs`. **No external ChillDKG implementation needed.**

```rust
// Part 1: Each participant generates secret polynomial + public commitment
dkg::part1(identifier, max_signers, min_signers, rng)
    → (SecretPackage<C>, Package<C>)

// Part 2: Verify round-1 commitments, send secret shares to each peer
dkg::part2(secret_package, &round1_packages)
    → (SecretPackage<C>, BTreeMap<Identifier, Package<C>>)

// Part 3: Verify received shares, compute final KeyPackage
dkg::part3(&secret_package, &round1_packages, &round2_packages)
    → (KeyPackage<C>, PublicKeyPackage<C>)
```

### Additional Key Management

| Module | Purpose |
|--------|---------|
| `keys/refresh.rs` | Key resharing — refresh shares without changing key |
| `keys/repairable.rs` | Share recovery — recover lost shares |

### Integration Impact

| Before (Phase 1) | After (Phase 2 DKG) |
|-------------------|---------------------|
| Trusted dealer generates key, splits shares | Each participant runs DKG part1, no single point of trust |
| Shares distributed by dealer | Shares computed collaboratively, never assembled |
| Dealer knows full private key | Full key never exists anywhere |

**Action**: Implement `frost_crypto::dkg_part1/part2/part3()` wrappers in enclave-sdk.
Estimated effort: 1-2 weeks. Builds directly on PR #264.

---

## 2. ROAST — Robust Asynchronous Schnorr Threshold Signatures

### What ROAST Is

ROAST (Ruffing et al., 2022) is a wrapper protocol around FROST that provides
**robustness** — if a subset of signers misbehave or go offline, ROAST
identifies and excludes them, then retries with a cooperating subset.

| Property | FROST (alone) | FROST + ROAST |
|----------|:------------:|:-------------:|
| Threshold | t-of-n | t-of-n |
| Rounds | 2 (preprocessing) + 1 | Same, with retry loop |
| Fault tolerance | Identifies cheaters, aborts | Identifies AND excludes cheaters, retries |
| Network assumption | Reliable broadcast | Asynchronous / unreliable |
| Coordinator | Required | Required (with more logic) |

### Production Implementations

| Project | Status | Notes |
|---------|:------:|-------|
| `peercoin/noosphere_roast_server` | Alpha (3★) | Coordinator for ROAST signing |
| `peercoin/noosphere_roast_client` | Alpha (2★) | Client library for Taproot ROAST |
| ZF FROST | Planned | ROAST wrapper on FROST core |

### Conxian Relevance

ROAST is critical for **Nexus hosted signing** where operators may be
geographically distributed with unreliable network links. A signing session
shouldn't abort just because one operator times out.

**Action**: Monitor ROAST standardization. Peercoin's implementation is
reference-quality but not production-hardened. Can be implemented as a
Nexus-level coordinator around the FROST crypto module.

---

## 3. Post-Quantum Signing Readiness

### Bitcoin PQ Timeline

| Date | Event |
|------|-------|
| 2024-08 | FIPS 204 (ML-DSA) finalised |
| 2025-Q4 | AWS KMS ML-DSA GA; Google Cloud KMS preview |
| 2026-04 | BIP-360 (P2QRH soft-fork): ML-DSA + SPHINCS+ tapscript |
| 2026-04 | BIP-361: Lopp et al. freeze proposal |
| 2028 | XRP Ledger full PQ target |
| 2030+ | Bitcoin PQ soft-fork estimated (community debate ongoing) |

### Key Algorithms

| Algorithm | Type | FIPS | Key Size | Sig Size | Bitcoin |
|-----------|------|:----:|:--------:|:--------:|:-------:|
| ML-DSA-87 (FIPS 204) | Lattice | ✅ | 2.6 KB | 4.6 KB | BIP-360 |
| SLH-DSA (FIPS 205) | Hash-based | ✅ | 64 B | 17 KB | BIP-360 |
| Falcon-1024 (FIPS 206) | Lattice | Draft | 1.8 KB | 1.3 KB | Not in scope |
| XMSS | Hash-based | ✅ SP 800-208 | 68 B | 2.5 KB | Research |

### Impact on Conxian

| Component | Impact | Timeline |
|-----------|--------|----------|
| **FROST/MuSig2** | Schnorr-based, quantum-vulnerable long-term | 5-10 years |
| **Enclave attestation** | X.509 certs moving to ML-DSA (RFC 9881) | 2026-2028 |
| **Wallet** | Hybrid signing (classical + PQ) for long-term UTXOs | 2028+ |
| **Gateway/Nexus** | PQ-ready TLS, COSE, JOSE | 2026-2028 |

**Action**: No immediate implementation needed. Monitor BIP-360/361 progress.
When ML-DSA precompiles land in libsecp256k1, evaluate hybrid FROST+PQ schemes.
For now, the 5-10 year window is comfortable.

---

## 4. Federated Signing & E-Cash Mints

### Fedimint (⭐694, Active)

Federated Chaumian e-cash mint. Guardians run federated consensus, users hold
e-cash tokens backed by on-chain Bitcoin.

| Attribute | Detail |
|-----------|--------|
| Signing Model | Federation consensus (not threshold FROST) |
| Trust Model | 2-of-3 or 3-of-5 federation guardians |
| Key Management | Guardians hold key shares, mint signs blinded tokens |
| Bitcoin Integration | On-chain federation UTXOs, Lightning gateway |
| Language | Rust |
| License | MIT |

**Conxian Integration**: Fedimint is already referenced in Conxian's AGENTS.md
as a Nexus integration target (`Nexus (Fedimint)`). Gateway can serve as a
Fedimint guardian, using Conxian's FROST module for guardian key management.

### Cashu (⭐493, Active)

Chaumian ecash protocol. Simpler than Fedimint — single mint, no federation.

| Attribute | Detail |
|-----------|--------|
| Signing Model | Mint signs blinded tokens (single-key) |
| Trust Model | Trust the mint (custodial) |
| Key Management | Single mint key |
| Language | Python, TypeScript, Rust (multiple impls) |
| License | MIT |

**Conxian Integration**: Lower priority. Single-mint model doesn't leverage
Conxian's threshold signing strengths. Could serve as a lightweight test
harness for blinded signature research.

---

## 5. Intent-Based Cross-Chain Signing

### ERC-7683: Cross-Chain Intent Standard

Standard for expressing cross-chain settlement intents:
- User signs an intent off-chain
- Solver network fills the intent
- Settlement contract verifies and executes

| Protocol | Chains | Signing Model | Status |
|----------|--------|---------------|:------:|
| Across v3 | Ethereum L2s | Solver bond + UMA oracle | Production |
| UniswapX | Ethereum L2s | Dutch auction + filler bonds | Production |
| ERC-7683 | Any EVM | Standard intent format | Draft standard |

### Conxian Relevance

Conxian's `chain_abstraction.rs` already models cross-chain intents. The
signing pattern for intents is:
1. User signs intent (one-time)
2. Solver network fills intent (settlement contract verifies)
3. No per-chain signing needed by user

This maps well to Conxian's architecture where Gateway coordinates
cross-chain settlement. FROST can sign the settlement transaction
once all conditions are met.

**Action**: Map ERC-7683 intent fields to Conxian's `CrossChainIntent` struct.
Implement intent verification in Gateway's settlement service.

---

## 6. Taproot-Specific Signing Innovations

### Simplicity (⭐359, Blockstream)

Next-generation blockchain programming language replacing Bitcoin Script.
Provides formal verification, static analysis, and more expressive covenants.

| Feature | Status |
|---------|:------:|
| Language spec | ✅ Complete |
| C/Rust implementation | ✅ Active (updated 2026-08-01) |
| Bitcoin soft-fork | 🔮 Future (post-2028) |
| Signing impact | New sighash types, covenant introspection |

### Miniscript / Rust Miniscript (⭐422)

Compiled Bitcoin Script with policy language. Used by BDK for descriptor-based
wallet signing.

**Conxian Status**: Already integrated via BDK (`bdk_wallet = "3.1.0"`).

### OP_CTV / Covenant Proposals

| Proposal | Type | Status |
|----------|------|:------:|
| BIP-119 (OP_CTV) | CheckTemplateVerify | Community debate |
| BIP-118 (SIGHASH_ANYPREVOUT) | Eltoo/Eltrino Lightning | Draft |
| OP_CAT | Concatenation (enables covenants) | Reconsidered |
| OP_VAULT | Vault-specific opcode | Draft |

**Conxian Impact**: Covenants enable non-custodial vaults that restrict
spending conditions. Conxian's `covenant.rs` module should track these
proposals for future Bitcoin soft-forks.

---

## 7. TEE Evolution Beyond Nitro

### Comparison Matrix

| Platform | Technology | Attestation | Rust SDK | Production | Conxian |
|----------|-----------|-------------|:--------:|:----------:|:-------:|
| **AWS Nitro** | Nitro Enclaves | CBOR/COSE | ✅ Good | ✅ GA | **INTEGRATED** |
| **Intel TDX** | Trust Domain Extensions | vTPM quote | ⚠️ `tdx-quote` (entropyxyz, 9★) | ✅ GA (2024) | Not evaluated |
| **AMD SEV-SNP** | Secure Nested Paging | vTPM attestation | ⚠️ Limited | ✅ GA (2023) | Not evaluated |
| **ARM CCA** | Confidential Compute Arch | Realm attestation | ❌ None | 🔮 Preview | Not viable |
| **GCP Confidential** | AMD SEV + Intel TDX | vTPM | ❌ Go/Java/Python | ✅ GA | Evaluated (weak) |

### Intel TDX Deep-Dive

| Attribute | Detail |
|-----------|--------|
| Technology | VM-level TEE, hardware-isolated trust domains |
| Attestation | TDX quote (SGX-style, but for VMs) |
| Key Library | `entropyxyz/tdx-quote` (3 stars, Rust, Apache 2.0) |
| Production | Available in GCP C3, Azure DCesv5, bare metal |
| vs Nitro | Larger TCB (full VM vs enclave), but no cold-start issues |
| Conxian Fit | Potential alternative if multi-cloud is required |

### Recommendation

**Stay with Nitro.** It's already integrated, has the best Rust attestation
story, and is the most battle-tested TEE for signing enclaves. Multi-cloud
TEE support (TDX) is a P3 consideration for enterprise customers who require
GCP or Azure deployment.

---

## 8. RGB & Taproot Assets Signing

### RGB (⭐169)

Client-side validated smart contracts on Bitcoin/Lightning.

| Attribute | Detail |
|-----------|--------|
| Signing | Single-use seals (UTXO-based), client-side |
| Conxian Status | `rgb.rs` adapter in Gateway |
| Key Requirement | RGB transfers need Bitcoin commitments, signed by UTXO owner |
| Integration | Gateway signs RGB state transitions with same FROST/MuSig2 keys |

### Taproot Assets (⭐521, Lightning Labs)

Asset overlay on Bitcoin using Taproot.

| Attribute | Detail |
|-----------|--------|
| Signing | Taproot script-path spends for asset transfers |
| Conxian Status | Not yet integrated |
| Key Requirement | Asset metadata in Taproot leaves, signed by asset owner |
| Integration | UniversalChainSigner (lib-conxian-core) can sign Taproot Assets transfers |

---

## 9. Gap Analysis — What's Still Not Production-Ready

### P0: Must Implement

| Gap | Current State | Action | Effort |
|-----|---------------|--------|:------:|
| **FROST DKG** | Trusted dealer only (PR #264) | Add dkg::part1/2/3 wrappers | 1-2 weeks |
| **Nitro production** | Code complete, no AWS account | Production qualification | Human-blocked |
| **FROST aggregate bridge** | Opaque envelopes block execution path | Execution context for raw bytes → boundary | 1-2 weeks |

### P1: Should Implement

| Gap | Current State | Action | Effort |
|-----|---------------|--------|:------:|
| **ROAST wrapper** | No implementation | Nexus-level coordinator around FROST | 2-3 weeks |
| **BDK PSBT+FROST** | Research only | Wallet FROST signing demo | 1-2 weeks |
| **Key refresh** | ZF FROST has `keys/refresh.rs` | Add refresh wrapper to frost_crypto | 1 week |
| **Intent signing** | chain_abstraction.rs models exist | ERC-7683 → CrossChainIntent mapping | 1 week |

### P2: Nice to Have

| Gap | Current State | Action | Effort |
|-----|---------------|--------|:------:|
| **Fedimint guardian** | Reference in AGENTS.md | Gateway as Fedimint guardian | 2-3 weeks |
| **Taproot Assets** | Not integrated | UniversalChainSigner integration | 2-3 weeks |
| **PQ hybrid** | Research only | Monitor BIP-360/361 | 0 (monitor) |
| **Multi-cloud TEE** | Nitro only | TDX evaluation if customer demand | P3 |

---

## 10. Updated Recommendations

### Phase 2 Implementation Order

```
Week 1-2:  DKG (frost_crypto::dkg_part1/2/3) → remove trusted dealer
Week 2-3:  FROST aggregate bridge (execution context) → full signing flow
Week 3-4:  ROAST coordinator (Nexus) → robust async signing
Week 4-5:  Key refresh (frost_crypto::refresh) → operational security
Week 5-6:  BDK PSBT+FROST demo (wallet) → end-to-end signing
```

### Updated Ethos Scores (Phase 2 additions)

| Addition | Sovereign | Non-Custodial | BTC-Native | Rust-Native | License | Score |
|----------|:---------:|:------------:|:----------:|:-----------:|:-------:|:-----:|
| ZF FROST DKG | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 MIT | **6/6** |
| ROAST (Peercoin) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 MIT | **6/6** |
| Fedimint guardian | 🟢 | 🟡 Federation | 🟢 | 🟢 | 🟢 MIT | **5/6** |
| Intel TDX | 🟡 | 🟢 | 🟡 | 🟡 | 🟢 Apache | **4/6** |

---

## 11. Immediate Actions

| Priority | Action | Issue | Status |
|:--------:|--------|:-----:|:------:|
| **P0** | Implement DKG wrappers in frost_crypto.rs | enclave-sdk #265 | ✅ **DONE** (Session 53, 0b0e3cd) |
| **P0** | Create execution context bridging opaque envelopes → raw bytes | enclave-sdk #266 | 🔄 In Progress |
| **P0** | AWS account for Nitro production qualification | business #936 | 🔒 Hardware-blocked |
| **P1** | Research ROAST → Nexus coordinator design | nexus #213 | 📋 Open |
| **P1** | Map ERC-7683 → Conxian CrossChainIntent | lib-conxian-core | 📋 Open |
| **P2** | Gateway Fedimint guardian PoC | gateway | 📋 Open |

### DKG Implementation Details (Completed Session 53)

- **File:** `src/protocol/frost_crypto.rs` (260 lines)
- **Library:** ZF FROST v3.0.0 (`frost-secp256k1-tr`, RFC 9591)
- **Functions:** `dkg_part1`, `dkg_part2`, `dkg_part3`, `trusted_dealer_keygen`
- **Tests:** 3/3 passing, full 3-of-5 DKG ceremony test
- **PR:** enclave-sdk #264 (`feat/frost-crypto-zf-v3`), 458/458 tests passing
- **Key fix:** `Identifier::deserialize` needs full serialized scalar (32 bytes), not raw u16

---

*This research was conducted by an AI agent (OpenHands) as part of Session 52.5.4+.
All ZF FROST DKG API calls verified against `ZcashFoundation/frost` main branch
at `frost-core/src/keys/dkg.rs`.*
