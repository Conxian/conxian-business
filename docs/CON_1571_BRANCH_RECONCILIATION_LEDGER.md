# CON-1571 Branch Reconciliation Disposition Ledger

**Recorded:** 2026-07-28
**Authority:** [GitHub Issues-1571](https://github.com/Conxian/conxian-business/issues?q=CON-1571), [GitHub issue #945](https://github.com/Conxian/conxian-business/issues/945), and draft [PR #971](https://github.com/Conxian/conxian-business/pull/971)

## Purpose and boundary

This public-safe ledger preserves the exact pre-reconciliation evidence and records how historical enhancement units may be considered without replaying divergent histories. It contains no restricted strategy content, credentials, private-submodule contents, or administrator-only repository settings.

The selected hierarchy remains:

- `main` is the GitHub default and production branch.
- `dev` is the non-production integration branch.
- `staged` is the candidate branch.

`main` and the historical `dev`/`staged` lineage have split roots, while the historical payload mixes workflows, dependencies, scripts, documents, workspaces, and gitlinks. Therefore no bulk merge, reset, rebase, history graft, wholesale cherry-pick, or broad pin restoration is permitted. Approved enhancements must return as bounded, current-tree changes with independent provenance and tests.

## Preserved source heads

The following annotated tags are preservation evidence only. They are not releases, promotion candidates, deployment instructions, or approval to restore their payloads. The tags and peeled commits were verified after a no-force push, but repository administration access is unavailable, so they are **not verified protected or immutable**.

| Source | Role at capture | Exact source commit | Archive tag | Tag object | Peeled commit |
|---|---|---|---|---|---|
| `main` | Default / production baseline | [`f6e7331c3e2eb6e35ed42e47b9e4c88aafbc7bc2`](https://github.com/Conxian/conxian-business/commit/f6e7331c3e2eb6e35ed42e47b9e4c88aafbc7bc2) | `archive/con-1571/main-f6e7331-2026-07-28` | `8858fe5044c305ab04de71aa2b2a6ca32f05f3cc` | `f6e7331c3e2eb6e35ed42e47b9e4c88aafbc7bc2` |
| `dev` | Historical integration head | [`2f4010b2ff2d172e69ef33d67da53187dd2e066a`](https://github.com/Conxian/conxian-business/commit/2f4010b2ff2d172e69ef33d67da53187dd2e066a) | `archive/con-1571/dev-2f4010b-2026-07-28` | `4e5520fc6ebff67fb6bf6264cd1778043c9b75e3` | `2f4010b2ff2d172e69ef33d67da53187dd2e066a` |
| `staged` | Historical candidate head | [`101b9b2556ab91a0c92f13ae680cfdd51d23fe27`](https://github.com/Conxian/conxian-business/commit/101b9b2556ab91a0c92f13ae680cfdd51d23fe27) | `archive/con-1571/staged-101b9b2-2026-07-28` | `d699916d1e024bfb0be7effa28bcbab41a8ca25b` | `101b9b2556ab91a0c92f13ae680cfdd51d23fe27` |
| [PR #939](https://github.com/Conxian/conxian-business/pull/939) boundary source | Clean-room candidate evidence | [`81d2ed670cf7b4c3f18d074ab7c94eab2f775028`](https://github.com/Conxian/conxian-business/commit/81d2ed670cf7b4c3f18d074ab7c94eab2f775028) | `archive/con-1571/pr939-boundary-source-81d2ed6` | `0f50a393ee215a09f4b4ce13777cdcc0c01d525b` | `81d2ed670cf7b4c3f18d074ab7c94eab2f775028` |

The exact PR #971 branch head before this ledger change was [`3d74b9b65caac0d9bf7be877f2563248a1273dab`](https://github.com/Conxian/conxian-business/commit/3d74b9b65caac0d9bf7be877f2563248a1273dab). The ledger commit extends that same draft branch and does not mutate a long-lived branch.

## Historical logical-unit disposition

This table classifies the mixed payload represented by historical `staged` commit `101b9b2` and its later `dev` lineage. A disposition is not approval to transplant code.

| Logical unit | Disposition | Re-adoption gate |
|---|---|---|
| Dependency and GitHub Action bumps | **Superseded; current-tree review only.** Historical version movement is not a safe update plan. | Re-resolve against current manifests, lockfiles, compatibility constraints, and pinned-action policy in a separate PR. |
| Promotion workflows | **Superseded by draft PR #971.** | Use the exact-route, trusted-code, finite-bootstrap design under review in PR #971; do not restore historical workflow files. |
| Generic/reusable CI framework | **Separate bounded audit if current callers require it.** | Inventory current callers, permissions, reusable-workflow inputs, pinned actions, and failure semantics before selecting individual units. |
| CI helpers and session/ecosystem scripts | **Archive only unless deliberately re-adopted with tests.** | Each script needs a current owner, current caller, focused tests, fail-closed behavior, and public-safe output. |
| Market integration and private-submodule wiring | **Human/product decision. Never synthesize missing private-submodule state.** | Confirm the product boundary and authorized private source, then test against real provenance or explicit public fixtures without fabricating a checkout. |
| Market fallback [`78702f104660900ccddd522cb45f44dc87f1cd95`](https://github.com/Conxian/conxian-business/commit/78702f104660900ccddd522cb45f44dc87f1cd95) / [PR #957](https://github.com/Conxian/conxian-business/pull/957) | **Explicitly rejected.** Do not restore its fallback behavior. | Fixtures may be used only if independently reimplemented under tests and clearly separated from claims about private-submodule state. |
| ZSE and repository-hygiene inventory | **Present or equivalent where independently verified; no wholesale `.gitmodules` restore.** | Compare each current control to the requirement and add only a missing, tested control without recovering historical gitlinks or restricted material. |
| Submodule pins | **Separate provenance-verified PRs only.** | Confirm upstream repository, exact commit provenance, owner approval, compatibility tests, contamination checks, and an explicit rollback pin. |
| Sandbox, Docker, and workspace material | **Separate developer-experience decision.** | Establish maintained scope, owners, isolation, secret handling, lockfile policy, and reproducible tests before any restoration. |
| Broad strategy and knowledge documents | **Archive or superseded.** | Any restoration requires a public-safe, current-fact review; do not copy sensitive strategy content from archived commits. |
| [PR #939](https://github.com/Conxian/conxian-business/pull/939) BOS production-boundary validator | **Approved candidate for a separate three-file clean-room restoration.** | Recreate only `scripts/verify_bos_production_boundary.py`, `tests/test_verify_bos_production_boundary.py`, and the focused `.github/workflows/conxian-unified-ci.yml` wiring against the current tree. Exclude all historical gitlinks and pins. |
| SDK integration commit [`6ddb69af0ce1cc38149bded1a9b332fa7db31724`](https://github.com/Conxian/conxian-business/commit/6ddb69af0ce1cc38149bded1a9b332fa7db31724) / [PR #953](https://github.com/Conxian/conxian-business/pull/953) | **Stale; do not restore verbatim.** | A current security owner must choose a provenance-verified pin and test plan; the historical CI expectation is not present-day approval. |

## SDK evidence and non-claim

The current root gitlink pins the SDK repository at older commit [`fb92680177e1fc6ad0a86cff2d5c3523efd3a5a2`](https://github.com/Conxian/conxius-enclave-sdk/commit/fb92680177e1fc6ad0a86cff2d5c3523efd3a5a2). Historical commit `6ddb69a` expected candidate [`3af2cb83988582073f726bebfffe21093a5e3b65`](https://github.com/Conxian/conxius-enclave-sdk/commit/3af2cb83988582073f726bebfffe21093a5e3b65), but the upstream default branch has advanced to [`4a5b01cb34cf544ed1f9b7371199fa9fd4ef5cfd`](https://github.com/Conxian/conxius-enclave-sdk/commit/4a5b01cb34cf544ed1f9b7371199fa9fd4ef5cfd). This is evidence of differing points in history, not a security, release, compatibility, or acceptance claim. A separate current security-owner pin and test decision is required.

## Rollout and abort criteria

### Rollout gates

1. Keep PR #971 draft and limited to governance controls, this ledger, and its knowledge-graph discovery link.
2. Review each candidate as a logical unit against the current `main` tree; use separate PRs for unrelated units.
3. Require exact provenance, focused tests, policy/static validation, secret/principal scans, and a rollback plan before accepting a restoration.
4. For submodules or private integrations, require authorized owner evidence; absence of private state must fail closed rather than be synthesized.
5. Restore the PR #939 validator candidate only as the stated three-file clean-room unit, with no historical gitlink changes.

### Abort conditions

Abort a restoration if it requires a bulk history operation, changes a long-lived branch outside the governed promotion path, imports unrelated files, revives stale pins without owner approval, synthesizes private state, exposes restricted material, weakens ZSE/fail-closed behavior, or fails current validation. Archive evidence remains available even when restoration is rejected.

## Typed BOS digest

| Entity | Type | Relationship / decision |
|---|---|---|
| CON-1571 | Governance authority | Governs the branch hierarchy and bounded reconciliation record; linked to GitHub issue #945 and draft PR #971. |
| `main` | Long-lived branch | Default and production baseline; preserved at `f6e7331c…` without changing the branch. |
| `dev` | Long-lived branch | Integration role; historical head preserved at `2f4010b…` without approving its mixed payload. |
| `staged` | Long-lived branch | Candidate role; historical head preserved at `101b9b2…` without approving its mixed payload. |
| Archive tags | Preservation evidence | Annotated, non-release references to exact commits; verified targets, but protection/immutability is not administrator-verified. |
| Historical enhancement units | Candidate evidence | Must be dispositioned and re-adopted independently; never replayed wholesale. |
| PR #939 boundary validator | Approved clean-room candidate | May proceed only as script, tests, and focused CI wiring in a separate PR; historical gitlinks are excluded. |
| SDK pin decision | Security-owner decision | Current root pin, historical candidate, and advanced upstream tip require a fresh provenance and compatibility review. |
| Market fallback `78702f1` | Rejected decision | Must not represent absent private state as verified; only independently designed fixtures may be considered. |
