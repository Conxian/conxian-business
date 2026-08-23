# CON-231: Pre-mainnet bounty claimability classification (2026-04-12)

This document is the classification artifact for https://sovereign.conxian.com/issue/CON-231/decide-which-bounties-can-open-before-mainnet-go-live.

## Decision

As of **2026-04-12**, **no current bounty items in the audited Conxian-Labs GitHub team and `Conxian/conxius-platform` registries should remain publicly claimable** before mainnet go-live.

Rationale (high level): the current bounty set is dominated by maintainer-only workflow/governance work, payout-gated enablement work, and release/CI hygiene items that require privileged repository access and are not safely reviewable as “open claims” during a mainnet cutover window.

## Source set audited (2026-04-12)

This classification is based on the two active “bounty registries” that are actually in use today:

1. GitHub team **Conxian-Labs** (`CON`) issues labeled `Bounty` / `Bounty Open`.
2. GitHub issues in `Conxian/conxius-platform` labeled `Bounty` / `Bounty Open` (synced to restricted vault/secure storage for the overlapping subset).

Replay queries used to derive the snapshot above:

```bash
# GitHub open bounty set
gh issue list -R Conxian/conxius-platform -l Bounty --state open --limit 1000

# GitHub open bounty set (Bounty Open)
gh issue list -R Conxian/conxius-platform -l 'Bounty Open' --state open --limit 1000

# GitHub bounty sets (Conxian-Labs team; all workflow states via no --state filter)
gh issue list -T CON -l Bounty --limit 1000
gh issue list -T CON -l 'Bounty Open' --limit 1000
```

If any query above ever returns as many rows as its `--limit` value, increase that `--limit` to keep the snapshot complete.

These queries were run on 2026-04-12 to produce this point-in-time snapshot. Future runs of the same commands may return a different set of issues; any new or relabeled `Bounty` / `Bounty Open` items must be explicitly reclassified before being treated as externally claimable.

Additional GitHub bounty items labeled `Bounty` (but not `Bounty Open`) and not present in the active GitHub open set as of 2026-04-12:

- https://github.com/Conxian/conxian-business/issues?q=CON-142
- https://github.com/Conxian/conxian-business/issues?q=CON-230

### Active GitHub bounty set (open, as of 2026-04-12)

From `Conxian/conxius-platform` open issues labeled `Bounty`:

- https://github.com/Conxian/conxius-platform/issues/210 → https://github.com/Conxian/conxian-business/issues?q=CON-231
- https://github.com/Conxian/conxius-platform/issues/197 → https://github.com/Conxian/conxian-business/issues?q=CON-222_orbit
- https://github.com/Conxian/conxius-platform/issues/170 → https://github.com/Conxian/conxian-business/issues?q=CON-198
- https://github.com/Conxian/conxius-platform/issues/159 → https://github.com/Conxian/conxian-business/issues?q=CON-186
- https://github.com/Conxian/conxius-platform/issues/152 → https://github.com/Conxian/conxian-business/issues?q=CON-178
- https://github.com/Conxian/conxius-platform/issues/153 → https://github.com/Conxian/conxian-business/issues?q=CON-182
- https://github.com/Conxian/conxius-platform/issues/139 → https://github.com/Conxian/conxian-business/issues?q=CON-167
- https://github.com/Conxian/conxius-platform/issues/102 → https://github.com/Conxian/conxian-business/issues?q=CON-131
- https://github.com/Conxian/conxius-platform/issues/101 → https://github.com/Conxian/conxian-business/issues?q=CON-129

For audit and enforcement purposes, each GitHub issue inherits the same classification as its mapped GitHub `CON-` issue in the **Classification** section below.

Derived GitHub classifications (snapshot 2026-04-12):

```txt
#210 → Internal-only (CON-231)
#197 → Security-sensitive (CON-222)
#170 → Security-sensitive (CON-198)
#159 → Security-sensitive (CON-186)
#152 → Security-sensitive (CON-178)
#153 → Security-sensitive (CON-182)
#139 → Payout-gated (CON-167)
#102 → Internal-only (CON-131)
#101 → Security-sensitive (CON-129)
```

### Snapshot: GitHub issues labeled `Bounty Open` (as of 2026-04-12)

These are expected to have `Bounty Open` removed for the pre-mainnet window per this classification.

- https://github.com/Conxian/conxian-business/issues?q=CON-178
- https://github.com/Conxian/conxian-business/issues?q=CON-182
- https://github.com/Conxian/conxian-business/issues?q=CON-186
- https://github.com/Conxian/conxian-business/issues?q=CON-198
- https://github.com/Conxian/conxian-business/issues?q=CON-218
- https://github.com/Conxian/conxian-business/issues?q=CON-222_orbit
- https://github.com/Conxian/conxian-business/issues?q=CON-78

As of 2026-04-12, the lists above represent the full set of active `Bounty` / `Bounty Open` items that were included in this classification (limited to the Conxian-Labs GitHub team and the `Conxian/conxius-platform` GitHub repository).

Coverage check (as of 2026-04-12): 13 unique `CON-` issues classified (2 internal-only, 7 security-sensitive, 2 payout-gated, 2 claimable later). GitHub mirrors are not counted separately.

### Classification table (canonical)

_The `Bounty Open` column shows the label state at snapshot time, not the recommended state after applying this classification._

| Issue | Category | `Bounty Open` on GitHub (snapshot before applying this classification, 2026-04-12) |
|---|---|---|
| https://github.com/Conxian/conxian-business/issues?q=CON-231 | Internal-only | No |
| https://github.com/Conxian/conxian-business/issues?q=CON-131 | Internal-only | No |
| https://github.com/Conxian/conxian-business/issues?q=CON-178 | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-182 | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-186 | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-198 | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-218 | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-222_orbit | Security-sensitive | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-129 | Security-sensitive | No |
| https://github.com/Conxian/conxian-business/issues?q=CON-167 | Payout-gated | No |
| https://github.com/Conxian/conxian-business/issues?q=CON-230 | Payout-gated | No |
| https://github.com/Conxian/conxian-business/issues?q=CON-78 | Claimable later | Yes |
| https://github.com/Conxian/conxian-business/issues?q=CON-142 | Claimable later | No |

## Classification

Everything below other than **Externally claimable (pre-mainnet)** is treated as **non-public / maintainer-gated work** for the pre-mainnet window. `Security-sensitive` and `Payout-gated` are subtypes of internal work that must not be treated as publicly claimable.

### Externally claimable (pre-mainnet)

None.

### Internal-only (meta/process work)

- https://github.com/Conxian/conxian-business/issues?q=CON-231 (meta classification)
- https://github.com/Conxian/conxian-business/issues?q=CON-131 (workflow enforcement + label automation)

Note: the issue referenced in older threads as `CON-135` is not retrievable via the GitHub API as of 2026-04-12 (it may have been deleted or renumbered). If it reappears, it should remain internal-only unless it is split into tightly scoped, reviewable sub-tasks.

For readers comparing against earlier discussion on CON-231: `CON-129` and `CON-167` were previously lumped into `internal-only` but are refined here into `Security-sensitive` and `Payout-gated` respectively. This does not change their pre-mainnet status (both remain non-public / maintainer-gated) but makes the risk and dependency structure more explicit.

### Security-sensitive (hold until after mainnet + maintainer review gates)

These items touch release discipline, required checks, tags, and/or `.github`-propagated standards. Even when the concrete work is “just docs,” the operational blast radius (and common requirement for maintainer privileges) makes them unsafe to treat as publicly claimable before mainnet.

- https://github.com/Conxian/conxian-business/issues?q=CON-178 (org-wide checks + CI blast radius)
- https://github.com/Conxian/conxian-business/issues?q=CON-182 (core repo release gating)
- https://github.com/Conxian/conxian-business/issues?q=CON-186 (release/CI discipline)
- https://github.com/Conxian/conxian-business/issues?q=CON-198 (deploy hygiene)
- https://github.com/Conxian/conxian-business/issues?q=CON-218 (core library release gating)
- https://github.com/Conxian/conxian-business/issues?q=CON-222_orbit (release discipline)
- https://github.com/Conxian/conxian-business/issues?q=CON-129 (launch readiness gate)

### Payout-gated (blocked on verified mainnet + funding path + maintainer controls)

- https://github.com/Conxian/conxian-business/issues?q=CON-167 (payout enablement runbook)
- https://github.com/Conxian/conxian-business/issues?q=CON-230 (funding + payout activation)

### Claimable later (post-go-live, after being split into verifiable units)

- https://github.com/Conxian/conxian-business/issues?q=CON-78 (too broad for pre-mainnet verification)
- https://github.com/Conxian/conxian-business/issues?q=CON-142 (readiness artifact, not open claims)

## Workflow hygiene recommendations

To make the repo and GitHub states accurately reflect the classification above:

1. For any issue in the audited Conxian-Labs GitHub team or `Conxian/conxius-platform` repo, remove `Bounty Open` from anything that is **not** in **Externally claimable (pre-mainnet)** (i.e., anything classified as internal-only, security-sensitive, payout-gated, or claimable later).
2. For any issue with existing “claims”, only treat a claim as payout-eligible if it links to a concrete implementation artifact (PR, commit, or equivalent). Claims without such evidence should be treated as invalid for payout/approval.
3. Only use `Bounty Open` when:
   - the issue is in `Todo` (claimable),
   - it is unassigned,
   - it has explicit acceptance criteria that can be validated via a PR/commit artifact.
4. For https://github.com/Conxian/conxian-business/issues?q=CON-231 specifically, all currently visible claims are considered invalid for approval as of 2026-04-12 because they lack linked implementation artifacts.
5. Before adding or keeping `Bounty Open` on any GitHub issue, ensure it is linked to a `CON-` issue that is explicitly covered by this document (or a clearly linked successor classification artifact) and inherits its classification. Unmapped GitHub bounty issues must not be treated as externally claimable.

Given there are no **Externally claimable (pre-mainnet)** items as of 2026-04-12, all audited issues should end up without the `Bounty Open` label until after mainnet go-live.

## Appendix: snapshot data (2026-04-12)

GitHub (`Conxian/conxius-platform`) open issues labeled `Bounty`:

```txt
#210 Decide which bounties can open before mainnet go-live [Governance, Bounty]
#197 Release hygiene — conxius-orbit [Release, Bounty, Bounty Open]
#170 Release hygiene — conxian-labs-site [Release, Bounty, Bounty Open]
#159 Release hygiene — Conxian_UI [Release, Bounty, Bounty Open]
#152 Release hygiene — .github [Release, Bounty, Bounty Open]
#153 Release hygiene — Conxian [Release, Bounty, Bounty Open]
#139 Maintainer payout enablement checklist for ALEX-funded bounties [Bounty]
#102 Adopt stricter bounty workflow for Conxian-Labs [Bounty]
#101 CSF mainnet readiness gate [Release, Bounty]
```

GitHub (`Conxian/conxius-platform`) open issues labeled `Bounty Open`:

```txt
#197 Release hygiene — conxius-orbit [Release, Bounty, Bounty Open]
#170 Release hygiene — conxian-labs-site [Release, Bounty, Bounty Open]
#159 Release hygiene — Conxian_UI [Release, Bounty, Bounty Open]
#152 Release hygiene — .github [Release, Bounty, Bounty Open]
#153 Release hygiene — Conxian [Release, Bounty, Bounty Open]
```

GitHub (team `CON`) issues labeled `Bounty Open`:

```txt
CON-178 Release hygiene — .github [Release, Bounty, Bounty Open]
CON-182 Release hygiene — Conxian [Release, Bounty, Bounty Open]
CON-186 Release hygiene — Conxian_UI [Release, Bounty, Bounty Open]
CON-198 Release hygiene — conxian-labs-site [Release, Bounty, Bounty Open]
CON-218 Release hygiene — lib-conxian-core [Release, Bounty, Bounty Open]
CON-222 Release hygiene — conxius-orbit [Release, Bounty, Bounty Open]
CON-78 CON-75: [BOUNTY] Gateway Edge - Offline-First POS Sync [Bounty, Bounty Open]
```

GitHub (team `CON`) additional issues labeled `Bounty` (but not `Bounty Open`) in this snapshot:

```txt
CON-142 Mainnet readiness checklist — conxius-platform [Release, Bounty]
CON-230 Confirm bounty funding and payout activation for mainnet [Bounty, Release]
```
