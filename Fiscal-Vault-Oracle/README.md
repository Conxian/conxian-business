# Fiscal Vault Oracle

> Current workspace release: **v1.8.2** (see [`CHANGELOG.md`](../CHANGELOG.md))

The **Fiscal Vault Oracle** is the autonomous financial engine of the Conxian Business Operations System (BOS). It powers the **OpenClaw** engine, which manages the Bitcoin treasury and debt issuance with hardware-attested security.

## Purpose

- **Treasury Rebalancing**: Automated rebalancing of sBTC yield against institutional LSEG pricing.
- **Debt Issuance**: Orchestrating Bitcoin-native DLC Bonds and settlement.
- **State Persistence**: Committing regulatory-shielded state to the global BOS state machine.

## Key Components

- **OpenClaw Engine**: TEE-enclosed execution environment for financial logic.
- **[BOS Integration Map](./BOS_INTEGRATION_MAP.md)**: Detailed mapping of state transitions and triggers.
- **[Bitcoin Bond Specification](./BITCOIN_BOND_DLC.json)**: JSON schema for DLC-based debt instruments.

## DLC Bond principal custody model

The DLC bond lifecycle contract (`dlc-bond.clar`) defaults to a **fully-collateralized** model:

- `subscribe` escrows principal sBTC into the contract.
- `redeem` returns principal sBTC from the contract once matured (or earlier if defaulted).

This design keeps redemptions solvent on-chain, but it also means there is no implicit "capital formation" drawdown.

For cases where principal must leave the contract (e.g., executor-controlled deployment), `dlc-bond.clar` supports an **opt-in** principal drawdown mode that must be enabled *before issuance* via `enable-principal-drawdown`. In that mode, the issuer can draw down principal while the bond is paused (`active = false`) via `drawdown-principal`.

If `principal-drawdown-enabled` is set and the oracle declares default, `redeem` switches to a recovery path that pays out the remaining in-contract sBTC **pro-rata** (and disables coupon claiming in that state). Since payouts are integer-based, very small positions may need to consolidate before redeeming.

## Guardrails

- **50bps Pricing Constraint**: Rebalancing logic must remain within 50bps of institutional data.
- **144-Block Time-Lock**: All debt issuance state changes require Bitcoin-level finality.

## Governance

This module is part of the Conxian Sovereign Autonomous Business (SAB).

See [`GOVERNANCE.md`](../GOVERNANCE.md) for CONTRIBUTING, SECURITY, and LICENSE.

---
🛡️ **Sovereign Autonomous Business (SAB)**. © 2026 Conxian-Labs. Powered by Bitcoin.
