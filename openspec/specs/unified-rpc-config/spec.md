# Unified RPC Configuration Contract (v1)

This document defines a minimal, machine-consumable configuration contract for Conxian RPC routing.

It captures the approved packaging decisions from https://linear.app/conxian-labs/issue/CON-457:

- Personas are tiers (not separate codebases): Home = `Public-Only`, Retail = `Mixed`, Enterprise = `Sovereign-First`.
- Add-ons are optional packs (extensible catalog).
- Default posture is remote RPC first, with a unified configuration screen to override endpoints / strategy.

## 1. Goals

1. Define a minimal schema for `rpcStrategy` + endpoint overrides + add-on toggles.
2. Keep it 1:1 mappable to the current env surface so it can drive `.env` generation without surprises.

## 2. Contract format

- Shape: JSON
- JSON Schema: `rpc-config.v1.schema.json`
- Schema identifier: `conxian.rpc-config.v1`

### 2.1 Example (Home / open tier)

```json
{
  "schema": "conxian.rpc-config.v1",
  "rpcStrategy": "Public-Only",
  "bitcoin": {
    "rpcUrl": "https://bitcoin-rpc.publicnode.com"
  },
  "stacks": {
    "gatewayRpcUrl": "https://api.mainnet.hiro.so",
    "nodeRpcUrl": "https://api.mainnet.hiro.so"
  },
  "addOns": {
    "bisq": { "enabled": false },
    "rgb": { "enabled": false },
    "bitvm": { "enabled": false }
  }
}
```

## 3. Field-to-env mapping (v1)

The contract is designed so `.env` generation is a straightforward projection.

### 3.1 Core routing

| Config field | Env var | Consumer |
| :--- | :--- | :--- |
| `bitcoin.rpcUrl` | `BITCOIN_RPC_URL` | `conxian-gateway` |
| `bitcoin.rpcAuth.user` | `BITCOIN_RPC_USER` | `conxian-gateway` |
| `bitcoin.rpcAuth.pass` | `BITCOIN_RPC_PASS` | `conxian-gateway` |
| `stacks.gatewayRpcUrl` | `STACKS_RPC_URL` | `conxian-gateway` |
| `stacks.nodeRpcUrl` | `STACKS_NODE_RPC_URL` | `conxian-nexus` |

Notes:

- If a field is omitted, the consuming service’s built-in default applies.
- If `bitcoin.rpcAuth` is present, both `user` and `pass` are required.

### 3.2 Add-on packs

Known packs in v1: `bisq`, `rgb`, `bitvm`.

| Pack | Config field | Env var | Consumer |
| :--- | :--- | :--- | :--- |
| `bisq` | `addOns.bisq.rpc.host` | `BISQ_RPC_HOST` | `conxius-platform` |
| `bisq` | `addOns.bisq.rpc.port` | `BISQ_RPC_PORT` | `conxius-platform` |
| `rgb` | `addOns.rgb.rpc.host` | `RGB_RPC_HOST` | `conxius-platform` |
| `bitvm` | `addOns.bitvm.rpc.host` | `BITVM_RPC_HOST` | `conxius-platform` |

For future packs, env var names **SHOULD** follow the convention:

- `addOns.<pack>.rpc.host` → `<PACK>_RPC_HOST`
- `addOns.<pack>.rpc.port` → `<PACK>_RPC_PORT` (optional)

Where `<PACK>` is the `addOns` key uppercased, with non-alphanumeric characters replaced by `_`.
