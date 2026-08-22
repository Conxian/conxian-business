# BOS service topology

**Status:** canonical deployment guidance, 2026-08-22

`conxian-business` is the source-of-truth repository for governance, evidence, deployment contracts, and the BOS Control Plane. The machine-readable inventory is `ops/service-registry.json`; CI validates that registry against `.gitmodules`.

## Host boundaries

- `www.conxian-labs.com`: public marketing/documentation only. It is not an admin API and must never be used as `CONXIAN_ADMIN_RUNTIME_BASE_URL`.
- `control.conxian-labs.com`: authenticated BOS Control Plane UI on Vercel.
- `admin-runtime.conxian-labs.com`: authenticated admin runtime API, independently deployed and reachable by the Control Plane.
- Gateway, Nexus, Platform, Orbit, Wallet, and Market: independently deployable services with their own health/readiness endpoints and M2M brokered access.

## Operational rules

1. Publish `/health` for process availability and `/readiness` for dependency/configuration readiness. The admin runtime uses `/admin/v1/runtime/health` and `/admin/v1/runtime/readiness`.
2. Keep service URLs in Vercel environment variables; commit names and route contracts, never secret values.
3. Use `CONXIAN_ADMIN_RUNTIME_BASE_URL` for server-side Control Plane access. Do not infer a runtime URL from the browser origin.
4. Cloudflare DNS and WAF must route each hostname to its intended origin; a marketing-domain challenge or 403 is not runtime evidence.
5. Live mutations require an authenticated test principal, explicit test mode, idempotency, audit evidence, and policy approval. Otherwise the operation remains blocked.
6. The registry and readiness ledger are evidence controls, not a claim that every service is currently deployed or online.

## Required human setup

Configure DNS, TLS, origins, Vercel domains, and runtime credentials through the approved provider consoles. After `admin-runtime.conxian-labs.com` is deployed, configure its HTTPS base URL in Vercel Production and Preview, then run authenticated health, readiness, read-only, and safe test-mode mutation verification.
