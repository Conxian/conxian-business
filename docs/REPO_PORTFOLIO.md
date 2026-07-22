# Repo portfolio trust-surface view

This page is an explanatory view of the Conxian-Labs repository portfolio for public evaluation and internal consistency. It does not replace the central [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md) or the [Portfolio Business-Unit Map](./PORTFOLIO_BUSINESS_UNIT_MAP.md).

For the doctrine that applies across every surface, see:

- [Doctrine Alignment Standard](./DOCTRINE_ALIGNMENT_STANDARD.md)
- [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md)
- [Trust & Proof Messaging](./TRUST_AND_PROOF_MESSAGING.md)
- [Repo Readiness Gates](./REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md)

## Source-of-truth boundaries

- Repos governed through this BOS repository are pinned as submodule gitlinks; paths and URLs are configured in `.gitmodules`.
- Every pinned submodule must be mapped in `docs/PORTFOLIO_BUSINESS_UNIT_MAP.md`.
- Repositories listed for context but not pinned are not governed by this repository’s submodule hygiene invariants unless they are added and mapped.
- The doctrine register is authoritative for role, audience, operating label, maturity, claim state, document classification, and contradiction disposition. This file only provides navigation and short role lines.

## Standard role line

Use one conservative role line in a repository description and the top of its README. Choose the repository’s operating label from the doctrine register; do not use the role line to imply custody, market operation, or readiness.

- Primary strategic: `Primary strategic — <one-line protocol, infrastructure, or client purpose>`
- Supporting: `Supporting — <one-line shared, governance, or developer purpose>`
- Reference: `Reference — <one-line public surface or demonstrator purpose>`
- Governance baseline: `Governance baseline — <one-line specification and boundary purpose>`
- Internal only: `Internal only — <one-line restricted coordination purpose>`

## Ecosystem repos

### Primary strategic

These are protocol, infrastructure, and client surfaces with primary architectural responsibility. Their maturity and claim state remain evidence-scoped in the doctrine register.

- [Conxian](https://github.com/Conxian/Conxian) — Protocol and on-chain contract layer.
- [conxian-gateway](https://github.com/Conxian/conxian-gateway) — Institutional routing, aggregation, and compliance middleware.
- [conxian-nexus](https://github.com/Conxian/conxian-nexus) — State, proof, synchronization, and telemetry node.
- [conxius-wallet](https://github.com/Conxian/conxius-wallet) — Android-first, offline-first self-custody client and signing surface.

### Supporting

These repositories provide shared primitives, local orchestration, deployment tooling, organization defaults, or governance support.

- [lib-conxian-core](https://github.com/Conxian/lib-conxian-core) — Shared protocol models, serialization, cryptographic, and state primitives.
- [conxius-enclave-sdk](https://github.com/Conxian/conxius-enclave-sdk) — Enclave, signing, and attestation abstractions.
- [conxius-platform](https://github.com/Conxian/conxius-platform) — Local stack composition and developer orchestration.
- [conxius-orbit](https://github.com/Conxian/conxius-orbit) — Stacks contract deployment and operations tooling.
- [.github](https://github.com/Conxian/.github) — Organization governance defaults and templates.

### Reference surfaces

- [`conxian_ui`](https://github.com/Conxian/Conxian_UI) — Public web interaction surface; upstream GitHub slug is retained, while display text is normalized.
- [conxian-labs-site](https://github.com/Conxian/conxian-labs-site) — Public website and documentation distribution surface.
- [demo-repository](https://github.com/Conxian/demo-repository) — Organization demonstration surface.
- [conxian.github.io](https://github.com/Conxian/conxian.github.io) — Public documentation/site hub.
- [conxian_market](https://github.com/Conxian/conxian_market) — Research/experimental marketplace surface pending external doctrine alignment.

### Governance baseline

- [conxian-business](https://github.com/Conxian/conxian-business) — Governance, OpenSpec, portfolio wiring, and public-safe trust surface.

### Internal coordination

- `.github-private` — Restricted ecosystem registry; not a public evidence surface.

## README canonical links

Portfolio-entry READMEs should link to:

- `../docs/DOCTRINE_ALIGNMENT_STANDARD.md`
- `../docs/PORTFOLIO_DOCTRINE_REGISTER.md`
- `../docs/REPO_PORTFOLIO.md`
- `../docs/PORTFOLIO_BUSINESS_UNIT_MAP.md`
- `../docs/DOCUMENTATION_ALIGNMENT_INDEX.md`

If a README lives at a different depth, keep the same targets and adjust the relative paths. Use [Claim vs Evidence Matrix](./CLAIM_EVIDENCE_MATRIX.md) for claim wording and [Trust & Proof Messaging](./TRUST_AND_PROOF_MESSAGING.md) for public proof expectations.
