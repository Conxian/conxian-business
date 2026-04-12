# CON-231: Pre-mainnet bounty claimability classification (2026-04-12)

This document is the classification artifact for https://linear.app/conxian-labs/issue/CON-231/decide-which-bounties-can-open-before-mainnet-go-live.

## Decision

As of **2026-04-12**, **no current Conxian-Labs bounty items should remain publicly claimable** before mainnet go-live.

Rationale (high level): the current bounty set is dominated by maintainer-only workflow/governance work, payout-gated enablement work, and release/CI hygiene items that require privileged repository access and are not safely reviewable as “open claims” during a mainnet cutover window.

## Source set audited (2026-04-12)

This classification is based on the two active “bounty registries” that are actually in use today:

1. Linear team **Conxian-Labs** (`CON`) issues labeled `Bounty` / `Bounty Open`.
2. GitHub issues in `Conxian/conxius-platform` labeled `Bounty` / `Bounty Open` (synced to Linear for the overlapping subset).

Additional Linear bounty items (not present in the active GitHub open set, but still labeled `Bounty` as of 2026-04-12):

- https://linear.app/conxian-labs/issue/CON-142/mainnet-readiness-checklist-conxius-platform
- https://linear.app/conxian-labs/issue/CON-230/confirm-bounty-funding-and-payout-activation-for-mainnet

### Active GitHub bounty set (open, as of 2026-04-12)

From `Conxian/conxius-platform` open issues labeled `Bounty`:

- https://github.com/Conxian/conxius-platform/issues/210 → https://linear.app/conxian-labs/issue/CON-231/decide-which-bounties-can-open-before-mainnet-go-live
- https://github.com/Conxian/conxius-platform/issues/197 → https://linear.app/conxian-labs/issue/CON-222/release-hygiene-stacksorbit
- https://github.com/Conxian/conxius-platform/issues/170 → https://linear.app/conxian-labs/issue/CON-198/release-hygiene-conxian-labs-site
- https://github.com/Conxian/conxius-platform/issues/159 → https://linear.app/conxian-labs/issue/CON-186/release-hygiene-conxian-ui
- https://github.com/Conxian/conxius-platform/issues/152 → https://linear.app/conxian-labs/issue/CON-178/release-hygiene-github
- https://github.com/Conxian/conxius-platform/issues/153 → https://linear.app/conxian-labs/issue/CON-182/release-hygiene-conxian
- https://github.com/Conxian/conxius-platform/issues/139 → https://linear.app/conxian-labs/issue/CON-167/maintainer-payout-enablement-checklist-for-alex-funded-bounties
- https://github.com/Conxian/conxius-platform/issues/102 → https://linear.app/conxian-labs/issue/CON-131/adopt-stricter-bounty-workflow-for-conxian-labs
- https://github.com/Conxian/conxius-platform/issues/101 → https://linear.app/conxian-labs/issue/CON-129/csf-mainnet-readiness-gate

### Active Linear “public claimable” set (`Bounty Open`, as of 2026-04-12)

- https://linear.app/conxian-labs/issue/CON-178/release-hygiene-github
- https://linear.app/conxian-labs/issue/CON-182/release-hygiene-conxian
- https://linear.app/conxian-labs/issue/CON-186/release-hygiene-conxian-ui
- https://linear.app/conxian-labs/issue/CON-198/release-hygiene-conxian-labs-site
- https://linear.app/conxian-labs/issue/CON-218/release-hygiene-lib-conxian-core
- https://linear.app/conxian-labs/issue/CON-222/release-hygiene-stacksorbit
- https://linear.app/conxian-labs/issue/CON-78/con-75-bounty-gateway-edge-offline-first-pos-sync

## Classification

Everything below other than **Externally claimable (pre-mainnet)** is treated as **non-public / maintainer-gated work** for the pre-mainnet window. `Security-sensitive` and `Payout-gated` are subtypes of internal work that must not be treated as publicly claimable.

### Externally claimable (pre-mainnet)

None.

### Internal-only (maintainer-controlled)

- https://linear.app/conxian-labs/issue/CON-231/decide-which-bounties-can-open-before-mainnet-go-live (meta classification)
- https://linear.app/conxian-labs/issue/CON-131/adopt-stricter-bounty-workflow-for-conxian-labs (workflow enforcement)

Note: the issue referenced in older threads as `CON-135` is not retrievable via the Linear API as of 2026-04-12 (it may have been deleted or renumbered). If it reappears, it should remain internal-only unless it is split into tightly scoped, reviewable sub-tasks.

### Security-sensitive (hold until after mainnet + maintainer review gates)

These items touch release discipline, required checks, tags, and/or `.github`-propagated standards. Even when the concrete work is “just docs,” the operational blast radius (and common requirement for maintainer privileges) makes them unsafe to treat as publicly claimable before mainnet.

- https://linear.app/conxian-labs/issue/CON-178/release-hygiene-github
- https://linear.app/conxian-labs/issue/CON-182/release-hygiene-conxian
- https://linear.app/conxian-labs/issue/CON-186/release-hygiene-conxian-ui
- https://linear.app/conxian-labs/issue/CON-198/release-hygiene-conxian-labs-site
- https://linear.app/conxian-labs/issue/CON-218/release-hygiene-lib-conxian-core
- https://linear.app/conxian-labs/issue/CON-222/release-hygiene-stacksorbit
- https://linear.app/conxian-labs/issue/CON-129/csf-mainnet-readiness-gate

### Payout-gated (blocked on verified mainnet + funding path + maintainer controls)

- https://linear.app/conxian-labs/issue/CON-167/maintainer-payout-enablement-checklist-for-alex-funded-bounties
- https://linear.app/conxian-labs/issue/CON-230/confirm-bounty-funding-and-payout-activation-for-mainnet

### Claimable later (post-go-live, after being split into verifiable units)

- https://linear.app/conxian-labs/issue/CON-78/con-75-bounty-gateway-edge-offline-first-pos-sync
- https://linear.app/conxian-labs/issue/CON-142/mainnet-readiness-checklist-conxius-platform

## Workflow hygiene recommendations

To make the repo and Linear states accurately reflect the classification above:

1. Remove `Bounty Open` from any issue that is **not** in **Externally claimable (pre-mainnet)** (i.e., anything classified as internal-only, security-sensitive, payout-gated, or claimable later).
2. Only use `Bounty Open` when:
   - the issue is in `Todo` (claimable),
   - it is unassigned,
   - it has explicit acceptance criteria that can be validated via a PR/commit artifact.
