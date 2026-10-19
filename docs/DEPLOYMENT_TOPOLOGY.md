# Deployment topology and hosting qualification

## Current qualification rules — 19 October 2026

This is deployment design context, not a live service inventory. The domain map below remains an intended mapping requiring owner resolution and actual DNS/host/source read-back; a source declaration, successful build or provider connector does not prove a running authorized service. Preserve ownership decisions under Platform #1167 and deployment acceptance under Business #1349/#1390.

- Choose hosts from the selected runtime's state and process requirements, independently of commercial package or cryptographic trust tier. Use the established [three deployment lanes](architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md) and [service activation method](SERVICE_PACKAGING_REVIEW_METHOD.md#progressive-activation-within-existing-packages).
- A free plan is appropriate only when it meets the actual runtime contract. Durable disk, required database/cache, backup and recovery are launch prerequisites where required; do not substitute ephemeral storage or omit controls until revenue arrives. Actual provisioning and ongoing costs belong to the approved deployment record.
- Platform has both file and Neon M2M registry implementations. File mode requires durable writable storage and the qualified writer topology. Neon mode requires the intended database/role/schema, configuration and independently tested readiness/recovery; its presence in source alone does not validate a Vercel deployment. Never point file mode at ephemeral `/tmp` to satisfy health.
- Gateway's selected exclusive-local-writer lane requires durable state/queue storage and one writer. Redis is not a universal prerequisite of that lane; qualify separate managed/distributed operations by their real call paths. Use the exact release's startup contract, including currently mandatory secrets and conditional providers.
- Nexus requires its actual SQL/Redis and selected RPC/provider contracts. A stateless frontend or local SDK/verification operation need not wait for unrelated optional backends, but any operation using them must remain unavailable until qualified.
- Deploy and accept exact promoted artifacts with identity, state, network and rollback read-back. Retire duplicates only after ownership, unique traffic/work and recovery are reconciled. The dated tables below are retained as migration context; their “live,” “undeployed” and provider counts require fresh evidence.

[Render's current disk contract](https://render.com/docs/disks) requires paid compute, persists only the mount subtree, limits a disk to one service instance and prevents zero-downtime deployments. Account for restart/deploy interruption and tested backups before promising availability. A larger commercial plan does not remove these architectural constraints.

## Historical placement snapshot — 3 October 2026

> Supersedes the host mapping in `conxian-labs-site/DOMAIN_CUTOVER.md` (stale: says
> `www → Render`). The authoritative machine-readable map is
> `conxius-platform/platform/domain-service-map.json`. This doc adds the
> **host ↔ service ↔ state** layer and the constraints that decide it.

## Hosting strategy (zero-to-cash)

- **Vercel** = everything a browser hits (frontends) + the AI Gateway for LLM traffic.
- **Render** = stateful services that need a **persistent disk** and/or **long-lived
  connections** (Bitcoin/Stacks RPC, Redis, file-based state).
- Upgrade a service from free → paid only when it starts earning.

## Service → host map

| Service | Repo | Kind | Host | State it needs | Status |
|---------|------|------|------|----------------|--------|
| admin-dashboard | `conxius-platform` | Next.js + M2M key store | **Render** | persistent disk (M2M key store) | Render build fixed #1370; env vars TBD |
| public site | `conxian-labs-site` | Express | Render | stateless | live (`conxian-labs-site-xhqq.onrender.com`) |
| org site | `conxian-org-site` | Astro | Vercel | stateless | **live** (`conxian.org`, deployed 2026-10-03) |
| gateway | `conxian-gateway` | Rust | Render | intended lane's persistence and RPC dependencies; managed-auth storage separately scoped | deployment unverified; reconcile the exact candidate's [startup contract](https://github.com/Conxian/conxian-gateway/blob/dev/docs/RUNTIME_INITIALIZATION.md) and #466 receipts |
| nexus | `conxian-nexus` | Rust | Render | Neon Postgres + RPC conns | undeployed |
| market / wallet / enclave-sdk | — | libs/SDK | — | — | published/npm/crates |

## Domain map (authoritative: `domain-service-map.json`)

| Domain | → Service | Host | DNS |
|--------|-----------|------|-----|
| `www.conxian-labs.com` (canonical) | admin-dashboard | Vercel (today) / Render (target) | CNAME `cname.vercel-dns.com` |
| `conxian-labs.com` (redirect) | admin-dashboard | same | A `76.76.21.21` |
| `conxian.org` (apex) | org-site | Vercel | A `76.76.21.21` (deployed 2026-10-03) |
| `www.conxian.org` | org-site | Vercel | CNAME `cname.vercel-dns.com` |
| `nexus/gateway/sdk/platform/market.conxian.org` | services | Render | TBD |
| `pages.conxian-labs.com` | legacy GH Pages | retired | **dead — no DNS record** |

## Constraints that decide the host

1. **M2M key store is file-based** (`M2M_SERVICE_KEY_REGISTRY_PATH` →
   `FileM2MKeyStore` with lock/marker/journal files). It requires a **persistent,
   writable filesystem** — Vercel serverless (`/tmp` is ephemeral) cannot provide this.
   Fix options: (a) run admin-dashboard on Render with a disk, or (b) migrate
   `FileM2MKeyStore` → Neon (DB-backed), then Vercel is viable.
2. **gateway** uses `GATEWAY_PERSISTENCE_MODE=exclusive-local-writer` + Redis + long-lived
   Bitcoin/Stacks RPC connections → Render Docker + persistent disk.
3. **nexus** is a long-lived oracle aggregator → Render.

## Known drift (as of 2026-10-03)

- admin-dashboard deployed **twice** (Vercel live + Render build-broken) — de-duplicate.
- `conxian.github.io` CNAME is `pages.conxian-labs.com` with no DNS record — retire.
- ~~`conxian.org` apex/www point at GitHub Pages → 404~~ — **resolved 2026-10-03**: org-site deployed to Vercel + DNS repointed (A `76.76.21.21` / CNAME `cname.vercel-dns.com`), now 200.
- Toolchain drift: platform `node:22` (fixed #1370) / `pnpm@9.15.5` (org std 10.28);
  gateway `rust:1.96` (fixed #459 → 1.98.1).

## Enforced by CI

- `scripts/verify_domain_topology.py` (DNS ↔ map drift) — run in `uptime-check.yml`.
- `.github/workflows/uptime-check.yml` — daily probe of every production URL.
