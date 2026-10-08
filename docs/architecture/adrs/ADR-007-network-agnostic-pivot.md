# ADR-007: Network-agnostic architecture — own protocol deprecated

## Status
Accepted (2026-10-08)

## Context
Conxian originally scoped an **own protocol**: a Clarity smart-contract layer
(`Conxian/Conxian` repo) carrying authority-transfer semantics, DAO governance,
and a Sovereign Swarm/SIDL incentive surface. BOS-001 mainnet gates
(Gate 2 authority-transfer, Gate 3 testnet rehearsal, Gate 6 mainnet handoff)
were defined against that own protocol.

The strategic direction has since pivoted to **network-agnostic**: Conxian does
not operate its own blockchain or L1. Instead it reuses existing networks and
expresses its surface as protocol-neutral rails/adaptors. The own-protocol repo
`Conxian/Conxian` was deleted intentionally (not archived).

## Decision
- Conxian is **network-agnostic**: it verifies/routes state across existing
  networks and settles on **Bitcoin L1 via Stacks**. It does not run its own chain.
- The own Clarity protocol is **deprecated**; `Conxian/Conxian` is deleted.
- The replacement architecture is:
  - `lib-conxian-core` — protocol-neutral `SettlementRail` (8 rails) and
    `TrustTier` (Strict/Managed/Expedient/ObserverOnly) as the canonical
    cross-network model.
  - `conxius-enclave-sdk` — signing/attestation (FROST threshold, KMS quorum,
    Nitro, Android KeyMint/StrongBox).
  - `conxian-nexus` + `conxian-gateway` — indexing/finality/proof and
    routing/policy across the Tier 1 chain families (ADR-006).
- BOS-001 own-protocol gates are **superseded**:
  - Gates 2/3/6 (authority-transfer, testnet rehearsal, mainnet handoff) are
    obsolete — there is no own protocol to transfer, rehearse, or hand off.
  - Gates 4/5 (hardware signing, independent review) are **re-homed** to the
    enclave-sdk domain (`#202`/#240`/#241`).

## Consequences
- Documentation that treats the own protocol as the core architecture
  (Clarity/`.clar`/SIDL/Sovereign Swarm) is superseded or re-scoped to the
  protocol-neutral rail model.
- The capabilities registry (`.github-private/docs/CAPABILITY_GATES.json`) records
  a `superseded` state for the own-protocol gates; the still-relevant signing and
  independent-review gates are tracked under `enclave-sdk.signing`.
- There is no own-protocol mainnet launch. "Mainnet" = Bitcoin/Stacks, already live.
- Future protocol work is expressed as **protocol-neutral adaptors/rails**, not
  new L1 contracts. Adding a new network family follows ADR-006's promotion path.
