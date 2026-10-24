# Conxian: sovereign operation across existing networks

**Version:** 2.1 evidence draft, 24 October 2026. **Publication state:** candidate.
**Owner:** [Business #1422](https://github.com/Conxian/conxian-business/issues/1422).
This draft corrects the technical narrative for review. The final authoritative
rewrite remains gated on accepted sprint-exit evidence. It grants no production
acceptance, custody rights, customer SLA or investment assurance.

The prior paper remains preserved at [the historical technical paper](../TECHNICAL_WHITEPAPER.md).
The [monthly evidence ledger](../research/MONTHLY_ALIGNMENT_2026_10_24.json)
pins sources, branches, claim IDs and limitations. A development branch, test
result or merged PR is not a deployed or independently accepted capability.

## Abstract

Conxian is building software for sovereign operations across existing networks.
Bitcoin is the canonical trust/finality root in its shared capability model;
external chains, assets and independently qualified adapters remain in scope.
Conxian has no native token and does not introduce its own L1. Its proposed
commercial value is integration, accountable policy, recoverable operations
and evidence-backed services, rather than recreating every network, model or
storage system. [C01, C08]

Shared Rust primitives, hardware/provider boundaries, observation and routing
services, operator interfaces and client-controlled wallets have distinct roles.
Current source includes capability contracts, bounded discovery, transactional
administrative workflow records and public artifact recovery tooling. These are
useful implemented components. They do not establish universally supported
signing, live settlement, independent custody, complete decentralisation or
fleet-wide production readiness. [C02–C06]

## 1. Purpose, scope and claim discipline

Operational sovereignty means a qualified operator can obtain the accepted
software and permitted data, run the required operation, recover it outside the
original provider and verify the result. This is an outcome to demonstrate, not
a property inferred from a deployment marketplace or repository name. [C08]

The ledger separates architecture decisions, implemented boundaries, scoped
test observations, research and missing evidence. “Tested” always needs a source,
fixture/environment and operation. “Deployed” needs actual artifact/environment
read-back. Independent acceptance requires the applicable owner/reviewer decision.
Neither a build nor a registration upgrades those evidence axes.

The rolling review window is 24 September–24 October 2026, Africa/Johannesburg.
Research written earlier but touched or cited during that period retains its
original date; it is not relabelled a new discovery. The current public catalogue
indexes 205 selected research/roadmap/capability paths across 12 public repositories.
Indexing is not exhaustive semantic review of every document or code line.
The private KB and restricted decisions remain outside this public draft.

## 2. Architecture and authority

| Boundary | Owning component | Permitted interpretation |
| --- | --- | --- |
| Shared contracts and cryptographic primitives | `lib-conxian-core` | Typed validation and reusable primitives; structural validation does not authenticate an issuer or authorize signing |
| Hardware, attestation and signing integration | `conxius-enclave-sdk` | Operation-specific provider composition; device, roots, freshness, replay and release evidence remain separate |
| Observation and proof | `conxian-nexus` | Observe/index/verify; administrative records do not become protocol settlement authority |
| Ingress, routing and execution boundary | `conxian-gateway` | Apply its qualified policy and provider contracts; not authority to manufacture verification |
| Operator and commercial workflows | Business / Platform | Authenticated control and read models; dashboards do not acquire signing keys |
| Client-controlled value operations | `conxius-wallet` | Preserve native authorization and existing fail-closed provider gates |
| Agent workflow and payment interfaces | `conxian_market` | Explicit protocol compatibility and evidence; a payment label or reputation score is not settlement |
| Public and commercial presentation | Org / Labs sites | Public protocol information and separately qualified commercial services |

This separation follows the network-agnostic direction and current capability
contracts. Nexus is not described as a general-purpose value execution or custody
engine. Existing external networks are not interchangeable trust domains. [C01–C04]

Protocol truth is established under the relevant network and proof rules.
PostgreSQL can be authoritative for an administrative workflow's recorded state
and audit receipts while remaining non-authoritative for chain settlement,
balances or custody. These different meanings of state must not be collapsed.
No migration should create uncoordinated writers for the same transition. [C02, C06]

Community/self-operated, managed-service and customer-controlled deployment lanes
are placement and operating choices. Each must satisfy its applicable operation
contract. A self-hosted service under one administrator is not evidence of
independent operator control. [C08]

## 3. Capability negotiation and safe failure

An inventory identifier, API, family alias and exact chain/network/operation
tuple are different objects. Current Gateway/Nexus discovery reports registered
components and explicitly leaves production operation qualification unestablished.
The Core contract separates API, implementation, integration, review and production
evidence and bounds declaration freshness. Its deterministic validator does not
verify provider identity, hardware or external evidence. [C02, C03]

Consumers must retain the approved source pin, authenticate the producer, bind
evidence to the deployed operation and recheck freshness/policy before protected
work. Missing, malformed, stale or unsupported input must remain unavailable.
Successful observation cannot authorize signing or broadcasting. [C03, C04]

A final BIP-340 signature under a supplied public key proves neither an independent
threshold ceremony nor the authority of that group key. Hardware labels, prefix
checks and metadata likewise cannot replace platform-root verification. Real-device
and provider qualification remain scoped to actual artifacts and operations. [C04]

## 4. Durable operational state and recovery

Nexus source now records administrative projections, command identities,
idempotent receipts and audit events in transactional PostgreSQL storage.
The owning implementation applies lifecycle validation and returns committed
receipts; database failure must not turn into a synthetic success. These records
are operational evidence, not an independent release approval. [C06]

The hosted recovery drill for Nexus #453 restored 34 workflow rows across 18
tables into a second PostgreSQL instance after stopping the source instance.
The recorded test source is `41b1c0f33ad65768a2204a388a77aa580b7ca32b`;
the full receipt is in the ledger. It compares actual conformance-generated
rows, including audit receipt bindings. [C06]

This is a fixture result on one CI runner. It does not prove independent operators,
geographic resilience, production RPO/RTO, every Nexus datastore, customer-data
recovery or end-to-end application resumption. Those require a separate permitted
operating drill. Raw fixture data and backup bytes are not public evidence artifacts.

The Business client currently validates required runtime fields but its list
helpers can discard pagination metadata. The owning runtime work must expose
bounded pages and incomplete collection state; offset traversal during concurrent
writes does not establish a consistent audit snapshot.

## 5. Decentralised-first placement and reuse

Prefer an existing maintained component when it meets the exact workload's rights,
confidentiality, consistency, recovery, performance, operating and cost needs.
Keep managed hosting as an optional service/recovery lane until replacement is
demonstrated. The preference does not justify a wholesale rewrite. [C08]

| Candidate | Bounded use | Required qualification |
| --- | --- | --- |
| IPFS | Public documentation and release distribution | Independently administered pins, multiple retrieval paths, accepted CID rollback; no confidential material |
| Akash | Stateless container/research-worker trial | Same accepted artifact, provider replacement, secrets boundary, actual latency/cost/recovery; TEE remains experimental |
| Sia `s3d` | Encrypted secondary object/backup trial | Exact S3 operations, independent key recovery, retention/deletion behavior and restore; no assumed full S3 equivalence |
| MeshLLM | Controlled inference-adapter experiment | Pinned model/code rights, admitted peers, bounded resource/payment policy, output/recovery tests; no production keys or confidential deal data |
| Iroh / Nostr | Transport or signed public discovery experiments | Application authorization, freshness, replay and operator/relay tests before adding another stack |
| OpenBao and workload identity tooling | Self-operated operational secret/identity controls | Scoped policies, recovery and administrator independence; not a replacement for threshold custody |

IPFS persistence needs explicit retention arrangements and public network metadata
remains observable. Akash's own documentation calls its confidential-compute
capability experimental. Sia's roadmap retains a full-compatibility work item;
published release availability is not a measured Conxian restore result.
These are qualification candidates, not adopted production replacements. [C08]

MeshLLM's distributed-inference project is `Mesh-LLM/mesh-llm`, distinct from
the similarly named 3D-mesh research project. Its source includes a Lightning
payments PoC and separately describes discovery/admission and wallet persistence
boundaries. An unpublished mesh is not automatically access-controlled, and a
release signature is not remote runtime attestation. [C09]
Conxian should reuse inference where it fits while retaining its own authorization,
custody, entitlement and evidence contracts.

## 6. Agent and payment boundaries

x402-style charging, agent discovery, payment assets, commercial entitlement,
settlement fees and signature quotas are separate concepts. ERC-8004 explicitly
separates its discovery/reputation/validation registries from payment settlement.
Conxian must verify the selected protocol/version, actual payment, durable
entitlement and consumer behavior rather than infer them from an identity record.
[C10]

BitVM3 remains research or unavailable where no qualified verifier is connected.
Result envelopes, circuit names, caller-supplied verification booleans and claimed
costs are not proof execution or measured economics. No Bitcoin consensus feature
or protocol activation is assumed merely because a research document mentions it.
[C10]

## 7. M&A and commercial sustainability

The existing M&A work separates acquisition integration, comparables and diligence.
The first admitted implementation should be read-only, source-attributed evidence:
retain raw document identifiers/hashes, filing/amendment context, parser versions,
observation times, units/currencies, source rights and uncertainty. Candidate
entity matches require review rather than silent legal-entity merging.

The accepted research compares a component portfolio, including primary filings/
XBRL tooling, data-quality/lineage components, entity-resolution tools, controls
and reporting. Each code license and each dataset's permitted use must be checked
independently. Simulated fixtures remain explicit test data; they cannot become
revenue, valuation, customer demand or production reliability observations.

Outside contributors can work on public standards, adapters, conformance fixtures,
documentation and independent operation. Their contributions do not grant access
to private deals, customers, credentials, trademarks or revenue rights. Commercial
value can come from integration, managed operation, support and evidence-backed
workflows. This draft changes no license, fee split, entitlement, contract or
commercial commitment.

Heuristic autonomy, moat, WPS or valuation equations are research models until
their inputs, units, lineage and calibration are demonstrated. No O(1) cost,
zero-operations burden, guaranteed return or arbitrary valuation is asserted.
[C11]

## 8. Threat and failure model

Qualify network tampering, dishonest or unavailable providers, compromised hosts,
stale trust collateral, replay/rollback, misconfigured access, malicious dependency
updates, split-brain state and loss of recovery keys. Hardware and threshold
mechanisms reduce particular risks only under their actual assumptions.
A t-of-n threshold scheme loses its intended threshold protection if t shares
or their authorization paths are compromised; distinct keys alone do not prove
separate administrative control.

Security review, statutory applicability and release acceptance remain their
own decisions. A scan cannot certify that no secret ever escaped; a protocol
mapping cannot certify regulatory or ISO compliance. Public source has
repository-specific licenses; “source available” is not automatically an
OSI-approved open-source grant. Check the owning license before reuse.

## 9. Delivery and whitepaper exit

Use the [capability roadmap](../architecture/ROADMAP_12_MONTH_CONTROL_PLANE.md)
and existing owner issues. R0–R5 are Conxian coordination workstreams. ITIL 5's
eight activities apply across them; they are not replaced by the old five-stage
ITIL v3 lifecycle. R5 remains deferred research/experiments, not a shortcut to
production or a synonym for accepted sprint exit. [C07]

Final publication needs an accepted, source/artifact/environment-bound claim
ledger; completed applicable provider, security and operating reviews; qualified
customer journeys; and preserved historical/supersession records. Until then this
document remains a candidate and makes no fleet-wide readiness claim. [C11]

## Evidence and references

Claim IDs map to exact source pins and observation scope in the
[monthly ledger](../research/MONTHLY_ALIGNMENT_2026_10_24.json).
The public [monthly review](../research/MONTHLY_RESEARCH_REVIEW_2026_10_24.md)
explains reconciliation, ownership and scope limits.

- **S01**: [docs/architecture/adrs/ADR-007-network-agnostic-pivot.md](https://github.com/Conxian/conxian-business/blob/265960e38354d16b4aaf767447735c4260f8ab91/docs/architecture/adrs/ADR-007-network-agnostic-pivot.md).
- **S02**: [docs/CAPABILITY_CONTRACT.md](https://github.com/Conxian/lib-conxian-core/blob/bf60a83473f7def42ad0a6d39d98ca026ec24a86/docs/CAPABILITY_CONTRACT.md).
- **S03**: [docs/CAPABILITY_DISCOVERY.md](https://github.com/Conxian/conxian-nexus/blob/b8d43a4b305bef5a3d3bc92ee0f0dffb8eb8c81d/docs/CAPABILITY_DISCOVERY.md).
- **S04**: [docs/CAPABILITY_DISCOVERY.md](https://github.com/Conxian/conxian-gateway/blob/5f551e15ea6a2a13732e7928cd7692aaee1a655d/docs/CAPABILITY_DISCOVERY.md).
- **S05**: [docs/operations/CAPABILITY_TRUTH.md](https://github.com/Conxian/conxius-wallet/blob/566e32ad719868eba34b59f2056a181c5917b61c/docs/operations/CAPABILITY_TRUTH.md).
- **S06**: [docs/architecture/capability-evidence.json](https://github.com/Conxian/conxius-enclave-sdk/blob/1472d65181eb063a8ae07eff8971808cb665303d/docs/architecture/capability-evidence.json).
- **S07**: [scripts/verify_public_ipfs_release.py](https://github.com/Conxian/conxian-business/blob/265960e38354d16b4aaf767447735c4260f8ab91/scripts/verify_public_ipfs_release.py).
- **S08**: [src/storage/admin_workflows.rs](https://github.com/Conxian/conxian-nexus/blob/b8d43a4b305bef5a3d3bc92ee0f0dffb8eb8c81d/src/storage/admin_workflows.rs).
- **S09**: [workflow](https://github.com/Conxian/conxian-nexus/actions/runs/40084035836); checked 2026-10-24.
- **S10**: [primary-documentation](https://www.itil.com/Itil-News-and-Announcements/itil-version-5-foundation-whats-new-guide); checked 2026-10-24.
- **S11**: [primary-documentation](https://akash.network/docs/learn/core-concepts/confidential-compute/); checked 2026-10-24.
- **S12**: [primary-documentation](https://docs.ipfs.tech/concepts/persistence/); checked 2026-10-24.
- **S13**: [primary-documentation](https://docs.ipfs.tech/concepts/privacy-and-encryption/); checked 2026-10-24.
- **S14**: [primary-documentation](https://sia.tech/roadmap); checked 2026-10-24.
- **S15**: [primary-specification](https://eips.ethereum.org/EIPS/eip-8004); checked 2026-10-24.
- **S16**: [mesh/docs/specs/lightning-payments.md](https://github.com/Mesh-LLM/mesh-llm/blob/45659de8ea57137d0c991395c8de55f535f1b4ce/mesh/docs/specs/lightning-payments.md).
- **S17**: [mesh/docs/MESHES.md](https://github.com/Mesh-LLM/mesh-llm/blob/45659de8ea57137d0c991395c8de55f535f1b4ce/mesh/docs/MESHES.md).
- **S18**: [docs/research/SESSION_76_RESEARCH_EXPANSION_AND_GAP_MATRIX.md](https://github.com/Conxian/conxian_market/blob/1003f1af8faf57d39e0724006201227174ec2dfc/docs/research/SESSION_76_RESEARCH_EXPANSION_AND_GAP_MATRIX.md).
- **S19**: [docs/research_implementation_reconciliation_2026_10_15.json](https://github.com/Conxian/conxian-business/blob/265960e38354d16b4aaf767447735c4260f8ab91/docs/research_implementation_reconciliation_2026_10_15.json).
- **S20**: [access-observation](https://api.github.com/orgs/Conxian/projects?state=open); checked 2026-10-24.

