# Immutable promotion head binding — 15 October 2026

The eight repositories below carry copies of the Python branch-promotion policy. This proposed change requires generated candidate names, recorded source metadata, commit-window endpoints and the actual PR head to identify the same immutable revision. Absent, malformed or moved head evidence rejects the candidate.

The current feature-to-dev routes, downward reconciliation paths and repository-specific handling are preserved. The privileged enforcement workflow still checks out trusted default-branch code with read-only permissions. The new regression workflow runs unprivileged PR tests and has no secrets or write permissions.

Parent implementation tracker: [Business #1415](https://github.com/Conxian/conxian-business/issues/1415). This is a code-review checkpoint; it supplies no production, licensing, provider or independent acceptance decision.

## Tested proposals

| Repository / PR | Source commit | Local policy tests |
|---|---|---|
| [Conxian/conxian-business#1417](https://github.com/Conxian/conxian-business/pull/1417) | `f6d765a91223977aa3c56eac0291f3165406b230` | 40 |
| [Conxian/conxius-wallet#734](https://github.com/Conxian/conxius-wallet/pull/734) | `57beb303af9c04d0dc9f1fd6a9e32f7dfd10ac99` | 15 |
| [Conxian/conxian-gateway#532](https://github.com/Conxian/conxian-gateway/pull/532) | `a860138755d8f14d9c2cca753e92611a23bc6a1f` | 15 |
| [Conxian/lib-conxian-core#460](https://github.com/Conxian/lib-conxian-core/pull/460) | `ad1095cbf8b70d9905f118d56c26747c5ca2346a` | 15 |
| [Conxian/conxian-nexus#421](https://github.com/Conxian/conxian-nexus/pull/421) | `ece81c6f6c5430f48a1740c64a9b6e33fe1996b6` | 15 |
| [Conxian/conxius-enclave-sdk#577](https://github.com/Conxian/conxius-enclave-sdk/pull/577) | `2f26d6221d906fd24607b39024f7a5974e60aacf` | 15 |
| [Conxian/conxius-platform#1441](https://github.com/Conxian/conxius-platform/pull/1441) | `5d7965e61ad5b8d9efcf7e4a22080b3bc2dd8b5d` | 15 |
| [Conxian/conxian_market#177](https://github.com/Conxian/conxian_market/pull/177) | `fdf5b64b426eaf8d639515ce8d9f046cc408e8c2` | 15 |

All **145 local policy tests** pass. Each of the eight new hosted regression workflows passed at the source commit listed above. Coverage includes both promotion directions, stale source/base/window metadata, absent and malformed SHAs, moving heads, forked candidates, retained routes and event-file process exit codes. The Business copy also retains its existing route and workflow trust-boundary tests.

The original implementation trees are recorded below. Tree equality was checked when publishing each proposal. The later addition of this note changes the Business PR tree, while its policy code and regression-test blobs remain unchanged.

| Repository | Original tested implementation tree |
|---|---|
| Conxian/conxian-business | `4c6fe2827d0bfdc4daa4c02d69b0ea0d30927fd4` |
| Conxian/conxius-wallet | `b96f225bc7dd090dab13e110481c443ef1e58109` |
| Conxian/conxian-gateway | `4f7ed3ef1787283e0a1f445b4e05df15618a8b10` |
| Conxian/lib-conxian-core | `9ef6d76211c78508d3a5c944c0c51bf2024cd5cb` |
| Conxian/conxian-nexus | `d7763d2770436f7f0f286c69bc4ac6dbded64440` |
| Conxian/conxius-enclave-sdk | `29b30a2cf90085875d4ee06a1d0fac7586ef7c95` |
| Conxian/conxius-platform | `ea425b59899e19687a2d473f335c8ad21e31a6da` |
| Conxian/conxian_market | `07f601a97549587ac461aad0c4b8a694c185f3f6` |

## Review and rollout

1. Complete each repository's required checks and applicable owner review for its current exact head.
2. Merge through the normal feature-to-dev route.
3. Promote fresh immutable candidates through staged and then main with real acceptance evidence and merge-time head guards.
4. Verify the later live policy run uses the promoted default-branch implementation. A passing regression workflow on dev does not establish that deployment.

Broader hosted runtime checks remain distinct from these focused tests. No fresh local Rust, Android or browser suite is claimed for this Python-only change. No branch protection, required review, production evidence, runtime configuration or cryptographic implementation is weakened by the proposal.

## Queue reconciliation

SDK #574 was closed only after a fresh comparison proved its exact head `f7e995484648908d30cdc0443b9b929f7ce9e79f` is an ancestor of retained #576 at `4fdb3d46ee6c0b98a798b12b9cbc253268f028c1` (five commits ahead, zero behind). The original branch remains available; approvals do not transfer.

Wallet #725 produced a clean local three-way merge tree `8dd5afea08b729cbe9dd06ef0a9923f4fc26b9b3`; the later GitHub read also reports it mergeable. Its existing audit gate is separate from textual mergeability.
