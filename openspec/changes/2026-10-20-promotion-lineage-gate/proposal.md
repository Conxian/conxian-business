# Promotion lineage and stale-event gate

## Problem
Queued push events create immutable promotion candidates even after the source branch advances. A shared merge base alone also permits a candidate that omits target history, including a reconciliation whose tree was retained by squash while its target parent was lost. This causes redundant candidates and repeated conflicted promotions.

## Selected change
Before any candidate ref/PR publication, compare the checked-out source SHA with the freshly fetched source branch. Skip obsolete events. Require the target SHA to be an ancestor of the exact source. Refuse diverged or squash-flattened histories with an actionable reconciliation message. Do not rewrite immutable candidates, auto-close older PRs, self-approve reviews or infer acceptance from CI.

## Acceptance
Execute the actual workflow capture shell against real temporary Git repositories: current linear source succeeds; an outdated push skips before publication; a shared-base divergent source and a squash with the correct target tree but no target ancestry both reject; a real merge preserving the target parent succeeds; unknown source/target fetch errors fail. Existing preservation and promotion policy tests must remain green.

## Remaining work
Existing Business lineage repair still requires a reviewed merge commit retaining the staged parent, integrated validation and normal promotion evidence. Use an explicit merge method and exact-head guard when eligible; do not use repository-default squash/auto-merge for ancestry-bearing reconciliation. This generator fix does not repair refs or qualify deployment. No current candidate or source branch is deleted.

## Hosted validation follow-up
The full workspace check builds the upgraded container but its anonymous sign-in HTTP smoke returns 500. Its failure handler discards container stderr, hiding the application cause. Retain a bounded final 100 lines from both container streams for this isolated synthetic CI container; retain the failing HTTP assertion. This diagnostic adjustment grants no runtime access and does not claim that the startup failure is fixed.
