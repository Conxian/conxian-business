# Control-plane runtime readiness

## Why
The control plane lacks a provisioned runtime URL and authenticated transport.
The original main baseline converted read failures and empty responses to sample
governance records. Current dev removes those fallbacks; this change preserves
that behavior and completes authenticated transport and unavailable-state handling.

## Changes
- Validate runtime configuration per request and send scoped server-side credentials.
- Preserve empty data, propagate failures to an unavailable page, and bound requests.
- Include the configured authentication origin, share the database pool, and document deployment prerequisites.
- Retire the unauthenticated Python emulator with an explanatory, nonzero exit; it must never fabricate admin API outcomes.
- Record cross-provider findings without treating historical KB claims as live evidence.

## Acceptance
Missing configuration, denied access, and network failures never yield sample data.
Reads and writes use their respective credentials, do not follow redirects, and have a timeout.
No credentials or endpoint details appear in the unavailable UI.
Runtime ownership remains in Nexus; deployment and DNS cutover require verified targets.

## Non-goals
No runtime deployment, credential generation, database migration, or DNS cutover.
No change to protocol authority, signing, custody, or submodule pins.
