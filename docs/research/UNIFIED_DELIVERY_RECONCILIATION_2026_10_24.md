# Unified delivery reconciliation — 24 October 2026

Captured: 2026-10-24T13:13:16.216Z. Authority: [portfolio #1390](https://github.com/Conxian/conxian-business/issues/1390), [promotion #1415](https://github.com/Conxian/conxian-business/issues/1415), [runtime #1349](https://github.com/Conxian/conxian-business/issues/1349), [operations #1423](https://github.com/Conxian/conxian-business/issues/1423). All work remains in one scope; sections express dependencies rather than optional work.

## Current outcome

15 open PRs across eight repositories were inspected at the queue freeze. Failing checks, mutated promotion heads, missing production acceptance, and missing independent review prevent main convergence. No deployment, approval, exception or production pass is inferred from this record. PR #1498 has already integrated the rolling September 24–October 24 research/roadmap/whitepaper alignment into dev; main candidate #1490 predates that work.

The machine-readable companion records full head/base/dev/tree SHAs, parents, checks, reviews, and next action for every candidate. Capture is a snapshot: refresh all refs and every check/status/review page immediately before any merge. GitHub issues/PRs remain the sole engineering records; Projects are optional views and their API was unavailable in this session.

## Section A — dependency remediation (R0/R1)

Current audit jobs report crypto-bigint 0.7.5 and, in some graphs, legacy 0.5.5; ctutils 0.4.2; SDK certificate validation dependencies; and wallet undici/fast-uri/Zod advisories. Prefer compatible patched dependencies with regenerated lockfiles. Do not suppress advisories or mark the graph clean while vulnerable legacy transitive versions remain.

Primary sources: [crypto-bigint RUSTSEC-2026-0387](https://rustsec.org/advisories/RUSTSEC-2026-0387.html), [ctutils RUSTSEC-2026-0385](https://rustsec.org/advisories/RUSTSEC-2026-0385.html), [undici advisory](https://github.com/nodejs/undici/security/advisories/GHSA-4qv8-2p9j-2685), [fast-uri advisory](https://github.com/fastify/fast-uri/security/advisories/GHSA-w74x-v6f9-j3xg), [Zod advisory](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5). Zod major-version overrides across consumers require compatibility analysis; an upgrade alone does not bound unconstrained inputs.

Dependency remediation is in isolated worktrees based on captured dev refs. Lockfile edits and local checks are implementation work, not an accepted release. Full repository verification and hosted exact-head checks must pass before integration.

## Section B — preserve work and repair promotion routes (R0/R4)

Never rewrite an immutable candidate to make its title/source assertion match a changed head. Recover useful changes and merge parents through ordinary work→dev reconciliation; generate a fresh immutable dev→staged candidate from the actual integrated SHA. Preserve staged/main ancestry using explicit merge commits where required. Retain superseded branches until unique work retention is proven.

Tree equality proves equal file content only. It does not establish ancestry, approval, security qualification or production readiness. In particular, a candidate...dev comparison with zero files can merely mean dev is an ancestor: this record separately checks actual Git tree SHAs.

| Candidate | Route | Exact head | Tree equals dev | Next action |
|---|---|---|---|---|
| [lib-conxian-core#492](https://github.com/Conxian/lib-conxian-core/pull/492) | ordinary/backmerge → dev | `1b9ac5d1836a` | Yes | Retain the zero-diff, parent-preserving backmerge; patch current dependency graph, refresh checks and obtain independent review. Preserve both parents when integrating. |
| [conxian-gateway#580](https://github.com/Conxian/conxian-gateway/pull/580) | staged → main | `af6fc1db7ff6` | Yes | Preserve staged/main ancestry and source tree; patch dependency audit on dev, integrate through ordinary reconciliation, then create a fresh immutable promotion with real production evidence. |
| [conxian-nexus#451](https://github.com/Conxian/conxian-nexus/pull/451) | staged → main | `e45b9b4a3153` | No | Reconcile the mutated head with current dev and staged without dropping workflow/recovery changes. Patch dependency audit. Keep restricted security work private. Replace immutable candidate only after retention proof. |
| [lib-conxian-core#491](https://github.com/Conxian/lib-conxian-core/pull/491) | dev → staged | `03ffb430ce96` | Yes | Head differs from named source but tree equals dev. Preserve its staged ancestry via the ordinary backmerge route #492; after dependency fix and review, generate a new immutable candidate. |
| [conxius-wallet#792](https://github.com/Conxian/conxius-wallet/pull/792) | dev → staged | `ddd7f79056b7` | Yes | Head differs from named source but tree equals dev. Integrate parent-preserving ordinary route #791 after audit fix/review; create fresh immutable promotion from resulting dev. |
| [conxius-enclave-sdk#610](https://github.com/Conxian/conxius-enclave-sdk/pull/610) | dev → staged | `7b70c55f4ccc` | Yes | Head differs from named source but tree equals dev. Preserve staged ancestry in a correctly named ordinary reconciliation route together with compatible security dependency fixes; new immutable promotion follows integration. |
| [conxius-enclave-sdk#609](https://github.com/Conxian/conxius-enclave-sdk/pull/609) | dev → staged | `9705a079f9fd` | No | Compare source and merge-parent history with #610, preserve all unique work, and supersede only after the reviewed successor retains it. Do not retitle or force-reset immutable branches to evade source binding. |
| [conxius-wallet#791](https://github.com/Conxian/conxius-wallet/pull/791) | ordinary/backmerge → dev | `7aa1eb291b2b` | Yes | Retain exact dev tree and staged ancestry; audit failure still blocks. Integrate with an explicit merge commit after exact-head checks and independent review, then read back actual dev parents/tree. |
| [conxius-wallet#790](https://github.com/Conxian/conxius-wallet/pull/790) | ordinary/backmerge → dev | `5f6bba90f98b` | No | Retain routine Solana/TypeScript ESLint dependency updates while repairing undici/fast-uri and investigating bounded Zod validation. Refresh dependency exception fingerprints only with measured path evidence and required approvals. |
| [conxius-wallet#785](https://github.com/Conxian/conxius-wallet/pull/785) | staged → main | `a2be57425113` | No | Retain modified promotion head until staged ancestry and all unique changes are verified in a reviewed successor. Review actual binary Gradle wrapper and full lockfile outside truncated patch response. Complete production acceptance. |
| [lib-conxian-core#489](https://github.com/Conxian/lib-conxian-core/pull/489) | staged → main | `d294bf9d2b6e` | No | Preserve main/staged reconciliation and release verification changes. Propagate dependency fixes via dev→staged, regenerate candidate and complete release evidence. |
| [conxian-business#1490](https://github.com/Conxian/conxian-business/pull/1490) | staged → main | `900bb4de8cf7` | No | Reconcile staged ancestry with newer dev work, including #1493–#1498. Preserve monthly research, runtime guardrails and release controls. Verify deployment source and production validation before final main promotion. |
| [conxian_market#195](https://github.com/Conxian/conxian_market/pull/195) | staged → main | `e41e8edfd716` | Yes | Tree equals captured dev, but history differs. Preserve existing exact-head independent approval without transferring it to changed heads; complete candidate-bound production acceptance before main. |
| [conxius-enclave-sdk#606](https://github.com/Conxian/conxius-enclave-sdk/pull/606) | staged → main | `3887e7006d30` | No | Retain existing exact-head independent approval. Incorporate later replay clock fixes through the proper staged route and requalify dependencies/artifacts/provider scope before a fresh main candidate. |
| [conxius-platform#1470](https://github.com/Conxian/conxius-platform/pull/1470) | staged → main | `c857379c4aa6` | Yes | Tree equals captured dev, but main acceptance and independent review remain incomplete. Resolve provider access and verify deployment source/environment; a successful Vercel build is insufficient runtime evidence. |

## Section C — finish runtime contracts (R1/R3)

Business collection pagination remains active: bounded requests, preserved page metadata, validated envelopes and visible incomplete/legacy coverage for audit/releases/policy. Retain existing auth, request timeout, TLS and no-store boundaries. Implement regression checks for malformed pagination and partial coverage. Coordinate Nexus endpoint contracts and separate-instance recovery evidence without treating fixture measurements as production or operator independence.

## Section D — evidence and acceptance (R2/R4)

Complete real candidate-bound CI, build artifacts/provenance, production boundary checks, required provider/device/custody evidence, deployment source/environment readback and accountable-owner acceptance. Existing approvals at SDK #606, Market #195 and Nexus #451 apply only to their recorded commits. Do not borrow another connected identity to self-approve. Missing evidence stays explicitly incomplete while other executable prerequisites continue.

## Section E — research, roadmap, whitepaper and KB (R0–R5)

Use the merged monthly alignment and capability roadmap from #1498; retain historical calendars and distinguish implemented contracts, tested fixtures, qualified operations and deferred research. R0 evidence → R1 bounded contracts → R2 provider/hardware/custody → R3 runtime/commercial → R4 independent release acceptance. R5 research is an ongoing experimental track, not a substitute for sprint exit. Final whitepaper publication remains tied to #1422 acceptance. Private KB #83 holds the internal alignment; restricted security material stays private.

## Completion criteria

1. Every candidate has retained/superseded/integrated disposition with actual commit/tree and ancestry evidence.
2. Every actionable dependency/runtime fix has passed required verification and integrated through its normal route.
3. Every main promotion has genuine applicable review and complete production evidence, with atomic expected-head merge.
4. Read back resulting main/staged/dev and intended deployment source, environment, health and rollback state.
5. Update issue/PR records and KB with observed outcomes; keep unfulfilled external evidence open with accountable next action.

Until those conditions are observed, the unified scope is active and main convergence is incomplete.

## Implementation checkpoint — 2026-10-24T13:30:26.695Z

Five dependency-fix candidates now retain exact local/remote tree evidence:

| Candidate | Verified work | Remaining requirement |
|---|---|---|
| [conxius-enclave-sdk#611](https://github.com/Conxian/conxius-enclave-sdk/pull/611) | 703 passed, 2 ignored; strict all-feature Clippy/fmt passed | crypto-bigint 0.5.5 remains vulnerable; applicable review/promotion/production evidence remains required. |
| [lib-conxian-core#493](https://github.com/Conxian/lib-conxian-core/pull/493) | 324 passed, 2 ignored; strict all-feature Clippy/fmt passed | crypto-bigint 0.5.5 remains vulnerable; applicable review/promotion/production evidence remains required. |
| [conxian-gateway#581](https://github.com/Conxian/conxian-gateway/pull/581) | hosted Test (workspace and mock-integrations), Clippy, fmt and MSRV passed; local bounded rerun in progress | crypto-bigint 0.5.5 remains vulnerable; applicable review/promotion/production evidence remains required. |
| [conxian-nexus#455](https://github.com/Conxian/conxian-nexus/pull/455) | contamination/direct-source pass; full local workspace reaches required missing disposable-PostgreSQL guard; existing hosted fixture workflow in progress | cargo audit 0.22.2: zero vulnerabilities; applicable review/promotion/production evidence remains required. |
| [conxius-wallet#793](https://github.com/Conxian/conxius-wallet/pull/793) | 619 passed, 1 skipped; frozen install, dual TypeScript and production build passed; hosted E2E passed | undici/fast-uri advisories removed; Zod and prior exceptions unresolved; applicable review/promotion/production evidence remains required. |

All five remain drafts. SDK/Core/Wallet parents explicitly retain the existing staged ancestry repair heads. Wallet #790 routine updates remain open and are not included by #793. Gateway and Nexus fixes are based on current dev; they do not resolve all earlier main-promotion history by themselves.

The first parallel native builds exhausted local scratch disk. Interrupted runs are incomplete. Completed task build outputs were cleaned with cargo clean; bounded reruns and the existing hosted workflows provide the subsequent verification. Nexus's full local workspace suite rejects absent CONFORMANCE_DATABASE_URL as designed; full conformance and source-loss recovery evidence must come from the disposable PostgreSQL hosted job. No destructive test ran against an application database.

Registry verification: alloy-signer 2.4.1/2.4.2/2.5.0 still require elliptic-curve ^0.13 and k256 ^0.13; frost-secp256k1-tr 3.0.0 requires k256 ^0.13. A routine latest-version bump alone does not remove legacy crypto-bigint 0.5.5. The coordinated upstream migration or reviewed compatible backport is an active requirement in [dependency maintenance #1414](https://github.com/Conxian/conxian-business/issues/1414). No advisory ignore or signing-feature removal was introduced.
