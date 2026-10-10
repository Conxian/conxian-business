# Billing Unification Design (issue #1343)

Status: proposal — implementation pending owner sign-off on tier changes.

## Problem

Four surfaces compute money four different ways with no shared source of truth:

| Surface | Scheme | Unit | Where |
|---|---|---|---|
| Gateway (managed) | $200/mo + $0.01 relay + $0.05 RWA + $0.10 settlement | USD cents | `conxian-gateway/internal/engine/src/billing.rs` |
| labs-site | mirrors gateway ($200/mo + per-op) | USD | `conxian-labs-site/server.js` |
| Nexus | Free/Pro/Enterprise by signature quota; one-time 100k sats (Pro) / 1M sats (Enterprise) | sats | `conxian-nexus/src/api/billing/mod.rs` |
| Market | per-settlement `TrustTier` fee bps (ADR-004 dynamic floor) | bps | `conxian_market/src/fee_calculator.ts` |

## Verified gaps

1. No linkage between a paid managed-gateway subscription and nexus `SubscriptionTier` — a gateway customer paying $200/mo is not recognised as `Pro`/`Enterprise` anywhere.
2. `SubscriptionTier::enterprise_fee_cap()` exists in nexus (G5) but has **no consumer in the gateway**.
3. Three disjoint "sources of truth" — gateway cents, nexus sats, market bps — can drift silently (already happened once: labs-site $99 vs billing.rs $200).

## Proposal — one canonical billing model + conformance binding

Reuse the pattern already proven for the fee model (ADR-004 / `fixtures/fee_conformance.json`): define one canonical JSON spec that every surface reads, and a single Rust `BillingTier` type that maps subscription tier -> gateway allowances.

### 1. Canonical spec (`billing_conformance.json`)

A single versioned JSON doc (living in `conxian-business` as the governance CNS) that declares:

- subscription tiers and their **monthly price + included allowances** (relay/RWA/settlement),
- per-operation unit prices (USD cents),
- enterprise volume discount threshold + bps,
- the nexus -> gateway tier mapping (Free/Pro/Enterprise -> managed allowances).

### 2. Single Rust source of truth

Move the price constants out of `billing.rs` into a shared, versioned module (or extend `lib-conxian-core`) that both gateway and nexus depend on, so the constants cannot diverge.

### 3. Linkage

- Gateway `compute_mrr` accepts a `SubscriptionTier` (mapped via the canonical spec) and applies `enterprise_fee_cap` when the customer holds an Enterprise subscription (committed 1M sats/mo) — closing gap 2.
- Market `TrustTier` fee bps stays settlement-priced (it is a per-settlement protocol fee, a different category), but is declared in the same canonical spec so the three stay auditable in one place.

## Concrete change list

1. Add `billing_conformance.json` to `conxian-business` (this doc's companion) + a drift-check CI step (`verify_billing_conformance.py`) that fails when any surface's constants disagree.
2. Gateway: consume `SubscriptionTier` + `enterprise_fee_cap` in `compute_mrr`; read prices from the canonical spec instead of hardcoded consts.
3. labs-site: read the same spec (single JSON fetch) instead of hand-edited `server.js` constants.
4. Nexus: expose the tier->gateway mapping; no price change to the sats-based upgrade (that is a separate, owner-gated decision).

## Not in scope (owner sign-off required)

- Tier *price* changes (e.g. Indie $29/$99 entry tier) — separate decision, see `docs/MANAGED_GATEWAY_PRICING_RESEARCH.md`.
- x402 no-subscription path (market #159).
- MoR webhook / dunning (gateway #507) — billing *collection*, not *definition*.

## Reference

- `docs/MANAGED_GATEWAY_PRICING_RESEARCH.md` (pricing research)
- `docs/TURNKEY_SELF_SERVE_GAP_ANALYSIS.md` (funnel map)
- `conxian_market/docs/adr/ADR_004_DYNAMIC_FEE_FLOOR_MODEL.md` (fee conformance pattern)
