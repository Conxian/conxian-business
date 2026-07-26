# Fiscal Vault Oracle

> **Classification:** Supporting · Public-safe
> **Operating label:** Reference implementation
> **Maturity / claim state:** Incubating; protocol/reference interfaces are **Implemented** where code evidence exists, while broader orchestration remains **Target-state**.
> **Doctrine boundary:** This repository describes a protocol/reference oracle and policy surface. It is not a Conxian-Labs custodian, company treasury, discretionary fund controller, market operator, or user-data extraction system.

> Current workspace release: **v1.9.2** (see [`CHANGELOG.md`](../CHANGELOG.md))

The **Fiscal Vault Oracle** is a public reference surface for policy coordination, oracle inputs, and contract-level financial state in the Conxian Business Operations System (BOS). Detailed operational, vendor, legal, and financial strategy material remains in the authorized Linear workspace under ZSE.

## Purpose

- Describe protocol- or participant-defined policy constraints and oracle interfaces.
- Keep public specifications separate from internal operational material.
- Make contract behavior and evidence boundaries explicit without implying company custody or managed funds.

## Status

**Incubating** — public-safe interfaces and constraints are documented for reference; deployment, production enforcement, and any value-bearing capability require their own evidence and gates.

## Canonical documentation

- [Doctrine Alignment Standard](../docs/DOCTRINE_ALIGNMENT_STANDARD.md)
- [Portfolio Doctrine Register](../docs/PORTFOLIO_DOCTRINE_REGISTER.md)
- [Documentation Alignment Index](../docs/DOCUMENTATION_ALIGNMENT_INDEX.md)
- [Repo portfolio](../docs/REPO_PORTFOLIO.md)
- [Portfolio business-unit map](../docs/PORTFOLIO_BUSINESS_UNIT_MAP.md)

## Key components

- **[BOS integration map](./BOS_INTEGRATION_MAP.md)**
- **[Bitcoin bond details](./BITCOIN_BOND_DLC.json)**

## Protocol-level principal handling

The `dlc-bond.clar` lifecycle contract models fully collateralized principal handling. The words “escrow”, “redeem”, “drawdown”, and “default” describe state transitions enforced by the contract and the choices of its participants. They do not mean that Conxian-Labs receives, custodies, or exercises discretionary control over the principal.

- `subscribe` escrows principal sBTC into the contract.
- `redeem` returns principal sBTC from the contract once matured, or earlier if the contract enters its documented default path.

For cases where principal must leave the contract (for example, executor-controlled deployment), `dlc-bond.clar` supports an **opt-in** principal drawdown mode enabled before issuance via `enable-principal-drawdown` (one-shot; errors if already enabled). In that mode, the issuer can draw down principal via `drawdown-principal` only while:

- `active = false`
- `defaulted = false`
- `coupon-index = 0`
- `burn-block-height < next-coupon-height`

Drawdowns are capped in aggregate at the current `dlc-bond` total supply; remaining drawdown capacity is `get-principal-drawdown-capacity`. Returning sBTC to the contract does not increase remaining drawdown capacity.

If the oracle does not declare default, the issuer or executor must restore sufficient sBTC liquidity to the contract before maturity for `redeem` to succeed. If `principal-drawdown-enabled` is set and the oracle declares default, `redeem` switches to the documented recovery path that pays remaining in-contract sBTC pro rata and disables coupon claiming in that state.

Because payouts are integer-based, very small positions may need to consolidate before redeeming. These are contract semantics, not a company promise or investment service.

## Governance

This module is part of the public BOS reference surface. See [`GOVERNANCE.md`](../GOVERNANCE.md) for contribution, security, and license expectations.
