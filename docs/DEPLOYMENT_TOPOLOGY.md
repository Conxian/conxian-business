# Deployment Topology (single source of truth)

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
| gateway | `conxian-gateway` | Rust | Render | persistent disk + Redis + RPC conns | undeployed (needs 11 secrets) |
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
