# Current organization state — 16 October 2026

Public-safe operational overlay for [Business #1390](https://github.com/Conxian/conxian-business/issues/1390), [research reconciliation #1416](https://github.com/Conxian/conxian-business/pull/1416), and [CLI #1411](https://github.com/Conxian/conxian-business/issues/1411). The October 15 register and its scores remain dated history; this overlay records refreshed state and the next bounded implementation. It does not confer release, custody, commercial or production authorization.

Inventory refreshed at `2026-10-16T03:39:33.252Z`: **13 accessible repositories, 142 branches, 12 open PRs, 43 open issues**. The original 12 open PRs were tested with Git merge-tree against freshly fetched target refs; none conflicted. SDK #576 then closed as superseded and Market #181 opened, leaving 12 open PRs. GitHub cached PR base metadata differed from current target refs on several older PRs, so local merge comparisons use the fetched branch tips.

Coverage is an org/branch/work inventory and targeted code verification, not a fresh manual audit of every source line or every deployment. Twelve public repositories were cloned. The private KB entry guidance, registry, governance and newest checkpoint were read through authenticated access; restricted packet contents are excluded. The present conversation and recovered continuity were reconciled; no complete untruncated transcript is asserted.

## Implemented continuation

- Merged Market #178 already supplies bounded authenticated registration diagnostics and a separate x402 v2 wire profile. Its remaining compatibility gaps are corrected in [Market #181](https://github.com/Conxian/conxian_market/pull/181), head `7b76e088150c4c1bf10584c3a344e566827c7cf9`, tested/published tree `9e16e14c5f130a7bc1c21b84db24b718ae561ea6`.
- The correction accepts missing/null optional resource metadata, validates server extension envelopes and resource discovery constraints, preserves settlement amount and diagnostics, and requires a broadcast identifier for a pending settlement. Parsing does not verify payment, execute tools, or trigger retries. Research and synthetic fixtures pin x402 revision `0e6e8c55d86b4f14234fb6e49a4052074fb93e57`.
- Market validation: **325 library tests, 31 CLI process tests, 15 promotion tests**, typecheck, ESM distribution validation and tracked-path/diff hygiene pass on Node 24.19.0. Exact-head hosted SDK, promotion, security and preview checks are green; reviewer requested.
- SDK #576 head `4fdb3d46ee6c0b98a798b12b9cbc253268f028c1` is an ancestor of retained #579 head `eba3cd35bac1e578b6eec1904d1348f0d70fedc0`. Both target main. Closing the older lane loses no history and preserves its branch; approvals and acceptance do not transfer.
- Existing candidate verification: Business #1417 passes **40 promotion tests**; Platform #1441 passes **15 promotion tests**. Business #1341 passes its **19 merge-check tests**. Business #1416 passes **20 ledger/reconciliation tests**, both validators, knowledge retention, doctrine and cross-repository alignment. These are scoped script/document tests; no new full Rust/browser/mobile suite is claimed.

## Repository heads

| Repository | Branches | Main | Staged | Dev |
| --- | ---: | --- | --- | --- |
| [.github](https://github.com/Conxian/.github) | 1 | `f378c670ba05` | `—` | `—` |
| [conxian-business](https://github.com/Conxian/conxian-business) | 28 | `cc718d59b5d1` | `c3ef84f7eaeb` | `3185f59ec8e0` |
| [lib-conxian-core](https://github.com/Conxian/lib-conxian-core) | 13 | `26f8b90f86d7` | `6121c99bc61b` | `04ac05205440` |
| [conxian.github.io](https://github.com/Conxian/conxian.github.io) | 1 | `677d5ccadc27` | `—` | `—` |
| [conxian-gateway](https://github.com/Conxian/conxian-gateway) | 8 | `d84c2a50e488` | `84815b6f6509` | `aa4b5556674b` |
| [conxian_market](https://github.com/Conxian/conxian_market) | 17 | `581383c6e8a2` | `fcee08eb3ced` | `10d4b1666198` |
| [conxius-platform](https://github.com/Conxian/conxius-platform) | 12 | `2f4acde57523` | `12ce5b4f35d2` | `1b9baa4696bb` |
| [.github-private](https://github.com/Conxian/.github-private) | 3 | `baed07c80126` | `fc326efca708` | `fc326efca708` |
| [conxian-nexus](https://github.com/Conxian/conxian-nexus) | 6 | `6d2a339a910d` | `4bb9b7698423` | `25843d25d018` |
| [conxius-wallet](https://github.com/Conxian/conxius-wallet) | 10 | `1310955daec7` | `ac5313dc71bd` | `25f04b674486` |
| [conxian-labs-site](https://github.com/Conxian/conxian-labs-site) | 5 | `86e6fcd04b7a` | `93f4b99f747d` | `7bdece931d82` |
| [conxius-enclave-sdk](https://github.com/Conxian/conxius-enclave-sdk) | 33 | `fbaa77a8f905` | `eba3cd35bac1` | `cb6b9c69752b` |
| [conxian-org-site](https://github.com/Conxian/conxian-org-site) | 5 | `c7549a4cafde` | `—` | `—` |

## Open PR dispositions

| PR | Exact head | Current blocker / next action |
| --- | --- | --- |
| [conxian_market #181](https://github.com/Conxian/conxian_market/pull/181) | `7b76e088150c4c1bf10584c3a344e566827c7cf9` | Hosted checks green; requested owner review. Keep separate from payment/runtime qualification. |
| [conxius-enclave-sdk #579](https://github.com/Conxian/conxius-enclave-sdk/pull/579) | `eba3cd35bac1e578b6eec1904d1348f0d70fedc0` | Code checks pass; production acceptance pack remains placeholder. Independent release evidence and owner review required. |
| [conxian_market #180](https://github.com/Conxian/conxian_market/pull/180) | `698dd0f3552c5a5572fabdef00ed7861a7ec8c9b` | Invalid immutable promotion: actual head differs from branch source and recorded target-base is stale. Preserve unique history; create a new exact candidate after source/target reconciliation and acceptance evidence. |
| [conxian-business #1417](https://github.com/Conxian/conxian-business/pull/1417) | `d0490a1da7f7ba77b85dad68586336b88fc7fd75` | Code checks and 40 local policy tests pass; Vercel deployment rate limit and applicable review remain. |
| [conxius-platform #1441](https://github.com/Conxian/conxius-platform/pull/1441) | `5d7965e61ad5b8d9efcf7e4a22080b3bc2dd8b5d` | Code checks and 15 local policy tests pass; Vercel deployment rate limit and applicable review remain. |
| [conxian-business #1364](https://github.com/Conxian/conxian-business/pull/1364) | `aa1e72e88e2fdafb13ee1cd4f8e23221f267ce69` | Code checks pass; Vercel deployment rate limit and requested-changes review remain. Retain review. |
| [conxian-business #1416](https://github.com/Conxian/conxian-business/pull/1416) | `996502cf19606ebcfcf030aaed6ec875a2644b69` | Code checks and reconciliation validation pass; Vercel control-plane deployment rate limit remains. This refreshed overlay extends the existing proposal. |
| [conxius-platform #1440](https://github.com/Conxian/conxius-platform/pull/1440) | `12ce5b4f35d2c62bc7056749b898ddc40cc9687e` | Mainnet acceptance gate fails; no generated sign-off or production claim. |
| [conxian-nexus #417](https://github.com/Conxian/conxian-nexus/pull/417) | `fda4688c332efb19e5a44577d8301fe57e668e13` | Old mutated promotion head, advisory audit failure and incomplete acceptance; later staged safety work needs a fresh exact candidate. |
| [conxius-wallet #725](https://github.com/Conxian/conxius-wallet/pull/725) | `7689c863be4d84cad4174d5e938407e887235126` | Dependency Audit fails; previous publication restriction remains in force. No ledger or guidance republishing attempted. |
| [conxian-gateway #530](https://github.com/Conxian/conxian-gateway/pull/530) | `13aee28bf997d69990d68e1849858f1f0df2d5d0` | Old backmerge regresses source-map-js 1.2.2 to 1.2.1 and removes newer destination changes. Reconcile actual current main/staged history; do not merge this stale candidate. |
| [conxian-business #1341](https://github.com/Conxian/conxian-business/pull/1341) | `e135002ece5c9cd5335e4c387a0a4143fea63de9` | Code checks and 19 local tests pass; Vercel control-plane deployment rate limit remains. |

The rows above are the inventory at the recorded refresh time. Business #1416 is then amended with this overlay itself; its subsequent head and hosted checks must be read from the live PR, separately from the older snapshot head. The reported Vercel rate limit is the observed commit-status message (retry in 24 hours); no quota, required check or review was bypassed. No new deployed-origin, cloud configuration, hardware or custody claim is made.

## Promotion rollout

The actual-head guard is present in six development branches and their staging branches. Business and Platform remain proposed in #1417/#1441. None of the eight main/default policy copies contains this new guard yet. Their trusted default-branch enforcement workflows therefore have not received it; local regression success is not live enforcement.

| Policy repository | Dev | Staged | Main/default |
| --- | --- | --- | --- |
| conxian-business | not yet bound | not yet bound | not yet bound |
| conxian-gateway | bound | bound | not yet bound |
| conxian-nexus | bound | bound | not yet bound |
| conxian_market | bound | bound | not yet bound |
| conxius-enclave-sdk | bound | bound | not yet bound |
| conxius-platform | not yet bound | not yet bound | not yet bound |
| conxius-wallet | bound | bound | not yet bound |
| lib-conxian-core | bound | bound | not yet bound |

## Phased next work

| Phase | Current action | Acceptance |
| --- | --- | --- |
| R0 — evidence/authority | Review the existing KB authority overlay and current registry; retain historical scores, licenses and disclosure boundaries. | Distinct authorized human review for strategic KB changes; evidence-specific claims. |
| R1 — contracts/code | Review Market #181; finish G06/G18 CLI/protocol work and G21 policy propagation; qualify consumer contracts and compatible dependency pins. | Exact artifact tests and denied-path conformance; no operation authority from registration/schema alone. |
| R2 — provider/custody | Continue owner-specific collateral, revocation, replay, device and independent custodian work. | Fresh authenticated operation/key-bound provider evidence and independent qualification. |
| R3 — runtime/commercial | Resolve real runtime origin and deployment access; wire actual billing, entitlements and measured cost feeds. | Actual health/error/rollback and payment lifecycle evidence for the owning service. |
| R4 — release | Reconcile stale/mutated candidates, then supply genuine acceptance and owner sign-off. | Exact-head required checks plus independent release review. |
| R5 — research/closeout | Retain deferred research by owner; close only evidenced completed work; clean merged branches at accepted sprint exit. | Updated source provenance, no unique work lost, successful preservation checks. |

All 43 current issues still map to the six-phase register. Keep G06/G18 open: codec conformance and diagnostics do not complete facilitator verification, durable replay, paid subscription integration, real registry identity or cross-repository operation negotiation. Keep G21 open until the relevant default policy copies and live enforcement are verified.

## Issue coverage

| Issue | Phase | Work groups |
| --- | --- | --- |
| [.github-private #60: Restricted review coordination](https://github.com/Conxian/.github-private/issues/60) | R4 | G12 |
| [.github-private #63: Restricted review coordination](https://github.com/Conxian/.github-private/issues/63) | R0 | G01 |
| [.github #43: Run org-wide GitHub operating model alignment using issue-only control](https://github.com/Conxian/.github/issues/43) | R0 | G15 |
| [.github #47: Verify security boundary and secret-prevention baseline](https://github.com/Conxian/.github/issues/47) | R0 | G15 |
| [.github #53: Resolve residual public repository presentation metadata from control matrix](https://github.com/Conxian/.github/issues/53) | R0 | G15 |
| [.github #60: chore(licenses): implement approved portfolio metadata, notices, and CI controls](https://github.com/Conxian/.github/issues/60) | R0 | G14 |
| [conxian-business #1317: CXIP?:: Conxian org wide upgrade and refinement proposal ](https://github.com/Conxian/conxian-business/issues/1317) | R0 | G02, G19, G23 |
| [conxian-business #1336: CXIP-1317 Phase C: security-proof, turnkey & fully-online rollout (phased)](https://github.com/Conxian/conxian-business/issues/1336) | R4 | G22 |
| [conxian-business #1343: Unify 3 disjoint billing schemes (gateway/labs-site/nexus/market)](https://github.com/Conxian/conxian-business/issues/1343) | R3 | G08, G17 |
| [conxian-business #1349: [ops] Production surface check failed](https://github.com/Conxian/conxian-business/issues/1349) | R3 | G07, G20 |
| [conxian-business #1359: [SECURITY] Replace remaining long-lived CI credentials with federated auth](https://github.com/Conxian/conxian-business/issues/1359) | R3 | G16 |
| [conxian-business #1390: P0 Epic: Universal capability propagation and deployment readiness](https://github.com/Conxian/conxian-business/issues/1390) | R4 | G05, G22 |
| [conxian-business #1399: P0: Remove AWS root integration and decentralize release signer control](https://github.com/Conxian/conxian-business/issues/1399) | R2 | G09 |
| [conxian-business #1411: P1: Review and upgrade the AI-native CLI across the system graph](https://github.com/Conxian/conxian-business/issues/1411) | R1 | G06 |
| [conxian-business #1414: P2: Rebaseline deferred dependency research by current owner and lock graph](https://github.com/Conxian/conxian-business/issues/1414) | R1 | G02, G03 |
| [conxian-business #1415: P1: Bind immutable promotion candidates to actual PR heads in policy validation](https://github.com/Conxian/conxian-business/issues/1415) | R1 | G21 |
| [conxian-business #936: [BOS-001][Gate 4] Hardware-backed signing/attestation and accountable owner](https://github.com/Conxian/conxian-business/issues/936) | R2 | G09, G10 |
| [conxian-business #937: [BOS-001][Gate 5] Independent security/release acceptance](https://github.com/Conxian/conxian-business/issues/937) | R4 | G12 |
| [conxian-business #940: [Research][FIBO] Pin ontology provenance, notices, and trademark boundary](https://github.com/Conxian/conxian-business/issues/940) | R0 | G14 |
| [conxian-business #989: [STRATEGY]: conxian position research ](https://github.com/Conxian/conxian-business/issues/989) | R5 | G23 |
| [conxian-gateway #189: [RESEARCH] G-1/G-20: BitVM3 adapter — garbled circuits & recursive proof verification](https://github.com/Conxian/conxian-gateway/issues/189) | R5 | G19 |
| [conxian-gateway #466: Deploy gateway: render.yaml merged (#459) but service undeployed (blocked on ~11 secrets)](https://github.com/Conxian/conxian-gateway/issues/466) | R3 | G07 |
| [conxian-gateway #500: Integrate Fireblocks/BitGo institutional custody adapter (shrink value-bearing audit surface)](https://github.com/Conxian/conxian-gateway/issues/500) | R2 | G24 |
| [conxian-gateway #507: Implement MoR billing webhook handler + Neon-backed key store (turnkey core)](https://github.com/Conxian/conxian-gateway/issues/507) | R3 | G08 |
| [conxian-gateway #526: P1: Replace supported_chains count claims with runtime capability negotiation](https://github.com/Conxian/conxian-gateway/issues/526) | R1 | G04 |
| [conxian-gateway #531: P2: Bind fee-policy inputs to measured rail cost and congestion evidence](https://github.com/Conxian/conxian-gateway/issues/531) | R3 | G17 |
| [conxian-labs-site #80: pricing page contradicts server.js managed pricing](https://github.com/Conxian/conxian-labs-site/issues/80) | R3 | G08, G20 |
| [conxian-nexus #174: Governance: restore license policy and complete source/dependency licensing](https://github.com/Conxian/conxian-nexus/issues/174) | R0 | G14 |
| [conxian-nexus #418: P1: Align Nexus observation manifest with canonical chain capability evidence](https://github.com/Conxian/conxian-nexus/issues/418) | R1 | G04 |
| [conxian_market #159: Real x402 subscription payment pointer + non-zero demand (managed tier)](https://github.com/Conxian/conxian_market/issues/159) | R3 | G08, G18 |
| [conxian_market #176: P1: Define and verify x402 v2 and agent identity conformance contracts](https://github.com/Conxian/conxian_market/issues/176) | R1 | G18 |
| [conxius-enclave-sdk #202: [P0] Complete independent security review and release acceptance evidence](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | R4 | G12 |
| [conxius-enclave-sdk #240: [P0] Operationalize attestation roots, collateral, revocation, and distributed replay](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | R2 | G10, G11 |
| [conxius-enclave-sdk #241: [P0] Qualify Android KeyMint/StrongBox authorization and Play Integrity verification](https://github.com/Conxian/conxius-enclave-sdk/issues/241) | R2 | G10 |
| [conxius-enclave-sdk #509: Turnkey KMaaS: pre-attested TEE compute + hardware-enforced threshold signing](https://github.com/Conxian/conxius-enclave-sdk/issues/509) | R2 | G13 |
| [conxius-enclave-sdk #558: P0: Restore fail-closed PR #552 and publish truthful support inventory](https://github.com/Conxian/conxius-enclave-sdk/issues/558) | R1 | G04 |
| [conxius-enclave-sdk #559: P0: Qualify decentralized signing with community-verifiable evidence](https://github.com/Conxian/conxius-enclave-sdk/issues/559) | R2 | G09 |
| [conxius-platform #1167: [ORG-WIDE] Protocol Handoff & Routing Layer Alignment (2026-07-15)](https://github.com/Conxian/conxius-platform/issues/1167) | R4 | G23 |
| [conxius-platform #1168: [RESEARCH] Conxian Protocol Founder Rights & Revenue Routing (2026-07-15)](https://github.com/Conxian/conxius-platform/issues/1168) | R5 | G23 |
| [conxius-platform #1426: P1: Ingest provider capability manifests into the control plane fail closed](https://github.com/Conxian/conxius-platform/issues/1426) | R1 | G04 |
| [conxius-wallet #357: Reduce technical debt and enforce code-quality / mobile-delivery efficiency hardening](https://github.com/Conxian/conxius-wallet/issues/357) | R1 | G20 |
| [conxius-wallet #727: P1: Replace static SDK coverage claims with negotiated wallet capability status](https://github.com/Conxian/conxius-wallet/issues/727) | R1 | G04 |
| [lib-conxian-core #440: P0: Publish canonical universal-chain capability contract for downstream negotiation](https://github.com/Conxian/lib-conxian-core/issues/440) | R1 | G04, G05 |

## Maintenance and cleanup

`git fsck --full`, commit-graph and incremental-repack maintenance passed across **12 local object stores**. Before/after hashes confirm unchanged refs, index bytes and tracked/untracked working content in the 12 checked primary views, including staged Market work. Private KB objects were read remotely rather than cloned.

The refreshed scan identifies **54 unprotected branches with no open PR whose exact tips are ancestors of retained main/staged/dev refs**. They are review candidates, not a deletion log; long-lived/owner retention rules and final head checks still apply. Sprint exit has not been accepted. No remote deletion, GitHub protection change or Project-v2 mutation occurred. Project-v2 and remote ref deletion operations are not exposed by the current connection; Git write credentials are unavailable in the shell.

Confidential review work and earlier automatic publication restrictions remain separate. No restricted patch, security ledger, credential history or private review contents are embedded here.
