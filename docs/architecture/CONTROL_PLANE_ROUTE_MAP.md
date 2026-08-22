# Control-Plane Route Map

This document describes the route structure for the internal BOS control-plane application. The application is deployed at `control.conxian-labs.com`; public/client service discovery belongs to the separate Labs deployment at `www.conxian-labs.com`.

## Root routes

- `/` — control-plane overview
- `/release-governance` — release approval and promotion workflows
- `/audit` — audit event visibility and evidence tracking
- `/policy-approvals` — governance and policy review queue
- `/environments` — environment registry and verification state

## Future routes

- `/identities`
- `/treasury`
- `/operators`
- `/settings`
- `/access`

## Navigation rules

- Keep top-level navigation module-based
- Prefer internal workflow labels over infrastructure jargon where possible
- Use explicit status chips and ownership fields for decision-heavy screens

## Initial module purpose

### Release governance
Shows release artifacts, readiness state, approval state, and promotion history.

### Audit
Shows audit events, evidence links, and operational history.

### Policy approvals
Shows pending governance actions that require review or approval.

### Environments
Shows environment records, classification, owners, and verification state.
