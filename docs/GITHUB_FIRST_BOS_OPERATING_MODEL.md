# GitHub-first BOS research-cycle operating model

| Metadata | Value |
|---|---|
| Classification | Public-safe canonical operating model |
| Status | Phase 0 authority alignment; active from 2026-07-28 |
| Owner role | BOS program steward |
| Last verified | 2026-07-28 against the linked GitHub records |
| Authority | [Business issue #943](https://github.com/Conxian/conxian-business/issues/943) |

## Scope and boundaries

This document governs repeatable, public-safe BOS research cycles: inventory,
gap mapping, comparable scoring, selection, implementation traceability,
sanitized evidence review, and refresh. GitHub Issues, pull requests, and the
authorized organization Project are the coordination surface for this scope.

It does **not** authorize product, release, security, legal, financial,
identity, custody, recovery, or production-acceptance decisions. It does not
make GitHub a restricted-record store, replace repository-specific engineering
controls, or transfer implementation ownership into `conxian-business`.

Restricted legal, financial, identity, custody, recovery, security, privileged
operational, secret, or personally identifying material must never enter Git,
GitHub issues, pull requests, Projects, attachments, or copied evidence. The
approved non-Git restricted-record successor and its accountable owner are
human-owned blockers; neither may be inferred. Public GitHub records may carry
only minimum-necessary sanitized references and non-sensitive status tokens.

## Canonical lifecycle

`inventory → gap map → score → selected initiative → implementation/evidence → review → next-cycle refresh`

One authority issue owns each cycle. Existing implementation and acceptance
trackers remain authoritative for their scope; a research cycle links to them
rather than creating a new umbrella or duplicating their content.

## Phase gates and required artifacts

| Phase | Gate | Required public-safe artifacts and links |
|---|---|---|
| Inventory | Candidate set is bounded and deduplicated. | Authority issue; owning repository; existing issue/PR/doc links; current state and verification date; explicit exclusions. |
| Gap map | Each candidate has a specific unmet control or outcome. | Verified gap statement; dependency and consumer links; restricted-record boundary; non-claims. |
| Score | Every candidate uses the same 100-point rubric. | Per-dimension score and short rationale; evidence links; uncertainty recorded as inference, not fact. |
| Selected initiative | Highest-value non-duplicative initiative is named. | Selection decision; owner repository and tracker; blockers; rejected/deferred candidate rationale. |
| Implementation/evidence | Work occurs in the owning repository. | Issue, PR, exact commit/artifact, hosted-check state, environment/hardware evidence when applicable, and sanitized rollback evidence. |
| Review | Evidence quality and claim boundaries are independently checked. | Review/acceptance tracker; reviewer or accountable role; unresolved findings; explicit distinction between merge, CI, environment proof, and acceptance. |
| Next-cycle refresh | States and scores are revalidated without erasing history. | Dated refresh; changed facts; retained prior decision; next candidate set; idempotent authority/index/graph updates. |

A phase advances only when its required artifacts exist or the authority issue
records the missing artifact as an explicit blocker. Administrative closure,
merged code, or green checks do not silently satisfy a later evidence gate.

## Reusable 100-point rubric

Use these exact dimensions for every comparable candidate:

| Dimension | Points |
|---|---:|
| Governance/risk leverage | 25 |
| Portfolio reuse/repeatability | 20 |
| Evidence/execution readiness | 15 |
| Dependency-unblocking value | 15 |
| Scope containment/non-duplication | 15 |
| Autonomous progress without owner decision | 10 |
| **Total** | **100** |

Scores prioritize work; they are not assurance levels, release gates, severity
ratings, funding approval, or production-readiness claims. Re-score only when a
linked fact changes, and retain the previous dated result for traceability.

## Evidence vocabulary

Use the following terms without collapsing their meanings:

| Term | Meaning |
|---|---|
| Verified fact | Directly observed in a canonical source at a stated date. |
| Inference | A reasoned conclusion from linked facts; label it explicitly and identify uncertainty. |
| Implementation presence | Code, configuration, documentation, or an artifact exists at an exact repository reference. It does not prove operation or acceptance. |
| Hosted-check state | The recorded GitHub check result for an exact commit/PR. It does not prove a target environment or hardware path. |
| Environment/hardware proof | Reproducible evidence from the named runtime, provider, device, or hardware boundary for an exact artifact. |
| Independent acceptance | An authorized reviewer accepts the exact artifact and capability under the owning acceptance tracker. |
| Explicit non-claim | A statement of what the available evidence does not establish. |

## Ownership and sequencing

Implementation, tests, release evidence, and acceptance live in the repository
that owns the capability. `conxian-business` holds only sanitized portfolio
coordination, comparable scoring, decisions, links, and evidence state.

The current sequence is:

1. Authority alignment — [Business #943](https://github.com/Conxian/conxian-business/issues/943).
2. Classified migration — [Business #944](https://github.com/Conxian/conxian-business/issues/944).
3. Branch and Project governance — [Business #945](https://github.com/Conxian/conxian-business/issues/945) and [organization tracker #61](https://github.com/Conxian/.github/issues/61).
4. Candidate execution in each owning repository.
5. Evidence review and the next-cycle refresh in #943 and the knowledge graph.

## Initial scorecard — 2026-07-28

| Candidate | Governance/risk leverage | Portfolio reuse/repeatability | Evidence/execution readiness | Dependency-unblocking value | Scope containment/non-duplication | Autonomous progress without owner decision | Total | Concise rationale and ownership boundary |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| [Business #943](https://github.com/Conxian/conxian-business/issues/943) | 23 | 20 | 11 | 13 | 14 | 3 | **84/100** | High governance and portfolio reuse: the public-safe authority cycle is bounded and evidence-ready, but final restricted-record and Project decisions remain human-owned. |
| Android-first attestation existing chain | 23 | 19 | 11 | 14 | 11 | 4 | **82/100** | High risk and dependency leverage, but already owned by [conxius-enclave-sdk #240](https://github.com/Conxian/conxius-enclave-sdk/issues/240) → [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241) / [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242) → [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202), with [conxius-wallet #444](https://github.com/Conxian/conxius-wallet/issues/444) as consumer; no new umbrella is created. |
| [conxian-nexus #178](https://github.com/Conxian/conxian-nexus/issues/178) | 14 | 7 | 15 | 8 | 15 | 10 | **69/100** | Fully bounded and independently executable CI remediation, with strong readiness/autonomy but lower governance, reuse, and cross-portfolio unblocking leverage. |

### Current-state corrections and non-claims

- [Business PR #956](https://github.com/Conxian/conxian-business/pull/956)
  merged on 2026-07-27, but its hosted checks included unresolved failures. It
  is implementation presence for the [#940](https://github.com/Conxian/conxian-business/issues/940)
  → [#955](https://github.com/Conxian/conxian-business/issues/955) semantic-source
  cycle, not a clean-check or production-acceptance claim.
- Repository PRs [#237](https://github.com/Conxian/conxius-enclave-sdk/pull/237),
  [#244](https://github.com/Conxian/conxius-enclave-sdk/pull/244), and
  [#249](https://github.com/Conxian/conxius-enclave-sdk/pull/249) are merged.
- Wallet PRs [#451](https://github.com/Conxian/conxius-wallet/pull/451),
  [#452](https://github.com/Conxian/conxius-wallet/pull/452), and
  [#455](https://github.com/Conxian/conxius-wallet/pull/455) are merged.
- Those merged artifacts are existing bounded implementation evidence, not
  fresh umbrella candidates. Merge or hosted-check state does not establish
  provider qualification, real-device/hardware proof, production support,
  independent acceptance, or release authorization.

## Blockers and idempotent updates

Human-owned blockers remain explicit and unguessed:

1. Approval of the non-Git restricted-record successor and identification of
   its accountable owner.
2. Organization Project authorization, name, and field/schema decisions under
   [Conxian/.github #61](https://github.com/Conxian/.github/issues/61).

When blocked, continue only public-safe work that cannot prejudge the decision;
record the blocker, decision owner role, affected gate, and safe next action.
Never create placeholder identities, Project URLs, approval states, restricted
details, or synthetic evidence.

Updates are idempotent: edit the marked authority section instead of appending
duplicates; update existing index/graph nodes rather than creating a second
research index; preserve dated facts and historical classifications; change a
score only when evidence changes; and keep one canonical link per owning
artifact. Re-running the cycle with no state change must produce no semantic
change.

## Session crystallization — 2026-07-28

| Entity | Type | Role/state | Relationships and decision |
|---|---|---|---|
| BOS program steward | Person/role | Accountable operating-model role; no individual inferred | Maintains #943, requests human decisions, and preserves public-safe boundaries. |
| `conxian-business` | Project/repository | Portfolio coordination and sanitized evidence | Owns #943/#944/#945 and links implementation in owning repositories. |
| `Conxian/.github` | Project/repository | Organization governance | #61 owns authorization/name/schema for the future organization Project. |
| `conxius-enclave-sdk` repository | Library/repository | Attestation prerequisite, provider, and acceptance ownership | #240 blocks #241/#242; all flow to #202; merged #237/#244/#249 are bounded evidence. |
| `conxius-wallet` repository | Client/repository | Consumer enforcement boundary | #444 consumes accepted evidence; merged #451/#452/#455 do not establish production acceptance. |
| `conxian-nexus` repository | Library/repository | Independent CI remediation owner | #178 remains separate from the #943 authority implementation. |
| External semantic-source control | Decision/control | Completed bounded implementation with non-clean hosted-check history | #940 selected #955; PR #956 merged, without implying clean checks or adoption/acceptance. |
| Research-cycle selection | Decision | #943 selected at 84/100 | Attestation chain retained under existing owners at 82/100; Nexus #178 retained independently at 69/100. |
| Restricted-record successor | Decision dependency | Human-owned and unresolved | Must be approved outside Git/GitHub with an accountable owner before restricted-record migration can advance. |

This crystallization is a compact navigation record. The structural portfolio
record remains [`BOS_KNOWLEDGE_GRAPH.md`](../BOS_KNOWLEDGE_GRAPH.md).
