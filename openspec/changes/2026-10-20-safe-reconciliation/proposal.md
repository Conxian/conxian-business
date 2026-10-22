# Stop automatic conflict-side selection during branch reconciliation

Tracking: Business1415/1390; concrete regression Gateway572.

Replace lane-wide ours/theirs conflict selection with ordinary conflict-free Git merges using --no-ff. Report unresolved paths and a nonzero overall reconciliation result; publish no branch or PR for a failed merge. Preserve existing candidates, create-only ref leases, ordinary reviewed backmerge routes and immutable promotion head binding.

Real Git tests must reject conflicting main-to-staged and staged-to-dev changes without modifying remote source/target or publishing a candidate; retain independent divergent changes and both real parents for successful merges. Existing preservation, race and source/target/head lineage checks remain mandatory.

Research and release-evidence remediation are recorded in docs/operations/RELEASE_REMEDIATION_2026_10_20.md. This is source automation hardening, not deployment, provider/hardware qualification, review approval or release acceptance. Active scheduled main automation changes only after normal integration and rollout.
