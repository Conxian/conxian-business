# Developer Adoption & Exponential Growth — Verified Research + Advice

> Status: advisory (2026-10-03). Research-verified. Decision open.
> Scope: IBM Hyperledger Fabric positioning, "everyone builds on Conxian", and how
> Conxian-Labs grows exponentially.

## 1. IBM Hyperledger Fabric — verified position (not a direct competitor)

**Verified:** Fabric is a **permissioned** enterprise DLT — Membership Service Providers
(MSP) backed by X.509 certs, private channels, ~3,500 TPS under Raft. Its home turf is
supply chain, business automation, and KYC/AML where **identity of participants is a hard
requirement**. It is *not* a public, permissionless chain.

| Dimension | Hyperledger Fabric | Conxian |
|-----------|--------------------|---------|
| Access | Permissioned (known entities, X.509/MSP) | Permissionless (anyone builds) |
| Security | Consortium/CA trust | Bitcoin L1 anchor (censorship-resistant) |
| Rails | Private channels | Agnostic: any bank / region / chain |
| Language | Go / chaincode | Rust (core SDK) |

**Advice — don't compete, bridge.** Conxian is not a Fabric replacement; it is the *public,
Bitcoin-native* complement. The differentiated play is **"notarize on Fabric (permissioned),
settle on Bitcoin (Conxian SettlementRail)"** — enterprises keep private consortium ledgers
and settle the final state onto a censorship-resistant rail. That is the same
"tokenize/clear into any blockchain" thesis as the open-banking layer, applied to enterprise.

## 2. "How do we make everyone build on Conxian?" — the developer surface we already own

Verified adoption levers (Sapphire Ventures, Quicknode, MongoDB): the winning base layers
**reduce complexity** with (a) SDKs that abstract away rail/chain specifics, (b) local dev
env + testing + docs + debugging, (c) sample projects, (d) community/education.

Conxian-Labs already has this surface — it is **under-leveraged**, not missing:

| Asset | State | Growth role |
|-------|-------|-------------|
| `lib-conxian-core` (Rust) | ✅ published (v0.3.3) | the canonical "build on Conxian" SDK — SettlementRail, TrustTier, fee model, intent, verifier, adapters |
| `conxius-enclave-sdk` | ✅ published (v2.0.17) | Nitro TEE attestation + 2-of-3 FROST threshold signing |
| `@conxian/market-sdk` | ⛔ implemented but **unpublished** (G2) | settlement SDK — **0 downstream imports today** |
| 8 `SettlementRail`s + bridge rails | ✅ in core/sdk | each rail = a plug-in point = a network-effect unit |
| fiat on-ramp adapters | ✅ just refactored (mode-gated) | open-banking (Yapily/Fiat Republic) as new variants |

**The easy wins (what we can support *now*):**

1. **Publish `@conxian/market-sdk` (unblock G2)** — the single highest-leverage move; the
   SDK is done and consuming zero of its own ecosystem.
2. **Treat every rail/adapter as the growth surface** — the `FiatOnRampProvider`/`SettlementRail`
   adapter pattern (just shipped) means "add a rail = add a variant, no core change". That is
   the literal "anyone can plug in a financial rail seamlessly" promise — make it the headline.
3. **Document + sample the SDKs** — a `cargo`-gettable core + `npm` market-sdk + sample apps
   (e.g. a "settle on Lightning in 50 lines" starter) lower onboarding from weeks to hours.

## 3. Growing Conxian-Labs exponentially — the aligned levers

Ranked by leverage (compound effect):

1. **G2 publish → G3 wire-in** (wallet #597 + platform #1347). Unblocks the first *consumers*
   of the SDK, which is the seed of the network effect.
2. **SDK-surface as product.** Publish + document + sample the core/enclave/market SDKs; ship
   a public "build on Conxian" landing + quickstarts. Developer adoption compounds.
3. **The adapter/rail network effect.** Every new rail (open-banking via Yapily/Fiat Republic,
   another SettlementRail, another bridge) increases the value of the base layer for *every*
   existing developer — growth by adding rails, not by rewriting core.
4. **Enterprise bridge (Fabric → Bitcoin settlement).** A unique position no public chain or
   private DLT holds alone: permissioned consortium ledger that *settles* on Bitcoin.
5. **Agnostic open-banking routing** (Yapily AIS/PIS + Fiat Republic settlement) as the
   "universal routing layer" — one integration, any bank/region, crypto-fiat decoupled.

### Open questions for the owner
- Is the *developer-platform* play (SDK/docs/samples) the near-term priority, or the
  *enterprise* play (Fabric → Bitcoin settlement)?
- Which 2–3 rails should ship first as public, sample-backed "reference integrations"?
- Should `@conxian/market-sdk` publish be re-prioritised above other G-items (it is the G2
  blocker for G3)?

## Sources (verified)
- Hyperledger Fabric: `hyperledger-fabric.readthedocs.io/en/latest/whatis.html`,
  `kaleido.io/blog/what-is-hyperledger-fabric`, `chainlaunch.dev/blog/permissioned-vs-permissionless-blockchain`.
- Developer adoption: `sapphireventures.com/blog/building-web3-block-by-block`,
  `quicknode.com/builders-guide`, `mongodb.com/resources/basics/databases/blockchain-implementation`.
- Org state: `.github-private` registry + capabilities audit; G2/G3 gap register.
