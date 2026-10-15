# Consolidate and validate the parent Rust dependency lock

Parent workload: #1390. Existing candidates: #1402 (Redis), #1403 (thiserror), #1404 (jsonwebtoken).

These candidates update only the parent Cargo.lock. Combine their requested compatible versions in #1402 and patch the parent TLS/QUIC resolution, preserving all current submodule pins, manifests, signing policy and workflow checks. Updating child lockfiles alone does not update this parent workspace's resolution.

Acceptance: regenerate the lock using the pinned submodule sources; demonstrate Redis 1.7.1, thiserror 2.0.21 and jsonwebtoken 11.1.0 together with patched rustls/quinn-proto; run locked workspace checks/tests and applicable governance checks. No blanket advisory exception, release promotion, submodule update or production enablement is authorized by this change. Keep #1403/#1404 open until the combined candidate is validated and accepted.
