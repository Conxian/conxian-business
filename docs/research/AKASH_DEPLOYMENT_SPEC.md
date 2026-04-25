# Akash Autonomous Deployment Specification (public-safe stub)

Treat this repository as public for boundary purposes.

Sensitive/internal deployment architecture, environment values, capacity assumptions, and production runbooks for this document have been migrated to the Linear Virtual Office.

See:

- https://linear.app/conxian-labs
- https://linear.app/conxian-labs/issue/CON-530/replace-sensitive-files-with-safe-examples-and-docs
- https://linear.app/conxian-labs/issue/CON-256

## How to work locally (public-safe)

1. Use local-only `.env` values with placeholders; never commit real credentials.
2. Validate SDL shape and service wiring before any deploy action.
3. Keep provider/account identifiers in local secret storage only.

### Local-safe example (non-production)

```yaml
version: "2.0"
services:
  nexus:
    image: ghcr.io/conxian/conxian-nexus:local-dev
    env:
      - DATABASE_URL=postgres://LOCAL_USER:LOCAL_PASS@localhost:5432/nexus_dev
      - NOSTR_RELAYS=wss://relay.example.invalid
  gateway:
    image: ghcr.io/conxian/conxian-gateway:local-dev
    env:
      - NEXUS_URL=http://nexus:3000
```

Internal: search Linear Virtual Office for "Akash Autonomous Deployment Specification".

This file is intentionally kept as a stub so existing links continue to resolve.
