# SAB/DAO handoff protocol (CON-423)

This document defines the staged handoff protocol from personal bootstrap control to the Sovereign Advisory Board (SAB) and finally to the Decentralized Autonomous Organization (DAO).

> **Boundary notice:** This is a protocol and signer-control transition, not a transfer of user or customer assets to Conxian-Labs or the SAB. User keys remain self-custodied, contract principals hold protocol state where applicable, DAO governance controls protocol policy, and regulated partners remain responsible for regulated custody.

For canonical wallet classes and the more granular staged migration protocol, see [`docs/BOS_WALLET_CONTROL_MODEL.md`](./BOS_WALLET_CONTROL_MODEL.md).

Stage mapping note: relative to `docs/BOS_WALLET_CONTROL_MODEL.md`, Stage 1 here ≈ Stage 0 (bootstrap allowed), Stage 2 here ≈ Stage 1–3 (SAB-approved protocol-control establishment + admin surface migration + automation cutover), and Stage 3 here ≈ Stage 4+ (DAO alignment).

## Handoff stages

### Stage 1: Personal bootstrap (Initial Deployment)
- **Status:** Current (Bootstrap-only).
- **Control holder:** Developer / operator personal address for deployment preparation only; this is not user-asset custody.
- **Authority:** Temporary administrative control for deployment, initialization, and testnet validation.
- **Risk:** High centralization / single-point-of-failure.
- **Exit criterion:** Core protocol contracts deployed and verified on testnet; mainnet deployment plan finalized.

### Stage 2: SAB-operated protocol controls (Operational Launch)
- **Status:** Required for Initial Mainnet Release.
- **Control boundary:** SAB-approved multi-sigs and system signers for protocol and approved operational actions; no company or user-asset custody is implied.
- **Authority:** Operational execution, parameter adjustments within defined bounds, and protocol-defined fee routing.
- **Handoff action:** Transfer contract-owner roles to the appropriate SAB multi-sigs and emergency authorities as defined in [`docs/BOS_WALLET_CONTROL_MODEL.md`](./BOS_WALLET_CONTROL_MODEL.md).
- **Exit criterion:** Protocol fees provably accruing to protocol/DAO-defined contract vaults; payout enablement (if any) follows separate readiness gates.

### Stage 3: DAO-aligned governance (Long-term Decentralization)
- **Status:** Post-launch maturity.
- **Governance boundary:** Community-governed DAO and automated policy engines define protocol policy; this does not make Conxian-Labs a custodian.
- **Authority:** Root protocol-policy control, contract-defined treasury parameters, and fee-rate setting.
- **Handoff action:** Transfer root administrative authority to the DAO-controlled executor contract and timelock.
- **Verification:** Continuous on-chain audit of state updates and policy changes.

## Step-by-step handoff procedure

Note: contract ownership transfer interfaces vary by contract. Some use a two-step (pending -> claim) flow; others are single-step. The steps below are intentionally interface-agnostic and list common function names as examples.

| Step | Action | Responsibility | Verification |
| :--- | :--- | :--- | :--- |
| **P-1** | Define the canonical mainnet principal for every required SAB wallet. | Operator | Publicly document in `docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md`. |
| **P-2** | Replace hardcoded principals in Clarinet plans and deployment scripts with the target SAB principals. | Dev | Pass CI verification for mainnet deployment plans. |
| **H-1** | Deploy and initialize the `governance-handover` contract. | Operator | Verify contract on Stacks Explorer. |
| **H-2** | Initiate ownership transfer on each core contract, setting the intended SAB authority as the next owner/admin (e.g., `set-pending-owner`, `transfer-ownership`, `set-owner`). | Bootstrap Wallet | Confirm transaction status on-chain. |
| **H-3** | Finalize ownership transfer from the receiving SAB authority where required (e.g., `claim-ownership`, `accept-ownership`). | SAB Signers | Confirm final owner/admin update. |
| **V-1** | Verify that no bootstrap or personal address remains as a privileged role or recipient in the protocol. | Auditor | Successful `python3 scripts/verify_bos_production_boundary.py` + `python3 scripts/verify_contamination_guard.py` run, plus on-chain owner/admin and recipient confirmation for each core contract. |

## Rollback authority (Emergency Action)
During the transition between Stage 2 and Stage 3, a **rollback control** is maintained by the **Emergency Control** wallet class to revert protocol configuration if critical bugs are found. Once Stage 3 is fully achieved, this authority is strictly bounded by the DAO-controlled timelock (default 144 blocks).

## DAO policy handoff
After the control handoff, the **Policy Handoff** ensures the DAO controls the protocol parameters.
1. The **SAB** remains the executor of the protocol.
2. The **DAO** controls the policy (the "What") by setting parameters in the governance layer.
3. The **Agents** execute the policy (the "How") via the BOS automation loop.

Revenue-policy evidence and ownership boundaries are indexed in the [CON-1542 typed digest](../BOS_KNOWLEDGE_GRAPH.md#typed-digest-con-1542-conxian-538-revenue-automation-policy-handoff-2026-07-25). That digest does not authorize a founder allocation or treat source, plan, routing, or observation artifacts as proof of deployment or live revenue.
