# Sovereign recovery execution and outcome evidence

Classification: Public-safe supporting execution guide. Claim state: Implemented
independent public-archive verification; target-state wider operator recovery.
Coordination: #1390 / #1423 / #1317 / #1415; M&A #1491 and economics #1419.

The owner has approved the complete decentralised path. This approval is the
standing direction for research, implementation, qualification and migration;
it does not need to be re-requested at each capability. Repository review,
confidential disclosure, custody and release responsibilities remain distinct.

Business #1496 is merged into dev at
`52c405d25a4f0a5f23233e1d3049581ad126f95c`; its actual tree is
`2fbdcc8c9bafb39ec226ca441de40db7c80e1b98`. Canonical KB #78 is merged at
`e6d15edc8414ded526379f9df5631aa718d42a4c`. The review endpoint returned no
submitted reviews at this refresh; a merge is an observed integration event,
not evidence from which to invent an independent review decision. Previous
dated records are retained.

## Concrete outcome

For each qualified workload, an operator must be able to acquire the exact
accepted software and permitted data, restore service outside the original
provider, verify the same contracts and recover without losing the required
audit/operational state. Signing remains under the authorised custody boundary.
Public distribution should survive loss of one serving operator. Managed
customer services must preserve their agreed availability and billing behavior
through the transition. Confidential M&A evidence must retain provenance,
access control, retention and deletion handling. A host migration cannot
substitute for an absent runtime API, durable write or hardware measurement.

No finite test guarantees every future outage or zero regressions. Record the
tested operation, source/artifact, environment, failure, recovery measurement
and remaining dependency. Claim only the result demonstrated by those records.

## Independently verify a public release

The exporter can now be checked through a separate operator-facing command. The
verifier does not trust `release.json`, an adjacent exported site, a warm local
Kubo cache, a branch label or a boolean claiming success. It requires a full
source SHA, an expected CID and an expected CAR SHA-256 obtained from the accepted
release record. The exact checkout's public sources must be tracked and clean.

```sh
python3 scripts/verify_public_ipfs_release.py /path/to/site.car \
  --source-sha "$ACCEPTED_SOURCE_SHA" \
  --expected-cid "$ACCEPTED_ROOT_CID" \
  --expected-car-sha256 "$ACCEPTED_CAR_SHA256" \
  --kubo /path/to/verified/ipfs
```

The command bounds and hashes the regular input file, copies it into a disposable
verification workspace, creates a fresh Kubo repository, imports offline, restores
the pinned CID and compares every file with the public allowlist built from the
pinned checkout. Wrong or incomplete pins, tampered archives, symlinks, missing
blocks and different public content fail. Errors are redacted and nonzero.

The successful receipt reports offline restoration only. It deliberately does
not authenticate operator independence, prove live replication or grant production
acceptance. Multiple receipts from one machine are not independent operators.
Use this command in the existing public conformance workflow and at each actual
operator handoff, retaining the exact source pin and independently obtained pins.

## Full-path capability sequence

| Capability | Implementation and verification | Completion evidence |
| --- | --- | --- |
| Public source and documentation | Allowlisted export plus independent offline verification, then separate live pins | Same CID/content restored and served by separately administered operators; rollback to the previous accepted CID |
| Stateless compute | Reuse the accepted OCI artifact with a decentralised compute adapter | Same contract tests on the chosen provider and its replacement, measured latency, cost and recovery; no sole registry/gateway dependency |
| Operational state | Portable schema/migrations, single-writer ownership and independent backup/restore | Actual write/read/restart/restore and idempotency evidence; derived protocol projections remain non-authoritative |
| Runtime contracts | Correct the owning implementation and prove authenticated positive/negative paths | Real handler and durable audit outcomes bound to source; truthful unavailable states until measured |
| Identity and signing | Qualified hardware/operator identities, release artifacts and revocation/replay controls | Real operation-specific collateral and independent acceptance; dashboards and hosting do not acquire keys |
| Engineering continuity | Controlled source, issue/PR/review and accepted artifact exports | Restore to another qualified operator without losing unique work or accepted evidence; GitHub remains authoritative until an approved cutover |
| M&A and commercial continuity | Separate public research from confidential deal records; use licensed real data | Provenance, authorised access/revocation, retention/deletion, reconciliation and customer/billing continuity under existing owners |

Prefer established decentralised systems where they pass the operation's actual
requirements. Keep Akash, IPFS, current Sia clients and the broader reuse research
as candidates. Provider topology, physical administration, shared upstreams,
token/payment exposure and recovery behavior must be observed rather than inferred
from branding. Record a grounded reason when a managed or self-operated component
remains the best qualified option.

This guide extends the [workspace allocation](DECENTRALISED_WORKSPACE_ALLOCATION_2026_10_24.md)
and [remediation map](DECENTRALISED_REUSE_REMEDIATION_2026_10_23.md). It does not
replace their issue ownership, create a second operating framework or close
unqualified work. Restricted remediation follows the owning security policy;
public coordination contains only sanitized progress.

## Validation

203 local Python tests pass with no skips using checksum-verified Kubo 0.43.1.
The independent verifier restores real CAR bytes and rejects altered archives,
wrong source/CID pins, incomplete pins and symlink input. A falsified adjacent
receipt and changed adjacent site do not affect the restored-source comparison.
Knowledge retention and doctrine checks pass. Local verification is separate
from hosted checks, genuine independent review and live operator qualification.
