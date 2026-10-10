# Billing & Pricing Strategy — Compete & Grow Fast (issue #1343)

Status: proposal — implementation pending owner sign-off on tier changes.

## Competitive thesis

The managed gateway is priced at a flat $200/mo entry — mis-priced against the actual buyer
(indie AI-agent developers) and against incumbent benchmarks. Industry (2026):

- Managed API gateways anchor a **$0–$365/mo** base with **$1–$20 per million** unit rates
  (AWS API Gateway $0 base; Kong Konnect ~$105/mo; Apigee ~$365/mo; Zuplo free→sub-$10).
- The indie/solo developer sweet spot is **$9–$29/mo** (individuals) and **$29–$99/mo** (teams).
- **Hybrid (base subscription + metered usage) is the fastest-growing SaaS model in 2026** — the shape
  Vercel/OpenAI/Cursor/LangSmith all converge on.
- **x402 pay-per-use is 0% protocol fees** vs 2–3% on Stripe, making sub-cent micropayments economical
  (CoinGecko precedent: $0.01/call via x402).

**To compete: undercut on entry and win on the crypto-native rail. To grow fast: usage-based with
land-and-expand tiers.** Unification (single source of truth) is the enabler that stops the four
surfaces drifting apart and mis-pricing the product.

## Competitive tier ladder (land-and-expand)

| Tier | Base | Included relay | Overage | Target buyer |
|------|------|----------------|---------|--------------|
| Starter | $0/mo | 1K | — | trial / adoption |
| Indie | $29/mo | 100K | $0.01/relay | indie agent devs |
| Business | $99/mo | 1M | $0.005/relay (volume) | teams |
| Enterprise | committed-use | — | 20–50% discount (true-up) | predictable revenue |

- RWA verification ($0.05) and settlement ($0.10) stay **value-based premiums** — the defensible
  margin, not the volume rail fee.
- Volume tiers reward growth: unit cost falls at scale (mirrors Lightspark 0.50%→0.15%).

## x402 pay-per-use path (acquisition)

- No subscription, no API key, per-call. Attracts the long-tail/experimental devs the $200/mo wall
  excludes; 0% fees keep sub-cent micropayments viable. This is the crypto-native differentiation the
  gateway is otherwise built around.

## Growth levers (why this compounds)

1. **Free tier → land** (developers won't pay before trying).
2. **Usage-based → revenue scales with customer success** automatically.
3. **Volume discounts → retain + grow** (lower unit at scale).
4. **Land-and-expand** free → Indie → Business → Enterprise.
5. **x402 → zero-friction acquisition**, no Stripe fee drag.

## Problem — four disjoint billing surfaces (unification gap)

| Surface | Scheme | Unit | Where |
|---|---|---|---|
| Gateway (managed) | $200/mo + $0.01 relay + $0.05 RWA + $0.10 settlement | USD cents | `conxian-gateway/internal/engine/src/billing.rs` |
| labs-site | mirrors gateway | USD | `conxian-labs-site/server.js` |
| Nexus | Free/Pro/Enterprise by signature quota; one-time 100k/1M sats | sats | `conxian-nexus/src/api/billing/mod.rs` |
| Market | per-settlement `TrustTier` fee bps (ADR-004 dynamic floor) | bps | `conxian_market/src/fee_calculator.ts` |

Verified gaps:
1. No linkage between a paid managed-gateway subscription and nexus `SubscriptionTier`.
2. `SubscriptionTier::enterprise_fee_cap()` (nexus, G5) has **no consumer in the gateway**.
3. Three disjoint sources of truth can drift silently (already happened: labs-site $99 vs billing.rs $200).

## Proposal — one canonical model + conformance binding

Reuse the proven ADR-004 `fee_conformance.json` pattern: one canonical JSON spec every surface
reads, plus a single Rust `BillingTier` type mapping subscription tier → gateway allowances.

1. **Canonical spec** `billing_conformance.json` (lives in `conxian-business`, the governance CNS):
   declares the tier ladder above, per-op unit prices, enterprise discount threshold/bps, and the
   nexus→gateway tier mapping.
2. **Single Rust source of truth**: move price constants out of `billing.rs` into a shared, versioned
   module (or `lib-conxian-core`) both gateway and nexus depend on.
3. **Linkage**: gateway `compute_mrr` accepts a `SubscriptionTier` (mapped via the spec) and applies
   `enterprise_fee_cap` for Enterprise holders. Market `TrustTier` bps stays settlement-priced but is
   declared in the same spec for auditability.

## Concrete change list

1. Add `billing_conformance.json` + a `verify_billing_conformance.py` drift-check CI step.
2. Gateway: consume `SubscriptionTier` + `enterprise_fee_cap` in `compute_mrr`; read prices from the spec.
3. labs-site: read the same spec (single JSON fetch) instead of hand-edited `server.js`.
4. Nexus: expose the tier→gateway mapping.

## Not in scope (owner sign-off required)

- Tier *price* changes themselves (the ladder above is the recommendation; committing the numbers is a
  separate owner-gated decision).
- x402 no-subscription implementation (market #159).
- MoR webhook / dunning (gateway #507) — billing *collection*, not *definition*.

## Reference

- `docs/MANAGED_GATEWAY_PRICING_RESEARCH.md` (industry benchmarks + options A/B/C)
- `docs/TURNKEY_SELF_SERVE_GAP_ANALYSIS.md` (funnel map)
- `conxian_market/docs/adr/ADR_004_DYNAMIC_FEE_FLOOR_MODEL.md` (fee conformance pattern)
