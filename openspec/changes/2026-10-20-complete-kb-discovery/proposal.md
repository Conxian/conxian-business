# Complete source-pinned KB discovery

Parent: Business #1390. Supports the owner's org-wide recurring knowledge, issue,
gap, research and implementation triage. Existing repo enumeration already fails
closed and paginates; preserve it rather than add a second scanner.

## Problem and change
`bos_org_review.inspect` silently returns only the first 100 matching KB paths.
Remove that slice so downstream triage receives every discovered candidate.
Retain deterministic ordering, path-only output, source revision binding,
symlink exclusion, unreadable-file failures and existing classification rules.

## Acceptance
- A fixture with 125 matching files returns all 125, including the final path.
- Existing inventory, privacy and partial-scan regressions continue to pass.
- Discovery is not semantic review, deployment verification or release acceptance.
- Private KB paths/results retain their existing restricted publication boundary.

This does not broaden filename heuristics to claim every document was found,
publish private content, alter promotion policy or grant production approval.
