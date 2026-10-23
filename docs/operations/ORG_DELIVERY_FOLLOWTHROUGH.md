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
when a consolidated child finishes. There are five active execution paths including the standards research below.

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

The actual PR head and base must be full lowercase commit SHAs, and the observed
base must match the current target ref. Refresh moving or missing identity before
acting. An immutable promotion name must parse completely and its encoded lane
must match the actual target branch; a malformed `promotion/` name is never
ordinary feature work. `checks` and `statuses` must both be explicit arrays of
objects, even when their completeness flags are true. An observed empty status
collection is `statuses: []`; an omitted collection is missing evidence. Malformed
PR entries produce an incomplete-read action while other valid PRs remain in the
plan. Coverage completeness describes the supplied reads, not release approval.

Do not store credentials, provider secrets, raw private KB records or customer and
financial information in a public snapshot. Keep the detailed collection in its
authorized boundary and publish only sanitized action/evidence records.

### Exact dependency and deployment preflight

Immutable promotion candidates additionally supply `dependency_validation` bound
to their actual `head_sha`. Where the promotion diff changes dependency inputs,
record `dependency_files_changed: true`, `frozen_or_locked: true`, `result: success`
and an `evidence_ref` to the actual source-bound frozen install or locked resolver
check. Pending, skipped, failed, absent and previous-head results request
`COLLECT_EXACT_DEPENDENCY_VALIDATION`. A documentation-only diff may instead use
`dependency_files_changed: false`, `result: not_applicable` and a nonempty
`rationale` derived from the complete diff. This is a separate observation, not an
inference from a green summary. Use the repository's pinned package manager; never
rewrite a lockfile automatically to make a promotion pass.

For every `deployment_required` repository, a matching commit alone is insufficient.
Supply `deployments_complete: true`, `deployment_targets` from the intended release
manifest and `deployment_observations` from provider reads. Each target has
`provider`, `scope`, `service`, `environment`, `source_sha` (current main) and an
immutable lowercase `sha256:` plus 64-hex-character `artifact_digest`. Observations
have those same fields plus `deployment_id`, `state: live` and timezone-qualified
`observed_at`. The collector normalizes provider terminal-success states to `live`
only when actually observed. All intended targets must appear exactly once; unknown,
duplicate, missing, extra or substituted targets fail. Observations older than one
hour or in the future, wrong source/digest and non-live states request
`VERIFY_DEPLOYMENT_ARTIFACT_BINDING`. Metadata unavailable from a provider stays
unknown; do not hash a commit string or invent an artifact digest as a substitute.

The planner compares supplied observations; it does not authenticate the collector,
verify signed provenance, measure a live user journey or confer release authority.
Keep intended manifests and raw observations restricted. The output includes only
repository/action identifiers, not provider account/service/deploy IDs or digests.
Existing snapshots remain readable but receive follow-up actions when new evidence
is absent. Existing check, review, soak and main acceptance requirements are unchanged.

## Institutional standards research

The fifth active task runs Thursdays around 14:00 SAST, starting 22 October 2026.
Inventory standards actually used, claimed and planned across current code and
compare them with the current official FINOS landscape. Keep specifications,
reference implementations, controls and frameworks distinct. Verify release
maturity, licences/IP, provenance, compatibility and conformance tooling. Prefer
maintained compatible components and thin tested adapters; justify new code where
there is a real unmet requirement. The full source-dated compatibility register
and work items live under Business #1423/#1424/#1390 and the canonical KB.
Recommendations are not adopted policy, certification or production acceptance.
Accepted findings feed weekly repo implementation and fortnightly alignment.
