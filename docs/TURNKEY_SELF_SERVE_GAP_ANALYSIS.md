# Turnkey / Self-Serve Service Gap Analysis

> Status: audit + implementation plan (2026-10-10)
> Scope: end-to-end managed SaaS gateway — onboarding → payment → provisioning → deploy → metering → enforcement → dunning
> Method: read-only audit across `conxian-labs-site`, `conxian-gateway`, `conxian_market`, `conxian-nexus`.

## Verdict

The managed SaaS gateway is currently a **documented design + a thin env-based auth layer**, not a
turnkey product. There is no executable path from `signup → pay → provision key → deploy → meter →
enforce → dunning`. The billing webhook handler, Neon-backed key store, deployment pipeline, and
usage metering are all absent/unwired.

## End-to-end funnel — status matrix

| Funnel step | Status | Where it breaks |
|-------------|--------|-----------------|
| Signup | Partial | `labs-site server.js:148-173` validates email+tier only; no account/tenant record. |
| Pay (card/MoR or x402) | **Missing** | No MoR webhook handler (only `gateway/docs/MANAGED_SAAS_BILLING_WEBHOOK.md`); `MERCHANT_CHECKOUT_URL` unset; x402 pointer `$conxian.com/market/subscription/managed` does not exist; demand amount hardcoded `"0"`; nexus `/verify-payment` fakes settlement (`mod.rs:540-590`). |
| Auto-provision key/tenant | **Missing** | `TenantKeyRegistry` reads `MANAGED_API_KEYS` env only (`tenant.rs:158-187`); `migrations/0001_managed_api_keys.sql` has no runner (no `sqlx`/postgres). |
| Deploy gateway | **Missing** | Managed code on `dev`/`staged`, not `main`; no `gateway-cloud-run.yml`; `render.yaml` (dev) not wired to a pipeline. |
| Metered billing | Unwired | `compute_mrr` (`billing.rs:160-235`) is a pure calculator, no route, no usage feed. |
| Usage/quota enforcement | Partial | Only fixed-window requests/min (`rate_limit.rs:41-63`, default 120); no monthly volume/tier quota. |
| Dunning/expiry | **Missing** | No revoke/expire/payment-failed handler; keys never expire; JWT `exp` optional. |

## Highest-leverage gaps (close first)

1. **MoR webhook handler (mint/rotate/revoke) + Neon loader** — currently only a doc and an orphan DDL.
2. **Wire Neon (`sqlx`/`tokio-postgres`) into `TenantKeyRegistry`** — stop treating env as source of truth.
3. **Real subscription payment-pointer + verification in `conxian_market`** (or fix `server.js:144/166`).
4. **Fix nexus `/verify-payment`** to fail-closed (no real Lightning proof = reject), and unify the 3 disjoint pricing schemes (gateway `$200/mo` cents vs nexus `free/pro/enterprise` sats vs market fee-bps).
5. **Promote managed-SaaS files to `main`** + add a real deploy workflow (cloud-run/render) that also runs migrations.

## Three disjoint billing systems (must unify)

| Surface | Scheme | Source |
|---------|--------|--------|
| Gateway | $200/mo + $0.01/$0.05/$0.10 per-op (cents) | `billing.rs:30-39` |
| labs-site | $200/mo + per-op USD (now matches gateway) | `server.js:127-130` |
| Nexus | free/pro/enterprise by signatures; one-time 100k/1M sats | `mod.rs:98-99` |
| Market | per-settlement `TrustTier` fee bps | `trust_tier_middleware.ts` |

There is no linkage between a paid "managed gateway" subscription and nexus `SubscriptionTier`,
and no `enterprise_fee_cap` consumer in the gateway. Nexus `TrustTier` `Managed` (attestation tier)
is a different concept from the gateway `"managed"` SaaS tier.

## Positioning mismatch (live)

`labs-site pricing/index.html` disclaims a self-serve price/ledger/endpoint (lines 88, 110, 531, 563),
while `server.js:127` advertises a fixed `$200/mo` and `:131` a public endpoint. The two pages tell
the buyer opposite stories.

## Implementation plan (prioritized)

- [x] Pricing benchmark + hybrid-option recommendation (`docs/MANAGED_GATEWAY_PRICING_RESEARCH.md`, PR #1342).
- [ ] Fail-closed nexus `/verify-payment` (reject without real Lightning proof) — security.
- [ ] Fix labs-site pricing page ↔ server.js positioning mismatch.
- [ ] Reconcile stale repo inventory (`conxius-platform/docs/REPOSITORY_TAXONOMY.md` ghost repos).
- [ ] MoR webhook handler + Neon loader (needs MoR creds + Neon wiring).
- [ ] Real x402 subscription pointer + non-zero demand (market).
- [ ] Deploy workflow + promote managed files to main (needs Render/Cloudflare creds).

## Gated items (external resources)

- Gateway deploy (#466): Render/Cloudflare prod credentials.
- MoR integration: Lemon Squeezy/Paddle credentials + webhook URL.
- Enclave P0s (#202/#240/#241): independent crypto review + real-device evidence.
- Org 2FA: org-owner action (Free-plan restricted).
