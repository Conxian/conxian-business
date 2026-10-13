# Deployment readiness review — 2026-10-11

## Scope and evidence

Parent baseline: `cc718d59b5d12cddc6973948f75022807a24992f` and all eight
submodules at their committed gitlinks. Read the parent and submodule root
AGENTS.md files, deployment topology, domain service map, runtime API contract,
current BOS knowledge graph entries, ADR-007, and the central governance registry
and continuity context. Historical status claims were checked against current code
and live provider reads; private KB details and credentials are not reproduced.

## Completed remediation

- Removed sample-data fallbacks from control-plane runtime adapters, including
  the fallback that previously replaced valid empty lists.
- Added per-request runtime origin validation and separate read/write credentials.
- Disabled caching and redirects for authenticated runtime fetches and bounded
  each request to ten seconds.
- Added a route error boundary which shows an unavailable state without credentials
  or endpoint details. Existing server-action role checks remain enforced.
- Retired the unauthenticated Python emulator. It starts no HTTP server and exits
  nonzero with migration guidance; Git state no longer masquerades as runtime proof.
- Added the configured authentication origin to trusted origins, prioritized the
  current deployment URL when no explicit auth URL is configured, and shared the
  existing PostgreSQL pool rather than constructing a second pool for auth.
- Pinned the parent Node/pnpm toolchain and aligned unified CI to `dev`, `staged`,
  and `main`, with focused runtime regression tests.
- Removed Vercel token arguments from showcase CI, scoped credentials to the
  authentication steps, and disabled persisted checkout credentials. Release
  approval and staged validation still need separate provider-backed verification.

## Live Cloudflare findings

- Both organization zones are active. Apex, `www`, and the control-plane website
  DNS records target Vercel and are DNS-only.
- Website HTTP HEAD probes returned 200 for both apex/www pairs and the control
  host. This is reachability evidence only, not an authenticated workflow test.
- Follow-up GETs found the control host and public Labs host both serving the
  title `Conxian Platform | Operations`, matching the platform dashboard's layout.
  The control host's `/release-governance` and `/sign-in` routes returned 404. This suggests a
  wrong application/domain binding or deployment revision; only Vercel project
  bindings can establish the exact cause. DNS resolution itself is working.
- The documented Nexus and Gateway custom hostnames have no DNS records in the
  current zones. No origin for the admin runtime has been verified.
- No Pages projects or tunnels were found across the three accessible accounts.
  The account owning the zones has one robots/content-signals Worker, no zone
  Worker routes, no Access applications, and one runtime-artifact R2 bucket.
- Zone settings report HTTPS redirects enabled, TLS minimum 1.0, and SSL mode Full.
  Because the website records are DNS-only, Cloudflare proxy/WAF/TLS settings do
  not establish protection for the current website traffic. Do not toggle proxying
  or DNS destinations without verifying origin certificates and application behavior.

No live DNS, TLS, firewall, credential, or deployment configuration was changed.

## Outstanding work register

| Priority | Item | Owning boundary and next evidence |
| --- | --- | --- |
| P1 | Nexus origin and credentials remain unprovisioned/unverified for the control plane | Inspect the selected Render workspace, locate the actual Nexus service, verify its authenticated `/admin/v1` contract, then provision scoped client credentials. Do not guess an origin from a frontend hostname. |
| P1 | Vercel project settings and deployed commit remain unverified | Connected project-detail/deployment reads returned 403. Verify project root, custom domains, environment scope, deployed SHA, and sign-in/runtime smoke results after access is restored. |
| P1 | Control host appears to serve the platform dashboard | Live title matches the platform source, rather than the business control-plane layout. Verify and correct the Vercel domain-to-project association before changing Cloudflare DNS. |
| P1 | Platform dashboard requires durable filesystem state | Existing topology selects Render with persistent storage for M2M registry, claims, and SIDL. Verify its service/disk/mounts before cutover; migrating these stores solely to fit Vercel is not assumed. |
| P1 | Conflicting domain/hosting documentation | Current control-plane README and DNS use the control host, while the older domain map also mentions a BOS host and conflicts about the public site's owning service. Reconcile against verified provider project bindings; no automatic DNS cutover. |
| P2 | Showcase workflow releases immediately after build | Add reviewed-code gates, staged production validation, and explicit promotion in a dedicated change. Verify its configured project root before changing working directories. |
| P2 | Platform pnpm version differs from parent | Platform's independent manifest pins 9.15.5; parent policy pins 10.28.0. Coordinate its own lockfile/toolchain update in that repo, not via implicit parent overrides. |
| P2 | Auth and data prerequisites | Verify database schema, role assignment, preview isolation, and persistent sessions on each intended origin. No database migrations were executed in this review. |
| P2 | Cloudflare hardening plan | Decide whether DNS-only remains intended. If proxy protection is desired, prepare verified origin TLS and cache/auth behavior first; the current Cloudflare rules are not evidence that Vercel traffic traverses them. |

## Knowledge-base reconciliation

ADR-007 (2026-10-08) supersedes own-protocol/Clarity launch assumptions in older
agent guides. Keep the network-agnostic architecture and separate signing/provider
acceptance gates. Current topology identifies long-lived runtimes on Render;
older deployment guides and historical audit summaries are not live readiness evidence.
The current Cloudflare connection can read the organization zones, superseding
the older session-specific account-access blocker. Vercel and Render access must
still be verified independently.

## Validation

- Twelve focused runtime transport/configuration tests pass, covering missing and
  invalid configuration, separate scopes, all four read adapters, empty results,
  401/403/500/503 responses, network failures, all three mutation clients, and
  credential refresh between requests.
- Provider inventory and website reachability were checked read-only.
- Knowledge-retention, BOS production-boundary, submodule-integrity, repository
  governance-baseline, and static promotion-control checks passed. Live branch
  protection remains unverified by the promotion checker.
- The retired runtime entrypoint was executed and confirmed to exit nonzero with
  migration guidance instead of starting a listener.
- A filtered frozen install with pnpm 10.28.0 and the existing 24-hour release-age
  policy completed. Next.js 16.3.8 production compilation, TypeScript, and route
  generation passed (exit 0). Better Auth reported missing base URL and secret in
  this unconfigured local environment; this is not authentication/runtime proof.

## References

- `docs/DEPLOYMENT_TOPOLOGY.md`
- `apps/control-plane/README.md`
- `docs/architecture/CONTROL_PLANE_ADMIN_RUNTIME_API_CONTRACT.md`
- `docs/architecture/adrs/ADR-007-network-agnostic-pivot.md`
- `conxius-platform/platform/domain-service-map.json`
- Cloudflare proxy behavior: https://developers.cloudflare.com/dns/proxy-status/


## Current alignment refresh — 2026-10-12 UTC

The GitHub fetch includes commits dated October 13 in repository history. Live
reads below were performed October 12 UTC. `main` remains `cc718d59`;
`dev` is `19a60f14`; `staged` is `b6842d49`. Dev and staged have identical
file trees, despite different promotion history. The local fix branch is based
on current dev, preserving its Neon connection settings and account schema.
No branch was pushed, merged, or deployed.

Upstream dev already removed sample fallbacks. The remaining application fix is
authenticated, bounded transport and an unavailable UI. Dev also adds an account
`issuer` column; verify the live authentication schema before promotion. The
repository schema declaration alone does not prove a database migration occurred.

All eight submodule dev/staged heads were fetched without changing committed
pins. Seven pins match current main. Enclave SDK main has advanced from
`2917c3c` to `f13de4f`; the tree difference is a CodeQL workflow correction.
Do not roll all submodules to dev merely to eliminate SHA differences.

| Repository | Pinned/main baseline | Current dev | Current staged |
| --- | --- | --- | --- |
| conxian-gateway | d84c2a5 | 8de1a4e | 305ea98 |
| conxius-wallet | 1310955 | b90897e | 52b2bba |
| conxian-nexus | 6d2a339 | aba5e32 | db914a9 |
| conxius-platform | 2f4acde | 927e581 | ea85a97 |
| conxian-labs-site | 86e6fcd | fcd2f52 | 93f4b99 |
| conxius-enclave-sdk | 2917c3c (main f13de4f) | 400de3e | 2045ecb |
| lib-conxian-core | fb2807f | 176044d | 015dd94 |
| conxian_market | 581383c | 99ff69a | 978abfa |

Latest root/submodule AGENTS files have no changes across these compared heads.
Platform and market dev file trees match their pinned baselines. Other dev
branches contain dependency, workflow, fee, wallet, WASM, and site changes;
these require their own release evidence. Historical recursive fetches encountered
unavailable old gitlink objects; current pinned checkouts remain intact, and
explicit non-recursive branch fetches succeeded. This is not proof every old
historical revision can be recursively reproduced.

Fresh Cloudflare DNS and HTTP GET evidence remains unchanged: the control and
public Labs roots serve the platform title; control sign-in and release-governance
routes return 404. Vercel project inspection still returns a team-scope 403 and
no authenticated CLI fallback is installed. Render service inspection remains
pending the connector-required explicit selection of Conxian-Business workspace.
The linked v0 conversation was not accessible; no claim is made to have read it.

### Recommended deployment alignment

| Surface | Recommended placement | Evidence needed before cutover |
| --- | --- | --- |
| Business control plane | Vercel project rooted at apps/control-plane | Correct project/domain association, isolated env scopes, auth schema and session test, verified Nexus origin and scoped tokens |
| Nexus and Gateway | Render long-lived services | Actual service URLs, health, authenticated admin contract, persistent data and required dependencies |
| Platform admin dashboard | Render with persistent storage per topology | Disk mounts and M2M/claims/SIDL persistence; keep its identity separate from the business control plane |
| Labs public website | conxian-labs-site deployment | Confirm provider service and map public www to this application |
| Protocol public website | Dedicated org-site Vercel project | Verify deployed repository/commit and domain association |
| Database | Existing Neon/PostgreSQL | Confirm intended database, schema, pool and environment isolation; no Supabase migration is needed to fix the runtime URL |
| DNS | Existing Cloudflare zones | Retain working DNS until application targets are verified; proxy/WAF adoption is a separate choice |

New UX research proposes `bos.conxian-labs.com`, while the application README
and existing DNS use `control.conxian-labs.com`. Preserve the existing control
hostname during repair and record the canonical hostname decision before any
rename or redirect. Neither research labels nor DNS prove deployed ownership.

Execution order: verify provider bindings and runtime service; configure the
app's private environment and database prerequisites; validate a preview;
then promote through dev → staged → main with authenticated smoke evidence.
Environment-variable changes apply to a new deployment, not an existing one.


## Render inspection — 2026-10-13 SAST

The user explicitly selected Conxian-Business. The workspace inventory, including
previews, contains four services. There is no Nexus, Gateway, or platform
admin-dashboard service in this workspace. This does not rule out services in
other accounts or providers. No verified Nexus origin can be obtained here.

| Service | Latest deployment | Confirmed finding |
| --- | --- | --- |
| conxian-org | build_failed, edcf1ff | Install fails with ERR_PNPM_IGNORED_BUILDS for esbuild@0.28.2. Dockerfile falls back from frozen install to non-frozen install, which fails too. |
| conxian-business | build_failed, cc718d59 | Configured Dockerfile ./Dockerfile is absent; build logs confirm file-not-found. This is not a Nexus service. |
| conxian-business-static-docs | build_failed, cc718d59 | Automatic dependency installation exits ELIFECYCLE before the echo-only build. Available logs do not identify the underlying lifecycle failure. Publish path is repository root. |
| conxian-labs-static-v1 | live, 86e6fcd | Publishes the labs-site repository root as a static site. It does not execute Express server.js. |

The static Labs service cannot itself implement server.js endpoints such as
/api/pricing/managed and /api/onboarding/subscribe. Verify intended routing and
backend ownership before treating the static deployment as a complete public
website. Both static services publish the repository root; replace this with an
explicit public output directory during their own deployment repair to prevent
accidental publication of source/configuration files. No secret exposure is
asserted by this inventory alone.

### Revised next steps

1. Provision a dedicated Nexus runtime from conxian-nexus after reviewing its
   current startup, database, port, auth, and persistence requirements. Select the
   required service plan explicitly; no paid service was created in this review.
   Do not point the control plane at either existing business service merely
   because its name resembles the application.
2. Restore Vercel project access, verify the control hostname's application
   binding, and configure the runtime origin/read-write credentials plus auth/DB
   settings. Validate preview sign-in, reads, denied writes, and durable audit.
3. Retain the existing Labs site while preparing its correct static output plus
   API routing, or its documented Express hosting configuration. Confirm the
   public www target before cutover.
4. Repair org-site dependency approval narrowly for the required package and use
   a pinned package manager with frozen installation. Do not enable every package
   script or silently regenerate the lockfile in deployment.
5. Decide whether the two business Render services have a continuing purpose
   before retiring or repointing them. Their latest builds failed, but that alone
   does not establish that no older deployment is serving traffic.

Render selection is now resolved. Earlier pending-selection statements above
are retained as historical audit context. Inspection changed no service, plan,
environment value, domain binding, or deployment.

Public GET probes confirmed the Labs static root returns 200 with the expected
Conxian-Labs title. The business static-docs root returns 404. The two Docker
service requests timed out; these timeouts alone do not prove permanent downtime.


## Nexus contract gate — 2026-10-13 SAST

Further handler-level review changes the immediate deployment recommendation:
**do not wire the current Nexus build into production as the control-plane admin
runtime**. Runtime ownership remains Nexus, but its current implementation is not
compatible with the canonical contract. Nexus dev has the same admin handler
source as the pinned main revision.

| Contract requirement | Current implementation in src/api/admin.rs | Required correction |
| --- | --- | --- |
| GET /admin/v1/releases | No registered route | Backed release registry with canonical response |
| GET /admin/v1/governance-actions | No registered route | Backed governance registry with canonical response |
| Environment records | Hard-coded strings dev/staging/prod | Canonical objects with actual verified registry state |
| Runtime readiness | Always reports ready after authorization | Real dependency/evidence checks with degraded/blocked outcomes |
| Durable audit | Audit list always empty; three workflow handlers generate IDs and log only | Transactional workflow persistence and durable audit retrieval |
| Decision response | Uses requestId for decisions | decisionId required by shared schema |
| Chain/attestation evidence | Fixed height/synchronized and verified=true responses | Measured evidence or explicit unknown/blocked results |

The database migrations contain no admin release/governance/audit storage schema.
Adding a DATABASE_URL cannot create the missing workflow implementation. Startup
runs the existing migrations automatically, so use an isolated staging database
for initial validation; never trial-run against a shared production database.
Production configuration additionally requires remote authenticated PostgreSQL
and Redis. Do not bypass these checks with ALLOW_DEFAULT_* or
NEXUS_ALLOW_UNSAFE_* flags. The only existing Render Key Value instance has no
persistence and an unrelated test name; it was not repurposed.

### Concrete runtime implementation acceptance

- Preserve Nexus authorization and dual-control validation. Three write handlers
  must deny execution until persistence is available, rather than acknowledge
  success for logging alone.
- Add reviewed schema and migrations for releases, governance actions,
  environments, and append-only audit events. Define seed/import ownership;
  do not insert fabricated operational records to populate screens.
- Persist state transitions and corresponding audit IDs atomically, enforce
  valid transitions and replay protection, and test rollback on storage errors.
- Implement both missing list routes and all four list shapes against the shared
  contract. Test malformed payloads, missing records, unauthorized access,
  accepted/rejected decisions, dual control, and durable readback after restart.
- Fix readiness and evidence handlers so absent evidence is blocked/unknown.
- Compile and run the Nexus Rust verification protocol and authenticated staging
  contract tests before creating a production binding. Rust and Docker tooling
  are not installed in this current execution environment.

This gate supersedes the earlier suggestion that simply provisioning Nexus and
setting its URL would complete the fix. The control-plane transport patch remains
useful, but is not runtime implementation or end-to-end readiness proof.


## Prepared org-site build remediation

A separate local branch, `fix/reproducible-render-build`, in conxian-org-site
now pins Node 24 / pnpm 10.28.0, uses frozen installs without fallback, explicitly
allows esbuild/sharp dependency scripts with strict checking and minimum release
age, and builds an adapter-free static target for the Docker/Nginx service.
The default Vercel target is preserved and CI covers both build modes.
Frozen installation and both 15-page builds passed. Existing missing-i18n and
404 route-conflict warnings remain; neither stopped generation. Docker itself
could not be tested because the engine is unavailable.

The attempted business-branch push failed because local Git has no authenticated
HTTPS push credentials. No remote branch or PR was created. The connected GitHub
API can publish the prepared branches once its required admin/personal account
selection is resolved. No production deployment has been triggered.
