# Control-plane container deployment

The Business web-service deployment expects a root Dockerfile, but the repository only packages the separate Gateway. Supply a reproducible, non-root Node 24 container for the existing BOS control-plane application, with the pinned workspace package manager and frozen dependency lockfile. Keep Gateway packaging and declared submodule revisions intact.

Use Next.js standalone output with the monorepo tracing root so shared schema/client imports remain available. Copy only the declared control-plane build inputs; exclude environment files, Git metadata, other applications and unrelated repositories from its context. Preserve authentication and runtime authorization. Add a hosted build-and-HTTP smoke check for the actual image without secrets or database changes.

Acceptance: existing runtime boundary tests pass; the actual container builds from the repository root and serves sign-in and static assets on the platform-supplied PORT, as an unprivileged user. The smoke test does not establish database/auth-session/Nexus availability. Promotion, protected configuration and full authenticated read/write/audit verification remain separate release gates.
