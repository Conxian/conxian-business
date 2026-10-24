# Provider-independent remediation and decentralised reuse

Observed: 23 October 2026. Status: implementation/research candidate; not an adopted migration, certified control set or production acceptance.
Coordination: Business #1390/#1317/#1349/#1423. Canonical strategy: [KB cloud research #75](https://github.com/Conxian/.github-private/pull/75); [M&A research #76](https://github.com/Conxian/.github-private/pull/76).

## Scope, evidence and decision

The refreshed public repository issue collections returned 56 open non-PR issues across 12 repositories, with no next-page links. Every one is mapped below. The org also has a restricted governance KB; its existing claims/restricted-review work remains in that boundary. This is not a claim that every issue body/comment, every code line or every connected provider was re-audited. The prior canonical KB inventory and broad comparison remain research inputs; this document is a new dated overlay, not their replacement.

Current Business dev at inspection: `0aea3ba97b70c0b95df8f410113ed1b121719fbd`. #1493 packaging and #1494 delivery evidence checks are independently approved and merged. Nexus dev inspected: `f906717a50ba91afd2f24460f16bfcd41b54254b`, selected admin routes/tests only. No production/provider outcome is inferred from these sources.

Recommendation: reuse established infrastructure and retain Conxian's policy/evidence/business boundary. First make current runtime/packaging/identity/state contracts correct and measurable; then compare independent operators with the same tests. A decentralised protocol cannot fix an absent API handler, absent durable audit write, unknown data rights or missing independent approval.

## Four blocker classes and remediation

| Blocker | Implementable remediation | What decentralisation can contribute | Evidence still required |
| --- | --- | --- | --- |
| Missing/mismatched runtime contracts | Runtime payload validation, auth-negative tests, route/schema compatibility and durable state/event design | Independent placement and peer transport after the same contract passes | Actual Nexus handlers, scoped roles, durable audit read-back, restart/recovery |
| Broken packaging | Reviewed non-root OCI build, narrow context, frozen install and actual container HTTP checks | Multiple compatible operators consuming the same verified image | Source/digest/provenance, filesystem and state contract, rollback |
| Pending reviews | Exact-source review requests and retained independent decisions | Signed collaboration objects and offline evidence distribution | Genuine authorised independent reviewer; no self-approval or quorum invention |
| Absent production evidence | Read-only live probe, provider/source/artifact binding, controlled non-production write/recovery tests | Independent witness/retrieval and failure-domain testing | Authenticated journeys, measurements, accountable release decision and current provider access |

The implemented client/probe validates required fields for six fixed read endpoints and three mutation receipts, preserves compatible bare-list/envelope forms and unknown/degraded states, rejects malformed records and contradictory readiness, and disables redirects. The opt-in probe uses a read credential only, sends GETs only, checks anonymous denial, bounds payloads and redacts output. It always reports source binding, durable writes and production acceptance false. It cannot transform an API receipt into a durable-write proof. Existing Node tests and hosted container CI cover this code; the operational probe still needs an approved runtime origin and scoped read credential.

## Reuse portfolio: alternatives, limitations and qualification

These are researched interfaces and upstream statements, not measured superiority for Conxian. Pin exact versions, review code/data licences, CVEs, support and operator concentration before any implementation trial. No new token, customer migration, payment or infrastructure spend is made by this document.

| Candidate / class | Reuse instead of building | Explicit limitation and first qualification |
| --- | --- | --- |
| [Akash compute](https://akash.network/docs/learn/core-concepts/providers-leases/) — decentralised marketplace | Stateless OCI fallback/research workers | [Persistent storage](https://akash.network/docs/learn/core-concepts/persistent-storage/) remains provider-local; prove export/recovery and independent operators. [Confidential compute](https://akash.network/docs/learn/core-concepts/confidential-compute/) is explicitly experimental; not a default signing solution. |
| [Sia s3d](https://github.com/SiaFoundation/s3d) — decentralised storage network with gateway/indexer dependencies | Secondary object/backup adapter | [Roadmap](https://sia.tech/roadmap), last updated June 26, still lists full S3 compatibility in progress. Test actual multipart/range/list/delete/restore semantics; do not assume API equivalence or independent control of all components. |
| [IPFS persistence](https://docs.ipfs.tech/concepts/persistence/) — peer distribution | Public releases/docs and public-safe evidence mirrors | Deliberate pins and independent retrieval are required; [privacy](https://docs.ipfs.tech/concepts/privacy-and-encryption/) is not automatic. No private KB, deal files, credentials or customer data on public IPFS. |
| [Iroh](https://docs.iroh.computer/what-is-iroh) — P2P library | Rust peer connectivity, encrypted transfer and relay fallback | Encryption does not supply authorisation, replay policy or current chain state. Benchmark against existing transports and qualify independent relays; no parallel transport stack without measured benefit. |
| [Nostr NIPs](https://github.com/nostr-protocol/nips) — relay protocol | Public signed capability/discovery announcements | Relay availability/delivery/freshness must be tested. NIP-17 encryption does not establish settlement, custody or release authority. Retain existing protocol boundaries. |
| [Radicle](https://radicle.dev/faq) — P2P collaboration | Public-source/collaboration recovery mirror | GitHub remains authoritative under owner direction. Pin and test review/identity/export semantics; never mirror private repositories publicly or convert a signature to approval. |
| [OpenBao Raft](https://openbao.org/docs/configuration/storage/raft/) — self-operated HA, not permissionless | Operational secrets and recovery controls | Seal configuration and independent recovery operators matter. Multiple nodes sharing administration are not independent custody; no signing-key migration without separate qualification. |
| [SPIFFE/SPIRE](https://spiffe.io/docs/latest/spiffe/concepts/) — federated workload identity | Cross-host workload identity and short-lived credentials | Specify attestors/trust domains, federation policy, rotation/revocation and negative authorisation tests. Workload identity is not business entitlement or TEE custody. |
| [Postgres/Patroni](https://patroni.readthedocs.io/en/latest/replication_modes.html) — self-operated distributed HA | Preserve SQL/replay semantics while reducing managed-DB dependence | Async replication can lose committed state; synchronous modes trade availability for durability. Test partitions, replay atomicity, approved RPO/RTO and recovery before use. Not a permissionless database. |
| [Keylime](https://keylime.dev/) — TPM attestation tooling | Reuse measured-boot/runtime-integrity tooling for qualified hosts | TPM boot measurements are not Nitro/StrongBox/TDX equivalence. Evaluate actual firmware, policies, collateral freshness/revocation and release binding. |
| [Phala/dstack](https://phala.com/posts/trust-center) — confidential-compute ecosystem | Compare a maintained attestation/deployment stack | Exact hardware profile, KMS/control model and trust roots remain material. Published attestation does not qualify independent custody or Conxian signing. |
| [Sigstore](https://docs.sigstore.dev/about/security/) — signing/transparency tooling | Artifact signature/identity/provenance verification | Public-service OIDC/CA/log trust remains; a Rekor entry is not multi-party release approval. Evaluate custom/offline verification and metadata privacy. |
| [TUF](https://theupdateframework.io/docs/security/) — secure update framework | Reuse signed/versioned/expiring update metadata and role separation | Does not run CI, audit business logic or approve releases. Key rotation, recovery and timestamp freshness remain operational obligations. |

Do not replace the authoritative transactional/replay store with eventual-consistency CRDTs, public ledgers or a dual writer merely to satisfy a decentralisation label. The broader KB comparison retains other compute/storage/database/threshold candidates; they need workload-specific evidence before selection. No universal network solves all 56 issues.

## Capability-based sequence

1. R0: retain the existing issue owner/acceptance and source-pinned licence/trust/contract inventory.
2. R1: integrate reviewed packaging and strict runtime boundaries; preserve existing features/interfaces and add negative tests.
3. R2: qualify a read-only public-artifact mirror, secondary backup restore and stateless independent-compute trial, one at a time. No private-data egress or funded lease without explicit scoped approval.
4. R3: run the same source/digest/auth/replay/recovery tests on each intended provider and collect actual receipts.
5. R4: require independent review, source-bound release/soak and accountable acceptance. Never invent a result or remove a gate to create an empty queue.
6. R5: expand only after measured benefit and accepted outcomes; retain paid managed delivery and customer commitments. M&A, economics and final whitepaper keep accepted-sprint-exit entry conditions.

## Current public issue-by-issue remediation map

Phase is a proposed coordination view, not a state change. Every owning issue retains its full acceptance criteria and history. New research does not close issues or override legal/security/custody owners.

| Existing issue | Phase | Reuse/approach | Next bounded action |
| --- | --- | --- | --- |
| [.github #81](https://github.com/Conxian/.github/issues/81) | R0 | Portable Rust tooling; TUF/Sigstore patterns | Prototype only where maintained tooling does not meet a measured gap. |
| [.github #60](https://github.com/Conxian/.github/issues/60) | R0 | No network replaces licence permission | Preserve approved licence/notices decisions; validate code and data rights. |
| [.github #53](https://github.com/Conxian/.github/issues/53) | R0 | No decentralised substitute | Reconcile presentation metadata against evidence and owners. |
| [.github #47](https://github.com/Conxian/.github/issues/47) | R1 | OpenBao + SPIFFE/SPIRE (self-operated/federated) | Verify secret prevention, scoped workload identity, rotation and recovery. |
| [.github #43](https://github.com/Conxian/.github/issues/43) | R0 | Radicle mirror only | Export/recover Git and collaboration history; GitHub stays authoritative. |
| [conxian-business #1491](https://github.com/Conxian/conxian-business/issues/1491) | R5 / sprint exit | 19-source evidence-engine research in canonical KB | Keep read-only primary-source acquisition, provenance and model validation; no automated deal execution. |
| [conxian-business #1429](https://github.com/Conxian/conxian-business/issues/1429) | R2 | Signed telemetry; no ledger substitutes measurements | Collect authentic costs/demand/SLA observations and reject simulated financial claims. |
| [conxian-business #1424](https://github.com/Conxian/conxian-business/issues/1424) | R0/R1 | Existing open standards and adapters | Retain jurisdiction/customer requirements and independent legal review. |
| [conxian-business #1423](https://github.com/Conxian/conxian-business/issues/1423) | R0/R4 | OSCAL-style evidence and portable probes | Map actual applicable controls to scoped operating evidence; no certification inference. |
| [conxian-business #1422](https://github.com/Conxian/conxian-business/issues/1422) | R5 / sprint exit | No decentralised substitute | Rewrite claims only from independently accepted operational evidence. |
| [conxian-business #1419](https://github.com/Conxian/conxian-business/issues/1419) | R5 / sprint exit | No decentralised substitute | Measure total cost, fees, support and actual revenue before pricing revision. |
| [conxian-business #1415](https://github.com/Conxian/conxian-business/issues/1415) | R1/R4 | Existing immutable promotion + delivery preflight | Bind current heads, full checks and independent review; never autofill acceptance. |
| [conxian-business #1414](https://github.com/Conxian/conxian-business/issues/1414) | R0/R1 | TUF + pinned/offline dependency inputs | Rebaseline lock graphs and support/licence risk; frozen/locked checks before promotion. |
| [conxian-business #1411](https://github.com/Conxian/conxian-business/issues/1411) | R1 | Reuse standards/CLI libraries, not a new transport | Retain machine-readable errors and scoped diagnostics; qualify adapters independently. |
| [conxian-business #1399](https://github.com/Conxian/conxian-business/issues/1399) | R1/R4 | OpenBao/SPIRE; qualified threshold and hardware domains | Eliminate root use; prove independent administration and custody rather than number of keys. |
| [conxian-business #1390](https://github.com/Conxian/conxian-business/issues/1390) | R0–R5 | Provider-neutral evidence adapters | Coordinate all existing owners, preserve promotion and service-specific acceptance. |
| [conxian-business #1349](https://github.com/Conxian/conxian-business/issues/1349) | R1/R3 | Portable OCI and authenticated live probes; Akash fallback later | Promote reviewed packaging, qualify actual runtime contracts, then source-bound provider/journey/recovery proof. |
| [conxian-business #1343](https://github.com/Conxian/conxian-business/issues/1343) | R1/R3 | Standard payment/event contracts | Preserve charge, quota, entitlement and settlement distinctions; real payment reconciliation. |
| [conxian-business #1336](https://github.com/Conxian/conxian-business/issues/1336) | R2/R4 | Qualified independent operators | Turnkey installation does not prove hardware/security/production acceptance. |
| [conxian-business #1317](https://github.com/Conxian/conxian-business/issues/1317) | R0–R5 | Existing canonical cloud + M&A research | Reuse maintained systems behind contracts; prototype one boundary at a time. |
| [conxian-business #989](https://github.com/Conxian/conxian-business/issues/989) | R0 | No decentralised substitute | Use primary market/customer evidence for positioning and preserve restricted strategy. |
| [conxian-business #940](https://github.com/Conxian/conxian-business/issues/940) | R0 | No decentralised substitute | Retain ontology attribution, source pinning and trademark/legal review. |
| [conxian-business #937](https://github.com/Conxian/conxian-business/issues/937) | R4 | Signed independent review evidence | Human/security acceptance cannot be generated by CI, a DAO or a transport. |
| [conxian-business #936](https://github.com/Conxian/conxian-business/issues/936) | R2/R4 | Keylime/TPM; separately qualified TEE profiles | Require actual platform/firmware/collateral and accountable owner evidence. |
| [conxius-wallet #727](https://github.com/Conxian/conxius-wallet/issues/727) | R1/R2 | Existing canonical capability contracts | Negotiate operation-level evidence; do not turn registration/transport into signing support. |
| [conxius-wallet #357](https://github.com/Conxian/conxius-wallet/issues/357) | R1 | Pinned toolchains and portable package tests | Repair dependencies and mobile-delivery quality without weakening native security. |
| [conxius-platform #1450](https://github.com/Conxian/conxius-platform/issues/1450) | R0/R2 | Provider-neutral capability evidence | Remove unsupported catalogue claims per evidence, not blanket capability disablement. |
| [conxius-platform #1426](https://github.com/Conxian/conxius-platform/issues/1426) | R1/R2 | Strict source/evidence validation | Reject malformed/stale manifests and qualify provider operations individually. |
| [conxius-platform #1168](https://github.com/Conxian/conxius-platform/issues/1168) | R0/R5 | No decentralised substitute | Founder rights and revenue routing require authorised legal/commercial decisions. |
| [conxius-platform #1167](https://github.com/Conxian/conxius-platform/issues/1167) | R0/R4 | Open protocol adapters, explicit authority boundaries | Hosting or consensus changes cannot silently transfer protocol/governance authority. |
| [conxius-enclave-sdk #583](https://github.com/Conxian/conxius-enclave-sdk/issues/583) | R2 | Keylime / qualified hardware collateral tooling | Validate real hardware/firmware roots, freshness, revocation and offline scope. |
| [conxius-enclave-sdk #559](https://github.com/Conxian/conxius-enclave-sdk/issues/559) | R2/R4 | Existing threshold implementations, independent operators | Prove DKG, signer-domain independence, liveness, replay and compromise response. |
| [conxius-enclave-sdk #558](https://github.com/Conxian/conxius-enclave-sdk/issues/558) | R1/R2 | Strict support inventory and conformance | Preserve fail-closed evidence labels and test each provider/operation. |
| [conxius-enclave-sdk #509](https://github.com/Conxian/conxius-enclave-sdk/issues/509) | R2/R4 | Phala/dstack or Akash TEE as comparison candidates | Benchmark actual attestation/KMS dependencies; never equate confidential hosting with qualified custody. |
| [conxius-enclave-sdk #241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) | R2/R4 | Android-native KeyMint/StrongBox validation | Cloud decentralisation cannot supply real-device authorisation and integrity proof. |
| [conxius-enclave-sdk #240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | R2/R4 | Keylime/attestation tooling + portable Postgres replay | Preserve freshness, revocation, atomic replay semantics and rollback protection. |
| [conxius-enclave-sdk #202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | R4 | Sigstore/in-toto/TUF for artifact evidence only | Require actual independent security and release acceptance; signatures are not review. |
| [lib-conxian-core #440](https://github.com/Conxian/lib-conxian-core/issues/440) | R1/R2 | Existing canonical contract | Propagate exact chain/family/operation semantics with downstream compatibility tests. |
| [conxian-gateway #551](https://github.com/Conxian/conxian-gateway/issues/551) | R2 | WireMock/Toxiproxy already proposed | Test timeouts, duplicates, dependency loss and recovery in an isolated lane. |
| [conxian-gateway #550](https://github.com/Conxian/conxian-gateway/issues/550) | R1/R2 | Portable OCI/Kubernetes if operationally justified | Qualify filesystem/state/health/secrets, without treating replicas as safe independent writers. |
| [conxian-gateway #549](https://github.com/Conxian/conxian-gateway/issues/549) | R1/R2 | Existing Compose/regtest | Provide reproducible non-production integration; never relabel regtest as live evidence. |
| [conxian-gateway #548](https://github.com/Conxian/conxian-gateway/issues/548) | R0/R1 | OpenBao/SPIRE + SBOM/notice tooling | Document env contracts and code/data licensing before new provider adapters. |
| [conxian-gateway #547](https://github.com/Conxian/conxian-gateway/issues/547) | R0/R1 | Akash, Sia, IPFS and portable Postgres candidates | Compare real operational cost, failure domains, support and export/recovery per workload. |
| [conxian-gateway #544](https://github.com/Conxian/conxian-gateway/issues/544) | R1 | No decentralised substitute | Finish backward-compatible token-name handling through runtime, installer and preflight tests. |
| [conxian-gateway #531](https://github.com/Conxian/conxian-gateway/issues/531) | R2/R3 | Measured node/provider telemetry | Bind fee inputs to actual cost/congestion; no oracle branding as evidence. |
| [conxian-gateway #526](https://github.com/Conxian/conxian-gateway/issues/526) | R1/R2 | Canonical capability negotiation | Separate registered route from supported chain/network/operation. |
| [conxian-gateway #507](https://github.com/Conxian/conxian-gateway/issues/507) | R1/R3 | Portable Postgres; existing payment adapters | Implement durable webhook/idempotency/key-store binding and real reconciliation. |
| [conxian-gateway #500](https://github.com/Conxian/conxian-gateway/issues/500) | R0/R2 | Customer-controlled qualified signing adapters | Compare custody/trust/contract boundaries; do not replace a regulated/custodial relationship by assumption. |
| [conxian-gateway #466](https://github.com/Conxian/conxian-gateway/issues/466) | R1/R3/R4 | Portable OCI + qualified Akash fallback | Provision least-privilege runtime, verify persistence/auth/chain dependencies and recovery. |
| [conxian-gateway #189](https://github.com/Conxian/conxian-gateway/issues/189) | R0/R2 | Upstream BitVM research, not invented verifier | Retain research-only status until real proof and adversarial verification evidence. |
| [conxian-nexus #439](https://github.com/Conxian/conxian-nexus/issues/439) | R2/R4 | Postgres + Patroni where HA is justified | Preserve atomic consume-once/replay semantics, independent review and actual restore/failover evidence. |
| [conxian-nexus #418](https://github.com/Conxian/conxian-nexus/issues/418) | R1/R2 | Canonical observation contracts | Implement current source-backed observations; transport/registration cannot imply readiness. |
| [conxian-nexus #174](https://github.com/Conxian/conxian-nexus/issues/174) | R0 | No decentralised substitute | Resolve source/dependency licensing through approved legal/governance controls. |
| [conxian_market #176](https://github.com/Conxian/conxian_market/issues/176) | R1/R2 | Existing x402 and identity specifications | Verify wire compatibility and scope; identity discovery is not payment settlement. |
| [conxian_market #159](https://github.com/Conxian/conxian_market/issues/159) | R3 | Existing payment rails/adapters | Prove actual subscription charge, entitlement and demand; do not manufacture activity. |
| [conxian-labs-site #80](https://github.com/Conxian/conxian-labs-site/issues/80) | R1/R3 | IPFS public mirror after claims correction | Align advertised offers/pricing to actual backend entitlement and accepted behaviour. |

## Access and residual work

Render inspection is paused by the connector because no workspace is selected; it requires owner confirmation of the intended workspace. No provider resources or secrets were changed. The live probe has been exercised only against disposable injected responses and the missing-configuration negative path in this session. Production origin/credential evidence, actual durable-write/recovery journeys, hardware collateral, commercial rights and independent release acceptance remain unresolved.

Public issue coverage was counted from complete returned collections, not estimated from chain counts or tool connection presence. Current PRs are separate mutable work records; refresh full check/status/review pages and head leases before any merge. Restricted security reviews and detailed cloud/customer observations remain in their approved private records.
