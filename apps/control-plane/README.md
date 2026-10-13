# BOS Control Plane

This application is the internal UI for the Conxian BOS control plane. Deploy it to `control.conxian-labs.com`; the public Labs experience remains a separate deployment at `www.conxian-labs.com`.

## Intended modules
- release governance
- audit dashboard
- policy approvals
- environment registry

## Route map
- `/`
- `/release-governance`
- `/audit`
- `/policy-approvals`
- `/environments`

## Notes
- This app is internal-facing.
- Runtime execution remains outside this app.
- Shared contracts should come from `packages/schemas`.
- Runtime integration helpers should come from `packages/client-sdk`.
- Admin/runtime boundaries are documented in `docs/architecture/CONTROL_PLANE_ADMIN_RUNTIME_API_CONTRACT.md`.

## Deployment prerequisites

Use Node 24 and pnpm 10.28.0 (pinned in the parent package manifest). For Vercel,
select `apps/control-plane` as the project Root Directory and include source files
outside that directory: this app imports `../../packages` through TypeScript aliases.
Initialize the parent's pinned submodules for a reproducible workspace install.

Provision these server-side variables in each deployment environment:

| Variable | Purpose |
| --- | --- |
| `NEON_POSTGRES_URL` or `DATABASE_URL` | Control-plane database with the authentication and audit schema applied; Neon URL takes precedence |
| `NEON_POSTGRES_PASSWORD` | Optional separate password for the existing Neon connection configuration |
| `BETTER_AUTH_SECRET` | Authentication secret |
| `BETTER_AUTH_URL` | The exact origin of this environment's control-plane deployment |
| `CONXIAN_ADMIN_RUNTIME_BASE_URL` | Verified Nexus HTTPS origin, without `/admin/v1`, credentials, query, or fragment |
| `CONXIAN_ADMIN_RUNTIME_READ_TOKEN` | Runtime-issued credential with `api.read` scope |
| `CONXIAN_ADMIN_RUNTIME_WRITE_TOKEN` | Runtime-issued credential with `admin.write` scope for workflow actions |

Use separate, appropriately scoped credentials for Preview and Production. These
are private settings; never rename them with a `NEXT_PUBLIC_` prefix. Credential
provisioning and rotation belong to the Nexus operator. Setting a client variable
alone does not create a valid runtime credential. Missing write credentials disable
mutations without preventing read-only pages from operating.

For local development, place the variables in `apps/control-plane/.env.local`,
which Next.js loads from the application root. Loopback HTTP is permitted only
outside production. The legacy `ADMIN_RUNTIME_BASE_URL` remains a URL alias.

The `conxian-business/admin_runtime_server.py` emulator is retired. It inferred
readiness from Git and acknowledged decisions without authentication or durable
storage. Its entrypoint now exits with guidance and starts no listener. Use the
Nexus `/admin/v1` contract for runtime data and mutations.

## Failure behavior

Runtime requests use separate read/write credentials, bypass the Next.js fetch
cache, reject redirects, and time out after ten seconds. Missing configuration,
authorization failures, and transport errors propagate to the route error boundary.
The page displays an unavailable state without exposing endpoint details or tokens.
Empty API results remain empty; no production adapter imports sample data.
Server actions retain their existing operator/approver role checks.

## Verification and release

From the repository root, after a frozen installation:

```sh
pnpm --filter @conxian/control-plane test
pnpm --filter @conxian/control-plane build
```

Before production promotion, verify sign-in and session persistence on the actual
custom domain, runtime reads with the read credential, and denied unauthorized
actions. Verify authorized mutations and durable audit records in the non-production
lane. A successful homepage response alone does not prove runtime readiness.
Environment changes require a new Vercel deployment.

See `docs/audits/2026-10-11-deployment-readiness.md` for outstanding provider and
cross-repository verification tasks.
