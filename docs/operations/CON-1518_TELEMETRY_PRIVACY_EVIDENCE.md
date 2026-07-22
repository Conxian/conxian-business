# CON-1518 telemetry privacy and operational evidence

**Status:** Public-safe implementation/evidence boundary — **Beta / conditional**
**Last updated:** 2026-07-21
**Tracking:** [CON-1518](https://linear.app/conxian-labs/issue/CON-1518/p1-define-telemetry-privacy-monitoring-and-public-safe-operational) is an internal work record; private issue content is not reproduced here.

## Scope and exact implementation reference

CON-1518 covers telemetry privacy, delivery semantics, monitoring guidance, disablement, rollback, and public-safe operational evidence for the enclave SDK. The implementation landed upstream in [PR #210](https://github.com/Conxian/conxius-enclave-sdk/pull/210), merged at `593af0d9120b612de5b2817866b0528e5c877570`.

This business repository does not duplicate upstream source or tests. Its exact reviewed `conxius-enclave-sdk` gitlink remains pinned to `451202f51a9efed8fde70b7a5567a3e7e16c1db9`; the upstream telemetry implementation is recorded at `593af0d9120b612de5b2817866b0528e5c877570`, and the submodule branch metadata is `main`. The upstream public operating guidance is [TELEMETRY_OPERATIONS.md](https://github.com/Conxian/conxius-enclave-sdk/blob/593af0d9120b612de5b2817866b0528e5c877570/docs/operations/TELEMETRY_OPERATIONS.md).

## Privacy and minimized payload behavior

- Telemetry is disabled unless an integrator explicitly attaches a client; an explicit disabled client is available.
- The request body contains only a schema version and a coarse event name. It does not contain credentials, private keys, raw signatures, signature-derived identifiers, raw attestation reports, addresses, assets, request data, or business metadata.
- The legacy signature-tracking compatibility method discards its identifier and emits only the same coarse event. New callers use the coarse event API.
- A configured API credential is sent only as a sensitive `X-Api-Key` transport header. It is not a JSON field and must not appear in logs, diagnostics, dashboards, tickets, or public evidence.
- The SDK does not define service-side retention or deletion policy. The service owner retains private ownership of that policy and must publish/review it before enabling telemetry for a deployment.

## Transport validation and bounded delivery

- Production endpoint configuration requires HTTPS, a host, no URL credentials, no query parameters, and no fragment. The SDK appends its fixed telemetry route; arbitrary endpoint data is not treated as payload data.
- The default request timeout is five seconds and the SDK accepts no policy above its 30-second maximum.
- The default is two retries (three total attempts), with bounded retry count and exponential backoff from 50 ms; the initial backoff cannot exceed one second.
- Transport failures and HTTP `408`, `429`, `500`, `502`, `503`, and `504` are retryable. Other HTTP failures are recorded without retry.
- Local delivery state is limited to `Disabled`, `Idle`, `Pending`, `Delivered`, and `Failed`, with safe failure categories and optional HTTP status. No request body, credential, or full endpoint is exposed by this state.
- There is no durable telemetry queue or shutdown-flush guarantee. An in-flight best-effort event may be lost during process shutdown.

## Rail non-gating behavior

Telemetry is best effort and is not a prerequisite for signing, attestation, settlement, or rail execution. Rail dispatch schedules telemetry without awaiting delivery; disabled telemetry, missing runtime, configuration failure, timeout, network failure, serialization failure, and terminal HTTP failure remain observable locally but do not become a rail authorization signal. Security and policy controls remain independent of telemetry.

## Monitoring, rollback, disablement, and recovery

- Monitor only aggregate delivery outcomes, retry exhaustion, and HTTP status classes. Do not retain or export payloads, headers, credentials, private keys, raw attestations, signature material, or full endpoint values.
- Disable telemetry by omitting client attachment or supplying the explicit disabled client. Disabling telemetry must not change signing, attestation, settlement, or rail policy.
- Use the public-safe [Phase 6 production rollout runbook](./CON-681_PHASE6_PRODUCTION_ROLLOUT_RUNBOOK.md), [rollback drill simulation](./CON-681_PHASE6_ROLLBACK_DRILL_SIMULATION.md), and [compatibility and acceptance gate checklist](../COMPATIBILITY_MATRIX_AND_ACCEPTANCE_GATE_CHECKLIST.md) for gate progression, rollback triggers, safe evidence capture, and recovery ownership. Restricted identifiers and privileged command details remain in the corresponding private operating records.
- Before release recovery or re-enable, verify the exact reviewed SDK pin, format/lint/test results, capability-evidence output, and the service-side retention/alerting decision. If any required evidence is absent, keep telemetry disabled and the capability Beta / conditional.
- For suspected secret egress or unexpected telemetry content: disable telemetry, preserve only safe timestamps/status categories/artifact references, and escalate through the service owner's private incident channel. Public-safe escalation and communication templates are in the [rollout runbook](./CON-681_PHASE6_PRODUCTION_ROLLOUT_RUNBOOK.md#6-communication-templates); implementation tracking is in [upstream issue #201](https://github.com/Conxian/conxius-enclave-sdk/issues/201) and [CON-1518](https://linear.app/conxian-labs/issue/CON-1518/p1-define-telemetry-privacy-monitoring-and-public-safe-operational).

## Public/private evidence boundary

This document records repository-visible implementation and safe operating expectations only. It does **not** claim service-side retention/deletion evidence, deployed monitoring or rollback/recovery evidence, release-candidate evidence, independent security review, or final production acceptance. Those artifacts remain private or open work until separately produced and reviewed.

## Beta and conditional support boundary

The enclave SDK remains **Beta / conditional**. This remediation does not authorize value-bearing production signing or settlement, and the presence of telemetry APIs, tests, a passing local build, or a pinned commit does not upgrade that status. No value-bearing production claim is made from this document.

## Acceptance and evidence checklist

- [x] Upstream implementation merged in PR #210 at `593af0d9120b612de5b2817866b0528e5c877570`.
- [x] Business repository retains the exact reviewed SDK SHA `451202f51a9efed8fde70b7a5567a3e7e16c1db9`.
- [x] Public-safe upstream operations guidance is linked.
- [x] Root CI verifies the pin and runs SDK format, clippy, all-feature tests, focused telemetry tests, and capability evidence when present.
- [ ] Independent review of the exact business-repo candidate.
- [ ] Service-side retention/deletion policy, ownership, and evidence (private boundary).
- [ ] Deployed monitoring, alerting, rollback, and recovery evidence.
- [ ] Final release and production acceptance gates.

## Focused SDK verification commands

From the business-repository root:

```bash
git submodule update --init conxius-enclave-sdk
git submodule status conxius-enclave-sdk
git -C conxius-enclave-sdk rev-parse HEAD

cd conxius-enclave-sdk
cargo fmt --package conxius-enclave-sdk -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
cargo test telemetry --all-features -- --nocapture
if test -f scripts/validate_capability_evidence.py; then
  python3 scripts/validate_capability_evidence.py --check
fi
cd ..
```

## Full-repository hygiene checks

From the business-repository root, initialize all configured submodules before running the repository-wide validator:

```bash
git diff --check
git submodule update --init --recursive

python3 scripts/verify_contamination_guard.py
python3 scripts/verify_submodule_integrity.py
```

The literal workspace-wide `cargo fmt --all -- --check` should also be run when all root workspace members are initialized; this repository's SDK CI gate is package-scoped so unrelated formatting drift in the preserved Nexus check cannot mask SDK coverage. `verify_submodule_integrity.py` requires the configured submodules to be initialized, so the recursive initialization command above is a prerequisite for that check.

The root CI job is the acceptance gate for the enclave SDK because the root Makefile's `test-all` intentionally avoids implicit submodule initialization and network-dependent work.
