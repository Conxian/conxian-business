# Repo portfolio (flagship vs supporting)

This page defines the Conxian public repo map for external evaluation and internal consistency.

Note: as of 2026-04-01, the UI repo is still named `Conxian/Conxian_UI` and should be renamed to `Conxian/conxian-ui` for naming consistency.

## Flagship (external trust surface)

- https://github.com/Conxian/conxius-wallet — Flagship: Sovereign wallet (Android-first, offline-first) for Bitcoin L1 and Bitcoin-adjacent layers.
- https://github.com/Conxian/conxian-gateway — Flagship: “Fusion” gateway aggregating cross-layer state + compliance pipelines.
- https://github.com/Conxian/Conxian — Flagship: Core protocol + on-chain contracts.
- https://github.com/Conxian/Conxian_UI (planned rename to https://github.com/Conxian/conxian-ui) — Flagship: Primary UI for interacting with the Conxian ecosystem.
- https://github.com/Conxian/conxian-labs-site — Flagship: Public Conxian Labs website.
- https://github.com/Conxian/conxius-platform — Flagship: Local dev stack to run the ecosystem end-to-end.

## Supporting (linked from flagship READMEs; not pinned)

- https://github.com/Conxian/lib-conxian-core — Supporting: Shared core models + conventions used across services.
- https://github.com/Conxian/lib-conclave-sdk — Supporting: Headless enclave + cryptographic state machine SDK.
- https://github.com/Conxian/conxian-nexus — Supporting: API bridge (“Glass Node”) between layers/services.
- https://github.com/Conxian/stacksorbit — Supporting: Stacks smart-contract deployment tooling.
- https://github.com/Conxian/.github — Supporting: Org-wide defaults (community health files, templates).
- https://github.com/Conxian/conxian-business — Supporting: Governance + OpenSpec + submodule wiring for the Conxian ecosystem.

## Standard role line (GitHub description + README top section)

Use the same single line in both the GitHub repo description and the README “top section” (right below the opening paragraph):

- Flagship:
  - `Flagship — <1-line purpose>`
- Supporting:
  - `Supporting — <1-line purpose>`

## Required links for flagship READMEs

Every flagship README should include the same “Ecosystem repos” block so the trust surface is navigable:

> Keep this snippet in sync with the Flagship and Supporting repo lists above whenever the portfolio changes.

```md
## Ecosystem repos

Flagship

- https://github.com/Conxian/conxius-wallet
- https://github.com/Conxian/conxian-gateway
- https://github.com/Conxian/Conxian
- https://github.com/Conxian/Conxian_UI (rename to https://github.com/Conxian/conxian-ui)
- https://github.com/Conxian/conxian-labs-site
- https://github.com/Conxian/conxius-platform

Supporting

- https://github.com/Conxian/lib-conxian-core
- https://github.com/Conxian/lib-conclave-sdk
- https://github.com/Conxian/conxian-nexus
- https://github.com/Conxian/stacksorbit
- https://github.com/Conxian/.github
- https://github.com/Conxian/conxian-business
```
