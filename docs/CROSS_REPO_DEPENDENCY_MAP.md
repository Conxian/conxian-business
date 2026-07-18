# Conxian Cross-Repo Dependency Map
> **Purpose**: Document dependencies between Conxian ecosystem repositories
> **Generated**: 2026-07-14
> **Version**: 1.0.0

---

## 1. Dependency Overview

### 1.1 Authority Chain (Upstream → Downstream)

```
Protocol (Conxian)
    ↓
Nexus (conxian-nexus) ──→ State verification, ZK proofs
    ↓
Gateway (conxian-gateway) ──→ ISO 20022 bridge, compliance
    ↓
Wallet/UI (conxius-wallet, conxian-ui) ──→ User-facing surfaces
    ↑
Platform (conxius-platform) ──→ Local orchestration
```

### 1.2 Shared Dependencies

```
lib-conxian-core (REPO-007)
    ├── conxian-nexus ──→ Crypto primitives, ZKC, SYI
    ├── conxian-gateway ──→ Crypto primitives
    └── conxian-market ──→ ZK compliance primitives
```

---

## 2. Repository Dependency Matrix

| Consumer → | Protocol | Nexus | Gateway | Wallet | Platform | Enclave SDK | Core | Market |
|------------|:--------:|:-----:|:-------:|:------:|:--------:|:----------:|:----:|:------:|
| **conxian-business** | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| **conxian-nexus** | ✅ | - | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| **conxian-gateway** | ⬜ | ✅ | - | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| **conxius-wallet** | ⬜ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ |
| **conxian-ui** | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| **conxius-platform** | ✅ | ✅ | ✅ | ✅ | - | ⬜ | ✅ | ✅ |
| **conxius-enclave-sdk** | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | - | ✅ | ✅ |
| **conxian-market** | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - |

**Legend**:
- ✅ = Direct dependency
- ⬜ = No direct dependency
- Protocol = Conxian/ (on-chain contracts)

---

## 3. Market Integration Dependencies

### 3.1 Market → Nexus (State Verification)

```yaml
conxian-market:
  depends_on:
    conxian-nexus:
      - ZK-proof verification for escrow
      - Glass Node state for payout verification
      - Cross-chain finality confirmation
  contract: nexus-state-verifier.clar
  api_endpoint: /api/v1/zk-proof/verify
```

### 3.2 Market → Gateway (Settlement Rails)

```yaml
conxian-market:
  depends_on:
    conxian-gateway:
      - ISO 20022 settlement egress
      - Fedimint adapter (CON-1389)
      - Citrea adapter (CON-1389)
      - External DeFi integration (ALEX, Uniswap)
  contract: gateway-settlement-bridge.clar
  api_endpoint: /api/v1/settlement/execute
```

### 3.3 Market → Wallet (User Settlement)

```yaml
conxian-market:
  depends_on:
    conxius-wallet:
      - BYOK key management
      - Transaction signing
      - Balance verification
  sdk: @conxius/enclave-sdk
  api_endpoint: /api/v1/wallet/sign
```

### 3.4 Market → Platform (Builder Sandbox)

```yaml
conxian-market:
  depends_on:
    conxius-platform:
      - Developer sandbox (CON-1437)
      - Local stack for testing
      - TTFV < 15 mins onboarding
  container: conxius-platform:latest
  endpoint: /api/v1/sandbox/spawn
```

### 3.5 Market → lib-conxian-core (Crypto Primitives)

```yaml
conxian-market:
  depends_on:
    lib-conxian-core:
      - ZKC (Zero-Knowledge Compliance) primitives
      - SYI (Sovereign Yield Index) calculations
      - BitVM2 SNARK proof verification
  crate: lib_conxian_core
  version: ">=0.2.0"
```

---

## 4. Critical Path Dependencies

### 4.1 Revenue Capture Path (BLOCKED)

```
Market (CON-1427) → Nexus (fee routing) → Gateway (settlement)
         ↓
    CON-1427: Fee collection is a no-op
    CON-1425: CXD stablecoin lacks peg
```

### 4.2 Builder Onboarding Path (IN PROGRESS)

```
Market (CON-1437) → Platform (sandbox) → Enclave SDK (BYOK)
         ↓
    CON-1437: Developer Sandbox pending
    CON-1440: @conxian/sdk not published
```

### 4.3 Sovereign Compliance Path (PENDING)

```
Market → Gateway (ISO 20022) → Nexus (ZK proofs) → Core (ZKC)
         ↓
    CON-1389: Fedimint/Citrea adapters incomplete
    CON-1439: DAO governance transition pending
```

---

## 5. Dependency Validation

### 5.1 Check Script

```bash
# Verify all Market dependencies are available
python3 scripts/verify_market_integration.py
```

### 5.2 Expected Outputs

| Dependency | Status | Blocker |
|------------|--------|--------|
| conxian-nexus | ✅ Available | None |
| conxian-gateway | ⚠️ Partial | Fedimint/Citrea missing |
| conxius-wallet | ⚠️ Private | SDK not published |
| conxius-platform | ✅ Available | Sandbox pending |
| lib-conxian-core | ✅ Available | None |

---

## 6. Integration Test Matrix

| Test Case | Source | Target | Status |
|-----------|--------|--------|--------|
| ZK-Proof Generation | conxian-market | lib-conxian-core | ✅ |
| Escrow Verification | conxian-market | conxian-nexus | ✅ |
| Settlement Egress | conxian-market | conxian-gateway | 🔴 |
| BYOK Signing | conxian-market | conxius-wallet | ⚠️ |
| Sandbox Spawn | conxian-market | conxius-platform | ⚠️ |
| Revenue Split | conxian-market | conxian-nexus | 🔴 |

---

## 7. Related Documents

- [BOS Knowledge Framework](BOS_KNOWLEDGE_FRAMEWORK.md) - REPO-008 entry
- [Market Enhancement Strategy](../conxian-market/docs/research/market_enhancement_strategy.md)
- [Org Reality Issue Audit](../conxian-market/docs/research/org_reality_issue_audit.md)
- [Market BOS Integration Research](MARKET_BOS_INTEGRATION_RESEARCH.md)

---

*Maintained by: Conxian-Labs Operations*
*Last updated: 2026-07-14*
