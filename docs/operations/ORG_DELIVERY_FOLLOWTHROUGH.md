# Organization delivery follow-through

Owner instruction: 21 October 2026. Engineering remains GitHub-only. This
operating procedure adds no merge exemption and changes no existing workflow,
validator, review, branch-protection, soak or release requirement.

## Managed cadence

- The hourly delivery operations task is a lightweight operational reconciliation,
  not a deep portfolio audit. It follows CI completion, incidents, ready merges,
  soak expiry, stale candidates, missed reviews, new repositories and task health.
- The Conxian PR delivery event task handles opened, ready-for-review, closed,
  commit-update and submitted-review events for the 13 currently accessible repos.
  PR comments are excluded to avoid a self-generated comment loop. These events
  do not cover arbitrary issue or CI-completion events.
- Weekly repo work runs in weekday groups around 09:00 Africa/Johannesburg,
  starting 22 October 2026. Each repository has one planned full weekly review
  and bounded implementation, with overdue work carried by delivery operations.
- Organization alignment runs every two weeks on Friday afternoon around 14:00
  Africa/Johannesburg, starting 23 October 2026. It reconciles the dependency and
  deployed graphs, risk/problem backlog, weekly coverage and improvement outcomes.

| Day | Weekly repository group |
|---|---|
| Monday | Enclave SDK, Core |
| Tuesday | Gateway, Nexus |
| Wednesday | Platform, Wallet, Market |
| Thursday | Labs Site, Org Site, conxian.github.io |
| Friday | Business, .github, .github-private |

Times are flexible scheduled windows, not a guaranteed job start. P0 response and
per-change delivery do not wait for a weekly or fortnightly review. The operating
mapping is `docs/ITIL_OPERATING_MODEL.md`: discover/design/acquire/build/transition/
operate/deliver/support. Each review records exact state, a bounded next action,
owner, gate and evidence under existing GitHub issues. Measured lead time, change
failure/rework, old PR/change age and deployed-state drift remain unknown unless
supported by actual observations. Limit implementation WIP to one coherent item
per repo and finish release follow-through before optional feature expansion.

The task plan permits five active tasks. Pricing research, the final whitepaper
and safe sprint-cleanup follow-ups are consolidated into delivery operations with
their original sprint-exit acceptance conditions. Their duplicate standalone
schedules are paused; their work is not canceled. Operations must not pause itself
when a consolidated child finishes. There are four active execution paths above.

At each run, read task health and the latest Business #1390 checkpoint. Detect a
paused delivery task while authorized work remains. Resume only under the current
owner authorization; a subsequent owner pause/cancellation overrides this rule.
Coordinate event and hourly work by refreshing heads before mutation, retaining
expected-head leases, and reading back results. Never retry a stale write blindly.

## Mandatory completion path

Inspect all open PRs, not only the newest implementation. Read the full diff,
paginated checks/statuses/reviews, current branch heads, applicable instructions
and release gates. Keep a per-repo record in existing owner issues containing the
exact source/target, next executable action, gate, owner and evidence link.

Accepted source must progress through dev, staged, real soak, main acceptance,
main integration and applicable package/deployment/live verification. A green PR,
dev merge, staged merge or empty PR queue is not completion. Close duplicates only
after replacement/retention proof. Preserve source/history until normal safe
cleanup requirements are satisfied. Independent acceptance cannot be synthesized.

## Deterministic audit

Run `python3 scripts/audit_org_delivery.py <snapshot.json>` using a fresh normalized
connector snapshot. Exit 0 means the supplied observations yielded no work actions,
1 means work actions remain, and 2 means invalid input. This is a read-only planner,
not a merge gate or proof that an external action was performed. Existing
`wait_for_checks`, promotion policy and independent release controls still apply.

The collector must supply `captured_at` with timezone, `inventory_complete`, the
full `expected_repositories`, `delivery_loop_enabled` and one `repositories` entry
per enumerated repo. Each entry includes `name`, `promotion_chain`, `prs_complete`,
`prs`, actual dev/staged/main `refs`, `trees`, independently checked `lineage`
(`staged_in_dev`, `main_in_staged`) and `soak_satisfied`. Services also supply
`deployment_required` and `deployment_source_sha`. Governance repositories can use
their existing main-direct reviewed route (`promotion_chain: false`).

Each PR supplies its actual number, head/base refs/SHAs, encoded `source_sha` and
`target_base_sha` if generated, full-diff and pagination completeness flags,
`checks` (head/status/conclusion), `statuses` (head/state), `reviews_complete`,
the separately evaluated `review_gate`, `protected_control_changes`, existing
`owner_issue` and concrete `next_action`. A separate workflow request is not implied
by general implementation approval. Main acceptance must be separately recorded
as `main_acceptance: accepted` bound to `acceptance_head_sha`; this planner never
creates that acceptance. Unknown or incomplete observations are not passing data.

Do not store credentials, provider secrets, raw private KB records or customer and
financial information in a public snapshot. Keep the detailed collection in its
authorized boundary and publish only sanitized action/evidence records.
