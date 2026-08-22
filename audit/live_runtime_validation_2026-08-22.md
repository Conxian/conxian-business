# Live Runtime Validation — 2026-08-22

## Scope

Validated the linked Vercel control-plane project and the latest production deployment without performing mutating runtime operations.

## Evidence

- Project: `conxian-business-control-plane`
- Production deployment observed: `https://conxian-business-control-plane-6sv1oga88.vercel.app`
- Vercel project root: `apps/control-plane`
- Vercel project runtime: Node.js `24.x`
- Production environment inventory contains Neon/Postgres variables, but no `CONXIAN_ADMIN_RUNTIME_BASE_URL`, `ADMIN_RUNTIME_BASE_URL`, or `NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL`.
- Direct browser access to the production URL is protected by Vercel deployment authentication; the control-plane UI and runtime routes could not be observed anonymously.
- Local validation passed: control-plane production build, client SDK tests, schema tests, M2M readiness verification, production-boundary verification, knowledge-retention verification.

## Result

**Not fully validated for live operations.** The control plane is build-valid, but its admin runtime is not wired in the Vercel production environment and live authenticated endpoint operations remain unverified. The application now fails closed to empty live datasets and reports `unconfigured` rather than presenting sample data as operational state.

## Required human/provider actions

1. Add the canonical runtime base URL to Vercel Production and Preview: `CONXIAN_ADMIN_RUNTIME_BASE_URL` (or the documented equivalent).
2. Provide an authenticated test principal or deployment-protection access path for non-mutating live checks.
3. After configuration, verify `/admin/v1/runtime/health`, `/admin/v1/runtime/readiness`, and all read routes; only then exercise explicitly approved test-mode mutations.
