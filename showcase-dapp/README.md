# Conxian Showcase DApp (March 2026 Audit Baseline)

The **Conxian Showcase DApp** is a reference implementation demonstrating the integration of Conxian protocol primitives (Clarity) with a modern web frontend (Next.js 15).

## Purpose
- Provide a "living specification" for frontend developers.
- Demonstrate standard patterns for wallet connection, contract interaction, and ZSE (Zero Secret Egress) compliance in the browser.
- Serve as a staging ground for new UI components from `conxian-ui`.

## Status
**Incubating.** This is a demonstration tool and reference implementation. For production-ready interfaces, see [Conxian UI](../conxian-ui) and [Conxius Wallet](../conxius-wallet).

## Relationship to the Conxian stack
- **Consumer**: Interacts with `Conxian` protocol contracts and `conxian-gateway` APIs.
- **Showcase**: Uses the centralized component library from `conxian-ui`.
- **Standard-bearer**: Enforces the Conxian Lexicon Enforcement Protocol (cxn- prefixing).

## Development

```bash
cd showcase-dapp
pnpm install
pnpm run dev
```

## Governance
This module is part of the Conxian Sovereign Autonomous Business (SAB).

- [**LICENSE**](./LICENSE): GNU GPL v3.0.
- [**CONTRIBUTING.md**](./CONTRIBUTING.md): Project-specific contribution guidance.
- [**SECURITY.md**](./SECURITY.md): Security reporting process.

For ecosystem-level governance, see the [Root Governance](../GOVERNANCE.md).

---
🛡️ **Sovereign Autonomous Business (SAB)**. © 2026 Conxian-Labs.
