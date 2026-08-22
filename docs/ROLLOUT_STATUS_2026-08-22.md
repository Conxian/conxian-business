# BOS rollout status — 2026-08-22

## Completed in repository

- Added public-safe `/nexus`, `/gateway`, and `/market` service surfaces.
- Added shared service surface component and client-safe messaging.
- Added links from the control-plane shell to public service surfaces.
- Preserved the control-plane's private governance navigation and runtime boundary language.
- Verified production build and TypeScript compilation.
- Verified `/nexus` in the browser at the local preview.

## Required outside this repository

These actions require Vercel/DNS credentials or an authorized maintainer and are not claimed as complete:

1. Create or select a separate Vercel project for the public Labs application and attach `www.conxian-labs.com`.
2. Attach `control.conxian-labs.com` only to the control-plane Vercel project.
3. Configure `conxian.org` as the open-source portal or redirect after selecting its source deployment.
4. Provision independent runtime origins for Nexus, Gateway, and Market; then replace target-state registry values with evidence-backed origins.
5. Configure `CONXIAN_ADMIN_RUNTIME_BASE_URL` in Preview and Production, never using a public Labs origin.
6. Verify DNS, TLS, WAF, authentication, M2M credentials, health/readiness, audit evidence, and rollback before production cutover.

## Current limitation

The current workspace is the `conxian-business` monorepo and its control-plane app. The public Labs and open-source portal repositories are represented in the workspace topology but are not available as editable application files in this checkout, so their production deployments cannot be created from this session alone.
