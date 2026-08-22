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
