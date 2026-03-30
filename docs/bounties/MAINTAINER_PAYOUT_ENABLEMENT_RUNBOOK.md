# Maintainer runbook: bounty payout enablement (ALEX-funded)

This is a maintainer-only checklist for enabling bounty payouts after ConxianCSF mainnet launch.

## Definitions

- **Payout-ready mode**: Maintainers have approved the program to begin sending bounty payments to contributors.
- **ALEX launch funding source (sole allowed source)**: `SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.alex-vault`.
- **Payout wallet**: The internal maintainer-controlled wallet/multisig that sends bounty payments.

## Payout enablement checklist (short)

### 1) Verify ConxianCSF full deployment on Stacks mainnet

1. Confirm the `alex-adapter` mainnet deployment batch ran as planned (see `Conxian/deployments/mainnet-release-plan.yaml`).
   - `contract-publish` succeeded for `alex-adapter`.
   - The follow-up `contract-call` succeeded:
     - contract: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.dex-factory`
     - method: `register-csf-protocol`
     - parameter: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.alex-adapter`
2. Confirm core contracts are present on mainnet and readable (minimum set):
   - `conxian-protocol`
   - `cxd-token`
   - `bme-engine`
   - `cxd-treasury`
   - `revenue-distributor`
   - `ops-engine`
   - `alex-adapter`
3. Confirm mainnet read-only health calls succeed and return sane values:
   - `bme-engine/get-protocol-status` returns `compliant: true`.
   - `ops-engine/get-protocol-status` returns `compliant: true`.
   - `alex-adapter/get-csf-health` returns `is-active: true`.

**Evidence to attach to the go/no-go record**: txids for the deployment and registration step, plus the read-only call outputs.

### 2) Verify ALEX launch source of funds is active and is the sole bounty funding source

1. Verify the ALEX funding source principal is exactly:
   - `SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.alex-vault`
2. Verify the payout wallet received at least one inbound funding transfer from the ALEX vault principal.
3. Verify the payout wallet received no inbound bounty funding transfers from any other principal since mainnet launch.

**Evidence to attach**: a short list of inbound funding txids to the payout wallet (last N transfers) with senders.

### 3) Verify signer / wallet ownership / approval controls (internal)

1. Confirm the payout wallet is controlled by maintainers (multisig or equivalent) and the signer set matches the internal custody record.
2. Confirm the minimum approval policy for bounty payouts is configured (example: 2-of-3 maintainers).
3. Confirm the incident owner (single human) is assigned for payout enablement week (who can make the stop decision immediately).

**Evidence to attach**: internal signoff record (no keys), signer set summary, and the incident owner name.

### 4) Verify post-deploy checks completed successfully

1. Confirm the last on-chain upgrade/deploy window is closed (no pending contract publishes or admin migrations).
2. Run a mainnet heartbeat smoke call and confirm expected behavior:
   - `ops-engine/trigger-epoch-update` returns `(ok true)`.
3. Confirm monitoring is live for:
   - `ops-engine/get-engine-status` (last action advancing)
   - inbound transfers to the payout wallet
   - outbound transfers from the payout wallet

**Evidence to attach**: txid for the heartbeat smoke call, plus monitoring links or screenshots.

### 5) Verify contributor-facing messaging is still non-payout unless the gate is enabled

Before enablement, contributor-facing copy must clearly state:

> Your submission/claim has been recorded, but payouts are not enabled yet. Do not treat any issue thread as payout-ready unless maintainers explicitly enable payout-ready mode.

## Maintainer-only go/no-go decision

**GO** only if all checklist sections 1–5 are complete and evidence is attached.

**NO-GO** if any of the following is true:

- The payout wallet has any non-ALEX inbound bounty funding transfers.
- `alex-adapter/get-csf-health` is not active.
- Any of the core read-only health checks fail.
- No incident owner is assigned.

## Maintainer action: flip to payout-ready

1. Create a maintainer-only decision record (internal) that includes:
   - the evidence items above
   - timestamp
   - 2 maintainer approvals
2. Post a short public announcement in the canonical bounty channel (GitHub issue / Linear) stating: "Payouts enabled" and the effective timestamp.
3. Begin processing payouts from the payout wallet according to the approval policy.

## Rollback: disable payouts (premature enablement or post-deploy issue)

### Immediate stop steps

1. Freeze outbound payments from the payout wallet (pause the signing flow; do not queue new transfers).
2. Post a public status update in the canonical bounty channel stating: "Payouts paused" and the effective timestamp.

### Funding-source containment

1. If the ALEX vault is no longer the sole funding source, treat this as a payout halt condition.
2. Reconcile inbound funding transfers and document the unexpected funding source(s) before resuming.

### Resume criteria

Resume only after:

- funding-source invariants are restored (ALEX vault is the sole inbound bounty funder)
- incident owner signs off that the triggering issue is resolved
- 2 maintainers re-approve payout-ready mode with updated evidence
