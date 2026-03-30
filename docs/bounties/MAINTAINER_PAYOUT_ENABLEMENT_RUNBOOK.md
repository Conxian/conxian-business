# Maintainer runbook: bounty payout enablement (ALEX-funded)

This is a maintainer-only checklist for enabling bounty payouts after ConxianCSF mainnet launch.

## Definitions

- **Payout-ready mode**: Maintainers have approved the program to begin sending bounty payments to contributors.
- **ALEX launch funding source (sole allowed source)**: `SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.alex-vault`.
- **Payout wallet**: The internal maintainer-controlled wallet/multisig that sends bounty payments.

## Mainnet identifiers (March 2026 release)

- **ConxianCSF mainnet deployer principal**: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P` (from [`Conxian/deployments/mainnet-release-plan.yaml`](../../Conxian/deployments/mainnet-release-plan.yaml)).
- **ALEX DEX factory contract**: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.dex-factory`.

## Payout enablement checklist (short)

### 1) Verify ConxianCSF full deployment on Stacks mainnet

1. Confirm the `alex-adapter` mainnet deployment batch ran as planned (see the mainnet release plan in this repo: [`Conxian/deployments/mainnet-release-plan.yaml`](../../Conxian/deployments/mainnet-release-plan.yaml)).
   - In the go/no-go record, include a GitHub permalink to the release plan pinned to the exact deployment commit (in GitHub UI: press `y` to generate a commit-pinned URL).
   - `contract-publish` succeeded for `alex-adapter`.
   - The follow-up `contract-call` succeeded:
     - contract: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.dex-factory`
     - method: `register-csf-protocol`
     - parameter: `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.alex-adapter`
2. Confirm core contracts are present on mainnet and readable (minimum set; fully-qualified):
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.conxian-protocol`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.cxd-token`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.bme-engine`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.cxd-treasury`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.revenue-distributor`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.ops-engine`
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.alex-adapter`
3. Confirm mainnet read-only health calls succeed and return sane values:
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.bme-engine/get-protocol-status` decodes to `compliant: true`.
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.ops-engine/get-protocol-status` decodes to `compliant: true`.
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.alex-adapter/get-csf-health` decodes to `is-active: true`.

#### How to run the read-only checks (reproducible)

- Use the Stacks API / explorer of choice, but always attach raw outputs.
- Minimum explorer sanity check: open `https://explorer.hiro.so/address/ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P?chain=mainnet` and confirm the expected contracts exist under the deployer principal.

CLI example (raw output + optional decode):

```bash
API_BASE='https://api.mainnet.hiro.so'
SENDER='ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P'

curl -sS -X POST \
  "$API_BASE/v2/contracts/call-read/ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P/bme-engine/get-protocol-status" \
  -H 'Content-Type: application/json' \
  -d "{\"sender\":\"$SENDER\",\"arguments\":[]}" \
  | tee /tmp/bme-engine.get-protocol-status.json

# Optional decode (requires @stacks/transactions available in your environment)
bun -e 'import { hexToCV, cvToJSON } from "@stacks/transactions";
const hex = process.argv[2];
console.log(JSON.stringify(cvToJSON(hexToCV(hex)), null, 2));' \
  "$(jq -r '.result' /tmp/bme-engine.get-protocol-status.json)"
```

**Evidence to attach to the go/no-go record**: txids for the deployment and registration step, plus the read-only call outputs.

### 2) Verify ALEX launch source of funds is active and is the sole bounty funding source

1. Verify the ALEX funding source principal is exactly:
   - `SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.alex-vault`
2. Verify the payout wallet received at least one inbound funding transfer from the ALEX vault principal.
3. Verify the payout wallet received no inbound bounty funding transfers from any other principal since mainnet launch.

For this checklist, treat any inbound STX transfer to the payout wallet as bounty funding unless explicitly reconciled as unrelated and documented in the decision record.
tmpfile="$(mktemp)"

#### Funding-source verification procedure (reproducible)

1. Define the mainnet launch boundary as the `block_height` of the `alex-adapter` publish txid from section (1) (record this in the decision record).
2. Export inbound transfers for the payout wallet and verify the sender set.
   - Important: paginate (`offset=`) until there are no more results.

```bash
API_BASE='https://api.mainnet.hiro.so'
ALEX_VAULT='SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.alex-vault'
: "${PAYOUT_WALLET:?Set PAYOUT_WALLET to the payout wallet principal/address}"
LAUNCH_BLOCK_HEIGHT=123456 # block height of alex-adapter publish txid

# Export inbound STX transfers to the payout wallet.
limit=200
offset=0
while :; do
  page="$(curl -sS "$API_BASE/extended/v1/address/$PAYOUT_WALLET/assets?limit=$limit&offset=$offset")"
  n="$(echo "$page" | jq '.results | length')"
  [ "$n" -eq 0 ] && break

  echo "$page" | jq -r --arg wallet "$PAYOUT_WALLET" '
    .results[]
    | select(.event_type=="stx_asset")
    | select(.asset.asset_event_type=="transfer")
    | select(.asset.recipient==$wallet)
    | [.tx_id, .asset.sender, .asset.amount] | @tsv
  '

  offset=$((offset+limit))
done | tee /tmp/payout-wallet.inbound-stx.tsv

# Must be at least one ALEX inbound funding transfer.
awk -v alex="$ALEX_VAULT" '$2 == alex' /tmp/payout-wallet.inbound-stx.tsv | head

# Must be zero non-ALEX inbound STX funding transfers.
awk -v alex="$ALEX_VAULT" '$2 != alex {print}' /tmp/payout-wallet.inbound-stx.tsv

# Strict boundary check (since launch): lists any non-ALEX senders for inbound STX transfers at/after LAUNCH_BLOCK_HEIGHT.
limit=50
offset=0
tmpfile="$(mktemp)"
trap 'rm -f "$tmpfile"' EXIT
: > "$tmpfile"

while true; do
  page="$(curl -sS "$API_BASE/extended/v1/address/$PAYOUT_WALLET/transactions?limit=${limit}&offset=${offset}")"

  echo "$page" | jq -r --argjson launch "${LAUNCH_BLOCK_HEIGHT}" --arg alex "${ALEX_VAULT}" --arg payout "${PAYOUT_WALLET}" '
    .results
    | map(select(.block_height >= $launch))
    | map(select(.tx_type == "token_transfer" and (.token_transfer.recipient_address == $payout)))
    | map(select(.token_transfer.sender_address != $alex))
    | .[].token_transfer.sender_address
  ' >> "$tmpfile"

  count="$(echo "$page" | jq '.results | length')"
  min_height="$(echo "$page" | jq '.results | map(.block_height) | min // 0')"
  if [ "$count" -lt "$limit" ] || [ "$min_height" -lt "$LAUNCH_BLOCK_HEIGHT" ]; then
    break
  fi

  offset=$((offset + limit))
done

sort -u "$tmpfile"
```

Treat any non-ALEX inbound transfer as **NO-GO** unless explicitly reconciled as unrelated and documented in the decision record.

**Evidence to attach**: a short list of inbound funding txids to the payout wallet (last N transfers) with senders.

### 3) Verify signer / wallet ownership / approval controls (internal)

1. Confirm the payout wallet is controlled by maintainers (multisig or equivalent) and the signer set matches the internal custody record.
2. Confirm the minimum approval policy for bounty payouts is configured (example: 2-of-3 maintainers).
3. Confirm the incident owner (single human) is assigned for payout enablement week (who can make the stop decision immediately).

**Evidence to attach**: internal signoff record (no keys), signer set summary, and the incident owner name.

### 4) Verify post-deploy checks completed successfully

1. Confirm the last on-chain upgrade/deploy window is closed (no pending contract publishes or admin migrations).
2. Do not run state-changing "smoke calls" as part of payout enablement.
   - Prefer read-only checks (Step 1 health calls, plus `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.ops-engine/get-engine-status`).
3. Confirm monitoring is live for:
   - `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.ops-engine/get-engine-status` (last action advancing)
   - inbound transfers to the payout wallet
   - outbound transfers from the payout wallet

**Evidence to attach**: read-only outputs for `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.ops-engine/get-engine-status`, plus monitoring links or screenshots.

### 5) Verify contributor-facing messaging is still non-payout unless the gate is enabled

Before enablement, contributor-facing copy must clearly state:

> Your submission/claim has been recorded, but payouts are not enabled yet. Do not treat any issue thread as payout-ready unless maintainers explicitly enable payout-ready mode.

## Maintainer-only go/no-go decision

**GO** only if all checklist sections 1–5 are complete and evidence is attached.

**NO-GO** if any of the following is true:

- The payout wallet has any non-ALEX inbound bounty funding transfers.
- `ST1BK6TFDEJ4TBVWH5SHNB6SPNWGY06YZFG9WMM4P.alex-adapter/get-csf-health` is not active.
- Any of the core read-only health checks fail.
- No incident owner is assigned.

## Maintainer action: declare payout-ready

Payout-ready mode is operational-only: there is no on-chain or config toggle. Maintainers declare payout-ready mode via the decision record + announcement, then execute payouts manually from the payout wallet.

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
