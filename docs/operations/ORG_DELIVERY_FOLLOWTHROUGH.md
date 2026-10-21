# Organization delivery follow-through

Owner instruction: 21 October 2026. Engineering remains GitHub-only. This
operating procedure adds no merge exemption and changes no existing workflow,
validator, review, branch-protection, soak or release requirement.

## Two execution paths

- The owner-authorized hourly Conxian org delivery task reconciles every accessible
  repository, PR, issue, KB and deployed/source state. It covers CI completion,
  issue changes, soak expiry and new repositories.
- The Conxian PR delivery event task handles opened, ready-for-review, closed,
  commit-update and submitted-review events for the 13 currently accessible repos.
  PR comments are excluded to avoid a self-generated comment loop. These events
  do not cover arbitrary issue or CI-completion events.

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
