# Decentralised workspace allocation and implementation

Classification: Public-safe supporting implementation record. Claim state:
Implemented tooling and deployment candidates; target-state provider allocation.
No production acceptance or independent review is granted by this record.

Coordination: Business #1390 (portfolio), #1423 (lifecycle), #1317 (research),
#1415 (release evidence), #1343 (billing). Preserve the existing remediation map
in [decentralised reuse](DECENTRALISED_REUSE_REMEDIATION_2026_10_23.md) and the
[three-lane architecture](../architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md).
This implementation extends them; it does not create another governance authority.

## Architectural decisions

Prefer decentralised systems that satisfy operation-specific confidentiality,
consistency, recovery, performance and support requirements. Managed hosting is
an optional commercial delivery channel. Self-hosting with one cloud operator
is an ownership option, not evidence of decentralisation. Provider count alone
does not demonstrate independent administration or failure domains.

Protocol truth remains on-chain and proof-verified. PostgreSQL may durably record
operational workflow and audit records, but derived balances/indexes do not become
protocol truth. No dual-writer settlement migration, automatic signing fallback,
new Conxian token, weaker runtime contract, or dashboard custody is introduced.

## Allocation by workload

| Workload / owning repository | Preferred qualification path | Managed allocation / release constraint |
| --- | --- | --- |
| Public protocol site: `conxian-org-site` | Static build, independent IPFS pins, CID-bound release and retrieval | Public-surfaces project; existing Docker service remains during qualification. Changing runtime requires a replacement, not an in-place conversion. |
| Labs: `conxian-labs-site` | Separate static presentation from dynamic onboarding before mirroring | Public-surfaces project; preserve checkout, subscriber and API behavior until parity evidence exists. |
| Business public documentation | Explicit allowlist, identical static bytes for IPFS and HTTPS | Public-surfaces/production; `deploy/render/public-docs.yaml` adopts only the named existing static service after ownership verification. |
| Business control plane | Same Node container on qualified operators; auth and role enforcement remain | Managed-runtime/staging then production. Supplied staging candidate is additive; production stays under existing acceptance. |
| Runtime backend: `conxian-nexus` | Qualify a portable API and derived-state baseline; resolve missing runtime contracts first | Managed-runtime, same environment as its consumers when private communication is required. No new worker is presumed executable. |
| Ingress: `conxian-gateway` | Qualify independent operator recovery and state restore | Managed-runtime; exclusive-local-writer state prohibits adding writers by horizontal scaling. Preserve the filesystem contract. |
| Operator/customer UI: `conxius-platform` | Portable server runtime and explicit provider adapters | Managed-runtime; auth/server functions prevent treating the complete app as a static site. |
| Public research collection / M&A analysis workers | Bounded Akash pilot, licensed real sources and recorded provenance | Integration lab; separate from private deal evidence and business-critical scheduling. No inferred scores are represented as measured data. |
| M&A deal documents and workflow records | Controlled storage plus qualified encrypted independent backup | Restricted data boundary; no public IPFS upload. Preserve access revocation, deletion, legal retention and audit requirements. |
| Derived SQL and caches | Portable SQL, migrations and tested independent restore | Keep existing qualified database endpoints until a measured reason to move; Render cohosting alone is not a migration reason. |
| Keys / attestation: `conxius-enclave-sdk` | Separately qualified hardware and operator independence | Outside generic public hosting. Experimental TEE availability is not signing acceptance. |
| `lib-conxian-core`, client SDKs, wallet builds, contract and `conxian_market` artifacts | Versioned reproducible artifacts, local verification, independent distribution | Do not create always-on services merely because repositories exist. Wallet-owned keys remain client-controlled. |
| Private KB, agents and engineering records | Controlled exports and a sovereign recovery rehearsal | GitHub remains the authoritative work record. Never publish the private KB through the public-doc builder. |

## Render grouping and adoption

Use one workspace initially, with public-surfaces, managed-runtime and integration-lab
projects. Production/staging must use separate identity roots, schemas, runtime
credentials and environment-scoped configuration. Isolation and protected
environments require the applicable workspace features; project names alone do
not isolate networks or authenticate public endpoints. Protected environments
also do not replace review of changes to their linked Blueprint repositories.

The two supplied Blueprints are deliberately separate adoption units:

- `deploy/render/public-docs.yaml`: existing static docs resource; retains static
  type/runtime and main branch, changes the publishing boundary to `_pages`,
  disables automatic deploys and adds static response headers. Also declares a
  new `conxian-org-static-candidate` using the org site's existing static build
  and `dist` output; the current org Docker service and its domains are retained.
- `deploy/render/control-plane-staging.yaml`: a new, paid, single-instance staging
  service on `staged`, with manual deploys, isolated environment, no disk and no
  copied production secrets. `/sign-in` is HTTP liveness only. Auth schema,
  runtime-route conformance and actual operation acceptance remain separate.

Both are opt-in files, not root `render.yaml`; publishing this PR cannot silently
sync them. Before adoption: confirm existing Blueprint ownership, export current
configuration privately, inspect the provider plan for removals/replacements,
and verify workspace feature access and service sizing. Do not place a service
under two Blueprints. Preserve current domains and resources until read-back and
rollback have been demonstrated. Do not recreate the workspace or migrate region
without database-region, network-latency and recovery evidence.

Private Render names are not automatically valid admin runtime URLs: Business
requires HTTPS in production mode. Provide an authenticated TLS origin and
exercise the existing runtime boundary probe; do not weaken TLS validation to
make private HTTP connectivity appear successful. The staging database requires
the existing reviewed auth migrations before use; it is not created by Blueprint.

## Public artifact and decentralised distribution

The existing Pages workflow referenced a missing builder. The implemented builder
uses `docs/public-artifact.json`, accepts only regular files under `public-docs/`,
rejects traversal, symlinks, duplicate/reserved destinations and existing outputs,
and copies no repository directories implicitly. Adjacent files are excluded.
Additions require reviewing both source content and the allowlist. The allowlist
is a publication boundary, not a replacement for secret scanning or content review.

Build the same artifact for HTTPS and IPFS:

```sh
bash scripts/build_pages_artifact_public_safe.sh _pages
python3 scripts/export_public_ipfs.py /absolute/new/release-directory --kubo /path/to/verified/ipfs
```

The exporter creates a new local Kubo repository, runs offline, imports the
allowlisted site with explicit CID/chunking options, and exports `site.car`,
`site/` and `release.json` with the CID, hashes and Kubo version. It does not
publish, contact pinning services, modify DNS or assert production acceptance.
Retain this release alongside its exact Git commit and normal review evidence.
Verify the CAR on a second clean offline repository and compare every restored
file before any live pinning. Operators can then import and pin the same CAR,
publish retrieval evidence through independent gateways/nodes, and retain the
previous CID for rollback. Changing DNS is a separate accepted release action.

The current content uses relative navigation and requires no remote scripts,
API, authentication, secret or signing key. No confidential M&A or private KB
content belongs in this artifact. Public IPFS metadata is observable.

## Capability gates and end-of-sprint actions

| Existing phase | Required result / evidence | Work record |
| --- | --- | --- |
| R0 evidence / authority | Compare provider independence, licensing, sustainable operations and customer commitments; prefer reuse of better open systems | #1317 / #1390 |
| R1 P0 remediation | Repair the publication boundary; review allowlist, runtime contracts and current-state-to-candidate configuration diff | #1390 / #1423 |
| R2/R3 enablement | Qualify auth migrations, runtime TLS and state contracts; perform CAR restoration and rollback | #1415 / owning runtime issue |
| R3/R4 delivery / operation | Exact-source CI, independent review, normal promotion, live source/digest read-back, incident owner and service objectives | #1423 / #1415 |
| R5 accepted evidence / sprint exit | Update existing records, compare measured economics and recovery, revise with evidence; retire resources only after retention and customer-continuity acceptance | #1317 / #1390 / #1343 |

End-of-sprint work, in priority order:

1. Recover Business and qualify the missing Nexus runtime routes using existing
   remediation ownership; a provider migration cannot satisfy those contracts.
2. Review/promote the public allowlist and adopt the docs-only Blueprint after
   checking the actual provider plan. Verify that no root files are published.
3. Independently restore the offline CAR, then qualify live independent pins
   and retrieval. Record failed measurements and unavailable access honestly.
4. Supply isolated staging auth/runtime configuration, apply migrations, deploy
   the accepted staged source and run the existing live read-only contract probe.
5. Qualify the org site's full static output and dynamic Labs separation in their
   owning repos; benchmark one stateless decentralised compute workload.
6. Reconcile source/digest, recovery, actual cost and commercial continuity before
   promoting any decentralised provider to primary or retiring managed capacity.

## Primary references checked on 24 October 2026

- [Render Blueprint specification](https://render.com/docs/blueprint-spec)
  and [current JSON schema](https://render.com/schema/render.yaml.json).
- [Render compute plans](https://render.com/docs/compute-plans): compute and
  workspace plans are separate; sizing is provisional until measured.
- [Render environment isolation](https://render.com/docs/projects) and
  [free-service limitations](https://render.com/docs/free).
- [Kubo CLI](https://docs.ipfs.tech/reference/kubo/cli/),
  [IPFS retention](https://docs.ipfs.tech/how-to/pin-files/) and
  [IPFS privacy](https://docs.ipfs.tech/concepts/privacy-and-encryption/).
- [Akash advanced features](https://akash.network/docs/developers/deployment/akash-sdl/advanced-features/):
  storage, provider behavior and experimental TEE must be qualified separately.
- [Sia software overview](https://github.com/SiaFoundation/docs/blob/main/get-started-with-sia/sia-software-overview.md):
  qualify the current client rather than copying legacy renter examples.

Provider superiority, live decentralised availability, confidential storage fitness
and savings remain unmeasured. The allocation is grounded inference from these
specifications and Conxian's existing contracts, not a completed migration claim.

## Local validation record

- 197 Python tests pass, including a real Kubo 0.43.1 offline export/re-export
  and restoration into a fresh repository; no skipped tests in this run.
- Identical CAR bytes and root CID across the two exports; all restored public
  files match. The archive is an offline artifact, not a live retrieval claim.
- Both Blueprint files pass the current Render JSON schema, SHA-256
  `8a3fb8da6b4f55fe686fbefa790e011d3dd7895f013f355953c572a21ab6494a`.
  Platform-aware sync validation remains separate from JSON schema validation.
- The unchanged org site at `c7549a4cafdec3a07e0df9a7ac4678e4b6fd609c`
  passes a frozen install and `DEPLOY_TARGET=static` build with Node 24.22.1 and
  pnpm 10.28.0: 16 pages generated. Existing empty-i18n and duplicate-404 build
  warnings remain; no live static-service or IPFS retrieval result is inferred.
- Knowledge retention, contamination guard, BOS production boundary, repository
  governance baseline and action-reference verification pass. No application
  runtime code or dependency pin changed.
- The doctrine checker exposed an existing documentation-index fragment mismatch
  in the 15 October reconciliation pointer. The index now uses the actual heading
  fragment and links this implementation; doctrine validation passes. Hosted
  checks and independent review remain candidate-specific release requirements.
