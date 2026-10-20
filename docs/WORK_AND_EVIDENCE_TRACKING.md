# Work and evidence tracking

Authority: Conxian/.github#43; phase coordinator: Business #1390. GitHub is the sole engineering work tracker. The current per-repo continuation is [the dated gap/support review](REPO_GAP_AND_SUPPORT_REVIEW_2026_10_19.md); its inventory counts and states are historical snapshots, not live totals.

## Distinct records

| Record | Purpose | Completion / authority boundary |
| --- | --- | --- |
| Issue | A problem or desired outcome, owning repo/person or role, priority, phase, dependencies and acceptance | Close only after its acceptance is evidenced; a merged implementation can leave operational acceptance open. Reuse an existing owner issue before creating another. |
| Task | A bounded checkbox in the owning issue with input revision, action, required test/receipt and next gate | A task's result is scoped to that action. Do not duplicate it across trackers or treat a checked research task as production support. Split into a linked issue only when independent ownership/acceptance requires it. |
| PR | One reviewable change on immutable source/tree identities, with tests and review | CI success is a candidate result, not issue or release completion. Preserve useful unrelated changes; source-qualified recovery can require a narrower PR. Do not weaken policy or manufacture checklist acceptance. |
| GitHub Project | An optional view grouping existing issues and PRs | A board is not a second task authority. Record verified board access and item state; no board reads or updates are claimed when the available connector cannot perform them. Missing board access does not block issue implementation. |
| Research record | Sources, version/date/digest, assumptions, comparison and the chosen implementation/test | Preserve unique findings and historical scores. Evidence gaps remain explicit; a proposal, simulation or source catalog cannot approve itself. |
| Operational receipt | Actual deployment artifact/source, resource identity, authenticated operation, intended network/tenant, timestamps and independent read-back | Keep restricted detail in its approved location. Health, registration, a configured secret or an app connection alone is not operation qualification. |

## Evidence dimensions and test order

| Dimension | Required evidence | If missing |
| --- | --- | --- |
| Source | Repository plus exact commit/tree and relevant dependency/lock identities | Source state unknown; do not transfer an old result to a new head. |
| Declarations | Runtime contract, generated templates, deploy modes and documentation agree | Correct code/docs before provisioning; do not count optional/conditional credentials as unconditional startup needs. |
| Provisioning | Redacted presence/configuration checks inside the approved secret boundary | Record unavailable. A declaration, placeholder or test credential is not a provisioned credential. Never export values, fingerprints or raw provider errors. |
| Connection | Authenticated identity and permitted scope, actual resources, exact service/tenant/network | Discovery alone is insufficient; empty, inactive, denied and unobserved are different states. |
| Operation | Allowed positive journey and denial, wrong tenant/network, missing/revoked credentials, rate limit, timeout, outage/recovery, replay/restart where applicable | Keep that operation unavailable; preserve separately accepted operations. |
| Release | Current-head tests, artifact provenance, required distinct review, branch gates and independent acceptance | Keep normal feature → dev → staged → main promotion; never rewrite an existing candidate or substitute a different head. |
| Service level | Complete observation window, service owner, recovery evidence and approved support terms | No availability, response-time or commercial qualification claim. Pricing/economics #1419 and final whitepaper #1422 retain accepted-exit timing. |

## Current remediation work packages

- **R0/R1 — Gateway contract/diagnostic truth:** #466/#548 and Business #1411/#1423. Gateway #568 replaces stale secret-count/readiness claims with a runtime-bound contract description, generated documentation, explicit CLI syntax/liveness scope and negative tests. Verify the exact submitted head; cross-repo mirrors must link the owning source rather than copy a permanent count.
- **R0/R1 — Inventory and knowledge:** the org scanner correction is merged through Business #1440. Its source scope does not enumerate runtime connections, every PR branch or undiscovered security gaps. Reconcile docs/agent mirrors with the current registry without treating registry `active` as deployed health. KB #63 and public controls .github#43/#47/#53/#60 retain their existing boundaries.
- **R1/R3 — CLI installation and runtime configuration:** doctor inspects defaults, while its templates still require operator completion against current runtime secrets, ports and persistence. The corrected diagnostic wording does not finish #1411. Verify generated templates, actual injected configuration and process lifecycle before advertising turnkey deployment.
- **R1/R3 — Connected systems:** Business #1423/#1424/#1429 own authenticated observation and customer-lifecycle work. A connected Zoho CRM app is not backend support ticket integration; actual provider/tenant, scoped backend identity, restricted mapping, lifecycle/idempotency and deployed read-back remain required. Keep engineering issues in GitHub; do not create ClickUp/Linear mirrors.
- **R1 — Native dependency and research recovery:** Business #1414, Wallet #357/#745/#741/#737, Platform #1426/#1450, Core #440, Nexus #418 and Market #176/#159 route the existing work. Preserve useful compiler/backend fixes, models and research. Resolve actual advisory/compiler/interface failures and policy changes separately; prototypes need qualified provider/verifier contracts.
- **R3/R4 — Billing and release:** Core billing restoration, Business export conformance and Labs #86 are implemented source work. Verify their exact candidates, consumers and deployed boundaries under #1343/#80; do not repeat merged repairs or infer payment-backed entitlement from sales stages. SDK hardware/signing owner tracks and independent review remain required.

For every involved PR, record one disposition: accepted and contained; useful work requiring bounded recovery; dependency/compatibility remediation; release candidate missing acceptance; conflicted preservation; or external upstream lead. A no-check result is unknown, not green. Close superseded work only after current-head ancestry/content proof and retention of unique discussion/research; retain its branch/history. Refresh the queue before acting because other maintainers and automation can change it during a session.
