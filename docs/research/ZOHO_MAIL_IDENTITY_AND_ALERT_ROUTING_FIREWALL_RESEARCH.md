# Corporate Email Identity & Alert Routing Firewall Specification

> **Document Status**: Canonical Research Specification
> **Classification**: Public-Safe / Architectural Policy
> **Date**: 2026-10-12 | Session 69
> **Authority**: [Business Issue #943](https://github.com/Conxian/conxian-business/issues/943)

---

##  EXECUTIVE SUMMARY & DOCTRINAL PRINCIPLE

The Conxian ecosystem enforces a strict architectural, security, and legal firewall separating the public open-source protocol developer surface (`conxian.org`) from the corporate governance and commercial entity surface (`conxian-labs.com`).

Corporate email systems (specifically Zoho Mail under `@conxian-labs.com`) **MUST NOT** be connected directly to runtime infrastructure, public protocol workflows, or automated deployment pipelines. Connecting corporate email directly to runtime systems or public protocol loops introduces severe security vulnerabilities, creates secret egress vector risks, violates non-custodial operating guarantees, and breaches the domain separation boundary between `conxian.org` and `conxian-labs.com`.

### Core Directive: "Don't Trust, Verify"
1. **Centralized Identity Provider (SSO) Only**: Corporate email is strictly an authentication anchor (SSO/OAuth) for human team members accessing internal operational tooling.
2. **Inbound-Only Alert Sink**: Corporate email aliases route notifications, vulnerabilities, and operational alerts into designated team channels without holding system permissions.
3. **Complete Runtime Isolation**: All service accounts, automated CI/CD runners, public protocol services, smart contracts, and cloud runtime infrastructure remain completely decoupled from corporate email accounts and credentials.

---

## 1. WHAT SHOULD BE CONNECTED TO ZOHO MAIL

Corporate Zoho Mail handles **human identity verification** and **centralized notification aggregation**.

```
                       +-----------------------------------+
                       |    Zoho Domain Directory (SSO)    |
                       |    (@conxian-labs.com Directory)   |
                       +-----------------------------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
               v                                                   v
  [ Team Authentication Anchor ]                        [ Centralized Alert Aliases ]
   • Single Sign-On (SSO / OAuth)                       (Inbound-Only Notification Routing)
   • Private Tools Access:                               • security@conxian-labs.com
     - Plane (Project Management)                         • devops@conxian-labs.com
     - Outline (Knowledge Base)                           • support@conxian-labs.com
     - Private GitHub Org                                 • info@conxian-labs.com
   • Immediate Offboarding Cascade:
     Disabling directory account
     revokes access across all tools.
```

### 1.1 Team Authentication (Identity Anchor)
- **Single Sign-On (SSO / OAuth)**: Use the Zoho Mail / Domain directory as the SAML 2.0 / OAuth 2.0 Single Sign-On source for team member logins to private operational software (e.g., Plane, Outline, private GitHub Organization).
- **Automated Revocation Cascade**: When onboarding or offboard team members, disabling their `@conxian-labs.com` user directory account instantly terminates their session and revokes access across all integrated company platforms.

### 1.2 Centralized Alert Aliases (Inbound-Only)
Infrastructure and platform notifications must route into dedicated, role-based inbound email aliases rather than individual personal inboxes:

| Email Alias | Purpose & Source Routing | Inbound Policy |
|---|---|---|
| `security@conxian-labs.com` | Gitleaks, GitHub vulnerability alerts, security disclosures, and CVE triage routing | Inbound-only, encrypted triage, PGP/S-MIME supported |
| `devops@conxian-labs.com` | Build failures, Render deployment status, Supabase/Neon database alerts, and uptime checks | Inbound-only, automated triage to internal monitoring channels |
| `support@conxian-labs.com` | External customer support, managed gateway inquiries, and client SLA ticket ingestion | Inbound ticket ingestion into B2B support desk |
| `info@conxian-labs.com` | General corporate, partnership, and enterprise B2B inquiries | Inbound marketing/sales triage |

---

## 2. WHAT MUST BE KEPT ISOLATED FROM ZOHO MAIL

Corporate email systems **MUST NEVER** intersect with runtime credentials, automated service logic, or protocol execution boundaries.

```
       [ Public Protocol & Cloud Runtime Surface ]
  ┌─────────────────────────────────────────────────────────┐
  │  • Multi-Cloud: Render / Supabase / Neon PostgreSQL     │
  │  • Protocol Stack: `conxian-gateway`, `conxian-nexus`   │
  │  • Hardware Enclave Attestations (AWS Nitro / StrongBox)│
  │  • Fusion JWTs & Sentinel Secret Filtering              │
  └─────────────────────────────────────────────────────────┘
                                ▲
                                │ STRICT ISOLATION FIREWALL
                                │ (Zero Secret Egress Boundary)
                                ▼
  ┌─────────────────────────────────────────────────────────┐
  │  • Corporate Email Directory (Zoho Mail)                 │
  │  • Human Personal Inboxes                               │
  │  • Private Team Communication Channels                  │
  └─────────────────────────────────────────────────────────┘
```

### 2.1 Service Accounts & Automation Isolation
- **Dedicated System Service Accounts**: API keys, database connection strings, cloud endpoints, and deployment automation scripts must never be tied to personal employee email addresses or human user accounts.
- **Bot Accounts**: System-level automation uses dedicated service accounts (e.g., `bot@conxian-labs.com` or `admin-conxian-labs` GitHub machine user) with least-privilege scoped permissions.
- **Key Storage**: Production API keys and secrets reside in hardware-attested secret managers (AWS Nitro KMS, Neon secret store) and are never transmitted via email loops.

### 2.2 Public Protocol & Public GitHub Surface (`conxian.org`)
- **Protocol Decoupling**: Public repositories (`conxian-gateway`, `conxian-nexus`, `conxian_market`), smart contracts, and decentralized services must never depend on or expose corporate Zoho Mail credentials or internal email loops.
- **Non-Custodial Cryptographic Authentication**: All backend authentication uses hardware enclave attestations, API JWTs (Fusion Auth), or secret filters (Sentinel).
- **Public Domain Separation**: Protocol surfaces on `conxian.org` operate independently of corporate governance infrastructure on `conxian-labs.com`.

### 2.3 Zero Secret Egress Boundary
- **Non-Custodial Posture**: To maintain a strict non-custodial operating posture, no runtime data, user secrets, private keys, database connection strings, or operational logs may ever flow into corporate email streams.
- **Automated DLP & Filtering**: Pre-commit hooks, Sentinel scanners, and Gitleaks rules actively block email-based key transmission and prevent credential leakage.

---

## 3. RECOMMENDED ARCHITECTURE TOPOLOGY

```
[ Team Members ] ──────────► [ Zoho Domain SSO ] ──────────► [ Private Tools: Plane / Outline / Private GitHub ]
                                                                      │
                                                                      │ (Isolated Operations)
                                                                      ▼
[ Public Ecosystem ] ──────► [ Gateway / Fusion Auth ] ───► [ Multi-Cloud: Render / Supabase / Neon ]
```

---

## 4. VERIFICATION & ENFORCEMENT ("DON'T TRUST, VERIFY")

To ensure strict compliance with this firewall specification, automated verification guardrails enforce the following checks across the repository:

1. **Static Secret Scanning**: `gitleaks` and `scripts/verify_contamination_guard.py` run on every PR to verify no corporate email credentials or secret keys are committed.
2. **Doctrine Alignment**: `scripts/verify_doctrine_alignment.py` enforces domain separation rules (`conxian.org` vs `conxian-labs.com`) and validates that public protocol docs contain no corporate credential dependencies.
3. **Submodule Integrity**: `scripts/verify_submodule_integrity.py` ensures that all 8 core submodules (`conxian-gateway`, `conxian-nexus`, `conxius-wallet`, `conxius-platform`, `conxian-labs-site`, `conxius-enclave-sdk`, `lib-conxian-core`, `conxian_market`) remain pinned to parent release commits without external configuration drift.

---

## 5. SUMMARY OF BENEFITS

- **Minimal Software Costs**: Reusing Zoho Mail solely for SSO and inbound alert routing keeps enterprise SaaS license fees predictable and low.
- **Clean Security Boundaries**: Decoupling runtime execution from human email accounts eliminates email-based credential compromise vectors for production infrastructure.
- **Non-Custodial Integrity**: Zero secret egress guarantees that private corporate communication channels remain completely segregated from the public open-source stack.
