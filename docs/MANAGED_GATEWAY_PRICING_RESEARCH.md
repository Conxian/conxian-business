# Managed Gateway Pricing — Industry Research & Options

> Status: research + recommendation (2026-10-10)
> Scope: `conxian-gateway/internal/engine/src/billing.rs` ↔ `conxian-labs-site/server.js` managed tier
> Supersedes the "$99/mo vs $200/mo" inconsistency (resolved by `a51c5f1` on labs-site).

## 1. Current state

The managed SaaS gateway is priced (both sources now aligned):

| Meter | Rate | Gateway constant |
|-------|------|------------------|
| Base | $200/mo | `MANAGED_GATEWAY_BASE_FEE_CENTS = 20_000` |
| Relay message | $0.01 | `RELAY_MESSAGE_COST_CENTS = 1` |
| RWA verification | $0.05 | `RWA_VERIFICATION_COST_CENTS = 5` |
| Settlement op | $0.10 | `SETTLEMENT_OP_COST_CENTS = 10` |
| Enterprise discount | 20% | `ENTERPRISE_DISCOUNT_BPS = 2000` |

labs-site now declares the billing engine as the single source of truth — correct, but the
*value* of the numbers was never benchmarked against the market. That is the gap this doc closes.

## 2. Industry benchmarks (2026)

### 2.1 Managed API gateways

| Vendor | Model | Entry cost | Unit rate |
|--------|-------|-----------|-----------|
| AWS API Gateway | pure consumption, no base | $0/mo | $1.00/M HTTP, $3.50/M REST |
| Kong Konnect Plus | base + included volume | ~$105/mo (1M req incl.) | ~$200/M overage |
| Apigee (Google) | env base + calls | ~$365/mo base env | $20/M standard, $100/M extensible |
| Zuplo | developer-first, usage | free tier → paid | sub-$10/mo indie tiers |

Takeaway: incumbent managed gateways anchor a **base of $0–$365/mo** with a **unit rate of
$1–$20 per million calls** (≈ $0.000001–$0.00002 per call at the gateway layer).

### 2.2 AI agent / developer platforms (the actual buyer set)

| Platform | Model | Entry |
|----------|-------|-------|
| Vercel AI SDK + Gateway | usage-based | $0/mo → Pro $20/mo + usage |
| LangChain / LangSmith | seat + usage | Plus $39/seat/mo, $0.001/node |
| OpenAI Responses API | pure usage + tool fees | Web search $10/1K calls, file search $2.50/1K queries |
| Cursor | seat + hidden agent limits | $20/mo Pro, $40/user/mo Business |
| eesel AI | flat fee per interaction band | predictable, no token fees |

Takeaway: **hybrid (base subscription + metered usage) is the fastest-growing SaaS model in
2026** and is what mature agent platforms converge on. The billing *unit* should match the
buyer: developers want per-call/per-token, business buyers want subscription + included
credits + overage, enterprise wants committed-usage tiers with true-up.

### 2.3 Indie / solo developer tool pricing

- Sweet spot: **$9–$29/mo individuals, $29–$99/mo teams** (Indie Hackers data).
- Usage-based pricing aligns revenue with value and grows automatically.
- "Do not charge per feature" — price on team size or usage, not feature gates.
- A generous free tier drives adoption (developers won't pay before trying).

### 2.4 x402 / HTTP-402 native payments (the Conxian rail)

- x402's core value proposition is **pay-per-use, no subscriptions, no API keys**.
- Real-world anchor: CoinGecko charges **$0.01/API call via x402** (no registration, no minimum).
- Micropayment floors: ~$0.001 on Base, ~$0.00001 on Lightning (vs ~$0.50 practical floor on cards).
- Protocol fees: 0% (vs 2–3% on Stripe) — which makes sub-cent micropayments economical.

Key tension: the current **$200/mo subscription contradicts the x402 "no subscription" ethos**
that the managed gateway is otherwise built around.

## 3. Options

### Option A — Pure x402 pay-per-use (crypto-native, zero-friction)
No base fee. Metered only: $0.01/relay, $0.05/RWA, $0.10/settlement.
- ✅ Matches x402 "no subscription", CoinGecko precedent, lowest friction for long-tail indie devs.
- ✅ Attracts infrequent/experimental users the $200/mo wall excludes.
- ❌ No committed revenue; revenue is unpredictable; needs volume to cover fixed infra.

### Option B — Hybrid base + usage (the 2026 default; **recommended primary**)
Tiered base with included volume + metered overage + enterprise committed tier.

| Tier | Base | Included relay | Overage |
|------|------|---------------|---------|
| Starter (free) | $0/mo | 1K relay/mo | upgrade |
| Indie | $29/mo | 100K relay/mo | $0.01/relay |
| Business | $99/mo | 1M relay/mo | $0.005/relay (volume) |
| Enterprise | custom | committed | 20–50% discount (true-up) |

- ✅ Predictable base + scalable usage; matches Kong/Vercel/OpenAI/Cursor shape.
- ✅ $29 entry removes the $200 wall for the "indie AI agent developer" target buyer.
- ✅ RWA ($0.05) and settlement ($0.10) stay *value-based* add-ons — the defensible premium.
- ⚠️ Subscription still (mildly) tensions with x402; frame base as "committed credits" if needed.

### Option C — Pure subscription / credit bands (predictable, simple)
Flat fee per interaction band (eesel-style): e.g. $29/mo for N interactions.
- ✅ Predictable budgeting, simplest to sell.
- ❌ Leaves money on the table at scale; doesn't absorb high-variance agent usage.

## 4. Recommendation

**Ship Option B (hybrid) as the primary, with Option A (pure x402) as the crypto-native entry point.**

1. Drop the base from $200/mo to a **$29/mo Indie tier** (and a $0 free tier) — $200/mo is
   mis-priced against the indie-agent buyer and the incumbent benchmark.
2. Keep relay at **$0.01** (already matches CoinGecko); add a volume discount at scale.
3. Keep RWA/settlement as **value-based premiums** (they are the defensible margin, not the rail fee).
4. Expose a **no-subscription x402 metered path** for the pay-per-use ethos.
5. Add **committed-usage enterprise tiers** (the `ENTERPRISE_DISCOUNT_BPS` hook already exists).

### Evidence / sources
- Kong vs AWS vs Apigee 2026: https://tech-insider.org/kong-vs-aws-api-gateway-vs-apigee-2026 ; https://zuplo.com/learning-center/api-gateway-pricing-comparison-2026
- AI agent pricing units + hybrid: https://getlago.com/blog/ai-agent-pricing-usage-based-models ; https://getmonetizely.com/articles/how-do-api-based-and-platform-based-ai-agent-pricing-models-differ
- x402 / HTTP-402 pay-per-use: https://www.dwellir.com/blog/what-is-x402-protocol ; https://x402.org ; https://blog.cloudflare.com/monetization-gateway
- Indie SaaS pricing benchmarks: https://trendgap.io/blog/saas-pricing-strategy-guide ; https://superframeworks.com/articles/micro-saas-ideas-solo-developers

### Next steps
- [ ] Decide A/B/C (recommend B + A).
- [ ] Implement chosen tiers in `billing.rs` + `server.js` (single source of truth).
- [ ] Reflect tiers in the `/pricing` page without violating the "no invented rates" test.
- [ ] Gate the deploy behind the existing staged→main dwell + evidence pack.
