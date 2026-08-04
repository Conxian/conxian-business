# Signing Partner Research & Ethos Alignment

> **Session 52.5.3 | 2026-08-03**
> **Scope**: Full ecosystem audit of signing partners for Conxian hosted signing,
> Nexus, Gateway, and enclave-based solutions.
> **Mandate**: Sovereign-first, non-custodial, Bitcoin-native, production-ready.

---

## 0. Conxian Signing Architecture: Current State (Ground Truth)

### What IS Implemented

| Module | Implementation | Library | Features |
|--------|:-------------:|---------|----------|
| **MuSig2** | ✅ Full | `musig2` crate (secp256k1) | Key aggregation, nonce gen, partial signing, aggregation |
| **BIP-322** | ✅ Full | `bitcoin` crate | PSBT, sighash, Taproot script-path, SimpleSig |
| **DLC** | ✅ Structural | Custom (sha2) | Contract structs, CET outlines, oracle attestation |
| **Stacks signing** | ✅ Full | `EnclaveManager` | Value-bearing sign requests, trust-tier gating |
| **Chain Abstraction** | ✅ Full | `EnclaveManager` | Cross-chain intents, multi-chain signing |
| **Nitro Enclave** | ✅ Full (2600+ lines) | AWS Nitro | CBOR/COSE attestation, TEE verification |
| **Android StrongBox** | ✅ Full | Android KeyMint | Hardware-backed key gen, TEE attestation |
| **Replay Guard** | ✅ Full | Custom | Durable replay protection, nonce tracking |

### What Is BOUNDARY-ONLY (No Crypto Execution)

| Module | Lines | Status | Gap |
|--------|:-----:|:------:|-----|
| **FROST** | 716 | ⚠️ Boundary | DTOs, versioning, validation only. All value-bearing ops → `ProtocolUnsupported` |
| **Statechain (Spark)** | ~200 | ⚠️ Boundary | Delegates to FROST (which is also boundary-only) |
| **BitVM / BitVM2** | ~400 | ⚠️ Boundary | SNARK verification stubs, Groth16 outlines |
| **Covenant** | ~200 | ⚠️ Boundary | Covenant template validation only |

### Core Gap

**FROST threshold signatures are the critical missing piece.** Conxian has a complete
boundary specification (ciphersuites, participant IDs, session management, versioned
envelopes) but zero cryptographic execution. The `musig2` crate proves Conxian CAN
integrate external crypto libraries — FROST needs the same treatment.

---

## 1. FROST Implementation Landscape

### 1.1 Zcash Foundation FROST (⭐270)

| Attribute | Detail |
|-----------|--------|
| **Repo** | `ZcashFoundation/frost` |
| **Language** | Rust |
| **Ciphersuites** | secp256k1, ed25519, ed448, p256, ristretto255 |
| **IETF Compliance** | RFC 9591 |
| **DKG** | Trusted dealer + ChillDKG (BIP draft) |
| **Signing** | 2-round (with preprocessing) or 3-round (no preprocessing) |
| **Last Updated** | 2026-07-29 (active) |
| **License** | MIT / Apache 2.0 |
| **Mainnet Usage** | Spark protocol (Bitcoin DeFi), Ducat (Bitcoin lending) |

**Ethos Alignment: STRONG** ✅
- Rust (Conxian's primary language)
- secp256k1 ciphersuite (Bitcoin native)
- IETF-standardized (RFC 9591)
- Active maintenance
- MIT/Apache 2.0 (compatible with Conxian's licensing)
- Already used by Bitcoin DeFi projects in production

**Integration Path:**
```rust
// Conxian's frost.rs boundary types → Zcash FROST crypto backend
// Example: FrostSignRequest { ciphersuite, participants, threshold, message }
// → frost_secp256k1::sign(secret_share, commitments, message)
```

### 1.2 BIP-FROST Signing Spec (In Progress)

| Attribute | Detail |
|-----------|--------|
| **Repo** | `siv2r/bip-frost-signing` |
| **Status** | BIP draft (v0.3.3, 2025-12-29) |
| **Focus** | BIP-340 compatible FROST signing |
| **DKG** | Out of scope (ChillDKG separate BIP) |
| **Test Vectors** | 2-of-3 secp256k1 |

**Ethos Alignment: STRONG** ✅
- Bitcoin-specific BIP standardization
- BIP-340 compatible (Taproot native)
- Reference implementation in Python
- Coordinates with ChillDKG BIP for key generation

### 1.3 Coinbase FROST Implementation

| Attribute | Detail |
|-----------|--------|
| **Approach** | No signature aggregator (each participant verifies) |
| **Rounds** | 3-round (no preprocessing) |
| **Security** | All participants verify others' contributions |
| **Status** | Internal production use |

**Ethos Alignment: MODERATE** ⚠️
- Strong security model (no aggregator trust)
- But: proprietary, not open-source
- Not available as a library for integration

### 1.4 Blockchain Commons FROST Tooling

| Attribute | Detail |
|-----------|--------|
| **Sponsor** | Human Rights Foundation (2024-2025) |
| **Outputs** | Gordian Envelope, CLI tools, Learning FROST course |
| **Focus** | Developer education, UX, wallet integration |
| **Demos** | PSBT signing with BDK + ZF FROST, Hubert Dead-Drop Hub |

**Ethos Alignment: STRONG** ✅
- Human rights / sovereignty aligned
- Open-source, educational
- Complementary tooling (CLI, wallet integration)

---

## 2. Decentralized Signer Networks

### 2.1 Lit Protocol (Naga Mainnet — Dec 2025)

| Attribute | Detail |
|-----------|--------|
| **Architecture** | MPC + TSS + TEE hybrid |
| **Network** | Decentralized nodes, Naga v1 mainnet (Dec 2025) |
| **Token** | LITKEY (TGE 2025) |
| **AUDM** | $422M+ assets under decentralized management |
| **Chains** | Ethereum, Solana, Cosmos, Polygon, Avalanche, Arbitrum |
| **SDK** | v8 (JavaScript/TypeScript) |
| **Features** | Vincent (AI agent wallets), programmable signing policies, encryption |
| **Signing** | ECDSA + BLS threshold, Schnorr in development |
| **License** | Open-source core |

**Ethos Alignment: MODERATE** ⚠️

| Strength | Concern |
|----------|---------|
| Decentralized key management | No native Bitcoin/Taproot support (ECDSA only for now) |
| TEE + MPC hybrid (defense in depth) | JavaScript SDK (not Rust-native) |
| Programmable policies | Lit Actions are JS, not WASM or Rust |
| Production scale ($422M AUDM) | ERC-20 native, not Bitcoin-native |
| AI agent signing (Vincent) | Token dependency (LITKEY) |

**Integration Fit:** Gateway cross-chain signing for non-Bitcoin chains (Ethereum, Solana, Cosmos).
Not suitable for Bitcoin-native threshold signing where FROST/MuSig2 are required.

### 2.2 Entropy (Substrate L1 for MPC Signing)

| Attribute | Detail |
|-----------|--------|
| **Architecture** | L1 blockchain (Substrate) + threshold signing servers |
| **Scheme** | CGGMP21 (via `synedrion` library) |
| **Signing** | ECDSA threshold (EVM-focused) |
| **Programs** | WebAssembly on-chain (mutable) |
| **Consensus** | BABE + Grandpa (PoS) |
| **Validators** | Run Entropy chain node + threshold server |
| **License** | AGPL-3.0 |
| **Status** | Testnet / early production |
| **Key Libraries** | `synedrion` (85★), `manul` (7★), `tdx-quote` (TDX TEE) |

**Ethos Alignment: WEAK** ❌

| Strength | Concern |
|----------|---------|
| Rust/Substrate (good language fit) | **AGPL-3.0 license** — incompatible with Conxian's commercial model |
| WASM programs | ECDSA only, no Schnorr/Bitcoin support |
| TDX TEE integration | Requires running Entropy blockchain (operational overhead) |
| CGGMP21 (strong MPC) | EVM-native, not Bitcoin-native |

**Verdict:** AGPL-3.0 is a non-starter for Conxian's sovereign enterprise model.
The `synedrion` library could be studied for CGGMP21 patterns, but not directly integrated.

### 2.3 Threshold Network (6 Years in Production)

| Attribute | Detail |
|-----------|--------|
| **Architecture** | Decentralized threshold cryptography network |
| **History** | 6 years production, evolved from Keep + NuCypher |
| **Signing** | ECDSA threshold (tBTC v2 bridge) |
| **Focus** | Bitcoin → Ethereum bridge (tBTC), access control |
| **License** | GPL-3.0 |
| **Token** | T token (governance + staking) |

**Ethos Alignment: MODERATE** ⚠️

| Strength | Concern |
|----------|---------|
| Bitcoin bridge proven (tBTC v2) | **GPL-3.0 license** — viral copyleft |
| Longest production MPC network | ECDSA only, no Schnorr/FROST |
| Decentralized node set | Token-gated (not permissionless sovereign) |
| 6-year track record | Focused on Ethereum bridging, not general signing |

---

## 3. Hardware / TEE Signing Partners

### 3.1 AWS Nitro Enclaves (ALREADY INTEGRATED)

| Attribute | Detail |
|-----------|--------|
| **Conxian Module** | `nitro.rs` (2600+ lines) |
| **Attestation** | CBOR/COSE, full verification chain |
| **Status** | ✅ Production code, not yet qualified (needs AWS account) |
| **Gap** | Production provider qualification (AWS account required) |

**No additional partner needed.** Nitro is the correct TEE for Conxian's cloud signing.
The gap is operational (AWS account, production deployment), not technical.

### 3.2 Android KeyMint / StrongBox (ALREADY INTEGRATED)

| Attribute | Detail |
|-----------|--------|
| **Conxian Module** | `android_strongbox.rs`, `android_authorization.rs` |
| **Status** | ✅ Production code |
| **Gap** | Android hardware for production qualification |

### 3.3 Google Cloud Confidential Computing

| Attribute | Detail |
|-----------|--------|
| **Technology** | AMD SEV, Intel TDX |
| **SDK** | Go, Java, Python (no native Rust) |
| **Attestation** | vTPM-based |
| **License** | Proprietary (GCP service) |

**Ethos Alignment: WEAK** ❌
- No native Rust SDK
- AMD SEV has had side-channel vulnerabilities
- Less mature attestation model than Nitro
- Vendor lock-in to GCP

### 3.4 Azure Confidential Computing

| Attribute | Detail |
|-----------|--------|
| **Technology** | Intel SGX (deprecated), AMD SEV-SNP |
| **SDK** | C/C++ (Open Enclave SDK), Rust bindings possible |
| **Status** | SGX being phased out, SEV-SNP in preview |

**Ethos Alignment: WEAK** ❌
- SGX deprecated (multiple CVEs)
- SEV-SNP less battle-tested than Nitro
- Azure not aligned with Bitcoin sovereignty ethos

### 3.5 Ledger / Hardware Security Modules (HSMs)

| Attribute | Detail |
|-----------|--------|
| **Devices** | Ledger Nano S/X, Ledger Vault (enterprise) |
| **SDK** | LedgerJS (JavaScript), Ledger Live SDK |
| **Chains** | Bitcoin, Ethereum, 5000+ tokens |
| **Attestation** | Secure Element (ST31/ST33) |

**Ethos Alignment: STRONG for wallet, WEAK for server** ✅/❌
- Best-in-class for Conxius Wallet integration
- Not suitable for Gateway/Nexus server-side signing (USB-dependent, not cloud-native)
- Could serve as admin/operator signing device for Gateway

---

## 4. Bitcoin-Native Signing Infrastructure

### 4.1 BDK (Bitcoin Dev Kit) + FROST

| Attribute | Detail |
|-----------|--------|
| **Repo** | `bitcoindevkit/bdk` |
| **Language** | Rust |
| **Features** | Wallet, PSBT, coin selection, transaction building |
| **FROST Integration** | BDK + ZF FROST demonstrated (Blockchain Commons 2025) |
| **License** | MIT / Apache 2.0 |

**Ethos Alignment: STRONG** ✅
- Rust-native
- Bitcoin-only focus
- PSBT-based (hardware wallet compatible)
- MIT/Apache 2.0
- Already demonstrated FROST signing with PSBT

### 4.2 Libsecp256k1 (Bitcoin Core)

| Attribute | Detail |
|-----------|--------|
| **Repo** | `bitcoin/bitcoin` (secp256k1 module) |
| **MuSig2** | ✅ Merged (BIP 327) |
| **FROST** | Under active development |
| **Language** | C with Rust bindings (rust-secp256k1) |

**Ethos Alignment: STRONG** ✅
- Bitcoin reference implementation
- Maximum security audit attention
- FROST support coming natively

### 4.3 DLC (Discreet Log Contracts) Infrastructure

| Attribute | Detail |
|-----------|--------|
| **Key Projects** | `p2pderivatives/rust-dlc`, `Crypt-iQ/dlcdevkit` |
| **Language** | Rust |
| **Conxian Status** | Structural DTOs exist, CET signing needs implementation |
| **Oracle Network** | Kormir (Lloyd Fournier), P2P derivatives oracles |

**Ethos Alignment: STRONG** ✅
- Bitcoin-native financial contracts
- Rust ecosystem
- Non-custodial by design
- Synergistic with FROST for oracle attestation aggregation

---

## 5. Cross-Chain Signing & Bridging

### 5.1 CCTP (Circle) — ALREADY MODELED

| Attribute | Detail |
|-----------|--------|
| **Conxian Module** | `cctp.rs` (structural DTOs) |
| **Protocol** | Native USDC burning/minting (not wrapped) |
| **Chains** | Ethereum, Solana, Arbitrum, Noble, OP, Base, Polygon |
| **Signing** | Circle's proprietary attestation service |

**Ethos Alignment: MODERATE** ⚠️
- Centralized attestation (Circle controls minting)
- USDC-only
- Already modeled in Conxian at boundary level

### 5.2 Wormhole — ALREADY MODELED

| Attribute | Detail |
|-----------|--------|
| **Conxian Status** | Listed in Rails (AGENTS.md) |
| **Guardian Network** | 19 validators (PoA) |
| **Signing** | Guardian quorum (2/3 threshold) |

**Ethos Alignment: WEAK** ❌
- 19-guardian PoA (centralized trust)
- Not Bitcoin-native
- Multiple bridge exploits (2022: $326M)

### 5.3 NTT (Noble Token Transfer) — ALREADY MODELED

Noble-native USDC routing. Similar to CCTP but Cosmos/IBC-native.

---

## 6. Research Papers & Academic Foundations

### Key Papers

| Paper | Authors | Year | Relevance |
|-------|---------|:----:|-----------|
| **FROST** (ePrint 2020/852) | Chelsea Komlo, Ian Goldberg | 2020 | Foundation of FROST threshold signing |
| **MuSig2** (BIP 327) | Nick, Ruffing, Seurin, Wuille | 2022 | n-of-n multisignature for Bitcoin |
| **ChillDKG** (BIP Draft) | Komlo, et al. | 2024 | Distributed key generation for FROST |
| **CGGMP21** | Canetti, Gennaro, Goldfeder, Makriyannis, Peled | 2021 | Proactive threshold ECDSA |
| **ROAST** | Ruffing, et al. | 2022 | Robust Asynchronous Schnorr Threshold Signatures |
| **FROST-BIP340** (BIP Draft) | Siv2r | 2024-2025 | FROST signing for Bitcoin Taproot |

### Key Implementations Referenced

| Library | Language | Ciphersuite | License |
|---------|----------|-------------|---------|
| `ZcashFoundation/frost` | Rust | secp256k1 | MIT/Apache 2.0 |
| `LLFourn/frost-secp256k1` | Rust | secp256k1 | MIT |
| `entropyxyz/synedrion` | Rust | ECDSA (CGGMP21) | AGPL-3.0 |
| `cmdruid/frost` | TypeScript | BIP-340 | MIT |
| `bitcoin/bitcoin` (secp256k1) | C | Schnorr/MuSig2 | MIT |
| `musig2` crate | Rust | secp256k1 | MIT |

---

## 7. Ethos Alignment Scoring Matrix

Scoring: 🟢=Strong 🟡=Moderate 🔴=Weak/Incompatible

| Partner/Solution | Sovereign | Non-Custodial | BTC-Native | Rust-Native | License | Production | **Score** |
|------------------|:---------:|:------------:|:----------:|:-----------:|:-------:|:----------:|:---------:|
| **ZF FROST** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 MIT | 🟢 Mainnet | **🟢 6/6** |
| **BIP-FROST Signing** | 🟢 | 🟢 | 🟢 | 🟡 Python | 🟢 BIP | 🟡 Draft | **🟢 5/6** |
| **BDK + FROST** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 MIT | 🟢 Mainnet | **🟢 6/6** |
| **Lit Protocol** | 🟢 | 🟢 | 🔴 | 🔴 JS | 🟢 Open | 🟢 Mainnet | **🟡 4/6** |
| **Entropy** | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 AGPL | 🟡 Testnet | **🔴 3/6** |
| **Threshold Network** | 🟢 | 🟢 | 🔴 | 🟡 | 🔴 GPL | 🟢 Mainnet | **🟡 3/6** |
| **Coinbase FROST** | 🔴 | 🟡 | 🟢 | 🟡 | 🔴 Proprietary | 🟢 Internal | **🔴 2/6** |
| **GCP Confidential** | 🔴 | 🟢 | 🟡 | 🔴 | 🔴 Proprietary | 🟢 GA | **🔴 2/6** |
| **Azure Confidential** | 🔴 | 🟢 | 🟡 | 🔴 | 🔴 Proprietary | 🟡 Preview | **🔴 1/6** |
| **Ledger HSM** | 🟢 | 🟢 | 🟢 | 🔴 JS | 🟡 Proprietary | 🟢 Mainnet | **🟡 4/6** |
| **Wormhole** | 🔴 | 🔴 | 🔴 | 🟡 | 🟢 Open | 🟢 Mainnet | **🔴 1/6** |

---

## 8. Recommendation: Tiered Signing Architecture

### Tier 1 — Bitcoin-Native Sovereign Core (PRIMARY)

```
FROST (ZF Frost) + MuSig2 (already implemented) + secp256k1
     │
     ├── Nexus: FROST threshold signing (distributed key shares)
     ├── Gateway: MuSig2 n-of-n + FROST t-of-n for settlement rails
     └── Enclave SDK: FROST boundary → ZF FROST crypto backend
```

**Action:** Integrate `ZcashFoundation/frost` (secp256k1) into conxius-enclave-sdk.
Replace `ProtocolUnsupported` stubs with real cryptographic execution.
Estimated effort: 2-4 weeks (boundary already complete).

### Tier 2 — Cross-Chain Signing (SECONDARY)

```
Lit Protocol (Naga mainnet)
     │
     ├── Gateway: EVM/Solana/Cosmos transaction signing
     └── Cross-chain intents: programmable signing policies
```

**Action:** Evaluate Lit SDK for Gateway cross-chain signing on non-Bitcoin chains.
Use Conxian's `chain_abstraction.rs` as the integration layer.
Lit signs non-Bitcoin; Conxian's FROST/MuSig2 signs Bitcoin.

### Tier 3 — Hardware / TEE (ALREADY INTEGRATED)

```
AWS Nitro (cloud) + Android StrongBox (mobile)
     │
     ├── Nexus: Nitro-attested signing enclave
     ├── Gateway: Nitro for ISO 20022 signing
     └── Wallet: StrongBox for Android key protection
```

**Action:** Production qualification only — code is complete. Needs AWS account + Android hardware.

### Tier 4 — Enterprise HSM (OPERATIONAL)

```
Ledger Vault / YubiKey
     │
     └── Gateway: Admin/operator transaction approval
```

**Action:** Optional. For Gateway admin operations where physical HSM adds security theater value for enterprise clients.

---

## 9. Immediate Next Steps

| Priority | Action | Effort | Impact |
|:--------:|--------|:------:|:------:|
| **P0** | Integrate `ZcashFoundation/frost` (secp256k1) into enclave-sdk | 2-4 weeks | Closes #1 signing gap |
| **P0** | AWS account for Nitro production qualification | 1 day | Unblocks Gate 4 attestation |
| **P1** | BDK + FROST PSBT signing demo (wallet integration) | 1-2 weeks | Wallet mainnet readiness |
| **P1** | Evaluate Lit SDK for cross-chain Gateway signing | 1 week | Multi-chain coverage |
| **P2** | ChillDKG integration for distributed key generation | 2-4 weeks | Removes trusted dealer assumption |
| **P2** | Monitor BIP-FROST standardization progress | Ongoing | Standards alignment |
| **P3** | Ledger integration for Gateway admin signing | 1-2 weeks | Enterprise HSM option |

---

## 10. What NOT To Do

| Anti-Pattern | Why |
|--------------|-----|
| ❌ Entropy integration | AGPL-3.0 license incompatible with commercial model |
| ❌ Threshold Network | GPL-3.0 license; ECDSA-only, no FROST |
| ❌ Wormhole | Centralized 19-guardian trust; $326M exploit history |
| ❌ Azure/GCP TEE | Vendor lock-in; less mature than Nitro |
| ❌ Coinbase FROST | Proprietary, not available as library |

---

*This research was conducted by an AI agent (OpenHands) as part of Session 52.5.3.
All findings cross-referenced against Conxian's codebase ground truth (enclave-sdk lib.rs,
frost.rs, musig2.rs, nitro.rs).*
