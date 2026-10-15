# Corporate identity and alert routing boundaries

Status: researched policy proposal; external configuration and operational acceptance are not verified.

Reviewed: 2026-10-15. Work: [PR #1364](https://github.com/Conxian/conxian-business/pull/1364), [sprint #1390](https://github.com/Conxian/conxian-business/issues/1390). Historical context: [#943](https://github.com/Conxian/conxian-business/issues/943).

## Scope and ownership

Conxian serves universal chains, networks, layers and assets with Bitcoin L1 as its canonical trust/finality root. It introduces no native Conxian token or speculative tokenomics. External-chain and external-asset adapters remain in scope.

`conxian.org` is the public protocol and developer boundary; `conxian-labs.com` is the managed service, commercial and internal operations boundary. Repository licenses govern distribution: public visibility does not make every repository OSI open source. Domain separation documents ownership and credential boundaries; it does not itself prove legal isolation, non-custody or deployed security enforcement.

Corporate identities may authenticate authorized humans to company tools and cloud administration consoles. Workload authentication, signing authority and customer funds require independently scoped identities and evidence. A corporate email address used as an account identifier is not a runtime credential and is not evidence of a boundary violation.

## Separate identity products and responsibilities

| Surface | Intended role | Required evidence before claiming operational support |
| --- | --- | --- |
| Zoho Mail | Company correspondence and selected redacted alert delivery | Domain/alias ownership, membership, mail routing and incident handoff tests |
| Zoho Directory or another approved IdP | Human authentication and application assignment | Explicit IdP/service-provider roles, supported integration, MFA, application configuration and operator approval |
| Application provisioning | Create, disable or remove app accounts | App-specific SCIM/API capability, configured provisioning, failure handling and tested deactivation |
| Application sessions and tokens | Bound continuing access after sign-in | App-specific session expiry/revocation and personal-token/key retirement tests |
| CI and runtime workloads | Service authentication to necessary APIs only | Scoped workload identity, audience/subject policy, short lifetime, rotation/revocation and audit evidence |
| Signing providers | Exact authorized cryptographic operation | Qualified provider/device, key/policy binding and independent acceptance; an SSO login grants no signing authority |

Zoho Mail's SAML documentation describes Mail consuming assertions from a configured identity provider. Mail ownership alone does not establish that Zoho Directory is deployed or that it authenticates GitHub, Plane, Outline or any other application. Each application needs its own supported federation configuration.

## Offboarding is an application-specific workflow

Zoho explicitly documents that Directory deactivation does not propagate to assigned SAML applications by itself. Zoho's provisioning documentation separately describes app lifecycle management through supported SCIM or management APIs. These are different controls.

The proposed offboarding workflow is:

1. Disable the human identity and revoke IdP sessions using the configured provider's controls.
2. Disable application assignments and accounts through a qualified SCIM/API integration or an accountable manual step.
3. Revoke application sessions, personal API tokens, recovery access and delegated grants according to each application's capabilities.
4. Transfer owned resources and remove unnecessary cloud/GitHub permissions without deleting shared workload identities.
5. Test fresh and existing sessions, record completion or failures, and escalate incomplete revocation.

No instantaneous cascade or universal session invalidation is claimed. The operator must define and measure the maximum revocation delay per application. Account deactivation alone is not proof that an existing session or token has stopped working.

## Alert delivery policy

The following role aliases are proposed destinations. Their existence, memberships, delivery and encryption configuration are not verified by this PR.

| Alias | Proposed use | Content boundary |
| --- | --- | --- |
| `security@conxian-labs.com` | Security disclosures and vulnerability triage | Redacted event summary and access-controlled incident reference |
| `devops@conxian-labs.com` | CI, deployment and availability incidents | Service/event identifiers and triage references; no credentials or raw sensitive logs |
| `support@conxian-labs.com` | Customer support intake | Minimum necessary support context and controlled ticket handoff |
| `info@conxian-labs.com` | General business inquiries | Public business correspondence |

For automated operational alerts, use one-way notification delivery into the triage workflow. Normal authorized human correspondence is not prohibited. Mailbox receipt, message content or an email reply must never authorize a deployment, payment, policy approval or signing operation. Validate provider webhooks independently and keep any automation credentials out of messages.

Never send private keys, recovery phrases, signing shares, credentials, full connection strings or sensitive customer payloads to email. Use redacted summaries and an access-controlled system of record for investigation. Do not claim that encrypted mail or automated DLP is configured without delivery and filtering evidence.

## Workload and public-protocol boundaries

- CI/runtime services use explicit workload identities and least-privilege authorization. Prefer qualified short-lived federation where available; do not copy a human mailbox password or OAuth session into a runner.
- Human cloud administration remains permitted through reviewed roles. Separate ordinary administration from workload credentials and use an accountable recovery process.
- Public protocol interfaces must not depend on a corporate mailbox session or an inbound email loop for correctness, finality, custody or signer authorization.
- Managed services may use their separately authenticated corporate control plane; deployment, tenant, runtime and signer permissions remain distinct.
- Hardware attestation, custody, algorithm support and threshold enforcement retain their independent SDK/device gates. Mail/SSO configuration does not establish Nitro/StrongBox qualification.

This proposal does not provision or select a new identity provider, modify any cloud permissions, configure mailboxes, rotate credentials or enable a signer.

## What repository checks establish

| Evidence | What it establishes | Additional operational acceptance |
| --- | --- | --- |
| Branch-promotion policy and negative tests | Ordinary work routes to `dev`; no special agent-to-`main` bypass | Exact-head CI, review and later promotion evidence |
| Research-ledger validation | Required fields, references and scoring-state consistency | Accountable owner, acceptance evidence and prioritization |
| Doctrine/documentation checks | The content and structural assertions actually inspected by those scripts | Current provider, deployment and identity configuration |
| Secret/contamination checks | Detection of the patterns covered by the configured scanner | Runtime mail filtering, secret-manager access controls and incident handling |
| Submodule integrity checks | Committed references satisfy the implemented repository checks | Compatibility, deployment status and independent runtime qualification |

Passing these checks does not verify a Zoho tenant, SSO session, app offboarding, mail alias, DLP policy, cloud identity or production service. Record each operational check as unverified until evidence exists.

## Acceptance before operational activation

- Record the identity provider, application, accountable operator, supported federation/provisioning method and approved role map without publishing secrets.
- Test allowed and denied sign-in, MFA/recovery, disabled-user behavior, existing-session revocation and personal-token retirement for every selected application.
- Verify role-alias membership and delivery with non-sensitive test notifications, including failure and escalation paths.
- Confirm workload authentication is independent of human mailbox sessions and privileges are limited to the declared workload.
- Preserve existing independent capability gates, universal-chain scope, Bitcoin-rooted trust and the zero-native-token boundary.
- Attach a reviewed change/rollback record before changing external configuration. This document is the design input, not the acceptance result.

## Primary research sources

Accessed 2026-10-15; these describe provider capabilities, not Conxian's tenant configuration.

- [Zoho Mail SAML authentication](https://www.zoho.com/mail/help/adminconsole/saml-authentication.html): Mail's identity-provider/service-provider relationship.
- [Zoho Directory user deactivation](https://help.zoho.com/portal/en/kb/directory/admin-guide/users-1/users/articles/deactivate-activate): deactivation and the assigned-SAML-app limitation.
- [Zoho Directory provisioning overview](https://help.zoho.com/portal/en/kb/directory/admin-guide/applications/provisioning/articles/overview-provisioning): supported SCIM/API application lifecycle management.
