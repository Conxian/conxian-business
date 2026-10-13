# Open pull-request regression review — 2026-10-13

## Scope and method

This review covers every open pull request returned for `involves:admin-conxian-labs org:Conxian` through the connected GitHub account on 2026-10-13: 23 pull requests across seven repositories. The review compares each PR's base/head, mergeability, changed-file count, and current check runs. It also inspects the substantive diffs and failing job logs where a red check is not solely a promotion-policy gate.

This is a point-in-time evidence record. A green dependency or branch-policy check does not prove runtime correctness. Promotion evidence remains incomplete until the exact candidate has passed its repository gates and the required deployment/test evidence is linked.

## Non-regression rules

1. Preserve the newest verified candidate in a promotion chain; older candidates do not regain authority because they remain open.
2. Do not complete acceptance checklists with inferred or historical evidence.
3. Keep production promotions as drafts while any evidence field is a placeholder.
4. Do not merge no-op, non-mergeable, duplicate, or superseded candidates.
5. Documentation-only changes must not claim that a control is technically enforced.
6. Structural proof validation, mutable in-memory state, and synthetic identifiers are not production verification, durable audit, or execution evidence.

## Review matrix

| PR | Observed state | Regression assessment | Required disposition |
|---|---|---|---|
| `conxian_market#166` | Main promotion; mergeable; zero changed files; promotion policy failed | No-op candidate with empty acceptance pack | Close as stale; generate a new candidate only from a later evidence-complete staged SHA |
| `conxian-gateway#520` | Main promotion; non-mergeable; 59 files; promotion policy failed | Broad candidate includes managed tenancy and ISO work, but its acceptance pack is placeholder text | Keep blocked/draft; resolve branch drift, vulnerable dependency evidence, deployed Gateway verification, and exact-candidate acceptance before regenerating |
| `conxian-org-site#12` | Draft; mergeable; 8 files; all reported checks green | Reproducible Render/Vercel build fix; Docker engine and live redeploy remain unverified | Keep draft until container build and preview/live provider checks pass |
| `conxian-business#1370` | Draft; mergeable; 18 files; promotion policy failed | Correctly fails closed when runtime configuration is absent; deployed runtime contract still missing | Keep draft; add the feature-to-dev checklist and preserve the Nexus/provider deployment gates |
| `conxian-nexus#413` | Ready; mergeable; 8 files; promotion policy failed | Critical: accepts arbitrary 32-byte blobs as verified zkVM proofs; hardcodes ISO payment data; accepts missing API keys; places Gateway code in Nexus | Replace with a fail-closed zkVM provider boundary, remove ISO from Nexus, correct claims, keep draft until real verifier fixtures exist |
| `conxius-enclave-sdk#544` | Ready; mergeable; 5 files; promotion policy failed | Duplicate feature line. Value cap silently skips enforcement when context length is not 8; code calls software memory policy “hardware-enforced”; watchtower “trigger” only mutates a map | Request changes; do not merge. Replace untyped context parsing with a versioned policy object and retain unsupported execution until a real broadcaster exists |
| `conxius-wallet#720` | Staged promotion; mergeable; policy failed | Superseded by `#722` | Close as superseded |
| `conxius-wallet#722` | Newest staged promotion; mergeable; policy failed twice | Current candidate in this chain, but checklist is incomplete and exact candidate evidence is absent | Keep only as draft; validate the full wallet/signer/treasury and deployment boundary before promotion |
| `conxius-wallet#716` | Staged promotion; mergeable; policy failed twice | Superseded by `#720` and `#722` | Close as superseded |
| `conxius-wallet#715` | Staged promotion; mergeable; policy failed twice | Superseded by later candidates | Close as superseded |
| `conxian-gateway#519` | Back-merge; mergeable; dependency review failed | GitHub dependency review reports vulnerable packages | Block until the exact vulnerable dependency change is identified and remediated; then re-run reconciliation |
| `conxian-business#1364` | Targets `main`; mergeable; promotion policy failed twice | Bypasses dev→staged→main and describes documentation as enforcement | Retarget/recreate against `dev`, narrow enforcement claims, and add required checklist evidence |
| `conxius-enclave-sdk#545` | Targets `dev`; mergeable; promotion policy failed twice | Policy documentation is useful, but text overstates that documentation “enforces” secret isolation | Keep blocked until wording is evidence-scoped and the feature-to-dev checklist is complete |
| `conxius-enclave-sdk#543` | Ready; mergeable; 4 files; promotion policy failed | Older duplicate of `#544` with the same fail-open value-cap behavior | Close as duplicate after preserving any unique review evidence |
| `conxian-business#1363` | Staged promotion; non-mergeable; policy failed | Stale/non-mergeable candidate | Close and regenerate only after current dev is validated |
| `conxius-wallet#712` | Staged promotion; mergeable; policy failed twice | Superseded by later wallet candidates | Close as superseded |
| `conxius-wallet#713` | Staged promotion; mergeable; policy failed twice | Superseded by later wallet candidates | Close as superseded |
| `conxius-wallet#702` | Dependency PR; mergeable; unit tests failed | Action SHA changed but policy tests still pin the previous upload-artifact SHA; 3 tests fail | Update the policy fixtures in the same PR and re-run; do not bypass the tests |
| `conxius-wallet#704` | Dependency PR; mergeable; unit tests failed | Action SHA changed but policy tests still pin the previous download-artifact SHA; 4 tests fail | Update policy fixtures and re-run; do not bypass the tests |
| `conxius-enclave-sdk#542` | Main promotion; non-mergeable; policy failed | Old candidate predates open dev work and has incomplete mainnet evidence | Keep draft or close; regenerate from staged after SDK fixes and external hardware evidence gates |
| `conxian-gateway#517` | Staged promotion; mergeable; zero changed files; policy failed | Stale no-op candidate | Close as stale |
| `conxian-gateway#516` | Staged promotion; mergeable; zero changed files; policy failed | Stale no-op candidate | Close as stale |
| `conxius-wallet#691` | Dependency PR; mergeable; dependency audit failed | Audit ledger contains a stale `GHSA-ch52-4w7c-c8xp` exception while the current audit still reports one high-severity vulnerability | Remove only the stale exception, identify the remaining advisory, and keep blocked until the current report is clean or a reviewed live exception exists |

## Cross-PR ordering

The following work must land before any production promotion containing it:

1. Repair Nexus `#413`; do not expose a zkVM endpoint until an actual SP1/RISC Zero backend validates upstream-generated fixtures.
2. Fix Gateway ISO normalization so it extracts message values rather than emitting `ISO-SIM-123`, fixed USD 50.00, and simulated parties.
3. Resolve or supersede Enclave `#543/#544`; neither implements hardware-enforced limits or watchtower transaction execution as titled.
4. Complete the business control-plane runtime contract and deploy it to a verified long-lived runtime before setting `CONXIAN_ADMIN_RUNTIME_BASE_URL` in Vercel.
5. Regenerate promotion PRs from the resulting verified `dev`/`staged` heads instead of promoting current stale candidates.

## Provider impact

No open PR currently supplies end-to-end evidence for the reported control-plane flow. Vercel configuration alone cannot repair it: the configured base URL must resolve to an authenticated runtime that implements the canonical read routes and durable mutation/audit behavior. Cloudflare DNS should remain DNS-only until the target services and health contracts are verified. The current Render inventory does not contain a deployable Nexus/Gateway runtime satisfying those contracts.
