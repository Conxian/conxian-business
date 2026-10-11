# BOS Business Systems Expansion: Evidence and Implementation Gates

**Review date:** 2026-10-11  
**Scope:** Bounded source review at the refreshed parent-repository submodule pins.  
**Classification:** Public-safe research; not a production-readiness or commercial commitment.

This report turns the Session 67 four-phase roadmap into an evidence-backed implementation queue. It records what the checked-out sources demonstrate, what remains a design or integration gap, and which repository owns the next change. Submodule references describe the exact parent-pinned commits below, not necessarily later remote tips.

## Evidence snapshot

The root PR branch was current with its remote. All eight submodules were fetched and advanced to their configured `main` tips; their worktrees are detached and clean. The market submodule follows `main` in `.gitmodules` and is not frozen by an `update=none` override.

| Repository | Parent pin |
|---|---|
| `conxian-gateway` | `d84c2a50e4882c4a979e5fabc08df63d96b2780c` |
| `conxian-labs-site` | `86e6fcd04b7ad0da2e100d87ef48a8bf727ca28e` |
| `conxian-nexus` | `6d2a339a910dbfed632d920d5600a3ec420471b1` |
| `conxian_market` | `581383c6e8a28aaa0f3a25829da1adbbb94c8766` |
| `conxius-enclave-sdk` | `2917c3cec16fce999edf7adc96f8457dce9cd93b` |
| `conxius-platform` | `2f4acde575233ca1fcc6916a97763656ec1e06b7` |
| `conxius-wallet` | `1310955daec71f91f0df58417ccac6ac9ceae768` |
| `lib-conxian-core` | `fb2807faef35c030e6d0a8911ef4c4913e951099` |

## Findings by phase

| Phase | Verified in pinned source | Remaining work and owner |
|---|---|---|
| 1. Strategic intelligence | `conxian-gateway` owns API/protocol adapters; `conxian-nexus` owns subscription tiers; `lib-conxian-core` owns the canonical settlement fee model; `conxian_market` contains the TypeScript fee reference and agent-payment SDK; `conxius-enclave-sdk` owns enclave/protocol primitives. The eight parent pins pass `scripts/verify_submodule_integrity.py`. | Keep taxonomy and domain boundaries in governance docs, but do not treat a valid gitlink as release compatibility. For each dependency bump, validate the consumer lockfile, API compatibility, and downstream tests. Business owns the index; implementation owners own code and acceptance. |
| 2. BaaP monetization | Core `fee.rs` implements ADR-004 settlement fees, rail floors, volume tiers, load clamping, and a **50/30/20** settlement-fee distribution. Nexus `SubscriptionTier::enterprise_fee_cap()` maps Enterprise to the core option, with billing/fee conformance tests. Gateway `billing.rs` separately defines a $200 managed base fee, per-operation prices, and a 20% relay-volume discount. | Billing is not one source of truth: Gateway does not consume the Nexus tier/cap, and its managed prices are separate. Continue the design in `docs/BILLING_UNIFICATION_DESIGN.md`; owner-approved values, a shared contract, consumer wiring, and drift tests are distinct gates. The commercial doctrine's **80/10/10** allocation is a separate business allocation, not ADR-004's settlement distribution. |
| 3. ISO 20022, CJCS, and agent commerce | Gateway `camt.rs` generates and structurally validates `camt.053.001.08` and `camt.054.001.08`, with optional OData v4 webhook dispatch; its API routes include `pacs.008` ingress. The Market SDK exports an MCP-402 facade, wires it into `ConxianMarketSDK`, and tests valid-receipt authorization and amount-mismatch rejection. CJCS-related types and integration tests also exist in Gateway/Core. | Existing generators and SDK tests are bounded evidence, not proof of full ISO 20022 XSD/business-rule conformance, terminal `pacs.002` end-to-end settlement finality, deployed MCP service, or tenant-isolated agent execution. Map each message to owner API, schema, persisted identifiers, and fail-closed finality tests before describing the entire workflow as shipped. Treat multi-chain names as adapter coverage only where each owner's tests prove them. |
| 4. Knowledge and candidate lifecycle | The research ledger has a machine-readable validator; cross-repo alignment, doctrine, client-onboarding, and repository checks are separate scripts. The new candidate is intentionally unscored with `tracker-required-before-scoring`. | Create or identify a canonical owner issue before scoring or expanding implementation scope. Keep evidence in the owning repository, preserve the ledger's bounded-scan rule, and make a dated refresh only when sources or decisions change. |

## Release and verification corrections

- At the refreshed enclave SDK pin, `Cargo.toml` declares `2.1.0`, while the latest `CHANGELOG.md` release heading is `[2.0.17]`. The repository has no `v2.1.0` tag at this pin. The release-hygiene verifier reports the changelog mismatch as a violation and the absent tag as a warning. The claim that the SDK changelog was synchronized to `2.1.0` is not supported by the checked-out source.
- `verify_submodule_integrity.py`, `verify_cross_repo_alignment.py`, `verify_doctrine_alignment.py`, and `verify_bos_research_candidate_ledger.py` pass. `verify_release_hygiene.py` fails on the SDK mismatch; `scripts/bos_repo_check.py` consequently fails its release-hygiene stage. Do not summarize this result as “100% of checks passed.”
- No price, yield split, SLA, live rail telemetry, partner integration, production status, or owner approval is created by this report. `docs/BILLING_UNIFICATION_DESIGN.md` remains a proposal pending owner sign-off on tier changes.

## Implementation queue

1. **Governance, this repository:** retain the four-phase roadmap as the index; link this evidence report and label each capability `implemented`, `partial`, `proposed`, or `owner-gated` with dated provenance.
2. **SDK, `conxius-enclave-sdk`:** resolve the `2.1.0` changelog/version discrepancy in the SDK's own release workflow, then run that repository's release-hygiene checks. Do not hand-edit a submodule worktree from this parent PR or imply that a release/tag was created.
3. **Billing, Gateway + Nexus + Core + Market:** owner-review the billing design; define the canonical contract and conformance vectors; wire one consumer at a time; test the mapping, fee cap, rounding, discounts, and failure behavior. Keep commercial tier prices owner-gated.
4. **Settlement interoperability, Gateway + Nexus:** map each supported message version to request/response types, schema validation, persisted identifiers, and finality state. Add tests for identifier mismatch, nonterminal/rejected `pacs.002`, timeout, and retry behavior in the owning repository before claiming complete settlement integration.
5. **Agent commerce, Market + owning Gateway/Platform surfaces:** distinguish the tested MCP-402 SDK facade from a deployed tool service. Verify payer/tenant authorization, replay/idempotency, rate limits, metering, and cross-tenant isolation before describing agent execution or pricing controls as operational.
6. **Research lifecycle, Business:** attach a canonical tracker, update the machine-readable and human-readable ledger together, run the dedicated ledger validator, then update the knowledge graph/changelog with only the verified result.

## Verification record

Commands run against the refreshed parent-pinned checkout:

- `python3 scripts/verify_submodule_integrity.py` — passed.
- `python3 scripts/verify_cross_repo_alignment.py` — passed.
- `python3 scripts/verify_doctrine_alignment.py` — passed.
- `python3 scripts/verify_bos_research_candidate_ledger.py` — passed.
- `python3 scripts/verify_release_hygiene.py` — failed on the pinned SDK changelog/version mismatch; absent `v2.1.0` tag reported as a warning.
- `python3 scripts/bos_repo_check.py` — failed at release hygiene for the same mismatch; other displayed repository gates passed, with live branch-protection state marked unverified/blocked.

This record is limited to repository-local checks. It does not validate external services, later remote tips, production deployments, or owner approval.