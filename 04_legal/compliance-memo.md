# Compliance Memo: Non-Custodial Regulatory Position

## Overview
Conxian Labs operates a strictly non-custodial architecture.

## Technical Architecture
- **Key Management**: User keys are generated and stored exclusively within on-device Trusted Execution Environments (TEE) or StrongBox.
- **Access Control**: Authentication via Fusion Auth (JWT/Enclave-based).
- **Sovereignty**: No private keys are transmitted to or stored by Conxian Labs servers.

## Regulatory Position
Since Conxian Labs never takes custody of user assets, it does not fall under traditional money transmitter regulations in most jurisdictions. All actions are mathematically certain and governed by SAB (Sovereign Autonomous Business) logic.
