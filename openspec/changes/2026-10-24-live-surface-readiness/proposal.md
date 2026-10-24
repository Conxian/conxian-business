# Detect deployed application failures behind successful page builds

Owners: Business #1349/#1390; topology coordination Platform #1167.

The 24 October connected-provider audit reproduced HTTP 200 pages with HTTP 503
Platform readiness, and a Business sign-in returning HTTP 500 because the deployed
database has no `user` relation. The existing topology check only checks home-page
status and can report success while authentication and persistence are unavailable.

Add a bounded, read-only Business health route that checks the schema and access
needed by its authentication and audit code. Return only generic health status;
never return database identifiers, errors, account records, or credentials. Extend
the existing topology checker to test the currently mapped Platform health
contract and identify the BOS control surface. Missing DNS evidence must remain
unknown and fail the full topology check; offer an explicit HTTP-only diagnostic.

Preserve the existing independent release gates. This work neither changes DNS
nor settles the contradictory `www` declarations in the retained site map. Record
observations separately from intended placements, including provider limitations.
Do not bootstrap empty state, migrate a database, weaken authentication, or turn
unconfigured services into healthy responses.

Acceptance: regression tests reproduce 200-page/503-backend false success,
wrong-control-application routing, missing/malformed schema, dependency failure,
and incomplete DNS evidence. Run source-bound checks and record the live failing
observations honestly before normal reviewed promotion and production acceptance.
