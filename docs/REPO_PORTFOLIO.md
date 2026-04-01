# Repo portfolio (flagship vs supporting)

This page defines the Conxian public repo map for external evaluation and internal consistency.

Note: the UI repo is still named `Conxian/Conxian_UI` and is planned to be renamed to `Conxian/conxian-ui` for naming consistency (track in [CON-238](https://linear.app/conxian-labs/issue/CON-238/define-flagship-repos-and-external-trust-surface)).

## Flagship (external trust surface)

Flagship repos are the external trust surface. The canonical list lives in [Ecosystem repos](#ecosystem-repos).

## Supporting (linked from flagship READMEs; not pinned)

Supporting repos are linked from flagship repos but are not the primary trust surface. The canonical list lives in [Ecosystem repos](#ecosystem-repos).

## Standard role line (GitHub description + README top section)

Use the same single line in both the GitHub repo description and the README “top section” (right below the opening paragraph):

- Flagship:
  - `Flagship — <1-line purpose>`
- Supporting:
  - `Supporting — <1-line purpose>`

## Ecosystem repos

Every flagship README should include this section so the trust surface is navigable. This is the canonical list; update it here only.

### Flagship

- https://github.com/Conxian/conxius-wallet — Sovereign wallet (Android-first, offline-first) for Bitcoin L1 and Bitcoin-adjacent layers.
- https://github.com/Conxian/conxian-gateway — “Fusion” gateway aggregating cross-layer state + compliance pipelines.
- https://github.com/Conxian/Conxian — Core protocol + on-chain contracts.
- https://github.com/Conxian/Conxian_UI (planned rename to https://github.com/Conxian/conxian-ui) — Primary UI for interacting with the Conxian ecosystem.
- https://github.com/Conxian/conxian-labs-site — Public Conxian Labs website.
- https://github.com/Conxian/conxius-platform — Local dev stack to run the ecosystem end-to-end.

### Supporting

- https://github.com/Conxian/lib-conxian-core — Shared core models + conventions used across services.
- https://github.com/Conxian/lib-conclave-sdk — Headless enclave + cryptographic state machine SDK.
- https://github.com/Conxian/conxian-nexus — API bridge (“Glass Node”) between layers/services.
- https://github.com/Conxian/stacksorbit — Stacks smart-contract deployment tooling.
- https://github.com/Conxian/.github — Org-wide defaults (community health files, templates).
- https://github.com/Conxian/conxian-business — Governance + OpenSpec + submodule wiring for the Conxian ecosystem.
