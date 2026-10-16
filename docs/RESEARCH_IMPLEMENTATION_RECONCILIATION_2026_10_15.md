# Research, implementation and phased work reconciliation — 15 October 2026

> Current operational overlay: [16 October organization state](audits/2026-10-16-current-org-state.md). The original inventory and scores below remain dated evidence.

Status: proposed current coordination checkpoint. Parent: [Business #1390](https://github.com/Conxian/conxian-business/issues/1390); research authority: [Business #1317](https://github.com/Conxian/conxian-business/issues/1317). Repository owners retain implementation and acceptance authority.

This record reconciles the knowledge-base/audit/research inventory with current source and existing work. Historical scores and evidence are retained. It does not authorize production, redefine fees or custody, replace independent review, or claim that every historical source was independently audited.

## Coverage

Indexed **1,735 public document versions** across all retained current branch heads in 12 public repositories, plus **54 private KB documents** at the pinned main revision: **1,789 catalog entries**. The index includes research, audits, plans, KBs, debt, readiness, evidence and supporting guidance. Confidential security-packet contents are excluded. Main/staged/dev and active proposal differences remain distinguishable by exact references.

All **43 open issue records** at this checkpoint have a primary phase and links to **24 reconciled work groups**. Five focused gaps received trackers: KB #63, Business #1414/#1415, Market #176 and Gateway #531. This adds missing work without duplicating existing implementation/acceptance umbrellas.

Historical archived/deleted repository paths return 404 with this connection; old references are retained as unverified leads. GitHub Project-v2 operations are not exposed by the current connection. Phase alignment is recorded in existing issues; no Project board/field update is claimed.

## Material reconciliation decisions

- The KB enabled/production-authorized labels need capability-specific evidence reconciliation against newer zero-production-support SDK records. Preserve independently accepted capabilities and CAPABILITY_GATES.json until an independently reviewed compatible migration is accepted.
- G3 Market SDK consumers exist in Wallet and Platform; G5 Enterprise mapping plus conformance fixtures exists; G6 bridge naming exists; G8 hysteresis/cost/load helpers exist. Their original trackers are closed. Measured runtime cost/congestion feeds are separate missing work under Gateway #531.
- Core #227 describes legacy v0.2 dependency remediation, Market #9 repository governance, Gateway #102 a historical PR, and Nexus #169/#172 Groth16 state binding. Old gap-table labels are not current issue evidence.
- The 11 scored / 16 unscored ledger remains dated history. Its old dependency thresholds are already met in current locks where applicable; remaining maintenance research is owner-specific under Business #1414.
- SDK #545 and Wallet #732 have merged since the earlier PR report. Their newer promotion candidates are #575 and #733. Source merges do not prove deployment or independent acceptance.
- Old external TVL, revenue, market-size, standard/alliance and regulatory-mandate claims are historical research until independently revalidated. Priority scores are not evidence grades or release approvals.

## Dependency-ordered phases

These are coordination lanes, not a new global enablement switch. Read-only and independently accepted capabilities can progress without unrelated provider gates. Apply hardware/custody dependencies only to the operation that needs them.

| Phase | Work | Entry | Exit evidence |
|---|---|---|---|
| R0 | Evidence and authority | Inventory current source and existing owner trackers. | Claims have dated provenance; contradictions, restricted boundaries and owner decisions are explicit. |
| R1 | Contracts and bounded implementation | A specific owner, contract and negative acceptance criteria exist. | Exact-head code and consumer conformance pass; implementation presence remains separate from runtime qualification. |
| R2 | Provider, hardware and custody evidence | Relevant operation contracts and owner-approved provider scope exist. | Authenticated fresh provider evidence, replay/revocation and actual key/operation binding are independently accepted. |
| R3 | Runtime and commercial integration | A real runtime/provider contract and accountable operator exist. | Actual deployment, data lifecycle, billing/entitlement, failures and rollback are demonstrated for the named capability. |
| R4 | Release and independent acceptance | The exact artifact has its relevant contract/provider/runtime evidence. | Required CI, independent review, owner sign-off and real acceptance evidence bind the immutable release candidate. |
| R5 | Deferred research and experiments | A bounded hypothesis and primary source are recorded. | Evidence supports a separate owner-approved pilot proposal, or the candidate remains explicitly deferred. |

## Current work register

| Gap | Phase / priority / state | Owner and canonical trackers | Next concrete action |
|---|---|---|---|
| G01: Reconcile KB authority and capability claims | R0 / P0 / evidence-missing | Conxian/.github-private; [.github-private#63](https://github.com/Conxian/.github-private/issues/63) | Trace every enabled claim to its own current artifact, provider proof and accountable acceptance; publish the current navigation overlay. |
| G02: Correct stale tracker and artifact mappings | R0 / P1 / coordination | Conxian/conxian-business; [conxian-business#1317](https://github.com/Conxian/conxian-business/issues/1317), [conxian-business#1414](https://github.com/Conxian/conxian-business/issues/1414) | Use the dated current overlay; keep the 11 scored and 16 unscored historical rows intact. |
| G03: Rebaseline deferred dependency maintenance | R1 / P2 / evidence-missing | Conxian/conxian-business; [conxian-business#1414](https://github.com/Conxian/conxian-business/issues/1414) | Identify exact feature/reachability paths and upstream maintenance evidence before selecting owner-specific changes. |
| G04: Propagate qualified operation contracts to consumers | R1 / P1 / integration-missing | Conxian/lib-conxian-core; [lib-conxian-core#440](https://github.com/Conxian/lib-conxian-core/issues/440), [conxian-gateway#526](https://github.com/Conxian/conxian-gateway/issues/526), [conxian-nexus#418](https://github.com/Conxian/conxian-nexus/issues/418), [conxius-platform#1426](https://github.com/Conxian/conxius-platform/issues/1426), [conxius-wallet#727](https://github.com/Conxian/conxius-wallet/issues/727), [conxius-enclave-sdk#558](https://github.com/Conxian/conxius-enclave-sdk/issues/558) | Add cross-repo contract fixtures and qualified operation producers; preserve the implemented diagnostic registrations. |
| G05: Coordinate dependency pins and release propagation | R1 / P1 / integration-missing | Conxian/lib-conxian-core; [lib-conxian-core#440](https://github.com/Conxian/lib-conxian-core/issues/440), [conxian-business#1390](https://github.com/Conxian/conxian-business/issues/1390) | Choose immutable compatible SDK/Core candidates and validate each downstream consumer before repinning. |
| G06: Complete the system graph CLI and installer contract | R1 / P1 / integration-missing | Conxian/conxian-business; [conxian-business#1411](https://github.com/Conxian/conxian-business/issues/1411) | Continue versioned schemas, transport/errors and bounded authenticated diagnostics from the existing tested first slice. |
| G07: Verify the admin and service runtime | R3 / P0 / evidence-missing | Conxian/conxian-business; [conxian-business#1349](https://github.com/Conxian/conxian-business/issues/1349), [conxian-gateway#466](https://github.com/Conxian/conxian-gateway/issues/466) | Verify an actual HTTPS admin/runtime origin and scoped read/write authorization before configuration or deployment. |
| G08: Implement real billing, entitlement and provisioning | R3 / P1 / integration-missing | Conxian/conxian-gateway; [conxian-gateway#507](https://github.com/Conxian/conxian-gateway/issues/507), [conxian_market#159](https://github.com/Conxian/conxian_market/issues/159), [conxian-labs-site#80](https://github.com/Conxian/conxian-labs-site/issues/80), [conxian-business#1343](https://github.com/Conxian/conxian-business/issues/1343) | Wire the owner-approved billing contract, signed/idempotent webhook, durable key lifecycle and actual subscription resolver. |
| G09: Remove root dependence and prove independent custody | R2 / P0 / evidence-missing | Conxian/conxian-business; [conxian-business#1399](https://github.com/Conxian/conxian-business/issues/1399), [conxius-enclave-sdk#559](https://github.com/Conxian/conxius-enclave-sdk/issues/559), [conxian-business#936](https://github.com/Conxian/conxian-business/issues/936) | Obtain current least-privilege identity, independently controlled custodians and exact operation/release proof. |
| G10: Qualify actual hardware providers and client authorization | R2 / P0 / evidence-missing | Conxian/conxius-enclave-sdk; [conxius-enclave-sdk#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240), [conxius-enclave-sdk#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241), [conxian-business#936](https://github.com/Conxian/conxian-business/issues/936) | Follow the existing provider matrix and obtain real device/firmware/driver, key-confinement and operation-binding evidence. |
| G11: Operationalize collateral, revocation and durable replay | R2 / P0 / integration-missing | Conxian/conxius-enclave-sdk; [conxius-enclave-sdk#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | Bind authenticated fresh collateral and atomic consume-once behavior to real provider operations and recovery tests. |
| G12: Complete independent security and release acceptance | R4 / P0 / evidence-missing | Conxian/conxius-enclave-sdk; [conxius-enclave-sdk#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202), [conxian-business#937](https://github.com/Conxian/conxian-business/issues/937) | Arrange distinct authorized reviewers for exact artifacts and keep restricted details outside Git/GitHub. |
| G13: Implement qualified KMaaS and challenge execution | R2 / P1 / integration-missing | Conxian/conxius-enclave-sdk; [conxius-enclave-sdk#509](https://github.com/Conxian/conxius-enclave-sdk/issues/509) | Implement typed amount/asset/network policy and actual provider execution only after the recorded acceptance contracts are met. |
| G14: Reconcile licenses and semantic-source provenance | R0 / P1 / evidence-missing | Conxian/conxian-business; [.github#60](https://github.com/Conxian/.github/issues/60), [conxian-nexus#174](https://github.com/Conxian/conxian-nexus/issues/174), [conxian-business#940](https://github.com/Conxian/conxian-business/issues/940) | Retain current repository licenses and obtain owner/counsel decisions for notices, policy and semantic-source intake. |
| G15: Verify organization controls and current repository roles | R0 / P1 / evidence-missing | Conxian/.github; [.github#43](https://github.com/Conxian/.github/issues/43), [.github#47](https://github.com/Conxian/.github/issues/47), [.github#53](https://github.com/Conxian/.github/issues/53) | Verify owner-controlled settings and presentation against current visibility; retain inaccessible historical repositories as unverified leads. |
| G16: Complete federated authentication cutovers | R3 / P1 / evidence-missing | Conxian/conxian-business; [conxian-business#1359](https://github.com/Conxian/conxian-business/issues/1359) | Validate provider-owned federated role/canary/cutover evidence for each real workflow without copying credentials. |
| G17: Supply measured cost and congestion inputs to fee policy | R3 / P2 / integration-missing | Conxian/conxian-gateway; [conxian-gateway#531](https://github.com/Conxian/conxian-gateway/issues/531), [conxian-business#1343](https://github.com/Conxian/conxian-business/issues/1343) | Connect measured input provenance/freshness outside Core; preserve configured floors as configured policy. |
| G18: Qualify versioned agent/payment protocol compatibility | R1 / P1 / integration-missing | Conxian/conxian_market; [conxian_market#176](https://github.com/Conxian/conxian_market/issues/176), [conxian_market#159](https://github.com/Conxian/conxian_market/issues/159) | Select and test explicit x402 HTTP/MCP schemas and distinguish semantic identity adapters from ERC-8004 wire/deployed-registry compatibility. |
| G19: Revalidate research-only protocol and sovereignty proposals | R5 / P2 / deferred-research | Conxian/conxian-business; [conxian-business#1317](https://github.com/Conxian/conxian-business/issues/1317), [conxian-gateway#189](https://github.com/Conxian/conxian-gateway/issues/189) | Revalidate primary sources and bounded adapter hypotheses before promoting BitVM3, RGB fork, Stacks/sBTC, ZKML or sovereignty pilots. |
| G20: Maintain mobile, UX and public-surface truth | R1 / P2 / integration-missing | Conxian/conxius-wallet; [conxius-wallet#357](https://github.com/Conxian/conxius-wallet/issues/357), [conxian-labs-site#80](https://github.com/Conxian/conxian-labs-site/issues/80), [conxian-business#1349](https://github.com/Conxian/conxian-business/issues/1349) | Continue concrete mobile/debt work and verify public/deployed surfaces against accepted capability evidence. |
| G21: Bind promotion policy to actual immutable heads | R1 / P1 / integration-missing | Conxian/conxian-business; [conxian-business#1415](https://github.com/Conxian/conxian-business/issues/1415) | Add actual PR-head binding for immutable dev/staged candidates and test missing/mismatched head evidence. |
| G22: Complete phased rollout with exact acceptance evidence | R4 / P0 / evidence-missing | Conxian/conxian-business; [conxian-business#1336](https://github.com/Conxian/conxian-business/issues/1336), [conxian-business#1390](https://github.com/Conxian/conxian-business/issues/1390) | Accept and release each capability only when its own exact artifact, checks, relevant provider/runtime proof and owner/reviewer gates pass. |
| G23: Revalidate positioning and economic research | R5 / P2 / deferred-research | Conxian/conxian-business; [conxian-business#989](https://github.com/Conxian/conxian-business/issues/989), [conxian-business#1317](https://github.com/Conxian/conxian-business/issues/1317), [conxius-platform#1168](https://github.com/Conxian/conxius-platform/issues/1168), [conxius-platform#1167](https://github.com/Conxian/conxius-platform/issues/1167) | Separate owner decisions, historical projections and primary-source observations before scoring or commercial adoption. |
| G24: Complete institutional custody provider integration | R2 / P1 / integration-missing | Conxian/conxian-gateway; [conxian-gateway#500](https://github.com/Conxian/conxian-gateway/issues/500) | Obtain an actual institution/provider account and qualified adapter contract with audited authorization and recovery behavior. |

## Implementation evidence and acceptance

The links are immutable source references. Existing test records establish only their stated scope; this documentation pass does not re-run every historical suite.

### G01 — Reconcile KB authority and capability claims

Sources: [.github-private/docs/CAPABILITY_GATES.json](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/CAPABILITY_GATES.json) (`8160417a2574`); [.github-private/docs/index.md](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/index.md) (`8160417a2574`).

Observed implementation: [conxius-enclave-sdk/docs/architecture/capability-evidence.json](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/capability-evidence.json) (`2e2aaa8012ae`).

- Preserve independently accepted capabilities; do not apply a blanket enable/disable.
- Retain CAPABILITY_GATES.json and historical scores until a reviewed compatible migration is accepted.
- A code feature, version, registry entry or signature is not production authority.

### G02 — Correct stale tracker and artifact mappings

Sources: [conxian-business/docs/GAPS.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/GAPS.md) (`3185f59ec8e0`); [conxian-business/docs/bos_research_candidate_ledger.json](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/bos_research_candidate_ledger.json) (`3185f59ec8e0`).

- Core #227 is a v0.2 dependency candidate, not a BitVM settlement implementation.
- Market #9 is repository governance, not an escrow implementation tracker.
- Gateway #102 is a historical PR, not a current open verification issue.
- Nexus #169/#172 concern Groth16 state-transition binding, not generic dependency remediation.

### G03 — Rebaseline deferred dependency maintenance

Sources: [conxian-business/docs/bos_research_candidate_ledger.json](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/bos_research_candidate_ledger.json) (`3185f59ec8e0`).

Observed implementation: [lib-conxian-core/Cargo.lock](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/Cargo.lock) (`c85dae282cab`); [conxian-nexus/Cargo.lock](https://github.com/Conxian/conxian-nexus/blob/104458dbb39548ab56550e0f8a3216b45bd9ab50/Cargo.lock) (`104458dbb395`); [conxian-gateway/Cargo.lock](https://github.com/Conxian/conxian-gateway/blob/0b15b59e2c1f031db0049ad36e6b8125f0918174/Cargo.lock) (`0b15b59e2c1f`); [conxius-enclave-sdk/Cargo.lock](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/Cargo.lock) (`2e2aaa8012ae`); [conxian-business/Cargo.lock](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/Cargo.lock) (`3185f59ec8e0`).

- Old crossbeam/quinn/anyhow thresholds are already met where those crates occur in current dev.
- Derivative/paste/ALuVM maintenance paths still need owner-specific disposition.
- Do not turn lock presence into an exploitability claim or add broad advisory ignores.

### G04 — Propagate qualified operation contracts to consumers

Sources: [lib-conxian-core/docs/CAPABILITY_CONTRACT.md](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/docs/CAPABILITY_CONTRACT.md) (`c85dae282cab`).

Observed implementation: [lib-conxian-core/examples/chain_taxonomy.rs](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/examples/chain_taxonomy.rs) (`c85dae282cab`); [conxian-gateway/docs/CAPABILITY_DISCOVERY.md](https://github.com/Conxian/conxian-gateway/blob/0b15b59e2c1f031db0049ad36e6b8125f0918174/docs/CAPABILITY_DISCOVERY.md) (`0b15b59e2c1f`); [conxius-platform/docs/architecture/PROVIDER_REGISTRATION_DISCOVERY_2026.md](https://github.com/Conxian/conxius-platform/blob/1b9baa4696bb3c46c50d1a79c158706ec9c31941/docs/architecture/PROVIDER_REGISTRATION_DISCOVERY_2026.md) (`1b9baa4696bb`); [conxius-wallet/docs/operations/CAPABILITY_TRUTH.md](https://github.com/Conxian/conxius-wallet/blob/101f0cfce2308b879810c58b57b9c1f586d17a39/docs/operations/CAPABILITY_TRUTH.md) (`101f0cfce230`).

- Exact chain/network/operation identity and source evidence are bound.
- Health/registration presence cannot qualify signing, finality or payment.
- Unknown, stale, untrusted or unsupported evidence remains unavailable.

### G05 — Coordinate dependency pins and release propagation

Sources: [lib-conxian-core/docs/MIGRATION.md](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/docs/MIGRATION.md) (`c85dae282cab`).

Observed implementation: [lib-conxian-core/Cargo.toml](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/Cargo.toml) (`c85dae282cab`); [conxian-gateway/Cargo.toml](https://github.com/Conxian/conxian-gateway/blob/0b15b59e2c1f031db0049ad36e6b8125f0918174/Cargo.toml) (`0b15b59e2c1f`); [conxian-nexus/Cargo.toml](https://github.com/Conxian/conxian-nexus/blob/104458dbb39548ab56550e0f8a3216b45bd9ab50/Cargo.toml) (`104458dbb395`).

- Core uses SDK b3d79d9 while separate POC/test declarations retain v2.0.17.
- Gateway Core v0.3.3 and Nexus Core b85625f do not automatically consume current dev.
- A bump, tag or submodule sync alone cannot establish release acceptance.

Relevant work dependencies: G04.

### G06 — Complete the system graph CLI and installer contract

Sources: [conxian-business/docs/architecture/FULL_SCOPE_IMPLEMENTATION_CHECKLIST.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/architecture/FULL_SCOPE_IMPLEMENTATION_CHECKLIST.md) (`3185f59ec8e0`).

Observed implementation: [conxian_market/bin/conxian-agent-init.mjs](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/bin/conxian-agent-init.mjs) (`95ee29a79993`); [conxian_market/src/client_onboarding.ts](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/src/client_onboarding.ts) (`95ee29a79993`).

- Preserve no-key/no-network/no-write local preview behavior.
- Read/plan/apply and idempotency require a qualified owner operation; no fabricated provisioning.
- Reconcile the existing Gateway installer rather than building a second installer.

Relevant work dependencies: G04.

### G07 — Verify the admin and service runtime

Sources: [conxian-business/docs/audits/2026-10-11-deployment-readiness.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/audits/2026-10-11-deployment-readiness.md) (`3185f59ec8e0`).

Observed implementation: [conxian-business/docs/architecture/CONTROL_PLANE_ADMIN_RUNTIME_API_CONTRACT.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/architecture/CONTROL_PLANE_ADMIN_RUNTIME_API_CONTRACT.md) (`3185f59ec8e0`).

- No marketing URL, sample-data fallback or fabricated governance rows.
- Demonstrate service health/dependencies, schema, errors and rollback on the exact artifact.
- Historical disconnected/undeployed labels are not fresh provider observations.

Relevant work dependencies: G04.

### G08 — Implement real billing, entitlement and provisioning

Sources: [conxian-business/docs/TURNKEY_SELF_SERVE_GAP_ANALYSIS.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/TURNKEY_SELF_SERVE_GAP_ANALYSIS.md) (`3185f59ec8e0`).

Observed implementation: [conxian-labs-site/server.js](https://github.com/Conxian/conxian-labs-site/blob/7bdece931d82505771101b1ef59011771abecf90/server.js) (`7bdece931d82`); [conxian_market/src/client_onboarding.ts](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/src/client_onboarding.ts) (`95ee29a79993`).

- Site #86 truthful unavailable signup is implemented on dev; it is not payment integration.
- Keep trust tier, subscription tier and settlement fee as distinct concepts.
- Real payment verification, quota/expiry/revocation and dunning need provider-backed tests.

Relevant work dependencies: G07, G18.

### G09 — Remove root dependence and prove independent custody

Sources: [.github-private/docs/DECENTRALISED_RELEASE_CEREMONY.md](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/DECENTRALISED_RELEASE_CEREMONY.md) (`8160417a2574`).

Observed implementation: [conxius-enclave-sdk/docs/architecture/decentralized-signing-inventory.json](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/decentralized-signing-inventory.json) (`2e2aaa8012ae`).

- Three P-256 challenge signatures do not prove threshold signing, Bitcoin signing or separate custody.
- Do not infer root access-key existence from an identity response.
- No new infrastructure or custody changes are authorized by this inventory.

### G10 — Qualify actual hardware providers and client authorization

Sources: [conxius-enclave-sdk/docs/architecture/HARDWARE_SIGNING_PROVIDER_MATRIX_2026.md](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/HARDWARE_SIGNING_PROVIDER_MATRIX_2026.md) (`2e2aaa8012ae`).

Observed implementation: [conxius-enclave-sdk/src/enclave/attestation.rs](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/src/enclave/attestation.rs) (`2e2aaa8012ae`).

- Android chain/signatures/root/security-level and current revocation must verify.
- Provider names and PKCS#11 C_Verify are inventory/operation facts, not hardware provenance.
- Keep client authorization, platform attestation and actual protocol-key custody separate.

Relevant work dependencies: G04.

### G11 — Operationalize collateral, revocation and durable replay

Sources: [conxius-enclave-sdk/docs/architecture/ISSUE-240_PHASE_A_CONTRACT.md](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/ISSUE-240_PHASE_A_CONTRACT.md) (`2e2aaa8012ae`).

Observed implementation: [conxius-enclave-sdk/src/enclave/durable_replay.rs](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/src/enclave/durable_replay.rs) (`2e2aaa8012ae`).

- Traits and single-process cache tests do not establish a distributed service.
- Reject stale/revoked/wrong-root and replayed operation evidence.
- Prove behavior across restart, replicas and recovery under the owner-selected backend.

Relevant work dependencies: G10.

### G12 — Complete independent security and release acceptance

Sources: [conxius-enclave-sdk/docs/audits/INDEPENDENT_SECURITY_REVIEW_RFP_2026-10-10.md](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/audits/INDEPENDENT_SECURITY_REVIEW_RFP_2026-10-10.md) (`2e2aaa8012ae`).

- CI success, a merged packet or general user approval is not independent acceptance.
- Provider/custody evidence is required only for the capability being accepted.
- Sanitized coordination metadata may reference a pending restricted review without publishing reproduction details.

Relevant work dependencies: G04.

### G13 — Implement qualified KMaaS and challenge execution

Sources: [conxius-enclave-sdk/docs/architecture/WATCHTOWER_KMAAS_POLICY_BOUNDARY_2026_10_15.md](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/WATCHTOWER_KMAAS_POLICY_BOUNDARY_2026_10_15.md) (`2e2aaa8012ae`).

- The consolidated #545 documentation is now merged; its runtime was unchanged.
- In-memory challenge bookkeeping and malformed context cannot authorize spending or claim execution.
- Require hardware policy proof, durable replay and authenticated operation evidence.

Relevant work dependencies: G10, G11.

### G14 — Reconcile licenses and semantic-source provenance

Sources: [conxian-business/docs/governance/EXTERNAL_SEMANTIC_SOURCE_INTAKE_POLICY.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/governance/EXTERNAL_SEMANTIC_SOURCE_INTAKE_POLICY.md) (`3185f59ec8e0`).

Observed implementation: [conxian-nexus/LICENSE](https://github.com/Conxian/conxian-nexus/blob/104458dbb39548ab56550e0f8a3216b45bd9ab50/LICENSE) (`104458dbb395`); [conxian-business/governance/external-semantic-sources.json](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/governance/external-semantic-sources.json) (`3185f59ec8e0`).

- Nexus LICENSE fields are populated; the old placeholder claim is stale.
- Source available is not equivalent to OSI open source.
- No relicensing, trademark approval or legal conclusion is inferred.

### G15 — Verify organization controls and current repository roles

Sources: [.github-private/docs/ECOSYSTEM_REGISTRY.json](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/ECOSYSTEM_REGISTRY.json) (`8160417a2574`).

- Business is currently public.
- A workflow file does not prove server-side branch protection, push protection or owner policy.
- The current tools expose no Project-v2 read/write operation; issue records carry the phase mapping.

### G16 — Complete federated authentication cutovers

Sources: [conxian-business/docs/audits/2026-10-11-deployment-readiness.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/audits/2026-10-11-deployment-readiness.md) (`3185f59ec8e0`).

- No blanket credential rotation or new secret values.
- Role trust/permissions and rollback need owner evidence for the actual environment.

### G17 — Supply measured cost and congestion inputs to fee policy

Sources: [.github-private/docs/GAP_EXPANSION_2026_10_02.md](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/GAP_EXPANSION_2026_10_02.md) (`8160417a2574`).

Observed implementation: [lib-conxian-core/src/fee.rs](https://github.com/Conxian/lib-conxian-core/blob/c85dae282cab9e45829a986385469d3923927d12/src/fee.rs) (`c85dae282cab`); [conxian-nexus/tests/billing_fee_conformance.rs](https://github.com/Conxian/conxian-nexus/blob/104458dbb39548ab56550e0f8a3216b45bd9ab50/tests/billing_fee_conformance.rs) (`104458dbb395`); [conxius-wallet/services/settlement.ts](https://github.com/Conxian/conxius-wallet/blob/101f0cfce2308b879810c58b57b9c1f586d17a39/services/settlement.ts) (`101f0cfce230`); [conxius-platform/services/admin-dashboard/src/lib/support/settlement.ts](https://github.com/Conxian/conxius-platform/blob/1b9baa4696bb3c46c50d1a79c158706ec9c31941/services/admin-dashboard/src/lib/support/settlement.ts) (`1b9baa4696bb`).

- G3 wiring, G5 enterprise mapping, G6 rename and G8 pure helpers exist; do not repeat them.
- Static estimates and mapping functions are not live observations.
- Any fee/economic policy change remains an owner decision.

### G18 — Qualify versioned agent/payment protocol compatibility

Sources: [.github-private/docs/RESEARCH_GAP_INVENTORY_2026_09_29.md](https://github.com/Conxian/.github-private/blob/8160417a25748b753a4104c5a67a031d701cff1c/docs/RESEARCH_GAP_INVENTORY_2026_09_29.md) (`8160417a2574`).

Observed implementation: [conxian_market/src/x402_facade.ts](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/src/x402_facade.ts) (`95ee29a79993`); [conxian_market/src/agent_registry.ts](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/src/agent_registry.ts) (`95ee29a79993`); [conxian_market/src/mcp_402.ts](https://github.com/Conxian/conxian_market/blob/95ee29a7999347243417b4369c61afbd3a98c48b/src/mcp_402.ts) (`95ee29a79993`).

- Current facade is local sats/payment-pointer data, not demonstrated x402 v2 transport conformance.
- ERC-8004 is Draft at this source check and treats payments as a separate concern.
- No automatic paid execution, custody or commercial commitment is added.

### G19 — Revalidate research-only protocol and sovereignty proposals

Sources: [conxian-business/docs/RESEARCH_BTC_L2_2026.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/RESEARCH_BTC_L2_2026.md) (`3185f59ec8e0`); [conxius-enclave-sdk/docs/architecture/GAP_SCORECARD.md](https://github.com/Conxian/conxius-enclave-sdk/blob/2e2aaa8012aea14496748143dec45fd923114315/docs/architecture/GAP_SCORECARD.md) (`2e2aaa8012ae`).

- Do not adopt old TVL, performance, market-size, mandate or alliance claims as current evidence.
- Kwil/Tableland, Radicle, Akash, multi-federation and ZKML remain separate pilots/research until accepted.
- No mass reimplementation or protocol replacement follows from a research score.

### G20 — Maintain mobile, UX and public-surface truth

Sources: [conxius-wallet/docs/operations/TECHNICAL_DEBT_REGISTER.md](https://github.com/Conxian/conxius-wallet/blob/101f0cfce2308b879810c58b57b9c1f586d17a39/docs/operations/TECHNICAL_DEBT_REGISTER.md) (`101f0cfce230`).

Observed implementation: [conxius-wallet/docs/operations/CAPABILITY_TRUTH.md](https://github.com/Conxian/conxius-wallet/blob/101f0cfce2308b879810c58b57b9c1f586d17a39/docs/operations/CAPABILITY_TRUTH.md) (`101f0cfce230`).

- Historical phase-complete labels do not mean all mobile protocols, native managers or provider paths are complete.
- Keep .org developer/protocol and .com commercial managed-service boundaries accurate.

### G21 — Bind promotion policy to actual immutable heads

Sources: [conxian-business/scripts/branch_promotion_policy.py](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/scripts/branch_promotion_policy.py) (`3185f59ec8e0`).

Observed implementation: [conxian-business/scripts/branch_promotion_policy.py](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/scripts/branch_promotion_policy.py) (`3185f59ec8e0`).

- Matching branch/source strings are not sufficient head evidence.
- Preserve valid feature and reviewed reconciliation paths.
- Mechanical policy success cannot certify a human acceptance pack.

### G22 — Complete phased rollout with exact acceptance evidence

Sources: [conxian-business/docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md) (`3185f59ec8e0`).

- Do not label independent review the only missing cell.
- Keep clean merges, CI, deployment, custody, support and release state separate.
- No blanket freeze of independently accepted capabilities.

Relevant work dependencies: G01, G04, G12.

### G23 — Revalidate positioning and economic research

Sources: [conxian-business/docs/research/STRATEGIC_ANALYSIS_CONXIAN_ECOSYSTEM_ISSUE_1317.md](https://github.com/Conxian/conxian-business/blob/3185f59ec8e08bb83322de40deeb53bafdbe8f0c/docs/research/STRATEGIC_ANALYSIS_CONXIAN_ECOSYSTEM_ISSUE_1317.md) (`3185f59ec8e0`).

- Do not preserve speculative native-token economics as current authority.
- External assets and independently evidenced staking adapters remain in scope.
- No financial forecast, fee change or contractual SLA is approved by this register.

### G24 — Complete institutional custody provider integration

Sources: [conxian-gateway/docs/research/ADAPTER_FAMILY_STRATEGY.md](https://github.com/Conxian/conxian-gateway/blob/0b15b59e2c1f031db0049ad36e6b8125f0918174/docs/research/ADAPTER_FAMILY_STRATEGY.md) (`0b15b59e2c1f`).

- Vendor names and SDK wrappers do not prove independent custody.
- Do not provision accounts, move assets or substitute software custody.

Relevant work dependencies: G09, G10.

## All historical candidate dispositions

| Historical candidate | Current disposition | Current work | Reconciliation |
|---|---|---|---|
| `lib-conxian-core#227` | historical-closed | G03, G05 | Closed v0.2 dependency work; not an active BitVM bridge task. |
| `conxian-market-alignment#10` | historical-closed | G08, G18 | Market #9 is a closed governance issue; preserve mapping history without using it as escrow evidence. |
| `conxian-nexus#169/pr#172` | historical-closed | G04 | Closed Groth16 state-transition work; historical title misclassifies it as dependency remediation. |
| `conxian-protocol-deprecation#612` | historical-unverified | G15, G19 | Legacy repository path returns 404; no current execution provider or active owner is inferred. |
| `conxian-business#943` | historical-closed | G01, G02 | Closed prior cycle authority; preserve rubric/history while current work uses #1317/#1390. |
| `android-first-attestation-owner-chain` | evidence-missing | G09, G10, G11, G12 | Existing #240/#241/#202 remain open; closed #242/#444 do not qualify every provider or consumer. |
| `conxius-platform#854` | historical-closed | G15 | Closed org-control tracker; title and scope are controls, not a license acceptance. |
| `conxius-platform#1082` | historical-closed | G15 | Closed CI script task; do not recreate obsolete missing-script claims. |
| `conxian-nexus#178` | historical-closed | G03 | Closed fixture secret-scan CI task, independent of current release acceptance. |
| `conxian-gateway#228` | historical-closed | G19, G04 | Closed RGB stash work; provider/release qualification remains a different evidence state. |
| `conxian-gateway#189` | deferred-research | G19 | Open BitVM3 research; no automatic build or production promotion. |
| `core-nexus-rustsec-2026-0204` | historical-closed | G03 | Current observed crossbeam-epoch is 0.9.20 where present; old threshold met, not a new vulnerability finding. |
| `core-rustsec-2026-0185` | historical-closed | G03 | Current quinn-proto is 0.11.18/0.11.19; old 0.11.15 threshold met. |
| `core-rustsec-2026-0190` | historical-closed | G03 | Current anyhow is 1.0.104 where present; old 1.0.103 threshold met. |
| `core-v0.2-dependency-review-sha-pin` | deferred-research | G03 | Historical v0.2 maintenance scope requires an explicit maintained-branch decision. |
| `core-v0.2-rustfmt-drift` | deferred-research | G03 | Historical baseline drift is not attributed to current candidates; do not bulk-format unrelated history. |
| `unmaintained-async-std-research` | evidence-missing | G03 | Identify actual current consumers before selecting migration work. |
| `unmaintained-arkworks-derivative-research` | evidence-missing | G03 | Derivative remains in current locks; exact feature paths, upstream status and owner disposition are required. |
| `unmaintained-bdk-sled-fxhash-instant-research` | evidence-missing | G03 | Rebaseline actual current graphs; the historical group is not proof that every crate is active. |
| `unmaintained-aluvm-rgb-paste-research` | evidence-missing | G03, G19 | ALuVM/paste appear in current relevant locks; research is not an accepted replacement design. |
| `bounded-lower-scope-owner-trackers` | historical-unverified | G15, G20 | Accessible site/governance trackers are closed; deleted Orbit/UI references remain unverified leads. |
| `client-onboarding-unified-installer-gap` | integration-missing | G06 | Existing first CLI slice and installer planner are inputs; #1411 owns remaining whole-graph work. |
| `org-wide-sla-positioning-commercial-pricing-gap` | evidence-missing | G08, G23 | Existing #1343/#159/#507 own contract and integration work; no new pricing or SLA decision. |
| `strategic-analysis-issue-1317-gap` | deferred-research | G23 | Use the already-open #1317 rather than a duplicate strategy umbrella or invented revenue commitment. |
| `bos-business-systems-expansion-gap` | deferred-research | G06, G08, G23 | Map the old four-phase plan to current work; no autonomous economic authority is inferred. |
| `ease-of-use-ux-domain-alignment-gap` | integration-missing | G07, G20 | Current runtime/public-surface issues own the missing deployment and UX truth evidence. |
| `agentic-system-wide-evaluation-blueprint-gap` | integration-missing | G06, G18 | CLI/schema slice exists; a production MCP service and qualified paid execution are not established. |

## All current issue phase assignments

| Issue | Primary phase | Work groups | Owner role / next gate |
|---|---|---|---|
| Restricted review coordination | R4 | G12 | Use G12 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [.github#60](https://github.com/Conxian/.github/issues/60) | R0 | G14 | Use G14 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [.github#53](https://github.com/Conxian/.github/issues/53) | R0 | G15 | Use G15 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [.github#47](https://github.com/Conxian/.github/issues/47) | R0 | G15 | Use G15 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [.github#43](https://github.com/Conxian/.github/issues/43) | R0 | G15 | Use G15 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-wallet#727](https://github.com/Conxian/conxius-wallet/issues/727) | R1 | G04 | Use G04 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-wallet#357](https://github.com/Conxian/conxius-wallet/issues/357) | R1 | G20 | Use G20 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-labs-site#80](https://github.com/Conxian/conxian-labs-site/issues/80) | R3 | G08, G20 | Use G08, G20 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#526](https://github.com/Conxian/conxian-gateway/issues/526) | R1 | G04 | Use G04 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#507](https://github.com/Conxian/conxian-gateway/issues/507) | R3 | G08 | Use G08 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#500](https://github.com/Conxian/conxian-gateway/issues/500) | R2 | G24 | Use G24 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#466](https://github.com/Conxian/conxian-gateway/issues/466) | R3 | G07 | Use G07 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#189](https://github.com/Conxian/conxian-gateway/issues/189) | R5 | G19 | Use G19 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [lib-conxian-core#440](https://github.com/Conxian/lib-conxian-core/issues/440) | R1 | G04, G05 | Use G04, G05 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-platform#1426](https://github.com/Conxian/conxius-platform/issues/1426) | R1 | G04 | Use G04 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-platform#1168](https://github.com/Conxian/conxius-platform/issues/1168) | R5 | G23 | Use G23 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-platform#1167](https://github.com/Conxian/conxius-platform/issues/1167) | R4 | G23 | Use G23 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-nexus#418](https://github.com/Conxian/conxian-nexus/issues/418) | R1 | G04 | Use G04 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-nexus#174](https://github.com/Conxian/conxian-nexus/issues/174) | R0 | G14 | Use G14 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1411](https://github.com/Conxian/conxian-business/issues/1411) | R1 | G06 | Use G06 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1399](https://github.com/Conxian/conxian-business/issues/1399) | R2 | G09 | Use G09 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1390](https://github.com/Conxian/conxian-business/issues/1390) | R4 | G05, G22 | Use G05, G22 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1359](https://github.com/Conxian/conxian-business/issues/1359) | R3 | G16 | Use G16 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1349](https://github.com/Conxian/conxian-business/issues/1349) | R3 | G07, G20 | Use G07, G20 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1343](https://github.com/Conxian/conxian-business/issues/1343) | R3 | G08, G17 | Use G08, G17 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1336](https://github.com/Conxian/conxian-business/issues/1336) | R4 | G22 | Use G22 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1317](https://github.com/Conxian/conxian-business/issues/1317) | R0 | G02, G19, G23 | Use G02, G19, G23 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#989](https://github.com/Conxian/conxian-business/issues/989) | R5 | G23 | Use G23 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#940](https://github.com/Conxian/conxian-business/issues/940) | R0 | G14 | Use G14 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#937](https://github.com/Conxian/conxian-business/issues/937) | R4 | G12 | Use G12 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#936](https://github.com/Conxian/conxian-business/issues/936) | R2 | G09, G10 | Use G09, G10 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#559](https://github.com/Conxian/conxius-enclave-sdk/issues/559) | R2 | G09 | Use G09 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#558](https://github.com/Conxian/conxius-enclave-sdk/issues/558) | R1 | G04 | Use G04 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#509](https://github.com/Conxian/conxius-enclave-sdk/issues/509) | R2 | G13 | Use G13 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) | R2 | G10 | Use G10 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | R2 | G10, G11 | Use G10, G11 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxius-enclave-sdk#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | R4 | G12 | Use G12 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian_market#159](https://github.com/Conxian/conxian_market/issues/159) | R3 | G08, G18 | Use G08, G18 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [.github-private#63](https://github.com/Conxian/.github-private/issues/63) | R0 | G01 | Use G01 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1414](https://github.com/Conxian/conxian-business/issues/1414) | R1 | G02, G03 | Use G02, G03 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian_market#176](https://github.com/Conxian/conxian_market/issues/176) | R1 | G18 | Use G18 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-gateway#531](https://github.com/Conxian/conxian-gateway/issues/531) | R3 | G17 | Use G17 acceptance criteria; record exact artifact and unresolved owner evidence. |
| [conxian-business#1415](https://github.com/Conxian/conxian-business/issues/1415) | R1 | G21 | Use G21 acceptance criteria; record exact artifact and unresolved owner evidence. |

## Primary-source research refresh

These five sources were checked on 15 October 2026. Conclusions about Conxian compatibility are inferences from comparing those specifications with the pinned local source; no interoperability deployment is claimed.

- [x402-v2](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md): Versioned payment requirements and signed authorization/verification/settlement are distinct from the local sats/payment-pointer facade.
- [x402-http](https://github.com/x402-foundation/x402/blob/main/specs/transports-v2/http.md): HTTP uses PAYMENT-REQUIRED, PAYMENT-SIGNATURE and PAYMENT-RESPONSE transport contracts.
- [x402-mcp](https://github.com/x402-foundation/x402/blob/main/specs/transports-v2/mcp.md): MCP transport defines structured payment-required results and x402/payment metadata, beyond a helper class.
- [erc-8004](https://eips.ethereum.org/EIPS/eip-8004): Draft registry specification; payments are orthogonal. A semantic Stacks adapter is not proof of an EVM registry deployment.
- [android-attestation](https://developer.android.com/privacy-and-security/security-key-attestation): Validate chain signatures, trusted roots, security level and revocation; real-device/operation evidence remains required.

## Validation and preservation

- The current register is checked for complete issue/candidate coverage, valid dependency references, phase cycles, exact source pins, and absence of production/independent-acceptance grants. The historical candidate identities/scores and original scoring tests remain unchanged; the ledger gains only a pointer to this current overlay.
- Existing dirty worktrees, root guidance publication restrictions, release/independent-review gates and the prior Wallet publication block remain intact. No credentials, infrastructure, fees, custody, domains, production switches or Project fields were changed.
- A bounded restricted review candidate was prepared and tested outside Git/GitHub under the owning security policy. Only sanitized coordination appears here; no public security issue, patch, reproduction or outbound message was posted.

## Refresh rule

Edit this dated overlay and the marked issue/index pointers when evidence changes. Keep historical ledgers and score arithmetic intact. Code presence, hosted CI, provider observation, independent acceptance and release authorization stay separate; do not turn missing evidence into either blanket enablement or blanket revocation.

The machine-readable issue/phase/dependency mappings and catalog digest are in [`research_implementation_reconciliation_2026_10_15.json`](research_implementation_reconciliation_2026_10_15.json). The complete catalog is included in the user review report; restricted annex contents are excluded from this GitHub edition.
