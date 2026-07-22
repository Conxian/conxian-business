# CON-1512 — hardware-backed signing and mandatory attestation phase plan

> **Status:** Canonical, public-safe research and sequencing record; not a production authorization.
>
> **Evidence snapshot:** July 22, 2026. **Normative-source access date:** July 22, 2026.
>
> **Linear authority:** https://linear.app/conxian-labs/issue/CON-1512/p0-enforce-hardware-backed-signing-and-mandatory-attestation-for-value

## Scope and boundary

CON-1512 covers the evidence and dependency chain required before a value-bearing operation may be authorized with hardware-backed signing and mandatory attestation. It is intentionally provider-neutral at the contract layer and provider-specific only at a qualified integration boundary.

This document does **not** claim current hardware production support, release readiness, protocol-key custody, or execution authorization. Unsupported production paths remain disabled and fail closed. A successful build, passing software fixture, simulated provider, current branch, or readiness wrapper is not sufficient evidence for a value-bearing production claim.

The Linear implementation decomposition is:

- Parent: https://linear.app/conxian-labs/issue/CON-1512/p0-enforce-hardware-backed-signing-and-mandatory-attestation-for-value
- Shared trust and replay prerequisite: https://linear.app/conxian-labs/issue/CON-1543/p0-operationalize-attestation-roots-collateral-revocation-and
- Android track: https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity
- AWS Nitro track: https://linear.app/conxian-labs/issue/CON-1545/p0-qualify-aws-nitro-attestation-and-kms-secret-release-boundary
- Runtime/platform evidence: https://linear.app/conxian-labs/issue/CON-1517/p1-harden-the-wasm-secret-boundary-and-add-runtimeplatform-evidence
- Independent review and release acceptance: https://linear.app/conxian-labs/issue/CON-1519/p0-complete-independent-security-review-and-release-acceptance

## 1. Three claims that must not be conflated

| Claim category | What it proves | Minimum evidence | What it does **not** prove |
| --- | --- | --- | --- |
| **Authorization proof** | A user or workload approved a particular action, principal, policy, challenge, and expiry. | Domain-separated request, proof-of-possession, user/workload binding, purpose binding, and replay-resistant freshness. | That the device is genuine, that a platform is measured correctly, or that a protocol private key is hardware-held. |
| **Platform attestation** | A verifier accepted evidence about key origin, device/app or workload measurement, posture, freshness, and policy version. | A signed attestation statement, trusted roots, current collateral, revocation result, nonce/challenge, and an auditable verifier decision. | That the user approved the action or that the attested key is the Bitcoin/Stacks protocol signer. |
| **Protocol-key custody and signing** | The exact value-bearing key is non-exportable or otherwise controlled by an approved custody boundary and signs the required protocol algorithm and payload. | Key identity and algorithm binding, custody evidence, signer authorization, deterministic protocol vectors, and release/runtime evidence for the exact artifact. | That a device/app/workload attestation or a structurally valid signature alone is enough. |

For a value-bearing operation, the acceptance predicate is the intersection of all three categories:

```text
authorized action
  AND verified platform evidence
  AND approved protocol-key custody/signing
  AND fresh, durable replay decision
  AND exact released artifact
```

If any term is unavailable, unsupported, stale, ambiguous, or unverifiable, the operation remains disabled.

## 2. Current artifact and status map

### Implementation and evidence baseline

| Artifact | Current state as of July 22, 2026 | Evidence boundary |
| --- | --- | --- |
| `conxius-enclave-sdk` baseline PRs [#205](https://github.com/Conxian/conxius-enclave-sdk/pull/205), [#214](https://github.com/Conxian/conxius-enclave-sdk/pull/214), [#216](https://github.com/Conxian/conxius-enclave-sdk/pull/216), [#220](https://github.com/Conxian/conxius-enclave-sdk/pull/220), [#224](https://github.com/Conxian/conxius-enclave-sdk/pull/224), [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237), [#238](https://github.com/Conxian/conxius-enclave-sdk/pull/238), and [#239](https://github.com/Conxian/conxius-enclave-sdk/pull/239) | Merged baseline and containment history. | Historical implementation evidence; not a current production-support statement. |
| SDK PR [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237) at `8f3fa687f4a880c0a12ec1fabc613ecc9e043df4` | Merged independent proof-factor verification. | Proves typed proof decomposition and independent checks at that changeset; does not qualify hardware or provider support. |
| SDK PR [#239](https://github.com/Conxian/conxius-enclave-sdk/pull/239) at `0510ecd5096c39eed4b8909f9e48e56697a7bc57` | Merged independent proof verification and fail-closed authorization behavior. | Strengthens authorization containment; does not prove platform attestation, protocol-key custody, or release evidence. |
| SDK PR [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244) at current head [`e3b1a69752f3e40f26b373e36ecab440c78419a9`](https://github.com/Conxian/conxius-enclave-sdk/commit/e3b1a69752f3e40f26b373e36ecab440c78419a9) | Open implementation PR; follow-up review [#4755756667](https://github.com/Conxian/conxius-enclave-sdk/pull/244#pullrequestreview-4755756667) after the replay-capacity fix reports no actionable findings and all reported SDK checks pass; requires the canonical six-proof rail before settlement authorization. | **Selected containment candidate.** It is not merged, does not provide a production verifier registry, and enables no hardware provider. |
| SDK issue [#195](https://github.com/Conxian/conxius-enclave-sdk/issues/195) | Open P0 umbrella for hardware-backed signing and mandatory attestation. | Current public implementation/evidence boundary for value-bearing operations. |
| SDK issue [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | Open P0 shared trust, collateral, revocation, and distributed replay work. | Shared prerequisite for provider tracks; current research scores are recorded below as planning aids. |
| SDK issue [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) / Linear [CON-1544](https://linear.app/conxian-labs/issue/CON-1544/p0-qualify-android-keymintstrongbox-authorization-and-play-integrity) | GitHub issue **closed** with `state_reason=completed`; Linear issue **Done**. | Administrative closure/completion is not production qualification evidence: real trusted roots/collateral, server-side verification, real-device/runtime evidence, exact key/operation binding, replay, and independent release acceptance remain required; unsupported production paths stay fail closed. |
| SDK issue [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) | Open AWS Nitro attestation and KMS release-boundary track. | Candidate server/cloud workload evidence and secret-release path; no current protocol-signer qualification. |
| Gate [#890](https://github.com/Conxian/conxian-business/issues/890) | Open, blocked at Gate 0. | A downstream protocol-control handoff shell, not authorization for funding, signer ceremony, deployment, authority transfer, or mainnet transactions. |

Stable bounded interface/containment artifacts linked to this snapshot are the merged SDK Android boundary [#243](https://github.com/Conxian/conxius-enclave-sdk/pull/243), open provider-neutral contracts [#245](https://github.com/Conxian/conxius-enclave-sdk/pull/245) with current review findings [#4755943314](https://github.com/Conxian/conxius-enclave-sdk/pull/245#pullrequestreview-4755943314), the merged wallet KeyMint boundary [#441](https://github.com/Conxian/conxius-wallet/pull/441), and open wallet Play Integrity/request-hardening follow-ups [#442](https://github.com/Conxian/conxius-wallet/pull/442) and [#443](https://github.com/Conxian/conxius-wallet/pull/443). These are bounded interface/containment artifacts only: they do not establish production provider verification, durable replay, real-device qualification, protocol-key custody evidence, or independent release acceptance. PR #245's current review identified unresolved policy-digest/expected-collateral binding, idempotent-vs-conflicting replay outcome, deserialization invariant, and non-production replay-store registration gaps; SDK #240 and CON-1543 remain open shared prerequisites, and this update does not modify PR #245.

The business repository must keep the SDK gitlink, an SDK released artifact, and the SDK current `main` head as separate evidence objects. The current business pin is not the same thing as PR #244, the released SDK, or upstream `main`.

### Explicit gaps and stale/high-risk claims

| Gap or claim risk | Current fact | Blocking consequence |
| --- | --- | --- |
| Production verifier registry | Unavailable in the current evidence set. | No provider result can be promoted to a production trust decision. |
| Roots, collateral, and revocation | Shared roots, freshness collateral, and revocation handling are absent as an operational verifier contract. | Attestation cannot be treated as durable or current; this is the shared #240 / CON-1543 prerequisite. |
| Replay protection | Replay state is process-local rather than durable and distributed. | A restart or replica boundary can invalidate uniqueness assumptions; value-bearing authorization remains disabled. |
| Canonical rail convergence | The six-proof rail is in open PR #244, not in the parent repository’s current pin. | The selected containment design is not yet a merged or released artifact. |
| Wallet value operations | Web/software value signer paths and synthetic-success fixtures remain gaps. | Wallet readiness language must not be read as current production evidence. |
| Android evidence | Heuristics and StrongBox AES storage are not the same as server-verified KeyMint signing attestation. | Android qualification requires attested signing-key authorization, chain validation, freshness, and Play Integrity verification; heuristics do not satisfy it. |
| Runtime, release, and independent evidence | WASM secret-boundary/runtime evidence, immutable release synchronization, and independent acceptance evidence remain absent or incomplete. | CON-1517, CON-1519, SDK #200, and SDK #202 remain release blockers for affected claims. |
| Business pin and branch drift | `.gitmodules` tracks SDK `master` while the upstream default is `main`; the business gitlink, an SDK release, and current upstream `main` are distinct. Pin/release drift is **not current evidence** of upstream capability. | Do not change the pin or promote readiness in this documentation PR; track synchronization separately. |
| Attestation versus custody | Device or workload evidence does not establish custody of a Bitcoin/Stacks protocol key or the correct protocol algorithm. | P-256 authorization and secp256k1/Schnorr signing must remain separate acceptance lanes. |

## 3. Typed dependency graph and provider decision

| From | Relationship | To | Meaning |
| --- | --- | --- | --- |
| `CON-1512` | decomposes into | `CON-1543`, `CON-1544`, `CON-1545` | Shared trust/replay work precedes concrete Android and Nitro qualification. |
| SDK PR [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237) | strengthens | authorization proof | Independent proof factors are typed and checked separately. |
| SDK PR [#239](https://github.com/Conxian/conxius-enclave-sdk/pull/239) | enforces | fail-closed authorization | Structural proof verification is not a hardware-support claim. |
| SDK PR [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244) | contains | canonical six-proof rail | The selected rail-convergence step gates settlement authorization before provider qualification. |
| SDK issue [#240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | blocks | SDK issues [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) and [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) | Provider tracks need common roots, collateral, normalized results, revocation, freshness, and durable replay semantics. |
| Android track [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) | supplies | bounded phone/client KeyMint/StrongBox and Play Integrity request/evidence interfaces | The current SDK/wallet slices provide bounded KeyMint/StrongBox and Play Integrity request/evidence interfaces; server-side verification, real-device qualification, and exact protocol-key custody remain separate acceptance gates. |
| Nitro track [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) | supplies | server/cloud workload evidence | Nitro measurements plus attested KMS release can protect a release boundary; they do not replace exact protocol-signer qualification. |
| `CON-1517` | blocks | runtime/platform claims | WASM secret-boundary and runtime evidence must match the exact released artifact. |
| `CON-1519` / SDK issue [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | gates | immutable release acceptance | Independent review and capability-by-capability acceptance remain required. |
| Gate [#890](https://github.com/Conxian/conxian-business/issues/890) | depends on | hardware/attestation and independent acceptance | Downstream control-plane handoff remains blocked and is not execution authorization. |

**Split-provider decision:** use separate tracks rather than a universal hardware claim.

- **Phone/client:** Current SDK/wallet slices provide bounded Android KeyMint/StrongBox and Play Integrity request/evidence interfaces. Server-side verification, real-device qualification, and exact protocol-key custody remain separate acceptance gates; keep the authorization key and any protocol signer distinct, and do not treat Android P-256 evidence as secp256k1/Schnorr custody evidence.
- **Server/cloud:** AWS Nitro attestation plus an attested KMS release boundary. Nitro measurement proves workload evidence for the configured policy; it does not by itself prove protocol-key custody or replace an approved signer boundary.
- **Complementary controls:** WebAuthn and TPM 2.0 are authorization/quote candidates, not substitutes for a protocol-key custody decision. Direct KMS/HSM custody is a custody comparator, not automatically an attestation result.
- **Deferred candidates:** AMD SEV-SNP, Intel SGX/TDX, Apple App Attest, and Arm CCA/PSA remain research candidates until their verifier, collateral, runtime, custody, and release evidence are scoped.

## 4. Weighted planning matrices

Scores use a transparent 0–5 scale: `0` means no demonstrated fit in this plan and `5` means strong relative fit for the stated criterion. The weighted total is `Σ(score / 5 × criterion weight)`. These are **planning aids, not support claims, certifications, or production approvals**.

### 4.1 Cross-repo containment candidates

| Candidate | Safety / containment leverage (30) | Dependency unlock (25) | Evidence readiness (20) | Delivery fit (15) | Fail-closed clarity (10) | Weighted / 100 | Planning state |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Canonical SDK rail convergence — [PR #244](https://github.com/Conxian/conxius-enclave-sdk/pull/244) | 5 | 5 | 4 | 4 | 5 | **93** | **Selected containment step; open PR, not production support.** |
| Wallet value-operation gate + provider-neutral envelope — [wallet #444 / CON-1546](https://github.com/Conxian/conxius-wallet/issues/444) | 5 | 5 | 3 | 3 | 5 | **86** | **Next** after the rail is canonical; blocks web/software signer and synthetic-success paths. |
| Provider-neutral trust/replay contracts — [SDK #240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) | 5 | 5 | 2 | 3 | 5 | **82** | Shared prerequisite for all provider tracks. |
| Runtime/release evidence synchronization — [CON-1517](https://linear.app/conxian-labs/issue/CON-1517/p1-harden-the-wasm-secret-boundary-and-add-runtimeplatform-evidence) and [CON-1519](https://linear.app/conxian-labs/issue/CON-1519/p0-complete-independent-security-review-and-release-acceptance) | 4 | 3 | 2 | 4 | 5 | **69** | Follow-on release and acceptance synchronization; not optional for promotion. |

The ordering favors a small, reversible containment boundary before provider-specific work. It does not imply that PR #244, #240, or any other candidate is production-ready.

For continuity with the earlier #240 research, the shared prerequisite was also scored separately as **73/75** for the provider-neutral trust/collateral/result contract and **66/75** for the backend-neutral durable replay contract. Those scores are planning aids for the two different contracts, not support claims.

### 4.2 First concrete verifier/provider candidates

The custody score is deliberately separate from attestation strength. A platform can produce strong evidence while leaving protocol-key custody or algorithm binding unresolved.

| Candidate | Authorization fit (20) | Attestation / verifier evidence (25) | Roots / collateral maturity (15) | Protocol-key custody / signing fit (25) | Portfolio leverage (15) | Weighted / 100 | Planning interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| AWS Nitro + KMS authorization | 2 | 5 | 5 | 4 | 5 | **83** | Concrete server/cloud track; KMS release is not automatically protocol signing. |
| TPM 2.0 quote | 3 | 5 | 4 | 3 | 4 | **76** | Strong workload/platform quote candidate; requires a protocol-specific custody decision. |
| Android KeyMint/StrongBox + Play Integrity | 5 | 4 | 3 | 2 | 5 | **74** | Concrete phone/client track; current heuristics/AES storage do not satisfy it. |
| WebAuthn user authorization | 5 | 3 | 4 | 1 | 5 | **67** | Strong user authorization lane; not a protocol-key custody claim. |
| Direct KMS/HSM custody | 1 | 2 | 5 | 5 | 4 | **66** | Custody comparator; requires a separate authorization and platform-evidence contract. |
| Apple App Attest | 4 | 4 | 4 | 1 | 3 | **62** | App-integrity candidate; not a protocol signer by itself. |
| Intel SGX/TDX with DCAP | 1 | 4 | 4 | 2 | 3 | **55** | Attested workload candidate; verifier/collateral and custody integration remain scoped. |
| AMD SEV-SNP | 1 | 4 | 3 | 2 | 3 | **52** | Confidential-VM attestation candidate; not current provider support. |
| Arm CCA/PSA | 1 | 3 | 2 | 2 | 3 | **44** | Research candidate; evidence and integration maturity remain to be established. |

The current implementation decision is still the **split Android/Nitro portfolio** because those tracks have concrete repository/issue ownership and complementary client/server roles. The scores do not authorize a provider, and no row should be read as a support statement.

## 5. Phased roadmap and acceptance gates

| Phase | Scope and dependency | Acceptance/evidence gate |
| --- | --- | --- |
| **Phase 0 — source of truth** | Freeze the three-claim taxonomy, update the graph, link the claim/evidence boundary, and mark unsupported routes explicitly. | Every current claim points to an artifact and date; no private configuration or provider secret is copied into Git; missing evidence produces a disabled outcome. |
| **Phase 1 — canonical rail containment** | Land the six-proof authorization rail represented by SDK PR #244 after review and merge. | Exact proof classes are required before value-bearing settlement authorization; negative tests cover missing, malformed, stale, mismatched, and unsupported proofs; provider verifiers remain unavailable and fail closed. |
| **Phase 2 — wallet gate and envelope** | Add a provider-neutral value-operation gate and envelope that separates user authorization, platform evidence, protocol-key identity, algorithm, purpose, and replay fields. | Web/software value signers are rejected for value-bearing paths; synthetic-success fixtures cannot satisfy the gate; authorization and protocol signing keys are disjoint; unsupported providers remain disabled. |
| **Phase 3 — trust roots, collateral, revocation, and distributed replay** | Complete SDK #240 / CON-1543: versioned verifier registry, roots, collateral, revocation, freshness, normalized results, and durable atomic `consume_once`. | A real verifier decision is reproducible across restarts/replicas; stale/revoked/unknown roots and replayed challenges fail closed; the registry and policy version are auditable. |
| **Phase 4 — provider tracks** | Qualify Android #241 / CON-1544 and Nitro #242 / CON-1545 against the common contract. | Android proves server-verified KeyMint/StrongBox signing attestation and Play Integrity; Nitro proves measurement-bound KMS release; each track records its own collateral, failure modes, freshness, and exact key/custody boundary. |
| **Phase 5 — runtime integration** | Close SDK #200 / CON-1517 runtime, WASM secret-boundary, wallet, and platform evidence gaps. | Browser/Node/bundler/worker and device/runtime results are recorded for the exact artifact; no mock or synthetic path is reachable from a production route; release metadata matches the tested source. |
| **Phase 6 — immutable release and independent review** | Complete SDK #202 / CON-1519 with immutable artifact, provenance, SBOM, dependency/security evidence, version/pin synchronization, and independent review. | Capability-by-capability acceptance names the exact commit and artifact; independent review covers the claimed scope; only then may a separately approved production enablement decision be considered. |

## 6. Claim and evidence rules

1. **Code is not qualification.** API presence, compiled code, software fixtures, default providers, and passing unit tests are implementation evidence only.
2. **Attestation is not authorization.** A valid platform statement cannot replace an action-specific user/workload approval and purpose binding.
3. **Attestation is not custody.** Device/app/workload evidence cannot prove that the exact protocol private key is non-exportable, approved, and used with the required algorithm.
4. **Heuristics are not signed evidence.** Android heuristics, StrongBox AES storage, or a local “hardware-backed” flag are not KeyMint signing attestation and do not replace server-side certificate-chain and policy verification.
5. **Replay must be durable.** Process-local nonce caches are insufficient across restarts, replicas, or recovery; a value-bearing decision requires an atomic durable replay record.
6. **Release identity is exact.** The business submodule pin, an SDK release, upstream `main`, and an open PR are different evidence objects. This PR does not change `.gitmodules`, the pin, or readiness language.
7. **Fail closed.** Unsupported production paths return a typed disabled/unsupported result and cannot silently fall back to a software or simulated signer.

## 7. Follow-up synchronization scope

This PR intentionally does not rewrite every stale readiness wrapper. Follow-up synchronization should reconcile this canonical record with:

- `docs/CLAIM_EVIDENCE_MATRIX.md` and its July 20 authority block;
- `docs/MAINNET_READINESS_CONXIUS_ENCLAVE_SDK.md`;
- `docs/TECHNICAL_READINESS_CERTIFICATION.md`;
- `docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md`;
- `docs/TRUST_AND_READINESS_VERIFICATION.md`;
- wallet readiness and signer-control documents that use StrongBox or Play Integrity language;
- the SDK `.gitmodules` branch reference and the business submodule pin, in a separate synchronization change.

Until that work is complete, this document and the dated evidence map above are the current public-safe boundary for CON-1512 research. Historical wrappers remain historical and cannot promote readiness.

## 8. Authoritative canonical sources

These sources were accessed or revalidated on **July 22, 2026**. They define standards or vendor primitives; they do not establish Conxian/Conxius production support.

| Topic | Canonical source | Use in this plan |
| --- | --- | --- |
| Android key attestation | [Android key and ID attestation](https://source.android.com/docs/security/features/keystore/attestation) | Attestation certificate, security level, key authorization, and chain-verification requirements. |
| Android KeyMint | [KeyMint implementer reference](https://source.android.com/docs/security/features/keystore/implementer-ref) | KeyMint authorization semantics and hardware-enforced characteristics. |
| WebAuthn | [W3C Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/) | Scoped user authorization, authenticator signatures, and optional attestation. |
| TPM 2.0 | [TCG TPM 2.0 Library Specification](https://trustedcomputinggroup.org/resource/tpm-library-specification/) | Quote, authorization, object, and platform-root primitives. |
| AWS Nitro and KMS | [Nitro cryptographic attestation](https://docs.aws.amazon.com/enclaves/latest/user/set-up-attestation.html) and [KMS Nitro condition keys](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-nitro-enclave.html) | Measurement-bound attestation and KMS release-policy semantics. |
| Intel SGX/TDX DCAP | [Intel SGX attestation services](https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/attestation-services.html) and [Intel TDX documentation](https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html) | Quote generation/verification, provisioning collateral, and TCB evidence. |
| AMD SEV-SNP | [AMD Secure Encrypted Virtualization](https://www.amd.com/en/developer/sev.html) | SEV-SNP guest isolation, attestation, and versioned endorsement context. |
| Arm PSA and CCA | [Arm Platform Security](https://www.arm.com/architecture/security-features/platform-security) and [Arm Confidential Compute Architecture](https://www.arm.com/architecture/security-features/arm-confidential-compute-architecture) | Device/platform security APIs, attestation, and confidential-compute boundaries. |
| Apple App Attest and Secure Enclave | [Establishing app integrity](https://developer.apple.com/documentation/DeviceCheck/establishing-your-app-s-integrity), [validating apps](https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server), and [Secure Enclave key protection](https://developer.apple.com/documentation/Security/protecting-keys-with-the-secure-enclave) | App attestation, server-side validation, counters, and non-exportable key handling. |
| Bitcoin protocol signing | [BIP-340 Schnorr signatures](https://bips.dev/340/) and [libsecp256k1](https://github.com/bitcoin-core/secp256k1) | Exact secp256k1/Schnorr algorithm and implementation reference; not a custody proof. |

## 9. Cross-references

- [`BOS_KNOWLEDGE_GRAPH.md`](../BOS_KNOWLEDGE_GRAPH.md) — typed entities, current issue state, relationships, and split-provider decision.
- [`docs/CLAIM_EVIDENCE_MATRIX.md`](CLAIM_EVIDENCE_MATRIX.md) — public claim/evidence vocabulary and current Beta/conditional boundary.
- [`docs/ENVIRONMENT_VERIFICATION_CHECKLIST.md`](ENVIRONMENT_VERIFICATION_CHECKLIST.md) — environment-backed checks that remain outstanding.
- [`docs/architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md`](architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md) — provider-neutral identity, freshness, revocation, and fail-closed invariants.
- [`docs/CONXIUS_ENCLAVE_SDK_BOS_BUILDOUT.md`](CONXIUS_ENCLAVE_SDK_BOS_BUILDOUT.md) — supporting business-role summary; this plan is the current CON-1512 research boundary.
