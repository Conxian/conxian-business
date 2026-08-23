# Portfolio repository inventory (CON-468)

This is the release-criticality inventory for the repositories listed here, classified by layer, role, and evaluation standard. The complete 16-repository doctrine and disposition map is the [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md).

For the current doctrine dimensions—role, audience, operating label, maturity, claim state, document classification, and contradiction disposition—see the [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md) and [Doctrine Alignment Standard](./DOCTRINE_ALIGNMENT_STANDARD.md). This inventory’s release-criticality field is not a maturity or claim-state label.

## Layer Taxonomy

- **Decentralization-critical**: Core protocol, state-consensus, and trust-minimized execution.
- **User and application surface**: Direct interaction layers for retail, business, and enterprise users.
- **Shared runtime and developer infrastructure**: SDKs, core libraries, and internal orchestration tools.
- **Governance and operating system**: BOS governance, OpenSpec, and internal EXCO coordination modules.

## Evaluation Standards (Release Criticality, separate from maturity)

- **P0**: Mainnet release blockers. Must adhere to strict production standards (no stubs, no testnet contamination).
- **P1**: Important supporting surfaces. Should follow standards; drift is not immediately mainnet-blocking.
- **P2**: Nice-to-have, experimental, or informational surfaces.

## Canonical Repository Map

| Repository | Layer | Role / Function | Owner | Standard |
| :--- | :--- | :--- | :--- | :--- |
| `conxian-business` | Governance | BOS & OpenSpec Governance | @botshelomokoka | P0 |
| `Conxian` | Decentralization | CSF Core Protocol (Clarity) | @botshelomokoka | P0 |
| `conxian-nexus` | Decentralization | Nexus State Node (Rust) | @botshelomokoka | P0 |
| `conxian-gateway` | Decentralization | Fusion Gateway (Rust Engine) | @botshelomokoka | P0 |
| `conxius-wallet` | User Surface | Sovereign Multi-chain Wallet | @botshelomokoka | P0 |
| `lib-conxian-core` | Shared Runtime | Shared Cryptographic & State Logic | @botshelomokoka | P0 |
| `conxius-enclave-sdk` | Shared Runtime | Enclave and attestation SDK | @botshelomokoka | P0 |
| `conxius-orbit` | Shared Runtime | Contract deployment and operations tooling | @botshelomokoka | P0 |
| `conxian_ui` (checkout `conxian-ui`; upstream slug retained) | User Surface | Public web interaction layer | @botshelomokoka | P1 |
| `conxius-platform` | Shared Runtime | Developer Platform & Orchestration | @conxian/core-devs | P1 |
| `conxian-labs-site` | User Surface | Public Communication Surface | @botshelomokoka | P2 |
| `Fiscal-Vault-Oracle` | Governance | Protocol/reference policy and oracle surface; not company treasury control | @botshelomokoka | P0 |
| `Nakamoto-Guardian` | Governance | EXCO: Compliance & Security | @botshelomokoka | P0 |
| `Sovereign-Ops-Orchestrator` | Governance | EXCO: Operations & Service Loop | @botshelomokoka | P0 |
| `Sovereign-Strategy-Nexus` | Governance | Public-safe strategy coordination stub; full internal strategy remains in restricted vault/secure storage | @botshelomokoka | P1 |
| `cxn-grid-oracle` | Shared Runtime | Decentralized Data Oracle | @botshelomokoka | P1 |
| `showcase-dapp` | User Surface | Demo & Integration Showcase | @botshelomokoka | P2 |
| `.github` | Governance | Org-wide Standards & Workflows | @Conxian/Admins | P0 |

---
© 2026 Conxian-Labs (Pty) Ltd.
