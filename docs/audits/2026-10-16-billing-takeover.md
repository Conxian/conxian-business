# Billing and capability propagation checkpoint — 16 October 2026

Public-safe development coordination under [#1390](https://github.com/Conxian/conxian-business/issues/1390)
and [#1343](https://github.com/Conxian/conxian-business/issues/1343).
This dated overlay advances G05 in R1 and the configuration part of G08;
the [research/phase register](../RESEARCH_IMPLEMENTATION_RECONCILIATION_2026_10_15.md)
retains its historical inventory and scores. It is not a new production or
commercial authorization.

## Current implementation

| Component | Exact source | Verified disposition |
| --- | --- | --- |
| SDK development source | `cb6b9c69752b7082d71b0ea7431a40a498ae8a6e` | Core's opt-in development dependency; provider identity and policy hardening retained. |
| Core | `9dd3676bb64a5ba327cc2717d9e9d32bd09a2c95` | [#462](https://github.com/Conxian/lib-conxian-core/pull/462) merged to dev as `b8fafdf6faf86d8314f5dd8ff3514f78696ff5be`; merged tree equals the tested source. Owns the versioned offline configuration catalog. |
| Gateway | `5b15b715c1b63e577197aaa76620c783ed7f7956` | [#536](https://github.com/Conxian/conxian-gateway/pull/536) merged to dev after reconciliation with journal-preview [#534](https://github.com/Conxian/conxian-gateway/pull/534). Exact merged tree is `7dd8a49e658cd9f4f4e9a759a8f7b7d88c3f6ee6`. |
| Nexus | `1a4e73e1a249e44a31e7e989cdeb61327b72170c` | [#423](https://github.com/Conxian/conxian-nexus/pull/423) is the remaining consumer review candidate. Exact tested/published tree is `821be2a9e3e6114d9e8ac0769cb5e8353d053c93`. |

Gateway and Nexus pin the same Core source. Gateway resolves Core's optional
development SDK at the recorded revision. Nexus's default feature graph does
**not** resolve the SDK. The propagation check verifies that distinction; it
does not silently enable a feature to make the graphs look identical. Core's
published-version companion adapter retains its separate SDK =2.0.17 contract.

## Contract and behavioral boundaries

- Managed-service charges remain Gateway configuration in USD cents. The legacy
  `compute_mrr` function estimates configured charges; it does not measure
  recognized revenue, cash collected or settled payments.
- Nexus retains its public `SubscriptionTier` type, wire values, parser, quota
  limits, feature eligibility, upgrade amounts and invoice expiry. Definitions
  delegate to Core; tenant authentication, metering and enforcement stay in Nexus.
- ADR-004 per-settlement fees and Enterprise cap eligibility retain their existing
  semantics. Configured eligibility does not establish a paid subscription.
- Payment-backed entitlement requires its own verified payment, tenant binding,
  durable state, expiry/renewal/revocation and integration evidence. An accounting
  preview, catalog, tier name or passing test does not supply those facts.

The Labs site's unsupported subscription offer was already disabled; the older
[billing proposal](../BILLING_UNIFICATION_DESIGN.md) remains historical. No proposed
commercial rate is activated. x402 names a payment protocol, not an asset.

## Validation and reproducibility

The [machine-readable inputs](../billing-propagation-2026-10-16.json) bind the
catalog's SHA-256, exact source commits, separate units and SDK resolution.
`scripts/verify_billing_propagation.py` reads committed source objects and checks
checkout identity, Core/SDK declarations and lock sources, shared imports and
reintroduced local constants. CI checks out those four exact sources with
read-only permissions and no persisted credentials. It validates a dated source
snapshot; it does not monitor every moving branch or deployed artifact.

```sh
python3 scripts/verify_billing_propagation.py --source-root /path/to/pinned-sources
python3 -m unittest scripts.tests.test_billing_propagation -v
```

The source root must contain checkouts named `conxius-enclave-sdk`,
`lib-conxian-core`, `conxian-gateway` and `conxian-nexus`, each at its recorded HEAD
with the corresponding GitHub origin. Working-file edits are not used as evidence.

Validation retained from the unchanged implementation candidates: Core's full
all-feature suite passed 340 tests (two existing ignored); Gateway passed 574
default and 589 mock tests plus all seven WireMock scenarios; Nexus's full locked
workspace passed 371 tests. Fresh confirmation on 16 October: Nexus billing
catalog/flow tests (3), dependency-policy tests (6), strict workspace/all-target
Clippy, formatting, contamination and license-structure checks pass. Gateway's
combined merged source passes all 72 client SDK tests and SDK typechecking.
Gateway #536's final head has green hosted code/policy checks and a recorded
approval. These results do not establish independent operator identity or runtime
qualification. Local browser acceptance remains unavailable because Chromium
was not usable in the recorded validation environment.

## Remaining work and phase ownership

| Work | Phase / existing owner | Next acceptance evidence |
| --- | --- | --- |
| Nexus consumer delivery | R1 / Nexus #423, Business #1390 | Current-head hosted checks and applicable owner review; normal dev integration. |
| Merchant and key lifecycle | R3 / [Gateway #507](https://github.com/Conxian/conxian-gateway/issues/507) | Signed/idempotent merchant events, durable lifecycle, tenant isolation and actual integration receipts. |
| Paid product integration | R3 / [Market #159](https://github.com/Conxian/conxian_market/issues/159), [Labs Site #80](https://github.com/Conxian/conxian-labs-site/issues/80), Business #1343 | Authentic payment/entitlement resolver and demonstrated provisioning, renewal/revocation and reconciliation. |
| Measured fee inputs | R3 / [Gateway #531](https://github.com/Conxian/conxian-gateway/issues/531) | Provenance, allocation and freshness of actual cost/congestion inputs. |
| Capability/release propagation | R2/R4 / Business #1390 and repository owners | Exact provider/hardware/runtime evidence, normal promotions, artifact read-back, required independent acceptance and release sign-off. |
| Pricing and ecosystem sustainability | R5 / [Business #1419](https://github.com/Conxian/conxian-business/issues/1419) | Begins after verified accepted sprint exit; competitor scope/terms, measured unit economics, retention and bounded shadow-pricing research. |

The sprint-exit research is a separate track. Its metric dictionary includes
gross/contribution margin, EBITDA reconciliation, cash flow, retention and R&D /
upstream support. Financial actuals, models and vendor agreements remain in the
approved non-Git record system. No production repricing, financial claim or funding
disbursement is authorized here. GitHub Projects-v2 was not updated; issue/PR
checkpoints carry the supported coordination. The parent issues remain open.
