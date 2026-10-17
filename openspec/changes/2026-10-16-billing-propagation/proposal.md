# Source-pinned billing propagation evidence

Refs Business #1343 and #1390. The shared Core configuration and consumer
changes need a reproducible coordination record that does not conflate them
with payment-backed entitlement, measured revenue or release acceptance.

Add a dated source record, an offline committed-source checker, failure tests
and path-scoped read-only CI. Require immutable commits, correct origins and
matching Core/SDK sources, a catalog digest, distinct accounting units and
shared definitions. Record the actual feature graph: SDK is opt-in in Core,
resolved in Gateway and disabled in Nexus. Keep the separate published-version
companion adapter's compatibility contract. Preserve historical research scores.

Acceptance: valid pinned sources pass; altered catalogs, mutable/incorrect pins,
missing source objects, reintroduced constants, changed SDK resolution or an
attempted authority grant fail with nonzero status. The result expressly grants
no runtime, commercial or release authority. Owner review and normal promotion
remain separate. Sprint-exit economics research is Business #1419.
