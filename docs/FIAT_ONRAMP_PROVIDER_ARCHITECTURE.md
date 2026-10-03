# Fiat On-Ramp & A2P Provider Architecture — Research & Options

> Status: research (2026-10-03). Decision open. Scope: `conxian-gateway` config gating for
> fiat on-ramp (RAMP, Investec, Alchemy Pay, Banxa) and A2P messaging (Infobip).

## 1. The decision

`conxian-gateway` `Config::from_env()` reads **13 secrets unconditionally** via
`get_mandatory_env()` — including the fiat-on-ramp (RAMP/Investec/Alchemy Pay/Banxa) and A2P
(Infobip) provider keys. `docker-compose.yml` has three lanes (sovereign/community, business,
enterprise), but a **community/sovereign node** — which is Bitcoin/Lightning-native and has no
fiat rails — is *forced* to supply business-provider credentials or fail at startup.

Question: should business-only providers be **mandatory for every lane**, or **gated per-lane**,
and how do we stay provider-agnostic (support industry leaders without locking into any one)?

## 2. Industry landscape (2025–2026)

### Fiat on-ramp / off-ramp providers

| Tier | Providers | Notes |
|------|-----------|-------|
| Global leaders | MoonPay, Ramp Network, Transak, Banxa, Mercuryo, Simplex/Nuvei, Alchemy Pay | Cards, bank rails (SEPA/PIX/open-banking), broad country coverage |
| Aggregators | Onramper, OnMeta | Single integration routing to many on-ramps; OnMeta targets India/SEA |
| Regional | (many) | Local rails: Faster Payments, PIX, UPI, etc. |

- **Integration models** split into two families:
  - **Hosted widget / merchant-of-record** (MoonPay): provider owns KYC + chargeback/fraud risk —
    fast to integrate but higher lock-in (KYC data lives with provider).
  - **Server-side REST API / whitelabel** (Ramp V3, Transak whitelabel, Banxa): more control,
    backend calls from whitelisted IPs, keeps KYC orchestration in your control.
- **Multi-provider aggregation is the norm** — wallets/exchanges run several providers + route by
  price/success-probability/KYC-friction (Onramper's model).
- **Fee/settlement** vary widely (cards ~0.5–5%); provider docs are the source of truth.

### A2P messaging

- Top-5 platform tier (≈35–42% of global revenue): **Twilio, Sinch, Vonage (Ericsson),
  Infobip, Syniverse/MessageBird**.
- **Infobip** is a legitimate enterprise leader (global, omnichannel, SLA-backed, quote-based) —
  but interchangeable with Twilio/Vonage/Sinch at the API level.
- Same adapter logic applies: a `MessagingProvider` interface (send / status webhook / provision)
  with pluggable connectors + rate limits + regional compliance + failover.

## 3. Standard architecture patterns (evidence-backed)

1. **Provider abstraction layer** — a canonical contract (`createQuote`, `execute`,
   `handleWebhook`) with typed objects (Quote, Order, paymentMethod); adapters map provider
   fields into the canonical shape.
2. **Adapter/strategy per provider** — each connector encapsulates auth (key/OAuth), rate limits,
   idempotency.
3. **Feature flags + per-deployment config** — enable/disable providers per lane/tier; provider
   priority lists for routing.
4. **Dynamic routing + fallback** — decision engine on region / method / fee / success / KYC
   friction; fallback chain.
5. **Resilience** — per-provider circuit breakers, health checks, telemetry.
6. **Optional plugins** — connectors shipped as optional modules; missing plugin → pre-install
   warning, not a hard failure.

**Lock-in indicators:** hosted-widget/merchant-of-record models (KYC retained by provider) are the
highest lock-in; prefer server-side APIs + adapter layer so switching = connector change only.

## 4. What the org already has (reuse, don't reinvent)

`lib-conxian-core` + `conxius-enclave-sdk` already define the taxonomy:

- **`TrustTier`** (core, `control_model/trust.rs`): `Strict | Managed | Expedient | ObserverOnly` —
  maps cleanly to lanes: `Strict` = sovereign/community, `Managed` = business, `Expedient` =
  enterprise.
- **`SettlementRail`** (core, `fee.rs`): 8 settlement destination rails (Lightning, Statechain,
  Fedimint, RGB, sBTC, ALEX/Stacks, Babylon, EVM/ERC-7683).
- **Bridge rails** (enclave-sdk): Bisq/Boltz/Changelly/NTT/Wormhole (cross-chain transport) — a
  *separate* "rail" namespace, disambiguated via `RailTrustTier`.
- **`RolloutMode`** (core, used in gateway `config.rs` for RGB): `Disabled | Shadow | Active` —
  **the exact gating pattern the fiat providers should reuse** (see §5).
- **Adapter pattern** (`core/src/adapters/mod.rs`): `StateProofError` + chain adapters.

Fiat on-ramp providers are a **fourth "rail" family** — currently with **no abstraction** (just
hard-coded mandatory env vars).

## 5. The pattern already in the codebase: `RolloutMode`

`gateway config.rs` gates RGB via a mode flag (lines ~319–344):

```
RGB_MODE = disabled|shadow|active   →   RolloutMode::Disabled|Shadow|Active
RGB_STASH_PATH / RGB_ESPLORA_URL    →   optional_env (absent = disabled)
if active && rgb-native:  require RGB_STASH_PATH + RGB_ESPLORA_URL   (fail closed)
```

This is exactly how each fiat provider should behave:
- provider `_MODE = disabled|shadow|active`;
- `active` → its secrets are **mandatory** (fail closed);
- `disabled|shadow` → its secrets are **optional/ignored** (provider absent, no startup panic).

## 6. Options

### Option A — keep unconditional mandatory (status quo)
All 13 secrets required for every lane. Simple, but breaks the sovereign/community lane and is not
provider-agnostic (every deploy must provision every provider). **Rejected** as a target.

### Option B — mode-gated secrets (reuse `RolloutMode`)
Add `RAMP_MODE`, `BANXA_MODE`, `ALCHEMY_PAY_MODE`, `INVESTEC_MODE`, `INFOBIP_MODE`
(`disabled|shadow|active`). Provider secrets become mandatory **only when `active`**; otherwise
optional. Lane defaults: `Strict` → providers default `disabled`; `Managed`/`Expedient` → opt-in
`active` per config. Minimal diff, org-consistent (mirrors RGB), keeps fail-closed for enabled
providers. Unblocks the community lane immediately.

### Option C — pluggable `FiatOnRampProvider` + adapter trait + routing (target)
Model providers as a first-class enum (industry leaders as named variants — Ramp, Banxa,
AlchemyPay, Investec, MoonPay, Transak, …) behind a `FiatOnRampAdapter` trait
(`createQuote`/`execute`/`handleWebhook`), mirroring `SettlementRail` + the adapter pattern.
Add dynamic routing/fallback + optional aggregation (Onramper). This is the industry-standard,
lock-in-free end-state — a larger refactor (new module + tests + provider sandbox harness).

## 7. Recommendation

**B now, C as the target.** B is a small, org-consistent change that resolves the lane-gating bug
and keeps providers optional-per-lane without losing fail-closed safety. C is the long-term shape
that makes providers pluggable and aggregation-optional. Neither option locks into any provider:
industry leaders are supported as *named* first-class variants, but the abstraction stays
provider-agnostic and extensible — a provider switch is a mode flag + adapter, never business
logic.

### Open questions for the owner
- Which providers are **mandated** for the `enterprise` lane (commercial SLA), vs optional?
- Is an **aggregator** (Onramper/OnMeta) in scope as a first-class provider, or direct-only?
- For `Strict` (sovereign) lane: should fiat rails be **unavailable by design** (BTC-native), or
  optional-but-off?

## Sources

- Crypto on/off-ramp landscape: spark.money, apidog.com, lightspark.com knowledge.
- Provider docs: Ramp Network (rest-api-v3), Banxa, Transak, MoonPay, Onramper, OnMeta.
- A2P market: imarcgroup A2P market, txtimpact, infobip, signalmash, sourceforge comparison.
- Org: `lib-conxian-core/src/fee.rs` (SettlementRail), `control_model/trust.rs` (TrustTier),
  `adapters/mod.rs`; `conxian-gateway/cmd/gateway/src/config.rs` (RolloutMode/RGB gating).
