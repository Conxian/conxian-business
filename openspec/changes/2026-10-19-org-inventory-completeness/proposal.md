# Fail closed on incomplete organization source inventory

Owners: Business #1390/#1423 and Conxian/.github#43. Phase R0/R1.

The organization scanner previously capped repository discovery at 100 and silently substituted submodules on authenticated enumeration failure. Clone failures still returned success, heuristic source scans were labelled reviewed, and no source revision was recorded. This cannot establish the coverage needed to triage source, research PRs and runtime gaps separately.

Use authenticated, fully paginated visible organization repositories; reject missing, malformed, duplicate and cross-organization metadata. Do not use dependency submodules as an organization inventory. Record immutable checkout revisions and return failure for unavailable or unreadable source, without disclosing provider errors. Label the scope as default-branch source heuristics, never runtime health, an exhaustive security audit, all-identity visibility or independent acceptance. Keep generated reports restricted for disclosure review. Add mocked conformance CI on dev/staged/main without granting organization credentials.

Acceptance: over-100 multi-page enumeration, authentication/late-page/clone/read failures, disabled repositories, untrusted clone URLs, missing source identity, symlink exclusion and redacted error paths are exercised. Preserve the separate live GitHub issue/PR inventory and per-repo acceptance gates. No CRM/customer operation, backend connection, pricing, cryptographic verifier or promotion policy is changed.
