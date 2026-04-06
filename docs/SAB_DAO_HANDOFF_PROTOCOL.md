# SAB/DAO handoff protocol (CON-423)

This document defines the staged handoff protocol from personal bootstrap control to the Sovereign Advisory Board (SAB) and finally to the Decentralized Autonomous Organization (DAO).

For canonical wallet classes and the more granular staged migration protocol, see [`docs/BOS_WALLET_CONTROL_MODEL.md`](./BOS_WALLET_CONTROL_MODEL.md).

Stage mapping note: relative to `docs/BOS_WALLET_CONTROL_MODEL.md`, Stage 1 here ≈ Stage 0 (bootstrap allowed), Stage 2 here ≈ Stage 1–3 (SAB custody establishment + admin surface migration + automation cutover), and Stage 3 here ≈ Stage 4+ (DAO alignment).

## Handoff stages

### Stage 1: Personal bootstrap (Initial Deployment)
- **Status:** Current (Bootstrap-only).
- **Custodian:** Developer / Operator personal address.
- **Authority:** Full administrative control for deployment, initialization, and testnet validation.
- **Risk:** High centralization / single-point-of-failure.
- **Exit criterion:** Core protocol contracts deployed and verified on testnet; mainnet deployment plan finalized.

### Stage 2: SAB-controlled custody (Operational Launch)
- **Status:** Required for Initial Mainnet Release.
- **Custodian:** SAB-controlled multi-sigs and system-controlled agents.
- **Authority:** Operational execution, parameter adjustments within defined bounds, and initial fee capture.
- **Handoff action:** Transfer contract-owner roles to the appropriate SAB multi-sigs and emergency authorities as defined in [`docs/BOS_WALLET_CONTROL_MODEL.md`](./BOS_WALLET_CONTROL_MODEL.md).
- **Exit criterion:** Protocol fees provably accruing to SAB-owned vaults; payout enablement (if any) follows separate readiness gates.

### Stage 3: DAO-aligned governance (Long-term Decentralization)
- **Status:** Post-launch maturity.
- **Custodian:** Community-governed DAO and automated policy engines.
- **Authority:** Root policy control, treasury rebalancing, and fee rate setting.
- **Handoff action:** Transfer root administrative authority to the DAO-controlled executor contract and timelock.
- **Verification:** Continuous on-chain audit of state updates and policy changes.

## Step-by-step handoff procedure

Note: contract ownership transfer interfaces vary by contract. Some use a two-step (pending -> claim) flow; others are single-step. The steps below are intentionally interface-agnostic and list common function names as examples.

Definition: "SAB authority" means the designated SAB-controlled multisig or executor principal for that contract, as defined in [`docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md`](./SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md).

| Step | Action | Responsibility | Verification |
| :--- | :--- | :--- | :--- |
| **P-1** | Define the canonical mainnet principal for every required SAB wallet. | Operator | Publicly document in `docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md`. |
| **P-2** | Replace hardcoded principals in Clarinet plans and deployment scripts with the target SAB principals. | Dev | Pass CI verification for mainnet deployment plans. |
| **P-3** | For each core contract, record its ownership-transfer mode (single-step vs two-step) in the control matrix before executing **H-2**/**H-3**. | Operator | Updated entries in `docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md`. |
| **H-1** | Deploy and initialize the `governance-handover` contract. | Operator | Verify contract on Stacks Explorer. |
| **H-2** | Execute the contract-specific ownership/admin transfer action, targeting the designated SAB authority. Two-step: set the pending/next owner/admin (e.g., `set-pending-owner`). Single-step: complete the transfer (e.g., `transfer-ownership`, `set-owner`). | Bootstrap Wallet | Confirm transaction status on-chain. |
| **H-3** | Only for two-step contracts: from the designated SAB authority, accept/claim the pending owner/admin update (e.g., `claim-ownership`, `accept-ownership`). Skip this step for single-step transfers (ownership/admin is already fully transferred in **H-2**). | SAB Signers | Confirm final owner/admin update. |
| **V-1** | Verify that no bootstrap or personal address remains as a privileged role or recipient in the protocol. | Auditor | Run `python3 scripts/verify_bos_production_boundary.py` + `python3 scripts/verify_contamination_guard.py` (repo/system boundary checks; does **not** replace on-chain privilege verification). Then complete the on-chain checklist below for each core contract enumerated in the control matrix. |

### H-2/H-3 transfer mode notes
- **Two-step transfers:** **H-2** sets the pending/next owner/admin to the designated SAB authority, and **H-3** is executed by the SAB authority to accept/claim the pending owner/admin update.
- **Single-step transfers:** **H-2** completes the transfer, and **H-3** is skipped.

### V-1 on-chain checklist (per core contract, per control matrix)
- `owner`/`admin` (or equivalent privileged roles, including any privileged role maps) match the designated SAB authority
- all fee/recipient addresses match the control matrix

## Rollback authority (Emergency Action)
During the transition between Stage 2 and Stage 3, a **rollback authority** is maintained by the **Emergency Control** wallet class to revert changes if critical bugs are found. Once Stage 3 is fully achieved, this authority is strictly bounded by the DAO-controlled timelock (default 144 blocks).

## DAO policy handoff
After the custody handoff, the **Policy Handoff** ensures the DAO controls the parameters.
1. The **SAB** remains the executor of the protocol.
2. The **DAO** controls the policy (the "What") by setting parameters in the governance layer.
3. The **Agents** execute the policy (the "How") via the BOS automation loop.
