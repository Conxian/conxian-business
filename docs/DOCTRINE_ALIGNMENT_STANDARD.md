# Doctrine Alignment Standard

> **Classification:** Canonical · Public-safe
> **Operating label:** Production intent
> **Maturity / claim state:** Implemented as a documentation policy; implementation and readiness claims still require evidence.
> **Last aligned:** 2026-07-22

This is the short, public-safe doctrine source for Conxian-Labs portfolio documentation. It defines role boundaries and vocabulary; it does not replace technical specifications, contract code, evidence records, or internal strategy.

## 1. Identity and role boundaries

- **Conxian-Labs (Pty) Ltd** is the legal builder/operator company and the non-custodial software and infrastructure builder/operator. “Operator” means maintaining software, routing, orchestration, integrations, and verification services; it does not mean discretionary asset management or market participation.
- Conxian-Labs is not a market participant, proprietary trading operation, fund manager, or user-data extraction business.
- Public material must describe the company as providing infrastructure, integrations, and developer/client software. It must not imply that the company takes custody of user assets, controls protocol funds at its discretion, or monetizes raw user data.

## 2. Brand and system boundaries

- **Conxian** is the protocol and DAO layer: contracts, protocol rules, state, verification, and governance interfaces.
- **Conxius** is the client, access, and developer-tooling layer: wallet, platform, deployment tooling, and enclave abstractions.
- Internal strategy, legal material, operating procedures, privileged infrastructure details, and sensitive commercial analysis remain separate from public-safe repository documentation and are maintained in the authorized Linear workspace under Zero Secret Egress (ZSE).

## 3. Canonical taxonomy crosswalk

The following crosswalk is normative. It preserves useful historical product-domain labels without allowing those labels to redefine the legal entity or the two canonical brand layers.

| Name | Canonical classification | Scope | Boundary |
| --- | --- | --- | --- |
| **Conxian-Labs (Pty) Ltd** | Legal builder/operator company | Builds and operates non-custodial software and infrastructure. | Not a custodian, discretionary fund manager, market participant, or user-data extraction business. |
| **Conxian** | Protocol and enterprise-infrastructure brand/layer | Protocol contracts, enterprise integration, state/proof infrastructure, compliance integration, and governance interfaces. | A brand/layer, not a separate legal custodian or fund controller. |
| **Conxius** | Client/access/developer-tooling brand/layer | Wallet, client access, local platform orchestration, deployment tooling, and enclave SDK surfaces. | A brand/layer, not a separate legal entity or custodian; users retain control of their keys. |
| **CSF / Conxian Finance Protocol** | Protocol/infrastructure product domain; legacy taxonomy | Contract, asset, fee, and protocol-state domain under the Conxian layer. | Not a standalone legal entity, custodian, or ambiguous business boundary. |
| **Fusion** | Enterprise integration/infrastructure product domain; legacy taxonomy | Gateway, compliance, and cross-layer integration domain under the Conxian layer. | Not a standalone legal entity, custodian, or independent authority over funds. |
| **Nexus** | State/proof/telemetry infrastructure product domain; legacy taxonomy | State projection, synchronization, proof, and telemetry services. | Not a standalone legal entity, custodian, or discretionary treasury authority. |

CSF, Fusion, and Nexus may remain useful operating labels in technical maps, but they must be described as product domains or legacy taxonomy. Canonical entity and brand boundaries are **Conxian-Labs**, **Conxian**, and **Conxius** as defined above.

## 4. Terminology and repository-slug policy

- **Current technical artifacts use exact repository slugs in backticks:** `conxian-gateway`, `conxius-enclave-sdk`, `conxius-orbit`, and `conxian_ui`. A checkout path such as `conxian-ui/` may be shown when a filesystem path is intended; the repository identity remains `conxian_ui`.
- Use those exact slugs when the product or repository identity is intended. Prose may use a neutral functional description such as “gateway middleware” only when no product identity is being asserted.
- Historical or deprecated names may appear only when they are explicitly marked as historical/deprecated or occur inside a preserved URL, issue identifier, filename, or other non-display identifier.
- AGENTS.md is normative instruction text and is the narrow documented exception for legacy aliases used to explain which names are prohibited. The verifier does not treat that instruction file as public product display text.
- The only non-display historical URL allowlist is the preserved Linear issue URLs in `docs/bounties/CON-231_BOUNTY_CLASSIFICATION_2026-04-12.md`; it does not allow the aliases in headings, prose, or rendered link labels.

## 5. Infrastructure posture and Bitcoin anchor

The system role is infrastructure: routing, orchestration, compliance integration, state handling, and verification. Blockchain is treated as an internet-protocol layer anchored to Bitcoin for trust and security; this framing does not make Conxian-Labs a blockchain custodian, issuer, exchange, or market operator.

The appropriate public question is **what boundary does the software enforce and what evidence supports it?** Avoid describing the portfolio as capturing markets, extracting user data, or exercising discretionary control over participant funds.

## 6. Custody, data, and protocol-behavior boundaries

- User-controlled keys and self-custody features belong to the client/access layer and must not be described as company custody.
- A smart contract or DAO may implement **escrow, settlement, treasury, or yield behavior**. Those terms describe protocol-level state transitions, contract-held balances, or governance-defined rules; they do **not** establish Conxian-Labs custody, discretionary fund control, or market operation.
- “Treasury” means protocol/DAO or participant-defined accounting only when the document names that boundary. “Settlement” means a protocol or integration state transition. “Yield” means a contract- or policy-defined outcome, not a company promise or managed-investment service.
- Data handling is minimized to the documented integration need. The portfolio is not a user-data extraction business; public docs must not present surveillance, resale, or raw-data monetization as a product purpose.

## 7. Claim states

Every material claim should use one explicit state, separate from maturity:

| Claim state | Meaning |
| --- | --- |
| **Implemented** | Code, configuration, or a documented control exists. This does not by itself prove production enforcement. |
| **Verified** | The claim is supported by named test, environment, release, audit, or other evidence at the stated scope. |
| **Target-state** | Intended architecture, roadmap, or design; not evidence that the capability exists today. |
| **Deprecated** | No longer the current approach; retained only for migration, history, or link continuity. |

Do not convert `Implemented` into `Verified`, or `Target-state` into `Implemented`, without an evidence pointer. Maturity remains a separate taxonomy: `Incubating`, `Beta`, `Stable`, or `Deprecated`.

## 8. Operating labels

Operating labels describe how an artifact is used, not how mature it is:

- **Production intent:** intended to support a production path, subject to its gates and evidence.
- **Reference implementation:** an example, integration surface, or demonstrator; not a service-level guarantee.
- **Research/experimental:** exploratory, provisional, or evaluation-oriented work.
- **Internal only:** strategy, operations, legal, security, or other restricted material that is not a public product claim.

An artifact may be `Production intent` and `Beta`, or `Reference implementation` and `Stable`; the two dimensions must not be collapsed.

## 9. Document classifications

Use these classifications for major artifacts:

- **Canonical:** current source of truth for its named domain.
- **Supporting:** explanatory, evidentiary, or contextual material that does not override a canonical source.
- **Public-safe:** suitable for public linking within its stated scope.
- **Public-safe stub:** a minimal public pointer; the full internal source remains outside Git.
- **Internal-only:** restricted strategy, legal, security, financial, or operational material.
- **Deprecated:** superseded but retained for migration or history.
- **Archive candidate:** should be retired, rewritten, or moved after link and evidence review.

Compound classifications are allowed only when the relationship is explicit, for example `Archive candidate (rewrite required)` or `Public-safe stub (canonical in Linear)`.

## 10. Contradiction-resolution rules

1. Use the [portfolio doctrine register](./PORTFOLIO_DOCTRINE_REGISTER.md) for portfolio role, audience, operating label, maturity, and classification; the [documentation alignment index](./DOCUMENTATION_ALIGNMENT_INDEX.md) is navigation, not a competing taxonomy.
2. Use the most specific current evidence. A code path can support `Implemented`; it cannot establish `Verified` or `Stable` without the required evidence.
3. Qualify protocol nouns. Contract escrow, DAO treasury, yield logic, and settlement are not company custody or discretionary market activity.
4. Prefer the non-claim when a document mixes present evidence with roadmap language. Mark the unsupported portion `Target-state`, `Deprecated`, or `Archive candidate` rather than silently upgrading it.
5. Do not copy internal strategy, competitive analysis, user-data plans, private operations, or custody procedures into public-safe docs. Replace migrated material with a public-safe stub and a pointer to the authorized Linear source.
6. External repository changes are follow-up work unless the file is in this repository. A register entry must record the disposition instead of implying that an upstream README, whitepaper, or contract document was already fixed.

## 11. Canonical anchors

- [Trust & Proof Messaging](./TRUST_AND_PROOF_MESSAGING.md)
- [Claim vs Evidence Matrix](./CLAIM_EVIDENCE_MATRIX.md)
- [Portfolio Business-Unit Map](./PORTFOLIO_BUSINESS_UNIT_MAP.md)
- [Boundary Decision Log](./BOUNDARY_DECISION_LOG.md)
- [Technical Whitepaper Outline](./TECHNICAL_WHITEPAPER_OUTLINE.md)
- [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md)

## Maintenance

When a repository, maturity claim, or document classification changes, update the register first, then update explanatory indexes and affected public surfaces. Do not use the register to upgrade evidence; link the evidence that justifies the change.

Run `python3 scripts/verify_doctrine_alignment.py` as the standalone deterministic check for the canonical doctrine documents. It validates local Markdown fragments, exact table taxonomies, public-safe strategy stubs, the public-safe Markdown scope derived from the alignment index, and explicit custody boundaries. It excludes indexed `Internal-only` and archive-candidate sources from affirmative policy enforcement while still checking public-safe stubs.
