# Wallet & Signer Control Verification Report (CON-233)

## Status: PUBLIC-SAFE SUMMARY

This file provides a non-sensitive summary of wallet and signer control posture.

> **Non-custody boundary:** Conxian-Labs and the SAB do not take custody of user assets. This summary describes signer controls for protocol operations; user keys remain self-custodied, contract principals hold protocol state where applicable, and regulated partners handle regulated custody.

Detailed signer inventories, principal/address assignments, and readiness evidence are maintained in restricted governance records.

### 1) Ownership & approval model
- Bootstrap and successor control roles are documented in governed private records.
- SAB-approved signer architecture and role boundaries are defined and reviewable through authorized channels.
- Role-based access remains a required control for protocol-critical functions.

### 2) Signing authority path
- Signing authority is managed under controlled signer standards.
- Verification pathways for operational signatures are documented in private implementation records.
- Public repositories do not publish production signer identifiers.

### 3) Emergency & recovery controls
- Emergency and recovery responsibilities are governed by approved signer policy.
- Recovery and rollback procedures exist in private operational runbooks.

### 4) Governance alignment
- Policy-mutation pathways follow staged governance controls.
- Public documentation excludes sensitive operational readiness evidence by design.
- Lifecycle `Verify`/`Release`/`Operate` control evidence for wallet-control and signer posture is tracked in [`docs/WALLET_LIFECYCLE_CONTROL_CHECKLIST.md`](./WALLET_LIFECYCLE_CONTROL_CHECKLIST.md).

---
© 2026 Conxian-Labs (Pty) Ltd.
