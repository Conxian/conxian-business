# Bitcoin-Native Upgrade Research (public-safe stub)

Treat this repository as public for boundary purposes.

Sensitive/internal analysis for bridge hardening, throughput assumptions, and rollout gates has been migrated to the Linear Virtual Office.

See:

- https://linear.app/conxian-labs
- https://linear.app/conxian-labs/issue/CON-530/replace-sensitive-files-with-safe-examples-and-docs
- https://linear.app/conxian-labs/issue/CON-256

## How to work locally (public-safe)

1. Model upgrades with feature flags and testnet-only placeholders.
2. Use synthetic transaction samples instead of production traces.
3. Keep threshold values and operational guardrails in Linear, not in repo docs.

### Local-safe feature-flag sketch

```text
BITCOIN_NATIVE_MODE=experimental
BRIDGE_PROOF_MODE=placeholder
SETTLEMENT_LATENCY_TARGET=LOCAL_TEST_ONLY
```

Internal: search Linear Virtual Office for "Bitcoin-Native Upgrade Research".

This file is intentionally kept as a stub so existing links continue to resolve.
