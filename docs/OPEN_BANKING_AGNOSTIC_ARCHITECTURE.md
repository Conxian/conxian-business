# Open Banking & Agnostic Base Layer — Verified Findings + Advice

> Status: advisory (2026-10-03). Research-verified, decision open.
> Scope: replacing the gateway's bank-scoped Investec rail with a true open-banking /
> infrastructure rail, and how the org's existing rail abstraction maps onto it.

## 1. Verification ("don't trust, verify")

The premise — *Investec requires being a customer, so it is not an agnostic rail* — is
**confirmed**.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Investec API is bank-scoped (needs an Investec account) | ✅ **True** | `developer.investec.com`: credentials come from "Investec Online → Manage → Investec Developer", API keys are bound to **your own** accounts. "Don't have an Investec account? … Sandbox APIs" → production access requires being a customer. |
| Yapily = infrastructure-first, white-label, multi-bank | ✅ **True** | 2,000+ banks / 19 EU markets; AISP+PISP+VRP; FCA (UK) + Bank of Lithuania (EU) so customers launch **without their own PSD2 licence**; explicitly "infrastructure for PSPs, not product layer"; crypto/iGaming supported. |
| Fiat Republic = crypto-friendly fiat-clearing middleware | ✅ **True** | UK/EU EMI (FCA FRN 900524, DNB R190553); single API for SEPA, SEPA Instant, Faster Payments (GBP), SWIFT (USD), Elixir, Pix; virtual IBANs; KYC/AML + Oxygen monitoring; business-only (VASPs); addresses crypto "debanking". |
| Open Bank Project = white-label, multi-bank connector | ⚠️ **Mischaracterised** | OBP is open-source software **a bank deploys** on top of its *own* core (pluggable connectors). It is **not** a managed multi-bank aggregator for third parties. |

**Correction to the quoted block:** Yapily and OBP are *not* equivalent. Yapily is a
managed multi-bank network (what Conxian wants); OBP is bank-side self-hosted software
(what a bank would run). For Conxian's base layer, the relevant pair is **Yapily
(orchestration) + Fiat Republic (settlement)**.

## 2. Payment orchestration vs data orchestration

Conxian needs **both**, and they are separable:

- **Payment orchestration** (primary): initiate/route fiat → crypto (and crypto → fiat).
  Open-banking **PIS** (payment initiation) + **Fiat Republic** (clearing/settlement).
- **Data orchestration** (supporting): identity/KYC/account verification for on-ramp
  compliance. Open-banking **AIS** (account info) via Yapily.

Yapily's single API covers AIS **and** PIS, so one adapter serves both orchestration
roles; Fiat Republic covers the *holding/clearing* of fiat, which is a separate concern.

## 3. How this maps onto what the org already has

The gateway refactor (`feat/fiat-provider-modes`) already built the right foundation:

- `FiatOnRampProvider` enum + `FiatOnRampAdapter` trait (mode-gated per lane).
- `SettlementRail` (core) — the destination chain a settlement lands on.
- `protocol/intent.rs` (core) — the canonical payment-intent model.

The agnostic base layer is realised as:

```
open-banking JSON (Yapily PIS / Fiat Republic)
        │  adapter maps provider JSON → canonical intent
        ▼
PaymentIntent (protocol/intent.rs)   ← network-agnostic, no bank/region baked in
        │  route + clear
        ▼
SettlementRail (Lightning/Stacks/sBTC/RGB/Babylon/ERC-7683)
```

- **Decoupling**: the base layer (intent + settlement) never references a bank, region, or
  crypto ecosystem. A regulatory shift (PSD2/FedNow/ZA open-banking) only swaps the
  *adapter*, never the protocol.
- **Unified payload**: one `PaymentIntent` shape regardless of whether the rail is Yapily,
  Fiat Republic, Ramp, or Banxa.

## 4. Recommendation

1. **Replace `InvestecAdapter` with an `OpenBankingAdapter` (Yapily-first).** Investec is
   bank-scoped and has no place in an agnostic layer; Yapily is the managed multi-bank rail
   (AIS+PIS). Keep it a **named variant + adapter**, mode-gated like the rest.
2. **Add `FiatRepublicAdapter` as a *settlement* rail** (separate from on-ramp) for the
   enterprise lane — virtual IBANs + SEPA/Faster Payments clearing without a banking licence.
3. **No new abstraction** — these are additional variants in the existing
   `FiatOnRampProvider`/adapter enum; the intent + `SettlementRail` layer is unchanged.

### Open questions for the owner
- Which regions/rails does Conxian need at launch (EU SEPA? UK Faster Payments? ZA open banking? US FedNow/ACH — Fiat Republic lists FedNow as *in development*)?
- Is an aggregator *in addition to* direct providers in scope (Onramper-style routing across Ramp/Banxa/Yapily)?
- Should the open-banking adapter live in the gateway (current) or move into `lib-conxian-core` as a first-class `FiatRail` alongside `SettlementRail`?

## Sources (verified)
- Investec Developer Portal: `developer.investec.com/individuals`, `/commercial-corporates`.
- Yapily: `yapily.com/blog/*`, `apis.io/providers/yapily`, `enablebanking.com`.
- Fiat Republic: `fiatrepublic.com`, `apis.io/providers/fiat-republic`, `coincub.com/cryptobanks/fiat-republic`.
- Open Bank Project: `open-bank-project.readthedocs.io`, `github.com/OpenBankProject/OBP-API`.
- Org: `lib-conxian-core/src/fee.rs` (SettlementRail), `src/protocol/intent.rs` (intent).
