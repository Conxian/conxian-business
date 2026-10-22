# Service packaging and tier review method

Coordination: Business #1390; current billing #1343; qualification #1429; operations #1423. The pricing/economics study #1419 and final whitepaper #1422 retain their accepted-sprint-exit sequence. This method supplies no offer, rate, contract, financial projection or production acceptance.

## Preserve independent dimensions

| Dimension | Review fields and owner | Evidence required before a stronger claim |
| --- | --- | --- |
| Service identity | Owning repository, operation, chain/network, supported interface/version | Pinned source and explicit owner contract; preserve the existing six service pillars and primary offer structure. |
| Deliverable | Crate/npm package, image, CLI, API, self-hosted deployment or managed operation | Exact version/digest, dependency/license notices, SBOM, authenticated build provenance and rollback identity. |
| Technical state | Known, implemented, configured, observed healthy, independently qualified | Tests and operation-specific evidence; each state is recorded separately. |
| Trust | Core TrustTier / SDK RailTrustTier and verification/finality assumptions | Applicable provider contract; a commercial plan must never increase cryptographic trust. |
| Commercial configuration | Managed-service charges, signature quota, settlement fee or payment-backed entitlement | Keep each domain's policy ID, integer/decimal unit and period; configured eligibility is not payment. |
| Access and entitlement | Authenticated tenant, product/operation scope, expiry/revocation, payment reconciliation | Authorized provider receipts and denial/replay/restart tests; flags and invoice creation alone do not grant access. |
| Service level | Intended scope/window, availability/latency/error budget, support/recovery | Complete authenticated observations, failure/recovery and approved contractual terms; point-in-time health is not an SLA. |
| Deployment and custody | Self-hosted/managed boundary, provider responsibility, region/data lifecycle | Qualified source/artifact/runtime read-back and independent release decision; installation does not establish custody authority. |

The shared Core billing catalog is configuration-only. Business's billing propagation checker verifies one pinned source snapshot and now checks that Core exports its billing module. It does not prove current deployment or dynamic branch health. Review current source and target trees separately at promotion.

Keep historical proposals and accepted policies distinguishable. The older packaging, onboarding and billing-design documents require reconciliation through their existing owners; their tier names, price suggestions, revenue scenarios and advertised SLA values must not be promoted into current offers merely by copying them. Preserve useful independent capabilities and repository ownership. Do not add another pricing or entitlement engine.

## Work phases and acceptance

- R0: inventory source identities, existing policy and offer authorities, unsupported claims, license and ownership gaps.
- R1: implement bounded conformance/contract corrections and negative tests; preserve rates, allocations and authority.
- R2: qualify the actual provider/device/key/operation and hardware boundaries in the SDK owner tracks.
- R3: verify metering, settlement/entitlement, tenant isolation, outage, restart, rollback and live read-back in the runtime owners.
- R4: independently accept one exact artifact/operation and use the normal dev → staged → main route.
- R5: start the separate measured economics/reinvestment and final publication tracks only after their accepted-exit conditions.

## Primary-source research baseline — 19 October 2026

- [OpenTelemetry resource conventions](https://opentelemetry.io/docs/specs/semconv/resource/): use consistent resource/service identity for observations. These attributes do not authenticate telemetry or prove a sampling window.
- [FOCUS specification 1.4](https://focus.finops.org/docs/specification/v1-4/): evaluate common cost/usage units, periods, currency and allocation provenance when #1419 begins. A normalization format is not recognized revenue, a price recommendation or proof of complete data.
- [OpenFeature flag evaluation](https://openfeature.dev/specification/sections/flag-evaluation/): typed defaults and evaluation details can support explicit unavailable states. Flag evaluation is not tenant authorization, entitlement or operation qualification.
- [SLSA 1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts): verify trusted builder/provenance and the artifact subject digest against the expected source and build policy. Provenance does not replace independent functional/security acceptance.

These are research inputs, not declarations of standards conformance or new dependencies. Customer contracts, negotiated prices, bills, raw infrastructure observations, forecasts and security findings remain in their approved restricted records. Public issue updates carry methods and bounded progress only.

## Operation-level packaging review

Review independently consumable operations within the existing offer structure and six service pillars. An operation can be delivered through a library, CLI, self-hosted image, API or MCP adapter; an interface is not an additional underlying capability. Preserve the existing owners and approval route. This method does not create a signing service or enable a value-bearing operation.

| Operation | Contract to review | Evidence and dependency boundary |
| --- | --- | --- |
| Prepare / normalize | Versioned input, chain/network, transaction/message representation and bounded unsigned output | Deterministic vectors, parsing limits and exact unsigned intent; no signing, submission or settlement implied. |
| Evaluate policy | Principal, tenant, operation, payload digest, policy version and expiry | Explicit denial/unavailable behavior and independently owned approval; a plan or commercial tier does not authorize an action. |
| Sign | Qualified provider/key identifier, algorithm, message/digest semantics and authorized intent | Key isolation, user/operation authorization, trust/revocation/replay evidence, supported hardware and exact signed bytes. Signing permission does not grant transmission. |
| Verify | Expected message, signature/proof, public key/trust anchor, algorithm, context and policy | Malformed/wrong-key/network/expired/revoked negatives. Signature validity, hardware attestation, proof validity and payment finality are different predicates. |
| Transmit / submit | Authorized signed payload, destination/network, deadline, request identity and retry semantics | Accepted/rejected/unknown outcomes, durable idempotency and receipt reconciliation; transport acknowledgement is not finality. |
| Observe / reconcile | Receipt identity, source/provider, chain position, freshness and finality rule | Reorg, stale/unavailable observations and provider disagreement; never convert timeout into success or blindly repeat an irreversible submission. |

Per-operation records should carry an operation ID/version, owner, artifact/interface, exact source/provider configuration identity, required/optional dependencies, trust assumptions, secret class (names only), access scope, evidence status/expiry, input/output schema, errors, metering unit and acceptance issue. Record usage at the supported operation boundary; do not bill a retry twice or count each adapter as a new service. Reconcile commercial configuration through #1343 and defer measured pricing/economics to #1419's accepted-exit conditions.

### Primary-source comparison — checked 19 October 2026

These are documented design examples, not an independent vendor performance ranking, deployment verification or a recommendation to adopt their custody model. Pin a chosen compatibility/version target before implementation.

| Example | Documented distinction | Applicable review question |
| --- | --- | --- |
| [AWS KMS Sign](https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html) and [Verify](https://docs.aws.amazon.com/kms/latest/APIReference/API_Verify.html) | Signing uses authorized private-key access; verification can use the corresponding public key. Algorithm and message/digest semantics matter. | Can verification be consumed without signing credentials, with the expected key/context and explicit trust limits? |
| [Bitcoin Core 30 testmempoolaccept](https://bitcoincore.org/en/doc/30.0.0/rpc/rawtransactions/testmempoolaccept/) and [sendrawtransaction](https://bitcoincore.org/en/doc/30.0.0/rpc/rawtransactions/sendrawtransaction/) | Acceptance testing and network submission are distinct RPC operations. | Is preflight scoped to its observed node state, with submission and finality separately evidenced? |
| [Turnkey policies](https://docs.turnkey.com/features/policies/overview) | Actor consensus, conditions and deny/allow evaluation govern activities; documented root-quorum exceptions exist. | Are approvals and privileged exceptions modeled/audited rather than inferred from a paid plan? |
| [Fireblocks raw signing](https://developers.fireblocks.com/docs/raw-signing) | Raw signing has distinct production enablement and policy constraints. | Are typed/domain-bound requests preferred and arbitrary signing outside ordinary product entitlement? |
| [Tenderly simulation](https://docs.tenderly.co/simulations/overview) | Simulation is exposed through API/RPC/SDK before network execution. | Can preview/diagnostic functionality stand alone without claiming execution or future-state certainty? |
| [x402 MCP transport](https://github.com/x402-foundation/x402/blob/main/specs/transports-v2/mcp.md) | Payment requirements, payload and settlement response are separate protocol artifacts. | Are wire parsing, payment verification, execution authorization and final settlement distinct? |

Research outcomes belong in the existing issue and restricted evidence record. Historical signing research is source material, not an assertion that every described algorithm, provider or ceremony is currently qualified. Use [knowledge-source routing](DOCUMENTATION_ALIGNMENT_INDEX.md) to find existing authorities rather than copying another current-looking table.

## Progressive activation within existing packages

The recommended rollout is an accepted base surface with operation-specific additions. “Online” must identify the surface and supported operation: a served website, authenticated console, reachable provider and qualified settlement route are different results. Keep required identity, authorization, persistence and audit controls fail closed. An unselected integration may remain unavailable without making an otherwise qualified base operation unavailable; an operation that requires it must still deny or report unavailable. This is a review/implementation target, not evidence that current deployments meet it.

Preserve the three lanes in [the runtime deployment architecture](architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md). They describe ownership and placement, not a ranking of cryptographic strength. Sovereignty includes key/control-plane authority, pinned upgrades, state export/recovery and provider exit; selecting managed hosting does not surrender or establish custody authority.

| Existing lane | Required for its accepted scope | Optional additions after separate qualification |
| --- | --- | --- |
| Community sovereign-node | Operator-controlled deployment, selected runtime's exact startup contract, durable state, authentication, recovery and explicit supported operations | Managed observability/support, extra providers and chains; offline library/verification use need not require a hosted full stack |
| Business-managed | Accepted images/configuration, tenant isolation, accountable managed operations, auth/audit persistence and qualified endpoints for the offered operations | Additional networks, enterprise identity, support-provider integration and measured capacity commitments |
| Enterprise/private-cloud | Customer-controlled identity/deployment authority, protected change process, explicit custody boundary, private connectivity and tested export/restore | Dedicated placement, additional provider choice, recovery objectives and contractual service commitments supported by measured evidence |

Review packages as a composition of operation set, deployment lane, provider/network scope, capacity/quota and support/recovery commitment. Keep existing Core billing policy IDs and domain units; add no parallel scoring, pricing or entitlement engine. Never make an unqualified feature purchasable merely because its adapter or billing configuration exists. Higher capacity/support can be commercial dimensions; stronger cryptographic claims require their own evidence regardless of price.

### Infrastructure needed for the selected operation

| Surface | Foundation that cannot be omitted | Dependency that should be selected by operation |
| --- | --- | --- |
| Static public sites | Qualified build/publish directory, TLS/domain ownership and accurate availability/offer text | No Gateway or signer dependency merely to serve documentation |
| Gateway | Exact candidate's startup secrets/configuration, qualified artifact, authenticated ingress and durable local state/queue for the single-writer lane | Provider credentials and route-specific RPCs only for enabled modes; do not reduce existing mandatory parser requirements without reviewed code/tests |
| Nexus | Actual SQL/Redis contracts, schema, scoped identity and recovery for the selected runtime | Chain observation, oracle, proof and Gateway operations according to their real call paths; avoid introducing a startup dependency cycle |
| Platform console | Its M2M registry's qualified persistence backend and authorization controls | Probe each configured integration independently; endpoint plus required credential before a protected read; configuration and HTTP status never grant operation qualification |
| Business console | Auth SQL/schema, session secret/origin, audit persistence and appropriate runtime scopes | Nexus-backed workflows need the qualified Nexus contract; support, CRM and payment providers require explicit adapters and lifecycle tests |
| Wallet / SDK / Core | Supported artifact and operation-specific verification, storage and key/attestation boundary | Unrelated hosted providers must not become dependencies of qualified local functions; signing/broadcasting remain separately authorized |

### Activation and recovery contract

For each existing operation, record dependency requirement, owner, source/artifact, names/classes of configuration, scope and allowed network destinations. Evaluate absent, partial, configured, reachable and independently qualified evidence separately. Re-evaluate after configuration changes; do not infer live activation from a connector OAuth session or a feature flag. Outages/revocations must invalidate affected operations while unrelated accepted operations continue. Test missing and wrong credentials, malformed responses, timeouts, restart, stale evidence, rollback and denied cross-tenant access. Avoid logging URLs, keys or provider bodies in public diagnostics.

Distinguish process liveness, readiness for the selected traffic, per-integration diagnostics and a representative user journey. A shallow endpoint cannot replace security/state readiness; a full optional-provider inventory must not be substituted for the selected operation's readiness. Existing health contracts may change only through their runtime owners with compatibility and negative tests.

### Expanded primary-source comparison — 19 October 2026

- [Docker Compose profiles](https://docs.docker.com/compose/how-tos/profiles/) supports selective service activation; unprofiled services start by default, and explicitly targeted services can start with their dependencies. Apply this dependency discipline to deployment design; profiles are not authorization or production qualification.
- [Kubernetes probe guidance](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) separates restart-oriented liveness from traffic readiness and startup timing. Apply the distinction without introducing Kubernetes as a new estate requirement.
- [GitLab health checks](https://docs.gitlab.com/administration/monitoring/health_check/) separates process, readiness and comprehensive dependency checks, warning against using broad backend health as load-balancer truth. Compare the supported traffic contract before changing Conxian health semantics.
- [Stripe Entitlements](https://docs.stripe.com/billing/entitlements?dashboard-or-api=api) separates product features and active customer entitlements, with grant/revoke notifications and paginated reconciliation. Reuse the lifecycle lesson in the existing billing owners; this does not choose Stripe or replace payment/provider authorization. A provider entitlement cannot qualify a cryptographic operation or prove settlement finality.

Implementation order: repair release ancestry and candidate evidence; qualify foundational auth/state/artifacts; accept a narrow base surface; attach one provider/operation with negative/recovery tests; reconcile entitlements/metering through existing owners; qualify commitments from observed operation windows. Track deployment in #1349/#1423, configuration/installer in #1411, runtime provider evidence in Platform #1426, billing in #1343, and measured packaging/economics in #1419 after accepted sprint exit. Never label the entire system live from a partial rollout.
