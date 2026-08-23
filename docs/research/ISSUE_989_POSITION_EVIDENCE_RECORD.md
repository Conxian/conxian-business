# Issue #989 Position Evidence Record

| Field | Value |
|---|---|
| Status | Public-safe, sanitized evidence audit; not a strategic market report |
| Record date | 2026-08-03 |
| Source snapshot date | 2026-08-03 |
| Issue | [Conxian/conxian-business #989](https://github.com/Conxian/conxian-business/issues/989) |
| Trigger | [Issue comment 5163152579](https://github.com/Conxian/conxian-business/issues/989#issuecomment-5163152579) |
| Restricted-record authority | [Conxian/conxian-business #943](https://github.com/Conxian/conxian-business/issues/943) |

## Purpose and classification boundary

This record replaces an unverified direct-to-`main` draft with a neutral,
evidence-graded Git record. It preserves only public-safe facts, dated source
links, sanitized technical evidence, and explicit non-claims.

The full TAM/SAM/SOM application, competitive positioning, customer and ACV
scenarios, pricing, partner analysis, market-capture recommendations, and
financial analysis are withheld until #943 designates an approved non-Git
restricted-record successor and its accountable owner. Historical GitHub
references are continuity artifacts, not authorization to store restricted
content in Git or GitHub.

## Scope and method

The 2026-08-03 review independently examined all 16 accessible organization
repositories: `.github-private`, `.github`, `Conxian`, `conxian_ui`,
`conxius-orbit`, `conxius-wallet`, `conxian-labs-site`, `conxian-gateway`,
`lib-conxian-core`, `conxius-platform`, `conxian-nexus`, `conxian-business`,
`conxius-enclave-sdk`, `demo-repository`, `conxian.github.io`, and
`conxian_market`.

The review read 46 substantive research, knowledge-base, SDK, audit, and PRD
documents; checked default-branch code, manifests, tests, releases, and hosted
check evidence at dated revisions; and compared the supplied external claims
with dated first-party or publisher landing pages. Exact repository snapshots
are recorded below.

This method verifies what the accessible sources state and what the inspected
code does. It does **not** make inaccessible or paywalled report methodology
independently verified. It is not a penetration test, deployment review,
mainnet certification, customer validation exercise, or financial opinion.

## Claim disposition

| Supplied claim | Disposition at 2026-08-03 | Evidence-safe conclusion |
|---|---|---|
| Broad blockchain-technology forecast | **Publisher landing page matched; application unsupported.** The supplied endpoints and growth rate match the cited publisher landing page. The underlying methodology is paywalled and was not independently verified. | Cite only as a broad third-party category forecast. It does not directly establish Conxian TAM. |
| Broad blockchain-interoperability forecast | **Publisher landing page matched; application unsupported.** The supplied endpoints and growth rate match the cited publisher landing page. The underlying methodology is paywalled and was not independently verified. | Cite only as a broad third-party category forecast. It does not directly establish Conxian SAM. |
| Endpoint and CAGR consistency | **Independently recomputed; exact values intentionally omitted.** The supplied endpoint and growth-rate relationships are mathematically consistent after ordinary rounding. A prior public-safe draft contained a rounding/recalculation error and was corrected before final handoff. | Mathematical consistency does not validate the publisher methodology, category selection, or Conxian-specific application. |
| Obtainable-market claim | **Unsupported.** No sourced bottom-up customer count, price, adoption, sales-capacity, or conversion model was supplied. | Remove from public claims. A future restricted analysis needs explicit assumptions, sources, owners, and sensitivity ranges. |
| Segment-share arithmetic used to derive the obtainable-market claim | **Unsupported and arithmetically inconsistent with the supplied obtainable-market claim.** The described segment-share calculation does not derive the claimed range. | Do not use the share or derived claim without a sourced denominator and a reproducible model. |
| Competitor-share claims | **Unsupported.** No sourced denominator, geography, category definition, or observation date was supplied. | Remove. Dynamic usage or protocol metrics must not be relabeled as market share. |
| LayerZero and Wormhole rely generically on standard multisig or EVM-centric validation | **Inaccurate/overbroad.** LayerZero documents configurable verification and execution services. Wormhole documents Guardian-network and additional security architecture; neither is accurately summarized by the supplied generic characterization. | Describe each system from its first-party architecture and security documentation. Do not infer a universal competitor weakness from historical bridge incidents. |
| “institutional-grade clearinghouse,” “universal,” or repository-wide “production-ready” | **Unverified or overstated.** The inspected repositories contain real components alongside unavailable, pilot, simulated, structural, placeholder, and runtime-gated paths. | Use bounded capability language tied to an exact revision, path, test, runtime dependency, and acceptance state. |

## Technical evidence matrix

Evidence states below distinguish code presence from cryptographic verification,
runtime wiring, deployment evidence, and production acceptance.

| Repository snapshot | Inspected evidence | Honest status |
|---|---|---|
| [`lib-conxian-core@ad28dfe10932477e7bc57e7d361d3e80867c186f`](https://github.com/Conxian/lib-conxian-core/commit/ad28dfe10932477e7bc57e7d361d3e80867c186f) | [`ProtocolVerifier`](https://github.com/Conxian/lib-conxian-core/blob/ad28dfe10932477e7bc57e7d361d3e80867c186f/src/verifier.rs#L1801-L1817) explicitly validates structure and advertised policy rather than cryptographic authenticity. The [`OnChainAnchoringPublisher`](https://github.com/Conxian/lib-conxian-core/blob/ad28dfe10932477e7bc57e7d361d3e80867c186f/src/anchoring.rs#L227-L270) synthesizes a receipt-like `0xonc...` reference and `Broadcasted` status without an RPC, transaction broadcast, or confirmation path. The universal signer test uses a [`DeterministicMockSigner`](https://github.com/Conxian/lib-conxian-core/blob/ad28dfe10932477e7bc57e7d361d3e80867c186f/tests/universal_chain_signer.rs#L12-L112). | Validation, policy, receipt-envelope, and signing abstractions are present. The cited paths are not proof of live chain verification, broadcast, confirmation, or hardware signing. |
| [`conxian-nexus` current `main` at `347297f1b5ec865c5210bfbf81ee27cff50bad8a`](https://github.com/Conxian/conxian-nexus/commit/347297f1b5ec865c5210bfbf81ee27cff50bad8a); code inspected at [`b11e2ce7d01bd5110b04d40d98aec6d05210cef8`](https://github.com/Conxian/conxian-nexus/commit/b11e2ce7d01bd5110b04d40d98aec6d05210cef8) | The Nexus verifier performs real Arkworks BN254 Groth16 [`verify_proof`](https://github.com/Conxian/conxian-nexus/blob/b11e2ce7d01bd5110b04d40d98aec6d05210cef8/src/executor/bitvm_groth16.rs#L433-L516), with repository adversarial tests. Current-main wiring uses [`UnavailableBitcoinHeightProvider`](https://github.com/Conxian/conxian-nexus/blob/347297f1b5ec865c5210bfbf81ee27cff50bad8a/src/main.rs#L119-L136), explicitly gating the production path. The Stacks adapter is a [`Pilot implementation`](https://github.com/Conxian/conxian-nexus/blob/b11e2ce7d01bd5110b04d40d98aec6d05210cef8/src/executor/stacks.rs#L34-L63) with structural checks and mock success for formatted input. | A real Groth16 verification component exists, but the inspected default runtime is unavailable until a reviewed Bitcoin-height provider is wired. The Stacks path is pilot structural validation, not transaction verification evidence. |
| [`conxian-gateway@86dcc20e280a163788b91ceb27c01e70a3df51ec`](https://github.com/Conxian/conxian-gateway/commit/86dcc20e280a163788b91ceb27c01e70a3df51ec) | The Groth16 module defines a backend-neutral boundary and an explicitly [`test-only`, non-cryptographic verifier](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/internal/engine/src/bitcoin/groth16_verifier.rs#L606-L608) whose fixture implementation does not perform pairings ([lines 746-753](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/internal/engine/src/bitcoin/groth16_verifier.rs#L746-L753)). The ISO and related normalization paths return fixed/sample envelope fields in [`zkc.rs`](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/internal/compliance/src/zkc.rs#L140-L353). The TEE-named verification path checks caller-supplied secp256k1 signatures and a device-ID prefix ([lines 35-116](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/internal/compliance/src/zkc.rs#L35-L116)); it does not validate vendor TEE certificate chains or collateral. | Canonical envelopes, validation boundaries, message normalization, and signature checks exist. The cited snapshot does not establish a production Groth16 backend, live ISO settlement, or vendor-backed TEE attestation. |
| [`conxius-enclave-sdk@e00bd869028f1e038801b23a7795e37ae2dece7d`](https://github.com/Conxian/conxius-enclave-sdk/commit/e00bd869028f1e038801b23a7795e37ae2dece7d) | The [production-enablement audit](https://github.com/Conxian/conxius-enclave-sdk/blob/e00bd869028f1e038801b23a7795e37ae2dece7d/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md) records strong fail-closed trust and value-bearing signing containment, while classifying the repository as **Beta / conditional** and stating that a real authenticated provider verifier/signer and vendor evidence remain unavailable. The [signer-backend policy](https://github.com/Conxian/conxius-enclave-sdk/blob/e00bd869028f1e038801b23a7795e37ae2dece7d/docs/architecture/SIGNER_BACKEND_POLICY_MATRIX.md) disallows software/mock production use. | Strong architecture and containment evidence. No unqualified value-bearing production signing or settlement claim is supported. |
| [`Conxian@51fe261515f4f787cbe74ad7064dc8abff0f4eae`](https://github.com/Conxian/Conxian/commit/51fe261515f4f787cbe74ad7064dc8abff0f4eae) | The snapshot is a large Clarity 4 contract codebase. Selected high-impact surfaces remain explicitly unavailable or incomplete: [`zkml-verifier.clar`](https://github.com/Conxian/Conxian/blob/51fe261515f4f787cbe74ad7064dc8abff0f4eae/contracts/compliance/zkml-verifier.clar#L9-L21) always returns `ERR_VERIFIER_UNAVAILABLE`; the [BitVM2 bridge test](https://github.com/Conxian/Conxian/blob/51fe261515f4f787cbe74ad7064dc8abff0f4eae/tests/bitvm2-bridge.test.ts) labels its proof a placeholder; and bridge surfaces retain TODO/placeholder boundaries. | Contract count and language-version migration show implementation breadth, not end-to-end readiness. Each capability needs its own cryptographic, runtime, network, and acceptance evidence. |
| [`conxian_market@403c4c3437f6e535beb7b29283b3bfa97c2a8ae9`](https://github.com/Conxian/conxian_market/commit/403c4c3437f6e535beb7b29283b3bfa97c2a8ae9) | The snapshot contains a rich research corpus but only one implementation file under `src/`: [`src/fee_calculator.ts`](https://github.com/Conxian/conxian_market/blob/403c4c3437f6e535beb7b29283b3bfa97c2a8ae9/src/fee_calculator.ts). | Research/reference surface at this snapshot; do not call it a production settlement core. |

## Evidence-safe positioning language

The currently supportable public description is:

> A fail-closed, sovereignty-oriented Bitcoin/Stacks integration stack with a
> real Groth16 verifier gated by runtime dependencies, plus verification,
> policy, signing-envelope, and protocol-adapter abstractions at mixed maturity.

Security, sovereignty, broad protocol coverage, and institutional integration
are design objectives. The reviewed evidence does not prove universal coverage,
institutional superiority, a clearinghouse role, production settlement, or
market leadership.

## Prohibited wording and explicit unknowns

Do not publish the following without a new evidence gate tied to an exact
release and independently reviewed acceptance artifacts:

- “institutional-grade clearinghouse”;
- “universal verification” or “universal chain connectivity” as an achieved,
  unrestricted production capability;
- repository-wide “production-ready,” “mainnet-ready,” “fully verified,” or
  equivalent language;
- unsourced market-share percentages, segment-share percentages, or capture
  targets;
- competitor security characterizations not supported by the competitor's
  dated first-party architecture;
- customer, ACV, pricing, partner-ranking, or financial claims in Git/GitHub.

Unknown from the accessible evidence:

- the paywalled market reports' full sampling, segmentation, currency,
  inclusion/exclusion, and forecast methodology;
- a defensible Conxian-specific TAM/SAM/SOM mapping;
- current customer count, contract value, conversion, pipeline, pricing, sales
  capacity, and obtainable share;
- deployed provider hardware, certificate roots/collateral, production runtime
  configuration, external security acceptance, and value-bearing operational
  evidence;
- a stable denominator for dynamic protocol usage or “market share.”

## Citation ledger

Source quality tiers used here:

- **Tier 1:** first-party protocol, platform, repository, code, test, release, or
  standards documentation at a dated revision.
- **Tier 2:** named market-research publisher landing page whose displayed
  values can be checked, but whose underlying report methodology is not fully
  accessible.
- **Tier 3:** reputable contextual incident analysis; useful for historical
  context, not for assigning current architecture or market share.

| Accessed | Tier | Canonical source | Use and limit |
|---|---:|---|---|
| 2026-08-03 | 2 | [Fortune Business Insights: Blockchain Technology Market](https://www.fortunebusinessinsights.com/industry-reports/blockchain-market-100072) | Confirms displayed broad-category forecast only; methodology not independently verified. |
| 2026-08-03 | 2 | [Fortune Business Insights: Blockchain Interoperability Market](https://www.fortunebusinessinsights.com/blockchain-interoperability-market-109372) | Confirms displayed broad-category forecast only; not a Conxian-specific SAM. |
| 2026-08-03 | 1 | [LayerZero: What is LayerZero?](https://docs.layerzero.network/v2/concepts/getting-started/what-is-layerzero) | First-party architecture overview. |
| 2026-08-03 | 1 | [LayerZero: Verification and execution services](https://docs.layerzero.network/v2/concepts/verification-execution-services) | First-party description of configurable verification/execution. |
| 2026-08-03 | 1 | [Wormhole protocol security](https://docs.wormhole.com/protocol/security/) | First-party Guardian and security architecture. |
| 2026-08-03 | 3 | [Chainalysis: Cross-chain bridge hacks in 2022](https://www.chainalysis.com/blog/cross-chain-bridge-hacks-2022/) | Historical bridge-risk context; not evidence that all bridges share one architecture. |
| 2026-08-03 | 1 | [Stacks: sBTC FAQ](https://docs.stacks.co/learn/sbtc/sbtc-faq) | First-party sBTC model and boundaries. |
| 2026-08-03 | 1 | [Stacks: block production and signing](https://docs.stacks.co/learn/block-production/signing) | First-party signer and block-production context. |
| 2026-08-03 | 1 | [`lib-conxian-core` exact source](https://github.com/Conxian/lib-conxian-core/tree/ad28dfe10932477e7bc57e7d361d3e80867c186f) | Technical matrix source. |
| 2026-08-03 | 1 | [`conxian-nexus` exact inspected source](https://github.com/Conxian/conxian-nexus/tree/b11e2ce7d01bd5110b04d40d98aec6d05210cef8) and [current-main runtime snapshot](https://github.com/Conxian/conxian-nexus/tree/347297f1b5ec865c5210bfbf81ee27cff50bad8a) | Technical matrix source; separates verifier implementation from runtime wiring. |
| 2026-08-03 | 1 | [`conxian-gateway` exact source](https://github.com/Conxian/conxian-gateway/tree/86dcc20e280a163788b91ceb27c01e70a3df51ec) | Technical matrix source. |
| 2026-08-03 | 1 | [`conxius-enclave-sdk` exact source](https://github.com/Conxian/conxius-enclave-sdk/tree/e00bd869028f1e038801b23a7795e37ae2dece7d) | Technical matrix source. |
| 2026-08-03 | 1 | [`Conxian` exact source](https://github.com/Conxian/Conxian/tree/51fe261515f4f787cbe74ad7064dc8abff0f4eae) | Technical matrix source. |
| 2026-08-03 | 1 | [`conxian_market` exact source](https://github.com/Conxian/conxian_market/tree/403c4c3437f6e535beb7b29283b3bfa97c2a8ae9) | Technical matrix source. |

## Corpus authority and document precedence

The following sources were treated as current evidence authorities for this
bounded record:

- [`docs/CLAIM_EVIDENCE_MATRIX.md`](../CLAIM_EVIDENCE_MATRIX.md) and
  [`docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`](../BOS_RESEARCH_CANDIDATE_LEDGER.md)
  for portfolio claim grading and research-cycle boundaries;
- the SDK [production audit](https://github.com/Conxian/conxius-enclave-sdk/blob/e00bd869028f1e038801b23a7795e37ae2dece7d/docs/audits/PRODUCTION_ENABLEMENT_AUDIT_2026-07-20.md)
  and [capability matrix](https://github.com/Conxian/conxius-enclave-sdk/blob/e00bd869028f1e038801b23a7795e37ae2dece7d/docs/architecture/CAPABILITY_MATRIX.md);
- the Nexus [PRD](https://github.com/Conxian/conxian-nexus/blob/347297f1b5ec865c5210bfbf81ee27cff50bad8a/docs/PRD.md);
- the Gateway [knowledge map](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/docs/research/KNOWLEDGE_MAP.md),
  [gap analysis](https://github.com/Conxian/conxian-gateway/blob/86dcc20e280a163788b91ceb27c01e70a3df51ec/docs/GAP_ANALYSIS_2026-07-22.md), and exact source;
- the Core [verifier inventory](https://github.com/Conxian/lib-conxian-core/blob/ad28dfe10932477e7bc57e7d361d3e80867c186f/docs/VERIFIER_INVENTORY.md),
  [PRD/API boundary](https://github.com/Conxian/lib-conxian-core/blob/ad28dfe10932477e7bc57e7d361d3e80867c186f/docs/PRD.md), and exact source;
- the Wallet [PRD](https://github.com/Conxian/conxius-wallet/blob/main/docs/business/PRD.md);
- the Market [unified positioning](https://github.com/Conxian/conxian_market/blob/403c4c3437f6e535beb7b29283b3bfa97c2a8ae9/docs/research/MARKET_UNIFIED_POSITIONING.md)
  and [cross-repository gap analysis](https://github.com/Conxian/conxian_market/blob/403c4c3437f6e535beb7b29283b3bfa97c2a8ae9/docs/research/CROSS_REPO_GAP_ANALYSIS_SESSION_48.md), used as research inputs rather than production proof.

Older readiness checklists, marketing copy, whitepapers, session summaries, and
repository-wide “ready” declarations are historical or non-authoritative where
they conflict with newer exact source, fail-closed runtime wiring, production
audits, capability matrices, or dated acceptance evidence.

## Reproducibility limits

- Local Rust tests are **not claimed as passed** in this review. The devbox
  system toolchain was Rust `1.89`, below dependencies or repository baselines
  requiring Rust `1.91-1.96`. Matching-head CI records and source-level tests
  were inspected instead; that does not substitute for a fresh matching-toolchain
  local run.
- External market pages are dynamic. Their displayed values were captured as a
  dated source snapshot, not frozen as permanent facts.
- Dynamic protocol usage, TVL, message count, developer activity, or similar
  metrics must retain their date, denominator, method, and source. They must not
  be converted into market share without a defensible category model.
- Repository evidence proves only the cited revision and path. A later default
  branch, release, deployment, provider configuration, or hosted check can
  change the disposition.

## Next gate

A full restricted market/position report may proceed only after #943 identifies
and approves the non-Git restricted-record successor and its accountable owner.
Until then, GitHub may hold only this sanitized evidence record and other
minimum-necessary public-safe coordination artifacts.
