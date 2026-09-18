# Conxian Service Level Agreement (SLA) — Version 1.0

| Metadata | Value |
|---|---|
| Classification | Public-safe SLA policy |
| Version | 1.0 (v1.9.5 Era) |
| Effective Date | 2026-09-18 |
| Authority | Conxian Business Operations System (BOS) |

---

## 1. Uptime Commitment

Conxian targets a **99.5% monthly uptime percentage** for managed Gateway and Nexus protocol endpoints, calculated over a calendar month excluding scheduled maintenance windows announced at least 24 hours in advance.

---

## 2. Incident Response Severities & Target Response Times

| Severity Level | Definition | Business Hours Response | Off-Hours Response |
|---|---|---|---|
| **SEV1 — Critical** | Complete service outage or data corruption affecting production gateway/settlement flows | **1 Hour** | Best Effort |
| **SEV2 — Major** | Degraded functionality or major feature impairment with no immediate workarounds | **4 Business Hours** | Next Business Day |
| **SEV3 — Moderate** | Non-critical bug or minor feature issue with viable workaround | **1 Business Day** | Next Business Day |
| **SEV4 — Minor** | Feature request, documentation clarification, or cosmetic issue | **2 Business Days** | Next Business Day |

*Business hours are defined as 09:00 to 18:00 UTC, Monday through Friday.*

---

## 3. Financial Credits & Remedy

For Version 1.0, **no financial service credits are issued**. Conxian commits to transparent incident discipline:
- Root Cause Analysis (RCA) delivered within 5 business days for all SEV1 incidents.
- Public post-mortem published to `docs/` repository upon request.

---

## 4. Deferred Features & Future Scaling Trigger

To maintain operational realism during early adoption, the following enterprise SLA features are explicitly deferred:
- 24/7/365 dedicated live phone or NOC monitoring.
- Enterprise ticketing system integration (Jira/PagerDuty).
- Dedicated status page infrastructure (`status.conxian.org`).

**Trigger for Deferral Removal:** Enterprise SLA features will be enabled upon onboarding **Customer #3** or signing the first dedicated Enterprise Support contract.
