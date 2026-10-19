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
