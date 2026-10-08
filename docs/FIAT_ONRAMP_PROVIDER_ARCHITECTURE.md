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

## 5.5 Duplication audit — what we actually have (gateway `internal/api`)

Before gating, audit the current shape so we don't re-duplicate.

### `fiat.rs` — `FiatRouter` (4 providers, duplicated in code)
- `OnRampSessionRequest.provider` is a **`String`** (`"ramp"|"investec"|"alchemypay"|"banxa"`) — no type safety.
- `FiatRouter::new()` takes **7 positional secret args**, all mandatory, no gating.
- `create_session()` does `match provider.as_str()` → **4 near-identical `create_*_session()` methods**; the only difference is the redirect URL template + which secret is embedded.
- `verify_webhook()` does a second `match` → **4 near-identical HMAC branches**.

| Provider | Redirect URL | Secret used | Distinct rail/region |
|----------|--------------|-------------|----------------------|
| Ramp | `buy.ramp.network?...&apiKey=` | `ramp_api_key` | EU/UK bank (SEPA/open-banking) + card |
| Investec | `investec.com/banking/pay?ref=...` | none (redirect only) | South Africa bank transfer (ZAR) |
| Alchemy Pay | `ramp.alchemypay.org?...&appId=` | `alchemy_pay_app_id` | APAC/LATAM + card |
| Banxa | `conxian-labs.banxa.com/?...` | none (hosted checkout) | global card/bank |

The four are **distinct regions/rails, not redundant** — but they are **duplicated in code** (4 parallel methods instead of one trait + 4 adapters).

### `a2p.rs` — `A2pRouter` (1 provider, not duplicated)
Single provider (Infobip) for OTP/A2P SMS (`send_otp`/`verify_otp`, HMAC via `hmac_secret`).
Not duplicated, but should sit behind a `MessagingProvider` trait to allow Twilio/Vonage/Sinch later.

### "Only connect to what we need"
- `Strict` (sovereign/community): needs **none** of fiat/A2P — currently *forced* to supply 7 fiat + infobip + hmac secrets.
- `Managed` (business): needs the **subset** matching its region (EU→Ramp, ZA→Investec, APAC→Alchemy).
- `Expedient` (enterprise): needs the **mandated** set (commercial SLA).

So the fix is not just "make secrets optional" — it is "collapse the 4 duplicated methods into a trait, then gate each provider by mode so a lane wires only what it needs."

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

## 7.5 Refined recommendation (expanded B)

**B (expanded) now, full C later.** The expanded B does two things at once:

1. **Removes the code duplication** — `FiatRouter`'s 4 parallel `create_*_session()` methods and
   4 webhook branches collapse into a `trait FiatOnRampAdapter { build_redirect_url();
   verify_webhook(); }` with 4 small adapters (Ramp/Investec/AlchemyPay/Banxa). `provider: String`
   becomes `enum FiatOnRampProvider`. This is a *scoped* C — no routing/aggregation engine yet.
2. **Gates providers per lane** — add `*_MODE` (`disabled|shadow|active`) per provider, mirroring
   RGB `RolloutMode`. Secrets are `get_mandatory_env` only when `active`; otherwise the adapter is
   simply not constructed (`Option<...>`), so a lane connects only to the providers it needs.

Concrete shape:
- `enum FiatOnRampProvider { Ramp, Investec, AlchemyPay, Banxa }`
- `trait FiatOnRampAdapter { fn build_redirect_url(&self, req) -> String; fn verify_webhook(...) -> bool; }`
- `FiatRouter { ramp: Option<RampAdapter>, investec: Option<...>, ... }` — only enabled ones.
- `A2pRouter` stays a single provider today, behind a `MessagingProvider` trait for future Twilio/Vonage/Sinch.

Lane defaults via `TrustTier`: `Strict` → all fiat/A2P disabled (BTC-native); `Managed` → configured
subset; `Expedient` → mandated set. No provider is "the only choice" — leaders are named first-class
variants behind a provider-agnostic trait, and switching = mode flag + adapter.

## Sources

- Crypto on/off-ramp landscape: spark.money, apidog.com, lightspark.com knowledge.
- Provider docs: Ramp Network (rest-api-v3), Banxa, Transak, MoonPay, Onramper, OnMeta.
- A2P market: imarcgroup A2P market, txtimpact, infobip, signalmash, sourceforge comparison.
- Org: `lib-conxian-core/src/fee.rs` (SettlementRail), `control_model/trust.rs` (TrustTier),
  `adapters/mod.rs`; `conxian-gateway/cmd/gateway/src/config.rs` (RolloutMode/RGB gating).
