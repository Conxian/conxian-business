# BOS research candidate ledger — 2026-07-28 (artifact refresh 2026-07-29)

| Metadata | Value |
|---|---|
| Classification | Public-safe bounded evidence ledger |
| Authority | [Business issue #943](https://github.com/Conxian/conxian-business/issues/943) |
| Cycle implementation | [Business PR #970](https://github.com/Conxian/conxian-business/pull/970) |
| Lifecycle and rubric authority | [`GITHUB_FIRST_BOS_OPERATING_MODEL.md`](GITHUB_FIRST_BOS_OPERATING_MODEL.md) |
| Machine-readable record | [`bos_research_candidate_ledger.json`](bos_research_candidate_ledger.json) |
| Deterministic verification | `python3 scripts/verify_bos_research_candidate_ledger.py` |
| Observed date | 2026-07-28 |
| Artifact refresh | 2026-07-29 — CON-1573 decision and Core PR #229/#231 evidence |

This ledger is a dated, bounded scan, **not an exhaustive ecosystem audit**.
Existing owner issues remain canonical for implementation, review, acceptance,
release, and administration. The ledger links those records; it does not create
duplicate umbrellas, replace owner decisions, or reproduce restricted records.

## Selection boundary

Two different selections are preserved:

- **Selected authority:** [Business #943](https://github.com/Conxian/conxian-business/issues/943)
  remains the public-safe lifecycle and rubric authority at **84/100**.
- **Selected next technical candidate:** [Core #227](https://github.com/Conxian/lib-conxian-core/issues/227)
  remains the highest scored technical candidate at **88/100**. Its predecessor
  [Core PR #229](https://github.com/Conxian/lib-conxian-core/pull/229) is merged;
  the current implementation artifact is review-ready
  [Core PR #231](https://github.com/Conxian/lib-conxian-core/pull/231).

Selecting a technical candidate does not complete #943 or transfer technical
ownership to `conxian-business`.

## Rubric and scored candidates

Score vectors use the operating-model order:

`governance/risk (25) + reuse (20) + evidence readiness (15) + dependency unblocking (15) + containment (15) + autonomy (10)`

The JSON companion records each dimension's concise rationale and provenance
links. The validator enforces the exact dimensions and caps, score bounds,
arithmetic totals, unique IDs, dispositions, selection roles, and maximum-score
technical selection.

| Candidate and owner | Score vector | Gap classes | Disposition and next gate | Uncertainty and explicit non-claim |
|---|---:|---|---|---|
| [Core #227](https://github.com/Conxian/lib-conxian-core/issues/227), `Conxian/lib-conxian-core`; [merged PR #229](https://github.com/Conxian/lib-conxian-core/pull/229), [review-ready PR #231](https://github.com/Conxian/lib-conxian-core/pull/231) | **23+16+13+15+15+6 = 88** | dependency-security; implementation; ci-infrastructure; evidence | **Selected technical.** Maintainers decide final release and coordinate exact immutable Nexus repin/validation after review and remaining evidence/admin gates. | The score is preserved from the dated cycle. Residual advisories remain separate. No release, production-readiness, universal-chain-support, Nexus-acceptance, license-resolution, or independent-acceptance claim. |
| [Nexus #169](https://github.com/Conxian/conxian-nexus/issues/169), `Conxian/conxian-nexus`; [PR #172](https://github.com/Conxian/conxian-nexus/pull/172) | **24+17+13+15+14+3 = 86** | dependency-security; implementation; evidence | Retained under owner. Nexus completes review and acceptance evidence in its existing records. | This scan did not re-execute the owner workflow. No ownership transfer, merge, release, or production-acceptance claim. |
| [Business #943](https://github.com/Conxian/conxian-business/issues/943), `Conxian/conxian-business`; [PR #970](https://github.com/Conxian/conxian-business/pull/970) | **23+20+11+13+14+3 = 84** | governance; owner-tracker; evidence | **Selected authority.** Preserve the cycle authority while technical work stays in owner repositories. | Restricted-record, Project, branch, and hosted-execution gates remain unresolved. No #943 completion, migration authorization, branch-model resolution, or technical acceptance claim. |
| Android-first attestation chain, `Conxian/conxius-enclave-sdk`; [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) → [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241)/[#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) → [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202), wallet [#444](https://github.com/Conxian/conxius-wallet/issues/444) | **23+19+11+14+11+4 = 82** | governance; evidence; implementation | Retained under existing owners; provider evidence flows to independent acceptance and then the wallet consumer. | No provider, device, hardware, release, production-support, or independent-acceptance outcome is inferred. |
| [Platform #854](https://github.com/Conxian/conxius-platform/issues/854), `Conxian/conxius-platform` | **24+20+4+15+14+1 = 78** | governance; licensing-admin; evidence | Retained/deferred owner-admin evidence. Owner maintainers supply the required decision and evidence. | Restricted administration state is not inferred. No license resolution, authorization, implementation readiness, or release claim. |
| [Platform #1082](https://github.com/Conxian/conxius-platform/issues/1082), `Conxian/conxius-platform` | **18+18+7+12+14+7 = 76** | workflow-drift; evidence; implementation | Retained under owner. Re-baseline exact workflow/script paths before changing or accepting scope. | The issue snapshot is partly stale. No claim that every issue statement remains current or merge-ready. |
| [Nexus #178](https://github.com/Conxian/conxian-nexus/issues/178), `Conxian/conxian-nexus` | **14+7+15+8+15+10 = 69** | ci-infrastructure; implementation | Independent narrow remediation; record exact CI evidence in the owner issue. | No broader portfolio acceptance or release effect inferred; not part of the #943 implementation. |
| [Gateway #228](https://github.com/Conxian/conxian-gateway/issues/228), `Conxian/conxian-gateway` | **18+11+7+10+14+5 = 65** | dependency-security; implementation; evidence | Retained under owner. Reproduce the current dependency path and record bounded remediation evidence. | No complete dependency/runtime reproduction was performed. No exploitability, completion, release, or production-acceptance claim. |
| [Gateway #189](https://github.com/Conxian/conxian-gateway/issues/189), `Conxian/conxian-gateway` | **17+13+2+9+14+5 = 60** | dependency-security; maintenance; evidence | Research-only/deferred until current reachability, impact, and an implementation gate exist. | Public evidence is preliminary. The score is not vulnerability severity, exploitability, remediation authorization, or release evidence. |

The original #943/attestation/#178 dated scores remain preserved in the
operating model. This expanded ledger adds candidates and records the later
two-layer selection without rewriting that history.

## Selected Core implementation artifact — refreshed 2026-07-29

[Core PR #229](https://github.com/Conxian/lib-conxian-core/pull/229) is merged
to `candidate-base/v0.2.5` at
`60eee84d3279dc73c02376bf2fe8abbfda5a88ce`; prior references describing it as
a draft at head `7a5c83795f473971161c80a117dd35150a4362ca` are stale. Follow-up
[Core PR #231](https://github.com/Conxian/lib-conxian-core/pull/231) is ready for
review at `7edcae397383bd99a9b7a97703d6cab1507a7657`, based on the merged PR #229
commit. PR #231 changes only `Cargo.toml` and `Cargo.lock` to configure BDK with
`default-features = false, features = ["std"]`.

Evidence recorded by the bounded review:

- Exact candidate check, 17 tests, clippy, documentation, and package validation
  pass for PR #231.
- Exact dependency checks show the legacy Electrum TLS path and unused
  Sled/crossbeam-epoch path absent.
- `cargo fmt --check` exposes historical unrelated drift; it is not attributed
  to the manifest/lock-only PR #231 change.
- Residual audit findings are separate work and are not claimed resolved by the
  BDK feature-boundary change.
- Nexus PR #177 was evaluated at its exact head against an equivalent std-only
  Core overlay. Nexus has no direct BDK dependency and did not re-enable BDK
  features; a final immutable Core SHA still requires exact repin validation.

## CON-1573 architecture decision

- **Immediate v0.2 maintenance:** Core uses BDK std-only and enables no
  networking or persistence drivers.
- **Strategic boundary:** Core owns transport-neutral capability and provenance
  contracts. Electrum, Esplora, RPC, light-client, and indexer backends are
  opt-in implementations outside Core in Gateway/backend or other owning
  adapter layers.
- **Verification rule:** TLS authenticates transport; chain-proof validation
  establishes state. Remote observations are not labeled verified unless the
  applicable proof policy succeeds.
- **Scope:** This preserves offline/non-custodial behavior and existing
  multi-chain protocol/adapter surfaces. It does not establish production-
  complete “universal blockchain support.”
- **Release gates:** PR #231 review, final immutable Core SHA, exact Nexus repin
  and downstream validation, release approval, and separate residual-audit
  disposition remain outstanding.

Primary dependency evidence includes the pinned
[BDK v0.30.2 manifest](https://github.com/bitcoindevkit/bdk/blob/f71bc34f32603b887d19d244878442c1895a41ea/Cargo.toml),
[Cargo feature-unification reference](https://github.com/rust-lang/cargo/blob/0158e40d8638a7de292b7242b1533caaf48cbe5f/doc/book/src/reference/features.md),
and pinned RustSec records for
[0098](https://github.com/RustSec/advisory-db/blob/0bfde9d6a469ae503f8a6147c2dd552856cd5999/crates/rustls-webpki/RUSTSEC-2026-0098.md),
[0099](https://github.com/RustSec/advisory-db/blob/0bfde9d6a469ae503f8a6147c2dd552856cd5999/crates/rustls-webpki/RUSTSEC-2026-0099.md), and
[0104](https://github.com/RustSec/advisory-db/blob/0bfde9d6a469ae503f8a6147c2dd552856cd5999/crates/rustls-webpki/RUSTSEC-2026-0104.md).

## Unscored gaps and refinement leads

These entries are deliberately **not numerically scored** and are not new
portfolio umbrellas. An unowned item must have a canonical tracker before it
can enter a later comparable scorecard.

| Gap | Gap class | Disposition and next gate | Boundary |
|---|---|---|---|
| [`RUSTSEC-2026-0204` crossbeam-epoch](https://rustsec.org/advisories/RUSTSEC-2026-0204.html), observed in the Core v0.2 candidate and current Core main; patched at `>=0.9.20`; tested lock-only path | dependency-security; owner-tracker | `tracker-required-before-scoring`; identify/create Core/Nexus owner tracker and reproduce exact reachability. | Lock presence is not runtime reachability, exploitability, severity, or acceptance. |
| [`RUSTSEC-2026-0185` quinn-proto](https://rustsec.org/advisories/RUSTSEC-2026-0185.html), v0.2 candidate only; patched at `>=0.11.15` | dependency-security; owner-tracker | `tracker-required-before-scoring`; create/identify Core tracker and test compatibility. | No current-main, exploitability, or release-blocking claim. |
| [`RUSTSEC-2026-0190` anyhow](https://rustsec.org/advisories/RUSTSEC-2026-0190.html), v0.2 candidate only; patched at `>=1.0.103` | dependency-security; owner-tracker | `tracker-required-before-scoring`; create/identify Core tracker and test compatibility. | No current-main, exploitability, or release-blocking claim. |
| Historical v0.2 Dependency Review action SHA pinning | ci-infrastructure; workflow-drift; owner-tracker | `tracker-required-before-scoring`; use reviewed immutable action references before relying on hosted analysis. | The failed workflow is not a dependency or code finding. |
| Historical v0.2 rustfmt drift | formatting-hygiene; owner-tracker | `tracker-required-before-scoring`; establish a bounded owner baseline. | Unchanged-file drift is not attributed to PR #229. |
| Unmaintained dependency research: async-std; Arkworks/derivative; BDK/sled/fxhash/instant; ALuVM/RGB/paste | maintenance; dependency-security where applicable; owner-tracker | `tracker-required-before-scoring`; split by exact consumer and owner before scoring. | These are research leads, not a complete consumer inventory, reachability result, or replacement mandate. |
| Existing lower-scope owner trackers: [conxian.github.io #3](https://github.com/Conxian/conxian.github.io/issues/3), [conxian-labs-site #59](https://github.com/Conxian/conxian-labs-site/issues/59)/[#60](https://github.com/Conxian/conxian-labs-site/issues/60), [conxius-orbit #278](https://github.com/Conxian/conxius-orbit/issues/278)/[#279](https://github.com/Conxian/conxius-orbit/issues/279), [conxian_ui #161](https://github.com/Conxian/conxian_ui/issues/161), [conxian_market #9](https://github.com/Conxian/conxian_market/issues/9) | owner-tracker; implementation | `retained-existing-owner`; score only if selected in a later bounded cycle. | Minimum-necessary tracker observation only; no restricted-repository detail, reprioritization, readiness, or acceptance claim. |

## Refresh rules

1. Preserve this dated ledger and its score history; add a dated refresh rather
   than silently changing the 2026-07-28 decision.
2. Re-score only when a linked fact changes and record the changed provenance,
   uncertainty, and non-claim.
3. Keep selected authority and selected technical candidate as separate fields.
4. Do not score an unowned gap until a canonical tracker exists.
5. Keep implementation and acceptance evidence in the owning repository.
6. Re-run the validator and focused tests; a no-fact-change refresh must produce
   no semantic change.

## August 2026 Workspace Security Override and Dependabot Audit Refresh

An August 2026 workspace-wide Dependabot audit and remediation pass was executed:
- **Root workspace overrides:** Enforced in `pnpm-workspace.yaml` for `next@^16.2.11`, `postcss@^8.5.18`, `sharp@^0.35.0`, `nanoid@^3.3.18`, `tar@^7.5.0`, `brace-expansion@^2.0.2`, `undici@^7.21.0`, `js-yaml@^4.1.1`, `fast-uri@^3.1.0`, `bigint-buffer@^1.1.5`, `vite@^6.2.1`, `ws@^8.18.1`, and `form-data@^4.0.2`.
- **Audit Verification:** `pnpm audit` verified that all 8 fixable high/critical severity security alerts across `conxian-ui`, `conxius-platform`, `conxian-gateway`, and workspace applications are resolved.
- **Unfixable upstream dependencies:** `elliptic` and `bigint-buffer` maintain unpatched status (`<0.0.0` upstream fixes available), mitigated via input validation boundary checks and workspace isolation.
