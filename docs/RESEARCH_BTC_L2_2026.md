# Bitcoin L2 Ecosystem Research — 2026 Mapping

> Generated: Session 47, Aug 2026
> Source: Tavily deep research across bitcoinlayers.org, Stacks blog, Spark Research, CoinGecko, Bitcoin Foundation

## Ecosystem Coverage Matrix

### State Channels (T1 Strict)

| Protocol | SDK Coverage | Core Types | Gateway Adapter | TVL/Activity |
|----------|-------------|------------|-----------------|--------------|
| Lightning Network | enclave-sdk (lightning.rs) | lib-conxian-core (LightningAdapter) | gateway (lightning.rs) | Millions tx/day |

### ZK Rollups on Bitcoin (T1 Strict)

| Protocol | SDK Coverage | Notes |
|----------|-------------|-------|
| Citrea | enclave-sdk (bitvm.rs) | BitVM2 via proof verification |
| Merlin Chain | NOT COVERED | EVM ZK-rollup, oracle-based DA to Bitcoin |
| SatoshiVM | NOT COVERED | EVM ZK-rollup, sidechain architecture |

### Federated Sidechains (T2 Managed)

| Protocol | SDK Coverage | Core Types | Gateway Adapter |
|----------|-------------|------------|-----------------|
| Liquid Network | enclave-sdk (bitcoin liquid_adapter) | lib-conxian-core | gateway |
| Rootstock (RSK) | Gateway adapter | — | gateway (81% hash power merge-mined) |
| Fedimint | enclave-sdk (nexus/fedimint) | lib-conxian-core | gateway (wired Session 47) |

### Smart Contract Layers (T2 Managed)

| Protocol | SDK Coverage | Core Types | Nexus Executor |
|----------|-------------|------------|----------------|
| Stacks | enclave-sdk (stacks.rs) | lib-conxian-core | stacks executor |
| Botanix (Spiderchain) | NOT COVERED | — | EVM-compatible, decentralized multisig |
| Bitlayer | NOT COVERED | — | EVM-compatible, BitVM bridge |

### Virtual UTXOs / Statechains (T2 Managed)

| Protocol | SDK Coverage | Notes |
|----------|-------------|-------|
| Ark | enclave-sdk (ark.rs) | VTXO protocol, ASP model |
| Spark | NOT COVERED | New protocol (2025), self-custody, Ark-like |

### Cross-chain / Staking (T3 Expedient)

| Protocol | SDK Coverage | Notes |
|----------|-------------|-------|
| Babylon | enclave-sdk (indirect) + lib-conxian-core (StakingIntent) | BTC staking, T2 managed |
| Hemi | NOT COVERED | EVM + Bitcoin state embedding |

### EVM Bridges (Not Directly Relevant — covered by ethereum.rs abstraction)

| Protocol | Via |
|----------|-----|
| Starknet (strkBTC) | enclave-sdk ethereum.rs |
| Arbitrum, Optimism, Base | enclave-sdk ethereum.rs |

## Coverage Summary

- **Fully Covered:** 10 protocols (Lightning, Stacks, Rootstock, Liquid, RGB, BitVM2/Citrea, DLC, Ark, Fedimint, Babylon)
- **Partially Covered:** 0
- **Not Covered:** 5 protocols (Merlin Chain, SatoshiVM, Botanix/Spiderchain, Bitlayer, Spark, Hemi)
- **Not Needed (EVM-native):** Starknet, Arbitrum, Optimism, Base — handled by EVM bridge abstraction

## Action Items

| Priority | Protocol | Action |
|----------|----------|--------|
| P1 | Spark | Research protocol; if Ark-compatible, minimal SDK work needed |
| P2 | Botanix/Spiderchain | Monitor TVL growth; evaluate if EVM bridge suffices |
| P3 | Merlin, SatoshiVM, Bitlayer, Hemi | EVM-compatible L2s; ethereum.rs bridge likely sufficient |

## Reference

- bitcoinlayers.org — authoritative L2 research
- L2Beat — Ethereum L2 framework (trust model analysis)
- Spark Research — 2026 comprehensive landscape
